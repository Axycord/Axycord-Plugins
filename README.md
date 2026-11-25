# Axycord Plugins

Plugin sources and the in-app Browse Plugins catalog for [Axycord](https://github.com/Axycord/Axycord),
maintained by **Maarij**. Each plugin lives in its own Gradle module, following the
layout of the Microcord plugins collection.

| Listing | Source module | Download size |
| --- | --- | --- |
| APlatformIndicators | [platformindicators](platformindicators) | 76 KiB |
| Emoji Replace (Compressed) | [emojireplace](emojireplace) | 49.1 MiB |
| Emoji Replace (Full) | [emojireplace](emojireplace) | 141.7 MiB |
| Permissions Viewer | [permissionsviewer](permissionsviewer) | 894 KiB |

Both Emoji Replace variants contain all 13 packs. Full uses higher-resolution
artwork. They share a package and signing identity, so installing one replaces the
other; they are not separate simultaneously enabled plugins.

**Published Axycord v1.0 accepts catalog APKs up to 50 MiB**, so it shows Compressed
but filters out Full. Full is listed in the catalog and can be installed manually
from its GitHub release. Both browser listings and same-version variant switching
require the client's large-download/variant-support update.

## Catalog publication

The app reads the `builds` branch through:

https://cdn.jsdelivr.net/gh/Axycord/Axycord-Plugins@builds/plugins.json

[third-party.json](third-party.json) uses the same catalog-entry format as the
upstream collection. Its four listings reference the original maintainer release
APKs. Each is pinned to a versioned URL, exact byte size, SHA-256, signing certificate,
package name, plugin ID, API level and version. No APK is re-signed for this catalog.
Emoji listings additionally carry `variant: compressed` or `variant: full`.

On pushes to `main`, [the workflow](.github/workflows/release.yml):

1. Verifies all APK bytes, signatures and Android discovery metadata.
2. Restores build-only emoji assets from the verified Compressed APK, checks source
   compilation/Android API compatibility, and runs the emoji regression tests.
3. Publishes the verified `plugins.json` to `builds` and refreshes the CDN cache.

Pull requests run verification without publishing. Publication needs no signing
secret because the APKs already carry the maintainer's original signature. Build
check APKs are not substituted for the published release files.

To publish an update, release a new APK with the **same original signing key** in
the corresponding source repository, synchronize its source module, and update
the pinned URL, version, size and SHA-256 in `third-party.json`. Keep the signer
fingerprint unchanged. Push this catalog change to `main`; the workflow verifies
it before publishing. Releases in other repositories are not imported automatically.

## Building sources

Use JDK 21, Python 3.11+, Android platform `platforms;android-37.0`, and Build Tools
36.0.0. Set `ANDROID_HOME` to your SDK directory or configure `local.properties`
for Gradle and pass `--sdk /path/to/sdk` to the verification script.

```bash
python3 -m unittest discover -s scripts -p 'test_*.py'
python3 scripts/release.py --prepare-assets
./gradlew lintDebug assembleDebug :emojireplace:testDebugUnitTest
```

On Windows, use `python` and `.\gradlew.bat`. The SDK and Gradle plugin resolve
from Axycord's public Maven branch. An optional local checkout can be selected
with `-PaxycordCheckout=/path/to/axycord` after generating its `pluginSdkJar`.

The emoji bootstrap restores only the pack and 13 index files from an APK whose
full digest and signature are verified first. These generated assets are ignored
by Git. To regenerate artwork from the pinned vendor source instead, follow
[the emoji module's build instructions](emojireplace/README.md) and its included
`tools/build_emoji_art.py` builder. Vendor artwork retains its respective terms.

## Provenance and licenses

The collection tooling is GPL-3.0-only; see [LICENSE](LICENSE). Imported plugin
implementations retain their individual MIT licenses and provenance notices.
Gradle Wrapper retains Apache-2.0. Axycord and its SDK are distributed separately
under AGPL-3.0-only. See [NOTICE.md](NOTICE.md) for the exact source snapshots.
