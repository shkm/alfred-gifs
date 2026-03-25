#!/bin/bash
set -euo pipefail

if [ -z "${1:-}" ]; then
  echo "Usage: ./release.sh <version>"
  echo "Example: ./release.sh 1.0.0"
  exit 1
fi

VERSION="$1"
TAG="v$VERSION"

if git rev-parse "$TAG" >/dev/null 2>&1; then
  echo "Error: tag $TAG already exists"
  exit 1
fi

# Update version in info.plist
/usr/libexec/PlistBuddy -c "Set :version $VERSION" info.plist

git add info.plist
git diff --cached --quiet || git commit -m "Release $TAG"
git tag "$TAG"
git push origin main "$TAG"

echo "Released $TAG — GitHub Actions will create the release."
