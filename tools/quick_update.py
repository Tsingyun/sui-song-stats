"""增量更新歌单数据——仅适用于日常新增少量歌曲，不跑全量重算"""
import json
from collections import defaultdict, Counter
from datetime import date

with open('song_data_processed.json', 'r', encoding='utf-8') as f:
    d = json.load(f)

# ===== 1. 新增歌曲（手动编辑此处）=====
new_records = []

# ===== 2. 去重并追加 =====
seen = {(r['date'], r['song'], r['audience']) for r in d['raw_data']}
added = 0
for r in new_records:
    key = (r['date'], r['song'], r['audience'])
    if key not in seen:
        d['raw_data'].append(r)
        seen.add(key)
        added += 1
print(f'新增: {added} 条 ({len(d["raw_data"])} total)')

# ===== 3. 增量更新 heatmap（只更新受影响的日期）=====
affected_dates = set(r['date'] for r in new_records)
for h in d['heatmap_data']:
    if h['date'] in affected_dates:
        h['count'] = sum(1 for r in d['raw_data'] if r['date'] == h['date'])
for dt in affected_dates:
    if not any(h['date'] == dt for h in d['heatmap_data']):
        d['heatmap_data'].append({'date': dt, 'count': 1})
d['heatmap_data'].sort(key=lambda x: x['date'])

# ===== 4. 增量更新月度榜单（只刷新涉及的新月份）=====
affected_months = set(r['date'][:7] for r in new_records)
for m in affected_months:
    counter = Counter(r['audience'] for r in d['raw_data'] if r['date'][:7] == m)
    d['monthly_leaderboard'][m] = [{'audience': aud, 'count': cnt} for aud, cnt in counter.most_common()]

# ===== 5. 增量更新季度榜 =====
from datetime import date as dt_type
affected_quarters = set()
for r in new_records:
    y, mo = r['date'][:4], int(r['date'][5:7])
    affected_quarters.add(f'{y}-Q{(mo-1)//3+1}')
for q in affected_quarters:
    year, quarter = q.split('-Q')
    y, qn = int(year), int(quarter)
    m_start = (qn-1)*3 + 1
    m_end = m_start + 2
    dates_in_q = []
    for r in d['raw_data']:
        ry, rm = int(r['date'][:4]), int(r['date'][5:7])
        if ry == y and m_start <= rm <= m_end:
            dates_in_q.append(r)
    # Only rebuild if the quarter already exists in data, otherwise skip (will be generated on next full run)
    if any(k.startswith(q) for k in d['quarterly_leaderboard']):
        counter = Counter(r['audience'] for r in dates_in_q)
        d['quarterly_leaderboard'][q] = [{'audience': aud, 'count': cnt} for aud, cnt in counter.most_common()]

# ===== 6. 增量更新年度榜 =====
affected_years = set(r['date'][:4] for r in new_records)
for y in affected_years:
    counter = Counter(r['audience'] for r in d['raw_data'] if r['date'][:4] == y)
    d['yearly_leaderboard'][y] = [{'audience': aud, 'count': cnt} for aud, cnt in counter.most_common()]

# ===== 7. 全量更新 total/song leaderboard（快速，只需遍历一次）=====
total = Counter(r['audience'] for r in d['raw_data'])
d['total_leaderboard'] = [{'audience': aud, 'count': cnt} for aud, cnt in total.most_common()]
song = Counter(r['song'] for r in d['raw_data'])
d['song_leaderboard'] = [{'song': s, 'count': cnt} for s, cnt in song.most_common()]

# ===== 8. 更新 audience_levels =====
def lvl(c):
    if c >= 100: return 5
    if c >= 61: return 4
    if c >= 31: return 3
    if c >= 11: return 2
    return 1
d['audience_levels'] = {item['audience']: {'level': lvl(item['count']), 'count': item['count']} for item in d['total_leaderboard']}

# ===== 9. 更新 last_request_dates =====
for r in new_records:
    d['last_request_dates'][r['audience']] = max(r['date'], d['last_request_dates'].get(r['audience'], ''))

# ===== 10. 更新 search_index（只追加新歌/新观众）=====
si = d['search_index']
song_set = set(si['songs'])
aud_set = set(si['audiences'])
date_set = set(si['dates'])
for r in new_records:
    song_set.add(r['song'])
    aud_set.add(r['audience'])
    date_set.add(r['date'])
si['songs'] = list(song_set)
si['audiences'] = list(aud_set)
si['dates'] = list(date_set)

d['data_version'] = date.today().isoformat()

with open('song_data_processed.json', 'w', encoding='utf-8') as f:
    json.dump(d, f, ensure_ascii=False, separators=(',', ':'))
print(f'Done — total={len(d["raw_data"])}, songs={len(si["songs"])}')
print('NOTE: similarity_matrix / champion_streaks / song_network / achievements 未更新')
print('如需刷新这些字段，请运行 tools/process_features.py')
