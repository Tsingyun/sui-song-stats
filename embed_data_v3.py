#!/usr/bin/env python3
"""Embed song_data_processed.json into index.html safely."""

import json, re

# 1. Load correct JSON data (Vaserkia=94, 770 records)
with open('song_data_processed.json', 'r', encoding='utf-8') as f:
    raw_data = json.load(f)

json_str = json.dumps(raw_data, ensure_ascii=False, indent=2)
new_block = '        const appData = ' + json_str + ';\n\n        // Initialize'

# 2. Read HTML
with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 3. Find start and end of existing appData block
start_marker = '        const appData = '
start_idx = content.find(start_marker)
if start_idx == -1:
    print("ERROR: Could not find 'const appData' in HTML!")
    exit(1)

# Find the end: `};\n\n        // Initialize`
# We need to find the `};` that is followed by `// Initialize`
# Strategy: find `// Initialize` after start_idx, then walk back to find the `};`
init_marker = '        // Initialize'
init_idx = content.find(init_marker, start_idx)
if init_idx == -1:
    print("ERROR: Could not find '// Initialize' after appData!")
    exit(1)

# Walk back from init_idx to find the `};` that ends appData
# The `};` should be right before `\n\n        // Initialize`
# Actually the format is: `};\n\n        // Initialize`
# So we search for `;\n\n        // Initialize` and the `}` is right before `;`
end_search = content.rfind(';\n\n        // Initialize', start_idx, init_idx + 50)
if end_search == -1:
    print("ERROR: Could not find end of appData block!")
    exit(1)

end_idx = end_search + 1  # Point to the character after `;`

# 4. Replace
new_content = content[:start_idx] + new_block + content[end_idx:]

# 5. Write back
with open('index.html', 'w', encoding='utf-8') as f:
    f.write(new_content)

# 6. Validate
with open('index.html', 'r', encoding='utf-8') as f:
    result = f.read()

m = re.search(r'const appData = (\{[\s\S]*?\});', result)
if m:
    try:
        parsed = json.loads(m.group(1))
        v = [x for x in parsed['total_leaderboard'] if x['audience']=='Vaserkia']
        print(f"✅ 验证通过！Vaserkia = {v[0]['count'] if v else '未找到'}")
        print(f"   总记录数: {parsed['metadata']['total_records']}")
        print(f"   替换完成，文件大小: {len(new_content)} 字符")
    except Exception as e:
        print(f"❌ 嵌入后JSON无效: {e}")
else:
    print("❌ 无法在结果中找到 appData")
