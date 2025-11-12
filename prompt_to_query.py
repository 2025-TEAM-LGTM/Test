# input : 챗봇 사용자의 프롬프트 - 어떤 공고를 찾고 있어. (자연어)
# output : 프롬프트 기반의 keyword json 
from dotenv import load_dotenv
load_dotenv()

from langchain_openai import ChatOpenAI # gpt 모델을 불러오는 클래스 
from langchain_core.prompts import ChatPromptTemplate # prompt를 체계적으로 관리하는 템플릿 
from datetime import date
from query_schema import QuerySchema # 개발자 지정 json 형식 

# LLM 인스턴스 
# temperature - 값이 높을수록 창의성이 올라가고 일관성이 낮아짐 (파싱 위해 0 )
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

# 날짜 바뀌면 바꿔줘야하나봄
THIS_YEAR = 2025

# ENUM 지정 
allowed_activity = "OFFLINE, ONLINE, HYBRID"
allowed_field    = "AI, ART, DATA, IDEA, ARCHITECTURE, BUSINESS, IT, STARTUP, SCIENCE, SOCIAL"
allowed_contact  = "KAKAO, EMAIL, DM, PHONE, OTHER"
allowed_roles    = "Manager, Backend_Developer, Frontend_Developer, Web_Designer, Designer, Analyst, DevOps, Surveyor, Marketer"

# 시스템 모델에게 주어지는 지침서 - gpt가 규칙 기반 파서처럼 행동하게 해준다. 
# 해당 프롬프트의 내용 요약
# 1. 자연어 프롬프트를 query schema에 맞게 구조화하라
# 2. 날짜 및 금액의 형식 지정
# 3. 모호한 부분은 null로 표시할 것 + ENUM에 맞게 매핑할 것 
# 4. 언급하지 않은 것 또한 NULL로 비워둘 것 
SYSTEM = (
    "너는 한국어 자연어 조건을 SQL 검색용 쿼리로 구조화한다. "
    "출력은 반드시 지정된 JSON 스키마(QuerySchema)에 맞춘다. "
    "모호하면 null로 비워둔다(추측 금지). ENUM 필드는 허용값만 사용한다. "
    "사용자가 특정 항목(분야, 활동 형태, 기간, 금액, 역할 등)을 언급하지 않은 경우, 그 필드는 null로 둔다. "
    "연·월 표현은 YYYY-MM-DD 절대 날짜로 풀어 쓴다(기준 연도는 2025, Asia/Seoul). "
    "예: '11월 내' → '2025-11-01' ~ '2025-11-30'. "
    "예: '12월 내에 끝내' → end_date='2025-12-31'. "
    "예: '팀 모집은 11월 이전에 끝' → recruit_date='2025-11-01'. "
    "금액은 원 단위 정수로 환산: '5만원 이하'→ cost=50000, '100만원 이상'→reward=1000000. "
    "역할 한글 표기는 ENUM으로 매핑: 백엔드→Backend_Developer, ... "
)

# 모델에 ENUM 형식과 함께 사용자 prompt 전달 
USER_TMPL = f"""

    허용 ENUM:
    - activity_type: {allowed_activity}
    - contest_field: {allowed_field}
    - contact_type: {allowed_contact}
    - role_type: {allowed_roles}

요청: 아래 자연어 조건을 QuerySchema에 맞게 구조화해.
자연어:
{{input_text}}

"""

# prompt 구성
prompt = ChatPromptTemplate.from_messages([
    ("system", SYSTEM), # 위의 지침서에 맞게 돌려보기
    ("user", USER_TMPL) # 사용자의 실제 입력 + enum에 맞게 넣음 

])
### langchain ###
# 여기 이해가 될랑말랑....

# 구조적 출력으로 감싸기
# prompt : 그냥 체계화된 문자열 
# | : 앞단계의 출력을 다시 다음 단계의 입력으로 넘기는 기호 
# llm.with_structured_output(QuerySchema): llm이 생성하는 텍스트를 queryschema 형태로 자동 변환하라 (즉, 모델의 응답을 json으로 파싱 )
chain = prompt | llm.with_structured_output(QuerySchema)

# 함수 형태로 랩핑 
def parse_prompt(natural_korean: str) -> QuerySchema:
    return chain.invoke({"input_text": natural_korean})


