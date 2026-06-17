#!/usr/bin/env python3
"""Embed song_data_processed.json into index.html, replacing existing appData block safely."""

import json, re

# 1. Load JSON data
with open('song_data_processed.json', 'r', encoding='utf-8') as f:
    raw_data = json.load(f)

# 2. Build JS assignment string
json_str = json.dumps(raw_data, ensure_ascii=False, indent=2)
# Indent inner lines for readability inside <script>
json_block = 'const appData = ' + json_str + ';'

# 3. Read HTML
with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 4. Replace the appData block using a robust regex
# Matches: const appData = { ... };\n        // Initialize
pattern = r'const appData = \{[\s\S]*?\};\s*\n\s*// Initialize'
replacement = json_block + '\n\n        // Initialize'
new_html, n = re.subn(pattern, replacement, html)

if n == 0:
    # Try alternate pattern - maybe the comment is different
    # Let's find the exact text around appData
    idx = html.find('const appData')
    if idx >= 0:
        snippet = html[idx:idx+200]
        print("Found const appData at position", idx)
        print("Surrounding text:")
        print(repr(snippet))
    else:
        print("ERROR: Could not find 'const appData' in HTML!")
    exit(1)
elif n > 1:
    print(f"WARNING: Replaced {n} matches (expected 1)")

# 5. Write back
with open('index.html', 'w', encoding='utf-8') as f:
    f.write(new_html)

# 6. Validate the result
with open('index.html', 'r', encoding='utf-8') as f:
    result = f.read()

m = re.search(r'const appData = (\{[\s\S]*?\});', result)
if m:
    try:
        parsed = json.loads(m.group(1))
        v = [x for x in parsed['total_leaderboard'] if x['audience']=='Vaserkia']
        print(f"✅ 验证通过！Vaserkia = {v[0]['count'] if v else '未找到'}")
        print(f"   总记录数: {parsed['metadata']['total_records']}")
    except Exception as e:
        print(f"❌ 嵌入后JSON无效: {e}")
else:
    print("❌ 无法在结果中找到 appData")

print(f"   替换了 {n} 处匹配")
print(f"   JSON块大小: {len(json_block)} 字符")
