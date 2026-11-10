# DDL

기존 CUBRID의 DDL 문법을 통해 벡터 컬럼을 포함한 테이블을 생성할 수 있습니다.

#### 벡터 컬럼이 있는 테이블 생성

```
CREATE TABLE items (
  host_year INT NOT NULL PRIMARY KEY,
  embedding vector(3)
);
```

이 예시는 기본 키 _host\_year_ 와 3차원 벡터 _embedding_ 컬럼을 가진 _items_ 라는 테이블을 생성합니다.

#### 벡터 컬럼 추가를 위한 테이블 변경

```
ALTER TABLE items
ADD COLUMN embedding vector(3);
```

이 예시는 기존 _items_ 테이블에 3차원 벡터 _embedding_ 컬럼을 추가합니다.

#### 추가 예시: 이진 벡터 (TODO)

```
CREATE TABLE binary_items (
  item_id INT NOT NULL PRIMARY KEY,
  binary_embedding vector(binary, 512)
);
```
