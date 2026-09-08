# MarkItDown-Service

A combined **REST** + **MCP** HTTP service for [MarkItDown](../markitdown), meant to be deployed
as a container (e.g. Azure Container Apps) and called over the network — unlike
[markitdown-mcp](../markitdown-mcp), which is documented as local-only and unauthenticated.

It exposes:

| Route              | Auth | Purpose                                                        |
|---------------------|------|-----------------------------------------------------------------|
| `GET /health`        | none | liveness/readiness probe                                       |
| `POST /convert`      | API key | `{"uri": "https://..."}` → `{"markdown": "..."}`             |
| `POST /convert/upload` | API key | multipart file upload → `{"markdown": "..."}`               |
| `/mcp`               | API key | the same `convert_to_markdown` MCP tool as markitdown-mcp, over Streamable HTTP |

Both `/convert` and `/convert/upload` accept `?format=text` to get the raw markdown back as
`text/plain` instead of JSON — handy for piping straight to a file from the command line without
needing to unwrap a JSON response:

```bash
curl -s -X POST "http://localhost:8000/convert/upload?format=text" \
  -H "X-API-Key: dev-secret" \
  -F "file=@/path/to/document.pdf" \
  -o document.md
```

## Security notes

- Every route except `/health` requires an `X-API-Key` header matching the `MARKITDOWN_API_KEY`
  environment variable. If that variable isn't set, authenticated routes fail closed (503) rather
  than running open.
- Only `http:`, `https:`, and `data:` URIs are accepted by `/convert` and the MCP tool. `file:` is
  rejected, since it would let any caller with the API key read files from inside the container.
- This does not protect against SSRF to internal/cloud-metadata endpoints reachable from the
  container's network. If you attach the Container App to a VNet with sensitive internal services,
  restrict egress accordingly.

## Local development

```bash
pip install -e .
export MARKITDOWN_API_KEY=dev-secret
markitdown-service   # serves on 0.0.0.0:8000
```

```bash
curl -s http://localhost:8000/health

curl -s -X POST http://localhost:8000/convert \
  -H "X-API-Key: dev-secret" \
  -H "Content-Type: application/json" \
  -d '{"uri": "https://example.com"}'

curl -s -X POST http://localhost:8000/convert/upload \
  -H "X-API-Key: dev-secret" \
  -F "file=@/path/to/document.pdf"
```

## Docker

```bash
docker build -t markitdown-service:latest .
docker run --rm -p 8000:8000 -e MARKITDOWN_API_KEY=dev-secret markitdown-service:latest
```

## Deploy to Azure Container Apps

The [infra/main.bicep](infra/main.bicep) template provisions an Azure Container Registry, a Log
Analytics workspace, a Container Apps environment, and the Container App itself (with a
system-assigned identity granted `AcrPull` on the registry — no registry admin credentials
involved). Run these from `packages/markitdown-service/`:

```bash
# 1. Create a resource group
az group create -n markitdown-rg -l eastus

# 2. First deployment: provisions the registry with a placeholder image
#    (the real image can't be built until the registry exists).
az deployment group create \
  -g markitdown-rg \
  -f infra/main.bicep \
  -p apiKey="$(openssl rand -base64 32)"

# 3. Build the real image directly in the new registry (no local Docker needed)
ACR_NAME=$(az deployment group show -g markitdown-rg -n main --query properties.outputs.acrName.value -o tsv)
az acr build -r "$ACR_NAME" -t markitdown-service:latest ..

# 4. Point the Container App at the real image
APP_NAME=$(az deployment group show -g markitdown-rg -n main --query properties.outputs.containerAppName.value -o tsv)
ACR_LOGIN_SERVER=$(az deployment group show -g markitdown-rg -n main --query properties.outputs.acrLoginServer.value -o tsv)
az containerapp update -g markitdown-rg -n "$APP_NAME" --image "$ACR_LOGIN_SERVER/markitdown-service:latest"

# 5. Call it
FQDN=$(az deployment group show -g markitdown-rg -n main --query properties.outputs.containerAppFqdn.value -o tsv)
curl -s -X POST "https://$FQDN/convert" \
  -H "X-API-Key: <the apiKey you passed in step 2>" \
  -H "Content-Type: application/json" \
  -d '{"uri": "https://example.com"}'
```

Keep the `apiKey` value somewhere safe (e.g. re-run step 2 with the same value, or store it in Key
Vault) — it's not retrievable from the deployed Container App secret afterwards.

`minReplicas` defaults to `0` (scale-to-zero, cheapest, but the first request after idle pays a
cold-start). Pass `-p minReplicas=1` to keep a replica always warm and avoid that latency at the
cost of continuous idle billing.

### Connecting an MCP client

Point any Streamable-HTTP MCP client at `https://<fqdn>/mcp`, sending the same `X-API-Key` header.
