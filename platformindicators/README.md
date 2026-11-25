# APlatformIndicators for Axycord

This folder is part of [Axycord Plugins](../README.md). From the repository root, run
`./gradlew :platformindicators:lintDebug :platformindicators:assembleDebug`. For Emoji Replace,
prepare artwork first as described in the root README. The standalone project
instructions below refer to [the original repository](https://github.com/mmaarij123/APlatformIndicators-Axycord).

See which Discord clients someone is using while reading chat or viewing their profile. Based on [Strencher’s APlatformIndicators for BetterDiscord](https://github.com/Strencher/BetterDiscordStuff/blob/master/PlatformIndicators/APlatformIndicators.plugin.js).

## What it shows

- **Chat headers** show platform icons on the message author’s line.
- **User profiles** show the icons inside Axycord’s badge pill alongside Discord badges. The pill also appears when platform icons are the only badges.
- **Platforms** include desktop, mobile, and web when Axycord has presence for the user. Your own Discord sessions can also show console and VR when reported.
- **Status colors** show online in green, idle in amber, and Do Not Disturb in red. Your own streaming activity uses purple. Offline and invisible sessions are hidden.

Both placements are enabled by default. Plugin settings let you choose which platforms appear in each placement. Bots are hidden by default.

## Install

1. Download the APK from the [latest GitHub release](https://github.com/mmaarij123/APlatformIndicators-Axycord/releases/latest).
2. Open the APK on your Android device and install it.
3. In **Axycord Settings → Plugins**, turn on **Load Plugins** if needed, then enable **APlatformIndicators**. Approve the signing certificate if Axycord prompts.

## Build from source

The plugin is written in Kotlin and compiles against Axycord Plugin SDK 1.0.6. It uses Axycord’s presence and session data and inserts indicators into the native profile badge row and chat author line. It requires Axycord plugin API level 3. [Axycord Plugin Template](https://github.com/Axycord/Axycord-Plugin-Template)

Use JDK 21, Android SDK Platform 37 (`platforms;android-37.0`), and Build Tools 36.0.0. Set `ANDROID_HOME` or point `sdk.dir` in `local.properties` to the SDK.

On Windows, run the following from the project directory.

```powershell
.\gradlew.bat lintDebug assembleDebug
```

On macOS or Linux, run `./gradlew lintDebug assembleDebug`. Gradle writes the APK to `build/outputs/apk/debug/`.

For a signed release build, copy [keystore.properties.example](keystore.properties.example) to `keystore.properties`, fill in your signing details, and run `assembleRelease`. Use the same signing key for each update you distribute.

## License

The port is released under the [MIT License](LICENSE). See the [source and dependency notices](NOTICE.md).
