import os
from dotenv import load_dotenv

# Load variables from the .env file into the environment
load_dotenv() 
# Returns None if 'API_KEY' is missing
api_key = os.getenv("FILMOTAPI_KEY")


import json
import math
import requests


def search_filmot_complete(
    query: str,
    n: int,
    api_key: str,
    lang: str = "en",
    clip_duration: int = 16,
) -> dict:
    """
    Search Filmot for N distinct videos containing an exact phrase.

    Returns a JSON-compatible dict with video IDs, timestamps,
    matching subtitle text, and YouTube clip URLs.

    By: ChatGPT
    """
    if n < 1:
        raise ValueError("n must be positive")
    if clip_duration < 1:
        raise ValueError("clip_duration must be positive")

    endpoint = "https://apiv1.filmot.com/api/v1/getsubtitlesearch"
    headers = {"X-API-Key": api_key}

    results = []
    seen_ids = set()
    page = 1
    page_size = min(n, 500)

    with requests.Session() as session:
        while len(results) < n:
            params = {
                "query": f'"{query}"',
                "lang": lang,
                "page": page,
                "perPageCount": page_size,
                "format": "json",
                "exportInline": 1,
                "columns": "id,title,channelname,hits",
                "getSnippets": 1,
            }

            response = session.get(
                endpoint,
                headers=headers,
                params=params,
                timeout=60,
            )
            response.raise_for_status()
            data = response.json()

            # Support flat exports and legacy envelopes.
            if isinstance(data, list):
                videos = data
            elif isinstance(data, dict):
                videos = data.get(
                    "result",
                    data.get("videos", data.get("items", []))
                )
            else:
                raise ValueError("Unexpected Filmot response")

            if not isinstance(videos, list):
                raise ValueError("Unexpected Filmot video list")

            if not videos:
                break

            for video in videos:
                video_id = video.get("id")

                if not video_id or video_id in seen_ids:
                    continue

                hits = video.get("hits") or []
                if isinstance(hits, str):
                    hits = json.loads(hits)

                if not hits:
                    continue

                hit = hits[0]

                # A hit can contain a timestamp and optional
                # contextual caption lines.
                timestamp = hit.get("start")
                lines = hit.get("lines") or []

                if timestamp is None and lines:
                    timestamp = lines[0].get("start")

                if timestamp is None:
                    continue

                match_start = float(timestamp)
                start = max(0, math.floor(match_start - 3))
                end = start + clip_duration

                if lines:
                    snippet = " ".join(
                        line.get("text", "")
                        for line in lines
                    )
                else:
                    snippet = " ".join(
                        str(hit.get(field, ""))
                        for field in (
                            "ctx_before", "token", "ctx_after"
                        )
                    ).strip()

                results.append({
                    "video_id": video_id,
                    "title": video.get("title"),
                    "channel": video.get("channelname"),
                    "match_start": match_start,
                    "start": start,
                    "end": end,
                    "text": snippet,
                    "url": (
                        f"https://www.youtube.com/embed/"
                        f"{video_id}?start={start}&end={end}"
                    ),
                    "watch_url": (
                        f"https://www.youtube.com/watch"
                        f"?v={video_id}&t={start}s"
                    ),
                })

                seen_ids.add(video_id)

                if len(results) == n:
                    break

            if len(videos) < page_size:
                break

            page += 1

    return {
        "query": query,
        "count": len(results),
        "videos": results,
    }

def search_filmot(query, n) -> dict:
    if api_key is None:
        raise ValueError("FILMOT_API_KEY is not set in the environment variables.")
    return search_filmot_complete(query, n, api_key=api_key)

# Example
if __name__ == "__main__":
    if api_key is None:
        raise ValueError("FILMOT_API_KEY is not set in the environment variables.")

    result = search_filmot_complete(
        query="some people",
        n=1,
        api_key=api_key,
    )

    with open("results.json", "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)

    print(json.dumps(result, indent=2, ensure_ascii=False))
