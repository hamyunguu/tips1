#!/usr/bin/env python3
"""TCI 미러 → TIPS 브랜드 적용 + nav 링크 로컬화.
모든 메뉴 페이지에서 로고/메뉴/슬로건/이미지가 유지되도록 동일 변환을 적용한다.
- 카드/아티클 등 내부 링크는 실제 도메인(절대경로)으로 (미캡처 페이지)
- nav 메뉴 링크는 로컬 캡처 페이지로 (브랜딩 유지)
- 에셋(/css /js /images /fonts)은 로컬 유지
"""
import re, os

BASE = "https://thecreativeindependent.com"
ROOT = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.join(ROOT, "site")
PAGES = os.path.join(ROOT, "raw", "pages")
ASSET = re.compile(r"^/(css|javascript|js|images|fonts)/")

# (로컬경로, 라벨) — 메인 탭
MAIN = [
    ("/", "Everything"),
    ("/interviews/", "Bookbinding"),
    ("/essays/", "Printing"),
    ("/guides/", "Paper"),
    ("/focuses/", "Finishing"),
    ("/approaches/", "Editions"),
    ("/tips/", "Workshops"),
    ("/wisdom/", "Journal"),
    ("/zines/", "Zines"),
]
RANDOM = (BASE + "/random", "Random")  # 동적 리다이렉트 → 실제 사이트
DROP = [
    ("/questions/", "Risograph"),
    ("/series/", "Letterpress"),
    ("/notes/", "Offset"),
    ("/transmissions/", "Foil &amp; Emboss"),
    ("/weekends/", "Die-cutting"),
    (BASE + "/quotes", "Samples"),  # 풀스크린 영상 경험 → 실제 사이트
    ("/snails/", "Archive"),
    ("/about/", "About"),
]

LOGO_RE = re.compile(
    r'(<a aria-label="Link to home page" id="logo" href=")[^"]*(">)\s*<svg.*?</svg>\s*(</a>)',
    re.S,
)
LOGO_MARK = (
    '\\1/\\2\n'
    '      <span class="tips-logo" aria-label="TIPS" role="img">\n'
    '        <span class="l-t">T</span>\n'
    '        <span class="l-row"><span class="l-i">i</span><span class="l-ps">PS</span></span>\n'
    '      </span>\n    \\3'
)
WORDMARK = "  <span>The Creative Independent</span>"
WORDMARK_NEW = (
    '  <span id="tips-wordmark">TIPS</span>\n'
    '  <p id="tips-tagline"><span class="en">Experiment for Many Ways to Bind Paper</span>'
    '<span class="kr">종이를 엮는 수많은 방법을 실험하다</span></p>'
)
NAV_RE = re.compile(r'<nav id="main-navigation">.*?</nav>', re.S)
EXPLORE_RE = re.compile(r'<a href="[^"]*" >Explore</a>')


def build_nav(active):
    L = ['  <nav id="main-navigation">']
    for href, label in MAIN:
        cls = ' class="active"' if href == active else ""
        L.append(f'    <a href="{href}"{cls}>{label}</a>')
    L.append(f'    <a href="{RANDOM[0]}">{RANDOM[1]}</a>')
    L.append('    <details id="main-navigation__more-dropdown" >')
    L.append('      <summary >...</summary>')
    L.append('      <ul id="main-navigation__more-dropdown__list">')
    for href, label in DROP:
        cls = ' class="active"' if href == active else ""
        L.append(f'        <li><a href="{href}"{cls}>{label}</a></li>')
    L.append('      </ul>')
    L.append('    </details>')
    L.append('    <button id="search-button" class="rounded">Search</button>')
    L.append('  </nav>')
    return "\n".join(L)


def rewrite_links(h):
    def repl(m):
        q, url = m.group(1), m.group(2)
        if ASSET.match(url):
            return m.group(0)
        return f'{q}="{BASE}{url}"'
    return re.sub(r'(href|action)="(/(?!/)[^"]*)"', repl, h)


def add_tips_css(h):
    if "css/tips.css" in h:
        return h
    anchor = '<link rel="stylesheet" href="/css/search.css?c235afc1beaade88875390452a6a8c08">'
    link = '<link rel="stylesheet" href="/css/tips.css?v=3">'
    if anchor in h:
        return h.replace(anchor, anchor + "\n" + link, 1)
    return h.replace("</head>", link + "</head>", 1)


def brandify(h, active, applied):
    h = rewrite_links(h)
    h = add_tips_css(h)
    h2 = LOGO_RE.sub(LOGO_MARK, h, count=1); applied['logo'] = h2 != h; h = h2
    if WORDMARK in h:
        h = h.replace(WORDMARK, WORDMARK_NEW, 1); applied['wordmark'] = True
    else:
        applied['wordmark'] = False
    h2 = NAV_RE.sub(lambda m: build_nav(active), h, count=1); applied['nav'] = h2 != h; h = h2
    h2 = EXPLORE_RE.sub('<a href="/" >Explore</a>', h, count=1); applied['explore'] = h2 != h; h = h2
    return h


# tci real path -> (local dir under site/, active local path)
JOBS = [
    ("interviews", "interviews", "/interviews/"),
    ("essays", "essays", "/essays/"),
    ("guides", "guides", "/guides/"),
    ("focuses", "focuses", "/focuses/"),
    ("approaches", "approaches", "/approaches/"),
    ("tips", "tips", "/tips/"),
    ("wisdom", "wisdom", "/wisdom/"),
    ("zines", "zines", "/zines/"),
    ("questions", "questions", "/questions/"),
    ("series", "series", "/series/"),
    ("notes", "notes", "/notes/"),
    ("transmissions", "transmissions", "/transmissions/"),
    ("weekends", "weekends", "/weekends/"),
    ("snails", "snails", "/snails/"),
    # quotes → 실제 도메인으로 링크(미러 X). about → 별도 스크립트(다른 템플릿)
]

if __name__ == "__main__":
    for src, outdir, active in JOBS:
        raw = open(os.path.join(PAGES, src + ".html"), encoding="utf-8", errors="replace").read()
        applied = {}
        out = brandify(raw, active, applied)
        d = os.path.join(SITE, outdir)
        os.makedirs(d, exist_ok=True)
        open(os.path.join(d, "index.html"), "w", encoding="utf-8").write(out)
        print(f"{outdir:14s} {applied}")
    print("DONE sub-pages")

    # --- home: nav 링크 로컬화 + 로고 href 로컬 + Explore 로컬 (기존 브랜딩/About카드 유지) ---
    hp = os.path.join(SITE, "index.html")
    h = open(hp, encoding="utf-8").read()
    h = NAV_RE.sub(lambda m: build_nav("/"), h, count=1)
    h = h.replace('id="logo" href="https://thecreativeindependent.com/"', 'id="logo" href="/"', 1)
    h = EXPLORE_RE.sub('<a href="/" >Explore</a>', h, count=1)
    open(hp, "w", encoding="utf-8").write(h)
    print("home patched: nav local, logo local, explore local")
