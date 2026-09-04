// Deploys markitdown-service to Azure Container Apps, behind an API key,
// with its container image built and hosted in a new Azure Container Registry.
//
// Usage (from packages/markitdown-service/):
//   az group create -n <resource-group> -l <location>
//   az deployment group create \
//     -g <resource-group> \
//     -f infra/main.bicep \
//     -p apiKey=<a-long-random-secret>
//
// This creates the registry and app with a placeholder image first, since the
// registry doesn't exist yet to build into. Then build and push the real
// image, and update the app to use it:
//
//   az acr build -r <acrName-from-output> -t markitdown-service:latest ..
//   az containerapp update -g <resource-group> -n <containerApp-from-output> \
//     --image <acrLoginServer-from-output>/markitdown-service:latest

@description('Azure region for all resources.')
param location string = resourceGroup().location

@description('Base name used to derive resource names.')
param baseName string = 'markitdown-service'

@secure()
@description('API key required (via the X-API-Key header) to call /convert, /convert/upload, and /mcp.')
param apiKey string

@description('Enable third-party MarkItDown plugins.')
param enablePlugins bool = false

@description('Container image to deploy. Defaults to a placeholder; update after the real image is pushed to the registry created here.')
param containerImage string = 'mcr.microsoft.com/k8se/quickstart:latest'

@description('Minimum number of replicas. 0 allows scale-to-zero (adds cold-start latency).')
param minReplicas int = 0

@description('Maximum number of replicas.')
param maxReplicas int = 3

@description('vCPU allocated per replica.')
param cpu string = '0.5'

@description('Memory allocated per replica.')
param memory string = '1.0Gi'

var uniqueSuffix = uniqueString(resourceGroup().id)
var acrName = toLower(replace('${baseName}${uniqueSuffix}', '-', ''))
var logAnalyticsName = '${baseName}-logs'
var envName = '${baseName}-env'
var containerAppName = baseName

resource acr 'Microsoft.ContainerRegistry/registries@2023-07-01' = {
  name: acrName
  location: location
  sku: {
    name: 'Basic'
  }
  properties: {
    adminUserEnabled: false
  }
}

resource logAnalytics 'Microsoft.OperationalInsights/workspaces@2022-10-01' = {
  name: logAnalyticsName
  location: location
  properties: {
    sku: {
      name: 'PerGB2018'
    }
    retentionInDays: 30
  }
}

resource containerAppEnv 'Microsoft.App/managedEnvironments@2023-05-01' = {
  name: envName
  location: location
  properties: {
    appLogsConfiguration: {
      destination: 'log-analytics'
      logAnalyticsConfiguration: {
        customerId: logAnalytics.properties.customerId
        sharedKey: logAnalytics.listKeys().primarySharedKey
      }
    }
  }
}

resource containerApp 'Microsoft.App/containerApps@2023-05-01' = {
  name: containerAppName
  location: location
  identity: {
    type: 'SystemAssigned'
  }
  properties: {
    managedEnvironmentId: containerAppEnv.id
    configuration: {
      ingress: {
        external: true
        targetPort: 8000
        allowInsecure: false
        transport: 'auto'
      }
      registries: [
        {
          server: acr.properties.loginServer
          identity: 'system'
        }
      ]
      secrets: [
        {
          name: 'api-key'
          value: apiKey
        }
      ]
    }
    template: {
      containers: [
        {
          name: 'markitdown-service'
          image: containerImage
          resources: {
            cpu: json(cpu)
            memory: memory
          }
          env: [
            {
              name: 'MARKITDOWN_API_KEY'
              secretRef: 'api-key'
            }
            {
              name: 'MARKITDOWN_ENABLE_PLUGINS'
              value: string(enablePlugins)
            }
          ]
          probes: [
            {
              type: 'Liveness'
              httpGet: {
                path: '/health'
                port: 8000
              }
            }
            {
              type: 'Readiness'
              httpGet: {
                path: '/health'
                port: 8000
              }
            }
          ]
        }
      ]
      scale: {
        minReplicas: minReplicas
        maxReplicas: maxReplicas
        rules: [
          {
            name: 'http-scale'
            http: {
              metadata: {
                concurrentRequests: '20'
              }
            }
          }
        ]
      }
    }
  }
}

resource acrPullRoleAssignment 'Microsoft.Authorization/roleAssignments@2022-04-01' = {
  name: guid(acr.id, containerApp.id, 'AcrPull')
  scope: acr
  properties: {
    roleDefinitionId: subscriptionResourceId(
      'Microsoft.Authorization/roleDefinitions',
      '7f951dda-4ed3-4680-a7ca-43fe172d538d' // AcrPull
    )
    principalId: containerApp.identity.principalId
    principalType: 'ServicePrincipal'
  }
}

output acrName string = acr.name
output acrLoginServer string = acr.properties.loginServer
output containerAppName string = containerApp.name
output containerAppFqdn string = containerApp.properties.configuration.ingress.fqdn
