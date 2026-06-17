#!/usr/bin/env python3
"""Robustly replace appData block in index.html using brace matching."""

import json, re

# 1. Load correct JSON data (Vaserkia=94, 770 records)
with open('song_data_processed.json', 'r', encoding='utf-8') as f:
    raw_data = json.load(f)

json_str = json.dumps(raw_data, ensure_ascii=False, indent=2)
new_assignment = 'const appData = ' + json_str + ';'

# 2. Read HTML
with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 3. Find start of appData
start_marker = 'const appData = '
start_idx = content.find(start_marker)
if start_idx == -1:
    print("ERROR: 'const appData = ' not found!")
    exit(1)

print(f"Found 'const appData' at position {start_idx}")

# 4. Use brace matching to find the end of the JSON object
brace_start = start_idx + len(start_marker)
if content[brace_start] != '{':
    print(f"ERROR: Expected `{{` at position {brace_start}, got: {repr(content[brace_start:brace_start+5])}")
    exit(1)

depth = 0
in_string = False
escape_next = False
end_idx = None

for i in range(brace_start, len(content)):
    ch = content[i]
    
    if escape_next:
        escape_next = False
        continue
    if ch == '\\' and in_string:
        escape_next = True
        continue
    if ch == '"' and not escape_next:
        in_string = not in_string
        continue
    if in_string:
        continue
    if ch == '{':
        depth += 1
    elif ch == '}':
        depth -= 1
        if depth == 0:
            end_idx = i + 1  # Point to character after `}`
            print(f"Found matching `}}` at position {end_idx}")
            break

if end_idx is None:
    print("ERROR: Could not find matching `}}` for appData!")
    exit(1)

# Include the `;` that should be right after `}`
if end_idx < len(content) and content[end_idx] == ';':
    end_idx += 1

print(f"Old block length: {end_idx - start_idx} chars")

# 5. Replace
new_content = content[:start_idx] + new_assignment + content[end_idx:]

# 6. Write back
with open('index.html', 'w', encoding='utf-8') as f:
    f.write(new_content)

print(f"✅ Replacement complete! New file size: {len(new_content)} chars")

# 7. Validate the result
with open('index.html', 'r', encoding='utf-8') as f:
    result = f.read()

m = re.search(r'const appData = (\{[\s\S]*?\});', result)
if m:
    try:
        parsed = json.loads(m.group(1))
        v = [x for x in parsed['total_leaderboard'] if x['audience'] == 'Vaserkia']
        count = v[0]['count'] if v else 'NOT FOUND'
        print(f"✅ Validation passed! Vaserkia = {count}")
        print(f"   Total records: {parsed['metadata']['total_records']}")
    except Exception as e:
        print(f"❌ Embedded JSON is invalid: {e}")
        exit(1)
else:
    print("❌ Could not find appData in result HTML!")
    exit(1)
