---
icon: terminal
layout:
  width: default
  title:
    visible: true
  description:
    visible: true
  tableOfContents:
    visible: true
  outline:
    visible: true
  pagination:
    visible: false
  metadata:
    visible: true
  tags:
    visible: true
  actions:
    visible: true
  anchors:
    visible: true
metaLinks:
  alternates:
    - /broken/spaces/M9ty6FYa3j98VSBHF9LN/pages/trLwwmumlaofzMKwR3fr
---

# CUBRID 벡터 서치 개발 리포트

본 문서는 **CUBRID DBMS에 벡터 데이터 타입과 벡터 검색(Vector Search) 기능을 도입한 전체 개발 이력 및 사용 매뉴얼**을 통합하여 제공하기 위해 작성되었다.

***

### **Document Purpose**

본 문서는 다음을 목적으로 한다:

1. **사용자 가이드 제공**
   * SQL을 이용한 벡터 데이터 처리 방법
   * 벡터 인덱스 생성 및 검색 기능 사용법
2. **개발자·기여자를 위한 기술 설명**
   * CUBRID 내부 모듈 구조
   * HNSW 기반 벡터 인덱스 설계
   * 저장소(storage) 추상화 및 trait 기반 템플릿 구조
   * 메모리/디스크 백엔드 구조
   * 질의 실행기와 옵티마이저 연동 방식
3. **프로젝트 기록 및 공유**
   * 개발 과정 기록 및 이력화
   * 팀 내부 공유 및 외부 기술 참고 제공
   * 새로운 기여자 온보딩 가이드

***

### **Target Audience**

* CUBRID 사용자
* CUBRID 개발자 및 기여자
* 벡터 검색(ANN) 기술에 관심 있는 연구자
* 기업 내부 벡터 기반 AI 시스템 구축 엔지니어
* SQL 기반 벡터 검색 기능을 활용하려는 일반 사용자

***

