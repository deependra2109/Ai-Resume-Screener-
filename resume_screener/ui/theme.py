"""
Visual theme: "The Reviewer's Desk" — a dark, editorial theme for a tool that
reads and judges documents. An ink-dark background with a faint warm glow
evokes a desk lamp at night; a serif display face gives resumes and scores
the weight of something being seriously read, not just computed.

Design tokens
-------------
Color:
  ink            #0B0E14   page background
  panel          #141922   card / section surface
  panel-raised   #1C222D   nested surface (tabs, expander body, inputs)
  hairline       #2A303C   borders / dividers
  brass          #C9A466   primary accent — headlines, buttons, the stamp
  sage           #7FA98A   signal: matched / good
  rust           #B2664B   signal: missing / gap
  parchment      #EDE7D9   primary text
  slate          #868C97   secondary / muted text

Type:
  display  Fraunces        headline, verdict stamp digits
  body     Manrope         UI labels, buttons, copy
  mono     IBM Plex Mono   scores, percentages, skill chips

Signature: the "Verdict Stamp" — a circular brass-ringed badge with the match
score, tilted slightly like an ink stamp on a reviewed document. Used once per
resume so it reads as a signature, not decoration.
"""

import streamlit as st

CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,400;9..144,500;9..144,600&family=Manrope:wght@400;500;600;700&family=IBM+Plex+Mono:wght@400;500;600&display=swap');

:root {
  --ink: #0B0E14;
  --panel: #141922;
  --panel-raised: #1C222D;
  --hairline: #2A303C;
  --brass: #C9A466;
  --brass-dim: #8A7550;
  --sage: #7FA98A;
  --rust: #B2664B;
  --parchment: #EDE7D9;
  --slate: #868C97;
}

/* ---------- base ---------- */
.stApp {
  background:
    radial-gradient(ellipse 900px 500px at 50% -10%, rgba(201,164,102,0.10), transparent 60%),
    var(--ink);
  color: var(--parchment);
}
.stApp, .stApp p, .stApp span, .stApp label, .stApp li {
  font-family: 'Manrope', sans-serif;
}
.stApp h1, .stApp h2, .stApp h3 {
  font-family: 'Fraunces', serif;
  font-weight: 500;
  letter-spacing: -0.01em;
}
.mono { font-family: 'IBM Plex Mono', monospace !important; }

::selection { background: rgba(201,164,102,0.35); }

::-webkit-scrollbar { width: 10px; height: 10px; }
::-webkit-scrollbar-track { background: var(--ink); }
::-webkit-scrollbar-thumb { background: var(--hairline); border-radius: 6px; }
::-webkit-scrollbar-thumb:hover { background: var(--brass-dim); }

/* ---------- sidebar ---------- */
[data-testid="stSidebar"] {
  background: var(--panel);
  border-right: 1px solid var(--hairline);
}

/* ---------- hero ---------- */
.hero-eyebrow {
  font-family: 'IBM Plex Mono', monospace;
  font-size: 0.72rem;
  letter-spacing: 0.22em;
  text-transform: uppercase;
  color: var(--brass);
  text-align: center;
  margin-bottom: 0.6rem;
}
.hero-title {
  font-family: 'Fraunces', serif;
  font-weight: 500;
  font-size: 2.6rem;
  text-align: center;
  color: var(--parchment);
  margin: 0;
}
.hero-sub {
  text-align: center;
  color: var(--slate);
  font-size: 0.98rem;
  max-width: 620px;
  margin: 0.9rem auto 0 auto;
  line-height: 1.5;
}
.hairline-rule { border: none; border-top: 1px solid var(--hairline); margin: 1.8rem 0; }

/* ---------- buttons ---------- */
.stButton > button, .stDownloadButton > button {
  background: transparent;
  color: var(--brass);
  border: 1px solid var(--brass-dim);
  border-radius: 6px;
  font-family: 'Manrope', sans-serif;
  font-weight: 600;
  padding: 0.5rem 1.1rem;
  transition: all 0.15s ease;
}
.stButton > button:hover, .stDownloadButton > button:hover {
  background: rgba(201,164,102,0.10);
  border-color: var(--brass);
  box-shadow: 0 0 0 1px var(--brass) inset;
}
.stButton > button[kind="primary"] { background: var(--brass); color: var(--ink); border: 1px solid var(--brass); }
.stButton > button[kind="primary"]:hover { background: #d8b479; }

/* ---------- inputs ---------- */
.stTextInput input, .stTextArea textarea,
.stSelectbox div[data-baseweb="select"] > div {
  background: var(--panel-raised) !important;
  color: var(--parchment) !important;
  border: 1px solid var(--hairline) !important;
  border-radius: 6px !important;
}
.stTextInput input:focus, .stTextArea textarea:focus {
  border-color: var(--brass) !important;
  box-shadow: 0 0 0 1px var(--brass) !important;
}
[data-testid="stFileUploader"] {
  background: var(--panel-raised);
  border: 1px dashed var(--hairline);
  border-radius: 8px;
  padding: 0.5rem;
}

/* ---------- metrics ---------- */
[data-testid="stMetric"] {
  background: var(--panel);
  border: 1px solid var(--hairline);
  border-radius: 8px;
  padding: 0.9rem 1rem;
}
[data-testid="stMetricLabel"] {
  font-family: 'IBM Plex Mono', monospace;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  font-size: 0.7rem;
  color: var(--slate) !important;
}
[data-testid="stMetricValue"] { font-family: 'Fraunces', serif; color: var(--brass) !important; }

/* ---------- tabs ---------- */
.stTabs [data-baseweb="tab-list"] { gap: 4px; border-bottom: 1px solid var(--hairline); }
.stTabs [data-baseweb="tab"] {
  font-family: 'IBM Plex Mono', monospace;
  font-size: 0.78rem;
  color: var(--slate);
  background: transparent;
  border-radius: 0;
}
.stTabs [aria-selected="true"] { color: var(--brass) !important; border-bottom: 2px solid var(--brass) !important; }

/* ---------- expanders ---------- */
[data-testid="stExpander"] {
  background: var(--panel);
  border: 1px solid var(--hairline);
  border-radius: 8px;
  overflow: hidden;
}
[data-testid="stExpander"] summary { font-family: 'Manrope', sans-serif; font-weight: 600; color: var(--parchment); }

/* ---------- alerts ---------- */
[data-testid="stAlert"] { border-radius: 6px; border: 1px solid var(--hairline); background: var(--panel-raised); }

/* ---------- dataframe ---------- */
[data-testid="stDataFrame"] { border: 1px solid var(--hairline); border-radius: 8px; overflow: hidden; }

/* ---------- skill chips ---------- */
.chip-row { display: flex; flex-wrap: wrap; gap: 6px; margin: 0.3rem 0 0.9rem 0; }
.chip {
  font-family: 'IBM Plex Mono', monospace;
  font-size: 0.72rem;
  padding: 3px 9px;
  border-radius: 4px;
  border: 1px solid;
}
.chip-good { color: var(--sage); border-color: var(--sage); background: rgba(127,169,138,0.08); }
.chip-gap  { color: var(--rust); border-color: var(--rust); background: rgba(178,102,75,0.08); }
.chip-empty { color: var(--slate); border-color: var(--hairline); }

/* ---------- verdict stamp (signature element) ---------- */
.stamp-wrap { display: flex; justify-content: center; margin: 0.4rem 0 1rem 0; }
.verdict-stamp {
  width: 104px; height: 104px;
  border-radius: 50%;
  border: 2px solid var(--brass);
  display: flex; flex-direction: column; align-items: center; justify-content: center;
  transform: rotate(-4deg);
  background:
    repeating-linear-gradient(115deg, rgba(201,164,102,0.05) 0px, rgba(201,164,102,0.05) 2px, transparent 2px, transparent 6px),
    var(--panel);
  box-shadow: 0 0 0 3px rgba(201,164,102,0.12);
}
.verdict-stamp .num { font-family: 'Fraunces', serif; font-size: 1.6rem; color: var(--brass); line-height: 1; }
.verdict-stamp .label {
  font-family: 'IBM Plex Mono', monospace;
  font-size: 0.52rem;
  letter-spacing: 0.14em;
  text-transform: uppercase;
  color: var(--slate);
  margin-top: 3px;
}
</style>
"""


def inject_theme():
    st.markdown(CSS, unsafe_allow_html=True)


def verdict_stamp_html(pct: float, label: str = "MATCH") -> str:
    """Renders the signature circular stamp badge for a match score."""
    return f"""
    <div class="stamp-wrap">
      <div class="verdict-stamp">
        <div class="num">{pct:.0f}%</div>
        <div class="label">{label}</div>
      </div>
    </div>
    """


def chip_row_html(items: list[str], variant: str) -> str:
    """Renders a row of skill chips. variant: 'good' | 'gap'."""
    if not items:
        return '<div class="chip-row"><span class="chip chip-empty">none</span></div>'
    chips = "".join(f'<span class="chip chip-{variant}">{s}</span>' for s in items)
    return f'<div class="chip-row">{chips}</div>'
