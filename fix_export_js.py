with open('template.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Find the toggleExportMenu function and replace it with a version
# that uses programmatic event handlers instead of inline onclick

old_func = '''                menu.innerHTML = '<div class="export-menu-divider">截图</div>' +
                    '<button class="export-menu-item" onclick="doExportScreenshot(\\\\'' + sectionId + '\\\\', 10)">截图 · 前10名</button>' +
                    '<button class="export-menu-item" onclick="doExportScreenshot(\\\\'' + sectionId + '\\\\', 0)">截图 · 完整榜单</button>' +
                    '<div class="export-menu-divider">数据文件</div>' +
                    '<button class="export-menu-item" onclick="doExportData(\\\\'' + sectionId + '\\\\', 'xlsx')">导出 XLSX</button>' +
                    '<button class="export-menu-item" onclick="doExportData(\\\\'' + sectionId + '\\\\', 'csv')">导出 CSV</button>' +
                    '<button class="export-menu-item" onclick="doExportData(\\\\'' + sectionId + '\\\\', 'json')">导出 JSON</button>';'''

# The correct version uses programmatic click handlers
new_func = '''                var sid = sectionId;
                menu.innerHTML = '<div class="export-menu-divider">截图</div>' +
                    '<button class="export-menu-item" data-action="screenshot" data-limit="10">截图 · 前10名</button>' +
                    '<button class="export-menu-item" data-action="screenshot" data-limit="0">截图 · 完整榜单</button>' +
                    '<div class="export-menu-divider">数据文件</div>' +
                    '<button class="export-menu-item" data-action="xlsx">导出 XLSX</button>' +
                    '<button class="export-menu-item" data-action="csv">导出 CSV</button>' +
                    '<button class="export-menu-item" data-action="json">导出 JSON</button>';
                // Attach click handlers programmatically
                var items = menu.querySelectorAll('.export-menu-item');
                items[0].addEventListener('click', function() { doExportScreenshot(sid, 10); });
                items[1].addEventListener('click', function() { doExportScreenshot(sid, 0); });
                items[2].addEventListener('click', function() { doExportData(sid, 'xlsx'); });
                items[3].addEventListener('click', function() { doExportData(sid, 'csv'); });
                items[4].addEventListener('click', function() { doExportData(sid, 'json'); });'''

html = html.replace(old_func, new_func)

with open('template.html', 'w', encoding='utf-8') as f:
    f.write(html)

print('Fixed - now using programmatic click handlers')
