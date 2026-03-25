# Alfred GIF Search

Search [Klipy](https://klipy.com) for GIFs from Alfred. Browse results in a grid and copy them to your clipboard for pasting into Slack, Signal, etc.

## Setup

1. Download `alfred-gifs.alfredworkflow` from the [latest release](https://github.com/shkm/alfred-gifs/releases/latest)
2. Double-click to install in Alfred
3. Get a free API key from https://partner.klipy.com/api-keys
4. Open the workflow settings in Alfred and paste your API key

## Usage

- Type `gif <search term>` and press Enter
- Browse results in the grid view
- Select a GIF to copy it to your clipboard
- Paste it anywhere

## Releasing

```
./release.sh 1.0.0
```

This updates the version in `info.plist`, commits, tags, and pushes. GitHub Actions will build the `.alfredworkflow` and create a release.
