# keyword_schema.py
from pydantic import BaseModel
from typing import List, Optional

class SKeywords(BaseModel):
    # 도메인: 하나만 대표로 저장 (DB CHECK와 맞추기 위함)
    domain: Optional[str] = None
    problem_type: List[str] = []    # 이건 여전히 여러 개 가능

class TKeywords(BaseModel):
    goal: List[str] = []
    # 역할도 대표 하나만 (BACKEND_DEVELOPER, FRONTEND_DEVELOPER 등)
    role: Optional[str] = None

class AKeywords(BaseModel):
    hard_skills: List[str] = []
    responsibility: List[str] = []
    deliverables: List[str] = []
    problem_solving: List[str] = []

class RKeywords(BaseModel):
    impact: List[str] = []
    growth: List[str] = []

class PortfolioKeywords(BaseModel):
    S: SKeywords
    T: TKeywords
    A: AKeywords
    R: RKeywords
