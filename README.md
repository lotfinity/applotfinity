# lotfinity website

Code for site at: http://hello-from.lotfinity.tech


## Getting started

Make sure a recent version of Python is installed on your system.
Open this directory in a command prompt, then:

1. Install the software:
   ```
   pip install -r requirements.txt
   ```

2. Run the development server:
   ```
   python manage.py runserver
   ```

3. Go to http://localhost:8000/ in your browser, or http://localhost:8000/admin/
   to log in and get to work!

## Documentation links

* To customize the content, design, and features of the site see
  [Wagtail CRX](https://docs.coderedcorp.com/wagtail-crx/).

* For deeper customization of backend code see
  [Wagtail](http://docs.wagtail.io/) and
  [Django](https://docs.djangoproject.com/).

* For HTML template design see [Bootstrap](https://getbootstrap.com/).

---

Made with ♥ using [Wagtail](https://wagtail.io/) +
[CodeRed Extensions](https://www.coderedcorp.com/cms/)

## Static site export

There are two ways to produce a static version of this site.

- Built-in (no new dependency):
  - Run: `python manage.py buildstatic` (outputs to `build/`).
  - Options: `--build-dir <path>`, `--skip-static`, `--skip-media`.
  - This renders every live public Wagtail page and copies `static/` and `media/` into the build.

- Wagtail‑Bakery (recommended when you can install packages):
  1. Install: `pip install wagtail-bakery`.
  2. Add to `INSTALLED_APPS`: `'bakery', 'wagtailbakery'`.
  3. In `mysite/settings/base.py`, add:
     - `BUILD_DIR = BASE_DIR / 'build'`
     - `BAKERY_VIEWS = ('wagtailbakery.views.AllPagesView',)`
  4. Build: `python manage.py build` (outputs to `build/`).

Notes:
- Forms, search, and AJAX-only features won’t work on a static host unless replaced with client-side or third‑party services.
- Ensure media files are safe to publish before copying `media/` to the static host.


## Foundation hardening (October 2026)

The source layout and one-page design are preserved. Changes live on the
`work/lotfinity-foundation` branch until reviewed and merged. The original
production secret in older Git history **must be considered exposed** and
replaced before any production redeployment. No secrets belong in Git.

### Preview on ASUS (local LAN and Tailscale only)

The running preview uses `mysite.settings.preview`, SQLite, and port 8092.
It is deliberately HTTP-only and **not** a production service.

```bash
cd /home/lofa/DEV/portfolio-previews/applotfinity
export PORTFOLIO_PREVIEW_SECRET="$(cat .preview_secret)"
.venv/bin/python manage.py check --settings=mysite.settings.preview
.venv/bin/python manage.py test website.tests --settings=mysite.settings.preview
.venv/bin/python manage.py runserver 0.0.0.0:8092 --settings=mysite.settings.preview --noreload --insecure
```

### Production deployment (requires HTTPS reverse proxy)

1. Generate a **new** random secret; do not reuse the historical key or preview key.
2. Copy `.env.example` to `.env` outside source control. Set
   `DJANGO_SECRET_KEY`, `DJANGO_ALLOWED_HOSTS`, and
   `DJANGO_CSRF_TRUSTED_ORIGINS` for your actual domain.
3. Run `python manage.py check --deploy --settings=mysite.settings.prod`
   using the production environment. The warnings about HSTS subdomains,
   preload, and SAMEORIGIN are intentional pending domain validation and
   Wagtail preview needs.
4. Terminate TLS at a trusted reverse proxy, forward only valid hostnames,
   and arrange static files in `/data/static` and media in `/data/media` to
   be served from the named Compose volume **by the proxy or a separate
   web server**. Never execute user-uploaded media.
5. Only if the proxy sanitizes and rewrites untrusted `X-Forwarded-Proto`, set
   `DJANGO_TRUST_PROXY_SSL_HEADER=1` to avoid HTTPS redirect loops.
6. Run `docker compose up -d --build` after sufficient disk space is available,
   and set up persistent backups for the SQLite database and media files.

The Compose configuration uses **Gunicorn**, keeps its container HTTP port
bound to `127.0.0.1:55553` on the host, and persists its database and media
under the `lotfinity_data` volume. It is **not** ready for direct public
exposure without a correctly configured TLS/static reverse proxy.

The production WSGI entry point defaults to the secure production settings.
Debug tooling is enabled only by `mysite.settings.dev`; never by requests.

### Known follow-up work

- Convert manually authored homepage portfolio cards into Wagtail-managed data.
- Fix AppPage/AppsIndexPage templates, localization, and project assets.
- Refactor duplicated large templates, review the JS bundle, and improve SEO.
- Restore original CMS data/media from a trusted backup, if available.
- Expand tests (currently foundation-level smoke and security checks).


### Editing the CMS-powered homepage portfolio

After applying migrations, visit **Wagtail Admin → Pages → Home → Projects**.
The project index is a normal Wagtail page; its four `AppPage` children can be
edited, unpublished or deleted using the Wagtail editor.

- **Title**, **App Description**, **Mockup Design**: slide heading, text, image.
- **External URL**: live preview target on click; if blank, links to the detail.
- **Key Features**: one text line per bullet.
- **Tech Stack**: reusable editable technologies under Wagtail Snippets.
- **Show on homepage**: exclude a project from the homepage without unpublishing.
- **Display order**: numeric sort order; lower means earlier slide.
- **Page Body**: long-form content shown on the project's own Wagtail page.

Publish edits to update the homepage; saving a draft alone does not publish
changes. Newly created project pages only appear when published and flagged
for homepage display. The homepage, project index, and project detail pages
share one reusable carousel slide template. Screenshots generate optimized WebP
renditions.

To import the four original homepage slides into a **new or existing database**
without overwriting editor changes to project pages:

```bash
python manage.py migrate --settings=mysite.settings.preview
python manage.py seed_portfolio --settings=mysite.settings.preview
```

On ASUS, export `PORTFOLIO_PREVIEW_SECRET` from `.preview_secret` first. The
import command uses the four checked-in images and creates Wagtail media copies,
six reusable technology snippets, and four published project pages. Running it
again will skip any already-imported projects. Back up the database and media
files before using imports outside the local preview. No superuser is seeded
by the command.

The local preview-only admin account is `lotfinity-editor`. Its password is
in `.preview_admin_password` (not Git-tracked). It is a demonstration account,
not a production login. The HTTP-based LAN preview is **not production-grade**.

**Current localization limitation:** the original imported project content is
in English on each language route. Translate `AppPage` content with Wagtail
Localize in a later pass; do not treat homepage routes as fully translated yet.

### Edit the entire animated homepage in Wagtail

The homepage's site-wide content is now editable in **Wagtail Admin →
Settings → Lotfinity homepage**. The ASUS preview settings editor is at:

`http://100.73.225.127:8092/admin/settings/website/homepagesettings/1/`

Editors can change the hero headline, work/service copy, project carousel labels,
ordered service checklist, Studio introduction, individual animated skill circles
(names, logos, descriptions, percentages and display order), contact links,
website title and SEO description. The **Show projects**, **Show services**, and
**Show studio** checkboxes control section visibility. The homepage animations
and original CSS selectors remain in place. Project **records** are still edited
under **Pages → Home → Projects**, rather than in site settings.

The editor is a **Wagtail Site Setting**: it applies to this site, including all
currently available language routes. It is **not locale-specific**; manually
translated homepage text is a separate next step. English seed content is used
until proper per-language content is implemented. Wagtail only stores and serves
what the editor publishes/saves; it does not make the marketing descriptions
true by itself. Review any capabilities claimed in those descriptions.

To initialize the existing 8 services and 8 skills in another database, run:

```bash
python manage.py migrate
python manage.py seed_homepage
```

On ASUS, set `PORTFOLIO_PREVIEW_SECRET` and select
`--settings=mysite.settings.preview` for both commands. The seeder is safe to
repeat: it skips existing nonempty service/skill lists and **does not overwrite
edited content**. It imports the original skill icons into Wagtail Images.

**Backup:** The current local preview database and media are backed up outside
Git in `/home/lofa/DEV/portfolio-backups/`. Secrets, credentials, database files,
media files, and cache output are ignored by Git. Branch
`work/lotfinity-foundation` is not merged into `main`.

Production page caching is intentionally disabled for now so the site-wide
homepage settings appear immediately after editor saves. Reintroduce caching
only with explicit invalidation when homepage settings change.

### Energy-saving WebGL / animations (October 2026)

The original 550 KB `website/static/js/main.js` bundle contains an animated
Three.js shader, GSAP and the smooth-scroll engine. It used to run a full-window
GPU render on **every requestAnimationFrame**, even while the page was idle on
mobile. This caused unusually high CPU/GPU load, hot phones and laptop fans.

To preserve the same 3D background without keeping the GPU at full load:

- After testing, **restore smooth frame rates**: target 60 FPS on desktop and
  45 FPS on touch; these are caps, not guaranteed device FPS.
- Preserve antialiasing and higher drawing-buffer resolution (1.25x desktop,
  1.15x touch), because the original lower caps visibly damaged quality.
- Replace the excessively dense wireframe geometry (130,680 indices per draw)
  with 34,680 desktop / 20,280 touch — **3.8x / 6.4x less mesh work**.
- Pause WebGL drawing after **6.5 seconds without input**, and while the page
  is hidden. Reactivate on scroll, pointer movement, touch, or keyboard input.
- With `prefers-reduced-motion: reduce` or Save-Data, draw the scene once.
- Remove the second externally loaded GSAP/ScrollTrigger runtime. Skill-ring
  progress now uses a native IntersectionObserver and a CSS transition when
  visible; it resets when scrolled out of view.

The changes are a small, exact-match patch to the **existing minified bundle**.
`scripts/optimize_webgl.py` documents the modification and is deliberately
one-shot, refusing to run on an already-patched or incompatible file. If you
replace/rebuild the bundle in the future, reapply and test this optimization
rather than reverting to the unbounded render loop. The `smooth-1` query string
on `main.js` refreshes existing browser caches.

The browser profiling used headless Chrome on ASUS with software rendering:
previously about **7.6 seconds of browser task time over 7.8 seconds**, and
with the capped/idle renderer **no draw calls while idle** and ~0.5 seconds
of task time over a subsequent 4 seconds. These are local reproduction results,
**not measurements of a visitor's actual phone**. In the preview we verified
that scrolling, the project carousel, and progress circles still work.

**Note on compiling:** the legacy 550 KB minified bundle *already contains*
Three.js and the original shader, mixed together with scrolling/GSAP logic.
Simply recompiling it would not reduce the 130K-index wireframe workload; the
mesh reduction does. A fully tree-shaken replacement would require separating
and rebuilding the original bundled animation sources, and needs independent
visual/interaction QA before replacing this working scene. The current patch
preserves the original shader and existing scroll choreography.

### Portfolio content refresh — public work and engineering philosophy (28 October 2026)

The site now introduces Lotfinity as a **systems-oriented product builder** with
"Connect the Unconnected" as the homepage headline. The core editorial stance:
inspect the constraints of existing hardware/software, reuse proven components,
connect the missing interfaces, and report practical results and limitations.
Marketing claims about omniscient/autonomous websites were removed because the
portfolio does not substantiate them. Skills are shown as areas of focus; the
legacy percentage circles are illustrative, **not measured proficiency scores**.

The updated **six featured public repositories** are: `ohmlet`, `pricebridge-clean`,
`lotot-android`, `neon-strip-studio`, `IstanbulPropTech` and
`beyond-website-v5`. Stage labels distinguish active development, prototype,
personal test release and case study. The LotoT project credits its AndrOBD
upstream foundation, while Neon Strip Studio discloses limitations of target
hardware testing. Descriptions are based on the owner's GitHub portfolio review
and representative public READMEs/metadata, not comprehensive execution audits.
**Private Synaptic repositories are deliberately excluded** from the published
repository listings and source links.

The old DentiDelil/Salon Nassnor content remains editable in Wagtail but is
unfeatured and lives in the historical section of the **Projects** index.

`AppPage` now has `source_url`, `focus_area` and `project_stage` fields, all editable
in Wagtail. A **source URL** points to an actual public repository; it is NOT
mistaken for an embeddable live demo. `external_url` is reserved for an external
website. The new project index and case-study detail pages are lightweight,
semantic, accessible layouts that do not initialize the heavy animated homepage
JavaScript. Project posters without screenshots are CSS illustrations rather than
fabricated screenshots. Ohmlet uses the real public source screenshot
`lotfinity/ohmlet/shots/desktop.png`, resized to
`website/static/img/ohmlet-portfolio.webp`.

**Reproduce on another environment** after creating the Wagtail site and running
migrations (and `seed_portfolio`, `seed_homepage` if the original CMS content is
absent):

```bash
python manage.py curate_portfolio --apply
```

The command is opt-in, does not overwrite an already-customized homepage,
preserves pre-existing project pages by slug, and is safe to re-run. Its dry run
(without `--apply`) only describes proposed changes. Run it with an appropriate
settings module. Back up the database/media first. In the ASUS preview,
`/en/projects/` shows featured and historical entries; `Settings → Lotfinity
homepage` edits the message; `Pages → Projects` edits each project, source link,
status and visibility.

**Localization remains outstanding:** homepage Wagtail Site Settings are currently
site-wide, and `/tr/` and `/fr/` still show this English editorial text. Do not
claim fully translated projects until Wagtail localization is wired up.

### Verified interactive Ohmlet demo (28 October 2026)

The public **Ohmlet 3D breadboard simulator** is live at
`https://byd.whatsynaptic.com/`. The endpoint was checked over HTTPS (200),
and its actual React/WebGL interface was tested in Chrome: workspaces, circuit
parts, simulation controls and onboarding are visible with no page JS errors.
The Ohmlet Wagtail entry has a distinct **Launch live app** link and a separate
**Public source** link. The project screenshot is linked to the live app when
that URL is present; the case study remains independently accessible.
The curator seeds this URL for new databases but never overwrites later Wagtail
editor changes to existing project pages.

### Reusable CSS laptop and phone mockups

`AppPage` supports two optional Wagtail image fields:
**Device desktop image** and **Device mobile image**. When either is populated,
`website/partials/device_showcase.html` renders a responsive, pure CSS laptop
and/or phone frame. There is no React runtime, WebGL or extra client-side JS on
the case-study pages. Browser image renditions are served by Wagtail.

IstanbulPropTech is the first example, using the actual two screenshots supplied
by the site owner on 28 October 2026, optimized as WebP assets. Its Wagtail
project page displays both frames. Future projects can reuse the same feature
simply by attaching their screenshots in **Wagtail Pages → Projects → [project]
→ Device desktop image / Device mobile image**. The original image fields can
be changed without editing HTML or CSS. Other projects keep their existing
normal case-study images until the optional fields are provided.

Preview: `/en/projects/istanbulproptech/`. Test with `python manage.py test
website.tests --settings=mysite.settings.preview` (with preview environment
variables configured).

### Low-power animated project case-study background (October 2026)

Individual case-study pages (`website/templates/website/app_page.html`) now show
an ambient **connected-nodes and electric-pulse network** over a dark blue/purple
CSS atmosphere. The shared projects index and the animated homepage are not
changed. The original project images, mobile/desktop mockups, Wagtail content,
links and headings are retained. CSS panels add a subtle glass-like finish.

The effect is deliberately built with **Canvas 2D and plain JavaScript**, not a
second Three.js/WebGL renderer. There are no CDN dependencies, extra fonts,
large images, or WebGL shaders. Source:
`website/static/js/project-network.js` (about 8 KB uncompressed).

Resource limits:

- Nodes: 23 on narrow screens; at most 55 on desktop.
- Connections: maximum 41 on mobile, 90 on desktop; pairs precomputed at resize.
- Canvas pixel buffer: approximately 430,000 pixels on phones and 1.6 million
  on desktops, even if the user has a very high-DPI or 4K display.
- Animation: at most 18 FPS active on mobile and 24 FPS on desktop; **7 FPS idle**.
- Electric sparks: one short segment roughly every 3–6 seconds.
- **No drawing in hidden tabs**; static single-frame rendering for user-reduced
  motion or browser Save-Data settings. The CSS backdrop remains if Canvas fails.
- All graphics are `aria-hidden`, sit behind the content and never intercept
  pointer or keyboard events.

To tune color, intensity or panel styling, edit the `.project-detail` and
`.project-energy` rules at the end of `project-pages.css`; to adjust network
node brightness or spark frequency, use `project-network.js`. Browser tests
verify actual draw counts, hidden-tab pausing, and that the project index does
not load the background. The optimization was measured in headless Chrome on
ASUS and should be confirmed visually on real Android browsers before release.

### Portfolio banners and genuine device mockups

Each Wagtail `AppPage` now has an independently editable **Banner image** in
addition to the original project visual and device screenshots. The homepage
carousel and numbered `/en/projects/` grid prefer the banner, falling back to
the original mockup or a text cover. Detail pages show **genuine screenshots**
inside optional CSS laptop/phone frames, not invented app dashboards. Featured
numbers are derived from Wagtail ordering; archive projects remain separate.

See [`docs/portfolio-art-direction.md`](docs/portfolio-art-direction.md) for the
six-project visual brief and the repeatable Ohmlet banner workflow. The v1 Ohmlet
WebP and CMS image are stored on ASUS under `media/`, not in Git.

**PriceBridge real screenshots (Oct 29, 2026):** a private Django/Docker
preview on ASUS uses **historical July 18 evidence**, prominently labelled
as archival, and supplies verified desktop/mobile Chrome captures to Wagtail's
`device_*_image` fields. The promotional `banner_image` is still separate and
unset. See `docs/portfolio-art-direction.md` for provenance and limitations.

**LotoT native Android showcase (Oct 29, 2026):** original `com.lotot.android`
screenshots captured through ADB on a connected Samsung phone. The
charcoal/lime banner and two CSS phone mockups are stored in Wagtail. No
vehicle adapter was connected, so no real ECU data was recorded. The
second optional mobile screenshot field (`device_mobile_secondary_image`)
allows a truthful two-screen gallery without manufacturing a desktop UI.
See `docs/portfolio-art-direction.md` for provenance and source paths.

**Neon Strip Studio (Oct 29, 2026):** real web editor/screensaver-demo
screenshots captured at desktop and mobile browser sizes from source commit
`89e5e8e`, with a distinct Wagtail banner and screenshot mockups. The
Tailscale-only static preview runs on ASUS as `neon-strip-studio-preview` at
`http://100.73.225.127:8137/`, and its source/Compose configuration are
outside Git. The asset generator/import scripts live in `scripts/`; original
captures and final WebPs live under `media/`, included in CMS backups.
These are offline demos, **not captured live WLED hardware**. See
`docs/portfolio-art-direction.md` for the reproducible workflow.

**IstanbulPropTech (Oct 29, 2026):** project 05 now has a 1600×900
pine/emerald mapping banner in Wagtail, composed from the pre-existing
owner-supplied desktop/mobile UI reference images (kept untouched in their
separate mockup slots). These UI references were not independently verified
against a running application. The reproducible generator is
`scripts/build_istanbulproptech_banner.py`, and generated media remains outside
Git under `media/design_exports/`. See `docs/portfolio-art-direction.md`.

**Beyond Website / BeyondClinic (Oct 29, 2026):** the final numbered project
has a blue/violet editorial banner based on the archived desktop/mobile UI
screenshots shipped in the `beyond-website-v5` source repository. The original
images were imported separately as CSS device mockups. The repository includes
sensitive checked-in server material, and no live Django backend was deployed.
The 1600×900 WebP is generated by `scripts/build_beyond_website_banner.py`;
`scripts/import_beyond_website_screenshots.py` imports the source screenshots
idempotently. All image files and CMS data remain outside Git and are backed
up. See `docs/portfolio-art-direction.md` for accuracy/privacy limits.

**Featured project banners completed (Oct 29, 2026):** the numbered portfolio
now has individual 1600×900 banners for all **six featured projects**. The
previously missing PriceBridge cover was generated using its *real archival*
desktop and mobile browser screenshots, and added as `banner_image` without
replacing the authentic device mockups. Regenerate with
`scripts/build_pricebridge_banner.py`; see `docs/portfolio-art-direction.md`.
Desktop/mobile gallery and homepage carousel were verified in Chromium.

### React Bits-inspired Letter Glitch — numbered projects gallery

The `/en/projects/` index has its own **Letter Glitch** background, adapted
from the [React Bits effect](https://reactbits.dev/c/backgrounds/letter-glitch)
without bringing a React build or WebGL runtime into the Wagtail templates.
The custom Canvas2D effect lives at `website/static/js/gallery-letter-glitch.js`;
the gallery-only markup is `website/templates/website/apps_index_page.html` and
the visual layers are in `website/static/css/project-pages.css`.
It is an independent implementation inspired by React Bits by David Haz
([source/license](https://github.com/DavidHDev/react-bits), MIT + Commons Clause).

The background uses a dark green/cyan/blue letter field, smooth color flashes,
pointer stirring, short click scrambling and edge vignette; all elements are
`aria-hidden` and have `pointer-events: none` so the real links remain usable.
It does not affect the homepage or individual case-study backgrounds.
The site remains plain Django/Wagtail with no new npm dependencies or CDN.

**Tuning**: adjust `colors`, `cellW`/`cellH` base spacing, `count` in `scramble`,
`glitch` timing and the two `fps` budgets in the JS, and the `.gallery-letter-glitch`
opacity / vignette in CSS. The renderer is intentionally capped at ~3,200
letters on desktops and 800 on phones and ~1.25 MP of backing raster.
Desktop runs at a maximum 24 FPS during interaction / 10 FPS idle; phones
15 FPS active / 6 FPS idle; hidden tabs stop completely. Reduced-motion or
browser Save-Data settings display a single static frame. These are budgets,
not guaranteed frame rates.

QA: automated tests verify route isolation and performance policies. Headless
Chrome confirms that the desktop/mobile effect is visible, does not trigger
errors/overflow, and respects reduced motion. 4K tests reduced the first
version's ~18,000 glyphs / 1.75 seconds CPU task time over 4.4 seconds to
~3,200 glyphs / 0.35 seconds task time over 3.1 seconds. These are headless
browser measurements on ASUS, not measured temperatures on the user's devices.

### Hidden words inside the gallery Letter Glitch (October 29, 2026)

The numbered projects gallery now occasionally **decodes real phrases from its
random letter grid**, holds them and then dissolves them back into glitches.
Phrases are **editable in Wagtail**, not baked into the JavaScript: open
`/admin/` → Pages → **Projects** → Edit → **Glitch messages**. Enter one
short phrase per line (up to eight; ASCII letters, numbers, spaces and
basic punctuation); leave the field empty to disable phrase reveals.

The current defaults are `LOTFINITY`, `CONNECT THE PIECES`, `BUILD / INTEGRATE`
and `SOFTWARE + HARDWARE`. Each phrase starts after a brief delay, decodes
letter-by-letter (~1.2 seconds), remains visible (~2.85 seconds), fades over
~1.15 seconds, and then gives way to another after ~1.55 seconds. On phones,
longer phrases wrap across up to three lines within dedicated whitespace
above the selected-builds heading. On desktops, the text appears in the open
upper-right portion of the letter field. The glyph field continues to run at
the existing low frame-rate budget. Motion-reduced devices show a static first
phrase, while hidden tabs pause rendering entirely.

Implementation is in `website/models.py` (`AppsIndexPage.glitch_messages`),
the safe Django `json_script` binding in `apps_index_page.html`, and
`website/static/js/gallery-letter-glitch.js`. The content is treated as
plain text (never evaluated as HTML), and previous interactive card behavior
is unchanged. The field was introduced in migration
`website/migrations/0010_appsindexpage_glitch_messages.py`.

### Ambient animated numbered project cards (October 2026)

The six featured cards on `/en/projects/` now have **self-running, staggered
ambient animations** independent of the Letter Glitch background. Each card
uses its own project accent (cyan, mint, lime, purple, emerald, indigo):

- Two small light pulses travel along the top and bottom borders (CSS transform,
  *not* an animated conic gradient).
- The real banner image gently breathes (about 1.9% scale change) and is swept
  by a brief low-opacity holographic line approximately every 12 seconds.
- Its `01 / 06`-style number occasionally flickers with a discrete, stepped
  glow; the six timelines are deliberately staggered.
- Desktop pointer hover adds a restrained 3D tilt (max ~2–2.5 degrees),
  raised shadow, localized light and stronger image scale. The native card links
  continue to work. Touch has no hover tilt; keyboard focus gets a visible
  accent outline.

There are **no new third-party JS or WebGL dependencies**. Styling is scoped to
`.gallery-page .case-tile` in `website/static/css/project-pages.css`. The
3.4-KB vanilla JS helper `website/static/js/gallery-cards.js` only maintains
an IntersectionObserver for visibility, pointer-based CSS variables and
accessibility/battery state. Only onscreen/nearby cards animate; offscreen
cards pause. Hidden tabs, reduced-motion users and browsers in Save-Data mode
stop card animations. No perpetual JS timer or RAF loop is introduced.

**Performance guard:** the initial idea of animating a masked conic-gradient
border caused excessive main-thread repaint work. It was replaced by GPU-
composited transforms of two thin border tracers. In headless Chrome on ASUS,
desktop browser TaskDuration over a 3.8-second interval was approximately
0.92 sec with the whole card effect and 0.57 sec with all card animations
suppressed (both include the existing Letter Glitch background). On simulated
mobile, it was approximately 0.51 sec versus 0.13 sec. These are *development
benchmarks*, not claims about battery draw or real-device temperature. The
layout, card links, visibility pausing, motion preferences, and desktop/mobile
rendering were also verified. Firefox ESR rendered the new background and card
surfaces in a headless smoke test.
