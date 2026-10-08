#!/usr/bin/env bash
set -euo pipefail

SOURCE_ROOT="${1:-../podcast-tts}"
OWNER="${GITHUB_OWNER:-jstart}"
REPO="${GITHUB_REPOSITORY_NAME:-podcast-hosting}"

python3 scripts/build_site.py --source "$SOURCE_ROOT"
python3 scripts/validate.py docs

for show in advanced-civic-planning planning-commission-prep public-policy-prep; do
  version="$(python3 -c 'import json,sys; print(json.load(open(sys.argv[1]))["show"]["version"])' "$SOURCE_ROOT/$show/episodes.json")"
  tag="$show-v$version"
  if ! gh release view "$tag" --repo "$OWNER/$REPO" >/dev/null 2>&1; then
    gh release create "$tag" --repo "$OWNER/$REPO" --title "$show $version" --notes "Immutable audio release for $show, production version $version."
  fi
  existing_assets="$(gh release view "$tag" --repo "$OWNER/$REPO" --json assets --jq '.assets[].name')"
  while IFS= read -r -d '' asset; do
    name="$(basename "$asset")"
    if ! printf '%s\n' "$existing_assets" | rg --fixed-strings --line-regexp "$name" >/dev/null; then
      gh release upload "$tag" "$asset" --repo "$OWNER/$REPO"
    fi
  done < <(find "$SOURCE_ROOT/$show/final" -maxdepth 1 -name '*.mp3' -print0)
done

git add README.md docs scripts .github
if ! git diff --cached --quiet; then
  git commit -m "Publish podcast library"
  git push
fi

echo "Published https://$OWNER.github.io/$REPO/"
