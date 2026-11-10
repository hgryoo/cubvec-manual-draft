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
