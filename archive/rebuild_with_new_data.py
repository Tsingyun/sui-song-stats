"""
添加新点歌数据 + 重新计算所有榜单 + 从模板重建HTML
新数据来源：用户截图 (2026-06-16)
  - 好久不见 | 大笨酱
  - Syrup | 无响应失败小熊
"""
import json
from collections import defaultdict
from datetime import datetime

# === 1. 读取现有数据 ===
with open('song_data_processed.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

raw = data['raw_data']

# === 2. 添加新记录 ===
new_entries = [
    {"date": "2026-06-16", "song": "好久不见", "audience": "大笨酱"},
    {"date": "2026-06-16", "song": "Syrup", "audience": "无响应失败小熊"},
]
raw.extend(new_entries)
print(f"✅ 添加了 {len(new_entries)} 条新记录，总记录数: {len(raw)}")

def parse_ym(d):
    """从日期提取 YYYY-MM，兼容中文和ISO格式"""
    import re
    m = re.match(r'(\d{4})[年\-](\d{1,2})', d)
    if m:
        return f"{m.group(1)}-{int(m.group(2)):02d}"
    return d[:7]

def parse_year(d):
    """提取年份"""
    return d[:4] if d[4] in '-_' else d[:4]

# === 3. 重新计算所有统计 ===

# Metadata
all_audiences = set(r['audience'] for r in raw)
all_songs = set(r['song'] for r in raw)
dates = [r['date'] for r in raw]
data['metadata'] = {
    "total_records": len(raw),
    "unique_audiences": len(all_audiences),
    "unique_songs": len(all_songs),
    "date_range_start": min(dates),
    "date_range_end": max(dates),
}

# Monthly leaderboard
monthly = defaultdict(lambda: defaultdict(int))
for r in raw:
    d = parse_ym(r['date'])
    monthly[d][r['audience']] += 1
data['monthly_leaderboard'] = {
    m: [{"audience": a, "count": c} for a, c in sorted(v.items(), key=lambda x: -x[1])]
    for m, v in sorted(monthly.items())
}

# Quarterly leaderboard
def get_quarter(date_str):
    ym = parse_ym(date_str)
    y, m = ym.split('-')
    q = (int(m) - 1) // 3 + 1
    return f"{y}-Q{q}"

quarterly = defaultdict(lambda: defaultdict(int))
for r in raw:
    q = get_quarter(r['date'])
    quarterly[q][r['audience']] += 1
data['quarterly_leaderboard'] = {
    q: [{"audience": a, "count": c} for a, c in sorted(v.items(), key=lambda x: -x[1])]
    for q, v in sorted(quarterly.items())
}

# Yearly leaderboard
yearly = defaultdict(lambda: defaultdict(int))
for r in raw:
    y = parse_year(r['date'])
    yearly[y][r['audience']] += 1
data['yearly_leaderboard'] = {
    y: [{"audience": a, "count": c} for a, c in sorted(v.items(), key=lambda x: -x[1])]
    for y, v in sorted(yearly.items())
}

# Total leaderboard
total_counts = defaultdict(int)
for r in raw:
    total_counts[r['audience']] += 1
data['total_leaderboard'] = [
    {"audience": a, "count": c} for a, c in sorted(total_counts.items(), key=lambda x: -x[1])
]

# Song leaderboard
song_counts = defaultdict(int)
for r in raw:
    song_counts[r['song']] += 1
data['song_leaderboard'] = [
    {"song": s, "count": c} for s, c in sorted(song_counts.items(), key=lambda x: -x[1])
]

# Audience preferences (top songs per audience, top12 audiences)
prefs = defaultdict(lambda: defaultdict(int))
for r in raw:
    prefs[r['audience']][r['song']] += 1
top_audiences = [a['audience'] for a in data['total_leaderboard'][:12]]
data['audience_preferences'] = {
    a: [{"song": s, "count": c} for s, c in sorted(prefs[a].items(), key=lambda x: -x[1])[:8]]
    for a in top_audiences if a in prefs
}

# Trend data (monthly counts)
trend_monthly = defaultdict(int)
for r in raw:
    trend_monthly[parse_ym(r['date'])] += 1
data['trend_data'] = dict(sorted(trend_monthly.items()))

# Verify 小熊2026 data
bear_2026 = sum(1 for r in raw if r['audience'] == '无响应失败小熊' and parse_year(r['date']) == '2026')
print(f"🐻 无响应失败小熊 2026年点歌数: {bear_2026}")

daban_2026 = sum(1 for r in raw if r['audience'] == '大笨酱' and parse_year(r['date']) == '2026')
print(f"🍳 大笨酱 2026年点歌数: {daban_2026}")

vaserkia_total = sum(1 for r in raw if r['audience'] == 'Vaserkia')
print(f"💎 Vaserkia 总计: {vaserkia_total}")

# === 4. 写回JSON ===
with open('song_data_processed.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
print("✅ JSON数据已更新")

# === 5. 重建HTML ===
with open('template.html', 'r', encoding='utf-8') as f:
    template = f.read()

appData_str = 'const appData = ' + json.dumps(data, ensure_ascii=False, indent=2) + ';'
html = template.replace('{{APPDATA}}', appData_str)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
print(f"✅ HTML已重建 ({len(html)} bytes)")

# === 6. 验证JS语法 ===
import subprocess
js_code = html.split('<script>')[1].split('</script>')[0]
try:
    subprocess.run(
        ['C:/Users/Tsing/.workbuddy/binaries/node/versions/22.22.2/node.exe', '-e', js_code],
        capture_output=True, text=True, check=True
    )
    print("✅ JS语法验证通过!")
except subprocess.CalledProcessError as e:
    print(f"❌ JS语法错误: {e.stderr[:300]}")
