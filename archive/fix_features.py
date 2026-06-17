import re

with open('template.html', 'r', encoding='utf-8') as f:
    html = f.read()

# ===== 1. Move search bar above nav =====
# Remove the search section HTML
html = html.replace('''
    <!-- Feature 14: Global Search -->
    <section class="section-dark" id="search">
        <div class="container">
            <span class="section-label">Search</span>
            <h2 class="section-title">全局搜索</h2>
            <div class="search-bar-wrap">
                <input type="text" class="search-bar" id="search-input" placeholder="搜索歌曲、观众或日期..." oninput="doSearch()">
            </div>
            <div class="search-results" id="search-results"></div>
        </div>
    </section>

''', '\n')

# Insert search bar between grid-lines and nav
old_nav = '''    <!-- Navigation -->
    <nav class="nav">
        <div class="nav-inner">
            <a href="https://tsingyun.github.io/sui-song-list-new/" class="nav-brand" target="_blank">岁己歌单</a>
            <ul class="nav-links">
                <li><a href="#monthly" class="nav-link">月度</a></li>
                <li><a href="#quarterly" class="nav-link">季度</a></li>
                <li><a href="#yearly" class="nav-link">年度</a></li>
                <li><a href="#total" class="nav-link">总榜</a></li>
                <li><a href="#songs" class="nav-link">歌曲</a></li>
                <li><a href="#audiences" class="nav-link">观众</a></li>
            </ul>
        </div>
    </nav>'''

new_nav = '''    <!-- Global Search Bar -->
    <div class="search-bar-top" id="search">
        <div class="container">
            <input type="text" class="search-bar" id="search-input" placeholder="搜索歌曲、观众或日期..." oninput="doSearch()">
            <div class="search-results" id="search-results"></div>
        </div>
    </div>

    <!-- Navigation -->
    <nav class="nav">
        <div class="nav-inner">
            <a href="https://tsingyun.github.io/sui-song-list-new/" class="nav-brand" target="_blank">岁己歌单</a>
            <ul class="nav-links">
                <li><a href="#monthly" class="nav-link">月度</a></li>
                <li><a href="#quarterly" class="nav-link">季度</a></li>
                <li><a href="#yearly" class="nav-link">年度</a></li>
                <li><a href="#total" class="nav-link">总榜</a></li>
                <li><a href="#songs" class="nav-link">歌曲</a></li>
                <li><a href="#audiences" class="nav-link">观众</a></li>
                <li><a href="#heatmap" class="nav-link">热图</a></li>
                <li><a href="#network" class="nav-link">网络</a></li>
                <li><a href="#achievements" class="nav-link">成就</a></li>
            </ul>
        </div>
    </nav>'''

html = html.replace(old_nav, new_nav)

# ===== 2. Update search CSS for top placement =====
old_search_css = '''        .search-bar-wrap { display: flex; justify-content: center; margin: 2rem auto 0; max-width: 520px; }
        .search-bar { width: 100%; padding: 0.75rem 1.25rem; font-family: var(--font-body); font-size: 0.95rem; border: 1px solid var(--accent-dim); border-radius: 999px; background: rgba(255,255,255,0.5); color: var(--text); outline: none; transition: all var(--dur); backdrop-filter: blur(10px); }
        .search-bar:focus { border-color: var(--accent); box-shadow: 0 0 0 3px rgba(212,175,55,0.12); }
        .search-results { margin: 1.5rem auto 0; max-width: 640px; }
        .search-result-item { padding: 0.75rem 1rem; border-bottom: 1px solid var(--accent-dim); cursor: pointer; transition: background var(--dur); }
        .search-result-item:hover { background: rgba(212,175,55,0.06); }
        .search-result-item .sr-type { font-size: 0.7rem; letter-spacing: 0.15em; text-transform: uppercase; color: var(--accent); margin-bottom: 0.15rem; }
        .search-result-item .sr-name { font-family: var(--font-display); font-size: 1.1rem; }
        .search-result-item .sr-meta { font-size: 0.8rem; color: var(--muted-fg); margin-top: 0.15rem; }
        .search-empty { text-align: center; color: var(--muted-fg); padding: 2rem; font-style: italic; }
        .search-highlight { background: rgba(212,175,55,0.2); padding: 0.05em 0.15em; border-radius: 2px; }'''

new_search_css = '''        /* Feature 14: Search bar (top) */
        .search-bar-top { padding: 2rem 0 0.5rem; text-align: center; }
        .search-bar { width: 100%; max-width: 480px; padding: 0.65rem 1.25rem; font-family: var(--font-body); font-size: 0.9rem; border: 1px solid var(--accent-dim); border-radius: 999px; background: rgba(255,255,255,0.6); color: var(--text); outline: none; transition: all var(--dur); backdrop-filter: blur(10px); }
        .search-bar:focus { border-color: var(--accent); box-shadow: 0 0 0 3px rgba(212,175,55,0.12); }
        .search-results { position: absolute; left: 50%; transform: translateX(-50%); width: 100%; max-width: 480px; margin-top: 0.35rem; background: var(--bg); border: 1px solid var(--accent-dim); border-radius: 0.75rem; box-shadow: 0 8px 32px rgba(0,0,0,0.08); overflow: hidden; z-index: 100; display: none; }
        .search-results:not(:empty) { display: block; }
        .search-result-item { padding: 0.65rem 1rem; border-bottom: 1px solid rgba(212,175,55,0.08); cursor: pointer; transition: background var(--dur); }
        .search-result-item:hover { background: rgba(212,175,55,0.06); }
        .search-result-item:last-child { border-bottom: none; }
        .search-result-item .sr-type { font-size: 0.65rem; letter-spacing: 0.15em; text-transform: uppercase; color: var(--accent); margin-bottom: 0.1rem; }
        .search-result-item .sr-name { font-family: var(--font-display); font-size: 1rem; }
        .search-result-item .sr-meta { font-size: 0.75rem; color: var(--muted-fg); margin-top: 0.1rem; }
        .search-empty { text-align: center; color: var(--muted-fg); padding: 1.5rem; font-style: italic; font-size: 0.85rem; }
        .search-highlight { background: rgba(212,175,55,0.2); padding: 0.05em 0.15em; border-radius: 2px; }'''

html = html.replace(old_search_css, new_search_css)

# ===== 3. Fix heatmap CSS - replace scrollbar with arrow nav =====
old_heatmap_css = '''        /* Feature 1: Calendar Heatmap */
        .heatmap-wrap { overflow-x: auto; padding: 0.5rem 0; }
        .heatmap-grid { display: grid; grid-auto-flow: column; grid-template-rows: repeat(7, 14px); gap: 3px; justify-content: center; min-width: fit-content; }
        .heatmap-cell { width: 14px; height: 14px; border-radius: 2px; background: var(--bg); cursor: pointer; transition: transform 0.15s; position: relative; }
        .heatmap-cell:hover { transform: scale(1.5); z-index: 2; }
        .heatmap-cell.l0 { background: var(--bg); border: 1px solid var(--accent-dim); }
        .heatmap-cell.l1 { background: #d4c5a0; }
        .heatmap-cell.l2 { background: #c4a96a; }
        .heatmap-cell.l3 { background: var(--accent); }
        .heatmap-cell.l4 { background: #b8860b; }
        .heatmap-legend { display: flex; align-items: center; justify-content: center; gap: 0.5rem; margin-top: 0.75rem; font-size: 0.7rem; letter-spacing: 0.1em; text-transform: uppercase; color: var(--muted-fg); }
        .heatmap-legend .hl-cell { width: 12px; height: 12px; border-radius: 2px; }
        .heatmap-months { display: flex; justify-content: center; gap: 0; margin-bottom: 0.25rem; font-size: 0.65rem; letter-spacing: 0.08em; text-transform: uppercase; color: var(--muted-fg); }'''

new_heatmap_css = '''        /* Feature 1: Calendar Heatmap */
        .heatmap-wrap { overflow: hidden; position: relative; }
        .heatmap-scroll { display: flex; transition: transform 0.4s cubic-bezier(0.25, 0.46, 0.45, 0.94); }
        .heatmap-grid { display: grid; grid-auto-flow: column; grid-template-rows: repeat(7, 14px); gap: 3px; flex-shrink: 0; }
        .heatmap-cell { width: 14px; height: 14px; border-radius: 2px; background: var(--bg); cursor: pointer; transition: transform 0.15s; position: relative; }
        .heatmap-cell:hover { transform: scale(1.5); z-index: 2; }
        .heatmap-cell.l0 { background: var(--bg); border: 1px solid var(--accent-dim); }
        .heatmap-cell.l1 { background: #d4c5a0; }
        .heatmap-cell.l2 { background: #c4a96a; }
        .heatmap-cell.l3 { background: var(--accent); }
        .heatmap-cell.l4 { background: #b8860b; }
        .heatmap-nav { display: flex; align-items: center; justify-content: center; gap: 1rem; margin-top: 0.75rem; }
        .heatmap-nav-btn { background: none; border: 1px solid var(--accent-dim); color: var(--muted-fg); width: 32px; height: 32px; border-radius: 50%; cursor: pointer; font-size: 0.85rem; transition: all var(--dur); display: flex; align-items: center; justify-content: center; font-family: var(--font-body); }
        .heatmap-nav-btn:hover { border-color: var(--accent); color: var(--accent); }
        .heatmap-nav-btn:disabled { opacity: 0.3; cursor: default; }
        .heatmap-nav-btn:disabled:hover { border-color: var(--accent-dim); color: var(--muted-fg); }
        .heatmap-months { display: flex; margin: 0 0.25rem 0.5rem; font-size: 0.6rem; letter-spacing: 0.1em; text-transform: uppercase; color: var(--muted-fg); overflow: hidden; white-space: nowrap; }
        .heatmap-months span { flex-shrink: 0; }
        .heatmap-legend { display: flex; align-items: center; justify-content: center; gap: 0.5rem; margin-top: 0.5rem; font-size: 0.7rem; letter-spacing: 0.1em; text-transform: uppercase; color: var(--muted-fg); }
        .heatmap-legend .hl-cell { width: 12px; height: 12px; border-radius: 2px; }'''

html = html.replace(old_heatmap_css, new_heatmap_css)

# ===== 4. Update heatmap HTML =====
old_heatmap_html = '''            <div class="heatmap-wrap" id="heatmap-container"></div>
            <div class="heatmap-legend">
                <span>少</span><span class="hl-cell l0"></span><span class="hl-cell l1"></span><span class="hl-cell l2"></span><span class="hl-cell l3"></span><span class="hl-cell l4"></span><span>多</span>
            </div>'''

new_heatmap_html = '''            <div class="heatmap-months" id="heatmap-months"></div>
            <div class="heatmap-wrap" id="heatmap-container"></div>
            <div class="heatmap-nav">
                <button class="heatmap-nav-btn" id="heatmap-prev" onclick="heatmapScroll(-1)" disabled>&larr;</button>
                <button class="heatmap-nav-btn" id="heatmap-next" onclick="heatmapScroll(1)">&rarr;</button>
            </div>
            <div class="heatmap-legend">
                <span>少</span><span class="hl-cell l0"></span><span class="hl-cell l1"></span><span class="hl-cell l2"></span><span class="hl-cell l3"></span><span class="hl-cell l4"></span><span>多</span>
            </div>'''

html = html.replace(old_heatmap_html, new_heatmap_html)

# ===== 5. Update heatmap JS =====
old_heatmap_js = '''        function renderHeatmap() {
            var data = appData.heatmap_data || [];
            if (!data.length) return;
            var container = document.getElementById('heatmap-container');
            // Group data by week
            var dates = data.map(function(d) { return d.date; });
            var minDate = new Date(dates[0]);
            var maxDate = new Date(dates[dates.length-1]);
            // Align to Sunday
            var startDay = minDate.getDay();
            var dateMap = {};
            for (var i = 0; i < data.length; i++) { dateMap[data[i].date] = data[i].count; }
            // Find max count for color scaling
            var maxCount = 0;
            for (var i = 0; i < data.length; i++) { if (data[i].count > maxCount) maxCount = data[i].count; }
            // Build cells
            var cells = [];
            var cur = new Date(minDate);
            // Go back to previous Sunday
            cur.setDate(cur.getDate() - startDay);
            var end = new Date(maxDate);
            end.setDate(end.getDate() + (6 - end.getDay()));
            while (cur <= end) {
                var ds = cur.toISOString().slice(0, 10);
                var count = dateMap[ds] || 0;
                var level = count === 0 ? 0 : count <= maxCount * 0.25 ? 1 : count <= maxCount * 0.5 ? 2 : count <= maxCount * 0.75 ? 3 : 4;
                cells.push('<div class="heatmap-cell l' + level + '" title="' + ds + ': ' + count + ' 首歌"></div>');
                cur.setDate(cur.getDate() + 1);
            }
            container.innerHTML = '<div class="heatmap-grid">' + cells.join('') + '</div>';
        }'''

new_heatmap_js = '''        var heatmapPage = 0, heatmapTotalPages = 1, heatmapColsPerPage = 20;
        function renderHeatmap() {
            var data = appData.heatmap_data || [];
            if (!data.length) return;
            var container = document.getElementById('heatmap-container');
            var monthsEl = document.getElementById('heatmap-months');
            var dates = data.map(function(d) { return d.date; });
            var minDate = new Date(dates[0]);
            var maxDate = new Date(dates[dates.length-1]);
            var startDay = minDate.getDay();
            var dateMap = {};
            for (var i = 0; i < data.length; i++) { dateMap[data[i].date] = data[i].count; }
            var maxCount = 0;
            for (var i = 0; i < data.length; i++) { if (data[i].count > maxCount) maxCount = data[i].count; }
            // Build all cells
            var cells = [], monthLabels = [];
            var cur = new Date(minDate);
            cur.setDate(cur.getDate() - startDay);
            var end = new Date(maxDate);
            end.setDate(end.getDate() + (6 - end.getDay()));
            var prevMonth = -1, colIdx = 0;
            var weekStarts = []; // track which column each week starts
            while (cur <= end) {
                var ds = cur.toISOString().slice(0, 10);
                var count = dateMap[ds] || 0;
                var lvl = count === 0 ? 0 : count <= maxCount * 0.25 ? 1 : count <= maxCount * 0.5 ? 2 : count <= maxCount * 0.75 ? 3 : 4;
                cells.push('<div class="heatmap-cell l' + lvl + '" title="' + ds + ': ' + count + ' 首"></div>');
                // Track month for labels (every 3 months)
                var m = cur.getMonth();
                if (m !== prevMonth && m % 3 === 0 && colIdx > 0) {
                    monthLabels.push({col: colIdx, label: (cur.getFullYear() + '.' + ('0'+(m+1)).slice(-2))});
                }
                prevMonth = m;
                cur.setDate(cur.getDate() + 1);
                if (cur.getDay() === 0) colIdx++;
            }
            // Calculate total pages
            var totalCols = colIdx;
            heatmapColsPerPage = Math.max(15, Math.floor(container.parentElement.offsetWidth / 20));
            heatmapTotalPages = Math.ceil(totalCols / heatmapColsPerPage);
            heatmapPage = Math.min(heatmapPage, heatmapTotalPages - 1);
            // Render Month labels
            var mlHtml = '<div style="display:flex;gap:0;">';
            var displayedCol = heatmapPage * heatmapColsPerPage;
            for (var i = 0; i < monthLabels.length; i++) {
                var ml = monthLabels[i];
                if (ml.col >= displayedCol && ml.col < displayedCol + heatmapColsPerPage) {
                    mlHtml += '<span style="flex:1;text-align:left;min-width:0;">' + ml.label + '</span>';
                }
            }
            mlHtml += '</div>';
            monthsEl.innerHTML = mlHtml;
            // Render grid
            container.innerHTML = '<div class="heatmap-scroll" id="heatmap-scroll" style="justify-content:center;width:100%;"><div class="heatmap-grid">' + cells.join('') + '</div></div>';
            // Update arrows
            updateHeatmapNav();
        }
        function heatmapScroll(dir) {
            heatmapPage = Math.max(0, Math.min(heatmapTotalPages - 1, heatmapPage + dir));
            var scroll = document.getElementById('heatmap-scroll');
            if (scroll) scroll.style.transform = 'translateX(-' + (heatmapPage * heatmapColsPerPage * 17) + 'px)';
            renderHeatmap();
        }
        function updateHeatmapNav() {
            var prev = document.getElementById('heatmap-prev');
            var next = document.getElementById('heatmap-next');
            if (prev) prev.disabled = heatmapPage <= 0;
            if (next) next.disabled = heatmapPage >= heatmapTotalPages - 1;
        }'''

html = html.replace(old_heatmap_js, new_heatmap_js)

# ===== 6. Fix network section - use light bg for dark text readability =====
html = html.replace('''    <!-- Feature 2: Song Relationship Network -->
    <section class="section-dark" id="network">''', '''    <!-- Feature 2: Song Relationship Network -->
    <section class="section" id="network">''')

# Fix network text color to dark
html = html.replace("                    ctx.fillStyle = '#F9F8F6';", "                    ctx.fillStyle = '#1A1A1A';")
html = html.replace("                    ctx.font = '9px Inter, system-ui, sans-serif';", "                    ctx.font = '11px Inter, system-ui, sans-serif';")

# Node outline should be darker on light bg
html = html.replace("                ctx.strokeStyle = '#fff';", "                ctx.strokeStyle = '#F9F8F6';")

# ===== 7. Fix achievements CSS - more restrained =====
old_ach_css = '''        /* Feature 5: Achievement Cards */
        .achievements-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(260px, 1fr)); gap: 1.25rem; margin-top: 1rem; }
        .ach-card { background: linear-gradient(135deg, rgba(212,175,55,0.06), rgba(212,175,55,0.01)); border: 1px solid var(--accent-dim); border-radius: var(--radius); padding: 1.5rem; text-align: center; transition: all var(--dur); position: relative; overflow: hidden; }
        .ach-card::before { content: ''; position: absolute; top: 0; left: 0; right: 0; height: 2px; background: var(--accent); opacity: 0; transition: opacity var(--dur); }
        .ach-card:hover { transform: translateY(-3px); box-shadow: 0 8px 24px rgba(0,0,0,0.08); border-color: var(--accent); }
        .ach-card:hover::before { opacity: 1; }
        .ach-card .ach-emoji { font-size: 2.5rem; margin-bottom: 0.5rem; }
        .ach-card .ach-name { font-family: var(--font-display); font-size: 1.2rem; color: var(--text); margin-bottom: 0.4rem; }
        .ach-card .ach-desc { font-size: 0.85rem; color: var(--muted-fg); line-height: 1.5; }
        .ach-card .ach-badge { display: inline-block; margin-top: 0.75rem; padding: 0.2em 0.8em; border: 1px solid var(--accent); border-radius: 999px; font-size: 0.65rem; letter-spacing: 0.15em; text-transform: uppercase; color: var(--accent); }'''

new_ach_css = '''        /* Feature 5: Achievement Cards */
        .achievements-container { display: flex; justify-content: center; margin-top: 1rem; }
        .ach-card { max-width: 400px; width: 100%; background: transparent; border: 1px solid var(--accent-dim); border-radius: var(--radius); padding: 2rem 2rem 1.75rem; text-align: center; transition: all var(--dur); position: relative; }
        .ach-card:hover { border-color: var(--accent); box-shadow: 0 4px 20px rgba(0,0,0,0.04); }
        .ach-card .ach-emoji { font-size: 3rem; margin-bottom: 0.75rem; display: block; }
        .ach-card .ach-name { font-family: var(--font-display); font-size: 1.4rem; color: var(--text); margin-bottom: 0.5rem; letter-spacing: 0.02em; }
        .ach-card .ach-desc { font-size: 0.85rem; color: var(--muted-fg); line-height: 1.6; max-width: 280px; margin: 0 auto; }'''

html = html.replace(old_ach_css, new_ach_css)

# ===== 8. Fix achievements HTML =====
old_ach_html = '''            <div class="achievements-grid" id="achievements-grid"></div>'''
new_ach_html = '''            <div class="achievements-container" id="achievements-container"></div>'''
html = html.replace(old_ach_html, new_ach_html)

# ===== 9. Fix achievements JS - only song king =====
old_ach_js = '''        function renderAchievements() {
            var ach = appData.achievements || [];
            var grid = document.getElementById('achievements-grid');
            if (!ach.length) { grid.innerHTML = '<p style="color:var(--muted-fg);text-align:center;">暂无成就</p>'; return; }
            grid.innerHTML = ach.map(function(a) {
                return '<div class="ach-card"><div class="ach-emoji">' + a.emoji + '</div><div class="ach-name">' + a.name + '</div><div class="ach-desc">' + a.desc + '</div><div class="ach-badge">UNLOCKED</div></div>';
            }).join('');
        }'''

new_ach_js = '''        function renderAchievements() {
            var ach = appData.achievements || [];
            var container = document.getElementById('achievements-container');
            // Only show "song king" achievement
            var songKing = null;
            for (var i = 0; i < ach.length; i++) {
                if (ach[i].id === 'song_king') { songKing = ach[i]; break; }
            }
            if (!songKing) { container.innerHTML = '<p style="color:var(--muted-fg);text-align:center;font-size:0.85rem;">暂无成就</p>'; return; }
            container.innerHTML = '<div class="ach-card"><div class="ach-emoji">' + songKing.emoji + '</div><div class="ach-name">' + songKing.name + '</div><div class="ach-desc">' + songKing.desc + '</div></div>';
        }'''

html = html.replace(old_ach_js, new_ach_js)

# ===== 10. Search results container needs position:relative parent =====
# Wrap search section in a relative container
html = html.replace('''    <!-- Global Search Bar -->
    <div class="search-bar-top" id="search">
        <div class="container">
            <input type="text" class="search-bar" id="search-input" placeholder="搜索歌曲、观众或日期..." oninput="doSearch()">
            <div class="search-results" id="search-results"></div>
        </div>
    </div>''', '''    <!-- Global Search Bar -->
    <div class="search-bar-top" id="search">
        <div class="container" style="position:relative;">
            <input type="text" class="search-bar" id="search-input" placeholder="搜索歌曲、观众或日期..." oninput="doSearch()">
            <div class="search-results" id="search-results"></div>
        </div>
    </div>''')

with open('template.html', 'w', encoding='utf-8') as f:
    f.write(html)

print('All feature fixes applied to template.html')
