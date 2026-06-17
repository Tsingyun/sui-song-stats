#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
只统计C列（哪个饼子点到的？）的观众数据
"""

import pandas as pd
import json
from datetime import datetime
from collections import defaultdict

# 读取Excel文件的第二个工作表
file_path = r"C:/Users/Tsing/Downloads/岁己数据统计.xlsx"
df = pd.read_excel(file_path, sheet_name=1)  # 岁己今天唱什么

print("重新处理原始点歌数据（只统计C列）...")
print(f"总记录数: {len(df)}")

# 转换Excel日期序列号为实际日期
def convert_excel_date(excel_serial):
    if pd.isna(excel_serial):
        return None
    try:
        base_date = datetime(1899, 12, 30)
        return (base_date + pd.Timedelta(days=int(excel_serial))).strftime('%Y-%m-%d')
    except:
        return None

# 处理合并单元格：向前填充日期
print("\n处理日期合并单元格...")
current_date = None
processed_data = []

for idx, row in df.iterrows():
    # 检查日期列
    date_serial = row.iloc[0]  # A列：日期
    
    if pd.notna(date_serial):
        current_date = convert_excel_date(date_serial)
    
    if current_date is None:
        continue
    
    # 获取歌曲名
    song_name = row.iloc[1]  # B列：歌曲名
    if pd.isna(song_name):
        continue
    
    song_name = str(song_name).strip()
    if not song_name:
        continue
    
    # 只统计C列：哪个饼子点到的？
    audiences = []
    primary_audience = row.iloc[2]
    if pd.notna(primary_audience):
        audience_name = str(primary_audience).strip()
        if audience_name and audience_name not in ['nan', 'NaN', '']:
            audiences.append(audience_name)
    
    # 为每位观众创建一条记录
    for audience in audiences:
        if audience and audience != '':
            processed_data.append({
                'date': current_date,
                'song': song_name,
                'audience': audience,
                'month': current_date[:7],
                'quarter': f"{current_date[:4]}-Q{((int(current_date[5:7]) - 1) // 3 + 1)}",
                'year': current_date[:4]
            })

print(f"处理后的点歌记录数: {len(processed_data)}")

# 验证：统计Vaserkia的点歌次数
vaserkia_count = sum(1 for r in processed_data if r['audience'] == 'Vaserkia')
print(f"\n验证 - Vaserkia的点歌次数（只统计C列）: {vaserkia_count}")

# 统计：总排行榜
audience_total = defaultdict(int)
audience_songs = defaultdict(set)
song_count = defaultdict(int)

for req in processed_data:
    audience_total[req['audience']] += 1
    audience_songs[req['audience']].add(req['song'])
    song_count[req['song']] += 1

# 按月统计
monthly_stats = defaultdict(lambda: defaultdict(int))
for req in processed_data:
    monthly_stats[req['month']][req['audience']] += 1

# 按季度统计
quarterly_stats = defaultdict(lambda: defaultdict(int))
for req in processed_data:
    quarterly_stats[req['quarter']][req['audience']] += 1

# 按年度统计
yearly_stats = defaultdict(lambda: defaultdict(int))
for req in processed_data:
    yearly_stats[req['year']][req['audience']] += 1

# 观众喜好分析
audience_preferences = defaultdict(lambda: defaultdict(int))
for req in processed_data:
    audience_preferences[req['audience']][req['song']] += 1

# 准备输出数据
output_data = {
    'metadata': {
        'total_records': len(processed_data),
        'date_range': f"{min(r['date'] for r in processed_data)} 至 {max(r['date'] for r in processed_data)}",
        'unique_audiences': len(audience_total),
        'unique_songs': len(song_count),
        'note': '只统计C列（哪个饼子点到的？）'
    },
    'total_leaderboard': [
        {'rank': i+1, 'audience': a, 'count': c, 'unique_songs': len(audience_songs[a])}
        for i, (a, c) in enumerate(sorted(audience_total.items(), key=lambda x: -x[1])[:50])
    ],
    'song_leaderboard': [
        {'rank': i+1, 'song': s, 'count': c}
        for i, (s, c) in enumerate(sorted(song_count.items(), key=lambda x: -x[1])[:50])
    ],
    'monthly_leaderboard': {},
    'quarterly_leaderboard': {},
    'yearly_leaderboard': {},
    'audience_preferences': {},
    'monthly_trends': defaultdict(int),
    'raw_data': processed_data
}

# 月度排行榜
for month in sorted(monthly_stats.keys()):
    top_audiences = sorted(monthly_stats[month].items(), key=lambda x: -x[1])[:10]
    output_data['monthly_leaderboard'][month] = [
        {'rank': i+1, 'audience': a, 'count': c}
        for i, (a, c) in enumerate(top_audiences)
    ]

# 季度排行榜
for quarter in sorted(quarterly_stats.keys()):
    top_audiences = sorted(quarterly_stats[quarter].items(), key=lambda x: -x[1])[:10]
    output_data['quarterly_leaderboard'][quarter] = [
        {'rank': i+1, 'audience': a, 'count': c}
        for i, (a, c) in enumerate(top_audiences)
    ]

# 年度排行榜
for year in sorted(yearly_stats.keys()):
    top_audiences = sorted(yearly_stats[year].items(), key=lambda x: -x[1])[:10]
    output_data['yearly_leaderboard'][year] = [
        {'rank': i+1, 'audience': a, 'count': c}
        for i, (a, c) in enumerate(top_audiences)
    ]

# 观众喜好
for audience in list(audience_total.keys())[:20]:
    top_songs = sorted(audience_preferences[audience].items(), key=lambda x: -x[1])[:5]
    output_data['audience_preferences'][audience] = [
        {'song': s, 'count': c}
        for s, c in top_songs
    ]

# 月度趋势
for req in processed_data:
    output_data['monthly_trends'][req['month']] += 1

# 保存数据
with open('song_data_processed.json', 'w', encoding='utf-8') as f:
    json.dump(output_data, f, ensure_ascii=False, indent=2)

print("\n✅ 数据处理完成（只统计C列）！")
print(f"  - 总点歌记录: {output_data['metadata']['total_records']}")
print(f"  - 独立观众数: {output_data['metadata']['unique_audiences']}")
print(f"  - 独立歌曲数: {output_data['metadata']['unique_songs']}")
print(f"  - Vaserkia的点歌次数: {audience_total.get('Vaserkia', 0)}")
print("\n数据已保存到 song_data_processed.json")
