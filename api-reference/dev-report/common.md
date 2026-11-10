# 공통

CUBRID의 벡터 서치 기능이 완료될 때까지 관련 레포지토리의 각각 다른 브랜치에서 관리합니다.\
올바른 기능 통합을 위해 다음을 참고합니다.

* CUBRID 엔진: [https://github.com/CUBRID/cubrid/tree/cubvec/cubvec](https://github.com/CUBRID/cubrid/tree/cubvec/cubvec)
  * 2026년 성능 개선과 트랜잭션·복구: [https://github.com/CUBRID/cubrid/tree/cubvec/m1](https://github.com/CUBRID/cubrid/tree/cubvec/m1)
  * 2026년 벤치마크 측정: [https://github.com/CUBRID/cubrid/tree/cubvec/tta](https://github.com/CUBRID/cubrid/tree/cubvec/tta)
* CUBRID 테스트 시스템
  * 테스트 도구: [https://github.com/CUBRID/cubrid-testtools](https://github.com/CUBRID/cubrid-testtools)
  * 테스트 케이스: [https://github.com/CUBRID/cubrid-testcases/tree/cubvec/cubvec](https://github.com/CUBRID/cubrid-testcases/tree/cubvec/cubvec)
  * 테스트 컨테이너 환경: [https://github.com/CUBRID/cubridci/tree/cubvec](https://github.com/CUBRID/cubridci/tree/cubvec)
* CUBRID 드라이버
  * Python: [https://github.com/CUBRID/cubrid-python](https://github.com/CUBRID/cubrid-python) (2026년 벡터 타입 바인딩과 `COPY`: `cubvec/tta` 브랜치)
  * CCI: [https://github.com/CUBRID/cubrid-cci](https://github.com/CUBRID/cubrid-cci) (2026년 벡터 타입: `cubvec/m1` 브랜치)



다음은 CUBRID 테스트를 추가한 ann-benchmarks forked repository이다.

* [https://github.com/cubrid/ann-benchmarks](https://github.com/cubrid/ann-benchmarks) (2026년 측정: `cubvec/tta` 브랜치, [벤치마크](2026/benchmark.md) 참고)
