## Technical Note: Andrew can expose sensitive data through the app's auto-generated screenshots when the app moves to the background

### Platform Guidance

**Android:** Apply `FLAG_SECURE` on every screen that can render secrets and test the recent-apps thumbnail path, not just screenshots triggered by the user.

```kotlin
class AccountActivity : AppCompatActivity() {
override fun onCreate(savedInstanceState: Bundle?) {
    super.onCreate(savedInstanceState)
    window.setFlags(
        WindowManager.LayoutParams.FLAG_SECURE,
        WindowManager.LayoutParams.FLAG_SECURE
    )
}
}
```

**iOS:** Use a privacy shield when the scene resigns active so iOS snapshots only a neutral screen while the user is in the app switcher.

```swift
final class SceneDelegate: UIResponder, UIWindowSceneDelegate {
var window: UIWindow?
private let privacyView = UIVisualEffectView(effect: UIBlurEffect(style: .systemChromeMaterial))

func sceneWillResignActive(_ scene: UIScene) {
    privacyView.frame = window?.bounds ?? .zero
    window?.addSubview(privacyView)
}

func sceneDidBecomeActive(_ scene: UIScene) {
    privacyView.removeFromSuperview()
}
}
```

### Relevant Tests

**Legacy Tests:** MASTG-TEST-0010, MASTG-TEST-0059
**New Tests:** MASTG-TEST-0250, MASTG-TEST-0293, MASTG-TEST-0356, MASTG-TEST-0276, MASTG-TEST-0333, MASTG-TEST-0377

### MASWE Weaknesses

- MASWE-0053, MASWE-0061, MASWE-0070: snapshot protection, sensitive UI lifecycle handling, and exposure of data when the app backgrounds.
