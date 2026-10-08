# Civic Audio Library

Public hosting for three independently produced podcast courses. GitHub Pages serves the website, RSS feeds, artwork, transcripts, chapters, notes, accessibility records, provenance, and manifests. Immutable GitHub Releases serve MP3 enclosures.

Published site: <https://jstart.github.io/podcast-hosting/>

## Feeds

- Advanced Civic Planning: <https://jstart.github.io/podcast-hosting/advanced-civic-planning/feed.xml>
- Planning the City: <https://jstart.github.io/podcast-hosting/planning-commission-prep/feed.xml>
- Public Policy Prep: <https://jstart.github.io/podcast-hosting/public-policy-prep/feed.xml>

## Publish an update

Install `gh`, authenticate as `jstart`, and run this repository beside the source `podcast-tts` checkout:

```sh
./scripts/publish.sh ../podcast-tts
```

The script regenerates hosting-safe files, validates all feeds, creates missing show-specific version releases, uploads MP3s that are not already present, commits changed Pages content, and pushes it. The Pages workflow validates and deploys the result.

Releases are immutable in practice: the script never overwrites a release asset. To replace an episode:

1. Keep the episode's existing stable GUID in its source `.episode.json`.
2. Increment the show's production version in `episodes.json`.
3. Retain the previous version in provenance and set its `supersedes` relationship when applicable.
4. Run `scripts/publish.sh`. This creates a new release tag and enclosure URL.
5. Confirm the feed item still has the same GUID but now points to the new versioned release asset.

Never delete the old release. Existing downloads and provenance must remain resolvable.

## Pocket Casts

The site uses Pocket Casts' documented web Follow URL:

```text
https://pocketcasts.com/follow/<percent-encoded-feed-url>
```

It opens the podcast in Pocket Casts Web but does not follow automatically. The listener chooses **Follow** on the resulting page. Each show also has a prominent copy-feed control because pasting the RSS URL into Pocket Casts Discover or Search is the supported fallback.

## Safety

Only finished MP3s and hosting-safe companion files are published. Voice references, secrets, source caches, raw WAVs, intermediate audio, and unrelated source materials are excluded.
