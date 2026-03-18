# ============================
# IMPORTY KNIŽNÍC
# ============================

import os
import re
from io import BytesIO
from pathlib import Path

# Tieto importy zatiaľ nemusíš aktívne používať všade,
# ale nechávam ich, keďže si ich chcel mať pripravené
import base64
import pandas as pd
import plotly.graph_objects as go
import streamlit as st

# ReportLab použijeme na export do PDF
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    ListFlowable,
    ListItem,
    PageBreak,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
)


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
# Tu nastavujeme tmavý vzhľad, sidebar, buttony, kartičky a texty

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

        /* Sidebar buttony, link buttony a download buttony */
        section[data-testid="stSidebar"] .stButton > button,
        section[data-testid="stSidebar"] .stLinkButton > a,
        section[data-testid="stSidebar"] .stDownloadButton > button {
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
        section[data-testid="stSidebar"] .stLinkButton > a:hover,
        section[data-testid="stSidebar"] .stDownloadButton > button:hover {
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
# Ukladáme si aktuálnu stránku a pozíciu sliderov

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

@st.cache_data(show_spinner=False)
def get_markdown_files(folder_str: str) -> list[str]:
    """
    Načíta všetky .md súbory z daného priečinka
    a zoradí ich podľa čísla v názve.
    """
    folder = Path(folder_str)

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

    sorted_files = sorted(files, key=sort_key)
    return [str(f) for f in sorted_files]

def get_markdown_paths(folder: Path) -> list[Path]:
    """Wrapper, ktorý vráti Path objekty."""
    return [Path(p) for p in get_markdown_files(str(folder))]

@st.cache_data(show_spinner=False)
def read_markdown_file(file_path_str: str) -> str:
    """Načíta text markdown súboru."""
    file_path = Path(file_path_str)

    if not file_path.exists():
        return f"# Súbor nebol nájdený\n\nChýba súbor: {file_path.name}"

    return file_path.read_text(encoding="utf-8")


# ============================
# VLASTNÝ RENDER MARKDOWNU
# ============================
# Tento renderer obchádza problémy, ktoré vznikali pri st.markdown
# na niektorých komplikovanejších blokoch.

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
# PDF EXPORT
# ============================

def find_font_path() -> str | None:
    """Nájde vhodný font na systéme."""
    possible_paths = [
        r"C:\Windows\Fonts\arial.ttf",
        r"C:\Windows\Fonts\Arial.ttf",
        r"C:\Windows\Fonts\calibri.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/dejavu/DejaVuSans.ttf",
        "/System/Library/Fonts/Supplemental/Arial Unicode.ttf",
        "/Library/Fonts/Arial.ttf",
    ]
    for path in possible_paths:
        if os.path.exists(path):
            return path
    return None


def register_pdf_font() -> str:
    """Zaregistruje unicode font pre PDF."""
    font_path = find_font_path()
    if font_path:
        try:
            pdfmetrics.registerFont(TTFont("CustomPDFUnicode", font_path))
            return "CustomPDFUnicode"
        except Exception:
            pass
    return "Helvetica"


def clean_inline_markdown_for_pdf(text: str) -> str:
    """Vyčistí markdown syntax pred exportom do PDF."""
    text = text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    text = re.sub(r"\*\*(.*?)\*\*", r"\1", text)
    text = re.sub(r"\*(.*?)\*", r"\1", text)
    text = re.sub(r"`(.*?)`", r"\1", text)
    text = re.sub(r"\[(.*?)\]\((.*?)\)", r"\1 (\2)", text)
    return text


def markdown_to_story(content: str, styles: dict) -> list:
    """Prevod markdown obsahu do ReportLab story."""
    story = []
    lines = content.replace("\r\n", "\n").split("\n")
    bullet_buffer = []

    def flush_bullets():
        nonlocal bullet_buffer, story
        if bullet_buffer:
            items = [
                ListItem(Paragraph(clean_inline_markdown_for_pdf(item), styles["body"]))
                for item in bullet_buffer
            ]
            story.append(ListFlowable(items, bulletType="bullet", leftIndent=18))
            story.append(Spacer(1, 8))
            bullet_buffer = []

    for raw_line in lines:
        line = raw_line.strip()

        if not line:
            flush_bullets()
            story.append(Spacer(1, 8))
            continue

        if line == "---":
            flush_bullets()
            story.append(Spacer(1, 10))
            continue

        if line.startswith("- "):
            bullet_buffer.append(line[2:].strip())
            continue

        flush_bullets()

        if line.startswith("# "):
            story.append(Paragraph(clean_inline_markdown_for_pdf(line[2:]), styles["h1"]))
            story.append(Spacer(1, 12))
        elif line.startswith("## "):
            story.append(Paragraph(clean_inline_markdown_for_pdf(line[3:]), styles["h2"]))
            story.append(Spacer(1, 8))
        elif line.startswith("### "):
            story.append(Paragraph(clean_inline_markdown_for_pdf(line[4:]), styles["h3"]))
            story.append(Spacer(1, 6))
        elif line.startswith("http://") or line.startswith("https://"):
            url = clean_inline_markdown_for_pdf(line)
            story.append(Paragraph(f'<link href="{url}">{url}</link>', styles["link"]))
            story.append(Spacer(1, 6))
        else:
            story.append(Paragraph(clean_inline_markdown_for_pdf(line), styles["body"]))
            story.append(Spacer(1, 6))

    flush_bullets()
    return story

def get_content_signature(folder: Path) -> tuple:
    """Podpis obsahu priečinka pre cache."""
    files = get_markdown_paths(folder)
    return tuple((f.name, f.stat().st_mtime) for f in files)

@st.cache_data(show_spinner=False)
def build_full_pdf(case_signature: tuple, questionnaire_signature: tuple) -> bytes:
    """Vygeneruje jedno spoločné PDF so zadaním a dotazníkom."""
    buffer = BytesIO()
    font_name = register_pdf_font()

    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        leftMargin=42,
        rightMargin=42,
        topMargin=42,
        bottomMargin=42,
    )

    styles = getSampleStyleSheet()
    custom_styles = {
        "title": ParagraphStyle(
            "title",
            parent=styles["Title"],
            fontName=font_name,
            fontSize=20,
            leading=24,
            alignment=TA_CENTER,
            textColor=colors.black,
            spaceAfter=10,
        ),
        "subtitle": ParagraphStyle(
            "subtitle",
            parent=styles["BodyText"],
            fontName=font_name,
            fontSize=11,
            leading=14,
            alignment=TA_CENTER,
            textColor=colors.black,
            spaceAfter=18,
        ),
        "section": ParagraphStyle(
            "section",
            parent=styles["Heading1"],
            fontName=font_name,
            fontSize=16,
            leading=20,
            alignment=TA_LEFT,
            textColor=colors.black,
            spaceAfter=14,
        ),
        "h1": ParagraphStyle(
            "h1",
            parent=styles["Heading1"],
            fontName=font_name,
            fontSize=14,
            leading=18,
            textColor=colors.black,
            spaceAfter=8,
        ),
        "h2": ParagraphStyle(
            "h2",
            parent=styles["Heading2"],
            fontName=font_name,
            fontSize=12,
            leading=16,
            textColor=colors.black,
            spaceAfter=6,
        ),
        "h3": ParagraphStyle(
            "h3",
            parent=styles["Heading3"],
            fontName=font_name,
            fontSize=11,
            leading=14,
            textColor=colors.black,
            spaceAfter=4,
        ),
        "body": ParagraphStyle(
            "body",
            parent=styles["BodyText"],
            fontName=font_name,
            fontSize=10.5,
            leading=15,
            textColor=colors.black,
        ),
        "link": ParagraphStyle(
            "link",
            parent=styles["BodyText"],
            fontName=font_name,
            fontSize=10,
            leading=14,
            textColor=colors.blue,
        ),
    }

    story = []
    story.append(Paragraph("GYMBEAM CASE STUDY INTERN", custom_styles["title"]))
    story.append(Paragraph("Bc. Michal Jiříček", custom_styles["subtitle"]))
    story.append(Spacer(1, 10))

    story.append(Paragraph("ZADANIE", custom_styles["section"]))
    story.append(Spacer(1, 8))

    zadanie_files = get_markdown_paths(CASE_STUDY_DIR)
    for i, md_file in enumerate(zadanie_files):
        content = read_markdown_file(str(md_file), md_file.stat().st_mtime)
        story.extend(markdown_to_story(content, custom_styles))
        if i < len(zadanie_files) - 1:
            story.append(PageBreak())

    story.append(PageBreak())

    story.append(Paragraph("DOTAZNÍK", custom_styles["section"]))
    story.append(Spacer(1, 8))

    dotaznik_files = get_markdown_paths(QUESTIONNAIRE_DIR)
    for md_file in dotaznik_files:
        content = read_markdown_file(str(md_file), md_file.stat().st_mtime)
        story.extend(markdown_to_story(content, custom_styles))
        story.append(Spacer(1, 12))

    doc.build(story)
    pdf = buffer.getvalue()
    buffer.close()
    return pdf


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

        if st.button("ZADANIE", use_container_width=True):
            go_zadanie()

        if st.button("DOTAZNÍK", use_container_width=True):
            go_dotaznik()

        st.divider()

        # Odkazy
        st.markdown("<div class='sidebar-center'><strong>ODKAZY</strong></div>", unsafe_allow_html=True)
        st.write("")

        st.link_button("LINKEDLN", "http://www.linkedin.com/in/michal-jiricek", use_container_width=True)
        st.link_button("GITHUB", "https://github.com/jirmic14", use_container_width=True)
        st.link_button("STREAMLIT", "https://share.streamlit.io/user/jirmic14", use_container_width=True)
        st.link_button("YOUTUBE", "https://www.youtube.com/@jiricekmichal", use_container_width=True)

        st.divider()

        # Export
        st.markdown("<div class='sidebar-center'><strong>EXPORT</strong></div>", unsafe_allow_html=True)
        st.write("")

        pdf_bytes = build_full_pdf(
            get_content_signature(CASE_STUDY_DIR),
            get_content_signature(QUESTIONNAIRE_DIR),
        )

        st.download_button(
            label="STIAHNUŤ PDF",
            data=pdf_bytes,
            file_name="gymbeam_case_study_intern_michal_jiricek.pdf",
            mime="application/pdf",
            use_container_width=True,
        )

        # Logo úplne dole pod exportom
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


# ============================
# SEKČNÁ STRÁNKA
# ============================

def render_section(title: str, folder: Path, state_key: str):
    """Vykreslenie sekcie Zadanie alebo Dotazník."""
    files = get_markdown_paths(folder)

    if not files:
        st.error(f"V priečinku `{folder.name}` sa nenašli žiadne .md súbory.")
        if st.button("Späť na hlavné menu"):
            go_home()
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

    nav1, nav2, nav3 = st.columns([1.2, 1.1, 1.2])

    with nav1:
        prev_disabled = st.session_state[state_key] == 1
        if st.button(
            "⬅ Predchádzajúca",
            use_container_width=True,
            key=f"prev_{state_key}",
            disabled=prev_disabled,
        ):
            st.session_state[state_key] -= 1

    with nav2:
        st.markdown(
            f"<p style='text-align:center; font-weight:700; margin-top: 0.7rem;'>Otázka {st.session_state[state_key]} z {max_questions}</p>",
            unsafe_allow_html=True,
        )

    with nav3:
        next_disabled = st.session_state[state_key] == max_questions
        if st.button(
            "Nasledujúca ➡",
            use_container_width=True,
            key=f"next_{state_key}",
            disabled=next_disabled,
        ):
            st.session_state[state_key] += 1

    st.divider()

    current_file = files[st.session_state[state_key] - 1]
    content = read_markdown_file(str(md_file))
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