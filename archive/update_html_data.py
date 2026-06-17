#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
更新HTML文件，嵌入最新的数据（只统计C列）
"""

import json
import re

# 读取最新的数据
with open('song_data_processed.json', 'r', encoding='utf-8') as f:
    app_data = json.load(f)

print(f"数据验证：")
print(f"  - 总记录数: {app_data['metadata']['total_records']}")
print(f"  - 独立观众: {app_data['metadata']['unique_audiences']}")
print(f"  - Vaserkia的点歌次数: {app_data['total_leaderboard'][0]['count'] if app_data['total_leaderboard'][0]['audience'] == 'Vaserkia' else '不是第1名'}")

# 读取当前HTML文件
with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 找到数据部分并替换
# 找到 "const appData = " 开始的位置
start_marker = 'const appData = '
start_idx = html.find(start_marker)

if start_idx == -1:
    print("❌ 未找到数据部分！")
    exit(1)

# 找到数据结束的位置
data_start = start_idx + len(start_marker)
brace_count = 0
data_end = data_start
in_string = False
escape_char = False

for i in range(data_start, len(html)):
    char = html[i]
    
    if escape_char:
        escape_char = False
        continue
    
    if char == '\\' and in_string:
        escape_char = True
        continue
    
    if char == '"' and not escape_char:
        in_string = not in_string
    
    if not in_string:
        if char == '{':
            brace_count += 1
        elif char == '}':
            brace_count -= 1
            if brace_count == 0:
                data_end = i + 1
                break

print(f"\n找到数据部分：位置 {start_idx} 到 {data_end}")

# 生成新的数据字符串
new_data_str = json.dumps(app_data, ensure_ascii=False, indent=2)

# 替换数据部分
html_new = html[:start_idx + len(start_marker)] + new_data_str + html[data_end:]

# 保存更新后的HTML
with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html_new)

print(f"\n✅ HTML文件已更新！")
print(f"  - 数据已重新内嵌")
print(f"  - 文件大小: {len(html_new)} 字节")

# 验证更新是否成功
with open('index.html', 'r', encoding='utf-8') as f:
    verified_html = f.read()
    if 'Vaserkia' in verified_html and str(app_data['metadata']['total_records']) in verified_html:
        print(f"  - ✅ 数据已成功内嵌")
    else:
        print(f"  - ❌ 数据内嵌可能失败")
