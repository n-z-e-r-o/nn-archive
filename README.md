# autopost — daily Instagram publishing (GitHub Actions)

Push this folder as the ROOT of a repo. Then:

## Meta side (done once, by the account owner)
Uses the **Instagram Graph API with Facebook Login** (`graph.facebook.com`).
No Instagram password or tester invite needed — the token comes from the
Facebook user who administers the Page linked to the Instagram account.

1. Instagram account of the channel: Professional (Business/Creator).
2. A Facebook Page linked to it (done via the Instagram professional settings or
   Meta Business Suite).
3. developers.facebook.com app with the **Instagram** use case; on
   **"API setup with Facebook login"** click **Add required content permissions**
   (adds instagram_basic, instagram_content_publish, pages_show_list,
   pages_read_engagement, business_management).
4. **Graph API Explorer** → select the app → Generate Access Token (authorize the
   Page and Instagram account) → this is a short-lived **user** token.
5. Get `IG_USER_ID`: query `me/accounts?fields=name,instagram_business_account{id,username}`
   → the `instagram_business_account.id` of your Page.
6. Get a **non-expiring Page token** for `IG_ACCESS_TOKEN`:
   - in the Explorer, dropdown "User or Page" → **Get Page Access Token** → pick
     your Page → copy that token;
   - open **Access Token Debugger** (developers.facebook.com/tools/debug/accesstoken),
     paste it, click **Extend Access Token**, copy the extended token.
   That extended Page token does not expire.

## GitHub side
Secrets: `IG_USER_ID`, `IG_ACCESS_TOKEN` (the extended Page token).
Variable: `REELS_BASE_URL` = `https://github.com/n-z-e-r-o/nn-archive/releases/download/reels`
Reels: `bash autopost/upload_reels.sh n-z-e-r-o/nn-archive` (files `NN_nX.mp4`).

## Token lifetime
A Page token extended from a long-lived user token does not expire, so no refresh
is needed. `refresh-token.yml` / `refresh_token.py` are only relevant if you store
a 60-day user token instead (then also set `APP_ID`, `APP_SECRET`, `ADMIN_PAT`).

## Test
Actions → post-reel → Run workflow with `post_date=2026-09-18`, `dry_run=1` →
prints the caption, publishes nothing.
Then `dry_run=` empty for one real test post (delete it in Instagram afterwards).
Schedule: 15:00 UTC daily (11:00 NY / 08:00 LA / 16:00 London / 18:00 Moscow).
