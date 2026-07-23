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
# Extract inline (no src=) <script> blocks, write each to a temp file, and
# run `node --check` (syntax-only, does NOT execute -> no DOM/runtime errors,
# no Windows command-line length limit). CDN <script src=...> tags are skipped.
import subprocess, tempfile, os, shutil, re

def _inline_scripts(h):
    out = []
    for m in re.finditer(r'<script\b([^>]*)>(.*?)</script>', h, re.DOTALL | re.IGNORECASE):
        attrs, body = m.group(1), m.group(2)
        if 'src=' in attrs:
            continue  # external / CDN script, nothing to syntax-check here
        if body.strip():
            out.append(body)
    return out

inline = _inline_scripts(html)
node = shutil.which('node') or 'C:/Users/Tsing/.workbuddy/binaries/node/versions/22.22.2/node.exe'
if not inline:
    print('⚠️  No inline <script> found, skipped JS validation')
elif not os.path.exists(node):
    print(f'⚠️  node not found ({node}), skipped JS validation')
else:
    all_ok = True
    for i, code in enumerate(inline):
        tmp = os.path.join(tempfile.gettempdir(), f'_sui_jscheck_{i}.js')
        with open(tmp, 'w', encoding='utf-8') as tf:
            tf.write(code)
        try:
            subprocess.run([node, '--check', tmp], capture_output=True, text=True, check=True)
        except subprocess.CalledProcessError as e:
            all_ok = False
            print(f'❌ JS syntax error in inline script #{i}:')
            print(e.stderr[:800])
        except Exception as e:
            all_ok = False
            print(f'⚠️  Could not validate JS: {e}')
        finally:
            try:
                os.remove(tmp)
            except OSError:
                pass
    if all_ok:
        print(f'✅ JS syntax validated ({len(inline)} inline script(s))!')
