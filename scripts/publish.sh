#!/usr/bin/env bash
set -euo pipefail

SOURCE_ROOT="${1:-../podcast-tts}"
OWNER="${GITHUB_OWNER:-jstart}"
REPO="${GITHUB_REPOSITORY_NAME:-podcast-hosting}"

active_owner="$(gh api user --jq .login)"
if [[ "$active_owner" != "$OWNER" ]]; then
  echo "GitHub CLI account is $active_owner; expected $OWNER." >&2
  exit 1
fi

python3 scripts/build_site.py --source "$SOURCE_ROOT"
python3 scripts/validate.py docs

for show in \
  how-california-schools-work \
  local-government-101 \
  local-officials-handbook \
  advanced-civic-planning \
  planning-commission-prep \
  public-policy-prep \
  financial-strategy-public-managers \
  census-academy \
  transportation-policies-programs-history \
  transportation-land-use-modeling \
  design-equity \
  environmental-justice-land-use-planning; do
  case "$show" in
    how-california-schools-work) source_dir="$SOURCE_ROOT" ;;
    local-government-101) source_dir="$SOURCE_ROOT/local-government-101-podcast" ;;
    local-officials-handbook) source_dir="$SOURCE_ROOT/local-officials-handbook-audio" ;;
    *) source_dir="$SOURCE_ROOT/$show" ;;
  esac
  version="$(python3 -c 'import json,sys; print(json.load(open(sys.argv[1]))["show"]["version"])' "$source_dir/episodes.json")"
  tag="$show-v$version"
  assets=()
  while IFS= read -r -d '' asset; do
    assets+=("$asset")
  done < <(find "$source_dir/final" -maxdepth 1 -name '*.mp3' -print0)
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
