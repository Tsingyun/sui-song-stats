import json, sys
from collections import defaultdict, Counter
from datetime import datetime
from pypinyin import lazy_pinyin

def pinyin_sort_key(item):
    """Sort key: pinyin of audience/song for tiebreaking."""
    name = item.get('audience', '') or item.get('song', '')
    return ' '.join(lazy_pinyin(name))

with open('song_data_processed.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

rw = data['raw_data']
mt = data['metadata']

# --- Rebuild all leaderboards from raw_data ---
# Total leaderboard (with pinyin tiebreak)
total = Counter()
for e in rw:
    total[e['audience']] += 1
data['total_leaderboard'] = sorted(
    [{'audience': aud, 'count': cnt} for aud, cnt in total.items()],
    key=lambda x: (-x['count'], pinyin_sort_key(x))
)
data['song_leaderboard'] = sorted(
    [{'song': aud, 'count': cnt} for aud, cnt in Counter(e['song'] for e in rw).items()],
    key=lambda x: (-x['count'], pinyin_sort_key(x))
)

# Monthly leaderboard
monthly = defaultdict(Counter)
for e in rw:
    monthly[e['date'][:7]][e['audience']] += 1
data['monthly_leaderboard'] = {}
for m, counter in sorted(monthly.items()):
    entries = [{'audience': aud, 'count': cnt} for aud, cnt in counter.items()]
    entries.sort(key=lambda x: (-x['count'], pinyin_sort_key(x)))
    data['monthly_leaderboard'][m] = entries

# Quarterly leaderboard
quarterly = defaultdict(Counter)
for e in rw:
    y, m = e['date'][:4], e['date'][5:7]
    q = f'{y}-Q{(int(m)-1)//3+1}'
    quarterly[q][e['audience']] += 1
data['quarterly_leaderboard'] = {}
for q, counter in sorted(quarterly.items()):
    entries = [{'audience': aud, 'count': cnt} for aud, cnt in counter.items()]
    entries.sort(key=lambda x: (-x['count'], pinyin_sort_key(x)))
    data['quarterly_leaderboard'][q] = entries

# Yearly leaderboard
yearly = defaultdict(Counter)
for e in rw:
    yearly[e['date'][:4]][e['audience']] += 1
data['yearly_leaderboard'] = {}
for y, counter in sorted(yearly.items()):
    entries = [{'audience': aud, 'count': cnt} for aud, cnt in counter.items()]
    entries.sort(key=lambda x: (-x['count'], pinyin_sort_key(x)))
    data['yearly_leaderboard'][y] = entries

tl = data['total_leaderboard']

# --- Feature 1: Heatmap daily counts ---
daily = defaultdict(int)
for e in rw:
    daily[e['date']] += 1
data['heatmap_data'] = [{'date': d, 'count': c} for d, c in sorted(daily.items())]

# --- Feature 1b: Monthly trend series (always recompute from raw_data) ---
# WARNING: trends / trend_data used to be hand-maintained and drifted badly —
# 2025-04 off by one, 2026-06 frozen at 15/17 vs actual 37, and 2026-07~09 missing
# entirely (which also under-counted the quarterly/yearly cards). They MUST be
# derived from raw_data like every other field, never patched by hand.
monthly_counts = Counter()
for e in rw:
    monthly_counts[e['date'][:7]] += 1
trend_series = {m: monthly_counts[m] for m in sorted(monthly_counts)}
data['trends'] = dict(trend_series)
data['trend_data'] = dict(trend_series)

# --- Feature 2: Song network (co-occurrence) ---
aud_songs = defaultdict(set)
for e in rw:
    aud_songs[e['audience']].add(e['song'])

# Only process top 100 songs by count to keep it fast
song_cnt = defaultdict(int)
for e in rw:
    song_cnt[e['song']] += 1
top100 = sorted(song_cnt.items(), key=lambda x: -x[1])[:100]
top_song_set = set(s[0] for s in top100)

cooc = defaultdict(int)
slist = list(top_song_set)
for i in range(len(slist)):
    for j in range(i+1, len(slist)):
        s1, s2 = slist[i], slist[j]
        c = sum(1 for aud, ss in aud_songs.items() if s1 in ss and s2 in ss)
        if c >= 2:
            key = (min(s1, s2), max(s1, s2))
            cooc[key] = c

edges = sorted(cooc.items(), key=lambda x: -x[1])[:50]
data['song_network'] = {
    'nodes': [{'id': s, 'count': c} for s, c in sorted(song_cnt.items(), key=lambda x: -x[1])[:30]],
    'edges': [{'source': e[0][0], 'target': e[0][1], 'weight': e[1]} for e in edges]
}

# --- Feature 2b: Audience preferences (top songs per audience) ---
# WARNING: audience_preferences used to be hand-maintained and froze at 12 stale
# entries (wrong people, wrong counts). The UI renders total_leaderboard.slice(0,12),
# so derive it for the Top-20 (headroom) — never patch by hand again.
PREF_AUDIENCES = 20
PREF_SONGS = 8
aud_song_counter = defaultdict(Counter)
for e in rw:
    aud_song_counter[e['audience']][e['song']] += 1
prefs = {}
for item in tl[:PREF_AUDIENCES]:
    aud = item['audience']
    items = [{'song': s, 'count': c} for s, c in aud_song_counter[aud].items()]
    items.sort(key=lambda x: (-x['count'], x['song']))
    prefs[aud] = items[:PREF_SONGS]
data['audience_preferences'] = prefs

# --- Feature 2c: Similarity matrix (song-taste overlap between audiences) ---
# jaccard = |A∩B| / |A∪B| over each audience's set of DISTINCT songs.
# Previously hand-maintained (stale 30 pairs). Now recomputed from raw_data.
aud_names = [t['audience'] for t in tl]
sim = []
for i in range(len(aud_names)):
    s1 = aud_songs[aud_names[i]]
    if not s1:
        continue
    for j in range(i + 1, len(aud_names)):
        s2 = aud_songs[aud_names[j]]
        if not s2:
            continue
        overlap = len(s1 & s2)
        if overlap < 2:
            continue  # shared a single song once = noise, not a taste signal
        union = len(s1 | s2)
        sim.append({
            'a1': aud_names[i],
            'a2': aud_names[j],
            'overlap': overlap,
            'total1': len(s1),
            'total2': len(s2),
            'jaccard': round(overlap / union, 4),
        })
sim.sort(key=lambda x: (-x['jaccard'], -x['overlap']))
data['similarity_matrix'] = sim[:30]

# --- Feature 2d: Champion streaks (cross-month consecutive monthly championships) ---
# A "champion" of month M = who topped monthly_leaderboard[M] (ties all count).
# A streak = a run of CALENDAR-CONTIGUOUS months (2024-12 -> 2025-01 counts) where
# the same audience kept the crown; only runs >= 2 are reported. Each audience keeps
# its single LONGEST run (earliest one wins a tie) so the board stays one row/person.
# Previously hand-maintained and stale. Now recomputed from raw_data.
def _midx(m):
    y, mm = m.split('-')
    return int(y) * 12 + int(mm)

month_champs = defaultdict(set)
for m, entries in data['monthly_leaderboard'].items():
    if not entries:
        continue
    top = entries[0]['count']
    for e in entries:
        if e['count'] == top:
            month_champs[e['audience']].add(m)

champ_months_sorted = sorted(set(data['monthly_leaderboard'].keys()))
champ_streaks = []
for aud, months in month_champs.items():
    ms = sorted(months, key=_midx)
    best = None
    run = [ms[0]]
    for prev, cur in zip(ms, ms[1:]):
        if _midx(cur) == _midx(prev) + 1:
            run.append(cur)
        else:
            if best is None or len(run) > len(best):
                best = run
            run = [cur]
    if best is None or len(run) > len(best):
        best = run
    if len(best) >= 2:
        champ_streaks.append({'audience': aud, 'months': best, 'count': len(best)})
champ_streaks.sort(key=lambda x: (-x['count'], _midx(x['months'][0])))
data['champion_streaks'] = champ_streaks

# --- Feature 5: Achievements ---
ach = []

# Song King
if tl:
    top = tl[0]
    ach.append({'id':'song_king','name':'点歌之王','emoji':'👑','desc':f'{top["audience"]} 以 {top["count"]} 次点歌夺得冠军','audience':top['audience'],'count':top['count']})

# 100 Club
for item in tl:
    if item['count'] >= 100:
        ach.append({'id':f'100club_{item["audience"]}','name':'百首俱乐部','emoji':'🎯','desc':f'{item["audience"]} 点歌 {item["count"]} 次，突破百首大关！','audience':item['audience'],'count':item['count']})

# Anniversary
sd = datetime.strptime(mt['date_range_start'], '%Y-%m-%d')
ed = datetime.strptime(mt['date_range_end'], '%Y-%m-%d')
years = (ed - sd).days / 365.25
if years >= 1:
    ach.append({'id':'anniversary_1','name':'一周年纪念','emoji':'📅','desc':f'岁己的点歌系统已经运行超过一年了！（{mt["date_range_start"]} 至今）','count':mt['total_records']})

# Consistent audience
amc = defaultdict(lambda: defaultdict(int))
for e in rw:
    amc[e['audience']][e['date'][:7]] += 1
best_a, best_m = None, 0
for a, ms in amc.items():
    if len(ms) > best_m:
        best_m = len(ms)
        best_a = a
if best_a:
    ach.append({'id':'consistent','name':'忠实观众','emoji':'🌟','desc':f'{best_a} 在 {best_m} 个不同的月份里点过歌，是最忠实的观众！','audience':best_a,'count':best_m})

data['achievements'] = ach

# --- Feature 6: Audience levels ---
def lvl(c):
    if c >= 100: return 5
    if c >= 61: return 4
    if c >= 31: return 3
    if c >= 11: return 2
    return 1

for item in tl:
    item['level'] = lvl(item['count'])

data['audience_levels'] = {item['audience']: {'level': item['level'], 'count': item['count']} for item in tl}

# --- Feature 14: Search index ---
data['search_index'] = {
    'songs': list(set(e['song'] for e in rw)),
    'audiences': list(set(e['audience'] for e in rw)),
    'dates': list(set(e['date'] for e in rw))
}

# --- Feature 14b: Last request date per audience (always recompute from raw_data) ---
aud_last_date = {}
for e in rw:
    aud = e['audience']
    d = e['date']
    if aud not in aud_last_date or d > aud_last_date[aud]:
        aud_last_date[aud] = d
data['last_request_dates'] = aud_last_date

# --- Feature 15: Consecutive live-session streaks (per month) ---
# Rule (per user 2026-07-14 clarification): within a month, a streak = a maximal
# run of CONSECUTIVE REQUEST DAYS (days on which >=1 audience point-song was made,
# i.e. the raw_data dates) on which the SAME audience requested songs. length >= 2
# counts as a streak.
#
# A host-only live day (主播自己选歌、当天无任何点歌) between two of an audience's
# point-songs is TRANSPARENT — it does NOT break the streak, because that day offered
# no request opportunity. Only a REQUEST DAY on which this audience did NOT request
# breaks the run. Example: 1/1 A点歌 → 1/2 主播自唱(无点歌) → 1/3 A点歌 ⇒ A 触发
# 连续两场🔥. This is a per-month board feature only; cross-month runs are not chained.
def recompute_streaks(raw):
    req_days = sorted(set(e['date'] for e in raw))
    by_month = defaultdict(list)
    for e in raw:
        by_month[e['date'][:7]].append(e)  # YYYY-MM
    result = {}
    for m, recs in by_month.items():
        req_days_m = [d for d in req_days if d[:7] == m]
        aud_dates = defaultdict(lambda: defaultdict(list))
        for e in recs:
            aud_dates[e['audience']][e['date']].append(e['song'])
        entries = []
        n = len(req_days_m)
        for aud, dmap in aud_dates.items():
            i = 0
            while i < n:
                if req_days_m[i] in dmap:
                    j = i
                    while j + 1 < n and req_days_m[j + 1] in dmap:
                        j += 1
                    run = req_days_m[i:j + 1]
                    if len(run) >= 2:
                        entries.append({
                            'audience': aud,
                            'chain': run,
                            'songs': [dmap[dt] for dt in run],
                            'length': len(run),
                        })
                    i = j + 1
                else:
                    i += 1
        entries.sort(key=lambda x: (x['chain'][0], x['audience']))
        result[m] = entries
    return result

data['consecutive_streaks'] = recompute_streaks(rw)

# --- Sync metadata counts from raw_data (always recompute, never hardcode) ---
mt['total_records'] = len(rw)
mt['unique_audiences'] = len(set(e['audience'] for e in rw))
mt['unique_songs'] = len(set(e['song'] for e in rw))
all_dates = sorted(e['date'] for e in rw)
mt['date_range_start'] = all_dates[0] if all_dates else ''
mt['date_range_end'] = all_dates[-1] if all_dates else ''

# --- live_dates: union only, NEVER overwrite ---
# live_dates 含 103 天「有直播但无人点歌」的日期，这部分无法从 raw_data 派生。
# 若直接用 raw_data 覆盖会永久丢失它们 —— 只能做并集补齐（当前缺 2026-07-14 起 27 天）。
ld = set(data.get('live_dates') or [])
ld.update(e['date'] for e in rw)
data['live_dates'] = sorted(ld)

# --- data_stats: 纯派生快照，跟随 metadata（此前冻结在 793/78/491，已漂移） ---
data['data_stats'] = {
    'total_records': mt['total_records'],
    'unique_audiences': mt['unique_audiences'],
    'unique_songs': mt['unique_songs'],
    'date_range_start': mt['date_range_start'],
    'date_range_end': mt['date_range_end'],
}

with open('song_data_processed.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, separators=(',', ':'))

print(f'OK: heatmap={len(data["heatmap_data"])}d, nodes={len(data["song_network"]["nodes"])}, edges={len(data["song_network"]["edges"])}, ach={len(ach)}, lvls={len(data["audience_levels"])}, idx_songs={len(data["search_index"]["songs"])}')
