# Civic Audio Library

Public hosting for 11 independently produced podcast courses. GitHub Pages serves the website, RSS feeds, artwork, transcripts, chapters, notes, accessibility records, provenance, and manifests. Immutable GitHub Releases serve MP3 enclosures.

Published site: <https://jstart.github.io/podcast-hosting/>

## Feeds

- Local Government and School Districts 101: <https://jstart.github.io/podcast-hosting/local-government-101/feed.xml>
- The Local Official's Handbook: <https://jstart.github.io/podcast-hosting/local-officials-handbook/feed.xml>
- Advanced Civic Planning: <https://jstart.github.io/podcast-hosting/advanced-civic-planning/feed.xml>
- Planning the City: <https://jstart.github.io/podcast-hosting/planning-commission-prep/feed.xml>
- Public Policy Prep: <https://jstart.github.io/podcast-hosting/public-policy-prep/feed.xml>
- Public Money, Public Strategy: <https://jstart.github.io/podcast-hosting/financial-strategy-public-managers/feed.xml>
- Census Data for Local Decisions: <https://jstart.github.io/podcast-hosting/census-academy/feed.xml>
- Transportation Policy in Practice: <https://jstart.github.io/podcast-hosting/transportation-policies-programs-history/feed.xml>
- Transportation and Land Use Models: <https://jstart.github.io/podcast-hosting/transportation-land-use-modeling/feed.xml>
- Designing for Equity: <https://jstart.github.io/podcast-hosting/design-equity/feed.xml>
- Planning for Environmental Justice: <https://jstart.github.io/podcast-hosting/environmental-justice-land-use-planning/feed.xml>

## Publish an update

Install `gh`, authenticate as `jstart`, and run this repository beside the source `podcast-tts` checkout:

```sh
./scripts/publish.sh ../podcast-tts
```

The script verifies that `gh` is using the `jstart` account, regenerates hosting-safe files, validates all feeds and companions, creates missing show-specific version releases, uploads MP3s that are not already present, commits changed Pages content, and pushes it. The Pages workflow validates and deploys the result.

Releases are immutable in practice: the script never overwrites a release asset. To replace an episode:

1. Keep the episode's existing stable GUID in its source `.episode.json`.
2. Increment the show's production version in `episodes.json`.
3. Retain the previous version in provenance and set its `supersedes` relationship when applicable.
4. Run `scripts/publish.sh`. This creates a new release tag and enclosure URL.
5. Confirm the feed item still has the same GUID but now points to the new versioned release asset.

Never delete the old release. Existing downloads and provenance must remain resolvable.

## Pocket Casts

The site keeps Pocket Casts' documented web Follow URL as each link's ordinary destination:

```text
https://pocketcasts.com/follow/<percent-encoded-feed-url>
```

On iOS, a progressively enhanced click first tries Pocket Casts' documented app URL:

```text
pktc://subscribe/https://<feed-host-and-path>
```

The custom scheme receives the complete raw HTTPS RSS URL, not the Pocket Casts web Follow URL or its percent-encoded identifier. If the app is unavailable, the browser returns to the web Follow URL. Other platforms use the web URL directly, and modified clicks keep normal browser behavior. Neither route follows automatically. The listener chooses **Follow** on the resulting page. Each show also has a prominent copy-feed control because pasting the RSS URL into Pocket Casts Discover or Search is the supported fallback.

## Safety

Only finished MP3s and hosting-safe companion files are published. Voice references, secrets, source caches, raw WAVs, intermediate audio, and unrelated source materials are excluded.
