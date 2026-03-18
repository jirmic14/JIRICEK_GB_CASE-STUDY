# ============================
# IMPORTY KNIŽNÍC
# ============================

import os
import re
from pathlib import Path

# Tieto importy zatiaľ nemusíš aktívne používať všade,
# ale nechávam ich, keďže si ich chcel mať pripravené
import base64
import pandas as pd
import plotly.graph_objects as go
import streamlit as st


# ============================
# ZÁKLADNÉ NASTAVENIA STRÁNKY
# ============================

st.set_page_config(
    page_title="GymBeam Case Study Intern",   # názov tabu
    page_icon="💼",                           # ikona tabu
    layout="wide",                            # široký layout
    initial_sidebar_state="expanded",         # sidebar otvorený od začiatku
)


# ============================
# CESTY K SÚBOROM
# ============================

# Aktuálny priečinok, kde je app.py
BASE_DIR = Path(__file__).parent

# Priečinok so zadaniami
CASE_STUDY_DIR = BASE_DIR / "1_zadanie"

# Priečinok s dotazníkom
QUESTIONNAIRE_DIR = BASE_DIR / "2_dotaznik"

# Logo GymBeam
LOGO_PATH = BASE_DIR / "logo.png"


# ============================
# VLASTNÉ CSS ŠTÝLY
# ============================

st.markdown(
    """
    <style>
        :root {
            color-scheme: dark;
        }

        html, body, [data-testid="stAppViewContainer"], .stApp {
            background-color: #020817 !important;
            color: white !important;
        }

        .stApp {
            background-color: #020817 !important;
        }

        .block-container {
            padding-top: 1.8rem;
            padding-bottom: 2rem;
            max-width: 1400px;
        }

        header[data-testid="stHeader"] {
            background: rgba(2, 8, 23, 0.95);
        }

        /* Sidebar pozadie */
        section[data-testid="stSidebar"] {
            background: linear-gradient(180deg, #232533 0%, #2a2d3f 100%) !important;
        }

        /* Sidebar buttony a link buttony */
        section[data-testid="stSidebar"] .stButton > button,
        section[data-testid="stSidebar"] .stLinkButton > a {
            width: 100%;
            border-radius: 12px !important;
            text-transform: uppercase;
            letter-spacing: 0.4px;
            font-weight: 700 !important;
            border: 1px solid rgba(255,255,255,0.18) !important;
            background-color: rgba(255,255,255,0.02) !important;
            color: white !important;
            min-height: 46px !important;
            justify-content: center !important;
            text-align: center !important;
        }

        /* Hover efekt */
        section[data-testid="stSidebar"] .stButton > button:hover,
        section[data-testid="stSidebar"] .stLinkButton > a:hover {
            border-color: #ff4b4b !important;
            color: #ff4b4b !important;
            box-shadow: 0 0 0 1px #ff4b4b inset;
        }

        /* Link button centrovanie */
        section[data-testid="stSidebar"] .stLinkButton > a {
            display: flex !important;
            align-items: center !important;
            justify-content: center !important;
        }

        /* Centrovaný blok v sidebare */
        .sidebar-center {
            width: 100%;
            text-align: center !important;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
        }

        .sidebar-subtitle {
            text-align: center !important;
            color: #b3b7c2;
            font-size: 0.95rem;
            margin-top: 0.15rem;
            width: 100%;
        }

        /* Logo v sidebare */
        .sidebar-logo-wrap {
            display: flex;
            justify-content: center;
            width: 100%;
            margin-top: 1.2rem;
            margin-bottom: 0.3rem;
        }

        /* Hlavný nadpis na homepage */
        .hero-title {
            text-align: center;
            font-size: 3.4rem;
            font-weight: 800;
            margin-bottom: 0.35rem;
            letter-spacing: 0.5px;
        }

        /* Podnadpis na homepage */
        .hero-subtitle {
            text-align: center;
            color: #9ca3af;
            margin-bottom: 2rem;
            font-size: 1.05rem;
        }

        /* Karty Zadanie / Dotazník */
        .menu-card {
            border: 1px solid rgba(255,255,255,0.18);
            border-radius: 18px;
            padding: 28px 24px 30px 24px;
            min-height: 220px;
            text-align: center;
            background: rgba(255,255,255,0.01);
        }

        .menu-card h2 {
            margin-top: 0;
            margin-bottom: 0.6rem;
            font-size: 2.1rem;
        }

        .menu-card p {
            font-size: 1.05rem;
            line-height: 1.6;
            margin-bottom: 0.3rem;
        }

        /* Nadpis sekcie */
        .section-title {
            font-size: 3rem;
            font-weight: 800;
            margin-bottom: 0.2rem;
        }

        /* Jemná čiara v obsahu */
        .subtle-divider {
            height: 1px;
            width: 100%;
            background: rgba(255,255,255,0.12);
            margin: 1rem 0 1rem 0;
        }

        /* Renderované markdown nadpisy */
        .content-h1 {
            font-size: 2.5rem;
            font-weight: 800;
            line-height: 1.2;
            margin-bottom: 1rem;
        }

        .content-h2 {
            font-size: 1.55rem;
            font-weight: 800;
            line-height: 1.3;
            margin-top: 1rem;
            margin-bottom: 0.6rem;
        }

        .content-h3 {
            font-size: 1.1rem;
            font-weight: 700;
            line-height: 1.3;
            margin-top: 0.8rem;
            margin-bottom: 0.35rem;
        }

        .content-p {
            font-size: 1rem;
            line-height: 1.75;
            margin-bottom: 0.5rem;
        }

        .content-link {
            font-size: 0.98rem;
            line-height: 1.6;
            margin-bottom: 0.25rem;
        }

        .content-ul {
            margin-top: 0.35rem;
            margin-bottom: 0.7rem;
            padding-left: 1.4rem;
        }

        .content-ul li {
            margin-bottom: 0.45rem;
            line-height: 1.6;
        }

        /* Presné centrovanie mena v sidebare */
        .sidebar-name {
            text-align: center;
            font-size: 1.95rem;
            font-weight: 800;
            width: 100%;
            margin: 0 auto;
            line-height: 1.2;
        }
    </style>
    """,
    unsafe_allow_html=True,
)


# ============================
# SESSION STATE
# ============================

if "page" not in st.session_state:
    st.session_state.page = "home"

if "zadanie_index" not in st.session_state:
    st.session_state.zadanie_index = 1

if "dotaznik_index" not in st.session_state:
    st.session_state.dotaznik_index = 1


# ============================
# NAVIGAČNÉ FUNKCIE
# ============================

def reset_indices():
    """Reset indexov sliderov späť na 1."""
    st.session_state.zadanie_index = 1
    st.session_state.dotaznik_index = 1


def go_home():
    """Presun na hlavnú stránku a reset sliderov."""
    reset_indices()
    st.session_state.page = "home"


def go_zadanie():
    """Presun do sekcie Zadanie od otázky 1."""
    st.session_state.zadanie_index = 1
    st.session_state.page = "zadanie"


def go_dotaznik():
    """Presun do sekcie Dotazník od otázky 1."""
    st.session_state.dotaznik_index = 1
    st.session_state.page = "dotaznik"


# ============================
# PRÁCA SO SÚBORMI
# ============================

def get_markdown_files(folder: Path) -> list[Path]:
    """
    Načíta všetky .md súbory z daného priečinka
    a zoradí ich podľa čísla v názve.
    """
    if not folder.exists():
        return []

    files = list(folder.glob("*.md"))

    def sort_key(file_path: Path):
        stem = file_path.stem
        try:
            return int(stem.split("_")[0])
        except ValueError:
            try:
                return int(stem)
            except ValueError:
                return 9999

    return sorted(files, key=sort_key)


def read_markdown_file(file_path: Path) -> str:
    """Načíta text markdown súboru."""
    if not file_path.exists():
        return f"# Súbor nebol nájdený\n\nChýba súbor: {file_path.name}"
    return file_path.read_text(encoding="utf-8")


# ============================
# VLASTNÝ RENDER MARKDOWNU
# ============================

def escape_html(text: str) -> str:
    """Escapovanie HTML znakov."""
    return (
        text.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
    )


def format_inline_markdown(text: str) -> str:
    """Spracovanie inline markdown syntaxe."""
    text = escape_html(text)
    text = re.sub(r"\*\*(.*?)\*\*", r"<strong>\1</strong>", text)
    text = re.sub(r"\*(.*?)\*", r"<em>\1</em>", text)
    text = re.sub(r"`(.*?)`", r"<code>\1</code>", text)
    text = re.sub(r"\[(.*?)\]\((.*?)\)", r'<a href="\2" target="_blank">\1</a>', text)
    return text


def render_markdown_safely(content: str):
    """Bezpečné zobrazenie markdownu po riadkoch."""
    lines = content.replace("\r\n", "\n").split("\n")
    in_list = False

    def close_list():
        nonlocal in_list
        if in_list:
            st.markdown("</ul>", unsafe_allow_html=True)
            in_list = False

    for raw_line in lines:
        line = raw_line.rstrip()
        stripped = line.strip()

        if not stripped:
            close_list()
            st.markdown("<div style='height: 0.3rem;'></div>", unsafe_allow_html=True)
            continue

        if stripped == "---":
            close_list()
            st.markdown("<div class='subtle-divider'></div>", unsafe_allow_html=True)
            continue

        if stripped.startswith("# "):
            close_list()
            text = format_inline_markdown(stripped[2:].strip())
            st.markdown(f"<div class='content-h1'>{text}</div>", unsafe_allow_html=True)
            continue

        if stripped.startswith("## "):
            close_list()
            text = format_inline_markdown(stripped[3:].strip())
            st.markdown(f"<div class='content-h2'>{text}</div>", unsafe_allow_html=True)
            continue

        if stripped.startswith("### "):
            close_list()
            text = format_inline_markdown(stripped[4:].strip())
            st.markdown(f"<div class='content-h3'>{text}</div>", unsafe_allow_html=True)
            continue

        if stripped.startswith("- "):
            item_text = format_inline_markdown(stripped[2:].strip())
            if not in_list:
                st.markdown("<ul class='content-ul'>", unsafe_allow_html=True)
                in_list = True
            st.markdown(f"<li>{item_text}</li>", unsafe_allow_html=True)
            continue

        if stripped.startswith("http://") or stripped.startswith("https://"):
            close_list()
            url = escape_html(stripped)
            st.markdown(
                f"<div class='content-link'><a href='{url}' target='_blank'>{url}</a></div>",
                unsafe_allow_html=True,
            )
            continue

        close_list()
        text = format_inline_markdown(stripped)
        st.markdown(f"<div class='content-p'>{text}</div>", unsafe_allow_html=True)

    close_list()


# ============================
# SIDEBAR
# ============================

def render_sidebar():
    """Vykreslenie ľavého sidebaru."""
    with st.sidebar:
        # Meno vycentrované
        st.markdown(
            """
            <div class='sidebar-center'>
                <div class='sidebar-name'>Michal Jiříček</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.divider()

        # Navigačné buttony
        if st.button("HLAVNÉ MENU", use_container_width=True):
            go_home()
            st.rerun()

        if st.button("ZADANIE", use_container_width=True):
            go_zadanie()
            st.rerun()

        if st.button("DOTAZNÍK", use_container_width=True):
            go_dotaznik()
            st.rerun()

        st.divider()

        # Odkazy
        st.markdown("<div class='sidebar-center'><strong>ODKAZY</strong></div>", unsafe_allow_html=True)
        st.write("")

        st.link_button("LINKEDLN", "http://www.linkedin.com/in/michal-jiricek", use_container_width=True)
        st.link_button("GITHUB", "https://github.com/jirmic14", use_container_width=True)
        st.link_button("STREAMLIT", "https://share.streamlit.io/user/jirmic14", use_container_width=True)
        st.link_button("YOUTUBE", "https://www.youtube.com/@jiricekmichal", use_container_width=True)

        st.divider()

        # Logo úplne dole
        if LOGO_PATH.exists():
            st.markdown("<div class='sidebar-logo-wrap'>", unsafe_allow_html=True)
            st.image(str(LOGO_PATH), use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)


# ============================
# HOME
# ============================

def render_home():
    """Hlavná domovská stránka."""
    st.markdown("<div class='hero-title'>GYMBEAM CASE STUDY INTERN</div>", unsafe_allow_html=True)
    st.markdown(
        "<div class='hero-subtitle'>Interaktívna prezentácia case study a dotazníka</div>",
        unsafe_allow_html=True,
    )

    col1, col2 = st.columns(2, gap="large")

    with col1:
        st.markdown(
            """
            <div class="menu-card">
                <h2>📝 Zadanie</h2>
                <p><strong>Case study – 5 otázok</strong></p>
                <p>Produkty, KPI, oblečenie, fitness hub a riešenie situácií.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.markdown("<div style='height: 22px;'></div>", unsafe_allow_html=True)
        if st.button("Otvoriť Zadanie", use_container_width=True, key="home_zadanie"):
            go_zadanie()
            st.rerun()

    with col2:
        st.markdown(
            """
            <div class="menu-card">
                <h2>📋 Dotazník</h2>
                <p><strong>Otázky 1–20</strong></p>
                <p>Osobné odpovede, motivácia, ciele, knihy, spolupráca a ďalšie.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.markdown("<div style='height: 22px;'></div>", unsafe_allow_html=True)
        if st.button("Otvoriť Dotazník", use_container_width=True, key="home_dotaznik"):
            go_dotaznik()
            st.rerun()


# ============================
# SEKČNÁ STRÁNKA
# ============================

def render_section(title: str, folder: Path, state_key: str):
    """Vykreslenie sekcie Zadanie alebo Dotazník."""
    files = get_markdown_files(folder)

    if not files:
        st.error(f"V priečinku `{folder.name}` sa nenašli žiadne .md súbory.")
        if st.button("Späť na hlavné menu"):
            go_home()
            st.rerun()
        return

    max_questions = len(files)

    current_index = st.session_state[state_key]
    if current_index < 1:
        current_index = 1
    if current_index > max_questions:
        current_index = max_questions
    st.session_state[state_key] = current_index

    top_col1, top_col2 = st.columns([6, 1])

    with top_col1:
        st.markdown(f"<div class='section-title'>{title}</div>", unsafe_allow_html=True)

    with top_col2:
        if st.button("⬅ Späť", use_container_width=True, key=f"back_{state_key}"):
            go_home()
            st.rerun()

    st.write("")

    selected_index = st.slider(
        "Vyber otázku",
        min_value=1,
        max_value=max_questions,
        value=st.session_state[state_key],
        step=1,
        key=f"slider_{state_key}",
    )

    st.session_state[state_key] = selected_index

    st.markdown(
        f"<p style='text-align:center; font-weight:700; margin-top: 0.7rem; margin-bottom: 1.2rem;'>Otázka {st.session_state[state_key]} z {max_questions}</p>",
        unsafe_allow_html=True,
    )

    st.divider()

    current_file = files[st.session_state[state_key] - 1]
    content = read_markdown_file(current_file)
    render_markdown_safely(content)


# ============================
# SPUSTENIE APLIKÁCIE
# ============================

render_sidebar()

if st.session_state.page == "home":
    render_home()
elif st.session_state.page == "zadanie":
    render_section("Zadanie", CASE_STUDY_DIR, "zadanie_index")
elif st.session_state.page == "dotaznik":
    render_section("Dotazník", QUESTIONNAIRE_DIR, "dotaznik_index")
