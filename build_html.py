import json, re

# 1. Read template
with open('template.html', 'r', encoding='utf-8') as f:
    template = f.read()

# 2. Read JSON data
with open('song_data_processed.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# 3. Build JS data string
appData_str = 'const appData = ' + json.dumps(data, ensure_ascii=False, indent=2) + ';'

# 4. Simple replacement - 100% reliable!
html = template.replace('{{APPDATA}}', appData_str)

# 5. Write output
with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print('✅ HTML generated successfully!')
print(f'   Template size: {len(template)} bytes')
print(f'   Data size: {len(appData_str)} bytes')
print(f'   Output size: {len(html)} bytes')

# 6. Validate JS syntax
import subprocess
js_code = html.split('<script>')[1].split('</script>')[0]
try:
    subprocess.run(
        ['C:/Users/Tsing/.workbuddy/binaries/node/versions/22.22.2/node.exe', '-e', js_code],
        capture_output=True, text=True, check=True
    )
    print('✅ JS syntax validated!')
except subprocess.CalledProcessError as e:
    print('❌ JS syntax error:')
    print(e.stderr[:500])
except Exception as e:
    print(f'⚠️  Could not validate JS: {e}')
