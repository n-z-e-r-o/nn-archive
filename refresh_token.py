"""Optional: refresh a long-lived Facebook user/page token before it expires and
write it back into the repo secret IG_ACCESS_TOKEN via the gh CLI.

NOTE: if IG_ACCESS_TOKEN is a long-lived *Page* token (derived from a long-lived
user token), it does not expire and this workflow is unnecessary. Keep it only if
you store a 60-day user token instead.

Secrets needed: APP_ID, APP_SECRET, IG_ACCESS_TOKEN, ADMIN_PAT (fine-grained,
'Secrets: write' on this repo). REPO is provided by the workflow.
"""
import json, os, subprocess, urllib.parse, urllib.request
q = urllib.parse.urlencode({"grant_type": "fb_exchange_token",
                            "client_id": os.environ["APP_ID"],
                            "client_secret": os.environ["APP_SECRET"],
                            "fb_exchange_token": os.environ["IG_ACCESS_TOKEN"]})
with urllib.request.urlopen(f"https://graph.facebook.com/v21.0/oauth/access_token?{q}", timeout=60) as r:
    new = json.load(r)["access_token"]
subprocess.run(["gh", "secret", "set", "IG_ACCESS_TOKEN", "--repo", os.environ["REPO"]],
               input=new.encode(), check=True)
print("token refreshed")
