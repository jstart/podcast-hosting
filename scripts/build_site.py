#!/usr/bin/env python3
import argparse
import hashlib
import html
import json
import re
import shutil
import xml.etree.ElementTree as ET
from datetime import datetime
from email.utils import format_datetime
from pathlib import Path
from urllib.parse import quote

OWNER = "jstart"
REPO = "podcast-hosting"
BASE = f"https://{OWNER}.github.io/{REPO}"
DOWNLOAD = f"https://github.com/{OWNER}/{REPO}/releases/download"
SHOWS = {
    "local-government-101": {
        "source_dir": "local-government-101-podcast",
        "description": "A 10-episode introduction to California cities, counties, special districts, school districts, public finance, voting, and civic participation."
    },
    "local-officials-handbook": {
        "source_dir": "local-officials-handbook-audio",
        "description": "A 14-episode practical guide to local public service, open government, planning, housing, regional institutions, and public decision-making."
    },
    "advanced-civic-planning": {
        "description": "A 36-episode advanced course in public hearings, land use, housing, transportation, environmental justice, and municipal finance."
    },
    "planning-commission-prep": {
        "description": "An eight-episode practical course for reading projects, making findings, navigating CEQA, and acting after the vote."
    },
    "public-policy-prep": {
        "description": "A 12-episode interdisciplinary study course spanning government, sociology, psychology, economics, writing, and algebra."
    },
    "financial-strategy-public-managers": {
        "description": "A nine-episode course connecting public-sector financial tools to mission, accountability, costs, budgets, and repeatable strategy."
    },
    "census-academy": {
        "description": "A 14-episode practical course on Census data, geography, uncertainty, APIs, housing, commuting, business, and government finance."
    },
    "transportation-policies-programs-history": {
        "description": "A 10-episode course on transportation policy history, institutions, planning, mobility programs, sustainability, and global lessons."
    },
    "transportation-land-use-modeling": {
        "description": "A 13-episode course on integrated transportation and land-use modeling, data, scenarios, trip generation, mode choice, and feedback."
    },
    "design-equity": {
        "description": "An eight-episode course on designing public places, services, information, and decision processes for equitable outcomes."
    },
    "environmental-justice-land-use-planning": {
        "description": "An eight-episode course on environmental justice evidence, land-use policy, implementation, accountability, and planning review."
    },
}
SAFE_SUFFIXES = {
    ".accessibility.json",
    ".chapters.json",
    ".credits.json",
    ".episode.json",
    ".license.txt",
    ".md",
    ".provenance.json",
    ".vtt",
}
PODCAST_NS = "https://podcastindex.org/namespace/1.0"
ITUNES_NS = "http://www.itunes.com/dtds/podcast-1.0.dtd"
HOST_NS = f"{BASE}/namespace/1.0"
ET.register_namespace("podcast", PODCAST_NS)
ET.register_namespace("itunes", ITUNES_NS)
ET.register_namespace("podhost", HOST_NS)


def sha256(path):
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def local_name(tag):
    return tag.split("}", 1)[-1]


def rewrite_urls(value, replacements):
    if isinstance(value, dict):
        return {key: rewrite_urls(item, replacements) for key, item in value.items()}
    if isinstance(value, list):
        return [rewrite_urls(item, replacements) for item in value]
    if isinstance(value, str):
        for old, new in replacements.items():
            if value == old:
                return new
    return value


def pretty_xml(element):
    ET.indent(element, space="  ")
    return '<?xml version="1.0" encoding="UTF-8"?>\n' + ET.tostring(
        element, encoding="unicode", short_empty_elements=True
    )


def build_show(source_root, docs, show_id):
    source = source_root / SHOWS[show_id].get("source_dir", show_id)
    manifest = json.loads((source / "episodes.json").read_text())
    show = manifest["show"]
    version = show["version"]
    tag = f"{show_id}-v{version}"
    output = docs / show_id
    assets = output / "episodes"
    artwork = output / "artwork"
    assets.mkdir(parents=True, exist_ok=True)
    artwork.mkdir(parents=True, exist_ok=True)
    episodes = []

    for jpg in sorted((source / "artwork").glob("ep*.jpg")):
        shutil.copy2(jpg, artwork / jpg.name)
    shutil.copy2(source / "artwork" / "ep01.jpg", output / "cover.jpg")

    by_number = {item["number"]: item for item in manifest["episodes"]}
    for mp3 in sorted((source / "final").glob("*.mp3")):
        match = re.search(r"_Ep(\d+)_", mp3.name)
        if not match:
            raise RuntimeError(f"Cannot determine episode number from {mp3.name}")
        number = int(match.group(1))
        stem = mp3.stem
        source_episode = json.loads((source / "final" / f"{stem}.episode.json").read_text())
        episode = by_number[number]
        release_url = f"{DOWNLOAD}/{tag}/{quote(mp3.name)}"
        canonical = f"{BASE}/{show_id}/episodes/{quote(stem)}.html"
        transcript = f"{BASE}/{show_id}/episodes/{quote(stem)}.vtt"
        chapters = f"{BASE}/{show_id}/episodes/{quote(stem)}.chapters.json"
        art = f"{BASE}/{show_id}/artwork/ep{number:02d}.jpg"
        accessibility = f"{BASE}/{show_id}/episodes/{quote(stem)}.accessibility.json"
        provenance = f"{BASE}/{show_id}/episodes/{quote(stem)}.provenance.json"
        notes = f"{BASE}/{show_id}/episodes/{quote(stem)}.md"
        hosting_manifest = f"{BASE}/{show_id}/episodes/{quote(stem)}.manifest.json"
        replacements = {
            source_episode.get("enclosure_url"): release_url,
            source_episode.get("transcript_url"): transcript,
            source_episode.get("chapters_url"): chapters,
            source_episode.get("artwork_url"): art,
            source_episode.get("canonical_url"): canonical,
        }
        rewritten = rewrite_urls(source_episode, replacements)
        rewritten["enclosure_url"] = release_url
        rewritten["transcript_url"] = transcript
        rewritten["chapters_url"] = chapters
        rewritten["artwork_url"] = art
        rewritten["canonical_url"] = canonical
        rewritten["accessibility_url"] = accessibility
        rewritten["notes_url"] = notes
        rewritten["provenance_url"] = provenance
        rewritten["release_tag"] = tag
        rewritten["release_version"] = version
        rewritten.setdefault("checksums", {})["audio_sha256"] = sha256(mp3)
        rewritten["checksums"]["transcript_sha256"] = sha256(
            source / "final" / f"{stem}.vtt"
        )

        for candidate in (source / "final").glob(f"{stem}.*"):
            suffix = candidate.name[len(stem) :]
            if suffix not in SAFE_SUFFIXES:
                continue
            destination = assets / candidate.name
            if suffix == ".episode.json":
                destination.write_text(json.dumps(rewritten, indent=2) + "\n")
            else:
                shutil.copy2(candidate, destination)

        hosted = {
            "stable_guid": rewritten["guid"],
            "show": show_id,
            "episode": number,
            "title": episode["title"],
            "release_version": version,
            "release_tag": tag,
            "enclosure": {
                "url": release_url,
                "bytes": mp3.stat().st_size,
                "sha256": rewritten["checksums"]["audio_sha256"],
            },
            "pages": {
                "canonical": canonical,
                "artwork": art,
                "transcript": transcript,
                "chapters": chapters,
                "notes": notes,
                "accessibility": accessibility,
                "provenance": provenance,
            },
        }
        (assets / f"{stem}.manifest.json").write_text(json.dumps(hosted, indent=2) + "\n")
        (assets / f"{stem}.html").write_text(
            episode_page(show, episode, hosted, stem)
        )
        episodes.append(
            {
                **hosted,
                "summary": episode["summary"],
                "publication_date": rewritten["publication_date"],
                "duration_seconds": rewritten["duration_seconds"],
            }
        )

    show_manifest = {
        "id": show_id,
        "title": show["title"],
        "album": show["album"],
        "description": SHOWS[show_id]["description"],
        "version": version,
        "release_tag": tag,
        "stable_feed_url": f"{BASE}/{show_id}/feed.xml",
        "release_url": f"https://github.com/{OWNER}/{REPO}/releases/tag/{tag}",
        "episodes": episodes,
    }
    (output / "manifest.json").write_text(json.dumps(show_manifest, indent=2) + "\n")
    (output / "feed.xml").write_text(feed_xml(show, show_id, episodes))
    (output / "index.html").write_text(show_page(show_manifest))
    return show_manifest


def feed_xml(show, show_id, episodes):
    rss = ET.Element("rss", {"version": "2.0"})
    channel = ET.SubElement(rss, "channel")
    ET.SubElement(channel, "title").text = show["title"]
    ET.SubElement(channel, "link").text = f"{BASE}/{show_id}/"
    ET.SubElement(channel, "description").text = SHOWS[show_id]["description"]
    ET.SubElement(channel, "language").text = "en-us"
    ET.SubElement(channel, "generator").text = "podcast-hosting/scripts/build_site.py"
    ET.SubElement(channel, f"{{{ITUNES_NS}}}author").text = show["author"]
    ET.SubElement(channel, f"{{{ITUNES_NS}}}explicit").text = "false"
    ET.SubElement(channel, f"{{{ITUNES_NS}}}type").text = "serial"
    ET.SubElement(channel, f"{{{ITUNES_NS}}}image", {"href": f"{BASE}/{show_id}/cover.jpg"})
    image = ET.SubElement(channel, "image")
    ET.SubElement(image, "url").text = f"{BASE}/{show_id}/cover.jpg"
    ET.SubElement(image, "title").text = show["title"]
    ET.SubElement(image, "link").text = f"{BASE}/{show_id}/"
    ET.SubElement(channel, f"{{{PODCAST_NS}}}locked", {"owner": OWNER}).text = "yes"
    ET.SubElement(channel, f"{{{PODCAST_NS}}}guid").text = hashlib.sha256(
        show_id.encode()
    ).hexdigest()
    ET.SubElement(channel, f"{{{PODCAST_NS}}}person", {"role": "host", "group": "writing"}).text = show["author"]
    ET.SubElement(channel, f"{{{PODCAST_NS}}}license").text = "See per-episode license and credits"

    for episode in sorted(episodes, key=lambda item: item["episode"], reverse=True):
        item = ET.SubElement(channel, "item")
        ET.SubElement(item, "title").text = episode["title"]
        ET.SubElement(item, "description").text = episode["summary"]
        ET.SubElement(item, "link").text = episode["pages"]["canonical"]
        ET.SubElement(item, "guid", {"isPermaLink": "false"}).text = episode["stable_guid"]
        published = datetime.fromisoformat(episode["publication_date"].replace("Z", "+00:00"))
        ET.SubElement(item, "pubDate").text = format_datetime(published)
        ET.SubElement(
            item,
            "enclosure",
            {
                "url": episode["enclosure"]["url"],
                "length": str(episode["enclosure"]["bytes"]),
                "type": "audio/mpeg",
            },
        )
        ET.SubElement(item, f"{{{ITUNES_NS}}}episode").text = str(episode["episode"])
        ET.SubElement(item, f"{{{ITUNES_NS}}}season").text = str(show["season"])
        ET.SubElement(item, f"{{{ITUNES_NS}}}duration").text = str(
            round(episode["duration_seconds"])
        )
        ET.SubElement(item, f"{{{ITUNES_NS}}}explicit").text = "false"
        ET.SubElement(item, f"{{{ITUNES_NS}}}image", {"href": episode["pages"]["artwork"]})
        ET.SubElement(
            item,
            f"{{{PODCAST_NS}}}transcript",
            {"url": episode["pages"]["transcript"], "type": "text/vtt", "language": "en"},
        )
        ET.SubElement(
            item,
            f"{{{PODCAST_NS}}}chapters",
            {"url": episode["pages"]["chapters"], "type": "application/json+chapters"},
        )
        ET.SubElement(item, f"{{{PODCAST_NS}}}person", {"role": "host"}).text = show["author"]
        ET.SubElement(item, f"{{{PODCAST_NS}}}license", {"url": episode["pages"]["notes"]}).text = "Episode-specific terms"
        ET.SubElement(item, f"{{{PODCAST_NS}}}txt", {"purpose": "accessibility"}).text = episode["pages"]["accessibility"]
        ET.SubElement(item, f"{{{HOST_NS}}}notes").text = episode["pages"]["notes"]
        ET.SubElement(item, f"{{{HOST_NS}}}manifest").text = (
            episode["pages"]["canonical"].removesuffix(".html") + ".manifest.json"
        )
        ET.SubElement(item, f"{{{HOST_NS}}}provenance").text = episode["pages"]["provenance"]
        ET.SubElement(item, f"{{{HOST_NS}}}sha256").text = episode["enclosure"]["sha256"]
        ET.SubElement(item, f"{{{HOST_NS}}}releaseVersion").text = episode["release_version"]
    return pretty_xml(rss) + "\n"


def layout(title, body, depth=""):
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="theme-color" content="#102238">
  <title>{html.escape(title)}</title>
  <link rel="stylesheet" href="{depth}assets/site.css">
  <script defer src="{depth}assets/site.js"></script>
</head>
<body>
  <a class="skip" href="#main">Skip to content</a>
  <header><a class="brand" href="{depth}">CIVIC AUDIO LIBRARY</a></header>
  <main id="main">{body}</main>
  <footer>Independent study productions. No institutional endorsement.</footer>
</body>
</html>
"""


def pocket_casts_links(feed):
    web = f"https://pocketcasts.com/follow/{quote(feed, safe='')}"
    feed_without_scheme = re.sub(r"^https?://", "", feed)
    ios = f"pktc://subscribe/{feed_without_scheme}"
    return web, ios


def show_card(show):
    feed = f"{BASE}/{show['id']}/feed.xml"
    pocket, pocket_ios = pocket_casts_links(feed)
    return f"""
<article class="show-card">
  <img src="{show['id']}/cover.jpg" alt="" width="560" height="560">
  <div>
    <p class="eyebrow">{len(show['episodes'])} EPISODES · VERSION {html.escape(show['version'])}</p>
    <h2><a href="{show['id']}/">{html.escape(show['title'])}</a></h2>
    <p>{html.escape(show['description'])}</p>
    <div class="actions">
      <a class="button" href="{show['id']}/feed.xml">RSS feed</a>
      <button data-copy="{feed}">Copy feed</button>
      <a class="button secondary" href="{pocket}" data-pocket-casts-ios="{pocket_ios}">Open in Pocket Casts</a>
    </div>
  </div>
</article>"""


def show_page(show):
    feed = show["stable_feed_url"]
    pocket, pocket_ios = pocket_casts_links(feed)
    episode_rows = "".join(
        f'<li><span>{item["episode"]:02d}</span><a href="episodes/{quote(item["pages"]["canonical"].rsplit("/", 1)[-1])}">{html.escape(item["title"])}</a></li>'
        for item in show["episodes"]
    )
    body = f"""
<section class="hero compact">
  <p class="eyebrow">{len(show['episodes'])} EPISODES · {html.escape(show['version'])}</p>
  <h1>{html.escape(show['title'])}</h1>
  <p>{html.escape(show['description'])}</p>
  <div class="actions">
    <a class="button" href="feed.xml">RSS feed</a>
    <button data-copy="{feed}">Copy feed</button>
    <a class="button secondary" href="{pocket}" data-pocket-casts-ios="{pocket_ios}">Open in Pocket Casts</a>
  </div>
  <p class="hint">On iOS, Pocket Casts opens the feed in the app when installed. Otherwise, the web player opens. Choose Follow there. If lookup is delayed, copy the RSS URL and paste it into Discover or Search.</p>
</section>
<section><h2>Episodes</h2><ol class="episode-list">{episode_rows}</ol></section>"""
    return layout(show["title"], body, "../")


def episode_page(show, episode, hosted, stem):
    body = f"""
<article class="episode">
  <p class="eyebrow">EPISODE {episode['number']:02d}</p>
  <h1>{html.escape(episode['title'])}</h1>
  <p>{html.escape(episode['summary'])}</p>
  <img class="episode-art" src="../artwork/ep{episode['number']:02d}.jpg" alt="{html.escape(show['artwork_alt'])}">
  <div class="actions">
    <a class="button" href="{hosted['enclosure']['url']}">Download MP3</a>
    <a class="button secondary" href="{quote(stem)}.vtt">Transcript</a>
    <a class="button secondary" href="{quote(stem)}.md">Notes</a>
    <a class="button secondary" href="{quote(stem)}.chapters.json">Chapters</a>
  </div>
  <dl>
    <dt>Stable GUID</dt><dd><code>{hosted['stable_guid']}</code></dd>
    <dt>Release</dt><dd>{hosted['release_tag']}</dd>
    <dt>SHA-256</dt><dd><code>{hosted['enclosure']['sha256']}</code></dd>
  </dl>
</article>"""
    return layout(episode["title"], body, "../../")


def write_static(docs, shows):
    cards = "".join(show_card(show) for show in shows)
    episode_count = sum(len(show["episodes"]) for show in shows)
    body = f"""
<section class="hero">
  <p class="eyebrow">INDEPENDENT CIVIC STUDY</p>
  <h1>Listen closely.<br>Govern thoughtfully.</h1>
  <p class="lede">{len(shows)} accessible audio courses with {episode_count} episodes for public service, planning, education, and policy study.</p>
</section>
<section aria-labelledby="shows"><h2 id="shows">The collection</h2>{cards}</section>
<aside class="pocket-note">
  <h2>Pocket Casts</h2>
  <p>On iOS, each Pocket Casts action opens the feed in the app when installed. Other devices and iOS devices without the app use Pocket Casts Web. Neither route follows automatically. Choose Follow, or copy the RSS URL and paste it into Discover or Search.</p>
</aside>"""
    (docs / "index.html").write_text(layout("Civic Audio Library", body))
    assets = docs / "assets"
    assets.mkdir(exist_ok=True)
    (assets / "site.css").write_text(CSS)
    (assets / "site.js").write_text(JS)
    (docs / ".nojekyll").write_text("")
    (docs / "namespace" / "1.0").mkdir(parents=True, exist_ok=True)
    (docs / "namespace" / "1.0" / "index.html").write_text(
        layout("Podcast hosting namespace", "<h1>Podcast hosting namespace</h1><p>Extension elements identify notes, manifests, provenance, checksums, and release versions.</p>", "../../")
    )


CSS = """
:root{--navy:#102238;--gold:#E8B04C;--ivory:#F0ECE2;--gray:#A0B2C4;--panel:#172f4b;--max:1120px}
*{box-sizing:border-box}html{color-scheme:dark}body{margin:0;background:var(--navy);color:var(--ivory);font-family:"Avenir Next",Avenir,system-ui,sans-serif;line-height:1.55}a{color:inherit}header,main,footer{width:min(var(--max),calc(100% - 40px));margin:auto}header{padding:38px 0 22px}.brand,.eyebrow{color:var(--gold);font-weight:700;letter-spacing:.15em;text-decoration:none}.skip{position:absolute;left:-9999px}.skip:focus{left:16px;top:16px;background:var(--ivory);color:var(--navy);padding:10px;z-index:2}.hero{padding:8vh 0 10vh;border-bottom:2px solid var(--gold)}.hero.compact{padding:5vh 0}.hero h1,.episode h1{max-width:850px;margin:.12em 0;font-family:Georgia,serif;font-size:clamp(3rem,9vw,7.5rem);line-height:.94;letter-spacing:-.04em}.hero.compact h1,.episode h1{font-size:clamp(2.8rem,7vw,6rem)}.lede{max-width:650px;color:var(--gray);font-size:1.3rem}section{padding:54px 0}h2{font-family:Georgia,serif;font-size:2rem}.show-card{display:grid;grid-template-columns:minmax(220px,390px) 1fr;gap:42px;align-items:center;padding:44px 0;border-top:1px solid #35506d}.show-card img,.episode-art{width:100%;height:auto}.show-card p,.hint{color:var(--gray);max-width:650px}.actions{display:flex;flex-wrap:wrap;gap:10px;margin:24px 0}.button,button{display:inline-block;border:2px solid var(--gold);border-radius:2px;background:var(--gold);color:var(--navy);font:inherit;font-weight:700;padding:10px 15px;text-decoration:none;cursor:pointer}.button.secondary{background:transparent;color:var(--ivory)}button:focus-visible,a:focus-visible{outline:3px solid var(--ivory);outline-offset:3px}.pocket-note{margin:40px 0 80px;padding:28px;border-left:8px solid var(--gold);background:var(--panel)}.episode-list{list-style:none;padding:0}.episode-list li{display:grid;grid-template-columns:3rem 1fr;gap:16px;padding:16px 0;border-bottom:1px solid #35506d}.episode-list span{color:var(--gold)}.episode{padding:6vh 0}.episode-art{max-width:600px;display:block;margin:40px 0}dl{display:grid;grid-template-columns:120px 1fr;gap:8px 20px}dt{color:var(--gray)}dd{margin:0;overflow-wrap:anywhere}code{color:var(--gold)}footer{color:var(--gray);padding:35px 0 65px;border-top:1px solid #35506d}
@media(max-width:720px){.show-card{grid-template-columns:1fr}.show-card img{max-width:420px}.hero{padding-top:5vh}dl{grid-template-columns:1fr}}
@media(prefers-reduced-motion:no-preference){.button,button{transition:transform .15s ease}.button:hover,button:hover{transform:translateY(-2px)}}
"""

JS = """
document.querySelectorAll("[data-copy]").forEach((button) => {
  button.addEventListener("click", async () => {
    await navigator.clipboard.writeText(button.dataset.copy);
    const old = button.textContent;
    button.textContent = "Copied";
    setTimeout(() => { button.textContent = old; }, 1600);
  });
});

const isIOS = /^(iPhone|iPad|iPod)$/.test(navigator.platform)
  || (navigator.platform === "MacIntel" && navigator.maxTouchPoints > 1);

if (isIOS) {
  document.querySelectorAll("[data-pocket-casts-ios]").forEach((link) => {
    link.addEventListener("click", (event) => {
      if (event.defaultPrevented || event.button !== 0
          || event.metaKey || event.ctrlKey || event.shiftKey || event.altKey) {
        return;
      }
      event.preventDefault();
      const fallback = link.href;
      const timer = setTimeout(() => {
        if (document.visibilityState === "visible") {
          window.location.assign(fallback);
        }
      }, 1200);
      window.addEventListener("pagehide", () => clearTimeout(timer), { once: true });
      window.location.assign(link.dataset.pocketCastsIos);
    });
  });
}
"""


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path, default=Path("../podcast-tts"))
    parser.add_argument("--output", type=Path, default=Path("docs"))
    args = parser.parse_args()
    if args.output.exists():
        shutil.rmtree(args.output)
    args.output.mkdir(parents=True)
    shows = [build_show(args.source.resolve(), args.output, show_id) for show_id in SHOWS]
    write_static(args.output, shows)
    print(json.dumps({show["id"]: len(show["episodes"]) for show in shows}, indent=2))


if __name__ == "__main__":
    main()
