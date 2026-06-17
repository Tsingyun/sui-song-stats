"""Generate a self-contained HTML file with data embedded inline."""
import json

# Read the processed data
with open('song_data_processed.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Read the current HTML
with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Replace the fetch-based loading with embedded data
# Find and replace the loadData function and DOMContentLoaded handler
embedded_js = f"""
    // ============================================
    // DATA (embedded for offline use)
    // ============================================
    
    let appData = {json.dumps(data, ensure_ascii=False, indent=2)};
    
    let rawData = null; // Store raw data for modal
    
    // Process raw data for modal
    rawData = {{}};
    appData.raw_data.forEach(record => {{
        const audience = record.audience;
        if (!rawData[audience]) {{
            rawData[audience] = [];
        }}
        rawData[audience].push({{
            song: record.song,
            date: record.date
        }});
    }});
    
    // Sort each audience's songs by date
    for (const audience in rawData) {{
        rawData[audience].sort((a, b) => b.date.localeCompare(a.date));
    }}
    
    async function loadData() {{
        initApp();
    }}
"""

# Replace the old data loading section in the HTML
old_section_start = "// ============================================\n        // DATA LOADING"
old_section_end = "document.addEventListener('DOMContentLoaded', loadData);"

# Build new content
new_html = html.replace(old_section_start, embedded_js.strip())

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(new_html)

print("Done! index.html is now self-contained.")
