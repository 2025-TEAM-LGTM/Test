# search_team_posts.py
from typing import List, Tuple # 자료 구조 
from db_connect import get_conn # db 연결 

# 동적 sql 만들기 위한 함수
# [] 형식에 있던 단어들만 빼내어 sql 쿼리에 넣을 수 있게 함!
def _in_clause(placeholders: List[str]) -> str:
    return ", ".join(["%s"] * len(placeholders))

# WHERE 절 생성하는 함수 
# q : langchain이 생성한 json (queryschema)
def build_team_where_clause(q: dict) -> Tuple[str, list]:
    where = [] # sql 문자열 조건 모음 
    params = [] # %s 자리에 들어갈 값 리스트 

    # --- team_info 기반 ---
    # 팀 모집 마감일: "11월 이전에 끝" → recruit_date < 2025-11-01
    if q.get("recruit_date"): # q에서 recruit_date 파트만 빼옴 
        where.append("ti.recruit_date <= %s") # where 조건 더하기 
        params.append(q["recruit_date"]) # param  

    # 연락 수단
    if q.get("contact_type"):
        where.append("ti.contact_type = %s") # 연락수단은 무조건 일치 
        params.append(q["contact_type"])


    # 필요한 역할 ANY 매칭 (백엔드 등)
    # EXISTS 서브쿼리로 해당 팀이 그 역할을 포함하는지 체크한다. 
    if q.get("needed_roles"):
        roles = q["needed_roles"]
        where.append(f"EXISTS (SELECT 1 FROM role r2 WHERE r2.team_id = ti.team_id AND r2.needed_roles IN ({_in_clause(roles)}))")
        params += roles

    # --- contests 기반 필터(팀이 특정 공모전에 붙어있을 때만 적용) ---
    # contest_id는 NULL일 수 있으므로 LEFT JOIN 기준 + 조건은 별도
    if q.get("field"):
        where.append("c.field = %s")
        params.append(q["field"])
    if q.get("activity_type"):
        where.append("c.activity_type = %s")
        params.append(q["activity_type"])
    if q.get("reception_start_date"):
        where.append("c.reception_start_date >= %s")
        params.append(q["reception_start_date"])
    if q.get("reception_end_date"):
        where.append("c.reception_end_date <= %s")
        params.append(q["reception_end_date"])
    if q.get("start_date"):
        where.append("c.start_date >= %s")
        params.append(q["start_date"])
    if q.get("end_date"):
        where.append("c.end_date <= %s")
        params.append(q["end_date"])
    if q.get("cost"):
        where.append("c.cost <= %s")
        params.append(q["cost"])
    if q.get("reward"):
        where.append("c.reward >= %s")
        params.append(q["reward"])
    if q.get("eligibility"):
        where.append("c.eligibility LIKE %s")
        params.append(f"%{q['eligibility']}%")

    # 최종 조립 
    where_clause = f"WHERE {' AND '.join(where)}" if where else ""
    print(where_clause)
    print(params)
    print("=" * 120)
    return where_clause, params


def search_team_posts(q: dict):
    """
    team_post 중심 검색:
      - 항상 team_info 조인
      - contests는 선택(LEFT JOIN): 공모전 필터가 있을 때만 영향
      - role은 GROUP_CONCAT로 모아보기 + EXISTS로 필터링
    """
    conn = get_conn()
    with conn.cursor() as cur:
        where_clause, params = build_team_where_clause(q)
        sql = f"""
        SELECT
          tp.post_id,
          tp.team_id,
          tp.leader_id,
          DATE_FORMAT(tp.created_at, '%%Y-%%m-%%d %%H:%%i') AS created_at,
          ti.current_team,
          ti.recruit_date,
          ti.collab_tool,
          ti.contact_type,
          ti.contact_value,
          ti.seeking_text,
          ti.culture_text,
          ti.extra_note,
          GROUP_CONCAT(DISTINCT r.needed_roles ORDER BY r.needed_roles SEPARATOR ',') AS needed_roles,
          c.contest_id,
          c.contest_name,
          c.field,
          c.activity_type,
          c.reception_start_date,
          c.reception_end_date,
          c.start_date,
          c.end_date,
          c.cost,
          c.reward,
          c.eligibility
        FROM team_post tp
        JOIN team_info ti ON ti.team_id = tp.team_id
        LEFT JOIN role r ON r.team_id = ti.team_id
        LEFT JOIN contests c ON c.contest_id = tp.contest_id
        {where_clause}
        GROUP BY
          tp.post_id, tp.team_id, tp.leader_id, tp.created_at,
          ti.current_team, ti.recruit_date, ti.collab_tool, ti.contact_type, ti.contact_value,
          ti.seeking_text, ti.culture_text, ti.extra_note,
          c.contest_id, c.contest_name, c.field, c.activity_type, c.reception_start_date, c.reception_end_date,
          c.start_date, c.end_date, c.cost, c.reward, c.eligibility
        ORDER BY
          c.reward DESC, 
          c.reward DESC,
          tp.created_at DESC;
        """
        cur.execute(sql, params)
        return cur.fetchall()
