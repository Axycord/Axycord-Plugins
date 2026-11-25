import copy
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

import release


class CatalogTest(unittest.TestCase):
    def setUp(self):
        self.entries = json.loads((release.ROOT / "third-party.json").read_text())

    def test_both_emoji_variants_have_the_same_plugin_identity(self):
        release.validate(self.entries)
        variants = [p for p in self.entries if p["id"] == "axycord.emojireplace"]
        self.assertEqual({"compressed", "full"}, {p["variant"] for p in variants})
        self.assertEqual(1, len({p["packageName"] for p in variants}))
        self.assertEqual(1, len({p["signerSha256"] for p in variants}))

    def test_duplicate_variant_is_rejected(self):
        self.entries.append(copy.deepcopy(self.entries[1]))
        with self.assertRaises(ValueError):
            release.validate(self.entries)

    def test_variants_cannot_change_package_identity_or_signer(self):
        self.entries[2]["signerSha256"] = "0" * 64
        with self.assertRaises(ValueError):
            release.validate(self.entries)

    def test_insecure_unpinned_and_oversized_downloads_are_rejected(self):
        for field, value in (("apkUrl", "http://example.com/x.apk"),
                             ("apkUrl", "https://github.com/example/plugin/releases/latest/download/plugin.apk"),
                             ("size", release.MAX_APK_BYTES + 1)):
            with self.subTest(field=field, value=value):
                entries = copy.deepcopy(self.entries)
                entries[0][field] = value
                with self.assertRaises(ValueError):
                    release.validate(entries)

    def test_corrupt_cached_download_is_not_trusted(self):
        entry = self.entries[0]
        with tempfile.TemporaryDirectory() as directory:
            cache = Path(directory)
            (cache / (entry["sha256"] + ".apk")).write_bytes(b"wrong APK")
            with patch("urllib.request.build_opener") as opener:
                opener.return_value.open.side_effect = OSError("offline")
                with self.assertRaises(OSError):
                    release.download(entry, cache)
                opener.assert_called_once()
            self.assertFalse((cache / (entry["sha256"] + ".part")).exists())

    def test_manifest_metadata_distinguishes_android_names_from_values(self):
        xml = '''E: meta-data
  A: android:name(0x01010003)="mmaarij.axycord.plugin.ID"
  A: android:value(0x01010024)="axycord.emojireplace"
E: meta-data
  A: android:name(0x01010003)="mmaarij.axycord.plugin.AXYCORD_VERSION_MINIMUM"
  A: android:value(0x01010024)=3
'''
        self.assertEqual({"mmaarij.axycord.plugin.ID": "axycord.emojireplace",
                          "mmaarij.axycord.plugin.AXYCORD_VERSION_MINIMUM": "3"}, release.manifest_metadata(xml))


if __name__ == "__main__":
    unittest.main()
