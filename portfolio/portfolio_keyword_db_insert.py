# portfolio_keyword_db_insert.py
# 포트폴리오 STAR 텍스트를 읽어서
# llm_extract.extract_keywords_from_star()로 키워드를 추출하고
# portfolio_keyword.keyword(JSON) 컬럼에 저장하는 스크립트

import json
from typing import List, Optional

import pymysql
from pymysql.connections import Connection

from portfolio_extract import extract_keywords_from_star  # LLM 키워드 추출 함수
from db_connect import get_conn

DB_NAME = "union_test"






# ============================
# SELECT / INSERT / UPDATE 헬퍼
# ============================

def get_portfolio_project(conn: Connection, portfolio_project_id: int) -> Optional[dict]:
    """
    portfolio_project 테이블에서
    특정 portfolio_project_id에 해당하는 STAR 텍스트를 가져온다.
    """
    with conn.cursor() as cur:
        cur.execute(
            """
            SELECT 
                portfolio_project_id,
                s_text,
                t_text,
                a_text,
                r_text
            FROM portfolio_project
            WHERE portfolio_project_id = %s
            """,
            (portfolio_project_id,),
        )
        return cur.fetchone()


def upsert_portfolio_keyword(conn: Connection, portfolio_project_id: int, keyword_json: dict) -> None:
    """
    portfolio_keyword 테이블에
    특정 portfolio_project_id에 대해 keyword(JSON)를 INSERT 또는 UPDATE 한다.
    """
    with conn.cursor() as cur:
        # 이미 존재하는지 체크
        cur.execute(
            """
            SELECT portfolio_keyword_id
            FROM portfolio_keyword
            WHERE portfolio_project_id = %s
            """,
            (portfolio_project_id,),
        )
        row = cur.fetchone()

        keyword_str = json.dumps(keyword_json, ensure_ascii=False)

        if row:
            # UPDATE
            cur.execute(
                """
                UPDATE portfolio_keyword
                SET keyword = %s
                WHERE portfolio_project_id = %s
                """,
                (keyword_str, portfolio_project_id),
            )
        else:
            # INSERT
            cur.execute(
                """
                INSERT INTO portfolio_keyword (portfolio_project_id, keyword)
                VALUES (%s, %s)
                """,
                (portfolio_project_id, keyword_str),
            )

    conn.commit()


def get_target_portfolio_ids(conn: Connection, only_without_keyword: bool = True) -> List[int]:
    """
    키워드를 생성해야 할 portfolio_project_id 목록을 가져온다.

    only_without_keyword=True:
        아직 portfolio_keyword에 없는 포트폴리오만 대상
    False:
        portfolio_project 전체 대상
    """
    with conn.cursor() as cur:
        if only_without_keyword:
            cur.execute(
                """
                SELECT p.portfolio_project_id
                FROM portfolio_project p
                LEFT JOIN portfolio_keyword k
                  ON p.portfolio_project_id = k.portfolio_project_id
                WHERE k.portfolio_project_id IS NULL
                ORDER BY p.portfolio_project_id
                """
            )
        else:
            cur.execute(
                """
                SELECT portfolio_project_id
                FROM portfolio_project
                ORDER BY portfolio_project_id
                """
            )
        rows = cur.fetchall()

    return [row["portfolio_project_id"] for row in rows]


# ============================
# 메인 처리 로직
# ============================

def process_one_portfolio(portfolio_project_id: int, conn: Optional[Connection] = None) -> None:
    """
    포트폴리오 1개 처리:
    1. portfolio_project에서 STAR 텍스트 가져오기
    2. LLM으로 JSON 키워드 추출
    3. portfolio_keyword.keyword에 upsert
    """
    own_conn = False
    if conn is None:
        conn = get_conn()
        own_conn = True

    try:
        row = get_portfolio_project(conn, portfolio_project_id)
        if not row:
            print(f"❌ portfolio_project_id={portfolio_project_id} 가 존재하지 않습니다.")
            return

        s = row["s_text"] or ""
        t = row["t_text"] or ""
        a = row["a_text"] or ""
        r = row["r_text"] or ""

        # 1) LLM으로 키워드 추출
        kw = extract_keywords_from_star(s, t, a, r)

        # 디버그용 출력 (보고 싶으면 주석 해제)
        # print("DEBUG:", portfolio_project_id, kw.model_dump())
        raw = kw.model_dump()
        ordered = {k: raw.get(k) for k in ["S", "T", "A", "R"]}
        # 2) DB에 JSON 저장
        upsert_portfolio_keyword(conn, portfolio_project_id, kw.model_dump())

        print(f"✅ portfolio_project_id={portfolio_project_id} 키워드 저장 완료")
    finally:
        if own_conn and conn:
            conn.close()


def process_all_portfolios(only_without_keyword: bool = True) -> None:
    """
    여러 포트폴리오를 한 번에 처리한다.

    only_without_keyword=True:
        아직 portfolio_keyword에 없는 포트폴리오만 처리
    False:
        전체 포트폴리오에 대해 키워드를 다시 생성/덮어쓰기
    """
    conn = get_conn()
    try:
        ids = get_target_portfolio_ids(conn, only_without_keyword=only_without_keyword)
        if not ids:
            print("📭 처리할 포트폴리오가 없습니다.")
            return

        print(f"🔎 총 {len(ids)}개 포트폴리오 처리 시작: {ids}")

        for pid in ids:
            process_one_portfolio(pid, conn=conn)

        print("🎉 모든 포트폴리오 키워드 추출 완료!")
    finally:
        conn.close()


# ============================
# 엔트리 포인트
# ============================

if __name__ == "__main__":
    # 1개만 테스트하고 싶으면 이거:
    # process_one_portfolio(1)

    # 아직 portfolio_keyword가 없는 포트폴리오 전체 처리
    process_all_portfolios(only_without_keyword=True)
