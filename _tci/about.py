#!/usr/bin/env python3
"""about 페이지(다른 템플릿: page.css 사이드바)를 TIPS 브랜드 About로 재구성."""
import os, re
import brandify as B  # build_nav, rewrite_links, add_tips_css, LOGO_MARK 등 재사용

ROOT = os.path.dirname(os.path.abspath(__file__))
raw = open(os.path.join(ROOT, "raw", "pages", "about.html"), encoding="utf-8", errors="replace").read()
h = raw

# 1) 내부 링크 → 실제 도메인, 에셋 유지
h = B.rewrite_links(h)
# 2) tips.css + main.css(메뉴 스타일) 링크 추가
h = h.replace(
    '<link rel="stylesheet" href="/css/page.css?7fa14e3f50602362d5901a986e47724a">',
    '<link rel="stylesheet" href="/css/page.css?7fa14e3f50602362d5901a986e47724a">\n'
    '<link rel="stylesheet" href="/css/main.css?210dd455a2df362b4d52d271a00e5a27">\n'
    '<link rel="stylesheet" href="/css/tips.css?v=3">', 1)

# 3) spiral-stamp 로고 → TiPS 마크 (id=logo 로 교체해 main/tips.css 적용)
h = h.replace(
    '<a href="https://thecreativeindependent.com/" id="spiral-stamp"></a>',
    '<a href="/" id="logo" aria-label="TIPS">\n'
    '      <span class="tips-logo" role="img">\n'
    '        <span class="l-t">T</span>\n'
    '        <span class="l-row"><span class="l-i">i</span><span class="l-ps">PS</span></span>\n'
    '      </span>\n    </a>', 1)
# (혹시 절대경로 변환 전 형태였다면)
h = h.replace('<a href="/" id="spiral-stamp"></a>',
    '<a href="/" id="logo" aria-label="TIPS">\n'
    '      <span class="tips-logo" role="img">\n'
    '        <span class="l-t">T</span>\n'
    '        <span class="l-row"><span class="l-i">i</span><span class="l-ps">PS</span></span>\n'
    '      </span>\n    </a>', 1)

# Explore 로컬화
h = B.EXPLORE_RE.sub('<a href="/" >Explore</a>', h, 1)

# 4) 헤더 다음에 워드마크+슬로건 + 우리 메뉴 주입
inject = (
    '\n  <span id="tips-wordmark">TIPS</span>\n'
    '  <p id="tips-tagline"><span class="en">Experiment for Many Ways to Bind Paper</span>'
    '<span class="kr">종이를 엮는 수많은 방법을 실험하다</span></p>\n'
    + B.build_nav("/about/") + "\n"
)
h = h.replace("</header>", "</header>" + inject, 1)

# 5) 사이드바 nav 교체
sidebar_new = '''<nav>
<h1>About</h1>
<ul style="margin-top:1rem; display:flex; flex-direction:column; row-gap: 0.5rem;">
<li><a style="background-color:#f0f0f0; padding:2px 6px; text-decoration:none;" href="#what-is-tips">What is TIPS?</a></li>
<li><a style="background-color:#f0f0f0; padding:2px 6px; text-decoration:none;" href="#approach">Approach</a></li>
<li><a style="background-color:#f0f0f0; padding:2px 6px; text-decoration:none;" href="#methods">Methods</a></li>
<li><a style="background-color:#f0f0f0; padding:2px 6px; text-decoration:none;" href="#contact">Contact</a></li>
</ul>
</nav>'''
h = re.sub(r'<nav>\s*<h1>About</h1>.*?</nav>', lambda m: sidebar_new, h, count=1, flags=re.S)

# 6) 본문 main 교체 — TIPS 소개/방식/메뉴 연계
main_new = '''<main>
      <h2 id="what-is-tips">What is TIPS?</h2>
<p><em>Experiment for Many Ways to Bind Paper · 종이를 엮는 수많은 방법을 실험하다</em></p>
<p>책을 만들 때, 우리는 늘 많은 선택 앞에 놓입니다. 어떤 종이에 인쇄할지, 어떤 방식으로 출력할지, 어떻게 엮어낼지. 그리고 우리는 늘 같은 선택 앞에서 멈춰 섭니다.</p>
<p>TIPS는 반복되는 선택에서 벗어나려는 시도입니다. 다양한 방법을 실험하며, 종이 속 단어와 맥락을 제본이라는 매개를 통해 전달합니다.</p>

<h2 id="approach">Approach</h2>
<p>We treat binding as a medium, not a final step. Each project is an experiment in how paper can hold words, images, and context together—through structure, sequence, and surface.</p>

<h2 id="methods">Methods</h2>
<p>우리가 다루는 작업들:</p>
<ul style="margin-top:1rem; display:flex; flex-direction:column; row-gap: 0.5rem;">
<li><a style="background-color:#f0f0f0; padding:2px 6px; text-decoration:none;" href="/interviews/">Bookbinding — 제본</a></li>
<li><a style="background-color:#f0f0f0; padding:2px 6px; text-decoration:none;" href="/essays/">Printing — 인쇄</a></li>
<li><a style="background-color:#f0f0f0; padding:2px 6px; text-decoration:none;" href="/guides/">Paper — 종이</a></li>
<li><a style="background-color:#f0f0f0; padding:2px 6px; text-decoration:none;" href="/focuses/">Finishing — 후가공</a></li>
<li><a style="background-color:#f0f0f0; padding:2px 6px; text-decoration:none;" href="/approaches/">Editions — 에디션</a></li>
<li><a style="background-color:#f0f0f0; padding:2px 6px; text-decoration:none;" href="/tips/">Workshops — 워크숍</a></li>
</ul>

<h2 id="contact">Contact</h2>
<p>Studio inquiries &amp; collaborations: <a href="mailto:hello@tips.studio">hello@tips.studio</a></p>
    </main>'''
h = re.sub(r'<main>.*?</main>', lambda m: main_new, h, count=1, flags=re.S)

out = os.path.join(ROOT, "site", "about")
os.makedirs(out, exist_ok=True)
open(os.path.join(out, "index.html"), "w", encoding="utf-8").write(h)
print("about page rebuilt:", "logo" if "tips-logo" in h else "NO-logo",
      "| nav" if 'id="main-navigation"' in h else "| NO-nav",
      "| main" if "what-is-tips" in h else "| NO-main")
