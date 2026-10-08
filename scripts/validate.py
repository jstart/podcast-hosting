#!/usr/bin/env python3
import json
import sys
import xml.etree.ElementTree as ET
from pathlib import Path
from urllib.parse import urlparse

EXPECTED = {
    "how-california-schools-work": 10,
    "local-government-101": 10,
    "local-officials-handbook": 14,
    "advanced-civic-planning": 36,
    "planning-commission-prep": 8,
    "public-policy-prep": 12,
}


def fail(message):
    raise SystemExit(message)


def main():
    docs = Path(sys.argv[1] if len(sys.argv) > 1 else "docs")
    for show, expected in EXPECTED.items():
        manifest = json.loads((docs / show / "manifest.json").read_text())
        if len(manifest["episodes"]) != expected:
            fail(f"{show}: expected {expected} episodes")
        root = ET.parse(docs / show / "feed.xml").getroot()
        items = root.findall("./channel/item")
        if len(items) != expected:
            fail(f"{show}: feed has {len(items)} items")
        guids = [item.findtext("guid") for item in items]
        if len(guids) != len(set(guids)):
            fail(f"{show}: duplicate GUID")
        for item in items:
            enclosure = item.find("enclosure")
            url = enclosure.attrib["url"]
            parsed = urlparse(url)
            if parsed.netloc != "github.com" or "/releases/download/" not in parsed.path:
                fail(f"{show}: invalid enclosure {url}")
            if int(enclosure.attrib["length"]) <= 0:
                fail(f"{show}: invalid enclosure length")
        for episode in manifest["episodes"]:
            for key, url in episode["pages"].items():
                if urlparse(url).netloc != "jstart.github.io":
                    fail(f"{show}: {key} is not hosted on Pages")
            if len(episode["enclosure"]["sha256"]) != 64:
                fail(f"{show}: invalid checksum")
    print(f"Validated {len(EXPECTED)} feeds and {sum(EXPECTED.values())} episodes")


if __name__ == "__main__":
    main()
