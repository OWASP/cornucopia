addEventListener("fetch", (event) => {
  event.respondWith(handleRequest(event.request));
});

function dec2hex(dec) {
  return ("0" + dec.toString(16)).substr(-2);
}

function generateNonce() {
  const arr = new Uint8Array(12);
  crypto.getRandomValues(arr);
  const values = Array.from(arr, dec2hex);
  return [
    btoa(values.slice(0, 5).join("")).substr(0, 14),
    btoa(values.slice(5).join("")),
  ].join("/");
}

/**
 * Respond to the request
 * @param {Request} request
 */
async function handleRequest(request) {
  const nonce = generateNonce();
  const originresponse = await fetch(request, {
    redirect: "manual",
  });

  const html = (await originresponse.text())
    .replace(/DhcnhD3khTMePgXw/gi, nonce)
    .replace(
      'src="https://ajax.cloudflare.com',
      `nonce="${nonce}" src="https://ajax.cloudflare.com`
    )
    .replace(
      'src="https://static.cloudflareinsights.com',
      `nonce="${nonce}" src="https://static.cloudflareinsights.com`
    )
    .replace(
      'cloudflare-static/email-decode.min.js"',
      `cloudflare-static/email-decode.min.js" nonce="${nonce}"`
    );

  const clientresponse = new Response(html, {
    status: originresponse.status,
    statusText: originresponse.statusText,
  });

  for (var [header, value] of originresponse.headers.entries()) {
    if (["via", "server"].includes(header)) {
      continue;
    }

    if (
      [
        "content-security-policy",
        "content-security-policy-report-only",
      ].includes(header)
    ) {
      // Reuse previously sent Content-Security-Policy
      if (originresponse.status === 304) continue
      value = value.replace(/DhcnhD3khTMePgXw/gi, nonce);
    }
    clientresponse.headers.set(header, value);
    clientresponse.headers.set("cf-nonce-generator", "HIT");
  }

  return clientresponse;
}
