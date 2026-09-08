# SPDX-License-Identifier: MIT
"""Static HTML for the unauthenticated GET /about landing page.

Kept as a Python string (not a loose static file) so it's guaranteed to be
included in the installed package regardless of build-backend file-selection
rules.
"""

ABOUT_HTML = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>MarkItDown Service</title>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,400;9..144,500;9..144,600;9..144,700&family=IBM+Plex+Sans:wght@400;500;600;700&family=IBM+Plex+Mono:wght@400;500;600&display=swap">
<style>
  :root{
    --paper:#EEF0F1;
    --paper-raised:#FFFFFF;
    --code-bg:#F4F5F3;
    --ink:#171B1F;
    --ink-soft:#4B535A;
    --accent:#1F5FBF;
    --accent-ink:#0E3E82;
    --accent-warm:#B9790A;
    --accent-warm-fill:#F3E3C4;
    --line:#D7DBDB;
    --shadow: 0 1px 2px rgba(23,27,31,0.06), 0 8px 24px -12px rgba(23,27,31,0.18);
  }
  @media (prefers-color-scheme: dark){
    :root:not([data-theme="light"]){
      --paper:#12161A;
      --paper-raised:#1A2024;
      --code-bg:#0E1215;
      --ink:#E7EAEC;
      --ink-soft:#9FA8AD;
      --accent:#6FA8FF;
      --accent-ink:#CFE1FF;
      --accent-warm:#E3A83B;
      --accent-warm-fill:#3A2E12;
      --line:#2A3136;
      --shadow: 0 1px 2px rgba(0,0,0,0.4), 0 12px 28px -14px rgba(0,0,0,0.6);
    }
  }
  :root[data-theme="dark"]{
    --paper:#12161A;
    --paper-raised:#1A2024;
    --code-bg:#0E1215;
    --ink:#E7EAEC;
    --ink-soft:#9FA8AD;
    --accent:#6FA8FF;
    --accent-ink:#CFE1FF;
    --accent-warm:#E3A83B;
    --accent-warm-fill:#3A2E12;
    --line:#2A3136;
    --shadow: 0 1px 2px rgba(0,0,0,0.4), 0 12px 28px -14px rgba(0,0,0,0.6);
  }

  *{ box-sizing:border-box; }
  body{
    margin:0;
    background:var(--paper);
    color:var(--ink);
    font-family:'IBM Plex Sans', -apple-system, 'Segoe UI', Roboto, sans-serif;
    line-height:1.6;
  }
  ::selection{ background:var(--accent); color:var(--paper-raised); }
  a{ color:var(--accent); text-decoration-thickness: 1.5px; text-underline-offset: 2px; }
  a:focus-visible, button:focus-visible, .navlink:focus-visible{
    outline: 2px solid var(--accent); outline-offset: 3px; border-radius:2px;
  }

  h1,h2,h3{ font-family:'Fraunces', Georgia, 'Times New Roman', serif; text-wrap:balance; margin:0; }
  .mono{ font-family:'IBM Plex Mono','SFMono-Regular',Consolas,monospace; }
  code, pre, .mono{ font-family:'IBM Plex Mono','SFMono-Regular',Consolas,monospace; }

  .wrap{ max-width: 880px; margin:0 auto; padding: 0 28px; }

  .topnav{
    position: sticky; top:0; z-index: 20;
    background: color-mix(in srgb, var(--paper) 88%, transparent);
    backdrop-filter: blur(8px);
    border-bottom: 1px solid var(--line);
  }
  .topnav-inner{
    max-width: 880px; margin:0 auto; padding: 14px 28px;
    display:flex; align-items:center; justify-content:space-between; gap: 20px;
  }
  .brand{ display:flex; align-items:baseline; gap:8px; font-family:'Fraunces',serif; font-weight:600; font-size:1.05rem; color:var(--ink); }
  .brand .dot{ color:var(--accent); }
  .navlinks{ display:flex; gap: 18px; flex-wrap: wrap; }
  .navlink{ font-size:0.86rem; color:var(--ink-soft); text-decoration:none; white-space:nowrap; }
  .navlink:hover{ color:var(--accent); }
  @media (max-width: 620px){ .navlinks{ display:none; } }

  .hero{ padding: 64px 0 40px; }
  .eyebrow{
    display:inline-flex; align-items:center; gap:8px;
    font-family:'IBM Plex Mono',monospace; font-size:0.78rem; letter-spacing:0.08em;
    text-transform:uppercase; color:var(--accent-warm);
    background: var(--accent-warm-fill); padding: 4px 10px; border-radius: 3px;
  }
  h1.title{ font-size: clamp(2.1rem, 5vw, 3.1rem); font-weight:600; margin-top:16px; line-height:1.08; }
  h1.title em{ font-style:normal; color:var(--accent); }
  .lede{ font-size:1.15rem; color:var(--ink-soft); max-width:60ch; margin-top:16px; }

  .convert-demo{
    margin-top: 44px; display:grid; grid-template-columns: 1fr auto 1fr;
    align-items:center; gap: 18px;
  }
  @media (max-width:680px){ .convert-demo{ grid-template-columns: 1fr; } .convert-demo .arrow{ transform:rotate(90deg); justify-self:center; } }

  .doc-card{
    background:var(--paper-raised); border:1px solid var(--line); border-radius:6px;
    box-shadow: var(--shadow); padding: 20px 22px; min-height: 190px;
  }
  .doc-card .tag{ font-family:'IBM Plex Mono',monospace; font-size:0.7rem; color:var(--ink-soft); letter-spacing:0.06em; text-transform:uppercase; }
  .doc-lines{ margin-top:14px; display:flex; flex-direction:column; gap:9px; }
  .doc-lines span{ display:block; height:9px; border-radius:2px; background: var(--line); }
  .doc-lines .h{ height:13px; width:55%; background: var(--ink-soft); opacity:0.55; }
  .doc-lines .w1{ width:96%; } .doc-lines .w2{ width:88%; } .doc-lines .w3{ width:70%; } .doc-lines .w4{ width:92%; }

  .md-card{ font-family:'IBM Plex Mono',monospace; font-size:0.86rem; }
  .md-card .ln{ color: var(--ink-soft); }
  .md-card .ln .mark{ color: var(--accent); font-weight:600; }
  .md-card .ln + .ln{ margin-top:10px; }

  .arrow{ display:flex; flex-direction:column; align-items:center; gap:6px; color: var(--ink-soft); }
  .arrow svg{ width:34px; height:16px; }
  .arrow .route{ font-family:'IBM Plex Mono',monospace; font-size:0.72rem; background:var(--code-bg); border:1px solid var(--line); padding:3px 7px; border-radius:4px; white-space:nowrap; }

  .stackrow{ display:flex; flex-wrap:wrap; gap:10px; margin-top:20px; }
  .badge{
    font-family:'IBM Plex Mono',monospace; font-size:0.8rem;
    border:1px solid var(--line); background:var(--paper-raised);
    padding:7px 12px; border-radius:20px; color:var(--ink);
  }
  .badge b{ color:var(--accent); font-weight:600; }

  section{ padding: 52px 0; border-top:1px solid var(--line); }
  section:first-of-type{ border-top:none; }
  .sec-eyebrow{ font-family:'IBM Plex Mono',monospace; font-size:0.78rem; letter-spacing:0.1em; text-transform:uppercase; color:var(--accent); }
  h2.sec-title{ font-size: clamp(1.5rem, 3vw, 1.9rem); font-weight:600; margin-top:8px; }
  .sec-body{ margin-top:18px; max-width:68ch; }
  .sec-body p{ margin: 0 0 14px; color:var(--ink); }
  .sec-body p.soft{ color:var(--ink-soft); }

  .tbl-wrap{ overflow-x:auto; margin-top:18px; border:1px solid var(--line); border-radius:6px; }
  table{ border-collapse:collapse; width:100%; min-width: 560px; background:var(--paper-raised); }
  th,td{ text-align:left; padding:11px 14px; border-bottom:1px solid var(--line); font-size:0.92rem; vertical-align:top; }
  th{ font-family:'IBM Plex Mono',monospace; font-size:0.72rem; letter-spacing:0.05em; text-transform:uppercase; color:var(--ink-soft); background:var(--code-bg); }
  tr:last-child td{ border-bottom:none; }
  td .mono, td code{ background:var(--code-bg); padding:1px 5px; border-radius:3px; font-size:0.85em; }
  .authtag{ font-family:'IBM Plex Mono',monospace; font-size:0.74rem; padding:2px 7px; border-radius:10px; }
  .authtag.key{ background:var(--accent-warm-fill); color:var(--accent-warm); }
  .authtag.none{ background:var(--code-bg); color:var(--ink-soft); }

  ul.plain{ list-style:none; margin:0; padding:0; display:flex; flex-direction:column; gap:12px; }
  ul.plain li{ padding-left:20px; position:relative; color:var(--ink); }
  ul.plain li::before{ content:"—"; position:absolute; left:0; color:var(--accent); }

  pre{
    background:var(--code-bg); border:1px solid var(--line); border-radius:6px;
    padding:16px 18px; overflow-x:auto; font-size:0.86rem; margin: 14px 0;
    line-height:1.55;
  }
  pre .prompt{ color:var(--accent); }
  pre .comment{ color:var(--ink-soft); }
  code.inline{ background:var(--code-bg); border:1px solid var(--line); padding:1px 6px; border-radius:4px; font-size:0.88em; }

  .callout{
    border-left:3px solid var(--accent-warm); background:var(--accent-warm-fill);
    border-radius: 0 6px 6px 0; padding:14px 16px; margin-top:16px; font-size:0.92rem;
  }
  .callout b{ color:var(--accent-warm); }

  .steps{ display:flex; flex-direction:column; gap:26px; margin-top:22px; }
  .step{ display:grid; grid-template-columns: 44px 1fr; gap:16px; }
  .step .num{ font-family:'Fraunces',serif; font-size:1.7rem; font-weight:600; color:var(--accent); line-height:1.2; }
  .step h3{ font-size:1rem; font-weight:600; }
  .step p{ margin:6px 0 0; color:var(--ink-soft); font-size:0.92rem; }

  footer{ padding: 44px 0 60px; }
  footer p{ color:var(--ink-soft); font-size:0.86rem; max-width:60ch; }

  @media (prefers-reduced-motion: no-preference){
    .fade-up{ animation: fadeUp 0.5s ease-out both; }
    .fade-up.d1{ animation-delay: .05s; }
    .fade-up.d2{ animation-delay: .12s; }
    @keyframes fadeUp{ from{ opacity:0; transform: translateY(8px);} to{opacity:1; transform:none;} }
  }
</style>
</head>
<body>

<nav class="topnav">
  <div class="topnav-inner">
    <div class="brand"><span class="dot">#</span> markitdown<span style="color:var(--ink-soft)">-service</span></div>
    <div class="navlinks">
      <a class="navlink" href="#stack">Stack</a>
      <a class="navlink" href="#architecture">Architecture</a>
      <a class="navlink" href="#security">Security</a>
      <a class="navlink" href="#docker">Docker</a>
      <a class="navlink" href="#deploy">Deploy</a>
      <a class="navlink" href="#usage">Usage</a>
    </div>
  </div>
</nav>

<header class="hero">
  <div class="wrap">
    <span class="eyebrow fade-up">Document &rarr; Markdown, over HTTP</span>
    <h1 class="title fade-up d1">Any document in.<br><em>Clean markdown</em> out.</h1>
    <p class="lede fade-up d2">A small REST + MCP service that wraps Microsoft's <span class="mono">MarkItDown</span> library so PDFs, Office files, images and audio can be converted to Markdown from anywhere &mdash; a shell script, an agent, a CI job &mdash; not just a local Python process.</p>

    <div class="convert-demo fade-up d2">
      <div class="doc-card">
        <div class="tag">report.docx</div>
        <div class="doc-lines">
          <span class="h"></span>
          <span class="w1"></span>
          <span class="w2"></span>
          <span class="w3"></span>
          <span class="w4"></span>
          <span class="w2"></span>
        </div>
      </div>
      <div class="arrow">
        <svg viewBox="0 0 34 16" fill="none" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">
          <path d="M0 8H32" stroke="currentColor" stroke-width="1.6"/>
          <path d="M25 2L32 8L25 14" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/>
        </svg>
        <span class="route">POST /convert/upload<br>?format=text</span>
      </div>
      <div class="doc-card md-card">
        <div class="tag">report.md</div>
        <div style="margin-top:14px;">
          <div class="ln"><span class="mark">##</span> Quarterly Summary</div>
          <div class="ln"><span class="mark">**</span>Status:<span class="mark">**</span> Final</div>
          <div class="ln"><span class="mark">-</span> Revenue up 12%</div>
          <div class="ln"><span class="mark">&gt;</span> See appendix for detail.</div>
        </div>
      </div>
    </div>

    <div class="stackrow">
      <span class="badge"><b>MarkItDown</b> &mdash; conversion engine</span>
      <span class="badge"><b>FastAPI</b> &mdash; REST layer</span>
      <span class="badge"><b>MCP</b> &mdash; agent tool over Streamable HTTP</span>
      <span class="badge"><b>uvicorn</b> &mdash; ASGI server</span>
      <span class="badge"><b>Docker</b> &mdash; packaging</span>
      <span class="badge"><b>Azure Container Apps</b> &mdash; hosting</span>
    </div>
  </div>
</header>

<section id="stack">
  <div class="wrap">
    <span class="sec-eyebrow">Why this stack</span>
    <h2 class="sec-title">One ASGI app, two protocols</h2>
    <div class="sec-body">
      <p><a href="https://fastapi.tiangolo.com/">FastAPI</a> wraps <a href="https://github.com/microsoft/markitdown">MarkItDown</a>'s conversion logic in a REST API &mdash; chosen specifically because the service also needs to speak <a href="https://modelcontextprotocol.io/">MCP</a> over the same app. FastAPI and Starlette let a Streamable-HTTP MCP handler mount onto <span class="mono">/mcp</span> right alongside the REST routes, so one process serves both a plain <span class="mono">curl</span> caller and an MCP-aware agent like Claude Desktop.</p>
      <p class="soft"><span class="mono">uvicorn</span> runs the app; the console entry point reads <span class="mono">HOST</span> and <span class="mono">PORT</span> from the environment, defaulting to <span class="mono">0.0.0.0:8000</span>.</p>
    </div>
  </div>
</section>

<section id="architecture">
  <div class="wrap">
    <span class="sec-eyebrow">Routes</span>
    <h2 class="sec-title">What the service exposes</h2>
    <div class="tbl-wrap">
      <table>
        <thead><tr><th>Route</th><th>Auth</th><th>Purpose</th></tr></thead>
        <tbody>
          <tr><td class="mono">GET /health</td><td><span class="authtag none">none</span></td><td>Liveness / readiness probe</td></tr>
          <tr><td class="mono">GET /about</td><td><span class="authtag none">none</span></td><td>This page</td></tr>
          <tr><td class="mono">POST /convert</td><td><span class="authtag key">API key</span></td><td><span class="mono">{"uri": "https://..."}</span> &rarr; markdown</td></tr>
          <tr><td class="mono">POST /convert/upload</td><td><span class="authtag key">API key</span></td><td>Multipart file upload &rarr; markdown</td></tr>
          <tr><td class="mono">/mcp</td><td><span class="authtag key">API key</span></td><td><span class="mono">convert_to_markdown</span> MCP tool, Streamable HTTP</td></tr>
        </tbody>
      </table>
    </div>
    <div class="sec-body">
      <p class="soft" style="margin-top:16px;">Both convert routes accept an optional <code class="inline">?format=text</code>. Omit it and you get <code class="inline">{"markdown": "..."}</code>; add it and the response is raw markdown as <code class="inline">text/plain</code> &mdash; built specifically so a plain <span class="mono">curl ... -o file.md</span> works without a JSON-unwrapping step.</p>
    </div>
  </div>
</section>

<section id="security">
  <div class="wrap">
    <span class="sec-eyebrow">Threat model</span>
    <h2 class="sec-title">Fails closed, not open</h2>
    <div class="sec-body">
      <ul class="plain">
        <li>Every route except <span class="mono">/health</span> and <span class="mono">/about</span> requires a matching <span class="mono">X-API-Key</span> header, enforced by a pure-ASGI middleware. If <span class="mono">MARKITDOWN_API_KEY</span> isn't set on the server, authenticated routes return <span class="mono">503</span> &mdash; never silently open.</li>
        <li>Only <span class="mono">http:</span>, <span class="mono">https:</span>, and <span class="mono">data:</span> URIs are accepted. <span class="mono">file:</span> is rejected, so a caller holding the API key can't read the container's own filesystem.</li>
        <li>This does not defend against SSRF to internal or cloud-metadata endpoints reachable from the container's network &mdash; constrain egress at the network layer if that's in scope for your deployment.</li>
      </ul>
    </div>
  </div>
</section>

<section id="docker">
  <div class="wrap">
    <span class="sec-eyebrow">Packaging</span>
    <h2 class="sec-title">One image, apt pinned to a snapshot</h2>
    <div class="sec-body">
      <p>The image is <span class="mono">python:3.13-slim-bullseye</span> plus <span class="mono">ffmpeg</span> and <span class="mono">exiftool</span> &mdash; dependencies MarkItDown's audio and image-metadata converters shell out to.</p>
      <p class="soft">Bullseye is past its normal support window, so its live <span class="mono">deb.debian.org</span> repositories now serve expired <span class="mono">Release</span> files. The build pins <span class="mono">apt-get</span> to a fixed <span class="mono">snapshot.debian.org</span> mirror instead of the moving live one, so the exact package set stays reproducible.</p>
    </div>
    <pre><span class="prompt">$</span> docker build -t markitdown-service:latest .
<span class="prompt">$</span> docker run --rm -p 8000:8000 -e MARKITDOWN_API_KEY=dev-secret markitdown-service:latest</pre>
  </div>
</section>

<section id="deploy">
  <div class="wrap">
    <span class="sec-eyebrow">Hosting</span>
    <h2 class="sec-title">Deploy to Azure Container Apps</h2>
    <div class="sec-body">
      <p class="soft">The repo ships a Bicep template (<span class="mono">infra/main.bicep</span>) that provisions a registry, a Log Analytics workspace, the Container Apps environment, and the app itself &mdash; with a system-assigned identity granted <span class="mono">AcrPull</span>, no registry admin credentials involved.</p>
    </div>
    <div class="steps">
      <div class="step">
        <span class="num">1</span>
        <div>
          <h3>Create a resource group</h3>
          <pre style="margin-top:8px;"><span class="prompt">$</span> az group create -n markitdown-rg -l eastus</pre>
        </div>
      </div>
      <div class="step">
        <span class="num">2</span>
        <div>
          <h3>Provision, with a placeholder image</h3>
          <p>The registry doesn't exist yet, so the first pass deploys infrastructure only.</p>
          <pre style="margin-top:8px;"><span class="prompt">$</span> az deployment group create \\
  -g markitdown-rg -f infra/main.bicep \\
  -p apiKey="$(openssl rand -base64 32)"</pre>
        </div>
      </div>
      <div class="step">
        <span class="num">3</span>
        <div>
          <h3>Build the real image, in the registry</h3>
          <p>No local Docker required &mdash; the build runs inside ACR.</p>
          <pre style="margin-top:8px;"><span class="prompt">$</span> ACR_NAME=$(az deployment group show -g markitdown-rg -n main \\
  --query properties.outputs.acrName.value -o tsv)
<span class="prompt">$</span> az acr build -r "$ACR_NAME" -t markitdown-service:latest ..</pre>
        </div>
      </div>
      <div class="step">
        <span class="num">4</span>
        <div>
          <h3>Point the app at the real image</h3>
          <pre style="margin-top:8px;"><span class="prompt">$</span> APP_NAME=$(az deployment group show -g markitdown-rg -n main \\
  --query properties.outputs.containerAppName.value -o tsv)
<span class="prompt">$</span> az containerapp update -g markitdown-rg -n "$APP_NAME" \\
  --image "$ACR_LOGIN_SERVER/markitdown-service:latest"</pre>
        </div>
      </div>
      <div class="step">
        <span class="num">5</span>
        <div>
          <h3>Call it</h3>
          <pre style="margin-top:8px;"><span class="prompt">$</span> FQDN=$(az deployment group show -g markitdown-rg -n main \\
  --query properties.outputs.containerAppFqdn.value -o tsv)
<span class="prompt">$</span> curl -s -X POST "https://$FQDN/convert" \\
  -H "X-API-Key: &lt;the apiKey from step 2&gt;" \\
  -H "Content-Type: application/json" \\
  -d '{"uri": "https://example.com"}'</pre>
        </div>
      </div>
    </div>
    <div class="callout"><b>Free grant:</b> Container Apps includes an ongoing monthly allowance &mdash; roughly 180,000 vCPU-seconds, 360,000 GiB-seconds, and 2 million requests. With <span class="mono">minReplicas=0</span> (the Bicep default) the app scales to zero when idle, so a low-traffic service can run for effectively nothing. The tradeoff: the first request after idle pays a cold-start.</div>
  </div>
</section>

<section id="usage">
  <div class="wrap">
    <span class="sec-eyebrow">From the terminal</span>
    <h2 class="sec-title">Command-line usage</h2>
    <div class="sec-body">
      <p class="soft">Every example below assumes <span class="mono">$FQDN</span> is your deployed Container App hostname and <span class="mono">$API_KEY</span> the value you passed as <span class="mono">apiKey</span> in step 2.</p>
    </div>

    <h3 style="font-size:1rem; margin-top:28px;">Health check</h3>
    <pre><span class="prompt">$</span> curl -s https://$FQDN/health</pre>

    <h3 style="font-size:1rem; margin-top:20px;">Convert a URL</h3>
    <pre><span class="prompt">$</span> curl -s -X POST https://$FQDN/convert \\
  -H "X-API-Key: $API_KEY" \\
  -H "Content-Type: application/json" \\
  -d '{"uri": "https://example.com"}'</pre>

    <h3 style="font-size:1rem; margin-top:20px;">Convert an upload, straight to a file</h3>
    <pre><span class="prompt">$</span> curl -s -X POST "https://$FQDN/convert/upload?format=text" \\
  -H "X-API-Key: $API_KEY" \\
  -F "file=@/path/to/document.pdf" \\
  -o document.md</pre>

    <h3 style="font-size:1rem; margin-top:20px;">As an MCP tool</h3>
    <p class="sec-body" style="margin-top:8px;">Point any Streamable-HTTP MCP client at <span class="mono">https://$FQDN/mcp</span>, sending the same <span class="mono">X-API-Key</span> header, to reach the <span class="mono">convert_to_markdown</span> tool.</p>

    <div class="tbl-wrap" style="margin-top:26px;">
      <table>
        <thead><tr><th>Flag</th><th>Meaning</th></tr></thead>
        <tbody>
          <tr><td class="mono">-s</td><td>Silent &mdash; suppress the progress meter</td></tr>
          <tr><td class="mono">-X POST</td><td>HTTP method</td></tr>
          <tr><td class="mono">-H "K: v"</td><td>Add a request header (repeatable)</td></tr>
          <tr><td class="mono">-F "field=@path"</td><td>Multipart form field; <span class="mono">@path</span> reads a file's contents &mdash; used for uploads</td></tr>
          <tr><td class="mono">-d "data"</td><td>Raw request body &mdash; used for JSON requests, not uploads</td></tr>
          <tr><td class="mono">-o file</td><td>Write the response body to a file instead of stdout</td></tr>
          <tr><td class="mono">-w "fmt"</td><td>Print extra info after the response, e.g. <span class="mono">%{http_code}</span></td></tr>
        </tbody>
      </table>
    </div>
    <p class="sec-body soft" style="margin-top:14px;">Full reference: <span class="mono">curl --help all</span>, <span class="mono">man curl</span>, or <a href="https://curl.se/docs/manpage.html">curl.se/docs/manpage.html</a>.</p>
  </div>
</section>

<footer>
  <div class="wrap">
    <p><span class="mono">markitdown-service</span> is a thin, authenticated network wrapper around Microsoft's open-source <a href="https://github.com/microsoft/markitdown">MarkItDown</a> library. Source, tests, and the Bicep template live alongside it in the same repository.</p>
  </div>
</footer>

</body>
</html>
"""
