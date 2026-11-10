# DML

이 페이지는 데이터베이스에서 벡터 데이터에 대한 CRUD(생성, 읽기, 업데이트, 삭제) 작업을 설명합니다.

### 테이블에 벡터 생성 및 삽입

테이블에 벡터를 삽입하려면 _INSERT_ 문을 사용합니다. 벡터는 SQL에서 단일 인용 부호로 감싸진 배열로 표현됩니다.

```
INSERT INTO items (
  embedding
)
VALUES
  ('[1,2,3]'),
  ('[4,5,6]');
```

* 여기서는 _embedding_ 열에 두 개의 벡터를 삽입하고 있습니다.
* 벡터는 문자열(_‘\[x,y,z]’_) 형식이어야 하며, _x_, _y_, _z_ 는 벡터 요소입니다.

### 벡터 읽기

테이블에서 벡터를 검색하려면 _SELECT_ 문을 사용합니다.

```
SELECT *
FROM items
LIMIT 5;
```

* 이것은 _items_ 테이블에서 처음 5개의 레코드를 가져옵니다.
* 결과에는 테이블에 저장된 벡터 열이 포함됩니다.

#### 가장 가까운 벡터 읽기

벡터의 최근접 이웃을 검색하려면 벡터 거리 연산자 또는 거리 함수를 사용할 수 있습니다.

거리 연산자를 사용하는 경우:

```
SELECT * FROM items
ORDER BY embedding <-> '[3,1,2]'
LIMIT 5;
```

* 이 쿼리는 _embedding_ 열의 벡터와 _\[3,1,2]_ 벡터 사이의 L2(유클리드) 거리에 따라 결과를 정렬합니다.

거리 함수를 사용하는 경우:

```
SELECT name
FROM items
ORDER BY l2_distance(embedding, '[3, 1, 2]')
LIMIT 5;
```

* 이 쿼리는 _l2\_distance_ 함수를 사용하여 벡터 간 거리를 계산하고, 최근접 이웃 순으로 정렬합니다.

이 두 쿼리는 기능적으로 동일합니다.

**최근접 이웃 검색에 대한 참고 사항**

* 벡터 인덱스가 없는 경우, **정확한 최근접 이웃** 검색이 수행됩니다.
* 벡터 인덱스가 있으면 검색은 **근사 최근접 이웃 (ANN)** 알고리즘을 사용하여 더 빠른 결과를 제공합니다.

**여러 벡터 인덱스에 대한 참고 사항**

* 단일 벡터 열에 여러 인덱스를 생성할 수 있지만, 각 인덱스는 서로 다른 거리 연산자(e.g., L2 거리, 코사인 유사도)에 해당해야 합니다.
* 하나의 벡터 열은 거리 유형당 하나의 인덱스만 가질 수 있습니다.

### 벡터 인덱스 사용 제어

쿼리 최적화 프로그램이 벡터 인덱스를 사용하거나 우회하도록 영향을 줄 수 있습니다.

* `/*+ VECTOR_INDEX_SCAN (my_col_name) */`: 최적화 프로그램이 _my\_col\_name_ 열의 벡터 인덱스를 사용하도록 강제합니다.
* `/*+ NO_VECTOR_INDEX_SCAN */`: 최적화 프로그램이 어떤 벡터 인덱스도 사용하지 않도록 합니다.

#### 벡터 인덱스 사용 강제화

쿼리에서 벡터 인덱스를 명시적으로 사용하려면, 먼저 _embedding_ 열에 ANN 벡터 인덱스가 존재해야 합니다.

인덱스 생성에 대한 세부 사항은 _벡터 인덱스_ [벡터 인덱스](https://cubvec.github.io/cubvec-spec-ko/vector-index.html) 페이지를 참조하십시오.

```
SELECT /*+ VECTOR_INDEX_SCAN (embedding) */ name
FROM items
ORDER BY l2_distance(embedding, '[3, 1, 2]')
LIMIT 5;
```

* 이 예에서는 _VECTOR\_INDEX\_SCAN_ 힌트를 사용하여 _embedding_ 열의 벡터 인덱스를 강제로 사용합니다.
* 인덱스가 없으면 힌트는 최적화 프로그램에 의해 조용히 무시됩니다.

#### 벡터 인덱스 사용 방지

쿼리에서 벡터 인덱스를 사용하지 않도록 하려면 _NO\_VECTOR\_INDEX\_SCAN_ 힌트를 추가하십시오.

```
SELECT /*+ NO_VECTOR_INDEX_SCAN */ name
FROM items
ORDER BY l2_distance(embedding, '[3, 1, 2]')
LIMIT 5;
```

* 이 방법은 쿼리가 벡터 인덱스를 우회하여 정확한 검색을 수행하도록 강제합니다.

### 벡터 업데이트

테이블에 저장된 벡터를 업데이트하려면 _UPDATE_ 문을 사용합니다.

```
UPDATE items
SET embedding = '[1, 2, 3]'
WHERE id = 1;
```

* 이 예에서는 _id_ 가 1인 행의 _embedding_ 열을 새로운 벡터 [\`](https://cubvec.github.io/cubvec-spec-ko/vector-dml.html#id10)\[1, 2, 3]\`로 업데이트합니다.

### 벡터 삭제

테이블에서 벡터를 삭제하려면 _DELETE_ 문을 사용합니다.

```
DELETE FROM items
WHERE id = 1;
```

* 이 예에서는 _id_ 가 1인 _items_ 테이블의 행을 삭제하며, 해당 벡터 데이터도 함께 삭제됩니다.

## 2026년 확장 사항

이 절은 2026년(3차년도)에 추가된 DML 관련 사용자 스펙을 설명합니다. 기능마다 적용 브랜치를 표시했습니다. 전체 변경 내역은 [변경 이력](revision.md)을 참고하십시오.

### 벡터 인덱스가 있는 테이블의 UPDATE와 DELETE

> 적용 브랜치: `cubvec/m1`

벡터 인덱스가 있는 테이블에서도 UPDATE와 DELETE의 결과가 벡터 검색에 그대로 반영됩니다.

* 벡터 컬럼을 UPDATE하면, 커밋 이후의 검색은 새 벡터로 그 행을 찾습니다. 이전 벡터와 가까운 질의를 해도 그 행이 이전 벡터 기준으로 선택되지 않습니다.
* 행을 DELETE하면, 커밋 이후의 검색 결과에 그 행이 나오지 않습니다.
* 벡터가 아닌 컬럼만 UPDATE하면 벡터 인덱스는 바뀌지 않습니다.
* 여러 행을 대상으로 하는 UPDATE와 DELETE도 같습니다.

```
CREATE TABLE t (id INT, v VECTOR(3), note VARCHAR(20));
CREATE VECTOR INDEX i_t_v ON t (v EUCLIDEAN);

INSERT INTO t VALUES (1, '[1.0, 0.0, 0.0]', 'a');
INSERT INTO t VALUES (2, '[0.0, 1.0, 0.0]', 'b');
COMMIT;

UPDATE t SET v = '[1.0, 1.0, 0.0]' WHERE id = 1;
DELETE FROM t WHERE id = 2;
COMMIT;

-- id = 1이 새 벡터로 검색됩니다.
SELECT id FROM t ORDER BY v <-> '[1.0, 1.0, 0.0]' LIMIT 1;

-- id = 2는 결과에 나오지 않습니다.
SELECT id FROM t ORDER BY v <-> '[0.0, 1.0, 0.0]' LIMIT 2;
```

삭제되거나 갱신된 벡터는 인덱스에서 곧바로 지워지지 않고 삭제 표시만 됩니다. 그래프 노드를 지우려면 그 노드를 가리키는 이웃 목록을 모두 다시 이어야 하는데, 그 비용이 크기 때문입니다. 삭제 표시된 항목은 검색 결과에 나오지 않습니다. 삭제 표시된 항목의 공간 정리는 아직 지원하지 않습니다.

### 트랜잭션 롤백

> 적용 브랜치: `cubvec/m1`

벡터 인덱스가 있는 테이블의 변경을 롤백하면 검색 결과도 변경 전으로 돌아갑니다.

| 롤백한 문장 | 롤백 후 검색 결과 |
| --- | --- |
| INSERT | 삽입한 행이 나오지 않습니다. |
| DELETE | 삭제했던 행이 다시 나옵니다. |
| UPDATE | 이전 벡터로 검색되고, 새 벡터로는 검색되지 않습니다. |

```
;autocommit off
UPDATE t SET v = '[0.0, 0.0, 1.0]' WHERE id = 1;
ROLLBACK;

-- id = 1이 이전 벡터 [1.0, 1.0, 0.0]으로 검색됩니다.
SELECT id FROM t ORDER BY v <-> '[1.0, 1.0, 0.0]' LIMIT 1;
```

### 대량 적재

#### COPY FROM STDIN (FORMAT BINARY)

> 적용 브랜치: `cubvec/m1`, Python 드라이버 `cubvec/tta`

`COPY` 구문은 클라이언트가 보낸 행을 바이너리 형식 그대로 테이블에 넣습니다. 벡터를 문자열로 바꾸지 않으므로 많은 벡터를 빠르게 적재할 수 있습니다.

```
<copy> ::= "COPY" <table_name> ["(" <column_name> {"," <column_name>} ")"]
           "FROM" "STDIN" "WITH" "(" "FORMAT" "BINARY" ")"
```

* 지원하는 컬럼 타입은 INT, BIGINT, FLOAT, DOUBLE, VARCHAR, VECTOR입니다.
* 현재는 Python 드라이버에서 쓸 수 있고, 한 세션 안에서 실행됩니다.

Python 드라이버에서는 `Connection.copy()`가 돌려주는 writer로 행을 보냅니다. `types`에는 행의 각 값 타입을 순서대로 씁니다.

```python
import CUBRIDdb

conn = CUBRIDdb.connect('CUBRID:localhost:33000:demodb:::', 'dba', '')

with conn.copy("COPY items FROM STDIN WITH (FORMAT BINARY)",
               types=["INT", "VECTOR(256)"]) as writer:
    for i, vec in enumerate(vectors):
        writer.write_row((i, vec))

print(writer.rows_loaded)
```

#### loaddb 병렬 적재

> 적용 브랜치: `cubvec/cubvec`, `cubvec/m1`

벡터 인덱스가 있는 테이블에도 `loaddb`의 병렬 적재(`-C`)를 쓸 수 있습니다. 데이터가 들어 있는 테이블에 벡터 인덱스를 만들 때는 서버가 여러 작업자로 벡터를 나누어 인덱스에 넣습니다.

```
cubrid loaddb -s schema_file -d object_file -C -u dba demodb
```

### 드라이버에서 벡터 바인딩

> 적용 브랜치: `cubvec/m1`, Python 드라이버 `cubvec/tta`

CCI와 Python 드라이버는 벡터 타입을 직접 주고받습니다. 질의 벡터를 `'[x, y, z]'` 문자열로 만들지 않고 바인드할 수 있으므로, 질의마다 반복되던 문자열 변환과 파싱이 없어집니다. Python에서는 값을 `CUBRIDdb.Vector`로 감싸 바인드합니다.

```python
import CUBRIDdb

cur = conn.cursor()
cur.execute("SELECT id FROM items ORDER BY embedding <-> ? LIMIT 10",
            (CUBRIDdb.Vector([0.12, 0.33, 0.51]),))
rows = cur.fetchall()
```

