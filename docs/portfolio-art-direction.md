# Lotfinity numbered project-banner series

The homepage carousel and `/en/projects/` cards are powered by Wagtail `AppPage` records. The **banner_image** field is deliberately separate from `mockup_design`, `device_desktop_image` and `device_mobile_image`: a banner is an editorial illustration, whereas the other fields must contain genuine application screenshots. The featured-project list is numbered from 01 through the current total and is sorted by `display_order`; archived entries are not part of the count.

## Proposed visual brief, reviewed one project at a time

| Number | Project | Banner purpose and verified functionality | Proposed color direction | Screenshot status |
| --- | --- | --- | --- | --- |
| 01 | Ohmlet | 3D breadboard, wiring, analog/digital simulation, AI-assisted circuit creation | Midnight navy `#071426`, signal cyan `#46D0EE`, silver | Existing verified desktop workbench screenshot; v1 banner created and Wagtail-linked. No mobile screenshot yet. |
| 02 | PriceBridge | Mobile listing aggregation, matching, historical evidence and price comparisons | Dark ocean `#0B2032`, bright mint `#57D7AE`, ice white | Capture from actual repository or deployed preview before creating mockups. |
| 03 | LotoT | Android OBD-II diagnostics, sensor context, React cockpit, MQTT | Charcoal `#101B27`, telemetry amber `#FFAA58`, cyan | Collect authentic app screens from installed APK or a running emulator. Not fleet-tracking software. |
| 04 | Neon Strip Studio | WLED layout editing, color strips, playback and transferable designs | Ink `#11152B`, electric magenta `#C755F5`, cyan | Use actual editor or WLED design screenshots. |
| 05 | IstanbulPropTech | Property and neighborhood exploration using map layers and filters | Midnight plum `#17162F`, violet `#AE8AF1`, teal | Actual desktop and mobile screenshots already exist in Wagtail. |
| 06 | Beyond Website | Django business portals, staff workflows and administrative integration | Slate `#102735`, warm gold `#F0B777`, teal | Gather actual project UI/screenshots rather than inventing working dashboards. |

All palettes above are starting points, not claims about uninspected application UIs. The four historical projects can be treated as an optional second collection after the six current featured projects have been approved.

## Deliverables per project

1. **Banner**: 1600×900 WebP, high contrast, large numbered identity, accurate app purpose and matched palette. Designed illustration or collage allowed, but no fabricated statistics or features. The homepage carousel and numbered projects index use this banner.
2. **Desktop / mobile mockups**: CSS device frames supplied by the website with **real screenshots** inside. No invented or stretched mobile UI. Attach only captures appropriate to that viewport.
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

**PriceBridge promotional banner remains pending**: it should combine genuine screenshots with an accurate deep-blue/mint-green editorial graphic. Do not imply the deployed app already contains fully populated live market intelligence. The original PriceBridge GitHub repository was not modified or pushed as part of the private Docker-preview setup.
