import json
from collections import defaultdict
from datetime import datetime

with open('song_data_processed.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

raw_data = data['raw_data']
metadata = data['metadata']

# Feature 1: Calendar Heatmap Data
daily_counts = defaultdict(int)
for entry in raw_data:
    date = entry['date']
    daily_counts[date] += 1

heatmap_data = []
for date_str, count in sorted(daily_counts.items()):
    heatmap_data.append({'date': date_str, 'count': count})

data['heatmap_data'] = heatmap_data

# Feature 2: Song Relationship Network
audience_songs = defaultdict(set)
for entry in raw_data:
    audience = entry['audience']
    song = entry['song']
    audience_songs[audience].add(song)

song_cooccurrence = defaultdict(int)
songs_set = list(set([e['song'] for e in raw_data]))

for i in range(len(songs_set)):
    for j in range(i+1, len(songs_set)):
        song1 = songs_set[i]
        song2 = songs_set[j]
        audiences_with_both = 0
        for audience, songs in audience_songs.items():
            if song1 in songs and song2 in songs:
                audiences_with_both += 1
        if audiences_with_both >= 2:
            key = (min(song1, song2), max(song1, song2))
            song_cooccurrence[key] = audiences_with_both

network_edges = []
for (song1, song2), weight in sorted(song_cooccurrence.items(), key=lambda x: -x[1])[:50]:
    network_edges.append({'source': song1, 'target': song2, 'weight': weight})

song_counts = defaultdict(int)
for entry in raw_data:
    song_counts[entry['song']] += 1

top_songs = sorted(song_counts.items(), key=lambda x: -x[1])[:30]
network_nodes = [{'id': song, 'count': count} for song, count in top_songs]

data['song_network'] = {
    'nodes': network_nodes,
    'edges': network_edges
}

# Feature 5: Achievement System
achievements = []

if data['total_leaderboard']:
    top_audience = data['total_leaderboard'][0]
    achievements.append({
        'id': 'song_king',
        'name': '点歌之王',
        'emoji': '👑',
        'description': f'{top_audience["audience"]} 以 {top_audience["count"]} 次点歌夺得冠军',
        'audience': top_audience['audience'],
        'count': top_audience['count']
    })

for item in data['total_leaderboard']:
    if item['count'] >= 100:
        achievements.append({
            'id': f'100club_{item["audience"]}',
            'name': '百首俱乐部',
            'emoji': '🎯',
            'description': f'{item["audience"]} 点歌 {item["count"]} 次，突破百首大关！',
            'audience': item['audience'],
            'count': item['count']
        })

start_date = datetime.strptime(metadata['date_range_start'], '%Y-%m-%d')
end_date = datetime.strptime(metadata['date_range_end'], '%Y-%m-%d')
days_active = (end_date - start_date).days
years_active = days_active / 365.25

if years_active >= 1:
    achievements.append({
        'id': 'anniversary_1',
        'name': '一周年纪念',
        'emoji': '📅',
        'description': f'岁己的点歌系统已经运行超过一年了！（{metadata["date_range_start"]} 至今）',
        'count': metadata['total_records']
    })

audience_month_counts = defaultdict(lambda: defaultdict(int))
for entry in raw_data:
    audience = entry['audience']
    month = entry['date'][:7]
    audience_month_counts[audience][month] += 1

most_consistent = None
max_months = 0
for audience, months in audience_month_counts.items():
    if len(months) > max_months:
        max_months = len(months)
        most_consistent = audience

if most_consistent:
    achievements.append({
        'id': 'consistent_audience',
        'name': '忠实观众',
        'emoji': '🌟',
        'description': f'{most_consistent} 在 {max_months} 个不同的月份里点过歌，是最忠实的观众！',
        'audience': most_consistent,
        'count': max_months
    })

data['achievements'] = achievements

# Feature 6: Audience Level System
def calculate_level(count):
    if count >= 100:
        return 5, 'Lv.5'
    elif count >= 61:
        return 4, 'Lv.4'
    elif count >= 31:
        return 3, 'Lv.3'
    elif count >= 11:
        return 2, 'Lv.2'
    else:
        return 1, 'Lv.1'

for item in data['total_leaderboard']:
    level_num, level_str = calculate_level(item['count'])
    item['level'] = level_num
    item['level_str'] = level_str

audience_levels = {}
for item in data['total_leaderboard']:
    audience_levels[item['audience']] = {
        'level': item['level'],
        'level_str': item['level_str'],
        'count': item['count']
    }

data['audience_levels'] = audience_levels

# Feature 14: Global Search Data
search_index = {
    'songs': list(set([e['song'] for e in raw_data])),
    'audiences': list(set([e['audience'] for e in raw_data])),
    'dates': list(set([e['date'] for e in raw_data]))
}

data['search_index'] = search_index

with open('song_data_processed.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print('Data processing complete!')
print(f'  Heatmap data: {len(heatmap_data)} days')
print(f'  Network nodes: {len(network_nodes)}, edges: {len(network_edges)}')
print(f'  Achievements: {len(achievements)}')
print(f'  Audience levels: {len(audience_levels)}')
print(f'  Search index: {len(search_index["songs"])} songs, {len(search_index["audiences"])} audiences')
