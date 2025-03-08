import os
import random
import requests
from github import Github
from collections import defaultdict

# **🔗 拉取 URL 数据**
URL = "https://jlips.jzhou.dns.navy/proxyip.txt?token=JLiptq"
response = requests.get(URL)

if response.status_code != 200:
    print("❌ 无法拉取数据，状态码:", response.status_code)
    exit(1)

# **📥 解析数据**
lines = response.text.strip().split("\n")
country_dict = defaultdict(list)

# **📌 处理数据，按国家分组**
for line in lines:
    parts = line.strip().split("\t")  # 按 Tab 分割
    if len(parts) == 3:  # 确保格式正确
        ip, port, country = parts
        formatted_line = f"{ip}:{port}#{country}"
        country_dict[country].append(formatted_line)

# **🎯 选择每个国家的 N 个 IP**
N = 5  # 每个国家随机选 5 个
output_lines = []

for country, ip_list in country_dict.items():
    selected_ips = random.sample(ip_list, min(N, len(ip_list)))  # 随机选取
    output_lines.extend(selected_ips)

# **📂 保存到本地文件**
output_file = "yxym.txt"
with open(output_file, "w", encoding="utf-8") as f:
    f.write("\n".join(output_lines) + "\n")

print(f"✅ 已筛选 {N} 个 IP/国家，保存到 {output_file}")

# **🔑 连接 GitHub**
GITHUB_TOKEN = os.getenv("MY_GITHUB_TOKEN")  # GitHub Secret
if not GITHUB_TOKEN:
    print("❌ Error: MY_GITHUB_TOKEN 未设置")
    exit(1)

REPO_NAME = "jzhou9096/jilianip"  # 你的 GitHub 私库
FILE_PATH = "yxym.txt"  # GitHub 仓库中的路径

# **🚀 推送到 GitHub**
g = Github(GITHUB_TOKEN)
repo = g.get_repo(REPO_NAME)

try:
    file = repo.get_contents(FILE_PATH)
    repo.update_file(FILE_PATH, "🔄 更新筛选 IP", "\n".join(output_lines), file.sha)
    print("✅ 文件已更新到 GitHub")
except:
    repo.create_file(FILE_PATH, "🆕 初次上传筛选 IP", "\n".join(output_lines))
    print("✅ 文件已创建并上传到 GitHub")
