# llm_extract.py
# opnenai를 사용하여, JSON 키워드를 뽑아준다. 

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



# 메인 함수
# S/T/A/R 텍스트를 넘기면, keyword_schema에서 정의한 JSON 스키마대로 키워드를 뽑아오는 함수.
# 리턴 타입 : portfoliokeywords라는 pydanic 모델
def extract_keywords_from_star(s: str, t: str, a: str, r: str) -> PortfolioKeywords:
    # llm에게 json 모양을 알려줄 자료를 준비시키기 
    schema = PortfolioKeywords.model_json_schema()

    system_msg = (
        "너는 포트폴리오 STAR 텍스트를 읽고, 미리 정의된 스키마에 맞춰 "
        "키워드만 JSON 형태로 추출하는 도우미야. "
        "반드시 유효한 JSON만 출력해. 설명 문장 넣지 마."

        
    )

    user_msg = f"""
아래는 한 사용자의 프로젝트 STAR 텍스트야.

[S] Situation (상황):
{s}

[T] Task (목표/역할):
{t}

[A] Action (실행):
{a}

[R] Result (성과/배운점):
{r}

이 내용을 바탕으로, 아래 JSON 스키마에 맞춰 키워드를 추출해줘.

규칙 :
1) S.domain은 아래 ENUM 중 하나만 허용됨:
{ALLOWED_DOMAINS}

   - 나열된 단어 외에는 절대로 사용하지 마라.
   - 모호하거나 해당 없음 → 가장 가까운 ENUM 하나를 선택해라.
   - NULL/빈 문자열 금지 (DB에서 체크 제약 때문에 오류 남).

2) T.role도 아래 ENUM 중 하나만 허용됨:
{ALLOWED_ROLES}

   - 절대 new string 만들지 마라.
   - NULL 금지. 가장 가까운 ENUM 하나 선택.

3) A.hard_skills는 반드시 아래 스택 이름 중에서만 선택:
{ALLOWED_HARD_SKILLS}

   - 기술스택/언어/프레임워크/라이브러리/DB/DevOps 도구만 허용
   - "문제 해결", "협업", "소통", "최적화" 같은 추상적 표현 금지
   - 없는 기술 절대 넣지 마라.

4) 나머지 text 필드는 자유롭게 작성 가능. 그러나, 추후 embedding을 실시할 것이기에 구체적인 수치나 분야보단 
포괄적인 언어로 바꿀 것

5) 출력은 반드시 아래 JSON 스키마를 따를 것.
   JSON 하나만 출력. 코드블록(```) 쓰지 말 것.

6) - 언급되지 않은 값은 빈 리스트([]) 또는 null로 둬도 된다.
 
스키마(JSON Schema):
{json.dumps(schema, ensure_ascii=False, indent=2)}


"""

    resp = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {"role": "system", "content": system_msg},
            {"role": "user", "content": user_msg},
        ],
        temperature=0,
    )

    content = resp.choices[0].message.content  # 문자열(JSON이어야 함)

    # 혹시라도 이상한 텍스트가 섞여 있을 수 있으니 한 번 파싱 시도
    try:
        data = json.loads(content)
    except json.JSONDecodeError as e:
        print("❌ JSON 파싱 실패, 원본 content:")
        print(content)
        raise e

    # pydantic으로 검증 + 모델 변환
    kw = PortfolioKeywords.model_validate(data)
    return kw