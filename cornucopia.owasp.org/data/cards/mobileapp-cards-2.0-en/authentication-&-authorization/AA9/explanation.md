## Scenario: Choi and Vandana's online romantic permission entanglement. 
 
Consider a scenario where Vandana installs an app recommended by Choi, an online flirt whom she trusts intimately. Given that the app is malicious, it can exploit other apps' components if those apps share components with entitlements or permissions set too loosely. It is not up to us to lecture Vandana on the dangers of online honeytrap scams, but we should do our best to minimize the damage if this happens.
 
### Example
 
Choi and Vandana have been chatting online on Facebook for quite some time. Choi suggests that Vandana should install a very secure messaging app where they can share more intimate details without worrying that Facebook might use that information to train its new AI. After all, who wants their love life to be food for a hungry AI that might end up copying their intimate phrases and sentences?
Vandana has not seen or met Choi in person but decides to install the app that Choi shares with a link.
 
Little does she know that this app will look for capabilities, objects, resources, or services exposed by other apps and use them to gain access to her phone and share everything with Choi. After a few days, Vandana notices that her phone bill has grown exponentially, her bank account is empty, and Choi is nowhere to be found.
 
## Threat Modeling

### STRIDE

This scenario belongs to the **Elevation of Privilege** category because Choi's app exploits vulnerabilities in permission management to gain unauthorized access to resources and data.

By bypassing intended security boundaries by exploiting loose entitlements or permissions, Choi can use the app to elevate his own permissions and reach protected components, ultimately allowing him to drain her bank account and monitor her phone.

### What can go wrong? 
 
- Custom Permission Typos: A custom permission may be declared in the manifest of one of the apps installed on Vandana's phone, but a different custom permission is used to protect exported Android components. Due to a typo, Choi's malicious application can capitalize on the misspelling by either:
  - Registering that permission first 
  - Anticipating the spelling in subsequent applications 
- Custom Orphaned Permissions: Permissions are used to guard app resources. Sometimes these permissions are not defined by a corresponding `<permission>` tag in a manifest of an APK on the device. In this case, they are called orphaned permissions. Choi's malicious app could define an orphaned permission and acquire it. If this happens, the privileged applications that trust the orphaned permission to protect a component could be compromised. In cases where the privileged app uses permissions to protect or restrict any component, this could grant the malicious app access to that component. Examples include launching activities protected by a permission, accessing a content provider, or broadcasting to a broadcast receiver protected by the orphaned permission.
- Misused android:protectionLevel: `android:protectionLevel` describes the potential risk level of a permission and indicates what procedures the system should follow when deciding whether to grant it. Using a normal or dangerous `protectionLevel` on your permissions means most apps can request and get the permission:
  - *"normal"* requires only declaring it 
  - *"dangerous"* will be approved by many users 
- Race Condition: If a legitimate app `A` defines a signature custom permission that is used by **X** other apps but is subsequently uninstalled, a malicious app `B` can define that same custom permission with a different `protectionLevel`, e.g., *normal*. In this way, `B` gains access to all components protected by that custom permission in the **X** apps without needing to be signed with the same certificate as app `A`.
The same happens if `B` gets installed before `A`. 
This is due to a privilege escalation vulnerability (CVE-2019-2200) which was fixed in Android 10. 
 
### What are we going to do about it?
 
- Verify that platform permissions are set appropriately, are narrow enough, and are enforced by the app manifest.
- Ensure that all custom permissions that the app uses to protect components are also defined in its manifest.
- Avoid using "normal" and "dangerous" `android:protectionLevel`.  
- Be aware of custom orphaned permissions. Prefer using signature permissions wherever possible to mitigate the risk of a dangling permission being used by malicious apps. You can use signature checks so that, when an app makes a request to another of your apps, the second app can verify that both apps are signed with the same certificate before complying with the request.
 
See the mapped MASTG tests for how to verify that the app is safe. Follow the mapped MASTG best practices during coding, and prepare yourself by reading through the mapped MASTG knowledge.