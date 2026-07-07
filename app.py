import time
import base64
from pathlib import Path

import streamlit as st
import plotly.graph_objects as go

st.set_page_config(
    page_title="Job Pulache · Analista de Operaciones y Procesos",
    page_icon="🌾",
    layout="wide",
    initial_sidebar_state="collapsed",
)

ASSETS = Path(__file__).parent / "assets"


def img_b64(name: str) -> str:
    p = ASSETS / name
    if not p.exists():
        return ""
    return base64.b64encode(p.read_bytes()).decode()


PHOTO_NATURAL = img_b64("profile_natural.jpg")
PHOTO_DUOTONE = img_b64("profile_duotone.jpg")

# ----------------------------------------------------------------------------
# THEME STATE
# ----------------------------------------------------------------------------
if "theme" not in st.session_state:
    st.session_state.theme = "dark"

_qp_theme = st.query_params.get("theme")
if _qp_theme in ("dark", "light"):
    st.session_state.theme = _qp_theme

THEME = st.session_state.theme
THEME_OTHER = "light" if THEME == "dark" else "dark"

if THEME == "dark":
    C = dict(
        bg="#0E1210",
        bg_alt="#141B18",
        card="#131916",
        card_hover="#171F1B",
        text="#E7EFE9",
        text_dim="#8FA79A",
        text_faint="#576760",
        accent="#4FD183",
        accent_2="#E8C468",
        border="rgba(231,239,233,0.10)",
        border_strong="rgba(79,209,131,0.35)",
        grid_line="rgba(79,209,131,0.06)",
        shadow="0 20px 60px rgba(0,0,0,0.45)",
        mode_label="MODO_NOCTURNO",
        toggle_icon="☾",
    )
else:
    C = dict(
        bg="#F3F1E7",
        bg_alt="#EAE7D9",
        card="#FCFBF6",
        card_hover="#FFFFFF",
        text="#14181A",
        text_dim="#4B5750",
        text_faint="#8A9187",
        accent="#2E6B45",
        accent_2="#9C6B1F",
        border="rgba(20,24,26,0.10)",
        border_strong="rgba(46,107,69,0.35)",
        grid_line="rgba(46,107,69,0.07)",
        shadow="0 20px 50px rgba(20,24,26,0.08)",
        mode_label="MODO_DIURNO",
        toggle_icon="☀",
    )

# ----------------------------------------------------------------------------
# GLOBAL CSS
# ----------------------------------------------------------------------------
st.markdown(
    f"""
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=Public+Sans:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">

<style>
:root {{
    --bg: {C['bg']};
    --bg-alt: {C['bg_alt']};
    --card: {C['card']};
    --card-hover: {C['card_hover']};
    --text: {C['text']};
    --text-dim: {C['text_dim']};
    --text-faint: {C['text_faint']};
    --accent: {C['accent']};
    --accent-2: {C['accent_2']};
    --border: {C['border']};
    --border-strong: {C['border_strong']};
    --grid-line: {C['grid_line']};
    --shadow: {C['shadow']};
}}

#MainMenu {{visibility: hidden;}}
footer {{visibility: hidden;}}
header[data-testid="stHeader"] {{background: transparent;}}
div[data-testid="stToolbar"] {{visibility: hidden;}}
div[data-testid="stDecoration"] {{display:none;}}

html, body, [class*="css"] {{
    font-family: 'Public Sans', sans-serif;
}}

[data-testid="stAppViewContainer"] {{
    background-color: var(--bg);
    background-image:
        linear-gradient(var(--grid-line) 1px, transparent 1px),
        linear-gradient(90deg, var(--grid-line) 1px, transparent 1px);
    background-size: 42px 42px;
    color: var(--text);
    transition: background-color 0.4s ease, color 0.4s ease;
}}

[data-testid="stAppViewContainer"] > .main {{ padding-top: 0rem; }}

.block-container {{
    max-width: 1180px;
    padding-top: 1.2rem;
    padding-bottom: 4rem;
}}

h1, h2, h3, h4 {{ font-family: 'Space Mono', monospace; letter-spacing: -0.01em; }}

::-webkit-scrollbar {{ width: 10px; }}
::-webkit-scrollbar-track {{ background: var(--bg); }}
::-webkit-scrollbar-thumb {{ background: var(--border-strong); border-radius: 0px; }}

.mono {{ font-family: 'Space Mono', monospace; }}
.tag {{
    display:inline-block;
    font-family:'Space Mono', monospace;
    font-size: 0.72rem;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: var(--accent);
    border: 1px solid var(--border-strong);
    padding: 3px 10px;
    border-radius: 2px;
    background: color-mix(in srgb, var(--accent) 8%, transparent);
}}

.status-dot {{
    display:inline-block; width:7px; height:7px; border-radius:50%;
    background: var(--accent); margin-right:7px;
    box-shadow: 0 0 8px var(--accent);
    animation: blink 1.8s infinite;
}}
@keyframes blink {{ 0%,100%{{opacity:1}} 50%{{opacity:0.25}} }}

/* ---- Hero ---- */
.hero-eyebrow {{
    font-family:'Space Mono', monospace;
    color: var(--text-dim);
    font-size: 0.85rem;
    letter-spacing: 0.05em;
    margin-bottom: 10px;
}}
.hero-eyebrow::before {{ content: "> "; color: var(--accent); }}
.hero-title {{
    font-family:'Space Mono', monospace;
    font-weight: 700;
    font-size: clamp(2.1rem, 5vw, 3.6rem);
    line-height: 1.08;
    margin: 0 0 6px 0;
    color: var(--text);
}}
.hero-title .accent {{ color: var(--accent); }}
.hero-role {{
    font-size: 1.08rem;
    color: var(--text-dim);
    max-width: 580px;
    line-height: 1.65;
    margin-bottom: 20px;
}}
.hero-role b {{ color: var(--text); font-weight: 600; }}
.hero-cursor {{
    display:inline-block; width:10px; height:1.15em; background: var(--accent);
    vertical-align: middle; margin-left: 4px;
    animation: blink 1s steps(2) infinite;
}}
.photo-frame {{
    position: relative;
    border: 1px solid var(--border-strong);
    padding: 10px;
    background: var(--card);
    box-shadow: var(--shadow);
}}
.photo-frame img {{ width: 100%; display:block; filter: saturate(0.96) contrast(1.03); }}
.photo-frame .corner {{ position:absolute; width:14px; height:14px; border-color: var(--accent); border-style: solid; }}
.photo-frame .tl {{ top:-1px; left:-1px; border-width: 2px 0 0 2px; }}
.photo-frame .br {{ bottom:-1px; right:-1px; border-width: 0 2px 2px 0; }}
.photo-caption {{
    font-family:'Space Mono', monospace; font-size: 0.72rem; color: var(--text-faint);
    margin-top: 8px; display:flex; justify-content: space-between;
}}

/* ---- Hero status panel (mini dashboard) ---- */
.hero-status {{
    background: var(--card);
    border: 1px solid var(--border-strong);
    padding: 4px 18px;
    margin-top: 6px;
}}
.hero-status .result-field:last-child {{ border-bottom: none; }}

/* ---- Section headers ---- */
.sec-num {{ font-family:'Space Mono', monospace; color: var(--accent); font-size: 0.85rem; }}
.sec-title {{ font-size: 1.55rem; font-weight: 700; margin: 2px 0 4px 0; color: var(--text); }}
.sec-sub {{ color: var(--text-dim); font-size: 0.95rem; margin-bottom: 22px; max-width: 640px; }}

/* ---- Generic panel card (exec profile, capability matrix, kpi-style slots) ---- */
.panel-card {{
    background: var(--card);
    border: 1px solid var(--border);
    border-left: 2px solid var(--accent);
    padding: 18px 20px;
    height: 100%;
    transition: border-color 0.25s ease, transform 0.25s ease, background 0.25s ease;
}}
.panel-card:hover {{ border-color: var(--border-strong); transform: translateY(-2px); background: var(--card-hover); }}
.panel-card .glyph {{ font-size: 1.3rem; color: var(--accent); margin-bottom: 10px; display:block; }}
.panel-card .p-title {{ font-weight: 700; font-size: 1rem; color: var(--text); margin-bottom: 6px; }}
.panel-card .p-body {{ color: var(--text-dim); font-size: 0.86rem; line-height: 1.55; }}

/* ---- Badges (tier system, no invented numbers) ---- */
.badge {{
    display:inline-block;
    font-family:'Space Mono', monospace;
    font-size: 0.66rem;
    letter-spacing: 0.08em;
    padding: 3px 9px;
    border-radius: 2px;
    margin-bottom: 10px;
}}
.badge-core {{ background: var(--accent); color: var(--bg); font-weight:700; }}
.badge-solid {{ border: 1px solid var(--border-strong); color: var(--accent); }}
.badge-growth {{ border: 1px dashed var(--border-strong); color: var(--text-dim); }}

/* ---- Cards (case studies) ---- */
.case-card {{
    background: var(--card);
    border: 1px solid var(--border);
    padding: 26px 26px 22px 26px;
    height: 100%;
    transition: border-color 0.25s ease, transform 0.25s ease;
}}
.case-card:hover {{ border-color: var(--border-strong); transform: translateY(-3px); }}
.case-card .idx {{ font-family:'Space Mono', monospace; color: var(--accent); font-size: 0.8rem; margin-bottom: 10px; }}
.case-card h4 {{ font-size: 1.15rem; margin: 0 0 4px 0; }}
.case-card .co {{
    font-family:'Space Mono', monospace; font-size: 0.78rem; color: var(--text-faint);
    margin-bottom: 14px; letter-spacing: 0.04em;
}}
.case-card .block-label {{
    font-family:'Space Mono', monospace; font-size: 0.68rem; letter-spacing: 0.1em;
    color: var(--accent); margin-top: 12px; margin-bottom: 4px; display:flex; align-items:center; gap:6px;
}}
.case-card .block-label::before {{ content: ""; width:12px; height:1px; background: var(--border-strong); }}
.case-card .impact {{
    margin-top: 14px; padding: 10px 12px;
    background: color-mix(in srgb, var(--accent) 7%, transparent);
    border-left: 2px solid var(--accent);
    font-size: 0.86rem; color: var(--text);
}}
.case-card p {{ color: var(--text-dim); font-size: 0.9rem; line-height: 1.55; margin: 0; }}
.chip {{
    display:inline-block; font-family:'Space Mono', monospace; font-size: 0.68rem;
    color: var(--text-dim); border: 1px solid var(--border); padding: 2px 8px; margin: 3px 6px 0 0;
}}

/* ---- Narrative rail (storytelling thread) ---- */
.rail {{
    display:flex; align-items:stretch; gap:0; margin: 10px 0 8px 0;
    border: 1px solid var(--border); background: var(--card);
    overflow-x: auto;
}}
.rail a {{
    flex: 1; min-width: 150px; display:flex; flex-direction:column; gap:4px;
    padding: 14px 16px; text-decoration:none; color: var(--text-dim);
    border-right: 1px solid var(--border);
    transition: background 0.2s ease, color 0.2s ease;
}}
.rail a:last-child {{ border-right:none; }}
.rail a:hover {{ background: color-mix(in srgb, var(--accent) 6%, transparent); color: var(--text); }}
.rail .step-idx {{ font-family:'Space Mono', monospace; font-size:0.68rem; color: var(--accent); }}
.rail .step-lbl {{ font-family:'Space Mono', monospace; font-size:0.82rem; color: inherit; }}

/* ---- Timeline ---- */
.tl-row {{ display:flex; gap: 18px; padding: 16px 0; border-bottom: 1px solid var(--border); }}
.tl-row:last-child {{ border-bottom: none; }}
.tl-date {{ font-family:'Space Mono', monospace; font-size: 0.78rem; color: var(--accent); min-width: 130px; padding-top: 2px; }}
.tl-content .skill-title {{ margin: 0 0 3px 0; font-size: 1.05rem; font-weight:700; color:var(--text); font-family:'Space Mono',monospace; }}
.tl-content .role {{ color: var(--text-faint); font-size: 0.8rem; margin-bottom: 6px; letter-spacing:0.03em; }}

/* ---- Demo / enterprise module panel ---- */
.demo-panel {{ background: var(--card); border: 1px solid var(--border-strong); padding: 22px 24px; }}
.demo-terminal-head {{
    display:flex; align-items:center; gap:8px; margin-bottom: 14px;
    font-family:'Space Mono', monospace; font-size: 0.75rem; color: var(--text-faint);
}}
.dot {{ width:9px; height:9px; border-radius:50%; display:inline-block; }}
.result-field {{ display:flex; justify-content: space-between; padding: 9px 0; border-bottom: 1px dashed var(--border); font-size: 0.88rem; }}
.result-field .k {{ color: var(--text-faint); font-family:'Space Mono', monospace; font-size:0.75rem; }}
.result-field .v {{ color: var(--text); font-weight: 600; text-align:right; }}
.status-pill {{
    font-family:'Space Mono', monospace; font-size: 0.68rem; padding: 2px 9px;
    background: color-mix(in srgb, var(--accent) 16%, transparent); color: var(--accent); font-weight:700;
}}

/* Streamlit native components, retheme to match */
[data-testid="stStatusWidget"], [data-testid="stStatus"] {{
    background: var(--card) !important;
    border: 1px solid var(--border-strong) !important;
    border-radius: 0px !important;
}}
[data-testid="stStatus"] p, [data-testid="stStatus"] span {{
    font-family: 'Space Mono', monospace !important;
    font-size: 0.82rem !important;
}}
div[data-testid="stMetric"] {{
    background: var(--card);
    border: 1px solid var(--border);
    border-left: 2px solid var(--accent);
    padding: 12px 16px;
}}
div[data-testid="stMetricLabel"] {{ font-family:'Space Mono', monospace !important; color: var(--text-dim) !important; }}
div[data-testid="stMetricValue"] {{ font-family:'Space Mono', monospace !important; color: var(--text) !important; }}
.stProgress > div > div {{ background-color: var(--accent) !important; }}

/* ---- Buttons ---- */
.stButton>button {{
    font-family: 'Space Mono', monospace !important;
    background: transparent !important;
    color: var(--text) !important;
    border: 1px solid var(--border-strong) !important;
    border-radius: 0px !important;
    padding: 8px 18px !important;
    font-size: 0.8rem !important;
    letter-spacing: 0.04em;
    transition: all 0.2s ease;
}}
.stButton>button:hover {{ background: var(--accent) !important; color: var(--bg) !important; border-color: var(--accent) !important; }}
.stButton>button:focus:not(:active) {{ color: var(--text) !important; }}

[data-testid="stSelectbox"] label {{
    font-family:'Space Mono', monospace !important; font-size: 0.78rem !important;
    color: var(--text-dim) !important; text-transform: uppercase; letter-spacing: 0.06em;
}}

.footbar {{
    margin-top: 60px; padding-top: 22px; border-top: 1px solid var(--border);
    display:flex; justify-content: space-between; align-items:center;
    font-family:'Space Mono', monospace; font-size: 0.75rem; color: var(--text-faint);
    flex-wrap: wrap; gap: 10px;
}}
.footbar a {{ color: var(--text-dim); text-decoration:none; }}
.footbar a:hover {{ color: var(--accent); }}
a.linklike {{ color: var(--accent) !important; text-decoration: none; border-bottom: 1px solid var(--border-strong); }}

/* ---- Reveal-on-scroll microinteraction ----
   Visible by default: the animation is a bonus for when the observer fires in time,
   never a condition for the content to be seen (avoids blank gaps on slow loads/reruns). */
.reveal {{ opacity: 1; transform: translateY(0); }}
@keyframes revealIn {{ from {{ opacity: 0; transform: translateY(16px); }} to {{ opacity: 1; transform: translateY(0); }} }}
.reveal.in-view {{ animation: revealIn 0.6s ease; }}

/* Responsive stacking */
@media (max-width: 900px) {{
    [data-testid="stHorizontalBlock"] {{ flex-wrap: wrap !important; }}
    [data-testid="stHorizontalBlock"] > div {{ min-width: 100% !important; flex: 1 1 100% !important; }}
    .hero-title {{ font-size: 2.1rem; }}
    .rail {{ flex-direction: column; }}
    .rail a {{ border-right:none; border-bottom: 1px solid var(--border); }}
    .rail a:last-child {{ border-bottom:none; }}
}}

/* ============================================================
   NAV — fixed top bar (desktop) + floating dock (mobile)
   ============================================================ */
[id] {{ scroll-margin-top: 84px; }}

.jp-topnav {{
    position: fixed; top: 0; left: 0; right: 0; z-index: 1000;
    display: flex; align-items: center; justify-content: space-between;
    padding: 14px 4vw;
    background: color-mix(in srgb, var(--bg) 82%, transparent);
    backdrop-filter: blur(14px); -webkit-backdrop-filter: blur(14px);
    border-bottom: 1px solid var(--border);
}}
.jp-topnav .jp-brand {{ font-family: 'Space Mono', monospace; font-size: 0.95rem; color: var(--text); white-space: nowrap; }}
.jp-topnav .jp-brand span {{ color: var(--accent); }}
.jp-topnav .jp-links {{ display: flex; align-items: center; gap: 30px; }}
.jp-topnav .jp-links a {{
    display: flex; align-items: center; gap: 7px; color: var(--text-dim); text-decoration: none;
    font-family: 'Space Mono', monospace; font-size: 0.8rem; letter-spacing: 0.02em;
    transition: color 0.2s ease; white-space: nowrap;
}}
.jp-topnav .jp-links a .gl {{ color: var(--accent); font-size: 0.9rem; }}
.jp-topnav .jp-links a:hover, .jp-topnav .jp-links a.active {{ color: var(--text); }}
.jp-topnav .jp-right {{ display:flex; align-items:center; gap:14px; }}
.jp-theme-toggle {{
    display:flex; align-items:center; justify-content:center; width: 34px; height:34px;
    border: 1px solid var(--border-strong); color: var(--text-dim); text-decoration:none;
    font-size: 0.95rem; transition: all 0.2s ease;
}}
.jp-theme-toggle:hover {{ color: var(--accent); border-color: var(--accent); }}
.jp-cta {{
    background: var(--accent); color: var(--bg) !important; font-family: 'Space Mono', monospace;
    font-size: 0.78rem; font-weight: 700; padding: 9px 20px; border-radius: 999px;
    text-decoration: none; letter-spacing: 0.03em; white-space: nowrap; transition: opacity 0.2s ease;
}}
.jp-cta:hover {{ opacity: 0.85; }}
.jp-topnav-spacer {{ height: 70px; }}

@media (max-width: 900px) {{
    .jp-topnav {{ display: none; }}
    .jp-topnav-spacer {{ height: 20px; }}
}}

.jp-dock {{
    display: none; position: fixed; bottom: 18px; left: 50%; transform: translateX(-50%); z-index: 1000;
    align-items: flex-end; gap: 6px; padding: 10px 14px;
    background: color-mix(in srgb, var(--bg) 78%, transparent);
    backdrop-filter: blur(16px); -webkit-backdrop-filter: blur(16px);
    border: 1px solid var(--border); border-radius: 999px; box-shadow: var(--shadow);
}}
.jp-dock a {{
    display: flex; flex-direction: column; align-items: center; gap: 3px; width: 46px;
    color: var(--text-dim); text-decoration: none; font-family: 'Space Mono', monospace;
    font-size: 0.55rem; letter-spacing: 0.02em; transition: all 0.2s ease;
}}
.jp-dock a .dg {{
    display:flex; align-items:center; justify-content:center; width: 36px; height: 36px;
    border-radius: 50%; font-size: 1.05rem; transition: all 0.25s ease;
}}
.jp-dock a.active {{ color: var(--accent); }}
.jp-dock a.active .dg {{ background: var(--accent); color: var(--bg); box-shadow: 0 0 18px var(--accent); transform: translateY(-8px); }}
@media (max-width: 900px) {{
    .jp-dock {{ display: flex; }}
    .block-container {{ padding-bottom: 110px; }}
}}
</style>

<script>
(function() {{
    function initNav() {{
        var ids = ["inicio","perfil","trayectoria","casos","agrobrain","demo","capacidades","contacto"];
        var sections = ids.map(function(id) {{ return document.getElementById(id); }}).filter(Boolean);
        var links = document.querySelectorAll(".jp-navlink");
        function setActive(id) {{
            links.forEach(function(l) {{
                if (l.getAttribute("data-target") === id) {{ l.classList.add("active"); }}
                else {{ l.classList.remove("active"); }}
            }});
        }}
        if (sections.length && links.length) {{
            if (window.__jpObserver) {{ window.__jpObserver.disconnect(); }}
            var obs = new IntersectionObserver(function(entries) {{
                entries.forEach(function(e) {{ if (e.isIntersecting) setActive(e.target.id); }});
            }}, {{ rootMargin: "-35% 0px -55% 0px", threshold: 0 }});
            sections.forEach(function(s) {{ obs.observe(s); }});
            window.__jpObserver = obs;
        }}

        var reveals = document.querySelectorAll(".reveal:not(.in-view)");
        if (reveals.length) {{
            if (window.__jpReveal) {{ window.__jpReveal.disconnect(); }}
            var robs = new IntersectionObserver(function(entries, o) {{
                entries.forEach(function(e) {{
                    if (e.isIntersecting) {{ e.target.classList.add("in-view"); o.unobserve(e.target); }}
                }});
            }}, {{ threshold: 0.12 }});
            reveals.forEach(function(el) {{ robs.observe(el); }});
            window.__jpReveal = robs;
        }}
    }}
    setTimeout(initNav, 200);
}})();
</script>
""",
    unsafe_allow_html=True,
)


# ----------------------------------------------------------------------------
# SMALL HELPERS (reused across sections)
# ----------------------------------------------------------------------------
def section_header(num: str, title: str, subtitle: str = "", anchor: str = "") -> str:
    # Built as one unbroken line: Streamlit's markdown parser can misread multi-line
    # indented HTML blocks and leak a stray closing tag as literal text.
    anchor_html = f'<div id="{anchor}"></div>' if anchor else ""
    sub_html = f'<div class="sec-sub">{subtitle}</div>' if subtitle else ""
    return f'{anchor_html}<div class="sec-num">{num}</div><div class="sec-title">{title}</div>{sub_html}'


def panel_card(glyph: str, title: str, body: str) -> str:
    return (
        f'<div class="panel-card reveal"><span class="glyph">{glyph}</span>'
        f'<div class="p-title">{title}</div><div class="p-body">{body}</div></div>'
    )


def capability_card(domain: str, badge_class: str, badge_label: str, tools: list, note: str) -> str:
    chips = "".join(f'<span class="chip">{t}</span>' for t in tools)
    return (
        f'<div class="panel-card reveal"><span class="badge {badge_class}">{badge_label}</span>'
        f'<div class="p-title">{domain}</div>'
        f'<div class="p-body" style="margin-bottom:10px;">{note}</div>'
        f'<div>{chips}</div></div>'
    )


def case_card(idx_label: str, title: str, org: str, stages: list, chips: list, link: str = "") -> str:
    stage_html = ""
    for label, text in stages[:-1]:
        stage_html += f'<div class="block-label">{label}</div><p>{text}</p>'
    impact_label, impact_text = stages[-1]
    stage_html += (
        f'<div class="impact"><b style="font-family:\'Space Mono\',monospace; font-size:0.68rem; '
        f'letter-spacing:0.08em; color:var(--accent); display:block; margin-bottom:4px;">{impact_label}</b>{impact_text}</div>'
    )
    chip_html = "".join(f'<span class="chip">{c}</span>' for c in chips)
    link_html = (
        f'<div style="margin-top:14px;"><a class="linklike" href="{link}" target="_blank">Ver documentación completa ↗</a></div>'
        if link else ""
    )
    return (
        f'<div class="case-card reveal"><div class="idx">{idx_label}</div>'
        f'<h4>{title}</h4><div class="co">{org}</div>'
        f'{stage_html}'
        f'<div style="margin-top:14px;">{chip_html}</div>'
        f'{link_html}</div>'
    )


# ----------------------------------------------------------------------------
# NAV — fixed top bar (desktop) + floating dock (mobile)
# ----------------------------------------------------------------------------
NAV_ITEMS = [
    ("inicio", "⌂", "Inicio"),
    ("trayectoria", "◷", "Trayectoria"),
    ("casos", "▣", "Casos"),
    ("agrobrain", "◈", "AgroBrain"),
]
nav_links_html = "".join(
    f'<a class="jp-navlink" data-target="{tid}" href="#{tid}"><span class="gl">{glyph}</span>{label}</a>'
    for tid, glyph, label in NAV_ITEMS
)
dock_links_html = "".join(
    f'<a class="jp-navlink" data-target="{tid}" href="#{tid}"><span class="dg">{glyph}</span>{label}</a>'
    for tid, glyph, label in NAV_ITEMS
)
dock_links_html += '<a class="jp-navlink" data-target="contacto" href="#contacto"><span class="dg">✉</span>Contacto</a>'

st.markdown(
    f"""
    <div class="jp-topnav">
        <div class="jp-brand"><span class="status-dot"></span>JOB<span>.</span>PULACHE</div>
        <div class="jp-links">{nav_links_html}</div>
        <div class="jp-right">
            <a class="jp-theme-toggle" href="?theme={THEME_OTHER}" title="Cambiar modo">{C['toggle_icon']}</a>
            <a class="jp-cta" href="#contacto">Contacto</a>
        </div>
    </div>
    <div class="jp-dock">{dock_links_html}</div>
    <div class="jp-topnav-spacer"></div>
    """,
    unsafe_allow_html=True,
)

# ----------------------------------------------------------------------------
# HERO — executive positioning
# ----------------------------------------------------------------------------
st.markdown('<div id="inicio"></div>', unsafe_allow_html=True)
hero_l, hero_r = st.columns([1.3, 1], gap="large")
with hero_l:
    st.markdown(
        """
        <div class="hero-eyebrow">piura, perú &nbsp;·&nbsp; analista de operaciones y procesos</div>
        <div class="hero-title">Job Pulache<br><span class="accent">Carreño</span><span class="hero-cursor"></span></div>
        <div class="hero-role">
            Leo la operación agroindustrial antes que la hoja de cálculo. Entiendo dónde se pierde
            información entre el campo, RRHH y almacén, <b>rediseño el proceso</b> que la captura, y
            cuando el proceso lo justifica, <b>construyo el sistema</b> que lo sostiene.
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown(
        f"""
        <div class="hero-status reveal">
            <div class="result-field"><span class="k">STATUS</span><span class="v" style="color:var(--accent);">● DISPONIBLE PARA NUEVOS ROLES</span></div>
            <div class="result-field"><span class="k">UBICACIÓN</span><span class="v">Piura, Perú</span></div>
            <div class="result-field"><span class="k">FOCO ACTUAL</span><span class="v">Analítica de operaciones agroindustriales</span></div>
            <div class="result-field"><span class="k">PROYECTO EN CURSO</span><span class="v">AgroBrain IA — plataforma de decisión agrícola</span></div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown("<div style='height:20px'></div>", unsafe_allow_html=True)
    b1, b2, b3 = st.columns(3)
    with b1:
        st.link_button("↗ LinkedIn", "https://www.linkedin.com/in/jobpulachecarreno/", width="stretch")
    with b2:
        st.link_button("✆ WhatsApp", "https://wa.me/51930938449", width="stretch")
    with b3:
        st.link_button("✉ Correo", "mailto:pulachecarrenojob@gmail.com", width="stretch")

with hero_r:
    photo_src = f"data:image/jpeg;base64,{PHOTO_NATURAL}" if PHOTO_NATURAL else ""
    st.markdown(
        f"""
        <div class="photo-frame reveal">
            <div class="corner tl"></div>
            <div class="corner br"></div>
            <img src="{photo_src}" alt="Job Pulache Carreño"/>
        </div>
        <div class="photo-caption">
            <span>IMG_PERFIL.JPG</span>
            <span>PIURA / PE</span>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.markdown("<div style='height:34px'></div>", unsafe_allow_html=True)

# ----------------------------------------------------------------------------
# NARRATIVE RAIL — the thread that ties every section together
# ----------------------------------------------------------------------------
RAIL_STEPS = [
    ("01", "Comprender la operación", "#trayectoria"),
    ("02", "Analizar la información", "#casos"),
    ("03", "Optimizar procesos", "#casos"),
    ("04", "Automatizar tareas", "#demo"),
    ("05", "Construir AgroBrain", "#agrobrain"),
]
rail_html = "".join(
    f'<a href="{href}"><span class="step-idx">{idx}</span><span class="step-lbl">{lbl}</span></a>'
    for idx, lbl, href in RAIL_STEPS
)
st.markdown(f'<div class="rail reveal">{rail_html}</div>', unsafe_allow_html=True)
st.markdown(
    '<div style="font-family:\'Space Mono\',monospace; font-size:0.72rem; color:var(--text-faint); margin-bottom:40px;">'
    '&gt; el hilo conductor de todo lo que sigue en esta página</div>',
    unsafe_allow_html=True,
)

# ----------------------------------------------------------------------------
# EXECUTIVE PROFILE — replaces generic KPIs
# ----------------------------------------------------------------------------
st.markdown(
    section_header(
        "01 / PERFIL EJECUTIVO",
        "Cómo pienso, no solo qué hice",
        "Cuatro capacidades que se repiten en cada rol que he tenido, sin importar el nombre del cargo.",
        anchor="perfil",
    ),
    unsafe_allow_html=True,
)
EXEC_PROFILE = [
    ("◉", "Lectura operativa", "Entiendo cómo se mueve la información en campo, planilla y almacén antes de tocar una sola celda."),
    ("◐", "Rigor analítico", "Valido cada dato antes de que llegue a una decisión — el margen de error no es negociable en un reporte gerencial."),
    ("⌁", "Optimización de procesos", "Detecto dónde un proceso pierde tiempo y rediseño el flujo completo, no solo el reporte final."),
    ("◈", "Automatización con criterio", "Cuando el proceso lo justifica, construyo la herramienta — consulta, dashboard o plataforma — que lo sostiene."),
]
ep_cols = st.columns(4)
for col, (glyph, title, body) in zip(ep_cols, EXEC_PROFILE):
    with col:
        st.markdown(panel_card(glyph, title, body), unsafe_allow_html=True)

st.markdown("<div style='height:56px'></div>", unsafe_allow_html=True)

# ----------------------------------------------------------------------------
# TRAYECTORIA — reframed as skills acquired, not job titles
# ----------------------------------------------------------------------------
tl_l, tl_r = st.columns([1, 1.15], gap="large")
with tl_l:
    st.markdown(
        section_header(
            "02 / TRAYECTORIA",
            "Una habilidad por etapa, no una lista de cargos",
            "Cada rol me dejó una forma distinta de pensar la operación. AgroBrain es donde convergen todas.",
            anchor="trayectoria",
        ),
        unsafe_allow_html=True,
    )

    TIMELINE = [
        ("2026", "Comprendiendo la operación", "Sunshine Export · Operaciones Agrícolas",
         "Entendí cómo fluye la información agrícola desde el campo hasta facturación, y detecté que gran parte "
         "del tiempo del área se perdía en búsquedas manuales de datos de productores. Diseñé una consulta "
         "automatizada contra la API de SUNAT que eliminó ese cuello de botella."),
        ("2025", "Calidad del dato", "ProAgro · Recursos Humanos",
         "Construí y validé reportes de personal usados directamente por gerencia para decidir. Aprendí que un "
         "reporte confiable no es el que se ve ordenado, es el que gerencia puede usar sin tener que revisarlo dos veces."),
        ("2025", "Optimización de procesos", "Almacén · Logística",
         "Rediseñé el registro documentario del flujo de almacén para dar trazabilidad real a cada entrada y "
         "salida, coordinando directamente con logística en vez de limitarme a registrar datos."),
        ("En curso", "Transformación digital", "AgroBrain IA · Proyecto propio",
         "Estoy llevando ese mismo enfoque —entender la operación, confiar en el dato, optimizar el proceso— "
         "a una plataforma propia de gestión agroindustrial."),
    ]
    for date, skill, role, desc in TIMELINE:
        st.markdown(
            f"""<div class="tl-row reveal">
                <div class="tl-date">{date}</div>
                <div class="tl-content">
                    <div class="skill-title">{skill}</div>
                    <div class="role">{role}</div>
                    <div style="color:var(--text-dim); font-size:0.87rem; line-height:1.55;">{desc}</div>
                </div>
            </div>""",
            unsafe_allow_html=True,
        )

with tl_r:
    categories = ["AgroBrain · en curso", "Almacén · Logística", "ProAgro · RRHH", "Sunshine · Agro"]
    starts = [2026.55, 2025.0, 2025.0, 2026.0]
    ends = [2026.9, 2025.6, 2025.95, 2026.55]

    fig = go.Figure()
    for cat, s, e in zip(categories, starts, ends):
        fig.add_trace(go.Scatter(
            x=[s, e], y=[cat, cat], mode="lines",
            line=dict(color=C["accent"], width=16),
            hovertemplate=f"<b>{cat}</b><extra></extra>",
            showlegend=False,
        ))
    fig.update_layout(
        height=280,
        margin=dict(l=10, r=10, t=30, b=10),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Space Mono, monospace", color=C["text_dim"], size=11),
        xaxis=dict(title="", showgrid=True, gridcolor=C["grid_line"], zeroline=False, tickfont=dict(color=C["text_faint"])),
        yaxis=dict(showgrid=False, tickfont=dict(color=C["text"], size=11)),
    )
    st.plotly_chart(fig, width="stretch", config={"displayModeBar": False})

    st.markdown(
        """<div class="panel-card reveal" style="margin-top:6px;">
            <div class="p-title" style="font-size:0.85rem; letter-spacing:0.04em;">LECTURA DEL RECORRIDO</div>
            <div class="p-body">
            Tres sectores distintos (agro, RRHH, logística) que exigieron la misma pregunta:
            ¿de dónde viene este dato y en quién se convierte cuando llega arriba? AgroBrain
            es la respuesta a esa pregunta, escalada a plataforma.
            </div>
        </div>""",
        unsafe_allow_html=True,
    )

st.markdown("<div style='height:56px'></div>", unsafe_allow_html=True)

# ----------------------------------------------------------------------------
# CASOS DE ÉXITO — Problema → Análisis → Solución → Resultado → Impacto
# ----------------------------------------------------------------------------
st.markdown(
    section_header(
        "03 / CASOS",
        "Estudios de caso",
        "Tres ejemplos de convertir un problema operativo en un proceso más rápido, medible y confiable "
        "— con el impacto real para el negocio, no solo la solución técnica.",
        anchor="casos",
    ),
    unsafe_allow_html=True,
)

cs1, cs2 = st.columns(2, gap="large")
with cs1:
    st.markdown(
        case_card(
            "CASO 01",
            "Automatización de búsqueda de productores",
            "SUNSHINE EXPORT · OPERACIONES AGRÍCOLAS",
            stages=[
                ("PROBLEMA", "El área de facturación perdía tiempo cada día buscando manualmente los datos de cada productor antes de emitir comprobantes."),
                ("ANÁLISIS", "Identifiqué que la información ya existía en una fuente pública (SUNAT) y que el proceso solo necesitaba un punto de consulta directo, no más personas buscando a mano."),
                ("SOLUCIÓN", "Diseñé una consulta automatizada que consume la API de SUNAT y trae los datos del productor por RUC, sin intervención manual."),
                ("RESULTADO", "La búsqueda manual desapareció por completo del flujo de facturación."),
                ("IMPACTO PARA EL NEGOCIO", "Facturación emite comprobantes más rápido y con menos margen de error humano en cada operación."),
            ],
            chips=["API SUNAT", "AUTOMATIZACIÓN", "FACTURACIÓN"],
        ),
        unsafe_allow_html=True,
    )
with cs2:
    st.markdown(
        case_card(
            "CASO 02",
            "Reportes para decisiones de personal",
            "PROAGRO · RECURSOS HUMANOS",
            stages=[
                ("PROBLEMA", "Gerencia necesitaba información de personal confiable y a tiempo para decidir, y los datos venían de fuentes dispersas."),
                ("ANÁLISIS", "Mapeé qué área generaba cada dato y en qué punto se rompía la trazabilidad antes de llegar al reporte final."),
                ("SOLUCIÓN", "Construí un proceso de reportes periódicos con validación cruzada de cada dato antes de consolidarlo."),
                ("RESULTADO", "Reportes con un margen de error mínimo, listos para revisión gerencial sin retrabajo."),
                ("IMPACTO PARA EL NEGOCIO", "Decisiones de personal tomadas sobre información validada, no sobre estimaciones."),
            ],
            chips=["RRHH", "REPORTING", "VALIDACIÓN DE DATOS"],
        ),
        unsafe_allow_html=True,
    )

st.markdown("<div style='height:22px'></div>", unsafe_allow_html=True)

st.markdown(
    case_card(
        "CASO 03 · PROYECTO PROPIO",
        "RPMS — Mapeo de procesos AS-IS / TO-BE",
        "PROYECTO INDEPENDIENTE · CLIENTE FICTICIO \"PURAFRUIT CO.\" · SECTOR AGRO-EXPORTADOR",
        stages=[
            ("PROBLEMA", "El proceso de aprobación de requerimientos de campo no tenía registro digital, SLA de respuesta ni bitácora de rechazos."),
            ("ANÁLISIS", "Modelé el proceso actual (AS-IS) en BPMN 2.0 con Bizagi Modeler y detecté 4 fallas críticas, incluyendo la ausencia total de aviso a logística."),
            ("SOLUCIÓN", "Diseñé el proceso optimizado (TO-BE) con un SLA de aprobación de 24 horas y trazabilidad completa de cada requerimiento."),
            ("RESULTADO", "Un flujo medible, con indicadores construidos en un dashboard de Power BI sobre datos simulados de una campaña real."),
            ("IMPACTO PARA EL NEGOCIO", "Menor tiempo de aprobación y visibilidad total del estado de cada requerimiento para todas las áreas involucradas."),
        ],
        chips=["BPMN 2.0 / BIZAGI", "AS-IS / TO-BE", "POWER BI", "DAX", "KPI MANAGEMENT"],
        link="https://processanalytcsjobpulache.netlify.app/",
    ),
    unsafe_allow_html=True,
)

st.markdown("<div style='height:56px'></div>", unsafe_allow_html=True)

# ----------------------------------------------------------------------------
# AGROBRAIN IA — the natural evolution of the journey, vision-first
# ----------------------------------------------------------------------------
st.markdown(
    section_header(
        "04 / VISIÓN",
        'AgroBrain IA <span class="tag" style="margin-left:8px; vertical-align:middle;">EN DESARROLLO</span>',
        "",
        anchor="agrobrain",
    ),
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="panel-card reveal" style="border-left:2px solid var(--accent); margin-bottom:26px;">
        <div class="p-body" style="font-size:0.98rem; color:var(--text); line-height:1.7;">
        AgroBrain IA no nació como un ejercicio de programación. Nació de una pregunta que me hice trabajando
        en operaciones agrícolas, recursos humanos y logística: <b style="color:var(--accent);">¿qué pasaría
        si la información de campo llegara ya lista para decidir?</b>
        <br><br>
        AgroBrain es mi respuesta: una plataforma que organiza fundos, lotes, cuadrillas y producción,
        detecta desviaciones de productividad y calidad, y entrega recomendaciones operativas a supervisores
        y jefes de campo — antes de que el problema escale hasta gerencia. No es solo tecnología: es la forma
        en que decidí escalar lo que aprendí en cada rol anterior.
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

ab_cols = st.columns(3)
AB_PILLARS = [
    ("◐", "Gestión", "Fundos, lotes, cuadrillas y operarios en un solo modelo de datos, con trazabilidad de campo a reporte."),
    ("⌁", "Optimización", "Un motor de alertas detecta desviaciones de productividad y calidad antes de que se conviertan en pérdidas."),
    ("◈", "Inteligencia", "Recomendaciones operativas para supervisores y jefes de campo, no solo dashboards para revisar."),
]
for col, (glyph, title, body) in zip(ab_cols, AB_PILLARS):
    with col:
        st.markdown(panel_card(glyph, title, body), unsafe_allow_html=True)

st.markdown("<div style='height:18px'></div>", unsafe_allow_html=True)

with st.expander("Ver detalle técnico de arquitectura ↗"):
    dt_l, dt_r = st.columns([1, 1], gap="large")
    with dt_l:
        st.markdown(
            """
            <div class="block-label">ANÁLISIS FUNCIONAL</div>
            <p>Requerimientos, casos de uso, stakeholders y diagramas UML del dominio agroindustrial
            (fundos, lotes, cuadrillas, operarios, producción, incidencias).</p>
            <div class="block-label">ARQUITECTURA</div>
            <p>Clean Architecture sobre ASP.NET Core Web API, con separación de dominio, aplicación e infraestructura.</p>
            <div class="block-label">BASE DE DATOS</div>
            <p>Modelo relacional en SQL Server para trazabilidad completa de campo: de la cuadrilla al lote, del lote al incidente.</p>
            <div class="block-label">ENTREGA</div>
            <p>Dashboard operativo, consultas inteligentes, y repositorio versionado en GitHub con desarrollo incremental.</p>
            <div style="margin-top:14px;">
                <span class="chip">ASP.NET CORE</span><span class="chip">C#</span><span class="chip">SQL SERVER</span>
                <span class="chip">REACT</span><span class="chip">ENTITY FRAMEWORK CORE</span><span class="chip">JWT</span>
                <span class="chip">SWAGGER</span><span class="chip">POWER BI</span><span class="chip">DOCKER</span>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with dt_r:
        st.markdown(
            f"""
            <div class="demo-panel" style="height:100%;">
                <div class="demo-terminal-head">
                    <span class="dot" style="background:#E05252"></span>
                    <span class="dot" style="background:#E8C468"></span>
                    <span class="dot" style="background:{C['accent']}"></span>
                    &nbsp;arquitectura.diagram
                </div>
                <div style="display:flex; flex-direction:column; gap:0; font-family:'Space Mono',monospace; font-size:0.78rem;">
                    <div style="border:1px solid var(--border-strong); padding:10px 14px; text-align:center; color:var(--text);">
                        REACT <span style="color:var(--text-faint);">· interfaz de campo</span>
                    </div>
                    <div style="text-align:center; color:var(--accent); padding:4px 0;">↓</div>
                    <div style="border:1px solid var(--border-strong); padding:10px 14px; text-align:center; color:var(--text);">
                        ASP.NET CORE WEB API <span style="color:var(--text-faint);">· clean architecture</span>
                    </div>
                    <div style="text-align:center; color:var(--accent); padding:4px 0;">↓</div>
                    <div style="display:flex; gap:10px;">
                        <div style="flex:1; border:1px solid var(--border); padding:10px; text-align:center; color:var(--text-dim); font-size:0.72rem;">MOTOR DE<br>ALERTAS</div>
                        <div style="flex:1; border:1px solid var(--border); padding:10px; text-align:center; color:var(--text-dim); font-size:0.72rem;">SQL SERVER<br>fundos·lotes·producción</div>
                        <div style="flex:1; border:1px solid var(--border); padding:10px; text-align:center; color:var(--text-dim); font-size:0.72rem;">POWER BI<br>dashboard</div>
                    </div>
                    <div style="text-align:center; color:var(--accent); padding:4px 0;">↓</div>
                    <div style="border:1px dashed var(--border-strong); padding:8px 14px; text-align:center; color:var(--text-faint); font-size:0.72rem;">CONTENEDORIZADO CON DOCKER</div>
                </div>
                <div style="margin-top:18px; color:var(--text-faint); font-size:0.78rem; line-height:1.6;">
                    &gt; estado: desarrollo incremental activo<span class="hero-cursor"></span><br>
                    &gt; próximo hito: motor de recomendaciones v1
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

st.markdown("<div style='height:56px'></div>", unsafe_allow_html=True)

# ----------------------------------------------------------------------------
# AUTOMATIZACIÓN EN VIVO — enterprise module, not a "toy demo"
# ----------------------------------------------------------------------------
st.markdown(
    section_header(
        "05 / MÓDULO EN VIVO",
        "Automatización de consulta de productor",
        "Una versión operativa del proceso que construí en Sunshine. Datos de ejemplo, no información real "
        "de SUNAT — el objetivo es mostrar cómo se comporta el flujo en producción.",
        anchor="demo",
    ),
    unsafe_allow_html=True,
)

demo_l, demo_r = st.columns([1, 1.3], gap="large")

MOCK_PRODUCERS = {
    "20601234567 — Agroexportadora Los Médanos S.A.C.": dict(
        razon_social="AGROEXPORTADORA LOS MÉDANOS S.A.C.",
        estado="ACTIVO", condicion="HABIDO",
        direccion="CAR. PIURA-SULLANA KM 12, PIURA",
        actividad="CULTIVO DE FRUTAS (UVA / MANGO)",
    ),
    "20558877441 — Fundo San Miguel E.I.R.L.": dict(
        razon_social="FUNDO SAN MIGUEL E.I.R.L.",
        estado="ACTIVO", condicion="HABIDO",
        direccion="AV. PANAMERICANA NORTE KM 4, SULLANA",
        actividad="CULTIVO DE BANANO ORGÁNICO",
    ),
    "20489912303 — Procesadora Agrícola del Norte S.A.": dict(
        razon_social="PROCESADORA AGRÍCOLA DEL NORTE S.A.",
        estado="ACTIVO", condicion="HABIDO",
        direccion="ZONA INDUSTRIAL, PIURA",
        actividad="PROCESAMIENTO Y CONSERVACIÓN DE FRUTAS",
    ),
}
PIPELINE_STEPS = [
    "Conectando con API SUNAT...",
    "Validando estructura de RUC...",
    "Consultando registro tributario...",
    "Estructurando respuesta para facturación...",
]

with demo_l:
    choice = st.selectbox("Selecciona un productor de ejemplo", list(MOCK_PRODUCERS.keys()))
    run = st.button("▶ Ejecutar pipeline de automatización", width="stretch")
    st.markdown(
        """<div class="panel-card reveal" style="margin-top:16px;">
            <div class="p-title" style="font-size:0.85rem;">CÓMO LEER ESTE MÓDULO</div>
            <div class="p-body">Este es el mismo flujo que dejó de ser manual en Sunshine: entra un RUC,
            sale una ficha de productor lista para facturación. Sin buscadores, sin copiar y pegar.</div>
        </div>""",
        unsafe_allow_html=True,
    )

with demo_r:
    st.markdown(
        f"""<div class="demo-panel">
            <div class="demo-terminal-head">
                <span class="dot" style="background:#E05252"></span>
                <span class="dot" style="background:#E8C468"></span>
                <span class="dot" style="background:{C['accent']}"></span>
                &nbsp;consulta_sunat.py
            </div>""",
        unsafe_allow_html=True,
    )

    placeholder = st.empty()

    if run:
        with placeholder.container():
            with st.status("Ejecutando pipeline de automatización...", expanded=True) as status:
                progress = st.progress(0, text=PIPELINE_STEPS[0])
                for i, step in enumerate(PIPELINE_STEPS):
                    st.write(f"› {step}")
                    progress.progress(int((i + 1) / len(PIPELINE_STEPS) * 100), text=step)
                    time.sleep(0.45)
                status.update(label="Consulta completada", state="complete", expanded=False)

            data = MOCK_PRODUCERS[choice]
            st.markdown(
                f'<div style="display:flex; justify-content:space-between; align-items:center; margin:14px 0 4px 0;">'
                f'<span style="font-family:\'Space Mono\',monospace; font-size:0.78rem; color:var(--text-faint);">FICHA DE PRODUCTOR</span>'
                f'<span class="status-pill">{data["estado"]}</span></div>',
                unsafe_allow_html=True,
            )
            fields = [
                ("RUC", choice.split(" — ")[0]),
                ("RAZÓN SOCIAL", data["razon_social"]),
                ("CONDICIÓN", data["condicion"]),
                ("DIRECCIÓN FISCAL", data["direccion"]),
                ("ACTIVIDAD ECONÓMICA", data["actividad"]),
            ]
            rows = "".join(f'<div class="result-field"><span class="k">{k}</span><span class="v">{v}</span></div>' for k, v in fields)
            st.markdown(rows, unsafe_allow_html=True)

            st.markdown("<div style='height:14px'></div>", unsafe_allow_html=True)
            m1, m2 = st.columns(2)
            with m1:
                st.metric("Proceso manual (antes)", "~8 min", help="Tiempo estimado de búsqueda manual por productor")
            with m2:
                st.metric("Pipeline automatizado", "~12 seg", delta="-99% del tiempo", delta_color="normal")
    else:
        with placeholder.container():
            st.markdown(
                """<div style="color:var(--text-faint); font-family:'Space Mono',monospace; font-size:0.82rem; padding: 30px 0;">
                &gt; esperando ejecución...<span class="hero-cursor"></span>
                </div>""",
                unsafe_allow_html=True,
            )

    st.markdown("</div>", unsafe_allow_html=True)

st.markdown("<div style='height:56px'></div>", unsafe_allow_html=True)

# ----------------------------------------------------------------------------
# CAPACIDADES — executive competency matrix (no invented percentages)
# ----------------------------------------------------------------------------
st.markdown(
    section_header(
        "06 / CAPACIDADES",
        "Dónde aporto valor hoy",
        "Sin porcentajes inventados: una lectura honesta de qué domino a fondo y qué estoy construyendo activamente.",
        anchor="capacidades",
    ),
    unsafe_allow_html=True,
)

CAPABILITIES = [
    ("Análisis de datos", "badge-core", "NÚCLEO", ["Excel avanzado", "SQL Server", "Power BI", "DAX", "Power Query"],
     "Uso diario, sin supervisión — es donde resuelvo la mayoría de los problemas operativos."),
    ("Procesos y mejora continua", "badge-core", "NÚCLEO", ["BPMN 2.0", "Bizagi Modeler", "AS-IS / TO-BE", "KPI Management", "SLA Design"],
     "El lente con el que miro cualquier operación antes de tocar una herramienta."),
    ("Automatización", "badge-solid", "SÓLIDO", ["APIs REST", "Postman", "Python", "SUNAT API"],
     "Aplicado en un proceso real de producción, con resultado medible."),
    ("Sistemas y arquitectura", "badge-growth", "EN CRECIMIENTO", ["Clean Architecture", "ASP.NET Core", "Docker", "Git / GitHub"],
     "En desarrollo activo — la evidencia en curso es AgroBrain IA."),
]
cap_cols = st.columns(4)
for col, (domain, bcls, blabel, tools, note) in zip(cap_cols, CAPABILITIES):
    with col:
        st.markdown(capability_card(domain, bcls, blabel, tools, note), unsafe_allow_html=True)

st.markdown(
    """<div style="margin-top:16px;">
        <a class="linklike" href="https://jobpulachecarreno.netlify.app/" target="_blank">Ver mi portafolio técnico de desarrollo ↗</a>
    </div>""",
    unsafe_allow_html=True,
)

st.markdown("<div style='height:56px'></div>", unsafe_allow_html=True)

# ----------------------------------------------------------------------------
# CONTACT / FOOTER
# ----------------------------------------------------------------------------
st.markdown(
    section_header(
        "07 / CONTACTO",
        "Conversemos",
        "Abierto a roles de analista de operaciones, analista de procesos o analista de datos en el sector agroindustrial.",
        anchor="contacto",
    ),
    unsafe_allow_html=True,
)

ct1, ct2, ct3 = st.columns(3)
with ct1:
    st.link_button("✉  pulachecarrenojob@gmail.com", "mailto:pulachecarrenojob@gmail.com", width="stretch")
with ct2:
    st.link_button("✆ (WhatsApp)", "https://wa.me/51930938449", width="stretch")
with ct3:
    st.link_button("↗  linkedin.com/in/jobpulachecarreno", "https://www.linkedin.com/in/jobpulachecarreno/", width="stretch")

st.markdown(
    f"""
    <div class="footbar">
        <div>© 2026 JOB PULACHE CARREÑO · PIURA, PERÚ</div>
        <div>build:// streamlit + plotly · {C['mode_label']}</div>
    </div>
    """,
    unsafe_allow_html=True,
)
