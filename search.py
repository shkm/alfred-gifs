#!/usr/bin/python3
import concurrent.futures
import hashlib
import json
import os
import sys
import urllib.parse
import urllib.request

CACHE = os.environ.get("alfred_workflow_cache", "/tmp/alfred-gif-cache")
API_KEY = os.environ.get("api_key", "")
UA = {"User-Agent": "Alfred-GIF-Workflow/1.0"}


def out(items):
    print(json.dumps({"skipknowledge": True, "items": items}))
    sys.exit(0)


def fetch(url):
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=10) as r:
        return r.read()


def cache_file(url, ext="gif"):
    path = os.path.join(CACHE, hashlib.md5(url.encode()).hexdigest() + "." + ext)
    if not os.path.exists(path):
        with open(path, "wb") as f:
            f.write(fetch(url))
    return path


def cache_quicklook(gif_url):
    path = os.path.join(CACHE, hashlib.md5(gif_url.encode()).hexdigest() + ".html")
    if not os.path.exists(path):
        with open(path, "w") as f:
            f.write(
                "<html><body style='margin:0;background:#000;display:flex;"
                "align-items:center;justify-content:center;height:100vh'>"
                f"<img src='{gif_url}' style='max-width:100%;max-height:100vh'>"
                "</body></html>"
            )
    return path


def fmt_size(b):
    return f"{b // 1024} KB" if b < 1024 * 1024 else f"{b / (1024 * 1024):.1f} MB"


def main():
    query = sys.argv[1].strip() if len(sys.argv) > 1 else ""
    if len(query) < 2:
        out([{"title": "Type at least 2 characters...", "valid": False}])
    if not API_KEY:
        out([{"title": "Set your Klipy API key in workflow settings", "valid": False}])

    params = urllib.parse.urlencode({"q": query, "per_page": 24, "content_filter": "medium"})
    try:
        data = json.loads(fetch(f"https://api.klipy.com/api/v1/{API_KEY}/gifs/search?{params}"))
        results = data.get("data", {}).get("data", [])
    except Exception as e:
        out([{"title": "Search failed", "subtitle": str(e), "valid": False}])

    if not results:
        out([{"title": "No results found", "valid": False}])

    os.makedirs(CACHE, exist_ok=True)

    # Download tiny GIF thumbnails in parallel
    thumb_urls = [
        r.get("file", {}).get("xs", {}).get("gif", {}).get("url", "")
        for r in results
    ]
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as pool:
        thumbs = list(pool.map(lambda u: cache_file(u) if u else "", thumb_urls))

    items = []
    for r, thumb in zip(results, thumbs):
        gif = r.get("file", {}).get("hd", {}).get("gif", {})
        gif_url = gif.get("url", "")
        if not gif_url:
            continue
        w = gif.get("width", 0)
        h = gif.get("height", 0)
        size_str = fmt_size(gif.get("size", 0))
        item = {
            "uid": str(r.get("id", "")),
            "title": r.get("title", "") or r.get("slug", "GIF"),
            "subtitle": f"{w}×{h} · {size_str}",
            "arg": gif_url,
            "valid": True,
            "quicklookurl": cache_quicklook(gif_url),
        }
        if thumb:
            item["icon"] = {"path": thumb}
        items.append(item)

    out(items)


if __name__ == "__main__":
    main()
