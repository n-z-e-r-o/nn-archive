"""Publish today's reel to Instagram via the Graph API (Content Publishing).

Runs inside GitHub Actions once a day. Steps:
  1. find the note scheduled for today (data/plan.json, dates are UTC-agnostic;
     the workflow's cron decides the local posting hour)
  2. skip if it is already in posted.json (idempotent on reruns)
  3. POST /{ig_user}/media  media_type=REELS video_url=<public mp4> caption=...
  4. poll the container until status_code == FINISHED
  5. POST /{ig_user}/media_publish creation_id=...
  6. append to posted.json (the workflow commits it back)

Uses the Instagram API with Instagram Login (graph.instagram.com): the token is
an Instagram user token, IG_USER_ID is the Instagram-scoped user id, and the
media/publish endpoints live on graph.instagram.com — no Facebook Page hop.

Env (GitHub secrets): IG_USER_ID, IG_ACCESS_TOKEN, REELS_BASE_URL
  REELS_BASE_URL = https://github.com/<owner>/<repo>/releases/download/<tag>
Optional: POST_DATE=YYYY-MM-DD to force a date (testing), DRY_RUN=1.
"""
import datetime as dt
import json
import os
import sys
import time
import urllib.parse
import urllib.request

API = "https://graph.instagram.com/v21.0"
HERE = os.path.dirname(os.path.abspath(__file__))


def call(method, path, **params):
    url = f"{API}/{path}"
    data = urllib.parse.urlencode(params).encode()
    req = urllib.request.Request(url, data=data if method == "POST" else None,
                                 method=method)
    if method == "GET":
        req = urllib.request.Request(f"{url}?{urllib.parse.urlencode(params)}")
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.load(r)


def main():
    ig = os.environ["IG_USER_ID"]
    token = os.environ["IG_ACCESS_TOKEN"]
    base = os.environ["REELS_BASE_URL"].rstrip("/")
    dry = os.environ.get("DRY_RUN") == "1"
    today = os.environ.get("POST_DATE") or dt.date.today().isoformat()

    plan = json.load(open(os.path.join(HERE, "data", "plan.json"), encoding="utf-8"))["plan"]
    caps = json.load(open(os.path.join(HERE, "data", "captions.json"), encoding="utf-8"))
    posted_path = os.path.join(HERE, "posted.json")
    posted = json.load(open(posted_path)) if os.path.exists(posted_path) else {}

    rows = sorted(plan, key=lambda r: r["date"])
    row = next((r for r in rows if r["date"] == today), None)
    if row is None:
        print(f"no note scheduled for {today}; nothing to do")
        return
    n = row["note"]
    if str(n) in posted:
        print(f"note {n} already posted on {posted[str(n)]}; skip")
        return
    idx = rows.index(row) + 1
    video_url = f"{base}/{idx:02d}_n{n}.mp4"
    caption = caps[str(n)]["caption"]
    print(f"posting note {n} ({today}) from {video_url}")
    if dry:
        print("DRY_RUN — caption:\n" + caption)
        return

    c = call("POST", f"{ig}/media", media_type="REELS", video_url=video_url,
             caption=caption, share_to_feed="true", access_token=token)
    cid = c["id"]
    for _ in range(40):                       # up to ~10 min of processing
        st = call("GET", cid, fields="status_code,status", access_token=token)
        code = st.get("status_code")
        print("container", cid, code)
        if code == "FINISHED":
            break
        if code == "ERROR":
            raise SystemExit(f"container error: {st}")
        time.sleep(15)
    else:
        raise SystemExit("container not finished in time")

    pub = call("POST", f"{ig}/media_publish", creation_id=cid, access_token=token)
    print("published media id", pub["id"])
    posted[str(n)] = today
    json.dump(posted, open(posted_path, "w"), indent=1)


if __name__ == "__main__":
    main()
