import os
import random
import requests
from github import Github
from collections import defaultdict

# **🔗 目标数据 URL**
URL = "https://jlips.jzhou.dns.navy/proxyip.txt?token=JLiptq"

# **📥 下载数据**
try:
    response = requests.get(URL, timeout=10)
    response.raise_for_status()
    data = response.text.strip()
    print(f"📥 下载的数据内容（完整）：\n{data}")
except requests.exceptions.RequestException as e:
    print(f"❌ 下载数据失败: {e}")
    exit(1)

# **检查数据是否为空**
if not data:
    print("⚠️ 下载的数据为空，检查 URL 或 token")
    exit(1)

# **📌 解析数据**
lines = data.split("\n")
country_dict = defaultdict(list)

for i, line in enumerate(lines):
    parts = line.strip().split("\t")  # 按 Tab 分割
    if len(parts) == 3:
        ip, port, country = parts
        formatted_line = f"{ip}:{port}#{country}"
        country_dict[country].append(formatted_line)
    else:
        print(f"⚠️ 第 {i+1} 行解析失败：{line}")  # 打印无法解析的行

# **打印解析出的国家 IP 数据**
print(f"🌍 解析出的国家数据（完整）：{dict(country_dict)}")

# **🎯 每个国家随机选 N 个 IP**
N = 5
output_lines = []
for country, ip_list in country_dict.items():
    if not ip_list:
        print(f"⚠️ {country} 没有可用的 IP，跳过")
        continue
    selected_ips = random.sample(ip_list, min(N, len(ip_list)))
    output_lines.extend(selected_ips)

# **检查解析结果**
if not output_lines:
    print("⚠️ 解析结果为空，检查数据格式")
    exit(1)

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

try:
    g = Github(GITHUB_TOKEN)
    repo = g.get_repo(REPO_NAME)

    # **🚀 推送到 GitHub**
    try:
        file = repo.get_contents(FILE_PATH)
        repo.update_file(FILE_PATH, "🔄 更新 IP", "\n".join(output_lines), file.sha)
        print("✅ GitHub 文件已更新")
    except Exception:
        print("⚠️ 文件不存在，尝试创建新文件")
        repo.create_file(FILE_PATH, "🆕 初次上传 IP", "\n".join(output_lines))
        print("✅ GitHub 文件已创建")

except Exception as e:
    print(f"❌ GitHub 操作失败: {e}")
    exit(1)
