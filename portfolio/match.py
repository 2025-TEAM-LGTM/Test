# match.py

from typing import Dict, List, Tuple
from keyword_schema import PortfolioKeywords


def _list_intersection_size(a: List[str], b: List[str]) -> int:
    return len(set(a) & set(b))


def score_portfolio(query: PortfolioKeywords, candidate: PortfolioKeywords) -> float:
    """
    query: 사용자의 의도(조건)를 담은 PortfolioKeywords
    candidate: 어떤 포트폴리오의 PortfolioKeywords

    두 JSON을 비교해서 점수를 계산한다.
    점수가 높을수록 "사용자가 찾는 사람"에 더 잘 맞는 포트폴리오.
    """
    score = 0.0

    # 1) 도메인 (S.domain) 일치
    if query.S.domain and candidate.S.domain:
        if query.S.domain == candidate.S.domain:
            score += 3.0

    # 2) 역할 (T.role) 일치
    if query.T.role and candidate.T.role:
        if query.T.role == candidate.T.role:
            score += 5.0  # 역할이 잘 맞는 게 중요하다고 가정

    # 3) 하드 스킬 겹치는 개수
    hs_query = query.A.hard_skills or []
    hs_cand = candidate.A.hard_skills or []
    score += 2.0 * _list_intersection_size(hs_query, hs_cand)

    # 4) 목표(goal) 키워드 겹침
    goals_q = query.T.goal or []
    goals_c = candidate.T.goal or []
    score += 1.0 * _list_intersection_size(goals_q, goals_c)

    # 5) problem_type, impact, growth 등도 간단하게 겹치는 만큼 가산
    pt_q = query.S.problem_type or []
    pt_c = candidate.S.problem_type or []
    score += 1.0 * _list_intersection_size(pt_q, pt_c)

    impact_q = query.R.impact or []
    impact_c = candidate.R.impact or []
    score += 0.5 * _list_intersection_size(impact_q, impact_c)

    growth_q = query.R.growth or []
    growth_c = candidate.R.growth or []
    score += 0.5 * _list_intersection_size(growth_q, growth_c)

    return score


def rank_portfolios(
    query: PortfolioKeywords,
    candidates: Dict[int, PortfolioKeywords],
    top_k: int = 10,
) -> List[Tuple[int, float]]:
    """
    query: 사용자의 조건(JSON; PortfolioKeywords)
    candidates: { portfolio_project_id: PortfolioKeywords } 딕셔너리
    top_k: 상위 몇 개까지 가져올지

    return: [(portfolio_project_id, score), ...] score 내림차순
    """
    results: List[Tuple[int, float]] = []

    for pid, cand_kw in candidates.items():
        s = score_portfolio(query, cand_kw)
        results.append((pid, s))

    # 점수 내림차순 정렬
    results.sort(key=lambda x: x[1], reverse=True)

    return results[:top_k]
