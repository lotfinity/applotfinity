# Lotfinity numbered project-banner series

The homepage carousel and `/en/projects/` cards are powered by Wagtail `AppPage` records. The **banner_image** field is deliberately separate from `mockup_design`, `device_desktop_image` and `device_mobile_image`: a banner is an editorial illustration, whereas the other fields must contain genuine application screenshots. The featured-project list is numbered from 01 through the current total and is sorted by `display_order`; archived entries are not part of the count.

## Proposed visual brief, reviewed one project at a time

| Number | Project | Banner purpose and verified functionality | Proposed color direction | Screenshot status |
| --- | --- | --- | --- | --- |
| 01 | Ohmlet | 3D breadboard, wiring, analog/digital simulation, AI-assisted circuit creation | Midnight navy `#071426`, signal cyan `#46D0EE`, silver | Existing verified desktop workbench screenshot; v1 banner created and Wagtail-linked. No mobile screenshot yet. |
| 02 | PriceBridge | Historical Algeria/Türkiye smartphone listing evidence, canonical variant matching and opportunity comparison | Deep ocean `#071424`, mint `#62ECB7`, pale ice | Actual desktop and mobile captures from the private historical-data preview are in Wagtail; matching 1600×900 banner created and published. Prices are not live. |
| 03 | LotoT | Android OBD-II diagnostics, native sensor context, React cockpit, MQTT | Verified in-app colors: charcoal `#0C0F11`, lime `#D7FF45`, muted sage | Authentic on-device cockpit + sensor explorer screenshots captured and published; 1600×900 banner created. No OBD adapter connected during capture. |
| 04 | Neon Strip Studio | 150-group continuous WLED layout editor, editable perimeter/infinity loop, animation demo, JSON import/export | Verified screen palette: near-black `#090A14`, rainbow accent, magenta `#DB66F0`, cyan `#B5EFF7` | Real desktop and mobile-browser editor captures published in Wagtail with original 1600×900 banner. Offline demo only; physical WLED not tested. |
| 05 | IstanbulPropTech | Neighborhood/property exploration with hierarchical geographic filters, location context and map layers | Screen-derived palette: pine `#0B393B`, emerald `#38E7B4`, mist `#E6F3EB` | Owner-supplied desktop/mobile UI reference images retained in Wagtail; 1600×900 editorial banner published separately. Running app not independently verified. |
| 06 | Beyond Website | BeyondClinic patient-facing service dashboard: messages, appointments, prescriptions, billing and connected operations | Source-derived: blue `#6478F4`, navy `#0A102A`, mint `#3EE3C0`, coral `#FD7672` | Archived desktop/mobile screenshots found in the public repository and linked in Wagtail; 1600×900 banner created. Not verified against a running production server. |

All palettes above are starting points, not claims about uninspected application UIs. The four historical projects can be treated as an optional second collection after the six current featured projects have been approved.

## Deliverables per project

1. **Banner**: 1600×900 WebP, high contrast, large numbered identity, accurate app purpose and matched palette. Designed illustration or collage allowed, but no fabricated statistics or features. The homepage carousel and numbered projects index use this banner.
2. **Desktop / mobile mockups**: CSS device frames supplied by the website with **authentic running-app captures when available**, or clearly documented owner-supplied design reference images. Never claim an unverified UI reference is a working deployment. No invented or stretched mobile UI. Attach only images appropriate to that viewport.
3. **Wagtail**: import the banner to `AppPage.banner_image`; keep the original `mockup_design` untouched. Use existing `device_desktop_image` and `device_mobile_image` separately.
4. **Review**: verify the numbered card, homepage slideshow, detail page and mobile layout before starting the next project.

## Reproducible Ohmlet version 1

The reviewed-source first draft is made with the actual `media/original_images/ohmlet-portfolio.webp` screenshot and produces a 1600×900 WebP (~70 KB). It is saved on ASUS in `media/design_exports/01-ohmlet-banner-v1.webp` and uploaded to Wagtail (`media/original_images/01-ohmlet-banner-v1.webp`). Its cyan/blue circuit-trace treatment conveys the actual electronics-simulation project without fabricated UI.

To regenerate the local draft and attach it to a new Wagtail database (do **not** overwrite an editor-selected existing banner without an explicit `--replace`):

```bash
python scripts/build_project_banner.py
python manage.py apply_project_banner --slug ohmlet \
  --file media/design_exports/01-ohmlet-banner-v1.webp \
  --desktop-from-mockup
```

Use the local preview settings environment when running these on ASUS. All original images, CMS content and media databases stay outside Git; media exports need to be included in normal server backups.

### PriceBridge — real preview screenshots captured 2026-10-29

No publicly discoverable `lotfinity/pricebridge` or `lotfinity/pricebridge-clean` image was found on Docker Hub. A private, locally-built Django Docker preview runs on ASUS at `http://100.73.225.127:8136/` (Tailscale only). The upstream repository provides no precomputed opportunities; a sanitized historical database from the repository's **2026-07-18** snapshots was used to recompute **one real Apple iPhone comparison**. Historical FX and listings must **not** be described as fresh prices or currently available offers. The cloned preview visibly labels this archival status and does not allow web writes.

Authentic desktop and mobile browser screenshots were captured with Playwright and imported into Wagtail PriceBridge `device_desktop_image` and `device_mobile_image` slots using `scripts/import_pricebridge_screenshots.py`. Their original PNGs are under ASUS `/home/lofa/DEV/portfolio-previews/pricebridge-deploy/screenshots/`; uploaded optimized WebPs are under `media/original_images/`. The case study now displays the two real captures inside its CSS-only laptop/phone mockups.

**PriceBridge promotional banner completed (2026-10-29):** the deep-blue/mint artwork combines these genuine desktop/mobile screenshots with a clearly marked historical-data caption. It is not a claim of live market prices or new records. The original PriceBridge GitHub repository was not modified or pushed as part of the preview or artwork setup.

### 03 — LotoT authentic Android screens and banner (2026-10-29)

The LotoT Android repository was cloned read-only from `https://github.com/lotfinity/lotot-android` to ASUS under `/home/lofa/DEV/portfolio-previews/lotot-android/`. A connected Samsung Android device was verified to have the actual installed `com.lotot.android` application (version `0.9.0-ui`). Original Android screenshots were captured through ADB on ASUS and preserved alongside site media under `media/design_sources/lotot/` (also available in `/home/lofa/DEV/portfolio-previews/lotot-captures/`): cockpit, live sensor explorer and health/ECU screen. The media backup includes the full-resolution captures. **No ELM327 or vehicle ECU was connected**; live motion values come from phone sensors, not a car. The phone was returned to its previous ChatGPT screen afterwards.

A reviewable **1600 × 900, 69-KB** charcoal/lime banner was generated using **unaltered screenshot pixels** inside ornamental phone frames, with no fictional OBD figures. The source is `scripts/build_lotot_banner.py` and the server export is `media/design_exports/03-lotot-banner-v1.webp`. The banner is stored in `AppPage.banner_image` (Wagtail) and displayed on both the main carousel and numbered Projects grid.

Two authentic Android screenshots were independently imported to `AppPage.device_mobile_image` and the new optional `AppPage.device_mobile_secondary_image` through `scripts/import_lotot_screenshots.py` (idempotent, preserves existing editorial choices). The project case-study displays them side by side in *two CSS-only phone mockups*, without pretending the app has a desktop interface. The other existing desktop+mobile project layouts are unchanged. The original third screen (health / fault scan) is still stored in the ASUS captures directory as a possible later gallery image.

**Provenance and limitations:** LotoT extends AndrOBD (GPL-3.0), as credited in its repository. The marketing artwork is an editorial composition made from real screens; screen values are those visible on the captured device. Screenshots alone do not demonstrate a live vehicle connection or diagnostic accuracy. For the next project, reuse the `banner_image` workflow and only source project visuals from verified installations or owner-provided screenshots.

### 04 — Neon Strip Studio browser/editor capture (2026-10-29)

The **actual source** was cloned from `https://github.com/lotfinity/neon-strip-studio` at commit `89e5e8e` (no source modifications). Two existing browser-side rendering/geometry test suites passed **12/12**. A private static browser preview (not a live controller) was deployed on ASUS with a read-only Docker filesystem, no admin/backend service, 128 MB memory limit, 0.5 CPU limit and Tailscale-only access at `http://100.73.225.127:8137/`. The Compose file resides outside the portfolio repo at `/home/lofa/DEV/portfolio-previews/neon-strip-deploy/compose.yml` and mounts the real `web/` sources read-only.

Using Chromium with the running editor, actual **desktop 1440×900** and **mobile-browser 780×1688** screenshots were recorded and saved under `media/design_sources/neon-strip-studio/` and the capture directory `/home/lofa/DEV/portfolio-previews/neon-captures/`. The desktop screenshot shows actual edit control points over the 120 perimeter + 30 infinity/lead geometry; the mobile-browser screenshot shows the responsive editor. Wagtail `device_desktop_image` and `device_mobile_image` contain optimized WebPs (imported with `scripts/import_neon_studio_screenshots.py`). Existing project images were not overwritten.

The **1600×900 WebP banner** (`media/design_exports/04-neon-strip-studio-banner-v1.webp`, about 65 KB) uses the true editor screenshot and mobile-browser screenshot placed inside editorial device illustrations. Rainbow accents are abstract decoration, not recorded LED frames. Its reproducible generator is `scripts/build_neon_strip_banner.py`; it was uploaded and published in `AppPage.banner_image`, and the existing homepage carousel and numbered index use it automatically.

**Truthful product status:** all captured editor screens explicitly say **OFFLINE · DEMO**. No physical ESP32/WLED connection, relay, native Android screensaver, Windows screensaver, or GNOME idle integration was verified by these browser captures. Native package claims should be limited to what the project's README documents. The private preview has a WLED Connect button that is not used in the screenshots; the published portfolio has no external live-URL entry because Tailscale would be inaccessible to public site visitors.

### 05 — IstanbulPropTech — desktop/mobile references and editorial banner (2026-10-29)

This project already had two **owner-supplied** images in Wagtail: `media/original_images/istanbulproptech-desktop.webp` (760×466, Wagtail image 25) and `media/original_images/istanbulproptech-mobile.webp` (260×564, Wagtail image 26). They show a property-search map of Istanbul, neighborhood context, property cards and area-selection controls. They are preserved in the `device_desktop_image` and `device_mobile_image` fields. Their origins are identified as **owner-supplied UI references**, **not** independently validated captures of a currently running server or actual property listings. The depicted prices and markers should not be interpreted as live market data.

For provenance the public source `https://github.com/lotfinity/IstanbulPropTech` was cloned on ASUS at commit `ba303b7`. Repository documentation describes the hierarchical store/category filters and map data, while the CMS description covers neighborhood and property exploration. No live Django instance was launched as part of this visual-artwork pass, and the source repository was not changed.

A **1600×900, ~87 KB WebP** banner was composed around the two exact existing UI images and a dark pine/emerald palette with abstract cartographic lines, location nodes, and the number **05**. The lines and markers outside the screenshots are decorative, not actual GIS features. The reproducible generator is `scripts/build_istanbulproptech_banner.py` and its output is `media/design_exports/05-istanbulproptech-banner-v1.webp`. Wagtail `banner_image` is image 36, separately stored as `media/original_images/05-istanbulproptech-banner-v1.webp` and displayed on the homepage and numbered grid. The original device images were not replaced.

Both the desktop and mobile portfolio case-study layouts and project-card banners were browser-tested at 1366px and 390px respectively: no broken banner/device images, no horizontal overflow, no JavaScript errors. The portfolio DB and media were backed up before importing. This completes the visual treatment for project 05; the next feature project is **06 — Beyond Website**.

### 06 — Beyond Website / BeyondClinic — archived interface screenshots (2026-10-29)

The selected case-study record is `Beyond Website — Business Workflows`, source `https://github.com/lotfinity/beyond-website-v5`, commit `f77d0fe` (2025-07-28). The repository contains a Django application with healthcare/patient-service workflows and administrative integration. The available branded interface screenshots use **BeyondClinic** and show an actual patient-facing dashboard design, including message, appointment and prescription cards. These source assets were found as `staticfiles/assets/img/screenshot1.png` (desktop 1280×720) and `staticfiles/assets/img/screenshot2.png` (mobile 720×1480), then copied into the portfolio's `media/design_sources/beyond-website/` directory for repeatable image builds. The source UI screenshots include demo-looking account labels and are **not** a freshly verified live login, working backend, or evidence of clinical efficacy. No real customer data was accessed for the banner.

The editorial **1600×900 WebP (~60 KB)** at `media/design_exports/06-beyond-website-banner-v1.webp` reuses both of those repository UI screenshots inside decorative browser/phone frames, with a deep blue/violet/mint palette and a conceptual workflow-node background. It is produced with `scripts/build_beyond_website_banner.py`, published into the Wagtail `banner_image` field, and used automatically on the homepage and numbered projects index.

`scripts/import_beyond_website_screenshots.py` imports the two real source-repository UI images independently into Wagtail `device_desktop_image` and `device_mobile_image`, preserving any existing editor-chosen images. The case-study page displays the screenshots in CSS-only laptop/phone frames. All outputs are backed up as CMS database/media and were checked at desktop and mobile widths with no missing image or horizontal overflow.

**Deployment/security:** the cloned repository also contains a checked-in application `.env`, cookie material and database/media files. It must **not** be deployed directly or exposed on the portfolio host without privacy/security review, environment-secret rotation, fake-data seeding and isolated dependency auditing. No backend or medical-system instance was launched for this visual task. The new throwaway clone used for source inspection should be removed once the two source images have been copied, because keeping extra sensitive duplicates on the ASUS would be unnecessary. Git commits contain only image-build code and prose, not medical records, credentials or media.

**Six of six featured project banners completed:** all six project records now have a Wagtail `banner_image`. The homepage carousel and numbered Projects grid both display the complete set, tested on desktop and mobile. The four earlier website entries are a separate archive collection and were not changed.

### Final asset 02 — PriceBridge editorial banner (2026-10-29)

`media/design_exports/02-pricebridge-banner-v1.webp` is a 1600×900 (~64 KB) promotional image built by `scripts/build_pricebridge_banner.py` from **existing actual application screenshots** `media/original_images/pricebridge-desktop-card-scroll180-20261029.webp` and `media/original_images/pricebridge-mobile-card-scroll370-20261029.webp`. It depicts the historical July 2026 evidence-gated smartphone comparison and explicitly states *not live offers*. The outside circuit/data graph background is abstract editorial decoration rather than an additional dataset. The two screenshot records (Wagtail images 28 and 29) are preserved as independent desktop/mobile case-study mockups.

Wagtail banner record 40 was created via `manage.py apply_project_banner --slug pricebridge` and linked to the project without modifying any other project's banner. All six project covers were confirmed to load in the actual `/en/projects/` gallery at desktop width and when each lazy-loaded card enters view on a narrow viewport, with no JavaScript errors or horizontal overflow. The same new image was also verified in the homepage carousel. A SQLite/media backup was taken before the CMS change.
