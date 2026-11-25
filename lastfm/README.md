# Last.fm Rich Presence for Axycord

Collection module: from the repository root use `./gradlew :lastfm:lintDebug :lastfm:testDebugUnitTest :lastfm:assembleDebug`.
The standalone instructions below apply to [the personal repository](https://github.com/mmaarij123/axycord-lastfm).

Maintained by **Maarij**. Native Axycord port of the Microcord plugin.

## Features and use

Show the track Last.fm reports as now playing through Axycord's native rich presence.

1. Enable the plugin and enter your Last.fm username in its settings.
2. Optionally enter your own Last.fm API key; the upstream read-only application key remains available by default.
3. Choose **Listening to** or **Playing**, status text/format, optional song/profile buttons, and the refresh interval (minimum five seconds).
4. Optionally hide the activity while Spotify or another activity is shown, and import Gramophone corrections for artwork/artist names.

Track and profile links use Gramophone. Invalid, unavailable or no-longer-playing
tracks clear this plugin's presence. Disabling the plugin stops polling and clears
its activity. Your playing track is shared with Discord when this plugin is enabled;
the Last.fm API receives the configured username and API key.

## Install

Download **Axycord-Lastfm-v1.0.0.apk** from
[Releases](https://github.com/mmaarij123/axycord-lastfm/releases/latest), or install it through
**Axycord Settings → Plugins → Browse Plugins**. Approve installation and the
plugin signing certificate when prompted, then enable **Last.fm Rich Presence**.

Requires Android 6.0+ and Axycord plugin API level 3, available in Axycord 1.0.
Plugin ID: `axycord.lastfm`. Android package: `mmaarij.axycord.lastfm`.
Plugin version: **1.0.0**. It uses the Axycord Plugin SDK **1.0.6**; these are separate
version numbers. No companion launcher activity is needed.

## Typography

The activity is rendered by Axycord's native presence UI, and all settings are
rendered by the native plugin settings components. The plugin creates no custom
text widgets or system-font substitutions.

## Axycord port fixes

Polling is tied to the active scope/executor so an old request cannot schedule
work into a newly enabled instance. Activity labels use correct invisible Unicode
padding and never split a surrogate pair at the length limit. Request failures
log sanitized information rather than URLs containing a user-supplied API key.

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

GPL-3.0; see [LICENSE](LICENSE) and [NOTICE.md](NOTICE.md). Original credits
are preserved there. The Axycord adaptation is maintained by Maarij.
