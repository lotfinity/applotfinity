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
