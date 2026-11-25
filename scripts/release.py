#!/usr/bin/env python3
"""Verify maintainer release APKs and publish the index consumed by Axycord."""
# SPDX-License-Identifier: GPL-3.0-only
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import urllib.request
from urllib.parse import urlparse
import zipfile

ROOT = Path(__file__).resolve().parent.parent
MAX_APK_BYTES = 200 * 1024 * 1024
PROVIDERS = ("Apple", "BlobMoji", "Facebook", "Google", "Huawei", "JoyPixels", "Microsoft",
             "Microsoft-3D", "OpenMoji", "Samsung", "Samsung-Old", "Toss", "WhatsApp")


def validate(entries):
    if not isinstance(entries, list) or not entries:
        raise ValueError("The catalog must contain plugin entries")
    keys, packages = set(), {}
    for entry in entries:
        for field in ("id", "name", "packageName", "versionName", "sourceUrl", "apkUrl"):
            if not isinstance(entry.get(field), str) or not entry[field].strip():
                raise ValueError(f"Missing {field}")
        if not re.fullmatch(r"[A-Za-z][A-Za-z0-9_]*(\.[A-Za-z][A-Za-z0-9_]*)+", entry["packageName"]):
            raise ValueError("Invalid package name")
        for field in ("sha256", "signerSha256"):
            if not re.fullmatch(r"[0-9a-f]{64}", entry.get(field, "")):
                raise ValueError(f"Invalid {field}")
        for field in ("versionCode", "pluginApiMinimum", "size"):
            if type(entry.get(field)) is not int or entry[field] <= 0:
                raise ValueError(f"Invalid {field}")
        if entry["size"] > MAX_APK_BYTES:
            raise ValueError("APK exceeds Axycord's 200 MiB limit")
        for field in ("apkUrl", "sourceUrl"):
            url = urlparse(entry[field])
            if url.scheme != "https" or not url.hostname or url.username or url.password:
                raise ValueError(f"Invalid HTTPS {field}")
        if "/releases/download/" not in entry["apkUrl"] or "/latest/" in entry["apkUrl"]:
            raise ValueError("Use a version-pinned GitHub release asset")
        variant = entry.get("variant")
        if variant is not None and not re.fullmatch(r"[a-z0-9_-]{1,32}", variant):
            raise ValueError("Invalid variant")
        key = entry["id"], variant
        if key in keys:
            raise ValueError("Duplicate catalog entry")
        keys.add(key)
        previous = packages.setdefault(entry["packageName"], [])
        for other in previous:
            if not variant or not other.get("variant") or any(
                entry[field] != other[field] for field in ("id", "versionCode", "versionName", "signerSha256")
            ) or entry["size"] == other["size"]:
                raise ValueError("Variants must share identity/version/signer and have distinguishable APK sizes")
        previous.append(entry)
    return entries


class HttpsRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        if urlparse(newurl).scheme != "https":
            raise ValueError("APK redirects must remain HTTPS")
        return super().redirect_request(req, fp, code, msg, headers, newurl)


def digest(path):
    with path.open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()


def download(entry, cache):
    cache.mkdir(parents=True, exist_ok=True)
    output = cache / (entry["sha256"] + ".apk")
    if output.exists() and output.stat().st_size == entry["size"] and digest(output) == entry["sha256"]:
        return output
    temporary = output.with_suffix(".part")
    try:
        request = urllib.request.Request(entry["apkUrl"], headers={"User-Agent": "Axycord-Plugins"})
        with urllib.request.build_opener(HttpsRedirect()).open(request, timeout=60) as response, temporary.open("wb") as stream:
            total = 0
            while chunk := response.read(64 * 1024):
                total += len(chunk)
                if total > entry["size"]:
                    raise ValueError("Downloaded APK exceeds its expected size")
                stream.write(chunk)
        if temporary.stat().st_size != entry["size"] or digest(temporary) != entry["sha256"]:
            raise ValueError("Downloaded APK size or SHA-256 mismatch")
        temporary.replace(output)
    finally:
        temporary.unlink(missing_ok=True)
    return output


def tool(command, *args):
    result = subprocess.run([str(command), *map(str, args)], check=True, capture_output=True, text=True, encoding="utf-8")
    return result.stdout


def manifest_metadata(xml):
    metadata, key = {}, None
    for line in xml.splitlines():
        if "E: " in line:
            key = None
        name = re.search(r'A: .*:name\([^)]*\)="(mmaarij\.axycord\.plugin\.[^"]+)"', line)
        if name:
            key = name[1]
        value = re.search(r'A: .*:value\([^)]*\)=(.*)', line)
        if key and value:
            raw = value[1].strip()
            metadata[key] = raw.split('"')[1] if raw.startswith('"') else raw.split()[0]
            key = None
    return metadata


def verify_apk(entry, apk, sdk):
    tools = sdk / "build-tools/36.0.0"
    aapt = tools / ("aapt2.exe" if os.name == "nt" else "aapt2")
    signer = tools / ("apksigner.bat" if os.name == "nt" else "apksigner")
    signature = tool(signer, "verify", "--print-certs", apk)
    certs = re.findall(r"^Signer #\d+ certificate SHA-256 digest: ([0-9a-f:]+)$", signature, re.MULTILINE)
    if len(certs) != 1 or certs[0].replace(":", "") != entry["signerSha256"]:
        raise ValueError("APK signing certificate does not match the catalog")
    badging = tool(aapt, "dump", "badging", apk)
    package = re.search(r"^package: name='([^']+)' versionCode='(\d+)' versionName='([^']*)'", badging, re.MULTILINE)
    if not package or (package[1], int(package[2]), package[3]) != (
        entry["packageName"], entry["versionCode"], entry["versionName"]
    ):
        raise ValueError("APK package or version does not match the catalog")
    xml = tool(aapt, "dump", "xmltree", apk, "--file", "AndroidManifest.xml")
    metadata = manifest_metadata(xml)
    prefix = "mmaarij.axycord.plugin."
    if metadata.get(prefix + "ID") != entry["id"] or int(metadata.get(prefix + "AXYCORD_VERSION_MINIMUM", "0"), 0) != entry["pluginApiMinimum"]:
        raise ValueError("APK discovery metadata does not match the catalog")
    if '="mmaarij.axycord.PLUGIN"' not in xml or not metadata.get(prefix + "ENTRYPOINT"):
        raise ValueError("APK is not discoverable by Axycord")


def prepare_artwork(apk):
    assets = ROOT / "emojireplace/src/main/assets"
    names = ["assets/emoji-art.emojipack"] + [f"assets/emoji-index/{provider}.tsv" for provider in PROVIDERS]
    with zipfile.ZipFile(apk) as archive:
        for name in names:
            info = archive.getinfo(name)
            if info.file_size > MAX_APK_BYTES:
                raise ValueError("Artwork exceeds its size limit")
            output = assets / name.removeprefix("assets/")
            output.parent.mkdir(parents=True, exist_ok=True)
            with archive.open(info) as source, output.open("wb") as target:
                while chunk := source.read(64 * 1024):
                    target.write(chunk)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("builds", nargs="?", type=Path, help="Write plugins.json to this builds-branch checkout")
    parser.add_argument("--sdk", type=Path, default=os.environ.get("ANDROID_HOME") or os.environ.get("ANDROID_SDK_ROOT"))
    parser.add_argument("--prepare-assets", action="store_true", help="Restore compressed emoji artwork from its verified APK")
    args = parser.parse_args()
    if not args.sdk:
        parser.error("Set ANDROID_HOME or pass --sdk")
    entries = validate(json.loads((ROOT / "third-party.json").read_text(encoding="utf-8")))
    for entry in entries:
        apk = download(entry, ROOT / ".catalog-cache")
        verify_apk(entry, apk, args.sdk)
        if args.prepare_assets and entry["id"] == "axycord.emojireplace" and entry.get("variant") == "compressed":
            prepare_artwork(apk)
        print("Verified:", entry["name"], entry["versionName"], entry["size"], "bytes", flush=True)
    if args.builds:
        index = json.dumps({"version": 1, "plugins": entries}, indent=2) + "\n"
        if len(index.encode()) > 256 * 1024:
            raise ValueError("Catalog exceeds the app's index size limit")
        args.builds.mkdir(parents=True, exist_ok=True)
        path = args.builds / "plugins.json"
        temporary = path.with_suffix(".tmp")
        temporary.write_text(index, encoding="utf-8", newline="\n")
        temporary.replace(path)
        print("Wrote", path, flush=True)


if __name__ == "__main__":
    main()
