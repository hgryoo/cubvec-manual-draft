# Table of contents

* [CUBRID 벡터 서치 개발 리포트](README.md)

## 매뉴얼

* [벡터 데이터](undefined/undefined.md)
* [벡터 연산](undefined/undefined-1.md)
* [DDL](undefined/ddl.md)
* [DML](undefined/dml.md)
* [벡터 인덱스 지원](undefined/undefined-2.md)
* [변경 이력](undefined/revision.md)

## 개발리포트

* [공통](undefined-1/undefined.md)
* [2025](undefined-1/2025.md)
* [2026](undefined-1/2026/README.md)
  * [디스크 기반 벡터 인덱스 구조](undefined-1/2026/disk-vector-index.md)
  * [동시성 제어와 트랜잭션·복구](undefined-1/2026/transaction-recovery.md)
  * [벡터 인덱스 기반 검색 질의](undefined-1/2026/vector-search-query.md)
  * [벤치마크 (CUBRID ann-benchmarks)](undefined-1/2026/benchmark.md)
  * [검증](undefined-1/2026/verification.md)

## Reference

* ```yaml
  props:
    models: false
  type: builtin:openapi
  dependencies:
    spec:
      ref:
        kind: openapi
        spec: gitbook-petstore
  ```
