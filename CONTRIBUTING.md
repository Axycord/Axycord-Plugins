# Contributing Axycord plugins

Community plugins are welcome. You keep your plugin repository, authorship,
maintenance and declared license. The catalog displays the names in `authors`;
use the actual developers' names. Axycord's catalog maintainership does not
replace those credits or your LICENSE/NOTICE files.

## Build and publish your plugin

1. Create a repository from the [Axycord Plugin Template](https://github.com/Axycord/Axycord-Plugin-Template).
2. Choose your own unique plugin ID and Android package, for example
   `yourname.example` and `dev.yourname.axycord.example`. Update the entrypoint,
   namespace, service and binding imports to match your code. Keep the SDK's
   `mmaarij.axycord.PLUGIN` discovery action and metadata keys unchanged.
3. Add a clear README, your license, and required original-author notices for
   any adapted code or assets. Document configuration, network use and permissions.
4. Build and check compatibility using the template's Gradle workflow. Use
   Axycord's native components and active Discord font attributes
   (`font_primary_normal`, `font_primary_bold`, `font_primary_semibold`) for text,
   inputs, menus and dialogs. Plugin resource contexts need host resources when
   resolving host font IDs. Background work and registrations must clean up on stop.
5. Publish a signed APK as an asset of a versioned GitHub release. Reuse your
   signing key for future updates. Only the public certificate fingerprint belongs
   in the catalog; keep private keys, passwords and account tokens out of the PR.

## Submit a listing

Open a pull request against this repository's `main` branch, adding an entry to
[third-party.json](third-party.json). Existing entries show the complete format.
Keep other developers' entries intact.

| Field | Required value |
| --- | --- |
| `id` | The plugin ID from its Gradle DSL and APK metadata |
| `packageName` | The APK's Android application ID |
| `name`, `description` | Clear display name and description |
| `authors` | Array of the actual authors' display names |
| `versionCode`, `versionName` | Values from the published APK |
| `pluginApiMinimum` | Required Axycord plugin API level, separate from the app/SDK version |
| `apkUrl` | HTTPS GitHub release-asset URL pinned to a specific version |
| `sha256` | APK SHA-256, 64 lowercase hexadecimal characters |
| `size` | Exact APK length in bytes |
| `signerSha256` | Signing-certificate SHA-256 as lowercase hex without separators |
| `sourceUrl` | Public source link, preferably pinned to the release's exact commit |

For alternate APK variants, add a unique `variant` slug such as `compressed` or
`full`. Variants share their plugin ID, package, version and signing certificate,
and need distinct APK sizes for the client's installed-variant detection. One
variant replaces the other when installed. Ordinary plugins omit this field.

Published Axycord 1.0 accepts APKs up to **50 MiB**. The catalog and the newer
variant-capable client support up to **200 MiB**; larger entries are filtered out
by the older client. Declare the correct API level and test on supported clients.

Calculate the public values with Android Build Tools and SHA-256 tools:

```bash
apksigner verify --print-certs plugin.apk
sha256sum plugin.apk
wc -c < plugin.apk
```

On PowerShell, use `Get-FileHash plugin.apk -Algorithm SHA256` and
`(Get-Item plugin.apk).Length`. Normalize the hexadecimal values to lowercase and
remove certificate-digest colons. Replace every metadata value with your APK's
actual value.

## Review and publication

CI downloads each submitted APK and checks its byte size, SHA-256, signature,
package, version, discovery action, plugin ID and required API level. Source
modules already included in the collection are also built, linted and tested.
For a catalog-only submission, link your own source CI and relevant test results
in the PR so maintainers can assess the external source as well.

Maintainers review functionality, compatibility, author/license notices and native
UI behavior before merging. Pull-request runs verify without publishing. Merging
an accepted entry into `main` runs the publishing workflow, updates
`builds/plugins.json` and refreshes the CDN used by Browse Plugins. New repositories
and releases are submitted explicitly; GitHub is not scanned for new listings.

## Updating your listing

Increase the APK's `versionCode` and version name, publish it with the same signing
key, and submit a PR updating its pinned release URL, source commit, hash and size.
Preserve the signer fingerprint, authorship and license notices. A source-module
update should accompany the listing when your code is mirrored in this collection.

The catalog tooling's GPL license applies to that tooling. Listed plugins retain
their own declared licenses, including any upstream attribution and asset terms.
