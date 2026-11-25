# Translate for Axycord

Collection module: from the repository root use `./gradlew :translate:lintDebug :translate:testDebugUnitTest :translate:assembleDebug`.
The standalone instructions below apply to [the personal repository](https://github.com/mmaarij123/axycord-translate).

Maintained by **Maarij**. Native Axycord port of the Microcord plugin.

## Features and use

Translate selected messages locally in the UI or send translated text with `/translate`.

- Long-press a message and choose **Translate Message**.
- **Show Original** switches the displayed message back. Editing the source invalidates its cached translation.
- Choose the target language in plugin settings.
- `/translate text [to] [from] [send]` offers searchable language choices.
- `send` defaults to **true**; set `send: false` to show the result without sending it.

The selected message or command text is sent to Google's free Translate endpoint.
It is rate limited and may change independently of this plugin. Translations are
cached only in memory, capped to 500 message records. In-flight subscriptions and
cached translations are cleared when the plugin stops.

## Install

Download **Axycord-Translate-v1.0.0.apk** from
[Releases](https://github.com/mmaarij123/axycord-translate/releases/latest), or install it through
**Axycord Settings → Plugins → Browse Plugins**. Approve installation and the
plugin signing certificate when prompted, then enable **Translate**.

Requires Android 6.0+ and Axycord plugin API level 3, available in Axycord 1.0.
Plugin ID: `axycord.translate`. Android package: `mmaarij.axycord.translate`.
Plugin version: **1.0.0**. It uses the Axycord Plugin SDK **1.0.6**; these are separate
version numbers. No companion launcher activity is needed.

## Typography

Translations decorate Axycord's existing message text view and keep its native
Discord typeface. Settings, language choices, context menus and result/error
dialogs use the host's native components. No system-font text widget is created.

## Axycord port fixes

Pending translation subscriptions are owned by the plugin and are cleared on
shutdown, preventing stale UI callbacks after disabling it.

## Build and verify

Use JDK 21, Android SDK `platforms;android-37.0` and Build Tools `36.0.0`.
Set `ANDROID_HOME` or configure `sdk.dir` in an ignored `local.properties` file.
The SDK and `mmaarij.axycord.plugin` Gradle plugin resolve from Axycord's public
Maven branch without a GitHub login.

```bash
./gradlew lintDebug testDebugUnitTest assembleDebug
```

Windows: `.\gradlew.bat lintDebug testDebugUnitTest assembleDebug`.
GitHub Actions runs the same checks and saves a debug APK as an artifact. Debug
artifacts use the runner's key and are intended for verification; published
release APKs use the maintainer's stable plugin key.

For a signed release, copy `keystore.properties.example` to `keystore.properties`,
fill in the original signing-key details and run `assembleRelease`. Release output
is under `build/outputs/apk/release/`. Keep the key private and reuse it for updates.
The signing properties and key files are ignored by Git.

To compile against a local host checkout, generate `pluginSdkJar` there and pass
`-PaxycordCheckout=/path/to/axycord`. Normal builds use the public SDK.

## Catalog updates

The [Axycord Plugins collection](https://github.com/Axycord/Axycord-Plugins) contains
the corresponding source module and a pinned release entry. For updates, increase
`versionCode` and `versionName`, release with the same key, synchronize that module,
and update the catalog URL, size and SHA-256. Catalog CI verifies the APK package,
plugin metadata and signing fingerprint before publishing.

## Verification boundary

Build/lint and offline regression checks cover the port. Live account actions,
third-party service behavior and visual rendering on a device require separate
runtime verification. The plugin never needs your Discord token in its settings.

## License and credits

CC BY-NC-SA 4.0; see [LICENSE](LICENSE) and [NOTICE.md](NOTICE.md). Original credits
are preserved there. The Axycord adaptation is maintained by Maarij.
