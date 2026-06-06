# The Creative Independent — 홈페이지(Explore) 정확 미러

원본: https://thecreativeindependent.com/

## 구성
- `raw/index.html` — 원본에서 받은 홈페이지 HTML (가공 전 원본 보관용)
- `site/` — 실제 서빙되는 정확 미러
  - `index.html` — 홈페이지. 에셋 링크(`/css`, `/images`)는 로컬, 그 외 내부 네비게이션 링크(아티클/카테고리/People 등 2390개)는 원본 도메인 절대경로로 연결해 클릭 시 실제 글로 이어짐
  - `css/` — default / new_explore / main / search (원본 그대로)
  - `javascript/` — filters.js, search.js (원본 그대로)
  - `images/` — 나선 로고는 인라인 SVG, bird / seedling / snail / favicon 등

## 기술 스택 (원본과 동일)
- 서버 렌더링 정적 HTML (프레임워크 없음)
- 인-페이지 필터링: `filters.js` (Themes/Disciplines/Languages → `.box` 카드 show/hide)
- 검색: Algolia + instantsearch (`tci_v2` 인덱스, 공개 search 키) + dayjs — CDN, 인터넷 필요
- 모션: 카드 hover `transform scale` 150ms, 상단 bird 스프라이트 애니메이션
- 폰트: 시스템 폰트(system-ui / Courier) — 별도 웹폰트 없음

## 실행
```bash
cd _tci
python3 serve.py     # no-cache 서버 (새로고침해도 항상 최신; 브랜딩 유지)
# http://localhost:5200/
```
(단순 `python3 -m http.server`는 브라우저가 옛 HTML을 캐시해 변경이 안 보일 수 있음 → serve.py 사용)
검색·Algolia·Plausible은 CDN/외부 API라 인터넷 연결 시 동작.

## 범위 메모
- **모든 메뉴 페이지를 로컬 캡처 + TIPS 브랜딩** (home 포함 16개). nav 링크 로컬 연결 → 페이지 이동해도 로고·메뉴·이미지 유지.
- 개별 아티클/카드는 실제 도메인 링크. Random·Samples(quotes)·People·Subscribe는 동적/외부라 실제 도메인 링크.
- 재생성: `python3 brandify.py && python3 about.py` (원본 raw: `raw/pages/`).
- 브랜딩 변경점: 로고(TiPS), 워드마크/슬로건, nav 라벨(인쇄소용), About 페이지 컨셉 재구성, `css/tips.css`.
