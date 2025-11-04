import requests
import json
import csv
import sys
import os

# === 获取命令行参数 ===
if len(sys.argv) != 2:
    print("用法: python report.py <issues_file.txt>")
    sys.exit(1)

issues_file = sys.argv[1]

# === 从文件读取 issue key 列表 ===
if not os.path.exists(issues_file):
    raise FileNotFoundError(f"{issues_file} 不存在！请先创建文本文件，每行一个 issue key。")

with open(issues_file, "r", encoding="utf-8") as f:
    issues = [line.strip() for line in f if line.strip()]

if not issues:
    raise ValueError(f"{issues_file} 里面没有有效的 issue key。")


# JIRA 基础 URL
jira_base = "https://jira.devtools.intel.com"

# JIRA REST API 基础路径
api_base = f"{jira_base}/rest/api/2/issue/"

# 从环境变量读取 PAT 更安全（推荐）
# export JIRA_PAT=xxxx
token = os.getenv("JIRA_PAT", "")

# HTTP 请求头
headers = {
    "Authorization": f"Bearer {token}",
    "Accept": "application/json"
}

# 输出 CSV 文件名
output_csv = "cwf.csv"

# === 开始处理 ===
data_rows = []

for issue_key in issues:
    issue_url = f"{api_base}{issue_key}"
    print(f"Fetching {issue_url} ...")

    try:
        response = requests.get(issue_url, headers=headers)
    except Exception as e:
        print(f"请求 {issue_key} 失败: {e}")
        continue

    if response.status_code != 200:
        print(f"请求 {issue_key} 失败，状态码: {response.status_code}")
        continue

    issue = response.json()
    fields = issue.get("fields", {})

    summary = fields.get("summary", "N/A")
    description = fields.get("description", "N/A")
    updated = fields.get("updated", "N/A")

    # 获取最后一条评论
    comments = fields.get("comment", {}).get("comments", [])
    if comments:
        last_comment = comments[-1]
        last_comment_author = last_comment.get("author", {}).get("displayName", "N/A")
        last_comment_body = last_comment.get("body", "")
        last_comment_time = last_comment.get("updated", "N/A")
        last_comment_text = f"{last_comment_author}: {last_comment_body}"
    else:
        last_comment_text = "No comments"

    # 构造 JIRA 网页链接
    jira_link = f"{jira_base}/browse/{issue_key}"

    data_rows.append([summary, jira_link, description, last_comment_time, last_comment_text])

# === 写入 CSV 文件 ===
with open(output_csv, "w", newline='', encoding="utf-8") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Summary", "JIRA Link", "Description", "Last update", "Last comment"])
    writer.writerows(data_rows)

print(f"\n✅ 已生成 CSV 文件: {output_csv}")

