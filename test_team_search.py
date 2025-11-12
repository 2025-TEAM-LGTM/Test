# test_team_search.py
from prompt_to_query import parse_prompt
from search_team_posts import search_team_posts

nl = input("검색 조건을 입력하세요: ")
q = parse_prompt(nl).model_dump()         # LangChain → QuerySchema(JSON)
rows = search_team_posts(q)               # JSON → SQL WHERE → 결과 조회

if rows:
    for r in rows:
        print(f"🎯 {r['contest_name'] or '(미지정)'} | {r['needed_roles'] or '-'} | 모집 마감: {r['recruit_date']}")
else:
    print("조건에 맞는 팀 모집 공고가 없습니다.")


