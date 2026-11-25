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
| Message Logger | [messagelogger](messagelogger) | 36.3 KiB |
| ReviewDB | [reviewdb](reviewdb) | 685.3 KiB |
| Translate | [translate](translate) | 29.1 KiB |
| Last.fm Rich Presence | [lastfm](lastfm) | 34.3 KiB |

Both Emoji Replace variants contain all 13 packs. Full uses higher-resolution
artwork. They share a package and signing identity, so installing one replaces the
other; they are not separate simultaneously enabled plugins.

**Published Axycord v1.0 accepts catalog APKs up to 50 MiB**, so it shows Compressed
but filters out Full. Full is listed in the catalog and can be installed manually
from its GitHub release. Both browser listings and same-version variant switching
require the client's large-download/variant-support update.

## Community and third-party plugins

Other developers are welcome to build Axycord plugins and submit them for Browse
Plugins. Start with the [Axycord Plugin Template](https://github.com/Axycord/Axycord-Plugin-Template),
publish a signed APK in your own GitHub repository, and submit a pull request adding
its verified metadata to `third-party.json`.

Third-party listings retain their real author names, licenses and original notices.
Maarij maintains the catalog; each plugin's developers maintain their own work.
Plugins execute inside Axycord's process. Catalog CI checks APK integrity and
discovery metadata; maintainers review source and compatibility before merging.

See [CONTRIBUTING.md](CONTRIBUTING.md) for required fields, typography, licensing,
signing, updates and the publication process. A catalog-only submission can keep
its source in the author's repository; copying it into this collection is optional.

## Catalog publication

The app reads the `builds` branch through:

https://cdn.jsdelivr.net/gh/Axycord/Axycord-Plugins@builds/plugins.json

[third-party.json](third-party.json) uses the same catalog-entry format as the
upstream collection. Its eight listings reference the original maintainer release
APKs. Each is pinned to a versioned URL, exact byte size, SHA-256, signing certificate,
package name, plugin ID, API level and version. No APK is re-signed for this catalog.
Emoji listings additionally carry `variant: compressed` or `variant: full`.

On pushes to `main`, [the workflow](.github/workflows/release.yml):

1. Verifies all APK bytes, signatures and Android discovery metadata.
2. Restores build-only emoji assets from the verified Compressed APK, checks source
   compilation/Android API compatibility, and runs the source modules' regression tests, including native typography, message history and emoji behavior.
3. Publishes the verified `plugins.json` to `builds` and refreshes the CDN cache.

Pull requests run verification without publishing. Publication needs no signing
secret because the APKs already carry the maintainer's original signature. Build
check APKs are not substituted for the published release files.

To publish an update, release a new APK with the **same original signing key** in
the corresponding source repository, synchronize its source module, and update
the pinned URL, version, size and SHA-256 in `third-party.json`. Keep the signer
fingerprint unchanged. Push this catalog change to `main`; the workflow verifies
it before publishing. Releases in other repositories are not imported automatically.

## Native Discord typography

Message Logger history and every ReviewDB text view resolve the host's active
Discord font attributes, with bundled Whitney faces as the fallback. This includes
nested input fields, dynamic review rows, scores, buttons and headings. ReviewDB
vote feedback stays inline instead of using a system Toast. Translate and Last.fm
reuse native host message, settings, menu, dialog and presence views.

The four personal repositories contain full installation, configuration, privacy,
build, signing, licensing and source-provenance documentation. Their source CI
and eight port regression tests pass. Live account/provider operations and visual
rendering on a device were not exercised in this release.

## Building sources

Use JDK 21, Python 3.11+, Android platform `platforms;android-37.0`, and Build Tools
36.0.0. Set `ANDROID_HOME` to your SDK directory or configure `local.properties`
for Gradle and pass `--sdk /path/to/sdk` to the verification script.

```bash
python3 -m unittest discover -s scripts -p 'test_*.py'
python3 scripts/release.py --prepare-assets
./gradlew lintDebug assembleDebug testDebugUnitTest
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

The collection tooling is GPL-3.0-only; see [LICENSE](LICENSE). APlatformIndicators,
Emoji Replace and Permissions Viewer retain their MIT licenses. Message Logger,
ReviewDB and Last.fm retain GPL-3.0; Translate retains CC BY-NC-SA 4.0. Individual
LICENSE and NOTICE files record original credits and template-file provenance.
Gradle Wrapper retains Apache-2.0. Axycord and its SDK are distributed separately
under AGPL-3.0-only. See [NOTICE.md](NOTICE.md) for the exact source snapshots.
