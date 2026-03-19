## Scenario: Andrew can expose sensitive data through the app's auto-generated screenshots when the app moves to the background

Consider a scenario where Andrew works at a busy co-working space and uses a banking app on his phone. Like most people, Andrew switches between apps frequently - checking messages, jumping on calls, and occasionally glancing at his bank balance. What Andrew does not know is that every time he presses the home button, the OS kindly takes a screenshot of whatever was on his screen and stores it as a preview thumbnail for the app switcher. It is a smooth UX feature. It is also a smooth data leak.

There are various ways Andrew's sensitive data can be exposed through these cached screenshots.

1. If Andrew's phone is left on the desk unlocked, a curious colleague can simply swipe up to the app switcher and see a pixel-perfect snapshot of Andrew's last banking screen - account number, balance and all - without ever opening the app or needing a password.

2. On a rooted Android or jailbroken iOS device, an attacker or a piece of malware can silently extract these cached screenshots from the filesystem without triggering any authentication prompt.

3. If Andrew's phone is lost or stolen, the thief does not need to break into the banking app. A quick swipe through the app switcher can reveal sensitive data from multiple apps at once.

### Example

Andrew had just checked his salary slip on his banking app when his phone buzzed with a meeting notification. He hit the home button and rushed to the conference room, leaving his phone unlocked on his desk. His colleague Priya, who had been eyeing Andrew's snack drawer for weeks, picked up his phone to borrow a charger. While doing so, she accidentally swiped into the app switcher and was greeted by a crisp screenshot of Andrew's banking screen, complete with his account balance and last three transactions. Priya now knows exactly how many snacks Andrew can afford. Andrew's dignity did not survive the standup meeting that followed.

## Threat Modeling

### STRIDE

This scenario falls under the **Information Disclosure** category in the STRIDE threat modeling framework.

Sensitive data is exposed passively through the OS screenshot caching mechanism without any active exploitation of authentication or encryption controls. The app fails to prevent the OS from capturing and storing its screen contents during the background transition, causing an unintended data leak.

### What can go wrong?

If the app does not suppress screenshots or clear sensitive UI content before moving to the background, the OS will cache a snapshot of the last visible screen. This image can be accessed through the app switcher by anyone holding an unlocked device, or extracted programmatically from storage on a rooted or jailbroken device. The exposed data could include account numbers, messages, medical records, credentials or any other sensitive information visible at the time the app was backgrounded.

### What are we going to do about it?

 - On Android, set the FLAG_SECURE window flag to prevent the OS from capturing screenshots of the app at any time, including during background transitions.
 - On iOS, add a privacy overlay view in the applicationWillResignActive lifecycle method and remove it in applicationDidBecomeActive to ensure the OS snapshot captures only a blank or branded screen.
 - Alternatively, navigate the app to a neutral or login screen before it enters the background state so that no sensitive content is visible when the snapshot is taken.
 - Test for this vulnerability explicitly during security reviews by backgrounding the app mid-session on both rooted and non-rooted devices and inspecting the app switcher preview.
