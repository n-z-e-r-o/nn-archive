"""Refresh the long-lived Instagram user token before it expires (60 days) and
write it back into the repo secret IG_ACCESS_TOKEN via the gh CLI.

Instagram Login tokens refresh with just the current (valid, >24h old) token —
no app id/secret needed. The refreshed token is valid for another 60 days.

Secrets needed: IG_ACCESS_TOKEN, ADMIN_PAT (fine-grained, 'Secrets: write' on
this repo). REPO is provided by the workflow (github.repository).
"""
import json, os, subprocess, urllib.parse, urllib.request

q = urllib.parse.urlencode({"grant_type": "ig_refresh_token",
                            "access_token": os.environ["IG_ACCESS_TOKEN"]})
url = f"https://graph.instagram.com/refresh_access_token?{q}"
with urllib.request.urlopen(url, timeout=60) as r:
    data = json.load(r)
new = data["access_token"]
print(f"refreshed; expires_in={data.get('expires_in')} s")
subprocess.run(["gh", "secret", "set", "IG_ACCESS_TOKEN", "--repo", os.environ["REPO"]],
               input=new.encode(), check=True)
print("token written back to IG_ACCESS_TOKEN")
