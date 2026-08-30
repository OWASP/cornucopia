One of the most important security principles is to ensure that a person or process only is given the minimum level of access rights (privileges) that is necessary for that person or process to complete an assigned operation. This right must be given only for the minimum amount of time that is necessary to complete the operation.
This helps to limits the damage when a system is compromised by minimising the ability of an attacker to escalate privileges both laterally and vertically. In order to apply the principle of *least privilege* proper granularity of privileges and permissions should be established.

It is vital that the application only uses the minimum number of entitlements or permissions in order to complete its functions. Therefore:

- Verify that platform permissions are appropriately set, narrow enough and enforced by the app manifest. 
- Ensure that all custom permissions that the app uses to protect components are also defined in its Manifest. 
- Avoid using "normal" and "dangerous" `android:protectionLevel`.  
- Be aware of custom orphaned permissions. Prefer using Signature Permissions wherever possible to mitigate the risk of dangling permission being used by malicious apps. You can use signature checks so when an app makes a request for another of your apps, the second app can verify that both apps are signed with the same certificate before complying with the request. 
- Determine whether the WebView should have resource access. If resource access is necessary, you need to verify that it's implemented following best practices. 
- Verify that the app mitigates the risk of sensitive data exfiltration and data tampering by preventing the user to influence how the WebView loads resources by altering the protocol, host, schema, path and name of the resource.
- limit entitlements to the minimum required for your IOS application to function. 
- Remove any unnecessary entitlements that your IOS app isn’t using.