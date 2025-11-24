
import json # 프롬프트에 json 스키마를 문자열로 넣을 떄 필요함 
from openai import OpenAI
from keyword_schema import PortfolioKeywords # 스키마 
from typing import Optional
from dotenv import load_dotenv
load_dotenv()

client = OpenAI()  # OPENAI_API_KEY 환경변수 세팅되어 있어야 함

# ============================
# ENUM 강제 목록
# ============================

ALLOWED_DOMAINS = [
    "EDUCATION", "LIFESTYLE", "SOCIAL", "ENTERTAINMENT", "HEALTHCARE",
    "PRODUCTIVITY", "E_COMMERCE", "TRAVEL", "FINTECH"
]

ALLOWED_ROLES = [
    "BACKEND_DEVELOPER", "FRONTEND_DEVELOPER",
    "UX/UI_DESIGNER", "PM", "AI_DEVELOPER"
]

ALLOWED_HARD_SKILLS = [
    # 언어
    "Python", "JavaScript", "TypeScript", "Java", "C++", "Go", "Kotlin",
    # 프레임워크/라이브러리
    "React", "Next.js", "Node.js", "Express", "Spring", "Django", "Flask",
    # DB
    "MySQL", "MariaDB", "PostgreSQL", "MongoDB", 
    # Infra/DevOps
    "AWS", "Docker", "Kubernetes", "Nginx", "Git", "GitHub Actions",
]


def extract_keywords_from_query(query: str) -> PortfolioKeywords:
    """
   사용자의 검색 프롬프트(자연어)를,
  '이 검색 조건에 맞는 이상적인 후보가 과거에 했을 법한 포트폴리오 경험'의
  키워드(JSON, PortfolioKeywords 스키마)로 변환한다.
    """

    schema = PortfolioKeywords.model_json_schema()

    system_msg = (
        "너는 사용자의 검색 문장을 분석해서, "
        "이 검색 조건에 맞는 '이상적인 후보자'가 과거에 수행했을 법한 "
        "포트폴리오 경험을 요약한 JSON(PortfolioKeywords 스키마)을 만드는 도우미야. "
        "항상 후보자의 입장에서, 과거 프로젝트/경험을 서술하듯이 작성해. "
        "출력은 무조건 유효한 JSON 하나만 반환해. 설명 문장은 넣지 마."
        )

    user_msg = f"""
사용자 검색 문장:
"{query}"

이 문장은 "어떤 프로젝트/경험을 가진 사람을 찾고 싶은지"를 나타낸다.
이 문장을 읽고, 아래 스키마(PortfolioKeywords)에 맞게 
'이상적인 후보자'의 포트폴리오 경험을 상상해서 JSON을 채워줘

- S: 사용자가 원하는 도메인/문제 유형
  - S.domain: 아래 ENUM 중, 후보자의 대표적인 프로젝트 도메인과 가장 가까운 것 1개를 선택해라.없으면 비워두기
    {ALLOWED_DOMAINS}
  - S.problem_type: 사용자가 해결하고 싶어하는 문제 유형을 표현하는 문장 리스트 (List[str])

- T: 사용자가 원하는 역할/목표
  - T.role: 아래 ENUM 중, 후보자가 이 검색 조건과 관련된 프로젝트에서 맡았던 역할과 가장 가까운 것 1개를 선택, 없으면 비워두기
    {ALLOWED_ROLES}
  - T.goal: 이 검색 조건에 맞는 사람이 과거에 수행했을 법한
            프로젝트의 목표를 문장 리스트(List[str])로 작성해.
    - 사용자의 검색 의도를 그대로 반복하지 말 것.
    - 항상 "이 사람이 했던 프로젝트의 목표"처럼 작성할 것.
    - 올바른 예:
      ["Node.js 기반 웹 서비스의 백엔드 서버를 구축하는 것이 목표였음",
       "실제 사용자에게 제공될 수 있는 서비스를 배포하는 것이 목표였음"]

- A: 후보자가 과거 프로젝트에서 사용했던 기술/역할/문제해결 방식
  - A.hard_skills: 아래 목록 중, 후보자가 실제로 사용했을 법한 기술 스택만 포함 (List[str]).
    {ALLOWED_HARD_SKILLS}
  - A.responsibility:
    - 후보자가 과거 프로젝트에서 수행했던 구체적인 역할/업무를 문장 리스트(List[str])로.
    - 예시:
      ["Node.js로 REST API를 설계하고 구현함",
       "데이터베이스 스키마 설계 및 쿼리 최적화를 수행함",
       "CI/CD 파이프라인을 구성하여 자동 배포를 담당함"]
  - A.deliverables:
    - 후보자가 실제로 만들어낸 주요 산출물을 문장 리스트(List[str])로.
    - 예시:
      ["실제 사용자에게 서비스되는 웹서비스 백엔드 서버",
       "관리자용 어드민 API",
       "배포 자동화 스크립트 및 설정"]
  - A.problem_solving:
    - 후보자가 프로젝트에서 겪었던 문제와 해결 방식을 문장 리스트(List[str])로.
    - 예시:
      ["트래픽 증가로 인해 응답 속도가 느려져 캐싱과 쿼리 최적화를 통해 성능을 개선함",
       "배포 중간에 환경 변수 설정 오류를 발견하고 롤백 후 재배포 전략을 수립함"]


- R: 후보자가 과거 프로젝트에서 만들어낸 성과/배운 점
  - R.impact:
    - 그 프로젝트가 만들어낸 결과/성과를 문장 리스트(List[str])로.
    - 예시:
      ["서비스 일일 활성 사용자 수가 500명 이상으로 증가함",
       "에러율이 30% 감소함",
       "무중단 배포에 성공하여 운영 안정성을 높임"]
  - R.growth:
    - 그 경험을 통해 후보자가 성장한 점/배운 점을 문장 리스트(List[str])로.
    - 예시:
      ["실제 서비스 운영 환경에서의 장애 대응 경험을 쌓음",
       "Node.js 기반 마이크로서비스 아키텍처 설계 역량이 향상됨"]

JSON Schema (반드시 이 구조를 따를 것):
{json.dumps(schema, ensure_ascii=False, indent=2)}

⚠ 매우 중요한 규칙:
- S.domain, T.role은 반드시 위 ENUM에서 하나를 선택해 문자열로 넣어라. 
- A.hard_skills에는 ALLOWED_HARD_SKILLS 안의 값만 넣어라.
- 나머지 필드는 프롬프트로부터 합리적으로 추론해서 채우되,
  정말 정보가 없다고 판단되는 경우에만 빈 리스트([])나 null을 사용해도 된다.
- "찾고 싶다/원한다/하고 싶어요" 등 검색자의 관점 표현은 절대 쓰지 말고,
  항상 "무엇을 했다/수행했다/경험했다"처럼 후보자의 과거 경험 관점으로 작성해라.
- 출력은 반드시 JSON 한 개만, ``` 없이 순수 JSON만.
"""

    resp = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {"role": "system", "content": system_msg},
            {"role": "user", "content": user_msg},
        ],
        temperature=0,
    )

    content = resp.choices[0].message.content

    try:
        data = json.loads(content)
    except json.JSONDecodeError:
        print("❌ JSON 파싱 실패 (query):")
        print(content)
        raise

    # 포트폴리오 키워드와 완전히 같은 스키마로 검증
    kw = PortfolioKeywords.model_validate(data)
    return kw
