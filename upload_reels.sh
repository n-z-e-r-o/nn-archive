#!/usr/bin/env bash
# One-time: put all finished reels into a public GitHub Release so the Graph API
# can fetch them. Run from D:/h/AIChannel with gh authenticated as the repo owner
# (or GH_TOKEN set). Usage: bash autopost/upload_reels.sh <owner/repo>
set -e
REPO="$1"; TAG="reels"
gh release view "$TAG" -R "$REPO" >/dev/null 2>&1 || gh release create "$TAG" -R "$REPO" --title "$TAG" --notes ""
gh release upload "$TAG" -R "$REPO" --clobber output/reels/*.mp4
echo "REELS_BASE_URL=https://github.com/$REPO/releases/download/$TAG"
