# 벡터 인덱스 지원

## 벡터 인덱스

이 페이지는 CUBRID 데이터베이스에서 벡터 인덱스의 CRUD 작업을 설명합니다.

현재 CUBRID는 벡터 데이터를 위한 **Hierarchical Navigable Small World (HNSW)** 인덱스를 지원합니다.

### 벡터 인덱스 생성

벡터 인덱스를 생성하려면 다음 사항을 지정해야 합니다:

1. 인덱스를 생성할 테이블과 열 이름.
2. 거리 계산에 사용할 메트릭 함수 (예: 코사인 거리).
3. 인덱스 생성 매개변수:
   * `ef_construction`: 인덱스 생성 시 확인할 이웃의 수를 제어합니다.
   * `M`: 그래프에서 노드당 최대 간선(연결) 수를 결정합니다.

**검색 매개변수:** HNSW 인덱스를 사용하여 쿼리할 때는 다음을 지정해야 합니다:

* `ef_search`: 쿼리 중 탐색할 최근접 이웃 후보의 수를 제어합니다.

#### BNF

CUBRID에서 벡터 인덱스를 생성하는 공식 문법은 다음과 같습니다:

<pre><code>&#x3C;create_vector_index> ::= "CREATE VECTOR INDEX" &#x3C;index_name>
"ON" &#x3C;table_name> "(" &#x3C;column_name> &#x3C;metric_function> ")" &#x3C;with_options>

&#x3C;index_name> ::= &#x3C;identifier>
&#x3C;table_name> ::= &#x3C;identifier>
&#x3C;column_name> ::= &#x3C;identifier>

&#x3C;metric_function> ::= &#x3C;cosine> | &#x3C;l2> | &#x3C;inner_product>
<strong>    &#x3C;cosine> ::= "cosine"
</strong>    &#x3C;l2> ::= "l2"
    &#x3C;inner_product> ::= "inner_product"

&#x3C;with_options> ::= "WITH" "(" &#x3C;option_list> ")"
    &#x3C;option_list> ::= &#x3C;option> | &#x3C;option> "," &#x3C;option_list>
    &#x3C;option> ::= &#x3C;parameter> "=" &#x3C;value>

&#x3C;parameter> ::= "M" | "ef_construction"
&#x3C;value> ::= &#x3C;integer>

&#x3C;identifier> ::= [A-Za-z_][A-Za-z_0-9]*
&#x3C;integer> ::= [0-9]+
</code></pre>

#### 매개변수 설명

* **M**: 이는 HNSW 구조의 각 레이어에서 그래프 내 노드(벡터)가 가질 수 있는 최대 연결 수를 의미합니다. 그래프에서 각 노드의 [\*](https://cubvec.github.io/cubvec-spec-ko/vector-index.html#id4)차수\*라고도 합니다. _M_ 값이 높아질수록 회상 정확도가 증가하지만 메모리 사용량과 생성 시간이 증가합니다.
* **ef\_construction**: 인덱스 생성 단계에서 동적 후보 리스트의 크기를 제어합니다. 그래프에 요소를 삽입할 때 확인할 이웃의 수를 정의합니다. 값이 높을수록 인덱스가 더 정확해지지만 생성 시간이 길어집니다.

#### 예시

코사인 유사도로 HNSW 인덱스를 생성하는 예:

```
CREATE VECTOR INDEX embedding_hnsw_idx
ON items (embedding cosine)
WITH (M = 16, ef_construction = 64);
```

* 이 예에서는 _items_ 테이블의 _embedding_ 열에 코사인 유사도를 사용하여 _embedding\_hnsw\_idx_ 벡터 인덱스를 생성하며, [\`](https://cubvec.github.io/cubvec-spec-ko/vector-index.html#id7)M\`은 16, [\`](https://cubvec.github.io/cubvec-spec-ko/vector-index.html#id9)ef\_construction\`은 64로 설정합니다.

### 벡터 인덱스 옵션 검사

테이블에서 인덱스를 선택하여 인덱스 구성을 검사할 수 있습니다.

```
SELECT embedding_hnsw_idx
FROM items;
```

이 쿼리는 _embedding\_hnsw\_idx_ 인덱스의 세부 정보를 검색합니다.

### 검색 매개변수 구성

_ef\_search_ 매개변수는 검색 쿼리 중에 탐색할 최근접 이웃 후보 수를 제어합니다.

* **ef\_search**: 검색 시 탐색 팩터로, 알고리즘이 최근접 이웃을 찾을 때 탐색할 후보 노드의 수를 결정합니다. _ef\_search_ 값이 높을수록 회상 정확도가 향상되지만 쿼리 시간이 느려질 수 있습니다.
* 기본적으로 _ef\_search_ 가 지정되지 않으면 인덱스 생성 시 사용된 _ef\_construction_ 값과 동일하게 설정됩니다.

#### 예시

쿼리에서 _ef\_search_ 매개변수를 구성하는 방법:

```
SELECT /*+ VECTOR_INDEX_SCAN (embedding) */ name
FROM items
ORDER BY l2_distance(embedding, '[3, 1, 2]')
LIMIT 5
WITH (ef_search = 64);
```

* 이 쿼리에서는 _VECTOR\_INDEX\_SCAN_ 힌트를 사용하여 벡터 인덱스를 강제로 적용하고, 검색 정확도를 제어하기 위해 _ef\_search_ 값을 64로 설정합니다.

### 벡터 인덱스 업데이트

현재 CUBRID에서는 벡터 인덱스 업데이트를 지원하지 않습니다. 매개변수를 변경하려면 인덱스를 재생성해야 합니다.

### 벡터 인덱스 삭제

벡터 인덱스를 삭제하려면 _DROP INDEX_ 명령을 사용합니다.

```
DROP INDEX embedding_hnsw_idx;
```

* 이 명령은 _items_ 테이블에서 _embedding\_hnsw\_idx_ 인덱스를 삭제합니다.

### 벡터 인덱스 구성

#### 메모리 사용량

벡터 인덱스에 사용할 메모리는 _cubrid.conf_ 구성 파일에서 설정할 수 있습니다. _vector\_memory\_size_ 매개변수는 벡터 인덱스 작업에 할당된 메모리 크기를 지정합니다.

```
# 파일명: cubrid.conf
vector_memory_size = 8G
```

* 이 예에서는 벡터 인덱스에 할당된 메모리 크기를 8GB로 설정합니다.

### 추가 구성 참고 사항

* 대규모 데이터셋의 경우 인덱스 생성이나 쿼리 처리 중 메모리 오버플로를 방지하기 위해 [\`](https://cubvec.github.io/cubvec-spec-ko/vector-index.html#id19)vector\_memory\_size\`가 충분히 높게 설정되었는지 확인하십시오.
* _M_, _ef\_construction_, _ef\_search_ 값을 조정하여 검색 정확도, 속도, 메모리 사용량을 애플리케이션 요구 사항에 맞게 균형을 맞출 수 있습니다.

## 2026년 확장 사항

이 절은 2026년(3차년도)에 추가된 벡터 인덱스 사용자 스펙을 설명합니다. 기능마다 적용 브랜치를 표시했습니다. 전체 변경 내역은 [변경 이력](revision.md)을 참고하십시오. 내부 구조는 개발리포트의 [2026](../dev-report/2026/README.md)에 있습니다.

### CREATE INDEX … USING 구문

> 적용 브랜치: `cubvec/cubvec`

B-tree 인덱스와 벡터 인덱스를 같은 `CREATE INDEX` 구문으로 만들고, 인덱스 구현은 `USING` 절로 고릅니다. 기존 B-tree 인덱스 구문은 바뀌지 않습니다.

```
<create_index> ::= "CREATE" ["UNIQUE"] "INDEX" <index_name> "ON" <table_name>
                   "(" <column_list> ")" ["USING" "btree"] [<btree_options>]

<create_vector_index> ::= "CREATE" "INDEX" <index_name> "ON" <table_name>
                          "(" <column_name> <metric> ")" ["USING" "hnsw"]
                          ["WITH" "(" <build_option> {"," <build_option>} ")"]

<metric>       ::= "cosine" | "dot" | "euclidean" | "manhattan"
<build_option> ::= "m" "=" <integer> | "ef_construction" "=" <integer>
```

* 컬럼 뒤에 거리 메트릭을 쓰면 벡터 인덱스입니다. `USING`을 생략하고 메트릭을 쓰면 `hnsw`로 만들어집니다.
* 메트릭은 `cosine`(코사인 거리), `dot`(내적), `euclidean`(L2 거리), `manhattan`(L1 거리) 가운데 하나입니다. 검색 질의의 거리 함수·연산자와 같은 메트릭이어야 인덱스를 씁니다.
* 빌드 옵션의 기본값은 `m = 16`, `ef_construction = 64`입니다. 각 옵션은 한 번만 쓸 수 있습니다.
* 이전 구문 `CREATE VECTOR INDEX … ON t (col metric) WITH (…)`도 같은 의미로 계속 쓸 수 있습니다. 새로 작성하는 SQL에는 `USING` 구문을 권장합니다.

```
-- 벡터 인덱스: 구현을 명시
CREATE INDEX idx_embedding ON items (embedding COSINE) USING hnsw
WITH (m = 16, ef_construction = 64);

-- 메트릭만 쓰면 hnsw
CREATE INDEX idx_embedding_l2 ON items (embedding EUCLIDEAN);

-- 기존 B-tree 인덱스 (USING btree는 생략 가능)
CREATE INDEX idx_id ON items (id);
```

벡터 인덱스에서 쓸 수 없는 조합은 구문 검사 단계에서 다음 오류로 거부됩니다.

| 경우 | 오류 메시지 |
| --- | --- |
| 알 수 없는 메트릭 | 올바르지 않은 `<메트릭>` 거리 메트릭이 지정되었습니다. |
| `btree`, `hnsw` 이외의 알고리즘 (예: `USING diskann`) | 지원하지 않는 인덱스 알고리즘 '`<이름>`' 입니다. |
| `USING btree`에 메트릭 지정 | 거리 메트릭은 hnsw 인덱스에만 지정할 수 있습니다. |
| `USING hnsw`에 메트릭 누락 | hnsw 인덱스에는 거리 메트릭이 필요합니다. 예: (컬럼 COSINE). |
| `UNIQUE` | hnsw 인덱스에서는 UNIQUE를 지원하지 않습니다. |
| `REVERSE` | hnsw 인덱스에서는 REVERSE를 지원하지 않습니다. |
| `ONLINE` 옵션 | hnsw 인덱스에서는 ONLINE 옵션을 지원하지 않습니다. |
| `DEDUPLICATE` 옵션 | hnsw 인덱스에서는 DEDUPLICATE 옵션을 지원하지 않습니다. |
| 부분 인덱스 (`WHERE` 절) | hnsw 인덱스에서는 부분 인덱스(WHERE 절)를 지원하지 않습니다. |
| B-tree에 `m`, `ef_construction` 지정 | 빌드 옵션(m, ef\_construction)은 hnsw 인덱스에만 지정할 수 있습니다. |

### 검색 파라미터 hnsw\_ef\_search

> 적용 브랜치: `cubvec/cubvec`, `cubvec/m1` — 2025년에 추가된 파라미터이며, 이 절에서 명세를 보완합니다.

검색할 때 탐색할 후보의 수는 시스템 파라미터 `hnsw_ef_search`로 정합니다. 값이 클수록 Recall이 높아지고 질의 시간이 늘어납니다.

| 항목 | 값 |
| --- | --- |
| 기본값 | 40 |
| 범위 | 1 – 1000 |
| 변경 | `cubrid.conf`에 지정하거나, 세션에서 `SET SYSTEM PARAMETERS`로 변경 |

```
SET SYSTEM PARAMETERS 'hnsw_ef_search=200';

SELECT id
FROM items
ORDER BY embedding <-> '[3, 1, 2]'
LIMIT 10;
```

### 트랜잭션과 장애 복구

> 적용 브랜치: `cubvec/m1`

벡터 인덱스는 디스크에 저장되며, B-tree 인덱스와 같이 트랜잭션과 장애 복구를 지원합니다.

* 벡터 인덱스가 있는 테이블의 INSERT, UPDATE, DELETE는 커밋하면 검색 결과에 반영되고, 롤백하면 반영되지 않습니다. 자세한 동작은 [DML](dml.md)을 참고하십시오.
* 커밋한 변경은 서버가 비정상 종료한 뒤 다시 시작해도 검색 결과에 남습니다. 커밋하지 않은 변경은 복구 과정에서 되돌려집니다.
* 서버를 다시 시작해도 인덱스를 다시 만들 필요가 없습니다. 인덱스를 처음 쓰는 시점에 디스크의 인덱스를 그대로 읽어 씁니다.
* 여러 세션이 같은 벡터 인덱스에 동시에 INSERT, UPDATE, DELETE를 실행할 수 있습니다.

현재 제약 사항은 다음과 같습니다.

* HA 복제 환경에서의 벡터 인덱스 동작은 아직 지원 범위가 아닙니다(4차년도 개발 예정).
* 벡터 인덱스를 만들고 지우는 DDL 자체의 롤백은 지원하지 않습니다.
* `WHERE` 조건과 함께 쓰는 벡터 검색은 조건과 트랜잭션 가시성으로 걸러진 만큼 `LIMIT k`보다 적은 행을 돌려줄 수 있습니다.

### 성능 통계

> 적용 브랜치: `cubvec/cubvec`, `cubvec/m1` (이웃 캐시 두 항목은 `cubvec/m1`에만 있음)

벡터 인덱스의 생성과 검색 중에 일어난 일은 `statdump`의 HNSW 통계로 확인합니다. 이름 끝에 `_l0`가 붙은 항목은 가장 아래 레벨(레벨 0)에서만 센 값입니다.

```
cubrid statdump -s hnsw -c -i 10 demodb
```

| 통계 | 의미 |
| --- | --- |
| `Num_hnsw_visited_node` | 방문한 노드 수 |
| `Num_hnsw_computed_distances` | 거리 계산 횟수 |
| `Num_hnsw_computed_distances_in_refines` | 새 노드의 이웃을 고를 때의 거리 계산 횟수 |
| `Num_hnsw_computed_distances_in_reverse_refines` | 기존 노드의 이웃 목록을 고칠 때의 거리 계산 횟수 |
| `Num_hnsw_entrypoint_updates` | 그래프 진입점이 바뀐 횟수 |
| `Num_hnsw_candidates_push` / `_pop` / `_prune` | 후보 큐에 넣고, 빼고, 버린 횟수 |
| `Num_hnsw_neighbors_scan` | 노드의 이웃 목록을 순회한 횟수 |
| `Num_hnsw_page_access` | 인덱스 페이지 접근 횟수 |
| `Num_hnsw_vector_access` | 벡터 접근 횟수 |
| `Num_hnsw_vector_cache_hit` / `_miss` | 벡터 캐시 적중·실패 횟수 |
| `Num_hnsw_neighbors_cache_hit` / `Num_hnsw_neighbors_page_fix` | 이웃 정보를 캐시에서 얻은 횟수와 페이지를 고정해 얻은 횟수 |

각 항목에는 `_l0` 항목이 함께 있습니다(진입점 변경 횟수 제외).
