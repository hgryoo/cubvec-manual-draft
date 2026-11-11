#!/usr/bin/env python3
"""Per-section figures for the 2026 development report (cubrid-book profile, width 680).

Reuses the primitives in gen_figures.py. Export each HTML with the diagram-design skill's
scripts/export_svg.py into api-reference/.gitbook/assets/; never hand-edit the SVG.
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from gen_figures import (W, PAPER, INK, MUTED, SOFT, RULE, ACCENT, ACCENT_TINT, NODE,  # noqa: E402
                         width, text, label, line, path, page)

GOOD, GOOD_FILL = "#2e7d32", "#e6f4ea"
WAIT, WAIT_TEXT, WAIT_FILL = "#b8860b", "#8a6200", "#fff6e5"
DEAD_FILL = "#f4f6f8"
KIND = {"plain": (INK, NODE), "focal": (ACCENT, ACCENT_TINT), "cost": (ACCENT, ACCENT_TINT),
        "good": (GOOD, GOOD_FILL), "wait": (WAIT, WAIT_FILL), "dead": (SOFT, DEAD_FILL)}


def wide(s):
    return width(s, 1) != width(s, 1, True) or any(ord(c) > 0x1100 for c in s)


def box(x, y, w, h, name, sub=None, kind="plain", rx=6, dash=False):
    stroke, fill = KIND[kind]
    assert width(name, 12) <= w - 12, (name, w)
    if sub:
        assert not any(ord(c) > 0x1100 for c in sub), sub
        assert width(sub, 8, True) <= w - 12, (sub, w)
    da = ' stroke-dasharray="4,3"' if dash else ""
    out = f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{PAPER}"/>'
    out += f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}" stroke="{stroke}" stroke-width="1"{da}/>'
    cx = x + w / 2
    tcol = MUTED if kind == "dead" else INK
    if sub:
        out += text(cx, y + h / 2 - 2, name, size=12, weight=600, anchor="middle", fill=tcol)
        out += text(cx, y + h / 2 + 13, sub, size=8, mono=True, fill=MUTED, anchor="middle")
    else:
        out += text(cx, y + h / 2 + 4, name, size=12, weight=600, anchor="middle", fill=tcol)
    return out


def oval(x, y, w, h, name, sub=None, kind="plain"):
    return box(x, y, w, h, name, sub, kind, rx=20)


def diamond(cx, cy, w, h, lines):
    pts = f"{cx},{cy - h / 2} {cx + w / 2},{cy} {cx},{cy + h / 2} {cx - w / 2},{cy}"
    out = f'<polygon points="{pts}" fill="{PAPER}"/><polygon points="{pts}" fill="{NODE}" stroke="{INK}" stroke-width="1"/>'
    y0 = cy - (len(lines) - 1) * 8 + 4
    for i, ln in enumerate(lines):
        assert width(ln, 12) <= w * 0.62, (ln, w)
        out += text(cx, y0 + i * 16, ln, size=12, weight=600, anchor="middle")
    return out


def zone(x, y, w, h, title):
    out = f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="8" fill="none" stroke="{RULE}" stroke-width="1.2" stroke-dasharray="4,3"/>'
    if title:
        out += text(x + 12, y + 20, title, size=12, weight=600, fill=MUTED)
    return out


def chip(x, y, w, h, s, kind="plain", mono=False):
    stroke, fill = KIND[kind]
    size = 8 if mono else 12
    assert width(s, size, mono) <= w - 8, (s, w)
    tcol = {"wait": WAIT_TEXT, "dead": MUTED}.get(kind, INK)
    out = f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="4" fill="{fill}" stroke="{stroke}" stroke-width="0.8"/>'
    out += text(x + w / 2, y + h / 2 + (3 if mono else 4), s, size=size, mono=mono, fill=tcol, anchor="middle",
                weight=500 if not mono else 400)
    return out


def opath(pts, accent=False, marker=True, dash=None, r=8):
    """Orthogonal path through pts with rounded corners."""
    d = f"M {pts[0][0]},{pts[0][1]}"
    for i in range(1, len(pts) - 1):
        (x0, y0), (x1, y1), (x2, y2) = pts[i - 1], pts[i], pts[i + 1]
        dx0 = (x1 > x0) - (x1 < x0)
        dy0 = (y1 > y0) - (y1 < y0)
        dx1 = (x2 > x1) - (x2 < x1)
        dy1 = (y2 > y1) - (y2 < y1)
        d += f" L {x1 - dx0 * r},{y1 - dy0 * r} Q {x1},{y1} {x1 + dx1 * r},{y1 + dy1 * r}"
    d += f" L {pts[-1][0]},{pts[-1][1]}"
    col = ACCENT if accent else MUTED
    mk = f' marker-end="url(#{"arrow-accent" if accent else "arrow"})"' if marker else ""
    da = f' stroke-dasharray="{dash}"' if dash else ""
    return f'<path d="{d}" fill="none" stroke="{col}" stroke-width="1.2"{da}{mk}/>'


def notes(y, lines):
    out = []
    for i, n in enumerate(lines):
        assert 16 + width(n, 12) < W - 16, (n, width(n, 12))
        out.append(text(16, y + i * 20, n, size=12, weight=500, fill=MUTED))
    return "\n".join(out), y + 20 * len(lines)


def lane(y, title, sub=None):
    out = text(16, y + (0 if sub else 4), title, size=12, weight=600)
    if sub:
        out += text(16, y + 18, sub, size=12, weight=500, fill=MUTED)
    return out


def node(cx, cy, kind="plain", label_=None, r=7, dash=False):
    stroke, fill = KIND[kind]
    da = ' stroke-dasharray="3,2"' if dash else ""
    out = f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{fill}" stroke="{stroke}" stroke-width="1"{da}/>'
    if label_:
        out += text(cx, cy + 3, label_, size=8, mono=True, fill=stroke if kind != "plain" else INK, anchor="middle")
    return out


def fig(slug, eyebrow, title, desc, height, body):
    return slug, page(slug, eyebrow, title, desc, height, "\n".join(body))


EB = " · 2026 development report"

# =============================================================== disk-vector-index




def d2_layers():
    b = []
    b.append(line(340, 100, 340, 132))
    b.append(line(208, 188, 208, 228))
    b.append(line(472, 188, 472, 228))
    b.append(line(472, 276, 472, 316))
    b.append(box(200, 52, 280, 48, "HNSW 알고리즘", "search · insert · neighbor repair"))
    b.append(f'<rect x="96" y="132" width="488" height="56" rx="6" fill="#f4f6f8" stroke="{RULE}" stroke-width="1"/>')
    b.append(text(112, 165, "스토리지 인터페이스", size=12, weight=600))
    x = 248
    for s, w in (("get_node(slot)", 88), ("get_vector(slot)", 96), ("add_node(key, vector)", 120)):
        b.append(chip(x, 148, w, 24, s, mono=True))
        x += w + 8
    b.append(box(96, 228, 224, 48, "메모리 스토리지", "used to check the porting"))
    b.append(box(360, 228, 224, 48, "페이지 스토리지", "slotted pages", kind="focal"))
    b.append(box(360, 316, 224, 40, "CUBRID 페이지 버퍼 · 로그"))
    t, y = notes(392, ["알고리즘은 슬롯 번호로만 노드를 가리키고, 노드가 메모리에 있는지 페이지에 있는지 모른다.",
                       "같은 알고리즘에 두 스토리지를 붙여, 메모리 쪽 결과로 페이지 쪽 포팅을 확인했다."])
    b.append(t)
    return fig("cubvec-2026-d2-layers", "Architecture" + EB, "알고리즘 계층과 스토리지 계층",
               "HNSW 알고리즘은 스토리지 인터페이스로만 노드와 벡터를 요청하고, 그 아래에 메모리 스토리지와 CUBRID 페이지 스토리지가 붙는다.",
               y, b)


def d3_layout():
    b = [zone(16, 48, 200, 212, "벡터 인덱스 파일")]
    b.append(line(200, 164, 280, 164, marker=False, dash="4,3"))
    b.append(line(380, 224, 380, 284, marker=False, dash="4,3"))
    b.append(box(32, 76, 168, 56, "루트 페이지", "params · height · entry"))
    b.append(box(32, 144, 168, 40, "노드 페이지"))
    b.append(box(32, 192, 168, 40, "노드 페이지"))
    b.append(text(116, 250, "…", size=12, fill=MUTED, anchor="middle"))
    b.append(f'<rect x="280" y="64" width="200" height="160" rx="4" fill="{NODE}" stroke="{INK}" stroke-width="1"/>')
    b.append(text(292, 84, "slotted page", size=8, mono=True, fill=MUTED, spacing="0.06em"))
    for i, yy in enumerate((96, 136, 176)):
        b.append(chip(296, yy, 168, 32, "노드 레코드", kind="focal" if i == 1 else "plain"))
    b.append(text(388, 258, "레코드 하나", size=12, weight=500, fill=MUTED))
    segs = [("키(OID)", 84, "plain"), ("레벨", 56, "plain"), ("상태·버전", 100, "plain"),
            ("벡터 (float32 × dim)", 168, "focal"), ("이웃 L0 (2M)", 120, "plain"), ("이웃 L1 (M)", 84, "plain"),
            ("…", 36, "plain")]
    x = 16
    for s, w, k in segs:
        b.append(chip(x, 284, w, 36, s, kind=k))
        x += w
    t, y = notes(352, ["루트 페이지에는 빌드 파라미터(차원, M, ef_construction, 메트릭), 그래프 높이, 진입점이 있다.",
                       "벡터를 노드 레코드 안에 두어 거리 계산에 페이지를 한 번만 고정한다. 레벨 0 이웃 칸은 2M개다."])
    b.append(t)
    return fig("cubvec-2026-d3-layout", "Layout" + EB, "파일, 페이지, 노드 레코드",
               "벡터 인덱스 파일은 루트 페이지와 노드 페이지로 이루어지고, 노드 페이지의 레코드 하나는 키, 레벨, 상태와 버전, 벡터, 레벨별 이웃 목록을 담는다.",
               y, b)











# =============================================================== transaction-recovery


def t1_snapshot():
    b = []
    t1, t2, t3, t4, x0, x1 = 160, 290, 400, 580, 112, 664
    for x, s in ((t1, "T1 삽입·커밋"), (t2, "T2 UPDATE"), (t3, "T2 커밋"), (t4, "vacuum")):
        b.append(f'<line x1="{x}" y1="64" x2="{x}" y2="268" stroke="{RULE}" stroke-width="1" stroke-dasharray="4,3"/>')
        b.append(text(x, 56, s, size=12, weight=600, anchor="middle"))
    b.append(line(x0, 276, x1, 276))
    b.append(text(x1, 296, "시간", size=12, weight=500, fill=MUTED, anchor="end"))
    b.append(lane(100, "엔트리 v1"))
    b.append(lane(140, "엔트리 v2"))
    b.append(lane(192, "스냅샷 S1"))
    b.append(lane(232, "스냅샷 S2"))
    b.append(chip(t1, 86, t2 - t1, 24, "ins = T1", mono=True))
    b.append(chip(t2, 86, t4 - t2, 24, "del = T2 (제거 대기)", kind="wait"))
    b.append(chip(t4, 86, 56, 24, "삭제됨", kind="dead"))
    b.append(chip(t2, 126, x1 - t2, 24, "ins = T2", kind="good", mono=True))
    b.append(chip(220, 180, 300, 20, "REPEATABLE READ", mono=True))
    b.append(text(528, 195, "v1을 본다", size=12, weight=600, fill=WAIT_TEXT))
    b.append(chip(440, 220, 160, 20, "new snapshot", mono=True))
    b.append(text(608, 235, "v2를 본다", size=12, weight=600, fill=GOOD))
    t, y = notes(320, ["UPDATE는 이전 엔트리에 제거 MVCCID를 남기고 새 엔트리를 넣는다. 각 스냅샷은 자기가 보는 버전으로",
                       "순위를 받는다. vacuum은 v1을 보는 스냅샷(S1)이 끝난 뒤에야 v1을 삭제 상태로 바꾼다."])
    b.append(t)
    return fig("cubvec-2026-t1-snapshot", "Timeline" + EB, "UPDATE 뒤의 두 버전과 두 스냅샷",
               "T2의 UPDATE 뒤 행은 v1과 v2 두 엔트리를 가지며, T2 커밋 전에 시작한 스냅샷 S1은 v1을, 커밋 뒤의 스냅샷 S2는 v2를 보고, vacuum은 S1이 끝난 뒤 v1을 정리한다.",
               y, b)


def t2_vacuum():
    b = []
    xs = [16, 184, 352, 520]
    w = 144
    for i in range(3):
        b.append(line(xs[i] + w, 78, xs[i + 1], 78))
    stages = [("① 제거 표시", "DML stamps del MVCCID"), ("② vacuum 판정", "no snapshot sees it"),
              ("③ 이웃 보수", "unlink the dead node"), ("④ 공간 회수", "optional, by parameter")]
    for x, (n, s) in zip(xs, stages):
        b.append(box(x, 52, w, 52, n, s))
    for k, x in enumerate(xs):
        cx = x + w / 2
        ax, bx, cy, top = cx - 44, cx + 44, 184, 144
        if k <= 1:
            b.append(f'<line x1="{ax}" y1="{cy}" x2="{bx}" y2="{cy}" stroke="{INK}" stroke-width="1"/>')
            b.append(f'<line x1="{cx}" y1="{top}" x2="{cx}" y2="{cy}" stroke="{INK}" stroke-width="1"/>')
        else:
            if k == 2:
                b.append(f'<line x1="{ax}" y1="{cy}" x2="{bx}" y2="{cy}" stroke="{SOFT}" stroke-width="1" stroke-dasharray="3,2"/>')
                b.append(f'<line x1="{cx}" y1="{top}" x2="{cx}" y2="{cy}" stroke="{SOFT}" stroke-width="1" stroke-dasharray="3,2"/>')
            b.append(opath([(ax, cy + 7), (ax, cy + 24), (bx, cy + 24), (bx, cy + 7)], marker=False, r=6)
                     .replace(MUTED, GOOD))
            b.append(opath([(cx + 7, top), (bx, top), (bx, cy - 7)], marker=False, r=6).replace(MUTED, GOOD))
        b.append(node(ax, cy))
        b.append(node(bx, cy))
        b.append(node(cx, top))
        if k == 0:
            b.append(node(cx, cy, "wait", "X"))
        elif k in (1, 2):
            b.append(node(cx, cy, "cost", "X"))
        else:
            b.append(node(cx, cy, "dead", None, dash=True))
    t, y = notes(244, ["제거 대기·삭제된 노드도 검색 경로로는 쓰이지만 결과에는 나오지 않는다. 보수는 죽은 노드를 가리키던",
                       "이웃 목록을 다시 잇는다(초록). 공간 회수는 보수가 끝난 뒤에만 하며, 파라미터로 켜고 끈다."])
    b.append(t)
    return fig("cubvec-2026-t2-vacuum", "Process" + EB, "DELETE·UPDATE에서 vacuum까지",
               "DELETE와 UPDATE가 엔트리에 제거 MVCCID를 표시하면, 그 버전을 보는 스냅샷이 사라진 뒤 vacuum이 노드를 삭제 상태로 바꾸고, 이웃 목록을 다시 이은 다음 선택적으로 공간을 회수한다.",
               y, b)






def t5_concurrency():
    b = [zone(16, 48, 312, 236, "1단계 · 인덱스 단위 직렬화"), zone(352, 48, 312, 236, "2단계 · 구간 잠금과 latch")]
    sx = [32, 128, 224]
    for x in sx:
        b.append(line(x + 40, 124, x + 40, 160))
    b.append(line(168, 200, 168, 228))
    for i, x in enumerate(sx):
        b.append(box(x, 88, 80, 36, f"세션 {i + 1}"))
    b.append(box(48, 160, 240, 40, "인덱스 잠금", kind="cost"))
    b.append(box(84, 228, 168, 40, "HNSW 그래프"))
    rx = [368, 464, 560]
    for x in rx:
        b.append(line(x + 44, 124, x + 44, 156))
        b.append(line(x + 44, 192, x + 44, 228))
    for i, x in enumerate(rx):
        b.append(box(x, 88, 88, 36, f"세션 {i + 1}"))
        b.append(box(x, 156, 88, 36, f"캐시 구간 {i + 1}"))
    b.append(box(368, 228, 280, 40, "HNSW 그래프", "page latch on neighbor lists", kind="good"))
    t, y = notes(316, ["1단계는 쓰기를 하나씩 실행해 결과가 맞는지 먼저 확인했다. 2단계는 캐시를 구간마다 따로 잠가",
                       "삽입과 검색이 함께 진행된다. 이웃 목록은 정해진 순서로 latch를 잡고 고쳐 교착 상태를 막는다."])
    b.append(t)
    return fig("cubvec-2026-t5-concurrency", "Architecture delta" + EB, "동시성 제어의 두 단계",
               "1단계에서는 모든 세션이 인덱스 하나의 잠금을 거쳐 차례로 그래프를 고치고, 2단계에서는 세션이 캐시 구간별 잠금과 페이지 latch를 따로 잡아 함께 진행한다.",
               y, b)





















ALL = [d2_layers, d3_layout, t1_snapshot, t2_vacuum, t5_concurrency]

if __name__ == "__main__":
    for fn in ALL:
        slug, html = fn()
        with open(os.path.join(HERE, slug + ".html"), "w", encoding="utf-8") as f:
            f.write(html)
        print("wrote", slug)
