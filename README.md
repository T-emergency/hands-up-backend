![header](https://capsule-render.vercel.app/api?text=Hands-%up👋!&animation=fadeIn )

## :star2: 거래 물품 경매플랫폼

## 👨‍👨‍👧‍👦 팀원 소개

<br>

**Gyeung Min Kim**

- 🐯Github: [https://github.com/KimGyeongMin-KR]

**Won Chae Yi**

- 🐰Github: [https://github.com/won-Yi]

**Jun Ho Hyeon**

- 🐴Github : [https://github.com/lucius-hyeon]

**Ki Hoon Kang**

- 🐔Github: [https://github.com/kihoongit]

**Min Su Kim**

- 🐶Github : [https://github.com/tikitaka205]

**Sang Hun Son**

- 🐷Github: [https://github.com/son950610]

## 📌 팀 프로젝트 기능 역할분담

경민 -  실시간 채팅 경매, 휴대폰 인증

민수 - 판매자 정보, 신고 기능

원채 - 마이 페이지, 경매 리스트&상품 등록

준호 - 실시간 채팅 경매, 경매 리스트

상훈, 기훈 - 커뮤니티 (자유,제보게시판)

## 📆 프로젝트 개요

![Untitled (4)](https://user-images.githubusercontent.com/113076031/209550003-7bcda95c-0824-497c-8728-afe0003cf062.png)

<br>

- 🕒**진행 기간**: 2022.11.30 ~ 2022.12.29

<br>

- **목표**

  - 온라인으로 서로의 물품을 경매로 내놓아서 보다 저렴하게 물건을 사고 팔 수 있게한다.
  - 소비자가 원하는 가격에 빠르게 물품을 판매할 수 있다.
  - 경매마감의 타임어택시간을 주어서 사이트에 참여유도 및 흥미유발을 만든다.
<br>  

- **🖼 와이어프레임**
  - ![넹](https://user-images.githubusercontent.com/113076031/209619133-3e7e44d3-8d2a-4c74-8820-0f11a4f49221.png)


<br>

- **🎬 프로젝트 시연영상**
  - <a href=" ">시연영상</a>
  
<br>


## ✍ 프로젝트 소개
  - **'Hands-up 👋'** 은 온라인으로 경매로 자신의 물품을 손쉽게 거래하는 플랫폼입니다.
  
  "더이상 필요치않는 본인의 물품이 집에 남아있으신가요?"
  <br>
  "서로 간 가격흥정의 에너지를 쏟고 계신가요?"
  <br>
  "짧은시간내에 빠르게 본인의 물품을 팔아치우시고 싶으신가요?"
  
  자신의 중고물품들을 타인과 거래하면서 빠르게 팔리지않는 것과 타인이 원하는 가격에 있어서 가격흥정에 에너지낭비를 하기에 만들어진 
  저희 **'Hands-up 👋'** 은 사용자분들께서 사용하지않는 아까운 물품들을 빠른경매를 통해 판매를 촉진하게 합니다.
  안전한 본인인증절차를 거쳐 범죄의 위험성을 낮추고 채팅기능으로 판매자와 입찰자간에 경매물품에 대한 궁금한 점을 해소시킵니다.
  
  
  
<br>

## ⭐️ 주요 기능


### 거래할 물품 경매 이용

### 평점 및 리뷰

### 자유 & 제보게시판

> 

### 👩‍❤️‍👨 유저 피드백 반영
피드백 기간 : 22.12.20 ~ 22.12.23
<br>
피드백 응답 수 : 59개
<br>
피드백 반영하기 : ~ 12/27(화)
<br>
- 프로젝트 리펙토링 진행

<br>

## :grey_question: 서비스 아키텍쳐

![hands-up System Architecture drawio (5)](https://user-images.githubusercontent.com/113076031/209558990-1cd4a69f-10d0-43e4-b13b-6a179012ed0d.png)


<br>


<br>

## ⚙​ 개발 환경 및 IDE

- django version 4.1.3
- Docker version 20.10.12
- python version 3.10.8
- django restframework version 3.13.0

<br>

## :hammer:기술 선정 Why ?
 
#### Django / DRF
- Serializer, 유저 관리, REST API 등 Django에서 제공하는 다양한 기능들을 사용하기 위해 채용

#### Django Channels
- 실시간 비동기로 들어오는 ws/wss 프로토콜을 장고에서 대응하기 위해 사용

#### Django Rest Framework simple-jwt
- 유저 인증을 토큰방식으로 암호화하기 위해 사용

#### Websocket
- 실시간 채팅 기능 구현에 있어 채팅을 칠 때마다 매번 HTTP 통신을 하는 것은 느리고 비효율적이기 때문에 실시간 비동기 프로토콜을 제공하는 웹소켓 기술을 사용

#### AWS EC2
- 용량을 줄이거나 늘릴 수 있는 탄력성을 가지고 있고, 보안 및 네트워크 구성, 스토리지 관리에 효과적이며 간단한 프로젝트 배포를 프리티어로 무료로 이용할 수 있다는 점에서 채용

#### AWS S3
- 서비스에서 이미지를 업로드 할때, EC2에 저장을 하게되면 용량이 부족해지고 파일들을 관리하기가 어렵습니다. 그래서 파일 저장에 최적화 되어있고, 저장용량이 무한대에 가까운 S3를 사용해서 이미지 파일들을 저장하고 관리 했습니다.

#### Docker
- Docker는 소프트웨어를 컨테이너라는 표준화된 유닛으로 패키징하는데, 컨테이너에는 라이브러리, 시스템 도구, 코드, 런타임 등 소프트웨어를 실행하는데 필요한 모든것이 포함되어 있습니다. 이러한 특징을 가진 Docker를 활용해서 환경에 구애받지 않고 애플리케이션을 신속하게 배포 및 확장하고 규모가 달라져도 안정적으로 저렴하게 애플리케이션을 구축, 제공 및 실행 하기위해 사용했습니다.

#### Nginx
- event-driven의 비동기 구조인 특징을 가지고 있는 nginx는 채팅기능 때문에 동시접속자 수의 증가에 대응하기에 적합한 방식의 웹서버라고 생각했습니다. 또한 무중단 배포가 가능하여 채팅기능이 있는 웹사이트에서 배포시 중단되지 않는점이 사용자들에게 사용성 및 편의성을 증대시킵니다.

#### Gunicorn
- 로컬개발환경에서는 django의 runserver를 사용하여 gunicorn이 없어도 유용하게 사용 할 수 있지만, 배포환경에서는 runserver를 사용하지 않도록 django에서도 권장되어있습니다. 그래서 Python WSGI 대표적으로 성능이 검증된 Gunicorn을 활용해서 Nginx로부터 받은 서버사이드 요청을 gunicorn을 활용해서 django로 전달하게끔 했습니다.

#### Daphne
- Gunicorn이 WSGI HTTP요청을 처리한다면 저희 서비스에 있는 채팅기능은 ASGI WS 요청을 처리해야 합니다. Daphne는 Channels 를 설치하면 자동으로 설치되며 Channels에서 지원하는 서버로 ASGI 프로토콜로 받은 WS요청을 처리하려고 사용했습니다.

#### PostgreSQL
- PostgreSQL은 MySQL보다 표준에 더 가깝게 구현하는것을 목표로 두고있고, 오픈소스 및 커뮤니티가 이끄는 데이터베이스 입니다. django에서 가장 권장하는 RDBMS가 PostgreSQL이었기 때문에 이를 직접 사용해봄으로써 MySQL과는 어떠한 차이점이 있는지 공부도 하고, 다른 RDBMS를 사용해봄으로써 경험치를 쌓고자 사용했습니다.

## 🌐 Server Description

- port (nginx)

  - | 443  | server default(https)                  |
    | ---- | -------------------------------------- |
    | 80   | server default(http) (redirect to 443) |
    | 6379 | redis(ws)|
    | 8080 | asgi server|
    | 8000 | wsgi server|



## 🎞 최종산출물

<a href=" ">최종 발표 시연영상</a>

<br>
<a href=" ">'Hands-up👋' 최종발표 pdf</a>







