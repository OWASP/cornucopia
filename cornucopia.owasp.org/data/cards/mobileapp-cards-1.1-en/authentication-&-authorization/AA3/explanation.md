### Scenario: Choi and Vandana's online romantic permission entanglement. 
 
Consider a scenario where Vandana installs an app recommended by Choi, an online flirt that she trusts intimately. Given that the app is malicious, it can exploit other apps components if these apps share components with entitlements or permissions set to loosely. It is not up to us to lecture Vandana on the dangers of online honeytrap scams, but we should do our best to minimise the damage in case it happens.
 
### Example: 
 
Choi and Vandana have been chatting online on Facebook for quite some time, Choi suggests that Vandana should install a very secure messaging app where they can share more intimate details without worrying that Facebook might use that information for training their new AI. After all, who wants their love life to be food for a hungry AI that might end up copying your intimate phrases and sentences. 
Vandana hasn't seen or met Choi physically but decides to install the app that Choi shares with a link. 
 
Little does she know that this app, in particular, will look for capabilities, objects, resources, or services exposed by other apps and use them to get access to her phone and share everything with Choi. After some days Verdana notices that her phone bill has grown exponentially, her bank account is empty, and Choi is nowhere to be found. 
 
### Risks:  
 
- Custom Permission Typos: A custom permission may be declared in the Manifest of one of the apps installed on Vandana's phone, but a different custom permission is used to protect exported Android components, due to a typo, Choi's malicious application can capitalize on the misspelling by either: 
  - Registering that permission first 
  - Anticipating the spelling in subsequent applications 
- Custom Orphaned Permissions: Permissions are used to guard resources of apps. Sometimes these permissions are not defined by a corresponding `<permission>` tag in a Manifest of an APK on the device. In this case, they are called orphaned permissions. Choi's malicious app could define an orphaned permission and acquire it. If this happens, then the privileged applications that trust the orphaned permission to protect a component could be compromised. In cases where the privileged app uses permissions to protect or restrict any component, this could grant the malicious app access to that component. Examples include launching activities protected by a permission, accessing a content provider, or broadcasting to a broadcast receiver protected by the orphaned permission. 
- Misused android:protectionLevel: `android:protectionLevel` describes the potential risk level in the permission and indicates what procedures the system should follow when deciding whether or not to grant the permission. Using a normal or dangerous `protectionLevel` on your permissions means most apps can request and get the permission: 
  - *"normal"* requires only declaring it 
  - *"dangerous"* will be approved by many users 
- Race Condition: If a legitimate app `A` defines a signature custom permission that is used by other **X** apps, but it is subsequently uninstalled, then a malicious app `B` can define that same custom permission with a different `protectionLevel`, e.g. *normal*. In this way, `B` gains access to all components protected by that custom permission in the **X** apps without any need to be signed with the same certificate as the app `A`. 
The same happens if `B` gets installed before `A`. 
This is due to a privilege escalation vulnerability (CVE-2019-2200) which was fixed in Android 10. 
 
### Mitigation: 
 
- Verify that platform permissions are appropriately set, narrow enough and enforced by the app manifest. 
- Ensure that all custom permissions that the app uses to protect components are also defined in its Manifest. 
- Avoid using "normal" and "dangerous" `android:protectionLevel`.  
- Be aware of custom orphaned permissions. Prefer using Signature Permissions wherever possible to mitigate the risk of dangling permission being used by malicious apps. You can use signature checks so when an app makes a request for another of your apps, the second app can verify that both apps are signed with the same certificate before complying with the request.
 
### References: 
 
- [Android: Custom Permissions](https://developer.android.com/privacy-and-security/risks/custom-permissions) 
