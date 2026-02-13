Scenario: Abdullah prefers shortcuts.



Abdullah isn’t particularly fond of waiting in line — even digital ones. When the app politely asks him to follow a carefully designed login flow, he wonders why he can’t simply skip ahead.



After inspecting the mobile app traffic with a proxy tool, Abdullah discovers that protected API endpoints can still be reached if he manually crafts the right requests. Instead of completing each authentication step in order, he jumps straight to the interesting parts.



He experiments further:



\- Replaying previously captured responses  

\- Adjusting his device clock to trick time-based validations  

\- Triggering premium features before authentication fully completes  

\- Using perfectly valid features in creatively unintended ways  



To his delight, the app trusts the sequence of events rather than verifying the actual authentication state.



Abdullah never properly logged in — yet here he is, browsing privileged content.



Example



Abdullah discovers that the app first checks whether a user has completed email verification before allowing access to premium features. By intercepting traffic and manually calling the “premium-content” endpoint, he bypasses the verification process entirely. The server assumes that because the endpoint was called, the previous steps must have been completed.



Unfortunately, assumptions are not security controls.



Threat Modeling



STRIDE



The situation falls under the Elevation of Privilege category in the STRIDE threat modeling framework.



Abdullah gains access to functionality that requires authentication by manipulating application logic and workflow, effectively increasing his privileges without proper authorization.



What can go wrong?



If authentication state is inferred from sequence rather than explicitly validated on the server, attackers may bypass access controls by:



\- Skipping required steps in a workflow  

\- Replaying stale or captured tokens  

\- Manipulating timestamps or device state  

\- Directly calling internal APIs  



This may result in unauthorized access to sensitive data, financial transactions, or administrative functionality.



What are we going to do about it?



\- Enforce authentication and authorization checks server-side for every protected endpoint.  

\- Validate session state explicitly rather than relying on assumed workflow order.  

\- Use short-lived tokens and verify their integrity and freshness.  

\- Reject requests that depend solely on client-side logic or sequence validation.  

\- Implement proper replay protection and time validation mechanisms.



