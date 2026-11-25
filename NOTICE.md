# Source provenance

Collection layout and catalog flow follow https://github.com/microcord/plugins
at `b6e911dd5da3384f9170e3b23f7f859496b7f158` (GPL-3.0).

Imported source snapshots:

- `platformindicators`: https://github.com/mmaarij123/APlatformIndicators-Axycord
  at `419cbd392d659b722e187314dd7755586cf1af8a`.
- `emojireplace`: https://github.com/mmaarij123/emoji-replace-axycord
  at `5977e491c8c0a8ced3951ec1351609c1aeaec844`.
- `permissionsviewer`: https://github.com/mmaarij123/axycord-permissions-viewer
  at `9917d049aab5250542e69219561ffc19f17d2c4d`. The published v1.0.0 APK points to
  `e67020661e0943cb1f83337f985f0d27fc6d91cf`; the later snapshot only normalizes
  wrapper line endings and adds Git attributes, without changing plugin source.

Kotlin implementations, resources, tests, artwork tooling and module license/
provenance files are retained. Build scripts and README instructions are adapted
for this multi-module collection. Each imported plugin retains its MIT LICENSE.
Inherited template build files retain the status described in the module notices.
The wrapper is the official Gradle 9.7.0 wrapper with its Apache-2.0 license.

Catalog APKs are the original maintainer release assets, not re-signed builds of
this collection. Source links in catalog entries point to their release commits.
The separately distributed Axycord host and SDK retain AGPL-3.0-only.

## Four additional Axycord ports

- `messagelogger`: https://github.com/mmaarij123/axycord-message-logger/tree/72114fd5b53ce52006c8e6278f6925f53624d61b .
- `reviewdb`: https://github.com/mmaarij123/axycord-reviewdb/tree/b18a08945bf28595ddfcdc9e0906987b3a3c9e1a .
- `translate`: https://github.com/mmaarij123/axycord-translate/tree/7e88cd8524c8fa5cc8abb1c3f0021fdfab5ca9fe .
- `lastfm`: https://github.com/mmaarij123/axycord-lastfm/tree/57d093d52df13de00cead8547b42a8143206e3e5 .

These ports originate in the same pinned Microcord collection above and use the Axycord template. Message Logger, ReviewDB and Last.fm retain GPL-3.0; Translate retains Tyman's CC BY-NC-SA 4.0 attribution and terms. Their individual notices and licenses are also included in the release APKs.
