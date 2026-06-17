import json
from collections import defaultdict
from datetime import datetime

with open('song_data_processed.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Rename
for e in data['raw_data']:
    if e['audience'] == '丸山彩':
        e['audience'] = '灰獺'

# Recalculate total leaderboard
aud_counts = defaultdict(int)
for e in data['raw_data']:
    aud_counts[e['audience']] += 1

tl = sorted(aud_counts.items(), key=lambda x: -x[1])
data['total_leaderboard'] = [{'audience': a, 'count': c} for a, c in tl]

# Recalculate song leaderboard
song_counts = defaultdict(int)
for e in data['raw_data']:
    song_counts[e['song']] += 1
sl = sorted(song_counts.items(), key=lambda x: -x[1])
data['song_leaderboard'] = [{'song': s, 'count': c} for s, c in sl]

# Recalculate monthly leaderboard
ml = defaultdict(lambda: defaultdict(int))
for e in data['raw_data']:
    ml[e['date'][:7]][e['audience']] += 1
data['monthly_leaderboard'] = {m: [{'audience': a, 'count': c} for a, c in sorted(d.items(), key=lambda x: -x[1])] for m, d in ml.items()}

# Recalculate quarterly
ql = defaultdict(lambda: defaultdict(int))
for e in data['raw_data']:
    y, m = e['date'][:4], int(e['date'][5:7])
    q = y + '-Q' + str((m-1)//3 + 1)
    ql[q][e['audience']] += 1
data['quarterly_leaderboard'] = {q: [{'audience': a, 'count': c} for a, c in sorted(d.items(), key=lambda x: -x[1])] for q, d in ql.items()}

# Recalculate yearly
yl = defaultdict(lambda: defaultdict(int))
for e in data['raw_data']:
    yl[e['date'][:4]][e['audience']] += 1
data['yearly_leaderboard'] = {y: [{'audience': a, 'count': c} for a, c in sorted(d.items(), key=lambda x: -x[1])] for y, d in yl.items()}

# Recalculate trends
trends = defaultdict(int)
for e in data['raw_data']:
    trends[e['date'][:7]] += 1
data['trend_data'] = dict(trends)

# Recalculate audience levels
def lvl(c):
    if c >= 100: return 5
    if c >= 61: return 4
    if c >= 31: return 3
    if c >= 11: return 2
    return 1

for item in data['total_leaderboard']:
    item['level'] = lvl(item['count'])

data['audience_levels'] = {item['audience']: {'level': item['level'], 'count': item['count']} for item in data['total_leaderboard']}

# Update metadata
data['metadata']['unique_audiences'] = len(aud_counts)

# Update search index
data['search_index']['audiences'] = list(set(e['audience'] for e in data['raw_data']))

# Update achievements
ach = data.get('achievements', [])
for a in ach:
    if a.get('audience') == '丸山彩':
        a['audience'] = '灰獺'
        a['desc'] = a['desc'].replace('丸山彩', '灰獺')

data['achievements'] = ach

# Save
with open('song_data_processed.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f'✅ Renamed 丸山彩 -> 灰獺')
print(f'   Total records: {len(data["raw_data"])}')
print(f'   Unique audiences: {data["metadata"]["unique_audiences"]}')
print(f'   New user 灰獺 count: {aud_counts.get("灰獺", 0)}')
