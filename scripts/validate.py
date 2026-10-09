#!/usr/bin/env python3
import json
import hashlib
import sys
import xml.etree.ElementTree as ET
from pathlib import Path
from urllib.parse import quote, urlparse

EXPECTED = {
    "local-government-101": 10,
    "local-officials-handbook": 14,
    "advanced-civic-planning": 36,
    "planning-commission-prep": 8,
    "public-policy-prep": 12,
    "financial-strategy-public-managers": 9,
    "census-academy": 14,
    "transportation-policies-programs-history": 10,
    "transportation-land-use-modeling": 13,
    "design-equity": 8,
    "environmental-justice-land-use-planning": 8,
}


def fail(message):
    raise SystemExit(message)


def sha256(path):
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main():
    docs = Path(sys.argv[1] if len(sys.argv) > 1 else "docs")
    home = (docs / "index.html").read_text()
    for show, expected in EXPECTED.items():
        manifest = json.loads((docs / show / "manifest.json").read_text())
        if len(manifest["episodes"]) != expected:
            fail(f"{show}: expected {expected} episodes")
        root = ET.parse(docs / show / "feed.xml").getroot()
        items = root.findall("./channel/item")
        if len(items) != expected:
            fail(f"{show}: feed has {len(items)} items")
        feed_url = manifest["stable_feed_url"]
        if feed_url not in home or quote(feed_url, safe="") not in home:
            fail(f"{show}: catalog discovery controls are incomplete")
        ios_url = f"pktc://subscribe/{feed_url}"
        if ios_url not in home:
            fail(f"{show}: catalog iOS Pocket Casts link is missing")
        show_page = (docs / show / "index.html").read_text()
        if quote(feed_url, safe="") not in show_page or ios_url not in show_page:
            fail(f"{show}: show Pocket Casts links are incomplete")
        guids = [item.findtext("guid") for item in items]
        if len(guids) != len(set(guids)):
            fail(f"{show}: duplicate GUID")
        episodes_by_guid = {
            episode["stable_guid"]: episode for episode in manifest["episodes"]
        }
        for item in items:
            guid = item.findtext("guid")
            if guid not in episodes_by_guid:
                fail(f"{show}: feed GUID is absent from manifest")
            enclosure = item.find("enclosure")
            url = enclosure.attrib["url"]
            parsed = urlparse(url)
            if parsed.netloc != "github.com" or "/releases/download/" not in parsed.path:
                fail(f"{show}: invalid enclosure {url}")
            if int(enclosure.attrib["length"]) <= 0:
                fail(f"{show}: invalid enclosure length")
            episode = episodes_by_guid[guid]
            if int(enclosure.attrib["length"]) != episode["enclosure"]["bytes"]:
                fail(f"{show}: enclosure length mismatch")
        for episode in manifest["episodes"]:
            for key, url in episode["pages"].items():
                if urlparse(url).netloc != "jstart.github.io":
                    fail(f"{show}: {key} is not hosted on Pages")
            if len(episode["enclosure"]["sha256"]) != 64:
                fail(f"{show}: invalid checksum")
            stem = Path(urlparse(episode["pages"]["canonical"]).path).stem
            episode_dir = docs / show / "episodes"
            required = {
                "canonical": episode_dir / f"{stem}.html",
                "transcript": episode_dir / f"{stem}.vtt",
                "chapters": episode_dir / f"{stem}.chapters.json",
                "notes": episode_dir / f"{stem}.md",
                "accessibility": episode_dir / f"{stem}.accessibility.json",
                "provenance": episode_dir / f"{stem}.provenance.json",
                "manifest": episode_dir / f"{stem}.manifest.json",
                "episode": episode_dir / f"{stem}.episode.json",
                "credits": episode_dir / f"{stem}.credits.json",
                "license": episode_dir / f"{stem}.license.txt",
            }
            missing = [key for key, path in required.items() if not path.is_file()]
            if missing:
                fail(f"{show}: episode {episode['episode']} missing {missing}")
            if not required["transcript"].read_bytes().startswith(b"WEBVTT"):
                fail(f"{show}: episode {episode['episode']} has invalid transcript")
            chapters = json.loads(required["chapters"].read_text())
            if not chapters.get("chapters"):
                fail(f"{show}: episode {episode['episode']} has no chapters")
            hosted = json.loads(required["manifest"].read_text())
            if hosted["stable_guid"] != episode["stable_guid"]:
                fail(f"{show}: episode {episode['episode']} GUID mismatch")
            release = json.loads(required["episode"].read_text())
            if release["guid"] != episode["stable_guid"]:
                fail(f"{show}: episode {episode['episode']} release GUID mismatch")
            if release["checksums"]["transcript_sha256"] != sha256(required["transcript"]):
                fail(f"{show}: episode {episode['episode']} transcript checksum mismatch")
            artwork = docs / show / "artwork" / f"ep{episode['episode']:02d}.jpg"
            if not artwork.is_file() or not artwork.read_bytes().startswith(b"\xff\xd8"):
                fail(f"{show}: episode {episode['episode']} artwork is invalid")
    site_js = (docs / "assets" / "site.js").read_text()
    if "[data-pocket-casts-ios]" not in site_js or "document.visibilityState" not in site_js:
        fail("Pocket Casts iOS fallback behavior is missing")
    print(f"Validated {len(EXPECTED)} feeds and {sum(EXPECTED.values())} episodes")


if __name__ == "__main__":
    main()
