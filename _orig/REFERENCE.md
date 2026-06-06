# Getty "Tracing Art" — 재구현 레퍼런스 (원본 분석)

원본: https://www.getty.edu/tracingart/  · Nuxt3 + GSAP/ScrollTrigger + Lenis + **WebGL2**

## 전체 구조
- 총 스크롤 높이: **87151px** (데스크탑 1920×963 기준)
- 레이어 (모두 `.scrollContent` 안, fixed):
  - `.pageLoader` — "Getty" 로더 (페이드)
  - `.nav` — 우상단 햄버거 + 챕터 메뉴(블러 패널) + 좌상단 Getty 워드마크
  - `.gl` — **WebGL2 캔버스** (3840×1926 retina). 떠다니는 그림/페인팅·전환·data-viz 전부 여기서 렌더.
  - `.viewportEl` — 우측 커스텀 스크롤바
- `.main > .page > .fillFixed` — 텍스트 오버레이(고정 100vh), 씬마다 내용 교체
- 섹션 앵커 y좌표: **section-1 = 0**, **section-2 = 17912**, **section-3 = 49595**, endPad = 86189

## 챕터(스크롤 구간)
| 구간(px) | 내용 |
|---|---|
| 0 – ~16900 | **Intro/Hero** + Chapter 1 도입. "Tracing Art" → "Millions of Resources, Spanning Five Centuries" → "Here's how the Getty Provenance Index is transforming research on the social life of art." + Scroll down. 떠다니는 페인팅들(intro 11점) parallax. |
| ~16900 – 49595 | **Ch1 Tracing a Painting** (Willem Kalf, *Still Life with a Chinese Porcelain Jar*) — 타임라인 1669·1700·1864·1936·1940·1944, ledger(장부) 줌, zoom-img. 이어서 **Ch2 Artists as Collectors** 도입. |
| 49595 – 86189 | **Ch3 Collectors, Museums & the Market** — data-viz 네트워크(스프라이트시트 102 인물), 수집가/딜러/미술관 리스트. |
| 86189 – 87151 | **Outro** — About the Getty Provenance Index + footer "© J. Paul Getty Trust". |

(주의: Ch1/Ch2 경계는 텍스트 흐름상 섞여 있음. 정확 매핑은 빌드 중 스크린샷 대조로 확정.)

## ScrollTrigger (15개, 전부 scrub, GSAP pin 미사용 → sticky/fixed + scrub 타임라인)
start→end (px): 0→18297 · 17430→20319 · 23208→27060 · 29468→33320 · 39579→49209 ·
32838→40542 · 16939→50172 · 48632→55613 · 49113→54650 · 55373→59465 · 55854→58502 ·
61632→64040 · 47909→86429 · 83203→86092 · (+1). 씬들이 크게 겹침(크로스페이드).

## 타이포 (style 원본)
- **Bradford** (serif, 본문/헤드라인): textH1 15rem(모바일 6.4rem), textH2 6rem, textBodyL 5rem, textBodyM 4rem. letter-spacing -0.02~-0.03em, line-height 1~1.2. html font-size:10px (1rem=10px).
- **Graphik** (UI/소형 라벨, 403로 못 받음 → 폴백: Inter/Helvetica Neue).
- font-display:swap. Bradford woff2 + LightItalic otf 확보.

## 에셋 (public/ 에 미러)
- `images/getty/intro/` (11) — 히어로 떠다니는 그림
- `images/getty/still-life/` (60) — Ch1/2 배경 페인팅 군집
- `images/getty/world-of-gpi/` (33) — Ch2/3 네트워크 페인팅
- `images/getty/artist-to-artist/` (4) — 초상화
- `images/section-1/` ledger, zoom-img (@sm/@lg)
- `images/section-2/` transaction-1, transaction-2-img-1/2, zoom-img, zoom-credit, husband-and-wife/{husband,wife}, world-of-gpi-title.svg
- `images/getty-spritesheets/generated/data-viz/` metadata.json 확보, **spritesheet_0/1.png 403 (쿨다운 후 재시도 필요)**
- 모든 페인팅 @sm + @lg 둘 다 확보(반응형).

## 재구현 전략 (DOM/CSS/GSAP)
- WebGL → 위치고정 `<img>` + transform/opacity scrub 로 동일 비주얼 재현.
- Ch3 네트워크 → Canvas2D (스프라이트시트) 또는 div 노드 + 라인.
- Lenis smooth + ScrollTrigger scrub. 1rem=10px 기준 그대로.
- prefers-reduced-motion 분기.
