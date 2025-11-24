# db_test.py
from db_connect import get_conn

def main():
    try:
        conn = get_conn()
        with conn.cursor() as cur:
            # 1) 연결 체크
            cur.execute("SELECT 1 AS ok")
            print("Ping:", cur.fetchone())

            # 2) 스키마/데이터 확인(있으면 카운트)
            for tbl in ["portfolio_project"]:
                cur.execute(f"SELECT COUNT(*) AS cnt FROM {tbl}")
                print(f"{tbl} rows:", cur.fetchone()["cnt"])

        conn.close()
        print("✅ DB 연결/쿼리 OK")
    except Exception as e:
        print("❌ DB 에러:", e)

if __name__ == "__main__":
    main()
