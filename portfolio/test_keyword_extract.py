# test_keyword_extract.py
from portfolio_extract import extract_keywords_from_star
from prompt_extract import extract_keywords_from_query

def test_extract_keywords_from_star():
    s = """학교 공지사항이 흩어져 있어서, 학생들이 중요한 공모전 정보를 놓치는 문제가 있었다.
    우리는 이를 해결하기 위해 학교 공모전/대외활동 정보를 한 곳에 모아주는 서비스를 기획했다."""
    
    t = """이 프로젝트에서 나는 Backend Developer로 참여했다.
    목표는 공모전 정보를 저장/검색할 수 있는 API 서버를 설계하고 구현하는 것이었다."""
    
    a = """Node.js와 Express를 사용해 REST API를 구현했고,
    MariaDB로 공모전/팀 모집 정보를 저장하는 스키마를 설계했다.
    검색 속도를 위해 제목/분야/모집 대상에 인덱스를 걸고,
    Docker를 사용해 로컬 개발 환경과 배포 환경을 통일했다."""
    
    r = """서비스 내부 베타 테스트에서 30명 정도가 사용했고,
    공모전 관련 질문이 기존 대비 40% 정도 줄어들었다.
    DB 인덱싱과 쿼리 최적화가 실제 체감 성능에 큰 영향을 준다는 것을 배웠다."""

    kw = extract_keywords_from_star(s, t, a, r)

    print("=== RAW Pydantic 객체 ===")
    print(kw)

    print("\n=== JSON 형태 ===")
    print(kw.model_dump_json(ensure_ascii=False, indent=2))

def test_extract_keywords_from_query():
    q = "프론트 개발자를 찾고 싶어요. 그 사람은 비즈니스 관련 프로젝트 경험이 있었으면 해요. "
    query_kw = extract_keywords_from_query(q)

    print(query_kw.model_dump_json(ensure_ascii=False, indent=2))

if __name__ == "__main__":
    #test_extract_keywords_from_star()
    test_extract_keywords_from_query()