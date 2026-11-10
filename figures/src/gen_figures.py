#!/usr/bin/env python3
"""Generate the 2026 development-report figures as diagram-design HTML sources.

Profile: cubrid-book (viewBox width 680, sans + mono, one red accent).
Export each HTML with the diagram-design skill's scripts/export_svg.py into
api-reference/.gitbook/assets/. Edit this script and re-export; never hand-edit the SVG.
"""
import os
import unicodedata

HERE = os.path.dirname(os.path.abspath(__file__))

SANS = "Pretendard, 'Noto Sans KR', 'Noto Sans CJK KR', sans-serif"
MONO = "'Geist Mono', 'Noto Sans Mono CJK KR', monospace"
PAPER = "#fbfaf7"
INK = "#3b4252"
MUTED = "#666666"
SOFT = "#7a7f89"
RULE = "#d8dee9"
ACCENT = "#c62828"
ACCENT_TINT = "rgba(198,40,40,0.08)"
NODE = "#ffffff"
W = 680


def width(s, size, mono=False):
    """Per-character width budget: wide chars 1em, others 0.60em sans / 0.62em mono."""
    w = 0.0
    for ch in s:
        if unicodedata.combining(ch):
            continue
        if unicodedata.east_asian_width(ch) in ("W", "F"):
            w += 1.0
        else:
            w += 0.62 if mono else 0.60
    return w * size


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def is_wide(s):
    return any(unicodedata.east_asian_width(c) in ("W", "F") for c in s)


def text(x, y, s, size=12, weight=400, fill=INK, mono=False, anchor="start", spacing=None):
    fam = MONO if mono else SANS
    ls = f' letter-spacing="{spacing}"' if spacing else ""
    return (f'<text x="{x}" y="{y}" fill="{fill}" font-size="{size}" font-weight="{weight}" '
            f'font-family="{fam}" text-anchor="{anchor}"{ls}>{esc(s)}</text>')


def label(cx, cy, s, fill=MUTED, anchor="middle"):
    """Arrow label on an opaque mask. cy is the text baseline. Latin -> 8px mono, Korean -> 12px sans."""
    if is_wide(s):
        size, mono, h, pad = 12, False, 16, 8
    else:
        size, mono, h, pad = 8, True, 12, 8
    w = width(s, size, mono) + pad
    w = int((w + 3) // 4 * 4)
    if anchor == "middle":
        x0 = cx - w / 2
    elif anchor == "start":
        x0 = cx - pad / 2
    else:
        x0 = cx - w + pad / 2
    y0 = cy - (12 if h == 16 else 9)
    out = f'<rect x="{x0:.0f}" y="{y0}" width="{w}" height="{h}" fill="{PAPER}"/>'
    out += text(cx, cy, s, size=size, mono=mono, fill=fill, anchor=anchor,
                spacing=None if size == 12 else "0.06em")
    return out


def box(x, y, w, h, name, sub=None, focal=False, rx=6):
    stroke = ACCENT if focal else INK
    fill = ACCENT_TINT if focal else NODE
    out = f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{PAPER}"/>'
    out += f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}" stroke="{stroke}" stroke-width="1"/>'
    cx = x + w / 2
    if sub:
        out += text(cx, y + h / 2 - 2, name, size=12, weight=600, anchor="middle")
        out += text(cx, y + h / 2 + 14, sub, size=8, mono=True, fill=MUTED, anchor="middle")
    else:
        out += text(cx, y + h / 2 + 4, name, size=12, weight=600, anchor="middle")
    return out


def oval(x, y, w, h, name, sub=None):
    return box(x, y, w, h, name, sub, rx=20)


def diamond(cx, cy, w, h, lines):
    pts = f"{cx},{cy - h / 2} {cx + w / 2},{cy} {cx},{cy + h / 2} {cx - w / 2},{cy}"
    out = f'<polygon points="{pts}" fill="{PAPER}"/>'
    out += f'<polygon points="{pts}" fill="{NODE}" stroke="{INK}" stroke-width="1"/>'
    n = len(lines)
    y0 = cy - (n - 1) * 8 + 4
    for i, ln in enumerate(lines):
        out += text(cx, y0 + i * 16, ln, size=12, weight=600, anchor="middle")
    return out


def line(x1, y1, x2, y2, accent=False, marker=True, dash=None):
    col = ACCENT if accent else MUTED
    mk = f' marker-end="url(#{"arrow-accent" if accent else "arrow"})"' if marker else ""
    da = f' stroke-dasharray="{dash}"' if dash else ""
    return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{col}" stroke-width="1.2"{da}{mk}/>'


def path(d, accent=False, marker=True):
    col = ACCENT if accent else MUTED
    mk = f' marker-end="url(#{"arrow-accent" if accent else "arrow"})"' if marker else ""
    return f'<path d="{d}" fill="none" stroke="{col}" stroke-width="1.2"{mk}/>'


DEFS = (f'<defs><marker id="arrow" markerWidth="8" markerHeight="6" refX="7" refY="3" orient="auto">'
        f'<polygon points="0 0, 8 3, 0 6" fill="{MUTED}"/></marker>'
        f'<marker id="arrow-ink" markerWidth="8" markerHeight="6" refX="7" refY="3" orient="auto">'
        f'<polygon points="0 0, 8 3, 0 6" fill="{INK}"/></marker>'
        f'<marker id="arrow-accent" markerWidth="8" markerHeight="6" refX="7" refY="3" orient="auto">'
        f'<polygon points="0 0, 8 3, 0 6" fill="{ACCENT}"/></marker></defs>')


def page(slug, eyebrow, title, desc, height, body):
    return f"""<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{slug}</title>
  <link href="https://fonts.googleapis.com/css2?family=Geist+Mono:wght@400;500;600&family=Noto+Sans+KR:wght@400;500;600;700&display=swap" rel="stylesheet">
  <style>
    *, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}
    body {{ font-family: {SANS}; background: {PAPER};
           color: {INK}; display: flex; justify-content: center; padding: 3rem 2rem; }}
    .frame {{ max-width: 720px; width: 100%; }}
    .eyebrow {{ font-family: {MONO}; font-size: 0.66rem;
               letter-spacing: 0.18em; text-transform: uppercase; color: {MUTED}; margin-bottom: 1rem; }}
    .diagram-container {{ width: 100%; overflow-x: auto; }}
    svg {{ width: 100%; min-width: {W}px; display: block; }}
  </style>
</head>
<body>
  <div class="frame">
    <p class="eyebrow">{esc(eyebrow)}</p>
    <div class="diagram-container">
<svg viewBox="0 0 {W} {height}" xmlns="http://www.w3.org/2000/svg" role="img" aria-labelledby="{slug}-title {slug}-desc">
<title id="{slug}-title">{esc(title)}</title>
<desc id="{slug}-desc">{esc(desc)}</desc>
{DEFS}
<rect width="100%" height="100%" fill="{PAPER}"/>
{text(16, 28, title, size=16, weight=700)}
{body}
</svg>
    </div>
  </div>
</body>
</html>
"""


# ---------------------------------------------------------------- figure 1
def fig_architecture():
    slug = "cubvec-2026-architecture"
    title = "디스크 기반 벡터 인덱스의 계층 구조"
    desc = ("SQL 인터페이스부터 옵티마이저와 실행기, 벡터 인덱스 관리, HNSW 알고리즘, 그래프 스토리지와 캐시, "
            "CUBRID 저장 엔진까지 여섯 계층으로 나눈 구조이며, 3차년도 작업의 중심인 그래프 스토리지 계층을 강조한다.")
    layers = [
        ("L1", "SQL 인터페이스", "VECTOR · distance fn · CREATE INDEX USING hnsw · COPY"),
        ("L2", "옵티마이저 · 실행기", "vector index scan plan · executor · visibility check"),
        ("L3", "벡터 인덱스 관리", "index type in catalog · build params · statdump stats"),
        ("L4", "HNSW 알고리즘", "search · insert · neighbor repair · int8 prefilter"),
        ("L5", "그래프 스토리지 · 캐시", "node records on slotted pages · vector / neighbor cache"),
        ("L6", "CUBRID 저장 엔진", "page buffer · log (REDO/UNDO) · MVCC · vacuum"),
    ]
    x0, x1, y0, h = 88, 656, 52, 52
    body = []
    # direction indicator (left margin)
    body.append(text(60, y0 + 8, "SQL", size=8, mono=True, fill=MUTED, anchor="middle", spacing="0.06em"))
    body.append(f'<line x1="60" y1="{y0 + 16}" x2="60" y2="{y0 + h * 6 - 16}" stroke="{MUTED}" stroke-width="1.2" marker-end="url(#arrow)"/>')
    body.append(text(60, y0 + h * 6 + 4, "PAGE", size=8, mono=True, fill=MUTED, anchor="middle", spacing="0.06em"))
    # stack
    body.append(f'<rect x="{x0}" y="{y0}" width="{x1 - x0}" height="{h * 6}" rx="6" fill="{NODE}" stroke="{INK}" stroke-width="1"/>')
    for i in range(1, 6):
        yy = y0 + i * h
        body.append(f'<line x1="{x0}" y1="{yy}" x2="{x1}" y2="{yy}" stroke="{RULE}" stroke-width="1"/>')
    focal = 4
    fy = y0 + focal * h
    body.append(f'<rect x="{x0}" y="{fy}" width="{x1 - x0}" height="{h}" fill="{ACCENT_TINT}" stroke="{ACCENT}" stroke-width="1.2"/>')
    for i, (tag, name, sub) in enumerate(layers):
        cy = y0 + i * h + h / 2
        body.append(text(104, cy + 3, tag, size=8, weight=500, mono=True, fill=ACCENT if i == focal else MUTED, spacing="0.18em"))
        body.append(text(136, cy + 4, name, size=12, weight=600))
        body.append(text(640, cy + 3, sub, size=8, mono=True, fill=SOFT, anchor="end"))
        assert 136 + width(name, 12) + 16 < 640 - width(sub, 8, True), (name, sub)
    ny = y0 + h * 6 + 32
    body.append(text(16, ny, "3차년도에는 L4–L5를 CUBRID 페이지 위로 옮기고, 그 위에서 L2의 검색 질의와 L6의 트랜잭션·복구 연동을 개발했다.",
                     size=12, weight=500, fill=MUTED))
    return slug, page(slug, "Layer stack · 2026 development report", title, desc, ny + 20, "\n".join(body))


# ---------------------------------------------------------------- figure 2
def fig_entry_lifecycle():
    slug = "cubvec-2026-entry-lifecycle"
    title = "벡터 인덱스 엔트리의 생명주기"
    desc = ("인덱스 엔트리는 삽입되면 유효 상태가 되고, DELETE나 UPDATE가 제거 MVCCID를 남기면 제거 대기 상태가 되며, "
            "그 버전을 보는 스냅샷이 사라지면 vacuum이 삭제됨 상태로 바꾼 뒤 이웃을 보수하고 공간을 회수한다. "
            "롤백은 제거 표시를 되돌리거나 삽입한 엔트리를 삭제됨으로 바꾼다.")
    bw, bh, cy = 128, 52, 172
    bx = [64, 272, 480]
    top, bot = cy - bh / 2, cy + bh / 2
    body = []
    # arrows first
    body.append(line(30, cy, bx[0], cy, marker=True))
    body.append(label(42, cy - 10, "INSERT"))
    # DELETE/UPDATE (upper lane) and ROLLBACK (lower lane) between box 0 and 1
    body.append(line(bx[0] + bw, cy - 9, bx[1], cy - 9))
    body.append(label((bx[0] + bw + bx[1]) / 2, cy - 18, "DELETE·UPDATE"))
    body.append(line(bx[1], cy + 9, bx[0] + bw, cy + 9))
    body.append(label((bx[0] + bw + bx[1]) / 2, cy + 30, "ROLLBACK"))
    # VACUUM (focal) between box 1 and 2
    body.append(line(bx[1] + bw, cy, bx[2], cy, accent=True))
    body.append(label((bx[1] + bw + bx[2]) / 2, cy - 10, "VACUUM", fill=ACCENT))
    # INSERT ROLLBACK: above, from box 0 top to box 2 top
    ax, ex, yy = bx[0] + bw / 2, bx[2] + bw / 2, top - 40
    body.append(path(f"M {ax},{top} V {yy + 8} Q {ax},{yy} {ax + 8},{yy} H {ex - 8} Q {ex},{yy} {ex},{yy + 8} V {top}"))
    body.append(label((ax + ex) / 2, yy - 8, "INSERT ROLLBACK"))
    # RECLAIM: box 2 bottom down to end state
    exx, eyy = bx[2] + bw / 2, bot + 64
    body.append(line(exx, bot, exx, eyy - 10))
    body.append(label(exx + 12, (bot + eyy) / 2 + 4, "REPAIR · RECLAIM", anchor="start"))
    # nodes
    body.append(f'<circle cx="24" cy="{cy}" r="6" fill="{INK}"/>')
    body.append(box(bx[0], top, bw, bh, "유효", "ins = T1, del = -"))
    body.append(box(bx[1], top, bw, bh, "제거 대기", "del = T2 stamped"))
    body.append(box(bx[2], top, bw, bh, "삭제됨", "tombstone", focal=True))
    body.append(f'<circle cx="{exx}" cy="{eyy}" r="8" fill="none" stroke="{INK}" stroke-width="1.2"/>')
    body.append(f'<circle cx="{exx}" cy="{eyy}" r="5" fill="{INK}"/>')
    body.append(text(exx - 16, eyy + 4, "회수 (선택)", size=12, weight=500, fill=MUTED, anchor="end"))
    ny = eyy + 40
    notes = [
        "검색은 스냅샷이 삽입(ins)은 보고 제거(del)는 보지 않는 엔트리만 결과로 돌려준다.",
        "각 전이는 전용 로그 레코드로 남아, 크래시 뒤 REDO와 UNDO로 같은 상태를 다시 만든다.",
    ]
    for i, n in enumerate(notes):
        body.append(text(16, ny + i * 20, n, size=12, weight=500, fill=MUTED))
        assert 16 + width(n, 12) < W - 16, n
    return slug, page(slug, "State machine · 2026 development report", title, desc, ny + 20 * len(notes), "\n".join(body))


# ---------------------------------------------------------------- figure 3
def fig_search_flow():
    slug = "cubvec-2026-search-flow"
    title = "벡터 검색 질의의 실행 흐름"
    desc = ("벡터 검색 질의는 정렬 단계 없는 벡터 인덱스 스캔 플랜으로 실행되고, 인덱스가 가까운 후보 k개를 넘기면 "
            "실행기가 그 가운데 보이지 않거나 삭제 표시되었거나 조건에 맞지 않는 행을 빼고 돌려주므로, 결과가 k건보다 적을 수 있다.")
    cx, bw, bh = 200, 208, 48
    lx = cx - bw / 2
    ys = [52, 128, 204, 280, 356]
    body = []
    for a, b in zip(ys, ys[1:]):
        body.append(line(cx, a + bh, cx, b))
    # example panel, tied to the filtering step
    fy = ys[3] + bh / 2
    px, pw, ph = 368, 288, 92
    py = fy - ph / 2
    body.append(line(lx + bw, fy, px, fy, marker=False, dash="4,3"))
    body.append(f'<rect x="{px}" y="{py}" width="{pw}" height="{ph}" rx="6" fill="#f4f6f8" stroke="{RULE}" stroke-width="1"/>')
    body.append(text(px + 16, py + 24, "예: LIMIT 10", size=12, weight=600))
    lines = ["그래프 탐색 → 가까운 후보 10건",
             "삭제 표시 1건, 조건 불일치 2건 제외",
             "결과 7건 (k = 10보다 적음)"]
    for i, ln in enumerate(lines):
        body.append(text(px + 16, py + 46 + i * 18, ln, size=12, weight=500, fill=ACCENT if i == 2 else MUTED))
        assert width(ln, 12) < pw - 32, ln
    # nodes
    body.append(oval(lx, ys[0], bw, bh, "벡터 검색 질의", "WHERE p ORDER BY dist LIMIT k"))
    body.append(box(lx, ys[1], bw, bh, "실행 계획", "vector index scan, no sort step"))
    body.append(box(lx, ys[2], bw, bh, "그래프 탐색", "hnsw_ef_search -> nearest k"))
    body.append(box(lx, ys[3], bw, bh, "가시성 · 조건 적용", "drop invisible / tombstoned / not p", focal=True))
    body.append(oval(lx, ys[4], bw, bh, "결과 반환", "nearest first, at most k rows"))
    ny = ys[4] + bh + 36
    notes = [
        "인덱스는 가까운 후보 k개를 넘기고, 실행기는 그 가운데 조건과 가시성에 맞지 않는 행을 뺀다.",
        "빠진 행은 다시 채우지 않으므로, 조건이 많이 거를수록 결과가 k건보다 적어진다.",
    ]
    for i, n in enumerate(notes):
        body.append(text(16, ny + i * 20, n, size=12, weight=500, fill=MUTED))
        assert 16 + width(n, 12) < W - 16, (n, width(n, 12))
    return slug, page(slug, "Process · 2026 development report", title, desc, ny + 20 * len(notes), "\n".join(body))


if __name__ == "__main__":
    for fn in (fig_architecture, fig_entry_lifecycle, fig_search_flow):
        slug, html = fn()
        with open(os.path.join(HERE, slug + ".html"), "w", encoding="utf-8") as f:
            f.write(html)
        print("wrote", slug + ".html")
