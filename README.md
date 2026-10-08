# The Systems Edge

A dark-theme Jekyll blog, compatible with GitHub Pages. Posts live in `_posts/`, layouts in `_layouts/`, styling in `assets/css/main.css`.

## Run it locally

1. Install Ruby 3.3 **with DevKit**: `winget install RubyInstallerTeam.RubyWithDevKit.3.3` (accept the MSYS2 setup prompt, option 1 + Enter, when it finishes). Open a **new** terminal afterwards.
2. In this folder:
   ```
   gem install bundler
   bundle install
   bundle exec jekyll serve
   ```
3. Open http://127.0.0.1:4000. To just check it builds: `bundle exec jekyll build` (output goes to `_site/`, which is git-ignored).

## Deploy to GitHub Pages (exact steps)

1. **Create the repo** on github.com: click **New repository**.
   - Simplest: name it `YOUR-GITHUB-USERNAME.github.io` (public). The site will live at `https://YOUR-GITHUB-USERNAME.github.io/`.
   - Or name it `affiliate-blog`; the site will then live at `https://YOUR-GITHUB-USERNAME.github.io/affiliate-blog/`.
   - Leave "Add a README" etc. **unticked** (this folder already has one).
2. **Edit `_config.yml`:**
   - `url: "https://YOUR-GITHUB-USERNAME.github.io"` (your real username)
   - `baseurl: ""` if the repo is `username.github.io`, or `baseurl: "/affiliate-blog"` if it's named `affiliate-blog`.
3. **Push the code** (from this folder, in a terminal):
   ```
   git init -b main
   git add .
   git commit -m "Initial site"
   git remote add origin https://github.com/YOUR-GITHUB-USERNAME/REPO-NAME.git
   git push -u origin main
   ```
4. **Turn on Pages:** repo **Settings -> Pages -> Build and deployment**. Source: **Deploy from a branch**. Branch: **main**, folder **/ (root)**. Click **Save**.
5. Wait 1-2 minutes (watch the **Actions** tab for the "pages build and deployment" run). The URL appears at the top of the Pages settings page.
6. **Optional custom domain:** Settings -> Pages -> Custom domain, then add a `CNAME` DNS record pointing at `YOUR-GITHUB-USERNAME.github.io`, and tick **Enforce HTTPS**.

## Before you publish: replace the affiliate placeholders

Every affiliate link in the posts is a highlighted placeholder like `[AFFILIATE_LINK_ODDSMONKEY]`. **Nothing is monetised until you replace them**, and the site must not go live with the raw placeholders showing.

Find every one still left:
```
grep -rn "AFFILIATE_LINK_" _posts
```

Replace each with your real tracked link, as a Markdown link, e.g. change
`<mark class="aff">[AFFILIATE_LINK_ODDSMONKEY]</mark>` to `[OddsMonkey](https://your-tracking-link)`.
(Delete the whole `<mark ...>...</mark>` wrapper, not only the text.)

Placeholders currently in use:

| Placeholder | Intended programme |
|---|---|
| `[AFFILIATE_LINK_ODDSMONKEY]` | OddsMonkey |
| `[AFFILIATE_LINK_PROFITACCUMULATOR]` | Profit Accumulator |
| `[AFFILIATE_LINK_FTMO]` | FTMO (or swap for GoatFunded) |
| `[AFFILIATE_LINK_AI_WRITING_TOOL]`, `[AFFILIATE_LINK_PROPERTY_CRM]` | choose a programme first |
| `[AFFILIATE_LINK_BEGINNER_MATCHED_BETTING_GUIDE]` | decide: your own guide post, or a service |

Only link to programmes you've actually been accepted into, and keep the affiliate disclosure and 18+/responsible gambling wording in place - UK ad rules (ASA/CAP) require them for gambling promotions, and this site is set up to show them on every page.

## Adding posts

- New posts from the generator: run `python import_posts.py` (it reads `C:\Users\matti\affiliate-marketing\content\` and rewrites `_posts/`). Re-running is safe. Note it uses today's date for the filename, so run it with a date (`python import_posts.py 2026-10-08`) to overwrite an existing import instead of creating duplicates on a later day.
- Or write by hand: create `_posts/YYYY-MM-DD-your-slug.md` starting with
  ```
  ---
  layout: post
  title: "Your title"
  description: "One-sentence summary used on the homepage and in search results."
  ---
  ```

## Layout of the repo

```
_config.yml        site title, url/baseurl, plugins
_layouts/          default (header/footer + disclosure), post, page
_posts/            the articles
assets/css/        main.css (dark theme; not style.css - the Pages default theme owns that name)
index.html         homepage with latest posts
blog.html          all-posts list
about.md           About page
import_posts.py    pulls generator output into _posts/
```
