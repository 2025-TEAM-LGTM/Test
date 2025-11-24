
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
    사용자의 검색 프롬프트(자연어)를, 포트폴리오와 동일한 JSON 스키마(PortfolioKeywords)로 변환한다.
    즉, 포트폴리오 키워드와 완전히 같은 형태의 JSON이 반환됨.
    """

    schema = PortfolioKeywords.model_json_schema()

    system_msg = (
        "너는 사용자의 검색 문장을 분석해서, "
        "포트폴리오 키워드와 동일한 스키마(PortfolioKeywords)를 가지는 JSON을 만드는 도우미야. "
        "출력은 무조건 유효한 JSON 하나만 반환해. 설명 문장은 넣지 마."
    )

    user_msg = f"""
사용자 검색 문장:
"{query}"

이 문장은 "어떤 프로젝트/경험을 가진 사람을 찾고 싶은지"를 나타낸다.
이 문장을 읽고, 아래 스키마(PortfolioKeywords)에 맞게 JSON을 채워줘.

- S: 사용자가 원하는 도메인/문제 유형
  - S.domain: 아래 ENUM 중 하나 선택 , 없으면 비워도 됨. 
    {ALLOWED_DOMAINS}
  - S.problem_type: 사용자가 해결하고 싶어하는 문제 유형 키워드들 (리스트)

- T: 사용자가 원하는 역할/목표
  - T.role: 아래 ENUM 중 하나 선택 , 없으면 비워도 됨. 
    {ALLOWED_ROLES}
  - T.goal: 프롬프트에서 드러나는 목표/목적을 짧은 문장 리스트로 정리

- A: 사용자가 원하는 기술/역량
  - A.hard_skills: 아래 목록 중 실제 기술 스택만 포함
    {ALLOWED_HARD_SKILLS}
  - A.responsibility: 사용자가 기대하는 역할/책임을 문장 리스트로
  - A.deliverables: 있으면, 기대하는 산출물 형태
  - A.problem_solving: 있으면, 기대하는 문제 해결 방식/경험

- R: 사용자가 원하는 성과/배운 점
  - R.impact: 원하는 결과/성과(있으면)
  - R.growth: 함께 일하며 기대하는 성장/역량(있으면)

JSON Schema (반드시 이 구조를 따를 것):
{json.dumps(schema, ensure_ascii=False, indent=2)}

⚠ 매우 중요한 규칙:
- S.domain, T.role은 반드시 위 ENUM에서 하나를 선택해 문자열로 넣어라. (NULL 금지)
- A.hard_skills에는 ALLOWED_HARD_SKILLS 안의 값만 넣어라.
- 나머지 필드는 프롬프트에 없으면 빈 리스트([])나 null로 둬도 된다.
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
