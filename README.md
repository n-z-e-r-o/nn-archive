# autopost — daily Instagram publishing (GitHub Actions)

Push this folder as the ROOT of a repo. Then:

## Meta side (done once, by the account owner)
Uses the **Instagram API with Instagram Login** (`graph.instagram.com`).

1. Instagram account of the channel: Professional → **Business** (or Creator).
2. developers.facebook.com → an app with the **"Instagram" use case** (Instagram API).
   Note the **Instagram App ID** on the API-setup page.
3. In **Permissions & features** make sure these are added (they show
   "Ready for testing" for the app admin's own account — no App Review needed):
   `instagram_business_basic`, `instagram_business_content_publish`.
4. **Roles → Instagram Tester**: add the channel account; accept the invite in
   the Instagram app (Settings → for developers / tester invites).
5. **API setup → step 2 "Generate access tokens" → Add account**: log into the
   channel account, authorize. You get a token and the **Instagram user id**.
6. The token from step 5 is short-lived (1h). Exchange it once for a long-lived
   (60-day) token:
   `GET https://graph.instagram.com/access_token?grant_type=ig_exchange_token&client_secret=<IG app secret>&access_token=<short token>`
   The `access_token` in the reply is `IG_ACCESS_TOKEN`.

## GitHub side
Secrets: `IG_USER_ID` (the Instagram user id from step 5), `IG_ACCESS_TOKEN`
(long-lived token from step 6).
Optional, only for weekly auto-refresh: `ADMIN_PAT` (fine-grained PAT with
Secrets: write on this repo).
Variable: `REELS_BASE_URL` = `https://github.com/n-z-e-r-o/nn-archive/releases/download/reels`
Reels: `bash autopost/upload_reels.sh n-z-e-r-o/nn-archive` (files `NN_nX.mp4`).

## Token lifetime
Instagram long-lived tokens last 60 days. The channel runs ~98 days
(2026-09-18 → 2026-12-25), so refresh once. Either:
- **manual**: around mid-November repeat step 6's refresh (or
  `GET graph.instagram.com/refresh_access_token?grant_type=ig_refresh_token&access_token=<current>`)
  and update the `IG_ACCESS_TOKEN` secret; or
- **auto**: set `ADMIN_PAT` and let `refresh-token.yml` do it weekly.

## Test
Actions → post-reel → Run workflow with `post_date=2026-09-18`, `dry_run=1` →
prints the caption, publishes nothing.
Then `dry_run=` empty for one real test post (delete it in Instagram afterwards).
Schedule: 15:00 UTC daily (11:00 NY / 08:00 LA / 16:00 London / 18:00 Moscow) —
global English audience; revisit after 1–2 weeks of Instagram Insights.
