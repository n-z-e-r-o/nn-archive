# autopost — daily Instagram publishing (GitHub Actions)

Push this folder as the ROOT of a repo. Then:

## Meta side (done once, by the account owner)
1. Instagram account of the channel: Professional → **Business** (or Creator).
2. A Facebook Page linked to it (Instagram → Settings → Linked accounts → Facebook).
3. developers.facebook.com → **My Apps → Create App** (type: Business/Other).
4. In the app add **Instagram Graph API** (Facebook Login for Business).
5. **Tools → Graph API Explorer**: pick the app, *Get User Token* with permissions
   `instagram_basic, instagram_content_publish, pages_show_list, pages_read_engagement, business_management`.
6. Extend it to a **long-lived token** (Tools → Access Token Debugger → *Extend*).
7. Find the IG user id: `GET /me/accounts` → page id → `GET /{page-id}?fields=instagram_business_account`.
   (Development mode is enough: the app admin's own accounts may publish without App Review.)

## GitHub side
Secrets: `IG_USER_ID`, `IG_ACCESS_TOKEN`, `APP_ID`, `APP_SECRET`, `ADMIN_PAT` (fine-grained PAT, Secrets: write).
Variable: `REELS_BASE_URL` = `https://github.com/n-z-e-r-o/nn-archive/releases/download/reels`
Reels: `bash autopost/upload_reels.sh n-z-e-r-o/nn-archive` (files `NN_nX.mp4`).

## Test
Actions → post-reel → Run workflow with `post_date=2026-09-24`, `dry_run=1` → prints the caption, publishes nothing.
Then `dry_run=` empty for one real test post (delete it in Instagram afterwards).
Schedule: 15:00 UTC daily (11:00 NY / 08:00 LA / 16:00 London / 18:00 Moscow) — global English audience; revisit after 1–2 weeks of Instagram Insights.
