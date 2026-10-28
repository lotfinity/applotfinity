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
