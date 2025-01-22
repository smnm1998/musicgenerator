# Melodify: AI 기반 음악 생성 웹 애플리케이션

## 프로젝트 요약
Melodify는 사용자가 이미지를 업로드하면 해당 이미지의 분위기와 내용을 기반으로 캡셔닝을 생성하고, 이를 활용하여 맞춤형 음악을 생성하는 AI 기반 웹 애플리케이션입니다. 이 프로젝트는 Django 백엔드와 Google Cloud Platform(GCP)의 Vertex AI를 활용하여 다수의 사용자가 동시에 접근할 수 있는 안정적이고 확장 가능한 서비스를 제공합니다.

---

## 프로젝트 배경
기존의 이미지 생성 서비스는 비주얼 중심의 콘텐츠 제공에 초점이 맞춰져 있었습니다. Melodify는 이미지의 감성과 분위기를 음악으로 표현하여 새로운 방식의 창작 경험을 제공합니다. 이 프로젝트는 창작자, 디자이너, 음악 애호가들이 영감을 얻고 창작 활동을 확장할 수 있도록 돕기 위해 설계되었습니다.

---

## 프로젝트 주요 화면

### 팀 멤버
<p align="center">
  <img src="./portfolio_images/member.png" alt="팀 멤버" width="30%">
</p>

### 구현 화면
<table style="width:100%; text-align:center;">
  <tr>
    <td>
      <br>
      <p align="center">
        <img src="./portfolio_images/upload_page.png" alt="업로드 페이지" width="40%">
      </p>
        <br><업로드 페이지><br>사용자가 이미지를 업로드하고, 음악 생성 작업을 시작할 수 있는 페이지입니다.
    </td>
    <td>
      <br>
      <p align="center">
        <img src="./portfolio_images/loading_page.png" alt="로딩 페이지" width="40%">
      </p>
        <br><로딩 페이지><br>음악 생성 작업 중 상태를 보여주는 페이지입니다.
    </td>
    <td>
      <br>
      <p align="center">
        <img src="./portfolio_images/result_page.png" alt="결과 페이지" width="40%">
      </p> 
        <br><결과 페이지><br>생성된 음악을 실시간으로 재생하고 다운로드할 수 있는 페이지입니다.
    </td>
  </tr>
</table>

---
    
## 주요 기능

1. **이미지 업로드 및 저장**
   - 사용자로부터 이미지를 업로드받아 Google Cloud Storage(GCS)에 안전하게 저장합니다.
   - 이미지 처리 속도와 안정성을 위해 비동기 작업 구조를 채택했습니다.

2. **이미지 캡셔닝 생성**
   - OpenAI API를 사용하여 업로드된 이미지의 분위기와 내용을 분석하고, 이를 기반으로 적절한 캡션을 생성합니다.
   - 생성된 캡션은 음악 생성 파이프라인의 입력 데이터로 활용됩니다.

3. **음악 생성**
   - GCP Vertex AI의 머신러닝 모델을 활용하여 자동으로 음악을 생성합니다.
   - 생성 과정은 GCP의 파이프라인을 통해 효율적으로 관리됩니다.

4. **결과 페이지 제공**
   - 생성된 음악을 웹 인터페이스에서 실시간으로 재생하고, 다운로드할 수 있는 옵션을 제공합니다.
   - 사용자 경험을 고려한 직관적인 UI를 설계했습니다.

---

## 🛠 사용 기술 및 라이브러리

- **프론트엔드**: HTML, CSS, JavaScript
- **백엔드**: Django, Django REST Framework
- **AI 및 머신러닝**:
  - OpenAI API: 이미지 캡셔닝 생성
  - GCP Vertex AI: 음악 생성 파이프라인
- **클라우드 및 배포**:
  - Google Cloud Storage: 이미지 및 음악 파일 저장
  - GCP CICD: 자동화된 모델 배포

---

## 🖥 담당한 기능 (FrontEnd)

- 이미지 업로드 및 미리보기 기능
  - 이미지 업로드 시 업로드 된 사진 미리보기 기능 구현
  - 미리보기 시 다시 입력하기와 업로드하기 버튼이 출력되는 로직 구현 

- 로딩 창
    
- 결과 페이지
  - CD 플레이어 style 퍼블리싱
  - 재생, 10초 되감기-넘어가기 기능 구현
  - 공유하기 기능 구현

---

## 💡 성장한 부분

- **FE 개발**
  - `z-index`를 적용한 원을 여러개 겹쳐서 CD 플레이어 처럼 보이도록 하였습니다.
  - `keyframes`를 이용하여 시계방향으로 돌아가도록 하였습니다.
  - `innerHTML`을 통해 사진 업로드 후에 다른 버튼이 나오는 로직을 구현 하였습니다.
  - 로딩 창을 구현하였습니다.

- **AI와 클라우드**
  - 주피터 노트북을 통한 AI 코드 작성 및 적용하는 방법을 배웠습니다.
  - Google Cloud Platform을 통해 스토리지, 서버, 클라우드 런, shell 기반 서버 배포하는 방법 등 전반적인 클라우드 기능 활용법을 배웠습니다.

- **협업**
  - 주기적인 팀 회의를 통해 진행도를 파악하여 서로가 서로를 도와줌으로써 시너지를 더 발휘하였습니다. 
    
---


## 참고 자료
- [발표 자료 PDF 보기](./portfolio_images/Melodify.pdf)

---

### 문의
궁금한 사항은 이메일로 연락해주세요: [jhs789654123@gmail.com]
