import os
import random
import requests
from github import Github
from collections import defaultdict

# **🔗 目标数据 URL**
URL = "https://jlips.jzhou.dns.navy/proxyip.txt?token=JLiptq"

def fetch_webpage_content(url):
    import requests
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.text
    except requests.RequestException as e:
        print(f"Error fetching webpage: {e}")
        return None

# **📌 解析数据**
lines = response.text.strip().split("\n")
country_dict = defaultdict(list)

for line in lines:
    parts = line.strip().split("\t")  # 按 Tab 分割
    if len(parts) == 3:
        ip, port, country = parts
        formatted_line = f"{ip}:{port}#{country}"
        country_dict[country].append(formatted_line)

# **🎯 每个国家随机选 N 个 IP**
N = 5
output_lines = []
for country, ip_list in country_dict.items():
    selected_ips = random.sample(ip_list, min(N, len(ip_list)))
    output_lines.extend(selected_ips)

# **📂 保存到本地**
output_file = "yxym.txt"
with open(output_file, "w", encoding="utf-8") as f:
    f.write("\n".join(output_lines) + "\n")

print(f"✅ 已筛选 {N} 个 IP/国家，保存到 {output_file}")

# **🔑 连接 GitHub**
GITHUB_TOKEN = os.getenv("MY_GITHUB_TOKEN")
if not GITHUB_TOKEN:
    print("❌ Error: MY_GITHUB_TOKEN 未设置")
    exit(1)

REPO_NAME = "jzhou9096/jilianip"
FILE_PATH = "yxym.txt"

g = Github(GITHUB_TOKEN)
repo = g.get_repo(REPO_NAME)

# **🚀 推送到 GitHub**
try:
    file = repo.get_contents(FILE_PATH)  # 先尝试获取文件
    repo.update_file(FILE_PATH, "🔄 更新 IP", "\n".join(output_lines), file.sha)
    print("✅ GitHub 文件已更新")
except Exception as e:
    print("⚠️ 文件不存在，尝试创建新文件")
    repo.create_file(FILE_PATH, "🆕 初次上传 IP", "\n".join(output_lines))
    print("✅ GitHub 文件已创建")
