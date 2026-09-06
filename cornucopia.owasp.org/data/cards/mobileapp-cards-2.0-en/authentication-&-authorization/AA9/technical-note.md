One of the most important security principles is to ensure that a person or process is granted only the minimum level of access rights (privileges) necessary to complete an assigned operation. These rights must be granted only for the minimum amount of time necessary to complete the operation.
This helps to limit the damage when a system is compromised by minimizing an attacker's ability to escalate privileges both laterally and vertically. In order to apply the principle of *least privilege*, the proper granularity of privileges and permissions should be established.

It is vital that the application only uses the minimum number of entitlements or permissions in order to complete its functions. Therefore:

- Verify that platform permissions are set appropriately, are narrow enough, and are enforced by the app manifest.
- Ensure that all custom permissions that the app uses to protect components are also defined in its manifest.
- Avoid using "normal" and "dangerous" `android:protectionLevel`.  
- Be aware of custom orphaned permissions. Prefer using signature permissions wherever possible to mitigate the risk of a dangling permission being used by malicious apps. You can use signature checks so that, when an app makes a request to another of your apps, the second app can verify that both apps are signed with the same certificate before complying with the request.
- Determine whether the WebView should have resource access. If resource access is necessary, you need to verify that it is implemented according to best practices.
- Verify that the app mitigates the risk of sensitive data exfiltration and data tampering by preventing users from influencing how the WebView loads resources by altering the protocol, host, schema, path, and name of the resource.
- Limit entitlements to the minimum required for your iOS application to function.
- Remove any unnecessary entitlements that your iOS app is not using.