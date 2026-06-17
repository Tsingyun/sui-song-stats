#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
重新生成完整的自包含HTML文件，修复所有问题
"""

import json
import re

# 读取最新的数据
with open('song_data_processed.json', 'r', encoding='utf-8') as f:
    app_data = json.load(f)

print(f"数据验证：")
print(f"  - 总记录数: {app_data['metadata']['total_records']}")
print(f"  - 月度排行榜: {len(app_data['monthly_leaderboard'])} 个月")
print(f"  - 季度排行榜: {len(app_data['quarterly_leaderboard'])} 个季度")
print(f"  - 年度排行榜: {len(app_data.get('yearly_leaderboard', {}))} 个年度")

# 读取当前HTML文件
with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. 修复重复声明的问题
html = html.replace('const appData = const appData = {', 'const appData = {')

# 2. 修复变量名冲突的bug
html = html.replace(
    'for (const a in rawData) rawData[a].sort((a, b) => b.date.localeCompare(a.date));',
    'for (const aud in rawData) rawData[aud].sort((a, b) => b.date.localeCompare(a.date));'
)

# 3. 移动总榜到年度排行榜之后
# 找到总榜section
total_section_start = html.find('<section id="total">')
if total_section_start == -1:
    print("❌ 未找到总榜section！")
else:
    # 找到总榜section的结束位置
    total_section_end = html.find('</section>', total_section_start) + len('</section>')
    
    # 提取总榜section
    total_section = html[total_section_start:total_section_end]
    
    # 从原位置删除
    html = html[:total_section_start] + html[total_section_end:]
    
    # 找到年度排行榜section的结束位置
    yearly_section_end = html.find('</section>', html.find('<section id="yearly"'))
    if yearly_section_end == -1:
        print("❌ 未找到年度排行榜section！")
    else:
        yearly_section_end += len('</section>')
        
        # 在年度排行榜之后插入总榜
        html = html[:yearly_section_end] + '\n' + total_section + '\n' + html[yearly_section_end:]
        
        print(f"✅ 已将总榜移动到年度排行榜之后")

# 4. 更新导航栏，将总榜链接移到最后
html = html.replace(
    '''            <li><a href="#total" class="nav-link">总榜</a></li>
            <li><a href="#monthly" class="nav-link">月度</a></li>
            <li><a href="#quarterly" class="nav-link">季度</a></li>
            <li><a href="#yearly" class="nav-link">年度</a></li>''',
    '''            <li><a href="#monthly" class="nav-link">月度</a></li>
            <li><a href="#quarterly" class="nav-link">季度</a></li>
            <li><a href="#yearly" class="nav-link">年度</a></li>
            <li><a href="#total" class="nav-link">总榜</a></li>'''
)

# 保存修复后的HTML
with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print(f"\n✅ HTML文件已修复！")
print(f"  - 修复了重复声明的问题")
print(f"  - 修复了变量名冲突的bug")
print(f"  - 已将总榜移动到年度排行榜之后")
print(f"  - 已更新导航栏顺序")

# 验证修复是否成功
with open('index.html', 'r', encoding='utf-8') as f:
    verified_html = f.read()
    
    # 检查是否还有重复声明
    if 'const appData = const appData = {' in verified_html:
        print(f"  - ❌ 仍有重复声明问题")
    else:
        print(f"  - ✅ 无重复声明问题")
    
    # 检查变量名冲突是否修复
    if 'for (const a in rawData) rawData[a].sort((a, b)' in verified_html:
        print(f"  - ❌ 变量名冲突未修复")
    else:
        print(f"  - ✅ 变量名冲突已修复")
    
    # 检查总榜位置
    total_pos = verified_html.find('<section id="total">')
    yearly_pos = verified_html.find('<section id="yearly">')
    if total_pos > yearly_pos:
        print(f"  - ✅ 总榜已在年度排行榜之后")
    else:
        print(f"  - ❌ 总榜位置不正确")
