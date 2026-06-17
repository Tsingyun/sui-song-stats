import re

with open('template.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Add CDN scripts before </head>
cdn = '''
    <script src="https://cdnjs.cloudflare.com/ajax/libs/html2canvas/1.4.1/html2canvas.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/xlsx/0.18.5/xlsx.full.min.js"></script>
'''
html = html.replace('</head>', cdn + '</head>')

# 2. Add export CSS before Feature 14 Nav Search CSS
export_css = '''
        /* Export button & dropdown */
        .export-wrap { display: inline-block; position: relative; margin-left: 1rem; vertical-align: middle; }
        .export-btn { background: none; border: 1px solid var(--accent-dim); color: var(--muted-fg); padding: 0.2rem 0.75rem; font-family: var(--font-body); font-size: 0.6rem; letter-spacing: 0.15em; text-transform: uppercase; cursor: pointer; transition: all var(--dur); }
        .export-btn:hover { border-color: var(--accent); color: var(--accent); }
        .section-dark .export-btn { color: var(--bg); border-color: rgba(249,248,246,0.3); }
        .section-dark .export-btn:hover { border-color: var(--accent); color: var(--accent); }
        .export-menu { position: absolute; left: 0; top: 100%; margin-top: 0.3rem; background: var(--bg); border: 1px solid var(--accent-dim); box-shadow: 0 4px 20px rgba(0,0,0,0.08); z-index: 50; min-width: 140px; display: none; }
        .export-menu.open { display: block; }
        .export-menu-item { display: block; width: 100%; padding: 0.5rem 1rem; background: none; border: none; text-align: left; font-family: var(--font-body); font-size: 0.7rem; letter-spacing: 0.05em; color: var(--text); cursor: pointer; transition: background var(--dur); }
        .export-menu-item:hover { background: rgba(212,175,55,0.08); color: var(--accent); }
        .export-menu-item + .export-menu-item { border-top: 1px solid rgba(0,0,0,0.04); }
        .export-menu-divider { padding: 0.3rem 1rem; font-size: 0.55rem; letter-spacing: 0.15em; text-transform: uppercase; color: var(--accent); border-top: 1px solid var(--accent-dim); }
'''
html = html.replace('''        /* Feature 14: Nav Search */''', export_css + '\n        /* Feature 14: Nav Search */')

# 3. Generate export button HTML snippet
export_btn_html = '<span class="export-wrap"><button class="export-btn" onclick="event.stopPropagation();toggleExportMenu(this)" title="导出">EXPORT ▾</button><div class="export-menu"></div></span>'

# 4. Add export button to each leaderboard section header
# Monthly
html = html.replace(
    '<h2 class="section-title">月度点歌榜</h2>',
    '<h2 class="section-title">月度点歌榜' + export_btn_html + '</h2>'
)
# Quarterly
html = html.replace(
    '<h2 class="section-title">季度点歌榜</h2>',
    '<h2 class="section-title">季度点歌榜' + export_btn_html + '</h2>'
)
# Yearly
html = html.replace(
    '<h2 class="section-title">年度点歌榜</h2>',
    '<h2 class="section-title">年度点歌榜' + export_btn_html + '</h2>'
)
# Total
html = html.replace(
    '<h2 class="section-title">总点歌榜</h2>',
    '<h2 class="section-title">总点歌榜' + export_btn_html + '</h2>'
)
# Songs
html = html.replace(
    '<h2 class="section-title">热门歌曲榜</h2>',
    '<h2 class="section-title">热门歌曲榜' + export_btn_html + '</h2>'
)

# 5. Add JS functions before </script>
export_js = '''
        // ==== Export ====
        function toggleExportMenu(btn) {
            var menu = btn.nextElementSibling;
            var open = menu.classList.contains('open');
            // Close all other menus
            document.querySelectorAll('.export-menu.open').forEach(function(m) { m.classList.remove('open'); });
            if (!open) {
                // Build menu items
                var wrap = btn.parentElement;
                var sectionId = wrap.closest('section').id;
                menu.innerHTML = '<div class="export-menu-divider">截图</div>' +
                    '<button class="export-menu-item" onclick="doExportScreenshot(\'' + sectionId + '\', 10)">截图 · 前10名</button>' +
                    '<button class="export-menu-item" onclick="doExportScreenshot(\'' + sectionId + '\', 0)">截图 · 完整榜单</button>' +
                    '<div class="export-menu-divider">数据文件</div>' +
                    '<button class="export-menu-item" onclick="doExportData(\'' + sectionId + '\', \'xlsx\')">导出 XLSX</button>' +
                    '<button class="export-menu-item" onclick="doExportData(\'' + sectionId + '\', \'csv\')">导出 CSV</button>' +
                    '<button class="export-menu-item" onclick="doExportData(\'' + sectionId + '\', \'json\')">导出 JSON</button>';
                menu.classList.add('open');
            }
        }
        // Close export menus on outside click
        document.addEventListener('click', function(e) {
            if (!e.target.closest('.export-wrap')) {
                document.querySelectorAll('.export-menu.open').forEach(function(m) { m.classList.remove('open'); });
            }
        });

        function getSectionData(sectionId) {
            // Determine current data for this section
            if (sectionId === 'total') return {data: appData.total_leaderboard, title: '总点歌榜', fields: ['audience', 'count']};
            if (sectionId === 'songs') return {data: appData.song_leaderboard, title: '热门歌曲榜', fields: ['song', 'count']};
            if (sectionId === 'monthly') {
                var m = months[currentMonthIdx];
                return {data: appData.monthly_leaderboard[m] || [], title: m + ' 月度点歌榜', fields: ['audience', 'count']};
            }
            if (sectionId === 'quarterly') {
                var q = quarters[currentQuarterIdx];
                return {data: appData.quarterly_leaderboard[q] || [], title: q + ' 季度点歌榜', fields: ['audience', 'count']};
            }
            if (sectionId === 'yearly') {
                var y = years[currentYearIdx];
                return {data: appData.yearly_leaderboard[y] || [], title: y + ' 年度点歌榜', fields: ['audience', 'count']};
            }
            return {data: [], title: 'Unknown', fields: []};
        }

        function doExportScreenshot(sectionId, limit) {
            var container = null;
            if (sectionId === 'monthly') container = document.getElementById('monthly-leaderboard');
            else if (sectionId === 'quarterly') container = document.getElementById('quarterly-leaderboard');
            else if (sectionId === 'yearly') container = document.getElementById('yearly-leaderboard');
            else if (sectionId === 'total') container = document.getElementById('total-leaderboard');
            else if (sectionId === 'songs') container = document.getElementById('songs-leaderboard');
            if (!container) return;
            // Temporarily expand if needed
            var wasExpanded = container._isExpanded;
            if (limit === 0) { container._isExpanded = true; }
            // Determine data
            var sd = getSectionData(sectionId);
            var displayData = limit > 0 ? sd.data.slice(0, limit) : sd.data;
            // Re-render temporarily
            var tmpContainer = document.createElement('div');
            tmpContainer.style.cssText = 'position:fixed;left:-9999px;top:0;width:800px;background:#F9F8F6;padding:2rem;font-family:Inter,sans-serif;z-index:99999;';
            tmpContainer.innerHTML = '<h2 style="font-family:Playfair Display,serif;font-size:1.8rem;margin-bottom:0.25rem;color:#1A1A1A;">' + sd.title + '</h2>' +
                '<p style="font-size:0.7rem;letter-spacing:0.15em;text-transform:uppercase;color:#6C6863;margin-bottom:1.5rem;">岁己 SUI 点歌统计</p>' +
                '<table style="width:100%;border-collapse:collapse;"><thead><tr style="border-bottom:2px solid #D4AF37;">' +
                '<th style="padding:0.5rem;text-align:left;font-size:0.65rem;letter-spacing:0.15em;text-transform:uppercase;color:#6C6863;">#</th>' +
                '<th style="padding:0.5rem;text-align:left;font-size:0.65rem;letter-spacing:0.15em;text-transform:uppercase;color:#6C6863;">' + (sd.fields[0] === 'song' ? '歌曲' : '观众') + '</th>' +
                '<th style="padding:0.5rem;text-align:right;font-size:0.65rem;letter-spacing:0.15em;text-transform:uppercase;color:#6C6863;">次数</th>' +
                '</tr></thead><tbody>' +
                displayData.map(function(item, i) {
                    return '<tr style="border-bottom:1px solid rgba(0,0,0,0.06);"><td style="padding:0.4rem 0.5rem;font-size:0.8rem;color:#6C6863;">' + (i+1) + '</td><td style="padding:0.4rem 0.5rem;font-size:0.9rem;color:#1A1A1A;">' + (item.audience || item.song || '') + '</td><td style="padding:0.4rem 0.5rem;text-align:right;font-size:0.85rem;color:#1A1A1A;">' + item.count + '</td></tr>';
                }).join('') +
                '</tbody></table>';
            document.body.appendChild(tmpContainer);
            html2canvas(tmpContainer, {scale: 2, backgroundColor: '#F9F8F6'}).then(function(canvas) {
                document.body.removeChild(tmpContainer);
                // Restore state
                container._isExpanded = wasExpanded;
                // Download
                var link = document.createElement('a');
                link.download = (sd.title + (limit > 0 ? '_Top' + limit : '_Full') + '.png').replace(/\s/g, '_');
                link.href = canvas.toDataURL('image/png');
                link.click();
                // Re-render to restore original view
                if (limit === 0) { renderCurrentSection(sectionId); }
            });
            // Close menu
            document.querySelectorAll('.export-menu.open').forEach(function(m) { m.classList.remove('open'); });
        }

        function renderCurrentSection(sectionId) {
            if (sectionId === 'monthly') renderMonth();
            else if (sectionId === 'quarterly') renderQuarter();
            else if (sectionId === 'yearly') renderYear();
            else if (sectionId === 'total') renderTotal();
            else if (sectionId === 'songs') renderSongs();
        }

        function doExportData(sectionId, format) {
            var sd = getSectionData(sectionId);
            var data = sd.data;
            if (!data || !data.length) return;
            if (format === 'json') {
                var blob = new Blob([JSON.stringify(data, null, 2)], {type: 'application/json'});
                downloadBlob(blob, sd.title.replace(/\s/g, '_') + '.json');
            } else if (format === 'csv') {
                var header = sd.fields.join(',');
                var rows = data.map(function(item) { return sd.fields.map(function(f) { return '"' + (item[f] || '') + '"'; }).join(','); });
                var csv = '\\uFEFF' + header + '\\n' + rows.join('\\n');
                var blob = new Blob([csv], {type: 'text/csv;charset=utf-8;'});
                downloadBlob(blob, sd.title.replace(/\s/g, '_') + '.csv');
            } else if (format === 'xlsx') {
                var wsData = [sd.fields].concat(data.map(function(item) { return sd.fields.map(function(f) { return item[f] || ''; }); }));
                var ws = XLSX.utils.aoa_to_sheet(wsData);
                ws['!cols'] = sd.fields.map(function() { return {wch: 20}; });
                var wb = XLSX.utils.book_new();
                XLSX.utils.book_append_sheet(wb, ws, 'Sheet1');
                XLSX.writeFile(wb, sd.title.replace(/\s/g, '_') + '.xlsx');
            }
            document.querySelectorAll('.export-menu.open').forEach(function(m) { m.classList.remove('open'); });
        }

        function downloadBlob(blob, filename) {
            var link = document.createElement('a');
            link.href = URL.createObjectURL(blob);
            link.download = filename;
            link.click();
            URL.revokeObjectURL(link.href);
        }
'''
html = html.replace('\n    </script>', export_js + '\n    </script>')

with open('template.html', 'w', encoding='utf-8') as f:
    f.write(html)

print('Export feature added to template')
