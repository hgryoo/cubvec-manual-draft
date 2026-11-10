# 변경 이력

이 페이지는 CUBRID 벡터 검색 기능의 사용자 스펙 변경을 연도별로 정리합니다. 각 항목의 적용 브랜치는 [CUBRID 저장소](https://github.com/CUBRID/cubrid)의 브랜치 이름이며, 관련 이슈는 [CUBVEC 프로젝트](https://jira.cubrid.org/projects/CUBVEC/issues)에서 볼 수 있습니다.

### 2026년 (3차년도)

| 구분 | 변경 내용 | 적용 브랜치 | 관련 이슈 | 매뉴얼 |
| --- | --- | --- | --- | --- |
| DDL | `CREATE INDEX … USING btree \| hnsw` 구문을 추가했습니다. 컬럼 뒤에 메트릭을 쓰면 벡터 인덱스이고, `USING`을 생략하면 `hnsw`입니다. `CREATE VECTOR INDEX`는 이전 구문으로 계속 쓸 수 있습니다. | `cubvec/cubvec` | [CUBVEC-137](https://jira.cubrid.org/browse/CUBVEC-137) | [벡터 인덱스 지원](vector-index.md) |
| DDL | 벡터 인덱스 구문 오류를 구문 검사 단계에서 알려 줍니다(지원하지 않는 알고리즘, 메트릭 누락·오용, UNIQUE·REVERSE·ONLINE·DEDUPLICATE·부분 인덱스, B-tree의 빌드 옵션). | `cubvec/cubvec` | [CUBVEC-137](https://jira.cubrid.org/browse/CUBVEC-137) | [벡터 인덱스 지원](vector-index.md) |
| 저장 | 벡터 인덱스의 그래프를 디스크 페이지에 저장합니다. 인덱스를 삭제하면 인덱스 파일도 제거됩니다. | `cubvec/cubvec` | [CUBVEC-130](https://jira.cubrid.org/browse/CUBVEC-130) | [벡터 인덱스 지원](vector-index.md) |
| 저장 | 서버를 다시 시작해도 벡터 인덱스를 다시 만들 필요가 없습니다. | `cubvec/m1` | [CUBVEC-188](https://jira.cubrid.org/browse/CUBVEC-188) | [벡터 인덱스 지원](vector-index.md) |
| 카탈로그 | 벡터 인덱스가 `_db_index`에 나옵니다(인덱스 이름, 키 개수, 키 속성, 주석). B-tree 통계에는 B-tree 인덱스만 들어갑니다. | `cubvec/cubvec` | [CUBVEC-142](https://jira.cubrid.org/browse/CUBVEC-142), [CUBVEC-144](https://jira.cubrid.org/browse/CUBVEC-144) | |
| DML | 벡터 인덱스가 있는 테이블의 UPDATE와 DELETE가 벡터 검색에 반영됩니다. | `cubvec/m1` | [CUBVEC-185](https://jira.cubrid.org/browse/CUBVEC-185) | [DML](dml.md) |
| 트랜잭션 | INSERT, UPDATE, DELETE를 롤백하면 벡터 검색 결과도 되돌아갑니다. 커밋한 변경은 장애 복구 후에도 남습니다. | `cubvec/m1` | [CUBVEC-180](https://jira.cubrid.org/browse/CUBVEC-180), [CUBVEC-186](https://jira.cubrid.org/browse/CUBVEC-186) | [DML](dml.md), [벡터 인덱스 지원](vector-index.md) |
| 트랜잭션 | 여러 세션이 같은 벡터 인덱스에 동시에 INSERT, UPDATE, DELETE를 실행할 수 있습니다. | `cubvec/m1` | [CUBVEC-183](https://jira.cubrid.org/browse/CUBVEC-183) | [벡터 인덱스 지원](vector-index.md) |
| 적재 | `COPY … FROM STDIN WITH (FORMAT BINARY)` 구문을 추가했습니다. | `cubvec/m1`, Python `cubvec/tta` | [CUBVEC-86](https://jira.cubrid.org/browse/CUBVEC-86) | [DML](dml.md) |
| 적재 | 데이터가 있는 테이블에 벡터 인덱스를 만들 때 여러 작업자로 병렬 입력합니다. `loaddb -C` 병렬 적재가 벡터 인덱스에서도 동작합니다. | `cubvec/cubvec` | [CUBVEC-152](https://jira.cubrid.org/browse/CUBVEC-152), [CUBVEC-154](https://jira.cubrid.org/browse/CUBVEC-154) | [DML](dml.md) |
| 드라이버 | CCI와 Python 드라이버가 벡터 타입을 직접 바인드합니다(Python: `CUBRIDdb.Vector`). | `cubvec/m1`, Python `cubvec/tta` | [CUBVEC-176](https://jira.cubrid.org/browse/CUBVEC-176) | [DML](dml.md) |
| 통계 | `statdump`에 HNSW 통계를 추가했습니다(방문 노드, 거리 계산, 후보 큐, 페이지·벡터 접근, 캐시 적중, 레벨 0 통계). | `cubvec/cubvec`, `cubvec/m1` | [CUBVEC-162](https://jira.cubrid.org/browse/CUBVEC-162), [CUBVEC-171](https://jira.cubrid.org/browse/CUBVEC-171), [CUBVEC-172](https://jira.cubrid.org/browse/CUBVEC-172) | [벡터 인덱스 지원](vector-index.md) |
| 호환성 | 벡터 데이터를 64바이트 경계에 맞춰 저장하도록 저장 형식이 바뀌었습니다. 이전 빌드에서 벡터를 입력한 데이터베이스는 그대로 쓸 수 없으므로 다시 만들어야 합니다. | `cubvec/m1` | [CUBVEC-177](https://jira.cubrid.org/browse/CUBVEC-177) | |
| 빌드 | Faiss, OpenBLAS, usearch 의존성을 제거했습니다. 거리 함수와 HNSW는 자체 구현을 씁니다. | `cubvec/cubvec` | [CUBVEC-160](https://jira.cubrid.org/browse/CUBVEC-160), [CUBVEC-168](https://jira.cubrid.org/browse/CUBVEC-168) | |

현재 제약 사항은 [벡터 인덱스 지원](vector-index.md)의 "트랜잭션과 장애 복구"에 정리되어 있습니다.

### 2025년 (2차년도)

| 구분 | 변경 내용 | 관련 이슈 |
| --- | --- | --- |
| 타입 | `VECTOR` 타입을 추가했습니다. 벡터 값은 `'[x, y, z]'` 문자열로 입력하고 조회합니다. | [CUBVEC-2](https://jira.cubrid.org/browse/CUBVEC-2) |
| 함수 | 거리 함수 `l2_distance`, `l1_distance`, `cosine_distance`, `inner_product`, `vector_distance`를 추가했습니다. | [CUBVEC-18](https://jira.cubrid.org/browse/CUBVEC-18) |
| 연산자 | 거리 연산자 `<->`(L2), `<#>`(음의 내적), `<c>`(코사인), `<+>`(L1)를 추가했습니다. 코사인 연산자는 CUBRID의 기존 `<=>`(NULL-safe 비교)와 겹치지 않도록 `<c>`를 씁니다. | [CUBVEC-29](https://jira.cubrid.org/browse/CUBVEC-29), [CUBVEC-66](https://jira.cubrid.org/browse/CUBVEC-66) |
| DDL | `CREATE VECTOR INDEX … ON t (col metric) WITH (m = …, ef_construction = …)` 구문을 추가했습니다. | [CUBVEC-16](https://jira.cubrid.org/browse/CUBVEC-16), [CUBVEC-73](https://jira.cubrid.org/browse/CUBVEC-73) |
| 검색 | `ORDER BY 거리 LIMIT k` 질의가 벡터 인덱스 스캔을 쓰며, 정렬 단계를 따로 두지 않습니다. 검색 조건에 호스트 변수와 세션 변수를 쓸 수 있습니다. | [CUBVEC-71](https://jira.cubrid.org/browse/CUBVEC-71), [CUBVEC-97](https://jira.cubrid.org/browse/CUBVEC-97), [CUBVEC-122](https://jira.cubrid.org/browse/CUBVEC-122), [CUBVEC-127](https://jira.cubrid.org/browse/CUBVEC-127) |
| 파라미터 | 시스템 파라미터 `hnsw_ef_search`를 추가했습니다(기본값 40). | [CUBVEC-74](https://jira.cubrid.org/browse/CUBVEC-74) |
| 적재 | `loaddb`가 ann-benchmarks의 HDF5 파일을 읽어 벡터 데이터를 적재합니다. | [CUBVEC-46](https://jira.cubrid.org/browse/CUBVEC-46) |
