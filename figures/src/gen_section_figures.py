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


def d1_incremental():
    b = [lane(80, "HNSW", "점진 빌드"), lane(170, "정적 그래프", "DiskANN 계열")]
    xs = [128, 260, 392, 524]
    w, h = 108, 44
    r1 = [("빈 인덱스", "empty", "plain"), ("행 삽입", "insert", "plain"), ("행 삽입", "insert", "plain"),
          ("품질 유지", "no rebuild", "good")]
    r2 = [("한 번에 빌드", "batch build", "plain"), ("행 삽입", "insert", "plain"), ("품질 저하", "graph drifts", "cost"),
          ("다시 빌드", "user rebuild", "plain")]
    for yc, row in ((86, r1), (176, r2)):
        for i in range(3):
            b.append(line(xs[i] + w, yc, xs[i + 1], yc))
        for x, (n, s, k) in zip(xs, row):
            b.append(box(x, yc - h / 2, w, h, n, s, k))
    t, y = notes(240, ["빈 인덱스에 행을 하나씩 넣어도 검색 품질이 유지되므로, 행이 계속 들어오는 테이블에 맞다.",
                       "정적 그래프 구조는 같은 스토리지 API 위에 나중에 추가할 수 있다."])
    b.append(t)
    return fig("cubvec-2026-d1-incremental", "Comparison" + EB, "점진 빌드와 정적 빌드",
               "HNSW는 빈 인덱스에 행을 하나씩 넣어도 검색 품질이 유지되지만, 정적 그래프 구조는 행이 들어올수록 품질이 떨어져 다시 빌드해야 한다.",
               y, b)


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


def d4_pagefit():
    b = []
    cx = 200
    b.append(line(cx, 96, cx, 118))
    b.append(line(cx + 100, 150, 400, 150))
    b.append(label(350, 140, "아니오"))
    b.append(line(cx, 182, cx, 224))
    b.append(label(cx + 12, 208, "예", anchor="start"))
    b.append(line(cx + 116, 258, 400, 258))
    b.append(label(358, 248, "아니오"))
    b.append(line(cx, 292, cx, 356))
    b.append(label(cx + 12, 328, "예", anchor="start"))
    b.append(opath([(480, 282), (480, 380), (304, 380)]))
    b.append(oval(100, 52, 200, 44, "새 노드", "size from dim, M, level"))
    b.append(diamond(cx, 150, 200, 64, ["한 페이지에", "들어가나?"]))
    b.append(box(400, 126, 176, 48, "삽입 오류", "before any page is allocated", kind="cost"))
    b.append(diamond(cx, 258, 232, 68, ["마지막 페이지에", "여유가 있나?"]))
    b.append(box(400, 234, 160, 48, "새 페이지 할당", "system operation"))
    b.append(box(96, 356, 208, 48, "그 페이지에 레코드 추가"))
    t, y = notes(440, ["페이지 크기는 데이터베이스를 만들 때 정한 4K·8K·16K이고, 레코드 하나는 페이지 하나를 넘을 수 없다.",
                       "새 페이지는 시스템 연산으로 할당하므로, 트랜잭션을 롤백해도 해제되지 않는다."])
    b.append(t)
    return fig("cubvec-2026-d4-pagefit", "Flowchart" + EB, "새 노드를 페이지에 놓는 흐름",
               "새 노드가 어떤 페이지에도 들어가지 않으면 삽입 오류로 처리하고, 마지막 페이지에 여유가 없으면 시스템 연산으로 새 페이지를 할당한 뒤 레코드를 추가한다.",
               y, b)


def d5_catalog():
    b = [zone(232, 52, 208, 184, "카탈로그")]
    b.append(line(192, 144, 232, 144))
    b.append(line(440, 144, 456, 144))
    b.append(line(524, 168, 524, 208))
    b.append(line(616, 168, 616, 208))
    b.append(box(16, 120, 176, 48, "CREATE INDEX", "USING hnsw"))
    for i, (n, s) in enumerate((("Root Class", "index type per attribute"), ("System Catalog", "B-tree stats only"),
                                ("_db_index", "name · keys · comment"))):
        b.append(box(248, 84 + i * 50, 176, 44, n, s))
    b.append(box(456, 120, 208, 48, "옵티마이저", "picks the scan by index type"))
    b.append(box(480, 208, 88, 44, "B-tree", "scan"))
    b.append(box(572, 208, 92, 44, "벡터 인덱스", "scan", kind="focal"))
    t, y = notes(284, ["인덱스 타입이 카탈로그 세 곳에 함께 기록된다. B-tree 통계에는 B-tree 인덱스만 들어간다.",
                       "옵티마이저는 이 타입을 보고 B-tree 스캔과 벡터 인덱스 스캔을 구분한다."])
    b.append(t)
    return fig("cubvec-2026-d5-catalog", "Architecture" + EB, "카탈로그에 기록되는 인덱스 타입",
               "벡터 인덱스를 만들면 Root Class, System Catalog, _db_index에 인덱스 타입이 기록되고, 옵티마이저는 그 타입으로 B-tree 스캔과 벡터 인덱스 스캔을 구분한다.",
               y, b)


def d6_cache():
    b = []
    cx = 200
    b.append(line(cx, 96, cx, 120))
    b.append(line(cx + 100, 150, 400, 150))
    b.append(label(350, 140, "예"))
    b.append(line(cx, 180, cx, 212))
    b.append(label(cx + 12, 200, "아니오", anchor="start"))
    b.append(line(cx, 260, cx, 288))
    b.append(line(cx, 336, cx, 364))
    b.append(opath([(488, 174), (488, 388), (304, 388)], accent=False))
    b.append(oval(100, 52, 200, 44, "이웃 목록 요청", "(node, level)"))
    b.append(diamond(cx, 150, 200, 60, ["이웃 캐시에 있나?"]))
    b.append(box(400, 126, 176, 48, "캐시에서 읽기", "no page fix", kind="good"))
    b.append(box(96, 212, 208, 48, "페이지 고정 · 읽기", "page buffer fix / unfix", kind="cost"))
    b.append(box(96, 288, 208, 48, "캐시에 저장", "kept in step with the page"))
    b.append(box(96, 364, 208, 48, "이웃마다 거리 계산", "vector cache works the same"))
    t, y = notes(448, ["노드 방문 한 번이 페이지 고정 한 번이므로, 캐시 적중이 곧 디스크 I/O 절감이다.",
                       "nytimes-256 인덱스 빌드에서 데이터 페이지 접근이 약 267억 회에서 7,085만 회로 줄었다."])
    b.append(t)
    return fig("cubvec-2026-d6-cache", "Flowchart" + EB, "이웃 캐시로 페이지 고정 줄이기",
               "이웃 목록이 캐시에 있으면 페이지를 고정하지 않고 읽고, 없으면 페이지를 고정해 읽은 뒤 캐시에 저장한다. 벡터 캐시도 같은 방식으로 동작한다.",
               y, b)


def d7_distance():
    b = []
    yc = 112
    b.append(line(112, yc, 136, yc))
    b.append(line(256, yc, 280, yc))
    b.append(line(416, yc, 440, yc))
    b.append(label(428, yc - 10, "예"))
    b.append(line(568, yc, 592, yc))
    b.append(line(348, yc + 32, 348, 192))
    b.append(label(360, 172, "아니오", anchor="start"))
    b.append(box(16, yc - 22, 96, 44, "후보 노드"))
    b.append(box(136, yc - 22, 120, 44, "int8 거리", "quantized, cheap"))
    b.append(diamond(348, yc, 136, 64, ["반경 안인가?"]))
    b.append(box(440, yc - 22, 128, 44, "fp32 거리", "SIMD, 64B aligned", kind="good"))
    b.append(box(592, yc - 22, 72, 44, "이웃 선택"))
    b.append(box(288, 192, 120, 40, "후보에서 제외", kind="dead"))
    t, y = notes(272, ["인덱스 빌드 시간의 대부분은 거리 계산이다. 값싼 int8 거리로 먼저 걸러,",
                       "SIMD(AVX2) 정밀 거리 계산의 횟수를 줄이는 방식을 시험했다."])
    b.append(t)
    return fig("cubvec-2026-d7-distance", "Flowchart" + EB, "두 단계 거리 계산",
               "후보 노드는 먼저 int8 양자화 거리로 반경 안인지 확인하고, 반경 안의 후보만 64바이트 정렬된 벡터로 SIMD fp32 거리를 계산한다.",
               y, b)


def d8_parallel():
    b = []
    b.append(line(128, 140, 160, 140))
    b.append(opath([(264, 128), (284, 128), (284, 80), (304, 80)]))
    b.append(line(264, 140, 304, 140))
    b.append(opath([(264, 152), (284, 152), (284, 200), (304, 200)]))
    b.append(opath([(440, 80), (460, 80), (460, 128), (488, 128)]))
    b.append(line(440, 140, 488, 140))
    b.append(opath([(440, 200), (460, 200), (460, 152), (488, 152)]))
    b.append(line(576, 236, 576, 164))
    b.append(box(16, 116, 112, 48, "힙 테이블", "existing rows"))
    b.append(box(160, 116, 104, 48, "행 묶음", "chunks"))
    for i, yc in enumerate((80, 140, 200)):
        b.append(box(304, yc - 22, 136, 44, f"작업자 {i + 1}", "own thread entry"))
    b.append(box(488, 116, 176, 48, "HNSW 그래프", "page storage", kind="focal"))
    b.append(box(488, 236, 176, 44, "loaddb -C", "parallel sessions"))
    t, y = notes(316, ["데이터가 있는 테이블에 인덱스를 만들면, 힙의 행을 묶음으로 나눠 작업자들이 동시에 넣는다.",
                       "작업자는 각자 스레드 문맥으로 페이지 버퍼에 접근한다. loaddb 병렬 적재도 같은 그래프에 넣는다."])
    b.append(t)
    return fig("cubvec-2026-d8-parallel", "Data flow" + EB, "인덱스 병렬 적재",
               "힙 테이블의 행을 묶음으로 나눠 worker pool의 작업자들이 동시에 HNSW 그래프에 넣고, loaddb 병렬 적재 세션도 같은 그래프에 넣는다.",
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


def t3_rollback():
    b = []
    for x, s in ((16, "롤백한 문장"), (176, "롤백 전"), (432, "롤백 후")):
        b.append(text(x, 56, s, size=12, weight=600, fill=MUTED))
    rows = [("INSERT", [("새 엔트리 · 유효", "good")], [("새 엔트리 · 삭제됨", "dead")]),
            ("DELETE", [("엔트리 · 제거 대기", "wait")], [("엔트리 · 유효", "good")]),
            ("UPDATE", [("이전 · 제거 대기", "wait"), ("새 · 유효", "good")],
             [("이전 · 유효", "good"), ("새 · 삭제됨", "dead")])]
    for i, (stmt, before, after) in enumerate(rows):
        yc = 96 + i * 72
        b.append(line(384, yc, 432, yc))
        b.append(chip(16, yc - 14, 96, 28, stmt, mono=True))
        for col_x, items in ((176, before), (432, after)):
            n = len(items)
            for j, (s, k) in enumerate(items):
                hh = 28 if n == 1 else 24
                yy = yc - 14 if n == 1 else yc - 26 + j * 28
                b.append(chip(col_x, yy, 208, hh, s, kind=k))
    lx = 16
    ly = 312
    b.append(f'<line x1="16" y1="{ly - 12}" x2="{W - 16}" y2="{ly - 12}" stroke="{RULE}" stroke-width="0.8"/>')
    for s, k in (("유효", "good"), ("제거 대기", "wait"), ("삭제됨", "dead")):
        b.append(chip(lx, ly, 72, 20, s, kind=k))
        lx += 88
    t, y = notes(360, ["롤백은 자기 트랜잭션이 남긴 표시만 되돌린다. DELETE 롤백은 로그에 함께 남긴 벡터로",
                       "되살릴 엔트리를 찾고, UPDATE 롤백은 제거와 삽입 두 연산의 되돌리기로 이루어진다."])
    b.append(t)
    return fig("cubvec-2026-t3-rollback", "State change" + EB, "문장별 롤백",
               "INSERT 롤백은 새 엔트리를 삭제 상태로, DELETE 롤백은 제거 대기 엔트리를 유효 상태로, UPDATE 롤백은 이전 엔트리를 유효로 새 엔트리를 삭제 상태로 되돌린다.",
               y, b)


def t4_recovery():
    b = [zone(176, 44, 168, 128, "로그")]
    yc = 108
    b.append(line(152, yc, 176, yc))
    b.append(line(344, yc, 368, yc))
    b.append(line(480, yc, 504, yc))
    b.append(opath([(560, 132), (560, 156), (476, 156), (476, 196)]))
    b.append(opath([(608, 132), (608, 196)]))
    b.append(opath([(476, 240), (476, 260), (520, 260), (520, 280)]))
    b.append(opath([(608, 240), (608, 280)]))
    b.append(box(16, 84, 136, 48, "인덱스 변경", "INSERT / DELETE / UPDATE"))
    for i, s in enumerate(("엔트리 삽입", "엔트리 삭제", "엔트리 되살리기")):
        b.append(chip(192, 72 + i * 32, 136, 26, s))
    b.append(box(368, 84, 112, 48, "비정상 종료", "kill -9", kind="cost"))
    b.append(box(504, 84, 160, 48, "재시작 복구", "log replay"))
    b.append(box(416, 196, 120, 44, "REDO", "committed txns"))
    b.append(box(552, 196, 112, 44, "UNDO", "uncommitted txns"))
    b.append(oval(432, 280, 232, 44, "힙과 인덱스 검색 결과 일치"))
    t, y = notes(360, ["로그 레코드는 페이지 바이트가 아니라 '어느 행의 어떤 벡터'라는 논리 연산을 남긴다.",
                       "복구는 커밋된 변경을 다시 적용하고(REDO), 커밋되지 않은 변경을 되돌린다(UNDO)."])
    b.append(t)
    return fig("cubvec-2026-t4-recovery", "Data flow" + EB, "로그 레코드와 복구",
               "벡터 인덱스 변경은 삽입·삭제·되살리기 로그 레코드로 남고, 비정상 종료 뒤 재시작 복구가 커밋된 변경은 REDO로, 커밋되지 않은 변경은 UNDO로 처리해 힙과 인덱스를 맞춘다.",
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


# =============================================================== vector-search-query


def q1_plan():
    b = [zone(16, 48, 312, 232, "인덱스 없음"), zone(352, 48, 312, 232, "벡터 인덱스")]
    b.append(line(172, 128, 172, 156))
    b.append(line(172, 200, 172, 228))
    b.append(line(508, 128, 508, 228))
    b.append(text(520, 182, "정렬 단계 없음", size=12, weight=500, fill=MUTED))
    b.append(box(72, 84, 200, 44, "힙 스캔", "distance for every row"))
    b.append(box(72, 156, 200, 44, "정렬", "ORDER BY dist", kind="cost"))
    b.append(box(72, 228, 200, 40, "LIMIT k"))
    b.append(box(408, 84, 200, 44, "벡터 인덱스 스캔", "nearest first", kind="good"))
    b.append(box(408, 228, 200, 40, "LIMIT k"))
    t, y = notes(312, ["ORDER BY의 거리 함수·연산자가 인덱스의 컬럼과 메트릭에 맞고 LIMIT이 있으면,",
                       "옵티마이저가 오른쪽 플랜을 고른다. 인덱스가 거리 순서로 결과를 넘기므로 정렬을 붙이지 않는다."])
    b.append(t)
    return fig("cubvec-2026-q1-plan", "Plan comparison" + EB, "벡터 인덱스 스캔 플랜",
               "인덱스가 없으면 모든 행의 거리를 계산해 정렬한 뒤 k건을 자르지만, 벡터 인덱스 스캔 플랜은 거리 순서로 결과를 받으므로 정렬 단계 없이 k건을 자른다.",
               y, b)


def q2_driver():
    b = [lane(84, "문자열 전송"), lane(164, "네이티브 전송"), lane(244, "대량 적재")]
    r1 = [(120, 96, "float 배열", None, "plain"), (240, 120, "'[x, y, …]'", "string", "plain"),
          (384, 104, "CAS 파싱", "per query", "cost"), (512, 104, "벡터 값", "DB_VALUE", "plain")]
    r2 = [(120, 120, "Vector 객체", "CUBRIDdb.Vector", "plain"), (264, 120, "차원 + float32", "binary", "good"),
          (512, 104, "벡터 값", "DB_VALUE", "plain")]
    r3 = [(120, 120, "copy() writer", "write_row()", "plain"), (264, 120, "바이너리 행", "FORMAT BINARY", "good"),
          (408, 120, "서버", "copy session", "plain"), (552, 64, "힙", None, "plain")]
    for yc, row in ((84, r1), (164, r2), (244, r3)):
        for a, c in zip(row, row[1:]):
            b.append(line(a[0] + a[1], yc, c[0], yc))
        for x, w, n, s, k in row:
            b.append(box(x, yc - 22, w, 44, n, s, k))
    t, y = notes(300, ["문자열 경로는 질의마다 float 배열을 문자열로 바꾸고, CAS가 다시 파싱한다.",
                       "네이티브 전송과 COPY는 float 배열을 그대로 보낸다."])
    b.append(t)
    return fig("cubvec-2026-q2-driver", "Data flow" + EB, "벡터를 서버로 보내는 세 경로",
               "질의 벡터를 문자열로 보내면 CAS가 매번 파싱하지만, 네이티브 벡터 타입은 차원과 float32 배열을 그대로 보내고, COPY는 바이너리 행을 서버에서 바로 힙에 넣는다.",
               y, b)


def q3_stats():
    b = [zone(272, 160, 392, 128, "statdump · HNSW 통계")]
    b.append(opath([(192, 144), (224, 144), (224, 92), (272, 92)]))
    b.append(opath([(192, 160), (224, 160), (224, 220), (272, 220)]))
    b.append(box(16, 128, 176, 48, "벡터 인덱스 스캔 · 빌드", "HNSW search / insert"))
    b.append(box(272, 64, 392, 56, "trace (;trace on)", "per query: time · fetch · ioread"))
    for i, s in enumerate(("탐색", "삽입", "후보 큐")):
        b.append(chip(288 + i * 124, 196, 112, 30, s))
    for i, s in enumerate(("스토리지 · 캐시", "레벨 0")):
        b.append(chip(288 + i * 124, 236, 112, 30, s, kind="focal" if i == 1 else "plain"))
    t, y = notes(320, ["trace는 질의 하나의 합계를, statdump는 서버 전체의 누적 카운터를 보여 준다.",
                       "탐색 비용의 대부분이 가장 아래 레벨에서 생기므로, 레벨 0 값을 따로 센다."])
    b.append(t)
    return fig("cubvec-2026-q3-stats", "Architecture" + EB, "trace와 statdump",
               "벡터 인덱스 스캔과 빌드에서 나온 값은 trace에서 질의별 합계로, statdump에서 탐색·삽입·후보 큐·스토리지와 캐시·레벨 0 묶음의 누적 카운터로 보인다.",
               y, b)


# =============================================================== benchmark


def b1_procedure():
    b = [lane(92, "fit", "빌드 측정"), lane(204, "query", "질의 측정")]
    xs = [120, 256, 392, 528]
    w = 124
    l1 = [("DB 기동", "db made at first start"), ("벡터 적재", "COPY binary"), ("인덱스 빌드", "M, ef_construction"),
          ("서버 재시작", "index persisted")]
    l2 = [("ef_search 설정", "SET SYSTEM PARAMETERS"), ("prepare", "ORDER BY <-> ? LIMIT k"),
          ("바인드 · 실행", "native vector bind"), ("Recall · QPS", "by ann-benchmarks")]
    for yc, row in ((96, l1), (208, l2)):
        for i in range(3):
            b.append(line(xs[i] + w, yc, xs[i + 1], yc))
    b.append(opath([(590, 118), (590, 152), (182, 152), (182, 186)]))
    for yc, row in ((96, l1), (208, l2)):
        for x, (n, s) in zip(xs, row):
            b.append(box(x, yc - 22, w, 44, n, s, kind="focal" if n == "인덱스 빌드" else "plain"))
    t, y = notes(264, ["빌드 단계(fit)의 시간이 인덱스 빌드 성능이다. 질의 단계에서는 ann-benchmarks가",
                       "Recall과 QPS를 계산하며, 이 단계를 ef_search 값마다 한 번씩 되풀이한다."])
    b.append(t)
    return fig("cubvec-2026-b1-procedure", "Process" + EB, "ann-benchmarks 측정 절차",
               "빌드 단계에서는 DB를 기동하고 벡터를 COPY로 적재한 뒤 인덱스를 빌드하고 서버를 재시작하며, 질의 단계에서는 ef_search를 설정하고 질의를 prepare한 뒤 네이티브 벡터로 바인드해 실행하고 Recall과 QPS를 계산한다.",
               y, b)


# =============================================================== verification


def v1_ctp():
    b = [zone(16, 48, 648, 176, "PR마다 CI (test_cubvec)")]
    b.append(line(192, 106, 232, 106))
    b.append(line(368, 106, 408, 106))
    b.append(opath([(464, 128), (464, 168), (496, 168)]))
    b.append(line(192, 192, 496, 192))
    b.append(box(40, 84, 152, 44, "cases/*.sql", "SQL test case"))
    b.append(box(40, 170, 152, 44, "answers/*.answer", "expected output"))
    b.append(box(232, 84, 136, 44, "CTP 실행", "run against the server"))
    b.append(box(408, 84, 112, 44, "실행 결과", "*.result"))
    b.append(box(496, 156, 152, 48, "바이트 비교", "pass only if identical", kind="focal"))
    t, y = notes(256, ["새 기능의 PR은 자기 케이스를 함께 추가하고, 기존 케이스를 모두 통과해야 병합된다.",
                       "케이스는 공개 저장소(cubrid-testcases, cubvec/cubvec)에서 관리한다."])
    b.append(t)
    return fig("cubvec-2026-v1-ctp", "Process" + EB, "SQL 테스트 케이스와 CI",
               "PR마다 CI가 케이스 SQL을 서버에서 실행하고, 실행 결과를 정답 파일과 바이트 단위로 비교해 같을 때만 통과로 판정한다.",
               y, b)


def v2_mixed():
    b = [zone(16, 108, 312, 236, "인덱스를 쓰지 않는 질의"), zone(352, 108, 312, 236, "인덱스를 쓰는 질의")]
    b.append(opath([(300, 92), (172, 92), (172, 144)]))
    b.append(opath([(380, 92), (508, 92), (508, 144)]))
    b.append(line(172, 188, 172, 212))
    b.append(line(508, 188, 508, 212))
    b.append(oval(300, 52, 80, 44, "질의"))
    b.append(text(340, 40, "WHERE p ORDER BY dist LIMIT k", size=8, mono=True, fill=MUTED, anchor="middle"))
    b.append(box(72, 144, 200, 44, "p를 만족하는 행 전부", "exact scan"))
    b.append(box(408, 144, 200, 44, "후보 k개", "vector index scan"))
    b.append(f'<rect x="40" y="212" width="264" height="116" rx="6" fill="{GOOD_FILL}" stroke="{GOOD}" stroke-width="1"/>')
    b.append(text(56, 236, "판정", size=12, weight=600, fill=GOOD))
    b.append(text(56, 260, "전체 정렬 결과와 같다", size=12, weight=500))
    b.append(f'<rect x="376" y="212" width="264" height="116" rx="6" fill="{GOOD_FILL}" stroke="{GOOD}" stroke-width="1"/>')
    b.append(text(392, 236, "판정", size=12, weight=600, fill=GOOD))
    for i, s in enumerate(("결과가 k건 이하이다", "모든 행이 p를 만족한다", "거리 순서로 나온다")):
        b.append(text(392, 260 + i * 22, s, size=12, weight=500))
    t, y = notes(376, ["조건의 선택도(행의 대부분부터 아주 일부까지)와 LIMIT 값을 바꿔 가며 같은 판정을 반복한다.",
                       "인덱스를 쓰는 질의는 조건과 가시성으로 걸러진 만큼 k건보다 적을 수 있다."])
    b.append(t)
    return fig("cubvec-2026-v2-mixed", "Comparison" + EB, "조건 결합 질의의 판정 기준",
               "인덱스를 쓰지 않는 질의는 조건을 만족하는 행을 전부 정렬한 결과와 같아야 하고, 인덱스를 쓰는 질의는 k건 이하이며 모든 행이 조건을 만족하고 거리 순서여야 한다.",
               y, b)


def v3_recovery():
    b = [lane(80, "세션"), lane(160, "서버"), lane(240, "확인")]
    b.append(line(224, 80, 240, 80))
    b.append(line(328, 80, 344, 80))
    b.append(line(552, 160, 568, 160))
    b.append(line(616, 180, 616, 216))
    b.append(box(112, 58, 112, 44, "INSERT 200건"))
    b.append(box(240, 58, 88, 44, "COMMIT", kind="good"))
    b.append(box(344, 58, 112, 44, "UPDATE", "not committed", kind="wait"))
    b.append(chip(112, 150, 360, 20, "cub_server running", mono=True))
    b.append(box(480, 140, 72, 40, "kill -9", kind="cost"))
    b.append(box(568, 140, 96, 40, "재시작", "recovery"))
    b.append(box(568, 216, 96, 44, "SELECT", "search + count"))
    t, y = notes(296, ["커밋한 200건은 재시작 뒤 모두 검색되고, 커밋하지 않은 UPDATE는 남지 않아야 한다.",
                       "힙의 행 상태와 벡터 검색 결과가 일치할 때만 통과다."])
    b.append(t)
    return fig("cubvec-2026-v3-recovery", "Timeline" + EB, "강제 종료와 복구 시나리오",
               "세션이 200건을 삽입해 커밋하고 다른 UPDATE를 커밋하지 않은 상태에서 서버를 강제 종료한 뒤, 재시작 복구 후 커밋한 행만 검색되는지 확인한다.",
               y, b)


def v4_concurrency():
    b = [zone(16, 48, 296, 200, "동시 실행"), zone(336, 48, 328, 336, "실행 뒤 검사")]
    b.append(line(92, 124, 92, 176))
    b.append(line(232, 124, 232, 176))
    b.append(line(500, 124, 500, 152))
    b.append(line(500, 196, 500, 220))
    b.append(line(500 + 80, 252, 600, 252))
    b.append(label(590, 242, "예"))
    b.append(line(500, 284, 500, 316))
    b.append(label(512, 304, "아니오", anchor="start"))
    b.append(box(32, 84, 120, 40, "삽입 세션들"))
    b.append(box(176, 84, 112, 40, "검색 세션"))
    b.append(box(32, 176, 256, 44, "같은 HNSW 인덱스", "searched while it is built"))
    b.append(box(392, 84, 216, 40, "테이블의 모든 행 r"))
    b.append(box(392, 152, 216, 44, "r의 벡터로 최근접 1건", "1-NN search"))
    b.append(diamond(500, 252, 160, 64, ["결과가 r인가?"]))
    b.append(box(600, 232, 56, 40, "통과", kind="good"))
    b.append(box(424, 316, 152, 44, "노드 유실 · 고립", kind="cost"))
    t, y = notes(416, ["동시 실행에서는 그래프가 매번 다르게 만들어지므로, 어떤 근사 결과가 나오는지는 판정하지 않는다.",
                       "오류·latch 시간 초과가 없고, 돌려준 행이 실제 행이며, 모든 행이 자기 벡터로 검색되는지를 본다."])
    b.append(t)
    return fig("cubvec-2026-v4-concurrency", "Process" + EB, "동시성 시나리오와 자기 검색 검사",
               "여러 삽입 세션과 검색 세션이 같은 인덱스를 동시에 쓰고 읽은 뒤, 모든 행에 대해 자기 벡터로 최근접 1건을 검색해 그 행 자신이 나오는지로 그래프가 온전한지 판정한다.",
               y, b)


ALL = [d1_incremental, d2_layers, d3_layout, d4_pagefit, d5_catalog, d6_cache, d7_distance, d8_parallel,
       t1_snapshot, t2_vacuum, t3_rollback, t4_recovery, t5_concurrency,
       q1_plan, q2_driver, q3_stats, b1_procedure, v1_ctp, v2_mixed, v3_recovery, v4_concurrency]

if __name__ == "__main__":
    for fn in ALL:
        slug, html = fn()
        with open(os.path.join(HERE, slug + ".html"), "w", encoding="utf-8") as f:
            f.write(html)
        print("wrote", slug)
