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

