import json
import pymysql

from prompt_extract import extract_keywords_from_query
from keyword_schema import PortfolioKeywords
from match import rank_portfolios
from db_connect import get_conn

# 1) 사용자 프롬프트 → query_kw
q = "프론트 개발자를 찾고 싶어요. 그 사람은 비즈니스 관련 프로젝트 경험이 있었으면 해요. "
query_kw = extract_keywords_from_query(q)

# 2) DB에서 모든 portfolio_keyword 로딩
conn = get_conn()
candidates = {}
with conn.cursor() as cur:
    cur.execute("SELECT portfolio_project_id, keyword FROM portfolio_keyword")
    for row in cur.fetchall():
        pid = row["portfolio_project_id"]
        kw_dict = json.loads(row["keyword"])
        candidates[pid] = PortfolioKeywords.model_validate(kw_dict)
conn.close()

# 3) 매칭
ranked = rank_portfolios(query_kw, candidates, top_k=5)

print("추천 결과 (상위 5개):")
for pid, score in ranked:
    print(f"- portfolio_project_id={pid}, score={score}")
