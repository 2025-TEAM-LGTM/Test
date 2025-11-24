# test_team_search.py
from prompt_to_query import parse_prompt
from search_team_posts import build_team_where_clause, search_team_posts
from datetime import date, datetime

nl = input("검색 조건을 입력하세요: ")
print("🔍 찾는 중... \n")
q = parse_prompt(nl).model_dump()         # LangChain → QuerySchema(JSON)

rows = search_team_posts(q)               # JSON → SQL WHERE → 결과 조회

def fmt_date(x):
    if x in (None, "", "0000-00-00"):
        return "-"
    if isinstance(x, (date, datetime)):
        return x.strftime("%Y-%m-%d")
    return str(x)

if rows:
    print(f"{'팀 ID':<8} | {'공모전명':<25} | {'모집 역할':<30} | {'팀 모집 마감일':<12} | {'접수 마감일':<12} | {'대회 시작일'}")
    print("-" * 120)
    for r in rows:
        team_id   = str(r.get('team_id', '-'))
        name      = (r.get('contest_name') or '(미지정)')[:25]
        roles     = (r.get('needed_roles') or '-')[:30]
        recruit   = fmt_date(r.get('recruit_date'))
        recv_end  = fmt_date(r.get('reception_end_date'))
        start     = fmt_date(r.get('start_date'))

        print(f"{team_id:<8} | {name:<25} | {roles:<30} | {recruit:<12} | {recv_end:<12} | {start}")
else:
    print("조건에 맞는 팀 모집 공고가 없습니다.")




