"""Refresh the long-lived Instagram/Facebook token before it expires (60 days)
and write it back into the repo secret IG_ACCESS_TOKEN via the gh CLI.
Secrets needed: APP_ID, APP_SECRET, IG_ACCESS_TOKEN, ADMIN_PAT (fine-grained,
'Secrets: write' on this repo)."""
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
