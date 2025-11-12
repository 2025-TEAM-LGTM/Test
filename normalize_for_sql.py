# normalize_for_sql.py
import re
from datetime import datetime
from typing import List, Optional, Dict, Any

TODAY = datetime(2025, 11, 11)  # Asia/Seoul 기준 현재 날짜(요 프로젝트 고정)

# ===== ENUM 화이트리스트 =====
ALLOWED_ACTIVITY = {"OFFLINE", "ONLINE", "HYBRID"}
ALLOWED_FIELD    = {"AI","ART","DATA","IDEA","ARCHITECTURE","BUSINESS","IT","STARTUP","SCIENCE","SOCIAL"}
ALLOWED_CONTACT  = {"KAKAO","EMAIL","DM","PHONE","OTHER"}
ALLOWED_ROLES    = {"Manager","Backend_Developer","Frontend_Developer","Web_Designer","Designer","Analyst","DevOps","Surveyor","Marketer"}

# ===== 한글/동의어 → ENUM 매핑 사전 (필요시 확장) =====
ACTIVITY_MAP = {
    "대면": "OFFLINE", "오프라인": "OFFLINE",
    "비대면": "ONLINE", "온라인": "ONLINE", "원격": "ONLINE", "리모트": "ONLINE",
    "혼합": "HYBRID", "하이브리드": "HYBRID",
}
FIELD_MAP = {
    "인공지능": "AI", "데이터": "DATA", "아이디어": "IDEA",
    "건축": "ARCHITECTURE", "비즈니스": "BUSINESS",
    "창업": "STARTUP", "과학": "SCIENCE", "사회": "SOCIAL",
    "미술": "ART", "아트": "ART", "IT": "IT"
}
CONTACT_MAP = {
    "카카오": "KAKAO", "카톡": "KAKAO", "오픈채팅": "KAKAO",
    "이메일": "EMAIL", "메일": "EMAIL",
    "전화": "PHONE", "연락처": "PHONE",
    "DM": "DM"
}
ROLE_MAP = {
    "백엔드": "Backend_Developer", "서버": "Backend_Developer", "BE": "Backend_Developer",
    "프론트": "Frontend_Developer", "프론트엔드": "Frontend_Developer", "FE": "Frontend_Developer",
    "웹디자이너": "Web_Designer", "웹 디자이너": "Web_Designer",
    "디자이너": "Designer", "기획": "Manager", "PM": "Manager",
    "데이터": "Analyst", "분석": "Analyst",
    "데브옵스": "DevOps", "인프라": "DevOps",
    "설문": "Surveyor", "마케터": "Marketer", "마케팅": "Marketer",
    "매니저": "Manager"
}

def _normalize_enum(value: Optional[str], allowed: set, mapping: Dict[str, str]) -> Optional[str]:
    if not value: 
        return None
    v = value.strip()
    if v in allowed:
        return v
    # 한글·동의어 맵핑
    v2 = mapping.get(v)
    if v2 in allowed:
        return v2
    # 추가 방어: 대문자화 시도
    if v.upper() in allowed:
        return v.upper()
    return None

def normalize_activity(activity_type: Optional[str]) -> Optional[str]:
    return _normalize_enum(activity_type, ALLOWED_ACTIVITY, ACTIVITY_MAP)

def normalize_field(field: Optional[str]) -> Optional[str]:
    return _normalize_enum(field, ALLOWED_FIELD, FIELD_MAP)

def normalize_contact_list(contact_types: List[str]) -> List[str]:
    out = []
    for c in contact_types or []:
        n = _normalize_enum(c, ALLOWED_CONTACT, CONTACT_MAP)
        if n and n not in out:
            out.append(n)
    return out

def normalize_roles(roles: List[str]) -> List[str]:
    out = []
    for r in roles or []:
        # 이미 ENUM이면 통과
        if r in ALLOWED_ROLES and r not in out:
            out.append(r); continue
        # 맵핑 테이블로 정규화(문장 안에 키워드 들어있는 경우도 처리)
        mapped = None
        for k, v in ROLE_MAP.items():
            if k.lower() in r.lower():
                mapped = v; break
        if mapped and mapped in ALLOWED_ROLES and mapped not in out:
            out.append(mapped)
    return out

# 날짜 파서: 다양한 포맷 → YYYY-MM-DD
DATE_PATTERNS = [
    r'(?P<y>\d{4})[.\-/](?P<m>\d{1,2})[.\-/](?P<d>\d{1,2})',
    r'(?P<m>\d{1,2})[.\-/](?P<d>\d{1,2})',           # 연도 없음
    r'(?P<m>\d{1,2})[.](?P<d>\d{1,2})',              # 11.18
]

def normalize_date(s: Optional[str]) -> Optional[str]:
    if not s:
        return None
    text = s.strip()
    for pat in DATE_PATTERNS:
        m = re.search(pat, text)
        if not m:
            continue
        gd = m.groupdict()
        y = int(gd.get("y") or TODAY.year)
        mth = int(gd["m"])
        d = int(gd["d"])
        # 유효성/0-padding
        try:
            dt = datetime(y, mth, d)
            return dt.strftime("%Y-%m-%d")
        except ValueError:
            return None
    return None

MONEY_NUM = re.compile(r'[\d,]+')
def normalize_money_to_int(text: Optional[str]) -> Optional[int]:
    """'총상금 300만원', '₩200,000', '참가비 2만 원' -> 원 단위 정수"""
    if not text: 
        return None
    t = text.replace(" ", "")
    mult = 1
    if "억" in t:
        mult *= 100_000_000
        t = t.replace("억", "")
    if "만" in t:
        mult *= 10_000
        t = t.replace("만", "")
    # 숫자만 추출
    m = MONEY_NUM.search(t)
    if not m:
        return None
    n = int(m.group(0).replace(",", ""))
    return n * mult

def normalize_eligibility(items: List[str]) -> Optional[str]:
    if not items:
        return None
    seen = []
    for x in items:
        xx = " ".join(x.split())
        if xx and xx not in seen:
            seen.append(xx)
    return ", ".join(seen) if seen else None

def normalize_record(raw: Dict[str, Any]) -> Dict[str, Any]:
    """2번 출력(JSON dict) -> DB INSERT-ready dict"""
    return {
        # contests
        "field":            normalize_field(raw.get("field")),
        "reception_start_date": normalize_date(raw.get("reception_start_date")),
        "reception_end_date":   normalize_date(raw.get("reception_end_date")),
        "start_date":       normalize_date(raw.get("start_date")),
        "end_date":         normalize_date(raw.get("end_date")),
        "activity_type":    normalize_activity(raw.get("activity_type")),
        "cost":             normalize_money_to_int(raw.get("cost_text")),
        "reward":           normalize_money_to_int(raw.get("reward_text")),
        "eligibility":      normalize_eligibility(raw.get("eligibility") or []),

        # team_info
        "recruit_date":     normalize_date(raw.get("recruit_date")),

        # role/contact (1:N)
        "needed_roles":     normalize_roles(raw.get("needed_roles") or []),
        "contact_types":    normalize_contact_list(raw.get("contact_types") or []),
    }

# ---- quick self-test ----
if __name__ == "__main__":
    sample = {
        "field": "인공지능",
        "reception_start_date": "2025-11-10",
        "reception_end_date": "2025.11.20",
        "start_date": "12/01",
        "end_date": "12.15",
        "activity_type": "혼합",
        "cost_text": "참가비 2만원",
        "reward_text": "총상금 300만원",
        "eligibility": ["대학생", "전공자 우대", "대학생"],  # dup 포함
        "recruit_date": "11.18",
        "needed_roles": ["백엔드 1", "프론트엔드 2", "디자이너"],
        "contact_types": ["이메일", "카톡", "전화"]
    }
    print(normalize_record(sample))

