# Emoji Replace for Axycord

This folder is part of [Axycord Plugins](../README.md). From the repository root, run
`./gradlew :emojireplace:lintDebug :emojireplace:assembleDebug`. For Emoji Replace,
prepare artwork first as described in the root README. The standalone project
instructions below refer to [the original repository](https://github.com/mmaarij123/emoji-replace-axycord).

Emoji Replace lets you change how built-in emojis look in Axycord on your device. The selected style appears in chat and the emoji picker. On Android 11 and later it also applies to built-in emoji reactions.

It includes 13 offline packs (Apple, BlobMoji, Facebook, Google, Huawei, JoyPixels, Microsoft, Microsoft-3D, OpenMoji, Samsung, Samsung-Old, Toss, and WhatsApp). If a pack is missing an emoji, Axycord shows its usual artwork for that emoji.

## Install from GitHub Releases

1. Choose one of the two APKs from the [latest GitHub release](https://github.com/mmaarij123/emoji-replace-axycord/releases/latest).
2. Open the downloaded APK on your Android device and install it.
3. Open **Axycord → Settings → Plugins** and enable **Emoji Replace**. Approve the signing certificate if Axycord prompts you.

### APK versions

- **Full quality (141.7 MiB)** uses higher-resolution artwork, especially useful for large emojis in chat. [Download full-quality APK](https://github.com/mmaarij123/emoji-replace-axycord/releases/download/v1.0.0/Emoji-Replace-Axycord-1.0.0-Full.apk)
- **Compressed (49.1 MiB)** includes the same packs in a smaller download. [Download compressed APK](https://github.com/mmaarij123/emoji-replace-axycord/releases/download/v1.0.0/Emoji-Replace-Axycord-1.0.0.apk)

## Change your emoji pack

Tap the gear next to **Emoji Replace** and open **Emoji pack**. Apple is selected by default. Choose **Default (Discord)** to restore Axycord’s usual emojis.

If emojis aren’t changing, open the picker once and then tap **Check emoji replacement** in the plugin settings.

## Technical details

Emoji Replace is a native Kotlin plugin for Axycord plugin API level 3, as shipped in Axycord 1.0. Both APKs use the Android package `mmaarij.axycord.emojireplace` and replace each other when installed. The package, discovery service, and SDK follow the [Axycord plugin template](https://github.com/Axycord/Axycord-Plugin-Template).

The plugin uses Axycord’s message decorator API to replace built-in emoji images in chat and updates the native picker grid as its cells are bound. On Android 11 and later, it also uses Android’s `ResourcesLoader` to supply artwork for Axycord’s bundled emoji resources, including reactions.

### Build from source

Use JDK 21, Android SDK Platform 37 (`platforms;android-37.0`), Build Tools 36.0.0, and Python with Pillow. From the plugin repository root, fetch the pinned artwork checkout and generate the assets locally. The builder bundles the artwork as indexed WebP images. The default build uses up to 46 px per side. The full-quality build uses up to 96 px per side.

```sh
git init ../BetterDiscordAddons
git -C ../BetterDiscordAddons remote add origin https://github.com/mwittrien/BetterDiscordAddons.git
git -C ../BetterDiscordAddons config remote.origin.promisor true
git -C ../BetterDiscordAddons config remote.origin.partialclonefilter blob:none
git -C ../BetterDiscordAddons fetch --depth=1 --filter=blob:none origin 9ea61dfba5599b1c8205d261fbbe35bf683120ab
git -C ../BetterDiscordAddons sparse-checkout set Themes/EmojiReplace/emojis
git -C ../BetterDiscordAddons checkout --detach FETCH_HEAD
python -m pip install Pillow==13.0.0
python tools/build_emoji_art.py ../BetterDiscordAddons
```

For the full-quality APK, add `--full` to the artwork generation command before building. Run the Gradle `clean` task before switching between artwork qualities so the APK is rebuilt from scratch.

Run `./gradlew assembleDebug` on macOS or Linux, or `gradlew.bat assembleDebug` on Windows. The APK is built under `build/outputs/apk/debug`.

Run the picker-cell regression tests with `./gradlew testDebugUnitTest` or `gradlew.bat testDebugUnitTest`.

## License

The original Emoji Replace plugin source is available under the [MIT License](LICENSE). The [Axycord host and SDK](https://github.com/Axycord/Axycord) are distributed separately under AGPL-3.0-only. The Gradle wrapper carries its own license in its JAR.

The pack builder draws artwork from [DevilBro's EmojiReplace project](https://github.com/mwittrien/BetterDiscordAddons/tree/9ea61dfba5599b1c8205d261fbbe35bf683120ab/Themes/EmojiReplace) and converts the images to WebP. The public repository contains plugin source and the local artwork builder. Vendor artwork retains its respective terms.
