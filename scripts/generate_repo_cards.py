import re
import sys

README_PATH = "README.md"
CARD_TEMPLATE = "[![{repo_name}]({svg_path})]({repo_url})"

def generate_card(repo_url: str) -> str:
    """根据仓库URL生成完整的Markdown图片链接"""
    # 提取用户名和仓库名
    match = re.match(r"https?://github\.com/([^/]+)/([^/]+)", repo_url.strip())
    if not match:
        print(f"⚠️  Invalid repo URL: {repo_url}")
        return f"<!-- Invalid repo URL: {repo_url} -->"

    owner, repo = match.groups()
    svg_path = f"./profile/repos/{repo}.svg"
    return CARD_TEMPLATE.format(
        repo_name=repo,
        svg_path=svg_path,
        repo_url=repo_url.strip()
    )

def main():
    with open(README_PATH, "r", encoding="utf-8") as f:
        content = f.read()

    # 匹配 {{REPO_CARD:url}} 格式
    pattern = r"\{\{REPO_CARD:(https?://github\.com/[^}]+)\}\}"

    def replacer(m):
        return generate_card(m.group(1))

    new_content = re.sub(pattern, replacer, content)

    if new_content != content:
        with open(README_PATH, "w", encoding="utf-8") as f:
            f.write(new_content)
        print("✅ README.md updated with repo cards")
    else:
        print("ℹ️  No repo card placeholders found or no changes needed")

if __name__ == "__main__":
    main()