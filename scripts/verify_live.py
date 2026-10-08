#!/usr/bin/env python3
import json
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET


BASE = "https://jstart.github.io/podcast-hosting"
EXPECTED = {
    "how-california-schools-work": 10,
    "local-government-101": 10,
    "local-officials-handbook": 14,
    "advanced-civic-planning": 36,
    "planning-commission-prep": 8,
    "public-policy-prep": 12,
}


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, request, file_pointer, code, message, headers, url):
        return None


def fetch(url, headers=None):
    request = urllib.request.Request(
        url, headers={"User-Agent": "podcast-hosting-verifier", **(headers or {})}
    )
    for attempt in range(5):
        try:
            with urllib.request.urlopen(request, timeout=30) as response:
                time.sleep(0.03)
                return (
                    response.status,
                    response.headers,
                    response.read(),
                    response.geturl(),
                )
        except urllib.error.HTTPError as error:
            if error.code < 500 and error.code != 429:
                raise
            if attempt == 4:
                raise
            time.sleep(2**attempt)


def redirect_location(url):
    request = urllib.request.Request(
        url, method="HEAD", headers={"User-Agent": "podcast-hosting-verifier"}
    )
    opener = urllib.request.build_opener(NoRedirect)
    try:
        opener.open(request, timeout=30)
    except urllib.error.HTTPError as error:
        if error.code not in {301, 302, 303, 307, 308}:
            raise
        return error.headers["Location"]
    raise RuntimeError(f"{url}: expected a release redirect")


def verify_url(url, expected_prefix=None):
    status, headers, body, _ = fetch(url)
    if status != 200 or not body:
        raise RuntimeError(f"{url}: status={status} bytes={len(body)}")
    if expected_prefix and not body.startswith(expected_prefix):
        raise RuntimeError(f"{url}: unexpected content")
    return body, headers


def main():
    home, _ = verify_url(f"{BASE}/", b"<!doctype html>")
    verified = 0
    for show, expected in EXPECTED.items():
        feed_url = f"{BASE}/{show}/feed.xml"
        if urllib.parse.quote(feed_url, safe="").encode() not in home:
            raise RuntimeError(f"{show}: Pocket Casts discovery link missing")
        feed_body, _ = verify_url(feed_url, b"<?xml")
        feed = ET.fromstring(feed_body)
        items = feed.findall("./channel/item")
        if len(items) != expected:
            raise RuntimeError(f"{show}: expected {expected} items, found {len(items)}")
        manifest_body, _ = verify_url(f"{BASE}/{show}/manifest.json", b"{")
        manifest = json.loads(manifest_body)
        by_guid = {episode["stable_guid"]: episode for episode in manifest["episodes"]}
        if len(by_guid) != expected:
            raise RuntimeError(f"{show}: duplicate or missing stable GUIDs")
        for item in items:
            guid = item.findtext("guid")
            episode = by_guid[guid]
            enclosure = item.find("enclosure")
            enclosure_url = enclosure.attrib["url"]
            expected_bytes = int(enclosure.attrib["length"])
            redirect_location(enclosure_url)
            status, headers, body, final_url = fetch(
                enclosure_url, {"Range": "bytes=0-1023"}
            )
            if status != 206 or not headers.get("Content-Range"):
                raise RuntimeError(f"{enclosure_url}: byte range failed")
            total = int(headers["Content-Range"].rsplit("/", 1)[1])
            if total != expected_bytes or total != episode["enclosure"]["bytes"]:
                raise RuntimeError(f"{enclosure_url}: enclosure length mismatch")
            if len(body) != min(1024, total) or final_url == enclosure_url:
                raise RuntimeError(f"{enclosure_url}: range or redirect mismatch")
            for key, url in episode["pages"].items():
                prefix = (
                    b"WEBVTT"
                    if key == "transcript"
                    else b"{"
                    if key in {"chapters", "accessibility", "provenance"}
                    else b"\xff\xd8"
                    if key == "artwork"
                    else b"<!doctype html>"
                    if key == "canonical"
                    else None
                )
                verify_url(url, prefix)
            verify_url(
                episode["pages"]["canonical"].removesuffix(".html") + ".manifest.json",
                b"{",
            )
            verified += 1
    print(f"Verified {len(EXPECTED)} live feeds and {verified} live episodes")


if __name__ == "__main__":
    try:
        main()
    except Exception as error:
        print(error, file=sys.stderr)
        raise
