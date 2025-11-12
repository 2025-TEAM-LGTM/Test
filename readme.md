# AI 기반 팀 모집 공고 검색기 (LangChain + MySQL)

이 프로젝트는 자연어 입력을 기반으로 팀 모집 공고를 자동 검색하는 시스템입니다.  
사용자가 "AI 분야 공모전 중 11월 접수, 백엔드 구함"처럼 문장으로 입력하면,  
LangChain이 조건을 구조화(JSON)로 변환하고 MySQL 데이터베이스에서 자동으로 검색합니다.

## 환경 설정
### 1. 필수 설치

~~~ bash
pip install -r requirements.txt
~~~

### 2. `.env` 파일 생성 
프로젝트 루트에 .env 파일을 만들고 아래 내용 추가:

~~~ bash
# OpenAI API Key
OPENAI_API_KEY=sk-여기에_본인_API_KEY_입력

# DB 설정
DB_HOST=127.0.0.1
DB_PORT=3306
DB_USER=root
DB_PASSWORD=비밀번호
DB_NAME=union_test

~~~

주의 !!! 
.env 파일은 절대 깃허브에 커밋하지 마세요.
Push Protection이 활성화된 저장소에서는 .env에 포함된 키가 감지되면 푸시가 거부됩니다.

## 주요 파일 구조
~~~ bash
project_root/
|── db/
├── prompt_to_query.py        # LangChain: 자연어 → QuerySchema(JSON)
├── prompt_input.py           # CLI에서 LangChain 실행 테스트
├── db_connect.py             # MySQL 연결 관리
├── search_team_posts.py      # JSON → SQL WHERE절 변환 및 DB 검색
├── test_team_search.py       # 예시 입력으로 검색 테스트
├── .env                      # 환경변수 (개인 로컬 전용)
└── README.md                 # 설명서 (현재 파일)
~~~

## 실행 방법

### 1. langchain json 출력 확인
~~~ bash
python prompt_input.py
~~~

예시 입력 : AI 분야, 11월 내 접수, 12월 내 종료, 백엔드 모집

### 2. 팀 모집 공고 검색 
~~~ bash
python test_team_search.py
~~~
