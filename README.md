# MakeMate

### 효율적인 동아리 운영을 위한 팀 빌딩 자동화 서비스

https://www.piromakemate.shop/

개발 기간: 2024/01/30~2024/02/20 (총 22일)

피로그래밍 20기 최종 프로젝트

## 프로젝트 소개

- 피로그래밍 최종 프로젝트 팀빌딩 시 사용할 수 있는 인터널 앱입니다.
- 팀빌딩 그룹을 개설하면 1차, 2차, 3차 투표가 진행됩니다.
- 각 투표 진행 시 참여자들은 아이디어를 올리거나 투표할 수 있습니다.
- 투표가 종료되면 알고리즘에 의해 결정된 팀 빌딩 결과를 운영진에게 제공합니다.
    - 실력과 팀 지망에 따라 알고리즘을 구축하였습니다.
- 운영진은 팀 빌딩 결과를 수정하고 참여자들에게 발표할 수 있습니다.

### UserFlow

![Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/e7addfaa-4f8a-4061-9612-8cbc944b2a76/42fe91b0-34ef-4315-8add-e61520a57b9d/Untitled.png)

## 시연 영상

[MakeMate 시연 영상 링크 (YouTube)](https://youtu.be/6fRprCYuKU4)

https://github.com/Pirogramming-20/MakeMate

## 기술 스택

- FE
    - vanilla javascript
- BE
    - Django
- Deploy
    - nginx/gunicorn
    - AWS EC2
- 라이브러리
    - APScheduler: 함수를 특정 시간에 실행시키기 위해 사용
    - Numpy: N dimension Array 데이터 처리를 위해 사용

## 팀원

| 김연우 (팀장) | 강용현 | 김하영 | 송하종 |
| --- | --- | --- | --- |
| @Yeonu-Kim | @khyeon1003 | @HayoungGloria | @hjsong123 |

## 역할 분담

- 김연우 (팀장)
    - UI/UX 디자인  기획
    - 회원가입/로그인/로그아웃
    - 모임 생성 및 인증
    - 배포
- 강용현
    - 메인 페이지
    - 운영자 페이지
    - 회원 정보 수정
    - 팀 빌딩 알고리즘 구현
    - APScheduler 활용 팀빌딩 함수 실행 관리
- 김하영
    - UI/UX 디자인
    - 투표 생성 및 수정
- 송하종
    - 임시결과 제공 및 수정
    - 결과 발표
    - 권한 인가
    - 팀 빌딩 알고리즘 구현

## 페이지별 기능

### 초기 화면

- 로그인하지 않았을 때
    - 로그인 및 회원가입 버튼이 나타납니다.
- 로그인했을 때
    - 로그아웃 및 모임 개설 버튼이 나타납니다.
    - 내가 속한 모임의 리스트가 나타납니다.

![로그인 전](https://prod-files-secure.s3.us-west-2.amazonaws.com/e7addfaa-4f8a-4061-9612-8cbc944b2a76/25bbaded-a420-43a7-90ef-3888f8bfc459/Untitled.png)

로그인 전

![로그인 후](https://prod-files-secure.s3.us-west-2.amazonaws.com/e7addfaa-4f8a-4061-9612-8cbc944b2a76/994ccd1d-f962-4dc9-8b4f-8ae42191160e/Untitled.png)

로그인 후

![로그인 후 내가 속한 모임 리스트](https://prod-files-secure.s3.us-west-2.amazonaws.com/e7addfaa-4f8a-4061-9612-8cbc944b2a76/86375d5f-bf7b-47d0-aff9-74df13a67b8c/Untitled.png)

로그인 후 내가 속한 모임 리스트

### 로그인/회원가입

- 장고 자체 로그인 및 회원가입 기능을 사용하여 구현하였습니다.
- form 에러 발생 시 field 아래에 에러가 나타나도록 구현했습니다.

![회원가입](https://prod-files-secure.s3.us-west-2.amazonaws.com/e7addfaa-4f8a-4061-9612-8cbc944b2a76/c63f0ada-e3a3-4e70-b005-124bf856f0e7/Untitled.png)

회원가입

![로그인](https://prod-files-secure.s3.us-west-2.amazonaws.com/e7addfaa-4f8a-4061-9612-8cbc944b2a76/2a980cc8-a4d2-44b2-8ca8-3ca3d8327301/Untitled.png)

로그인

![에러 발생 시 경고 문구](https://prod-files-secure.s3.us-west-2.amazonaws.com/e7addfaa-4f8a-4061-9612-8cbc944b2a76/110169b2-8e7a-489b-9a11-8597b840a052/Untitled.png)

에러 발생 시 경고 문구

### 모임 개설 (운영자)

- 총 세 단계를 거쳐 모임을 개설합니다.
    - 1단계: 모임 이름, 비밀번호
    - 2단계: 초기 정보(실력)에 대한 설명
    - 3단계: 1, 2, 3차 투표 마감일
- Ajax를 사용하여 모든 단계를 거쳤을 때만 모임 정보가 DB에 저장될 수 있도록 구현했습니다.
    - 이전 단계로 이동 기능은 아직 구현하지 못했습니다.
- 잘못된 값을 입력했을 경우에는 필드 아래에 에러 메세지가 나타나도록 구현했습니다.
    - 특히 3단계에서는 1차 투표 마감기한 < 2차 투표 마감기한 < 3차 투표 마감기한 조건을 만족하도록 구현하였습니다.
- 모임 개설 이후에는 참여자에게 공유할 링크와 비밀번호를 확인하는 창으로 이동합니다.
- 모임을 개설한 사람은 자동으로 운영자로 등록됩니다.

![모임 개설.gif](https://prod-files-secure.s3.us-west-2.amazonaws.com/e7addfaa-4f8a-4061-9612-8cbc944b2a76/b36e6fb8-eb09-418d-81ab-724d39ed3272/%EB%AA%A8%EC%9E%84_%EA%B0%9C%EC%84%A4.gif)

### 모임 가입 (참여자)

- 제공받은 링크를 통해 들어가면 모임 참여자 확인 창이 나타납니다.
- 비밀번호와 초기 정보(실력)를 입력하면 모임에 가입됩니다.
    - 각 실력에 대한 설명은 “모임 개설” 2단계에서 설정한 값으로 나타납니다.

![모임 가입.gif](https://prod-files-secure.s3.us-west-2.amazonaws.com/e7addfaa-4f8a-4061-9612-8cbc944b2a76/e35e0e14-1bd2-45a8-9e66-b0a1ff33e0dd/%EB%AA%A8%EC%9E%84_%EA%B0%80%EC%9E%85.gif)

### 아이디어 생성/수정/삭제 (참여자)

- 1차 투표
    - 나의 아이디어가 없을 때는 “아이디어 생성” 버튼이 나타납니다.
        - 각자의 팀 프로젝트 아이디어를 생성할 수 있습니다.
        - 발표 자료는 파일 업로드 기능을 사용하여 올릴 수 있습니다. (최대 4M)
    - 다른 사람의 아이디어는 디테일 페이지에서 확인할 수 있습니다.
    - 나의 아이디어가 있으면 “아이디어 수정” 버튼이 나타납니다.

![아이디어 추가.gif](https://prod-files-secure.s3.us-west-2.amazonaws.com/e7addfaa-4f8a-4061-9612-8cbc944b2a76/1151f59c-d647-47ce-a847-c04da2f1eccb/%EC%95%84%EC%9D%B4%EB%94%94%EC%96%B4_%EC%B6%94%EA%B0%80.gif)

- 2, 3차 투표
    - 나의 아이디어가 선정된 경우에는 아이디어를 수정할 수 있습니다.
    - 나의 아이디어가 선정되지 않은 경우에는 아이디어 수정 페이지가 나타나지 않습니다.

### 투표하기 (참여자)

- 자신이 원하는 아이디어에 대해 투표할 수 있습니다.
    - 투표 조건에 맞지 않는 경우 투표 내용이 저장되지 않으며 에러 메세지가 나타납니다.
- 투표 조건
    - 1차 투표: 무지망으로 10개 선정
    - 2차 투표: 무지망으로 5개 선정, 1차 투표에서 선발된 아이디어만 투표 가능
    - 3차 투표: 3지망 투표, 2차 투표에서 선발된 아이디어만 투표 가능
- 투표 이후에는 투표 내용을 수정할 수 있습니다.

![1차 투표하기](https://prod-files-secure.s3.us-west-2.amazonaws.com/e7addfaa-4f8a-4061-9612-8cbc944b2a76/27579d13-9f89-46e7-8095-464599c7c4bf/%ED%88%AC%ED%91%9C%ED%95%98%EA%B8%B0.gif)

1차 투표하기

![1차 투표 수정](https://prod-files-secure.s3.us-west-2.amazonaws.com/e7addfaa-4f8a-4061-9612-8cbc944b2a76/045b4ad1-a782-418e-a669-2942366665e6/%ED%88%AC%ED%91%9C_%EC%88%98%EC%A0%95.gif)

1차 투표 수정

![2차 투표](https://prod-files-secure.s3.us-west-2.amazonaws.com/e7addfaa-4f8a-4061-9612-8cbc944b2a76/facdcf03-17d3-4f54-838e-1a738e9516f5/2%EC%B0%A8_%ED%88%AC%ED%91%9C.gif)

2차 투표

![3차 투표](https://prod-files-secure.s3.us-west-2.amazonaws.com/e7addfaa-4f8a-4061-9612-8cbc944b2a76/2f25d4c3-1620-4b43-bd08-4372d10263bc/3%EC%B0%A8_%ED%88%AC%ED%91%9C.gif)

3차 투표

### 운영자 페이지 (운영자)

- 모임에 가입한 회원의 정보를 수정하거나 아이디어를 삭제할 수 있습니다.
- 운영자/비운영자(참여자) 여부를 수정할 수 있습니다.

![운영진/비운영진 정보 변경](https://prod-files-secure.s3.us-west-2.amazonaws.com/e7addfaa-4f8a-4061-9612-8cbc944b2a76/2545be92-8da0-444b-8c88-dd173028e77a/%EC%9A%B4%EC%98%81%EC%9E%90_%ED%8E%98%EC%9D%B4%EC%A7%80.gif)

운영진/비운영진 정보 변경

![실력 정보 수정](https://prod-files-secure.s3.us-west-2.amazonaws.com/e7addfaa-4f8a-4061-9612-8cbc944b2a76/9a294894-742b-468a-813f-493d940da949/%EC%9A%B4%EC%98%81%EC%9E%90_%ED%8E%98%EC%9D%B4%EC%A7%80_%EC%88%98%EC%A0%95.gif)

실력 정보 수정

### 임시 결과 페이지 (운영자)

- 1차 투표 (아이디어 뽑기)
    - 상위 10개의 팀을 미리 선택해둔 상태에서 운영자가 결과를 수정할 수 있도록 합니다.
    - 아이디어는 투표순으로 나열됩니다.
    - 발표하기 버튼을 누르면 2차 투표가 시작됩니다.

![운영자 임시결과.gif](https://prod-files-secure.s3.us-west-2.amazonaws.com/e7addfaa-4f8a-4061-9612-8cbc944b2a76/14434c7a-a37b-4205-a17a-2a9da629753c/%EC%9A%B4%EC%98%81%EC%9E%90_%EC%9E%84%EC%8B%9C%EA%B2%B0%EA%B3%BC.gif)

- 2차 투표 (아이디어 뽑기)
    - 상위 5개 팀을 미리 선택해둔 상태에서 운영자가 결과를 수정할 수 있도록 합니다.
    - 발표하기 버튼을 누르면 3차 투표가 시작됩니다.

![2차 임시결과.gif](https://prod-files-secure.s3.us-west-2.amazonaws.com/e7addfaa-4f8a-4061-9612-8cbc944b2a76/b7cc492c-9a8b-46fb-b219-b0b8eecefbc1/2%EC%B0%A8_%EC%9E%84%EC%8B%9C%EA%B2%B0%EA%B3%BC.gif)

- 3차 투표 (팀원 변경하기)
    - 팀원의 실력, 지망에 따라 알고리즘에 의해 결정된 결과를 운영진에게 제공합니다.
    - 팀원 정보를 수정할 수 있습니다.

![3차 임시결과.gif](https://prod-files-secure.s3.us-west-2.amazonaws.com/e7addfaa-4f8a-4061-9612-8cbc944b2a76/49b7475c-411b-40c0-b93d-d37b14b5d9c1/3%EC%B0%A8_%EC%9E%84%EC%8B%9C%EA%B2%B0%EA%B3%BC.gif)

### 임시 결과 페이지 (참여자)

- 투표가 종료된 이후에는 “투표하기” 버튼이 나타나지 않습니다.

### 결과 페이지

- 최종 팀빌딩 결과를 보여줍니다.

![Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/e7addfaa-4f8a-4061-9612-8cbc944b2a76/838b6998-106b-4b86-a9b6-50e69a5df3e2/Untitled.png)

## 구현 디테일

### 팀 빌딩 알고리즘

- 팀빌딩 방식
    - 수식을 사용하여 각 팀의 적합도 점수를 계산합니다.
    - 각 팀의 적합도 최대 값을 가진 회원을 선정합니다.
    - 최대 값을 가진 회원 중 적합도 점수가 최소인 회원에 대해 먼저 팀을 할당합니다.
    - 해당 방식을 반복하여 팀빌딩을 마무리합니다.
- 팀 빌딩 함수는 3차 투표가 마무리되는 시점에 1회만 시행됩니다. (APScheduler 사용)
    - 이러한 방식을 통해 서버 부하를 줄입니다.

![Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/e7addfaa-4f8a-4061-9612-8cbc944b2a76/aa755bf8-6fe3-49ec-b8cc-71bb5dc13203/Untitled.png)

### 권한 인가

- 로그인/비로그인, 참여자/운영자, 투표 중/투표 종료에 따라 페이지 접근 가능 유무가 달라집니다.
- 링크로 권한이 없는 유저가 접근하는 경우, 각 유저가 접근할 수 있는 페이지로 리다이렉트 시킵니다.