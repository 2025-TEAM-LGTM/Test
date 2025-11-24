# query_cli.py
import sys, json
from prompt_to_query import parse_prompt  # 이미 만든 체인 사용

BANNER = """\
[Query CLI] 자연어 조건을 QuerySchema(JSON)로 변환합니다.
여러 줄 입력 가능. 입력을 마치려면 빈 줄에서 Enter (또는 Ctrl+D) 를 누르세요.
--------------------------------------------------------------------------------
"""

def read_multiline() -> str:
    print(BANNER)
    lines = []
    try:
        while True:
            line = input()
            if line.strip() == "":
                break
            lines.append(line)
    except EOFError:
        pass
    return "\n".join(lines).strip()

def main():
    nl = read_multiline()
    if not nl:
        print("입력이 비었습니다. 종료합니다.")
        sys.exit(0)

    try:
        q = parse_prompt(nl)  # LangChain 통해 구조화
        data = q.model_dump()  # Python dict
        print("\n=== 구조화 결과(JSON) ===")
        print(json.dumps(data, ensure_ascii=False, indent=2))
    except Exception as e:
        print(f"[에러] {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
