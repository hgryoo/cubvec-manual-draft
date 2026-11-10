# 벡터 데이터

이 섹션은 벡터 데이터타입에 대한 선언 방법을 설명합니다.

```
vector -- `vector (2000)` 과 동일

vector(512) -- 512차원 `float32` 벡터

vector(float64, 128) -- 128차원 `float64` 벡터
```

### BNF

```
<declaration> ::= "vector" [ "(" [ <vector_type> "," ] <dim> ")" ]
<vector_type> ::= "float32"
<dim> ::= <positive_integer>
<positive_integer> ::= {digit}+
```

* `<dim>` 은 양의 정수 값입니다:
  * _\<vector\_type>_ 가 `float32` 일 때 1에서 2000 사이.
  * _\<vector\_type>_ 가 `float64` 일 때 1에서 1000 사이.
  * _\<vector\_type>_ 가 `binary` 일 때 1에서 64000 사이.

> 현재 float32 타입만 제공하며, 이후 quantization 타입 등의 확장에 따라 변경될 예정

#### 벡터 타입 사양

* _vector_ 데이터 타입은 고정 크기의 다차원 배열로, 부동소수점 숫자 또는 이진값을 저장할 수 있습니다.
* 타입이 지정되지 않은 경우 기본 벡터 타입은 `float32` 입니다.
* 차원은 타입 뒤에 괄호 안에 지정됩니다.

**차원 제한**

* `float32` 타입 벡터의 경우 차원은 1에서 2000 사이여야 합니다.
* `float64` 타입 벡터의 경우 차원은 1에서 1000 사이여야 합니다.
* 이진 벡터의 경우 차원은 1에서 64000 사이여야 합니다.

#### 선언 예시

1.  **기본 벡터 (float32)**

    ```
    vector -- `vector (2000)` 과 동일
    ```
2.  **512차원 벡터 (float32)**

    ```
    vector(512)
    ```
3.  **128차원 벡터 (float64)**

    ```
    vector(float64, 128)
    ```
