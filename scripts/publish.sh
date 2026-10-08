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
  assets=()
  while IFS= read -r -d '' asset; do
    assets+=("$asset")
  done < <(find "$SOURCE_ROOT/$show/final" -maxdepth 1 -name '*.mp3' -print0)
  if ! gh release view "$tag" --repo "$OWNER/$REPO" >/dev/null 2>&1; then
    gh release create "$tag" "${assets[@]}" --repo "$OWNER/$REPO" --title "$show $version" --notes "Immutable audio release for $show, production version $version."
  fi
  existing_assets="$(gh api "repos/$OWNER/$REPO/releases/tags/$tag" --jq '.assets[] | [.name, .size] | @tsv')"
  for asset in "${assets[@]}"; do
    name="$(basename "$asset")"
    existing_size="$(printf '%s\n' "$existing_assets" | awk -F '\t' -v name="$name" '$1 == name { print $2 }')"
    if [[ -z "$existing_size" ]]; then
      echo "$name is missing from immutable release $tag. Increment the show version." >&2
      exit 1
    elif [[ "$existing_size" -ne "$(wc -c < "$asset" | tr -d ' ')" ]]; then
      echo "$name changed in immutable release $tag. Increment the show version." >&2
      exit 1
    fi
  done
done

git add README.md docs scripts .github
if ! git diff --cached --quiet; then
  git commit -m "Publish podcast library"
  git push
fi

echo "Published https://$OWNER.github.io/$REPO/"
