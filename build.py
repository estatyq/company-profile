# -*- coding: utf-8 -*-
"""Build the Company Profile PDFs (EN + ID) and the Web Presentation (site/).

Usage:
    python build.py            -> Builds PDFs in output/ and Web version in site/
    python build.py --preview  -> Also renders PNG previews of every PDF page
"""
import asyncio
import html
import json
import os
import pathlib
import re
import shutil
import sys
from datetime import date

from PIL import Image
from playwright.async_api import async_playwright

from content import (
    BRAND_NAME,
    CONTACTS,
    LANGUAGES,
    PRODUCT_URLS,
    PRODUCTS,
    language_text,
    product_text,
)

ROOT = pathlib.Path(__file__).resolve().parent
SCREENS = ROOT / "assets" / "screens"
WEB = ROOT / "assets" / "web"
OUT = ROOT / "output"
HTML_DIR = OUT / "html"
PREVIEW = OUT / "preview"
SITE_DIR = ROOT / "site"
PUBLIC_BASE_URL = os.getenv("PUBLIC_BASE_URL", "https://xcombine.xyz").rstrip("/")

e = html.escape

# --------------------------------------------------------------------------- images


def prepare_images():
    """Crop / compress website screenshots into web-ready JPEGs."""
    WEB.mkdir(parents=True, exist_ok=True)

    def save(img, name, width=None, quality=86):
        img = img.convert("RGB")
        if width and img.width > width:
            img = img.resize((width, round(img.height * width / img.width)), Image.LANCZOS)
        img.save(WEB / name, "JPEG", quality=quality, optimize=True, progressive=True)

    if (SCREENS / "rieltix_crm-properties.png").exists():
        crm = Image.open(SCREENS / "rieltix_crm-properties.png")
        save(crm.crop((0, 0, 1600, 700)), "rieltix_crm.jpg")
    if (SCREENS / "rieltix_public-site.png").exists():
        save(Image.open(SCREENS / "rieltix_public-site.png"), "rieltix_site.jpg")
    if (SCREENS / "mapest_cards.png").exists():
        cards = Image.open(SCREENS / "mapest_cards.png")
        save(cards.crop((180, 200, 2700, 1460)), "mapest_cards.jpg", width=1600)
    if (SCREENS / "mapest_mobile.png").exists():
        save(Image.open(SCREENS / "mapest_mobile.png"), "mapest_mobile.jpg", width=600, quality=88)
    if (SCREENS / "forma_en_doc.png").exists():
        save(Image.open(SCREENS / "forma_en_doc.png"), "forma_doc.jpg", width=1600)


# --------------------------------------------------------------------------- icons

ICONS = {
    "crm": '<rect x="3" y="3" width="7" height="9" rx="1.5"/><rect x="14" y="3" width="7" height="5" rx="1.5"/><rect x="14" y="12" width="7" height="9" rx="1.5"/><rect x="3" y="16" width="7" height="5" rx="1.5"/>',
    "bot": '<rect x="4" y="8" width="16" height="12" rx="3"/><path d="M12 8V4"/><circle cx="12" cy="3" r="1"/><path d="M9 13v1.5M15 13v1.5"/><path d="M2 13v3M22 13v3"/>',
    "zap": '<path d="M13 2 3 14h9l-1 8 10-12h-9l1-8z"/>',
    "globe": '<circle cx="12" cy="12" r="10"/><path d="M2 12h20"/><path d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"/>',
    "code": '<polyline points="16 18 22 12 16 6"/><polyline points="8 6 2 12 8 18"/><path d="M14 4l-4 16"/>',
    "link": '<path d="M10 13a5 5 0 0 0 7.54.54l3-3a5 5 0 0 0-7.07-7.07l-1.72 1.71"/><path d="M14 11a5 5 0 0 0-7.54-.54l-3 3a5 5 0 0 0 7.07 7.07l1.71-1.71"/>',
    "target": '<circle cx="12" cy="12" r="10"/><circle cx="12" cy="12" r="6"/><circle cx="12" cy="12" r="2"/>',
    "sliders": '<path d="M4 21v-7M4 10V3M12 21v-9M12 8V3M20 21v-5M20 12V3M1 14h6M9 8h6M17 16h6"/>',
    "check": '<path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/><polyline points="22 4 12 14.01 9 11.01"/>',
    "wallet": '<path d="M20 7V5a2 2 0 0 0-2-2H5a2 2 0 0 0 0 4h15v4"/><path d="M3 5v14a2 2 0 0 0 2 2h15v-4"/><path d="M17 11h4v6h-4a3 3 0 0 1 0-6z"/>',
    "layers": '<polygon points="12 2 2 7 12 12 22 7 12 2"/><polyline points="2 17 12 22 22 17"/><polyline points="2 12 12 17 22 12"/>',
    "refresh": '<polyline points="23 4 23 10 17 10"/><polyline points="1 20 1 14 7 14"/><path d="M3.51 9a9 9 0 0 1 14.85-3.36L23 10M1 14l4.64 4.36A9 9 0 0 0 20.49 15"/>',
    "inbox": '<polyline points="22 12 16 12 14 15 10 15 8 12 2 12"/><path d="M5.45 5.11 2 12v6a2 2 0 0 0 2 2h16a2 2 0 0 0 2-2v-6l-3.45-6.89A2 2 0 0 0 16.76 4H7.24a2 2 0 0 0-1.79 1.11z"/>',
    "sparkle": '<path d="M12 3l1.8 5.2L19 10l-5.2 1.8L12 17l-1.8-5.2L5 10l5.2-1.8z"/><path d="M19 15l.8 2.2L22 18l-2.2.8L19 21l-.8-2.2L16 18l2.2-.8z"/>',
    "database": '<ellipse cx="12" cy="5" rx="9" ry="3"/><path d="M21 12c0 1.66-4 3-9 3s-9-1.34-9-3"/><path d="M3 5v14c0 1.66 4 3 9 3s9-1.34 9-3V5"/>',
    "tasks": '<polyline points="9 11 12 14 22 4"/><path d="M21 12v7a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11"/>',
    "bell": '<path d="M18 8A6 6 0 0 0 6 8c0 7-3 9-3 9h18s-3-2-3-9"/><path d="M13.73 21a2 2 0 0 1-3.46 0"/>',
    "whatsapp": '<path d="M21 11.5a8.38 8.38 0 0 1-.9 3.8 8.5 8.5 0 0 1-7.6 4.7 8.38 8.38 0 0 1-3.8-.9L3 21l1.9-5.7a8.38 8.38 0 0 1-.9-3.8 8.5 8.5 0 0 1 4.7-7.6 8.38 8.38 0 0 1 3.8-.9h.5a8.48 8.48 0 0 1 8 8v.5z"/>',
    "telegram": '<path d="M22 2 11 13"/><path d="M22 2 15 22l-4-9-9-4 20-7z"/>',
    "email": '<rect x="2" y="4" width="20" height="16" rx="2"/><polyline points="22,6 12,13 2,6"/>',
    "website": '<circle cx="12" cy="12" r="10"/><path d="M2 12h20"/><path d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"/>',
    "out": '<path d="M7 17 17 7"/><path d="M7 7h10v10"/>',
    "tick": '<polyline points="20 6 9 17 4 12"/>',
    "x": '<path d="M18 6 6 18M6 6l12 12"/>',
    "project": '<path d="M12 2l9 5v10l-9 5-9-5V7z"/><path d="M12 22V12M21 7l-9 5-9-5"/>',
    "calendar": '<rect x="3" y="4" width="18" height="18" rx="2"/><path d="M16 2v4M8 2v4M3 10h18"/><path d="m9 16 2 2 4-4"/>',
    "download": '<path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="7 10 12 15 17 10"/><line x1="12" y1="15" x2="12" y2="3"/>',
}


def icon(name, cls=""):
    return (
        f'<svg class="{cls}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" '
        f'stroke-linecap="round" stroke-linejoin="round">{ICONS.get(name, "")}</svg>'
    )


LOGO = (
    '<svg viewBox="0 0 32 32" fill="none" xmlns="http://www.w3.org/2000/svg">'
    '<defs>'
    '<linearGradient id="xc-a" x1="4" y1="4" x2="28" y2="28" gradientUnits="userSpaceOnUse">'
    '<stop offset="0%" stop-color="#38bdf8"/>'
    '<stop offset="100%" stop-color="#0284c7"/>'
    '</linearGradient>'
    '<linearGradient id="xc-b" x1="28" y1="4" x2="4" y2="28" gradientUnits="userSpaceOnUse">'
    '<stop offset="0%" stop-color="#22d3ee"/>'
    '<stop offset="100%" stop-color="#38bdf8"/>'
    '</linearGradient>'
    '</defs>'
    '<rect x="2" y="2" width="28" height="28" rx="8" fill="#0c1527" stroke="rgba(56, 189, 248, 0.3)" stroke-width="1.2"/>'
    '<path d="M9.5 9.5L22.5 22.5" stroke="url(#xc-a)" stroke-width="3" stroke-linecap="round"/>'
    '<path d="M22.5 9.5L18 14" stroke="url(#xc-b)" stroke-width="3" stroke-linecap="round"/>'
    '<path d="M14 18L9.5 22.5" stroke="url(#xc-b)" stroke-width="3" stroke-linecap="round"/>'
    '<circle cx="16" cy="16" r="2.2" fill="#22d3ee"/>'
    '</svg>'
)

# --------------------------------------------------------------------------- helpers


def contact_href(kind, value):
    if not value:
        return None
    if kind == "whatsapp":
        return "https://wa.me/" + re.sub(r"\D", "", value)
    if kind == "telegram":
        return "https://t.me/" + value.lstrip("@").replace("https://t.me/", "")
    if kind == "email":
        return "mailto:" + value
    if kind == "website":
        return value if value.startswith("http") else "https://" + value
    return None


def host(url):
    return url.replace("https://", "").replace("http://", "").rstrip("/")


def brand_mark(t):
    if BRAND_NAME:
        return f'<div class="mark">{LOGO}<span class="brand-name">{e(BRAND_NAME)}</span><span class="submark">digital agency</span></div>'
    return f'<div class="mark">{LOGO}<span>{e(t["descriptor"])}</span></div>'


def chrome(t, eyebrow, page_no, total):
    shown_products = PRODUCTS[:4]
    links = "".join(f'<a href="{e(p["url"])}">{e(host(p["url"]))}</a>' for p in shown_products)
    if len(PRODUCTS) > len(shown_products):
        links += f'<span class="links-more">+{len(PRODUCTS) - len(shown_products)}</span>'
    top = (
        f'<div class="bg-glow"></div><div class="bg-grid"></div>'
        f'<header class="top"><div class="eyebrow"><span class="dot"></span>{e(eyebrow)}</div>'
        f'{brand_mark(t)}</header>'
    )
    foot = (
        f'<footer class="foot"><span>{e(t["doc_label"])} · {t["year"]}</span>'
        f'<span class="links">{links}</span><span class="num">{page_no:02d} / {total:02d}</span></footer>'
    )
    return top, foot


# --------------------------------------------------------------------------- pages


def page_cover(t, lang, img_prefix="../../assets/web/"):
    long_cls = " long" if len(t["cover_title_a"] + t["cover_title_b"]) > 44 else ""
    pills = ""
    for p in PRODUCTS[:3]:
        name = p["name"]
        url = p["url"]
        sub = product_text(p, "cover_sub", lang)
        cls = p.get("badge_color", "r")
        pills += (
            f'<a class="pill" href="{url}"><span class="pm {cls}">{name[0].upper()}</span>'
            f'<span><b>{e(name)}</b><small>{e(sub)} · {host(url)}</small></span>{icon("out")}</a>'
        )
    if len(PRODUCTS) > 3:
        pills += (
            f'<a class="pill pill-more" href="#products"><span class="pm">+{len(PRODUCTS) - 3}</span>'
            f'<span><b>{e(t.get("ui_more_projects", "More projects"))}</b>'
            f'<small>{e(t.get("ui_view_portfolio", "View portfolio"))}</small></span>{icon("out")}</a>'
        )
    return f"""
<section class="page cover">
  <div class="bg-glow"></div><div class="bg-grid"></div>
  <header class="top">{brand_mark(t)}
    <div class="eyebrow" data-cover-eyebrow>{e(t.get("cover_eyebrow", "Software · AI · Automation"))}</div></header>
  <div class="left">
    <span class="chip"><span class="dot"></span>{e(t["cover_chip"])}</span>
    <h1 class="h1{long_cls}">{e(t["cover_title_a"])}<br><span class="grad">{e(t["cover_title_b"])}</span></h1>
    <div class="sub">{e(t["cover_sub"])}</div>
    <p class="lead">{e(t["cover_lead"])}</p>
  </div>
  <div class="collage">
    <div class="frame f1"><div class="bar"><i></i><i></i><i></i><span>rieltix.com · catalog</span></div>
      <img src="{img_prefix}rieltix_site.jpg" alt="Rieltix"></div>
    <div class="frame f2"><div class="bar"><i></i><i></i><i></i><span>rieltix.com · CRM</span></div>
      <img src="{img_prefix}rieltix_crm.jpg" alt="Rieltix CRM"></div>
    <div class="phone ph"><img src="{img_prefix}mapest_mobile.jpg" alt="Mapest"></div>
  </div>
  <div class="fade-r"></div><div class="fade-b"></div>
  <div class="products"><div class="label">{e(t["cover_products_label"])}</div><div class="row">{pills}</div></div>
</section>"""


def page_who(t, page_no, total):
    top, foot = chrome(t, t["p2_eyebrow"], page_no, total)
    probs = "".join(
        f'<div class="card prob"><span class="n">0{i + 1}</span><div><div class="h3">{e(h)}</div>'
        f'<p class="body">{e(b)}</p></div></div>'
        for i, (h, b) in enumerate(t["p2_problems"])
    )
    flow_icons = ["inbox", "sparkle", "database", "tasks", "bell"]
    nodes = []
    for i, (h, s) in enumerate(t["p2_flow"]):
        hl = " hl" if i == 1 else ""
        nodes.append(
            f'<div class="node{hl}"><div class="icon">{icon(flow_icons[i])}</div><b>{e(h)}</b><small>{e(s)}</small></div>'
        )
    flow = '<div class="arrow"></div>'.join(nodes)
    rows = "".join(
        f'<tr><td class="bad"><span>{icon("x")}{e(a)}</span></td>'
        f'<td class="good"><span style="color:var(--text)"><span style="color:var(--cyan)">{icon("tick")}</span>{e(b)}</span></td></tr>'
        for a, b in t["p2_cmp"]
    )
    h_bad, h_good = t["p2_cmp_head"]
    return f"""
<section class="page p2">{top}
  <div class="head">
    <h2 class="h2">{e(t["p2_title_a"])}<br><span class="grad">{e(t["p2_title_b"])}</span></h2>
    <p class="lead">{e(t["p2_lead"])}</p>
  </div>
  <div class="problems"><div class="label">{e(t["p2_problems_label"])}</div><div class="grid">{probs}</div></div>
  <div class="bottom">
    <div class="card flowcard"><div class="label">{e(t["p2_flow_label"])}</div><div class="flow">{flow}</div></div>
    <div class="card cmpcard"><div class="label">{e(t["p2_cmp_label"])}</div>
      <table class="cmp"><tr><th>{e(h_bad)}</th><th class="good">{e(h_good)}</th></tr>{rows}</table></div>
  </div>
{foot}</section>"""


def page_products(t, lang, products, page_no, total, chunk_index=0, chunk_count=1,
                  img_prefix="../../assets/web/"):
    eyebrow = t["p3_eyebrow"]
    title = t["p3_title"]
    lead = t["p3_lead"]
    if chunk_index:
        eyebrow = f"{t['p3_eyebrow']} · {chunk_index + 1}"
        title = t.get("p3_title_continued", title)
    top, foot = chrome(t, eyebrow, page_no, total)
    cards = ""
    col_style = f"grid-template-columns: repeat({len(products)}, 1fr);" if len(products) <= 4 else ""
    for p in products:
        url = p["url"]
        name = p["name"]
        shot = p.get("shot", "")
        status = product_text(p, "status", lang) or "Live"
        tag = product_text(p, "tag", lang)
        features = product_text(p, "features", lang)
        benefit = product_text(p, "benefit", lang)
        feats = "".join(f"<li>{icon('tick')}<span>{e(f)}</span></li>" for f in features)
        cards += f"""
    <div class="card prod">
      <a class="shot" href="{url}"><img src="{img_prefix}{shot}" alt="{e(name)}">
        <span class="status"><i></i>{e(status)}</span></a>
      <div class="info">
        <div class="name"><b>{e(name)}</b><a href="{url}">{host(url)}{icon("out")}</a></div>
        <div class="tag">{e(tag)}</div>
        <ul>{feats}</ul>
        <div class="benefit"><span class="label">{e(t["benefit_label"])}</span>{e(benefit)}</div>
      </div>
    </div>"""
    if not cards:
        cards = '<div class="portfolio-empty"><b>Portfolio</b><span>Add your first project in the editor.</span></div>'
    return f"""
<section class="page p3"{f' id="products"' if chunk_index == 0 else ''} data-product-page="{chunk_index}">{top}
  <div class="head"><h2 class="h2">{e(title)}</h2><p class="lead">{e(lead)}</p></div>
  <div class="cards" style="{col_style}">{cards}</div>
{foot}</section>"""


def page_services(t, page_no, total):
    top, foot = chrome(t, t["p4_eyebrow"], page_no, total)
    cards = ""
    for ic, title, body, ex in t["services"]:
        ex_html = e(ex)
        for marker in ("Voice AI assistant — in development", "Asisten suara AI — sedang dikembangkan"):
            if marker in ex:
                ex_html = e(ex.replace(marker, "")).rstrip(". ") + ". <em>" + e(marker) + "</em>"
        cards += (
            f'<div class="card svc"><div class="toprow"><div class="icon">{icon(ic)}</div>'
            f'<div class="h3">{e(title)}</div></div><p class="body">{e(body)}</p>'
            f'<div class="ex"><b>{e(t["example_label"])}</b>{ex_html}</div></div>'
        )
    return f"""
<section class="page p4">{top}
  <div class="head"><h2 class="h2">{e(t["p4_title"])}</h2><p class="lead">{e(t["p4_lead"])}</p></div>
  <div class="grid">{cards}</div>
{foot}</section>"""


def page_why(t, page_no, total):
    top, foot = chrome(t, t["p5_eyebrow"], page_no, total)
    phases = "".join(
        f'<div class="phase"><div class="dotc"><i></i></div><div><div class="t"><span>{e(a)}</span>{e(b)}</div>'
        f'<div class="d">{e(c)}</div></div></div>'
        for a, b, c in t["p5_phases"]
    )
    bens = "".join(
        f'<div class="card ben"><div class="icon">{icon(ic)}</div><div><div class="h3">{e(h)}</div>'
        f'<p class="body">{e(b)}</p></div></div>'
        for ic, h, b in t["benefits"]
    )
    return f"""
<section class="page p5">{top}
  <div class="leftcol">
    <h2 class="h2">{e(t["p5_title_a"])}<br><span class="grad">{e(t["p5_title_b"])}</span></h2>
    <p class="lead">{e(t["p5_lead"])}</p>
    <div class="card phases"><div class="label" style="margin-bottom:14px">{e(t["p5_phases_label"])}</div>{phases}</div>
  </div>
  <div class="grid">{bens}</div>
{foot}</section>"""


def page_contact(t, page_no, total):
    top, foot = chrome(t, t["p6_eyebrow"], page_no, total)
    steps = "".join(
        f'<div class="step"><div class="num">{i + 1}</div><b>{e(h)}</b><p>{e(b)}</p></div>'
        for i, (h, b) in enumerate(t["steps"])
    )
    model_icons = ["project", "calendar"]
    models = "".join(
        f'<div class="card model"><div class="icon">{icon(model_icons[i])}</div><div><div class="h3">{e(h)}</div>'
        f'<p class="body">{e(b)}</p></div></div>'
        for i, (h, b) in enumerate(t["models"])
    )
    contacts = ""
    for kind in ("whatsapp", "telegram", "email", "website"):
        val = CONTACTS.get(kind, "")
        href = contact_href(kind, val)
        inner = (
            f'<div class="ci">{icon(kind)}</div><div><small>{e(t["contact_labels"][kind])}</small>'
            + (f"<b>{e(val)}</b>" if val else f'<b class="ph">{e(t["contact_placeholders"][kind])}</b>')
            + "</div>"
        )
        contacts += f'<a class="contact" href="{href}">{inner}</a>' if href else f'<div class="contact">{inner}</div>'
    return f"""
<section class="page p6">{top}
  <div class="title"><h2 class="h2">{e(t["p6_title"])}</h2></div>
  <div class="steps">{steps}</div>
  <div class="bottom">
    <div class="models"><div class="label">{e(t["models_label"])}</div>{models}</div>
    <div class="cta">
      <div class="q">{e(t["cta_a"])} <span class="grad">{e(t["cta_b"])}</span></div>
      <p class="note">{e(t["cta_note"])}</p>
      <div class="contacts">{contacts}</div>
    </div>
  </div>
{foot}</section>"""


def balanced_chunks(items, page_size=3):
    if not items:
        return [[]]
    page_count = (len(items) + page_size - 1) // page_size
    base_size, extra = divmod(len(items), page_count)
    chunks = []
    cursor = 0
    for index in range(page_count):
        size = base_size + (1 if index < extra else 0)
        chunks.append(items[cursor:cursor + size])
        cursor += size
    return chunks


def build_pages(t, lang, img_prefix, page_size=3):
    chunks = balanced_chunks(PRODUCTS, page_size)
    total = 2 + len(chunks) + 3
    pages = [
        page_cover(t, lang, img_prefix=img_prefix),
        page_who(t, 2, total),
    ]
    for i, chunk in enumerate(chunks):
        pages.append(
            page_products(
                t, lang, chunk, 3 + i, total,
                chunk_index=i, chunk_count=len(chunks), img_prefix=img_prefix,
            )
        )
    services_page = 3 + len(chunks)
    pages.extend([
        page_services(t, services_page, total),
        page_why(t, services_page + 1, total),
        page_contact(t, services_page + 2, total),
    ])
    return pages


def public_profile_data(lang):
    """Serializable content used by the in-browser editor."""
    t = language_text(lang)
    return {
        "version": 1,
        "lang": lang,
        "brand": BRAND_NAME or t["descriptor"],
        "logo": "",
        "descriptor": t["descriptor"],
        "docLabel": t["doc_label"],
        "year": t["year"],
        "contacts": dict(CONTACTS),
        "products": [
            {
                "id": p["id"],
                "name": p["name"],
                "url": p["url"],
                "shot": p.get("shot", ""),
                "coverSub": product_text(p, "cover_sub", lang),
                "status": product_text(p, "status", lang) or "Live",
                "tag": product_text(p, "tag", lang),
                "features": list(product_text(p, "features", lang)),
                "benefit": product_text(p, "benefit", lang),
                "badgeColor": p.get("badge_color", "r"),
            }
            for p in PRODUCTS
        ],
        "text": t,
    }


def render_html_pdf(lang):
    t = language_text(lang)
    pages = build_pages(t, lang, img_prefix="../../assets/web/")
    title = f"{t['doc_label']} — {BRAND_NAME or t['descriptor']} ({lang.upper()})"
    return f"""<!doctype html>
<html lang="{t['lang']}"><head><meta charset="utf-8"><title>{e(title)}</title>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Geist:wght@300..800&family=Geist+Mono:wght@400;500;600&display=swap" rel="stylesheet">
<link rel="stylesheet" href="../../template/style.css"></head>
<body>{''.join(pages)}</body></html>"""


def render_web_site(lang):
    t = language_text(lang)
    meta = LANGUAGES[lang]
    wa_href = contact_href("whatsapp", CONTACTS.get("whatsapp"))
    wa_href_attr = f' href="{e(wa_href)}"' if wa_href else ""
    wa_hidden = "" if wa_href else " hidden"
    wa_button = (
        f'<a class="btn-cta" id="whatsapp-cta"{wa_href_attr}{wa_hidden} '
        f'target="_blank" rel="noopener">{icon("whatsapp")}<span>{e(t["ui_whatsapp_chat"])}</span></a>'
    )

    pages = build_pages(t, lang, img_prefix="assets/web/")
    title = f"{BRAND_NAME or t['descriptor']} — {t['doc_label']} ({lang.upper()})"
    profile_json = json.dumps(public_profile_data(lang), ensure_ascii=False).replace("</", "<\\/")
    brand = BRAND_NAME or t["descriptor"]
    page_path = meta["html"] if lang != "en" else ""
    canonical = f"{PUBLIC_BASE_URL}/{page_path}"
    language_options = "".join(
        f'<option value="{e(meta["html"])}" data-code="{code}"{" selected" if code == lang else ""}>'
        f'{e(meta["native"])}</option>'
        for code, meta in LANGUAGES.items()
    )
    language_alternates = "".join(
        f'<link rel="alternate" hreflang="{code}" '
        f'href="{PUBLIC_BASE_URL}/{meta["html"] if code != "en" else ""}">'
        for code, meta in LANGUAGES.items()
    )
    language_alternates += (
        f'<link rel="alternate" hreflang="x-default" href="{PUBLIC_BASE_URL}/">'
    )
    social_image = f"{PUBLIC_BASE_URL}/assets/web/{PRODUCTS[0]['shot']}"
    og_locales = {
        "en": "en_US",
        "id": "id_ID",
        "uk": "uk_UA",
        "de": "de_DE",
        "es": "es_ES",
    }
    organization_schema = {
        "@context": "https://schema.org",
        "@type": "ProfessionalService",
        "@id": f"{PUBLIC_BASE_URL}/#organization",
        "name": brand,
        "url": f"{PUBLIC_BASE_URL}/",
        "description": t["cover_lead"],
        "logo": f"{PUBLIC_BASE_URL}/assets/favicon.svg",
        "image": social_image,
        "areaServed": "Worldwide",
        "knowsLanguage": list(LANGUAGES),
        "serviceType": [service[1] for service in t["services"]],
    }
    schema_json = json.dumps(
        organization_schema, ensure_ascii=False
    ).replace("</", "<\\/")
    language_cards = "".join(
        f'<a class="language-choice" href="{e(meta["html"])}" data-language-choice="{code}">'
        f'<span class="language-code">{e(meta["label"])}</span>'
        f'<span><b>{e(meta["native"])}</b><small>{code.upper()}</small></span>'
        f'{icon("out")}</a>'
        for code, meta in LANGUAGES.items()
    )

    return f"""<!doctype html>
<html lang="{t['lang']}"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{e(title)}</title>
<meta name="theme-color" content="#05080f">
<meta name="description" content="{e(t['cover_lead'])}">
<meta name="robots" content="index,follow,max-image-preview:large,max-snippet:-1,max-video-preview:-1">
<link rel="canonical" href="{canonical}">
<link rel="icon" href="assets/favicon.svg" type="image/svg+xml">
<link rel="manifest" href="assets/site.webmanifest">
<meta property="og:type" content="website">
<meta property="og:site_name" content="{e(brand)}">
<meta property="og:title" content="{e(title)}">
<meta property="og:description" content="{e(t['cover_lead'])}">
<meta property="og:url" content="{canonical}">
<meta property="og:image" content="{social_image}">
<meta property="og:locale" content="{og_locales[lang]}">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{e(title)}">
<meta name="twitter:description" content="{e(t['cover_lead'])}">
<meta name="twitter:image" content="{social_image}">
{language_alternates}
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Geist:wght@300..800&family=Geist+Mono:wght@400;500;600&display=swap" rel="stylesheet">
<link rel="stylesheet" href="assets/style.css">
<link rel="stylesheet" href="assets/web.css">
<link rel="stylesheet" href="assets/editor.css">
</head>
<body>

<nav class="web-bar">
  <label class="language-select-wrap">
    <span class="sr-only">Language / Мова / Sprache / Idioma</span>
    <select id="language-select" aria-label="Language">{language_options}</select>
  </label>
  <span class="sep"></span>
  <button type="button" id="edit-profile">{icon("sliders")}<span>{e(t.get("ui_edit", "Edit"))}</span></button>
  <span class="sep"></span>
  <button type="button" id="download-pdf" title="Откроется диалог печати. Выберите «Сохранить как PDF».">{icon("download")}<span>PDF</span></button>
  <button type="button" id="download-word">{icon("download")}<span>Word</span></button>
  <span class="sep"></span>{wa_button}
</nav>

<main class="deck-container">
  {''.join(pages)}
</main>

<div class="language-gate" id="language-gate" hidden>
  <div class="language-gate-card" role="dialog" aria-modal="true" aria-labelledby="language-gate-title">
    <div class="language-gate-brand">{LOGO}<span>Company Profile</span></div>
    <span class="language-gate-kicker">Choose language · Оберіть мову · Sprache wählen · Elige idioma</span>
    <h2 id="language-gate-title">How would you like to view the site?</h2>
    <p>Choose a language. You can change it at any time from the top menu.</p>
    <div class="language-grid">{language_cards}</div>
  </div>
</div>

<script id="profile-config" type="application/json">{profile_json}</script>
<script id="organization-schema" type="application/ld+json">{schema_json}</script>
<script src="assets/docx.iife.js"></script>
<script src="assets/app.js"></script>
<script>
  function rescale() {{
    const w = window.innerWidth;
    const pages = document.querySelectorAll('.deck-container .page');
    if (w < 1320 && w >= 768) {{
      const scale = (w - 32) / 1280;
      pages.forEach(p => {{
        p.style.transform = `scale(${{scale}})`;
        p.style.marginBottom = `${{-(720 * (1 - scale))}}px`;
      }});
    }} else if (w < 768) {{
      const scale = (w - 24) / 1280;
      pages.forEach(p => {{
        p.style.transform = `scale(${{scale}})`;
        p.style.marginBottom = `${{-(720 * (1 - scale))}}px`;
      }});
    }} else {{
      pages.forEach(p => {{
        p.style.transform = 'none';
        p.style.marginBottom = '0';
      }});
    }}
  }}
  window.rescaleProfileDeck = rescale;
  window.addEventListener('resize', rescale);
  window.addEventListener('load', rescale);
  rescale();
</script>

</body></html>"""


def write_seo_files():
    """Write crawler directives, multilingual sitemap and web manifest."""
    sitemap_entries = []
    for code, meta in LANGUAGES.items():
        page_url = f"{PUBLIC_BASE_URL}/{meta['html'] if code != 'en' else ''}"
        alternates = "".join(
            f'<xhtml:link rel="alternate" hreflang="{alt_code}" '
            f'href="{PUBLIC_BASE_URL}/{alt_meta["html"] if alt_code != "en" else ""}"/>'
            for alt_code, alt_meta in LANGUAGES.items()
        )
        alternates += (
            f'<xhtml:link rel="alternate" hreflang="x-default" '
            f'href="{PUBLIC_BASE_URL}/"/>'
        )
        sitemap_entries.append(
            f"<url><loc>{html.escape(page_url)}</loc>"
            f"{alternates}"
            f"<lastmod>{date.today().isoformat()}</lastmod></url>"
        )
    sitemap = (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" '
        'xmlns:xhtml="http://www.w3.org/1999/xhtml">\n'
        + "\n".join(sitemap_entries)
        + "\n</urlset>\n"
    )
    robots = (
        "User-agent: *\n"
        "Allow: /\n"
        "Disallow: /admin\n"
        "Disallow: /api/admin/\n"
        f"Sitemap: {PUBLIC_BASE_URL}/sitemap.xml\n"
    )
    brand = BRAND_NAME or language_text("en")["descriptor"]
    manifest = json.dumps(
        {
            "name": brand,
            "short_name": brand[:24],
            "start_url": "/",
            "display": "standalone",
            "background_color": "#05080f",
            "theme_color": "#05080f",
            "icons": [
                {
                    "src": "/assets/favicon.svg",
                    "sizes": "any",
                    "type": "image/svg+xml",
                    "purpose": "any",
                }
            ],
        },
        ensure_ascii=False,
        indent=2,
    )
    (SITE_DIR / "robots.txt").write_text(robots, encoding="utf-8")
    (SITE_DIR / "sitemap.xml").write_text(sitemap, encoding="utf-8")
    (SITE_DIR / "assets" / "site.webmanifest").write_text(
        manifest, encoding="utf-8"
    )


# --------------------------------------------------------------------------- build execution


async def build(preview=False):
    prepare_images()
    HTML_DIR.mkdir(parents=True, exist_ok=True)
    SITE_DIR.mkdir(parents=True, exist_ok=True)
    site_assets = SITE_DIR / "assets"
    site_assets.mkdir(parents=True, exist_ok=True)

    # 1. Build PDF templates & PDFs
    results = []
    async with async_playwright() as p:
        browser = await p.chromium.launch(channel="chrome")
        page = await browser.new_page(viewport={"width": 1280, "height": 720})
        for lang, meta in LANGUAGES.items():
            html_path = HTML_DIR / f"profile_{lang}.html"
            html_path.write_text(render_html_pdf(lang), encoding="utf-8")
            await page.goto(html_path.as_uri(), wait_until="networkidle")
            await page.evaluate("document.fonts.ready")
            await page.wait_for_timeout(600)
            fam = await page.evaluate("document.fonts.check('600 20px Geist')")
            pdf_path = OUT / f"Company_Profile_{meta['file_suffix']}.pdf"
            await page.pdf(
                path=str(pdf_path),
                width="1280px",
                height="720px",
                print_background=True,
                prefer_css_page_size=True,
            )
            results.append((pdf_path, fam))
            print(f"[PDF] {pdf_path.name} ({pdf_path.stat().st_size / 1024:.0f} KB, Geist: {fam})", flush=True)

            # Copy PDF to site/ for 1-click download on the web
            shutil.copy2(pdf_path, SITE_DIR / pdf_path.name)
        await browser.close()

    # 2. Build Web site in site/
    # Merge generated screenshots without deleting admin-uploaded images.
    site_web_assets = SITE_DIR / "assets" / "web"
    site_web_assets.mkdir(parents=True, exist_ok=True)
    shutil.copytree(WEB, site_web_assets, dirs_exist_ok=True)
    (site_web_assets / "uploads").mkdir(parents=True, exist_ok=True)
    shutil.copy2(ROOT / "template" / "style.css", site_assets / "style.css")
    shutil.copy2(ROOT / "template" / "web.css", site_assets / "web.css")
    shutil.copy2(ROOT / "template" / "editor.css", site_assets / "editor.css")
    shutil.copy2(ROOT / "template" / "app.js", site_assets / "app.js")
    shutil.copy2(ROOT / "template" / "favicon.svg", site_assets / "favicon.svg")
    docx_bundle = pathlib.Path(
        r"C:\Users\maxhy\.cache\codex-runtimes\codex-primary-runtime\dependencies"
        r"\node\node_modules\docx\dist\index.iife.js"
    )
    if not docx_bundle.exists():
        raise FileNotFoundError(
            "docx browser bundle is missing. Run this build from the Codex desktop workspace."
        )
    shutil.copy2(docx_bundle, site_assets / "docx.iife.js")
    if (ROOT / "template" / "vercel.json").exists():
        shutil.copy2(ROOT / "template" / "vercel.json", SITE_DIR / "vercel.json")

    admin_store_path = ROOT / "data" / "profile.json"
    admin_store = None
    if admin_store_path.exists():
        try:
            admin_store = json.loads(admin_store_path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            admin_store = None

    # Render one language-specific landing page per registry entry. Existing
    # admin edits remain the public data source when the site is regenerated.
    for lang, meta in LANGUAGES.items():
        (SITE_DIR / meta["html"]).write_text(render_web_site(lang), encoding="utf-8")
        if admin_store and admin_store.get("languages", {}).get(lang):
            language_data = admin_store["languages"][lang]
            published = {
                "version": 2,
                "lang": lang,
                "brand": admin_store.get("brand", ""),
                "logo": admin_store.get("logo", ""),
                "contacts": admin_store.get("contacts", {}),
                "products": language_data.get("products", []),
                "text": language_data.get("text", {}),
            }
        else:
            profile_data = public_profile_data(lang)
            published = {
                "version": profile_data["version"],
                "lang": lang,
                "brand": profile_data["brand"],
                "logo": profile_data["logo"],
                "contacts": profile_data["contacts"],
                "products": profile_data["products"],
            }
        (SITE_DIR / f"profile-{lang}.json").write_text(
            json.dumps(published, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
    write_seo_files()
    print(
        f"[WEB] Static site generated in '{SITE_DIR.name}/' "
        f"({len(LANGUAGES)} languages + PDFs + Word)",
        flush=True,
    )

    # 3. Build default Word exports from the same browser-side renderer used by
    # the editor, so static downloads and interactive downloads stay identical.
    async with async_playwright() as p:
        browser = await p.chromium.launch(channel="chrome")
        for lang, meta in LANGUAGES.items():
            filename = meta["html"]
            context = await browser.new_context(accept_downloads=True)
            page = await context.new_page()
            await page.add_init_script(
                f"localStorage.setItem('company-profile-language-selection', {json.dumps(lang)});"
            )
            await page.goto((SITE_DIR / filename).as_uri(), wait_until="networkidle")
            async with page.expect_download(timeout=60000) as download_info:
                await page.locator("#download-word").click()
            download = await download_info.value
            word_path = OUT / f"Company_Profile_{meta['file_suffix']}.docx"
            await download.save_as(word_path)
            shutil.copy2(word_path, SITE_DIR / word_path.name)
            print(f"[DOCX] {word_path.name} ({word_path.stat().st_size / 1024:.0f} KB)", flush=True)
            await context.close()
        await browser.close()

    # 4. Optional Preview PNGs
    if preview:
        import fitz  # PyMuPDF

        PREVIEW.mkdir(parents=True, exist_ok=True)
        for pdf_path, _ in results:
            doc = fitz.open(pdf_path)
            for i, pg in enumerate(doc):
                pix = pg.get_pixmap(dpi=110)
                pix.save(PREVIEW / f"{pdf_path.stem}_p{i + 1}.png")


if __name__ == "__main__":
    asyncio.run(build(preview="--preview" in sys.argv))
