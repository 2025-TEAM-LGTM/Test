# TEAM LGTM _ ai 기술 시연 

- contest : 공모전 팀 모집 글 검색 챗봇 - 팀장 입장에서 “어떤 공고를 찾고 싶은지”를 자연어로 입력하면, SQL 검색용 조건 JSON으로 구조화해서 DB에서 공고를 찾아주는 모듈
- portfolio : 포트폴리오 키워드 추출 & 매칭 (사용자의 STAR 형식 포트폴리오에서 키워드를 추출해 DB에 저장하고, 자연어 질문과 매칭하는 모듈)

두 디렉토리는 각각 독립적인 작은 프로젝트처럼 동작한다. 

## 1. 폴더 구조 
~~~ bash
졸프_기술시연_VER.2/
├─uniON_test/              # 공모전 팀 모집글 검색 모듈
│  ├─ contest/
│  │  ├─ db/               # 공모전/팀 관련 SQL 스키마 · 더미데이터
│  │  └─ __pycache__/
│  ├─ .env                 # uniON_test용 환경변수(OpenAI, DB 설정)
│  ├─ .gitignore
│  ├─ db_connect.py        # DB 연결 헬퍼
│  ├─ db_test.py           # DB 연결/쿼리 테스트
│  ├─ prompt_input.py      # 사용자 프롬프트 입력/테스트 스크립트
│  ├─ prompt_to_query.py   # 자연어 → Query JSON(LLM) 변환
│  ├─ query_schema.py      # 팀 모집 검색용 Query Pydantic 스키마
│  ├─ search_team_posts.py # Query JSON을 이용해 team_post 검색
│  └─ test_team_search.py  # 프롬프트 → JSON → DB 검색 end-to-end 테스트
│
├─ portfolio/               # 포트폴리오 키워드 추출 & 매칭 모듈
│  ├─ db/                   # user / portfolio_* 관련 SQL 스키마 · 더미데이터
│  ├─ __pycache__/
│  ├─ .env                  # portfolio용 환경변수(OpenAI, DB 설정)
│  ├─ .gitignore
│  ├─ db_connect.py         # DB 연결 헬퍼
│  ├─ db_test.py            # DB 연결/쿼리 테스트
│  ├─ keyword_schema.py     # PortfolioKeywords(Pydantic) 스키마
│  ├─ portfolio_extract.py  # STAR 텍스트 → PortfolioKeywords(JSON) 추출(LLM)
│  ├─ portfolio_keyword_db_insert.py
│  │                        # portfolio_project 전체를 돌면서
│  │                        # PortfolioKeywords를 추출해 portfolio_keyword 테이블에 저장
│  ├─ prompt_extract.py     # 사용자 검색 프롬프트 → PortfolioKeywords(JSON) 추출(LLM)
│  ├─ match.py              # query JSON ↔ portfolio JSON 매칭/스코어링 로직
│  ├─ test_keyword_extract.py  # 단일 포트폴리오 키워드 추출 테스트
│  ├─ test_match.py            # 자연어 질의 → 매칭 결과 출력 테스트
│  ├─ tempCodeRunnerFile.py    # VSCode 임시 파일
├─ readme.md                # (이 파일: 포트폴리오 모듈용 README)
└─ requirements.txt         # 의존성 패키지 목록

~~~

## 2. 공통 사전 준비

### 2-1. python & 패키지 설치

~~~ bash
pip install -r requirements.txt
~~~

### 2.2. DB 준비
- MYSQL 설치
- 각 모듈의 db/ 디렉토리에 있는 스키마 및 더미데이터 sql 실행

### 2-3. `.env` 파일 생성 
각 폴더 (contest, portfolio) 내부에 .env 파일을 만들고 아래 내용 추가

#### contest/

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

#### portfolio/

~~~ bash
# OpenAI API Key
OPENAI_API_KEY=sk-여기에_본인_API_KEY_입력

# DB 설정
DB_HOST=127.0.0.1
DB_PORT=3306
DB_USER=root
DB_PASSWORD=비밀번호
DB_NAME=union_final

~~~

주의 !!! 
.env 파일은 절대 깃허브에 커밋하지 마세요.
Push Protection이 활성화된 저장소에서는 .env에 포함된 키가 감지되면 푸시가 거부됩니다.


## 3. contest 모듈 (공모전 팀 모집글 검색)

### 3-1. 역할

사용자가 자연어로

“미디어/콘텐츠 분야 공모전 중 이번 달 마감인 것만 보여줘”
같은 문장을 입력하면,

prompt_to_query.py가 LLM을 사용해서 이를 구조화된 Query JSON으로 변환하고,

search_team_posts.py가 이 JSON을 기반으로 contest, team_post, role 등의 테이블에서 조건 검색을 수행한다.

### 3-2. 주요 파일

- db_connect.py : MySQL 연결을 생성하는 공통 헬퍼

- query_schema.py : 분야, 활동 형태, 마감 기간, 필요한 역할 등 검색 조건을 표현하는 Pydantic 스키마 정의

- prompt_to_query.py : 자연어 프롬프트 → QuerySchema JSON으로 변환

OpenAI Chat/JSON 모드 사용

- search_team_posts.py :
    - Query JSON을 받아 실제 SQL WHERE 조건으로 변환
    - team_post, team_info, contest, role 테이블을 조인하여 검색 결과를 반환

- test_team_search.py :
    하나의 프롬프트를 입력으로 받아 JSON 추출, 
    DB 검색 결과를 콘솔에 출력하는 end-to-end 스크립트

## 4. portfolio 모듈 (포트폴리오 키워드 추출 및 매칭)

## 4-1. 역할

- 사용자가 포트폴리오에서 프로젝트별로 STAR 형식(Situation, Task, Action, Result) 텍스트를 입력

- portfolio_extract.py가 OpenAI를 사용해 이 텍스트를 PortfolioKeywords JSON으로 변환
    (도메인, 역할, 하드 스킬, 문제 유형, 성과 등)

- portfolio_keyword_db_insert.py가 portfolio_project 테이블 전체를 돌며 키워드를 추출해 portfolio_keyword.keyword 컬럼(JSON)에 저장

- 사용자가 자연어로

“Node.js로 웹 서비스를 만든 백엔드 개발자를 보여줘.”
라고 물어보면,
prompt_extract.py가 이 문장을 똑같은 스키마(PortfolioKeywords)로 구조화하고,
match.py가 포트폴리오와의 유사도를 계산해 상위 N개를 추천한다.

### 4-2. 주요 파일 
- keyword_schema.py : PortfolioKeywords Pydantic 모델 정의

~~~ json
// 구조
{
  "S": { "domain": "...", "problem_type": [...] },
  "T": { "role": "...", "goal": [...] },
  "A": { "hard_skills": [...], "responsibility": [...], "deliverables": [...], "problem_solving": [...] },
  "R": { "impact": [...], "growth": [...] }
}
~~~

- portfolio_extract.py : STAR 원문 텍스트와 ENUM(도메인, 역할, 하드 스킬 목록)을 프롬프트에 넣어 LLM이 DB 제약을 만족하는 JSON만 내도록 제한

- portfolio_keyword_db_insert.py
    - portfolio_project 테이블을 조회하여 각 프로젝트의 s_text, t_text, a_text, r_text를 LLM에 넘김

    - 결과 JSON을 portfolio_keyword.keyword 컬럼에 INSERT/UPDATE

    - process_all_portfolios()로 아직 키워드가 없는 프로젝트만 일괄 처리

- prompt_extract.py
    - 사용자의 자연어 검색 문장을 포트폴리오와 같은 스키마의 JSON으로 변환

- match.py
    - score_portfolio(query_kw, candidate_kw) -> float
        - 도메인/역할 일치 여부
        - 하드 스킬 교집합 개수
        - 목표/문제 유형/성과 텍스트의 겹침 정도

    - rank_portfolios(query_kw, candidates) -> [(portfolio_project_id, score), ...]
        - 여러 포트폴리오 중 점수가 높은 순으로 정렬

- test_keyword_extract.py
    하드코딩된 STAR 예시 텍스트로 LLM 키워드 추출이 잘 되는지 테스트

- test_match.py

    - 자연어 질의 → PortfolioKeywords (query side)

    - DB에서 모든 portfolio_keyword 로드 → PortfolioKeywords 리스트

    - match.py의 rank_portfolios로 상위 N개 추천 결과 출력
