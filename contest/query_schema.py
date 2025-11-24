# 프롬프트를 어떤 형식의 스키마에 저장할지에 대한 파일 

from typing import List, Optional; 
from pydantic import BaseModel, Field;


class QuerySchema(BaseModel):
    # contests
    field: Optional[str] = None                 # ENUM(FIELD): AI, ART, ...
    activity_type: Optional[str] = None         # ENUM(ACTIVITY): OFFLINE/ONLINE/HYBRID
    reception_start_date: Optional[str] = None  # 접수 시작일 : YYYY-MM-DD
    reception_end_date: Optional[str] = None    # 접수 마감일 : YYYY-MM-DD
    start_date: Optional[str] = None            # 활동 시작 : YYYY-MM-DD
    end_date: Optional[str] = None              # 활동 종료(예: "12월 내 끝" → 2025-12-31)
    cost: Optional[int] = None                  # 참가비 상한(원)
    reward: Optional[int] = None                # 총상금 하한(원)
    eligibility: Optional[str] = None           # 참가 대상 : 자유 텍스트

    # team_info / role
    recruit_date: Optional[str] = None          # 이 날짜 "이전"에 모집이 마감: 경계값(YYYY-MM-DD)
    contact_type: Optional[str] = None          # ENUM(CONTACT)
    needed_roles: List[str] = Field(default_factory=list)  # ENUM(ROLE)