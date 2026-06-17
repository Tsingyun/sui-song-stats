import pandas as pd
import json
from datetime import datetime
from collections import defaultdict

# 读取Excel文件的第二个工作表（原始数据）
file_path = r"C:/Users/Tsing/Downloads/岁己数据统计.xlsx"
df = pd.read_excel(file_path, sheet_name=1)  # 岁己今天唱什么

print("处理原始点歌数据...")
print(f"总记录数: {len(df)}")

# 转换Excel日期序列号为实际日期
def convert_excel_date(excel_serial):
    if pd.isna(excel_serial):
        return None
    try:
        # Excel日期从1899-12-30开始
        base_date = datetime(1899, 12, 30)
        return (base_date + pd.Timedelta(days=int(excel_serial))).strftime('%Y-%m-%d')
    except:
        return None

# 处理数据
song_requests = []  # 存储所有的点歌记录

for idx, row in df.iterrows():
    date_serial = row.iloc[0]  # A列：日期
    song_name = row.iloc[1]  # B列：歌曲名
    
    # 转换日期
    date_str = convert_excel_date(date_serial)
    if date_str is None or pd.isna(song_name):
        continue
    
    song_name = str(song_name).strip()
    if not song_name:
        continue
    
    # 收集所有点歌的观众（C列及之后）
    audiences = []
    
    # C列：哪个饼子点到的？
    primary_audience = row.iloc[2]
    if pd.notna(primary_audience):
        audiences.append(str(primary_audience).strip())
    
    # E列及之后：参与拼好歌的饼子（可能有多列）
    for col_idx in range(4, len(row)):  # 从E列开始
        audience = row.iloc[col_idx]
        if pd.notna(audience):
            audience_name = str(audience).strip()
            if audience_name and audience_name not in ['nan', 'NaN']:
                audiences.append(audience_name)
    
    # 去重
    audiences = list(set(audiences))
    
    # 为每位观众创建一条记录
    for audience in audiences:
        if audience and audience != '':
            song_requests.append({
                'date': date_str,
                'song': song_name,
                'audience': audience,
                'month': date_str[:7],  # YYYY-MM
                'quarter': f"{date_str[:4]}-Q{((int(date_str[5:7]) - 1) // 3 + 1)}"
            })

print(f"\n处理后的点歌记录数: {len(song_requests)}")

# 统计：总排行榜（观众点歌次数）
audience_total = defaultdict(int)
audience_songs = defaultdict(set)  # 每位观众点过的歌曲
song_count = defaultdict(int)  # 歌曲被点次数

for req in song_requests:
    audience_total[req['audience']] += 1
    audience_songs[req['audience']].add(req['song'])
    song_count[req['song']] += 1

# 按月统计
monthly_stats = defaultdict(lambda: defaultdict(int))
for req in song_requests:
    monthly_stats[req['month']][req['audience']] += 1

# 按季度统计
quarterly_stats = defaultdict(lambda: defaultdict(int))
for req in song_requests:
    quarterly_stats[req['quarter']][req['audience']] += 1

# 观众喜好分析（每位观众最喜欢点的歌曲类型）
audience_preferences = defaultdict(lambda: defaultdict(int))
for req in song_requests:
    audience_preferences[req['audience']][req['song']] += 1

# 准备输出数据
output_data = {
    'metadata': {
        'total_records': len(song_requests),
        'date_range': f"{min(r['date'] for r in song_requests)} 至 {max(r['date'] for r in song_requests)}",
        'unique_audiences': len(audience_total),
        'unique_songs': len(song_count)
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
    'audience_preferences': {},
    'monthly_trends': defaultdict(int),
    'raw_data': song_requests
}

# 月度排行榜（每个月TOP10）
for month in sorted(monthly_stats.keys()):
    top_audiences = sorted(monthly_stats[month].items(), key=lambda x: -x[1])[:10]
    output_data['monthly_leaderboard'][month] = [
        {'rank': i+1, 'audience': a, 'count': c}
        for i, (a, c) in enumerate(top_audiences)
    ]

# 季度排行榜（每季度TOP10）
for quarter in sorted(quarterly_stats.keys()):
    top_audiences = sorted(quarterly_stats[quarter].items(), key=lambda x: -x[1])[:10]
    output_data['quarterly_leaderboard'][quarter] = [
        {'rank': i+1, 'audience': a, 'count': c}
        for i, (a, c) in enumerate(top_audiences)
    ]

# 观众喜好（TOP20观众的点歌偏好）
for audience in list(audience_total.keys())[:20]:
    top_songs = sorted(audience_preferences[audience].items(), key=lambda x: -x[1])[:5]
    output_data['audience_preferences'][audience] = [
        {'song': s, 'count': c}
        for s, c in top_songs
    ]

# 月度趋势
for req in song_requests:
    output_data['monthly_trends'][req['month']] += 1

# 保存数据
with open('song_data_processed.json', 'w', encoding='utf-8') as f:
    json.dump(output_data, f, ensure_ascii=False, indent=2)

print("\n✅ 数据处理完成！")
print(f"  - 总点歌记录: {output_data['metadata']['total_records']}")
print(f"  - 时间范围: {output_data['metadata']['date_range']}")
print(f"  - 独立观众数: {output_data['metadata']['unique_audiences']}")
print(f"  - 独立歌曲数: {output_data['metadata']['unique_songs']}")
print("\n数据已保存到 song_data_processed.json")
