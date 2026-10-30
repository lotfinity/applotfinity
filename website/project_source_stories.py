"""Reviewed editorial snapshots of public engineering repositories (2026-10-30).

These data are presentation-only and contain no connection credentials or live
performance claims. Wagtail body paragraphs remain editor-controlled.
"""

STORIES = {
    "ohmlet": {
        "title": "Ohmlet — 3D Circuit & ESP32 Workbench",
        "description": "A browser-based 3D breadboard laboratory combining analog and digital circuit simulation, a wireable FireBeetle ESP32-E, experimental firmware co-simulation, verified MCP workbench control and studio-grade rendering.",
        "focus": "Hardware Simulation / Embedded Systems",
        "verified": "16 October 2026",
        "sha": "8ddf7388b3e4fbaf143a5826e585f3ee27570c5e",
        "intro": "From visual circuit assembly to a software-defined electronics workbench.",
        "summary": "Ohmlet pairs realistic 3D breadboards with electrical and digital simulation, then opens the same workbench to hardware models, agent control and experimental ESP32 firmware execution.",
        "accent": "cyan",
        "features": [
            "3D breadboard bench with 400–1660 point boards, multi-board grids and collision-aware wiring",
            "Hybrid analog MNA and digital behavior simulation, with instruments and an oscilloscope",
            "Performance, Enhanced and progressive Studio path-traced rendering modes",
            "Wireable FireBeetle ESP32-E and GPIO-oriented learning circuits",
            "Experimental ESP32 firmware co-simulation through a WebAssembly runtime and isolated compiler",
            "MCP workbench service for verified circuit editing with live browser synchronization",
            "Photo-derived ALS-001 RGB controller and PWM circuit example",
        ],
        "highlights": [
            (
                "BUILD",
                "3D circuit bench",
                "Wire, route and inspect circuits in a browser",
            ),
            (
                "SIMULATE",
                "Mixed signals",
                "Analog components and behavioral logic",
            ),
            (
                "EMBED",
                "ESP32 prototype",
                "FireBeetle wiring and firmware co-simulation",
            ),
            (
                "AUTOMATE",
                "MCP workbench",
                "Controlled programmatic edits and browser sync",
            ),
        ],
        "flow": [
            ("Place", "3D board & components"),
            ("Wire", "Validated routes and nodes"),
            ("Solve", "MNA + digital models"),
            ("Observe", "Meters & scope"),
            ("Extend", "FireBeetle / firmware"),
            ("Control", "MCP & UI"),
        ],
        "milestones": [
            (
                "2026-10-16",
                "8ddf7388b3e4fbaf143a5826e585f3ee27570c5e",
                "Physical board defaults",
                "400-point board and updated lessons",
            ),
            (
                "2026-10-16",
                "7e566715c",
                "Firmware co-simulation",
                "Arduino ESP32 execution prototype",
            ),
            (
                "2026-10-15",
                "531118893",
                "RGB control",
                "Photo-derived ALS-001 board and PWM behavior",
            ),
            (
                "2026-10-14",
                "875dac366",
                "MCP editing",
                "Workbench service and live browser synchronization",
            ),
        ],
        "caveat": "Firmware co-simulation and AI-assisted circuit creation are experimental software capabilities; they do not imply validated physical hardware or a certified electrical design. The public repository has later local ASUS work-in-progress that is deliberately not presented here as GitHub-released functionality.",
        "body": [
            (
                "Design philosophy",
                "Physical intuition without requiring a physical breadboard. Component shapes, clear wiring paths, movable instruments and three rendering pipelines allow the same circuit to be explored as a working schematic and as a near-photographic scene.",
            ),
            (
                "Simulation engine",
                "The engine mixes modified nodal analysis for analog nets with behavioral models for digital ICs and instruments. The source documents LU solving, nonlinear device iteration and reactive integration; simulated values are model outputs, not lab measurements.",
            ),
            (
                "From FireBeetle to firmware",
                "The October changes added a wireable FireBeetle 2 ESP32-E, GPIO simulation, photo-derived hardware components and an Arduino/ESP32 WebAssembly co-simulation prototype. An isolated compiler is part of the experimental flow; firmware support should be read as a prototype rather than all ESP32 peripherals being implemented.",
            ),
            (
                "Agent-controllable workbench",
                "The MCP server can receive structured circuit-edit operations and synchronize changes with a browser session. This creates a useful bridge between an assistant and a visually inspectable electronics bench. Source-side validation does not replace electrical safety testing.",
            ),
            (
                "Rendering as a design tool",
                "A low-cost raster Performance mode, Enhanced mode with postprocessing, and progressively path-traced Studio mode let users trade speed for visual quality. High fidelity is a still-image workflow, not evidence of electrical accuracy.",
            ),
        ],
    },
    "pricebridge": {
        "title": "PriceBridge — Evidence-Based Market Intelligence",
        "description": "A Django smartphone-market research pipeline that keeps raw listing evidence, canonical device identities and listing-level Algeria/Türkiye comparisons separate. Unverified matches remain in review rather than becoming confident price claims.",
        "focus": "Data Engineering / Market Evidence",
        "verified": "20 July 2026",
        "sha": "82d227272622d86efa9cb0384e8dae2af0486234",
        "intro": "A price comparison is only as trustworthy as its underlying match.",
        "summary": "PriceBridge is a Django ingestion and comparison pipeline: capture listings, resolve exact Samsung/iPhone variants, preserve evidence and compute an opportunity only when the comparison is sufficiently grounded.",
        "accent": "mint",
        "features": [
            "Evidence-first raw listing intake with review states and provenance",
            "Canonical Samsung and iPhone model / storage-variant matching gate",
            "Strict JSON extraction for Instagram evidence and deduplicated imports",
            "Sahibinden visible-row imports via user-controlled Chrome CDP",
            "Listing-level opportunity snapshots only for exact trusted variant matches",
            "Stored foreign-exchange inputs and Türkiye market references, not guaranteed live prices",
        ],
        "highlights": [
            (
                "CAPTURE",
                "Raw evidence",
                "Preserved listings and source context",
            ),
            (
                "NORMALIZE",
                "Canonical catalog",
                "Model and storage-variant matching",
            ),
            (
                "REVIEW",
                "Ambiguous identities",
                "Do not guess an uncertain device",
            ),
            (
                "COMPARE",
                "Opportunity snapshot",
                "Only when exact trusted evidence exists",
            ),
        ],
        "flow": [
            ("Ingest", "Instagram / Sahibinden"),
            ("Extract", "Structured fields"),
            ("Resolve", "Canonical device variant"),
            ("Review", "Reject ambiguity"),
            ("Compare", "Trusted market + FX"),
            ("Present", "Historical opportunity"),
        ],
        "milestones": [
            (
                "2026-07-20",
                "82d227272622d86efa9cb0384e8dae2af0486234",
                "Initial public source",
                "Django catalog, intake and opportunity pipeline",
            ),
        ],
        "caveat": "The GitHub repository has one public commit as checked on 30 October 2026. The private ASUS Docker preview includes additional local work and historical July 2026 data; neither should be mistaken for a published GitHub release, live feed, guaranteed deal or independently verified current prices.",
        "body": [
            (
                "Why identity comes first",
                "A phone model name is not a market match: storage capacity, variant and trust in the source matter. PriceBridge gates imports against an existing canonical catalog and sends uncertain identities to review instead of silently creating models.",
            ),
            (
                "Preserving provenance",
                "The pipeline separates immutable RawListing records, extraction results, CleanListing records and OpportunitySnapshot calculations. Instagram Markdown imports deduplicate on profile plus shortcode; incomplete snapshots are not presented as exact comparisons.",
            ),
            (
                "A measured market workflow",
                "Visible Sahibinden result rows can be imported from a user-controlled browser session. Comparisons use stored foreign-exchange inputs and trusted Türkiye evidence with listing-level calculations. Historical values are deliberately labeled as such.",
            ),
            (
                "What the preview proves",
                "Real browser captures show the application interface with a historical smartphone listing. A captured screen proves the UI was rendered; it does not prove every record was refreshed or that a current cross-border purchase would be profitable.",
            ),
        ],
    },
    "neon-strip-studio": {
        "title": "Neon Strip Studio — Cross-Platform Light Design",
        "description": "A visual editor and screensaver player for one continuous 150-group WLED neon strip. Shape editing, recorded playback and portable JSON designs connect a browser editor to Windows, GNOME Linux and Android players.",
        "focus": "IoT / Visual Tools / Cross-Platform",
        "verified": "21 October 2026",
        "sha": "89e5e8e9530ea53f8fde8eafe5a028923ffaccfe",
        "intro": "One LED design, multiple screens and a consistent geometry.",
        "summary": "Neon Strip Studio lets a physical 150-group installation be approximated, edited, played back and transferred as a shared layout between browser, desktop screensavers and Android.",
        "accent": "violet",
        "features": [
            "150-group geometry: 120 perimeter points plus 30 linking/inner points",
            "Editable spline curves, LED offsets, direction, portrait orientation and undo",
            "Portable JSON designs with optional recorded color playback",
            "WLED Peek preview/recording integration and explicit synthetic offline demo",
            "Windows, GNOME Linux and Android player source with distinct integration paths",
            "One WebGL mesh with a color texture and fallback Canvas renderer for older GPUs",
            "Compatibility mode and rendering-load reductions for legacy graphics",
        ],
        "highlights": [
            (
                "DESIGN",
                "150 LED groups",
                "Edit perimeter and infinity geometry",
            ),
            (
                "PREVIEW",
                "WLED Peek",
                "Live stream when a controller is available",
            ),
            (
                "RECORD",
                "Portable JSON",
                "Keep shape, settings and color recording",
            ),
            ("PLAY", "Three platforms", "Windows, GNOME and Android source"),
        ],
        "flow": [
            ("Draw", "Curves & LED offsets"),
            ("Preview", "WebGL / Canvas"),
            ("Connect", "WLED Peek"),
            ("Capture", "Up to two minutes"),
            ("Export", "Design JSON"),
            ("Replay", "Local desktop / Android"),
        ],
        "milestones": [
            (
                "2026-10-21",
                "89e5e8e9530ea53f8fde8eafe5a028923ffaccfe",
                "Compatibility",
                "Reduce render load on older hardware",
            ),
            (
                "2026-10-21",
                "11ddd467c84976a0642bee9a21d375e18aa1b446",
                "Factory geometry",
                "Use the supplied strip design as default",
            ),
            (
                "2026-10-21",
                "8c5c90cdbb0644f3da3768be4a60e08c508b24fe",
                "Cross-platform source",
                "Publish editor and screensaver players",
            ),
        ],
        "caveat": "The published source describes a personal test release. Windows startup and browser editing were checked; Android/GNOME packages and physical WLED connectivity were not verified on target hardware. Offline screenshots are synthetic demos, not recorded LED evidence. Source is published without an open-source license grant.",
        "body": [
            (
                "The strip as editable geometry",
                "Instead of drawing disconnected light segments, the editor models a single continuous addressable strip. The default profile contains 120 perimeter groups and 30 for the lead and infinity portion, with adjustable control points and orientation.",
            ),
            (
                "One design, many players",
                "Layout settings, offsets and optional color recording travel in a JSON design. Windows and GNOME players are packaged through a desktop host; Android uses a WebView-based DreamService screensaver. Installation and operating-system idle integration are distinct from rendering in a browser.",
            ),
            (
                "Live vs recorded vs demonstration",
                "A controller connection requests WLED Peek frames. Up to two minutes of colors can be recorded for offline replay. Without a recording or controller, the player uses a labeled synthetic rainbow demo; it does not suggest that an ESP32 or physical LEDs were connected.",
            ),
            (
                "Rendering budget",
                "The app uses a compact WebGL mesh with a 150-pixel color texture. A Canvas fallback and a lower-power compatibility path serve older GPUs, reflecting the lessons learned from testing graphics limitations.",
            ),
        ],
    },
    "istanbulproptech": {
        "title": "IstanbulPropTech — Geographic Property Explorer",
        "description": "A Django map-oriented property explorer combining listing context with local amenities, transit and hierarchical store filtering. Category and named-store selections refine which places appear on the map.",
        "focus": "Geospatial Apps / Django",
        "verified": "14 November 2025",
        "sha": "ba303b73d823839c357b3e3bb3bb07cf05d78d7c",
        "intro": "Turn location layers into useful neighborhood context.",
        "summary": "IstanbulPropTech combines geolocated property data and surrounding place layers with a map interface designed for filtering areas and exploring what matters around a listing.",
        "accent": "emerald",
        "features": [
            "Hierarchical store categories with individual business-selection checkboxes",
            "Map filtering for grocery, clothing and other store types",
            "Property, store, transit and education data layers in a Django application",
            "Cached closest-store lookup and configurable display behavior in the source",
            "Mobile-focused map controls and documentation of filter behavior",
            "Extensive technical handoff notes and implementation checklists",
        ],
        "highlights": [
            (
                "EXPLORE",
                "Property context",
                "Listings connected to geographic layers",
            ),
            (
                "FILTER",
                "Store hierarchy",
                "Types, names and individual locations",
            ),
            (
                "CONTEXT",
                "Local amenities",
                "Retail, transit and education layers",
            ),
            (
                "OPTIMIZE",
                "Cached proximity",
                "Reuse closest-store computations",
            ),
        ],
        "flow": [
            ("Choose", "Location / listing"),
            ("Load", "Map layers"),
            ("Expand", "Category of stores"),
            ("Select", "Named businesses"),
            ("Update", "Visible map markers"),
            ("Explore", "Area context"),
        ],
        "milestones": [
            (
                "2025-11-14",
                "ba303b73d823839c357b3e3bb3bb07cf05d78d7c",
                "Public source snapshot",
                "Project documentation and Django layers",
            ),
            (
                "2025-11-14",
                "b5861d10dcd9679fb448c11da15088846daadb3b",
                "Initial repository record",
                "Earlier source baseline",
            ),
        ],
        "caveat": "The public GitHub repository was last updated in November 2025. Several README files claim production readiness, but no deployment, current property inventory or live map backend was independently verified here. Existing screenshots are owner-supplied design references, not proof of live listing accuracy.",
        "body": [
            (
                "Filtering with a mental model",
                "Instead of making visitors toggle every store individually, hierarchical controls allow filtering an entire category first, then expanding to specific stores. The map responds as the selection changes.",
            ),
            (
                "More than listings",
                "Django code is organized into property listings, stores, transit and education layers, making the map a neighborhood-context tool rather than simply a collection of property pins.",
            ),
            (
                "Reuse expensive geographic work",
                "The source documents closest-store cache logic and display configuration, allowing repeated proximity lookups to be reused. Performance numbers depend on deployment and dataset size, neither of which was independently benchmarked here.",
            ),
            (
                "Design and evidence status",
                "The existing desktop and mobile images illustrate an intended user experience. The GitHub repository describes working implementation components, while the displayed places and property prices should not be treated as verified current inventory.",
            ),
        ],
    },
    "beyond-website": {
        "title": "Beyond Website — BeyondClinic Service Portal",
        "description": "An exploratory Django healthcare-service and operations portal bringing together patient-facing dashboard modules, appointments, messages, prescriptions, referrals and administrative workflows in one interface.",
        "focus": "Healthcare Software / Operations",
        "verified": "28 July 2025",
        "sha": "f77d0fee94ecc95e0135d0a6fe444402ddf52662",
        "intro": "A business portal is a connected service workflow, not just a homepage.",
        "summary": "BeyondClinic explores a unified Django dashboard for patient communications, appointment coordination, prescriptions, referrals, accommodation and scheduling alongside internal administrative tools.",
        "accent": "indigo",
        "features": [
            "Patient dashboard cards for messages, appointments and prescriptions",
            "Referral and balance-related service modules",
            "Accommodation, flight-reservation and schedule dashboard modules",
            "Administrative interface and guided dashboard tour components",
            "Server-rendered Django templates organized by reusable dashboard includes",
            "Archived desktop and mobile interface references retained separately in the case study",
        ],
        "highlights": [
            (
                "COMMUNICATE",
                "Messages",
                "Dashboard entry point for conversations",
            ),
            (
                "COORDINATE",
                "Appointments",
                "Patient service scheduling context",
            ),
            ("MANAGE", "Referrals", "Balances and referral functionality"),
            (
                "OPERATE",
                "Travel + schedules",
                "Accommodation and flight modules",
            ),
        ],
        "flow": [
            ("Enter", "Patient portal"),
            ("Review", "Dashboard modules"),
            ("Coordinate", "Messages / visits"),
            ("Support", "Referrals / balance"),
            ("Arrange", "Travel & lodging"),
            ("Operate", "Administrative processes"),
        ],
        "milestones": [
            (
                "2025-07-28",
                "f77d0fee94ecc95e0135d0a6fe444402ddf52662",
                "Latest source snapshot",
                "Django service portal / dashboard source",
            ),
            (
                "2025-07-25",
                "130fdc6ae4f07934a5720e602cd822094dd00c11",
                "Earlier source baseline",
                "Initial published project state",
            ),
        ],
        "caveat": "These modules are visible in repository templates, not proof of deployment or reliable operational integrations. The repository contains potentially sensitive development artifacts and must not be deployed unchanged. Screenshots are archived source references, not patient records or a live production session.",
        "body": [
            (
                "Services as one coordinated experience",
                "The dashboard collects messages, appointments, prescriptions, balances and referrals into reusable server-rendered cards. Additional components surface accommodation, flight reservations and schedules.",
            ),
            (
                "Reusable interface and process design",
                "The code includes dashboard partials and guided-tour support, aiming for consistent entry points across multiple patient-service actions rather than isolated application pages.",
            ),
            (
                "Internal workflows matter too",
                "Django administration and service modules illustrate the operational side of a portal: keeping customer-facing requests and back-office processes aligned.",
            ),
            (
                "Security and verification boundaries",
                "This is a source-backed interface and workflow case study. Deployment, real patient data handling and medical integration are not demonstrated here; development credentials and private records must be removed and reviewed before any production rollout.",
            ),
        ],
    },
}
