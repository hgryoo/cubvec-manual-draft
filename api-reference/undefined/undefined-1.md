# 벡터 연산

## 벡터 연산

이 페이지는 지원되는 벡터 연산을 설명합니다.

### 개요

#### 기본 벡터 함수

* `vector_dims(vector) -> integer`
* `vector_dimension_count(vector) -> integer`
* `vector_norm(vector) -> double`
* `vector_dimension_format(vector) -> INT8 | FLOAT32 | FLOAT64`
* ☐ TODO: _vector\_dimension\_format_ 출력에 대해 논의 필요

#### 벡터 거리 함수

* `l2_distance(vector1, vector2) -> double`
* `l1_distance(vector1, vector2) -> double`
* `cosine_distance(vector1, vector2) -> double`
* `inner_product(vector1, vector2) -> double`

### 벡터 연산자

#### 기본 벡터 연산자

* `+`: 요소별 덧셈
* `-`: 요소별 뺄셈
* `*`: 요소별 곱셈
* `||`: 연결

#### 거리 연산자

* `<->`: L2 거리
* `<#>`: 음의 내적
* `<=>`: 코사인 거리
* `<+>`: L1 거리

### 명세

#### VECTOR\_DIMS (vector) -> integer

#### VECTOR\_DIMENSION\_COUNT (vector) -> integer

```
VECTOR_DIMS ( EXPR )
VECTOR_DIMENSION_COUNT ( EXPR )
```

* `VECTOR_DIMS` 와 `VECTOR_DIMENSION_COUNT` 는 동일합니다.
* 벡터의 차원 수를 정수로 반환합니다.
* `EXPR` 은 벡터로 평가되어야 합니다.
* `EXPR` 이 NULL인 경우 NULL을 반환합니다.
* ☐ TODO: 정수형(INTEGER)으로 반환할지 아니면 숫자형(NUMBER)으로 반환할지 논의 필요.

#### VECTOR\_NORM (vector) -> double

```
VECTOR_NORM ( EXPR )
```

* 벡터의 크기(노름)를 반환합니다.
* `EXPR` 이 NULL인 경우 NULL을 반환합니다.

#### VECTOR\_DIMENSION\_FORMAT (vector) -> INT8 | FLOAT32 | FLOAT64

```
VECTOR_DIMENSION_FORMAT ( EXPR )
```

* 벡터 요소의 데이터 유형을 반환합니다: `INT8`, `FLOAT32`, 또는 `FLOAT64`.
* [\`\`](https://cubvec.github.io/cubvec-spec-ko/vector-operations.html#id9)EXPR\`\`이 NULL인 경우 NULL을 반환합니다.

### 벡터 거리 함수

* ☐ TODO: 거리 함수가 float 또는 double을 반환해야 하는지 논의 필요.

#### L2\_DISTANCE (vector, vector) -> double

```
L2_DISTANCE ( EXPR1, EXPR2 )
```

* 두 벡터 간의 L2 (유클리드) 거리를 반환합니다.
* 두 표현식은 벡터로 평가되어야 합니다.
* 표현식 중 하나라도 NULL인 경우 NULL을 반환합니다.

#### L1\_DISTANCE (vector, vector) -> double

```
L1_DISTANCE ( EXPR1, EXPR2 )
```

* 두 벡터 간의 L1 (맨해튼) 거리를 반환합니다.
* 두 표현식은 벡터로 평가되어야 합니다.
* 표현식 중 하나라도 NULL인 경우 NULL을 반환합니다.

#### COSINE\_DISTANCE (vector, vector) -> double

```
COSINE_DISTANCE ( EXPR1, EXPR2 )
```

* 두 벡터 간의 코사인 거리를 반환합니다.
* 두 표현식은 벡터로 평가되어야 합니다.
* 표현식 중 하나라도 NULL인 경우 NULL을 반환합니다.

#### INNER\_PRODUCT (vector, vector) -> double

```
INNER_PRODUCT ( EXPR1, EXPR2 )
```

* 두 벡터 간의 내적(점곱)을 반환합니다.
* 두 표현식은 벡터로 평가되어야 합니다.
* 표현식 중 하나라도 NULL인 경우 NULL을 반환합니다.
