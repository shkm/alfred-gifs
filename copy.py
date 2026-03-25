#!/usr/bin/python3
import hashlib
import os
import subprocess
import sys
import urllib.request

CACHE = os.environ.get("alfred_workflow_cache", "/tmp/alfred-gif-cache")
UA = {"User-Agent": "Alfred-GIF-Workflow/1.0"}


def main():
    url = sys.argv[1] if len(sys.argv) > 1 else ""
    if not url or not url.startswith("http"):
        return

    os.makedirs(CACHE, exist_ok=True)
    path = os.path.join(CACHE, hashlib.md5(url.encode()).hexdigest() + "_hd.gif")

    if not os.path.exists(path):
        req = urllib.request.Request(url, headers=UA)
        with urllib.request.urlopen(req, timeout=30) as r:
            with open(path, "wb") as f:
                f.write(r.read())

    subprocess.run([
        "osascript", "-e", 'use framework "AppKit"',
        "-e", f'set fp to current application\'s NSURL\'s fileURLWithPath:"{path}"',
        "-e", "set pb to current application's NSPasteboard's generalPasteboard()",
        "-e", "pb's clearContents()",
        "-e", "pb's writeObjects:{fp}",
    ])


if __name__ == "__main__":
    main()
