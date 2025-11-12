# Prompt Extraction CLI

이 프로젝트는 LangChain을 이용해 자연어 프롬프트를 구조화된 쿼리(JSON)로 변환하는 CLI 파일입니다. 

## 환경 설정

1. 프로젝트 루트에 **`.env` 파일**을 생성하세요.
2. 다음 내용을 추가하고, 본인의 OpenAI API 키를 입력하세요.
  파일 형식 : OPENAI_API_KEY=sk-여기에_본인_API_KEY_입력
## 실행 
python prompt_input.py


## 주의

.env 파일은 절대 깃허브에 커밋하지 마세요.
Push Protection이 활성화된 저장소에서는 .env에 포함된 키가 감지되면 푸시가 거부됩니다.
