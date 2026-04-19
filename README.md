# 👂 Audiology-AI-Agent

> **청력도(Audiogram) 및 이명도 데이터를 기반으로 한 개인 맞춤형 청능 재활 상담 에이전트**

본 프로젝트는 전문적인 청능 재활 지식을 LLM(GPT-4o)에 결합하여, 사용자의 검사 결과에 따른 정밀한 상태 분석과 의학적 근거 중심의 조언을 제공하는 AI 상담 시스템입니다.

---

## 🎯 주요 기능 (Key Features)

- **데이터 기반 맞춤형 상담:** 사용자가 입력한 주파수별 청력 수치 및 이명 데이터를 바탕으로 현재 상태를 정밀 분석합니다.
- **구조화된 정보 제공 (JSON Parsing):** 챗봇의 응답을 JSON 형식으로 강제하여 '상태 요약', '권장 조치', '💡 추천' 섹션으로 체계적으로 출력합니다.
- **전문적 상담 페르소나:** '전문 청능 재활 상담사' 역할을 부여하여 신뢰도 높은 상담 톤앤매너를 유지합니다.
- **학술 데이터 연동:** Google Scholar 등의 외부 학술 자료를 참고하여 답변의 전문성을 높이도록 프롬프트를 설계했습니다.
- **실시간 대화 관리:** 세션 상태(Session State)를 활용하여 대화 흐름을 유지하고 토큰 사용량을 최적화합니다.

## 🛠 기술 스택 (Tech Stack)

### **AI & Backend**
- ![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
- ![OpenAI](https://img.shields.io/badge/OpenAI-412991?style=for-the-badge&logo=openai&logoColor=white) (GPT-4o 모델 활용)
- ![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=Streamlit&logoColor=white)

### **Key Modules**
- **`chatbot.py`**: OpenAI API 연동, 대화 히스토리 관리 및 클래스 기반 챗봇 로직 구현.
- **`project_audiologist.py`**: Streamlit을 활용한 웹 인터페이스 구축 및 사용자 데이터 세션 관리.

---

## 📊 시스템 아키텍처 (System Architecture)



1. **사용자 입력:** 청력도 데이터 및 주관적 증상 입력.
2. **프롬프트 엔지니어링:** 시스템 프롬프트(청각학 가이드라인) + 사용자 데이터 결합.
3. **LLM 추론:** OpenAI GPT-4o를 통한 분석 및 상담 내용 생성.
4. **결과 시각화:** JSON 파싱을 통해 Streamlit 화면에 영역별 가독성 높은 UI로 출력.

---

## 📂 파일 구조 (File Structure)

## 📂 파일 구조 (File Structure)

- [📄 project_audiologist.py](./project_audiologist.py): 전체 애플리케이션의 메인 실행 파일 및 UI 레이아웃 정의.
- [⚙️ chatbot.py](./chatbot.py): `ChatBot` 클래스를 포함한 핵심 비즈니스 로직 모듈.
---
