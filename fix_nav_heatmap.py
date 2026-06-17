import re

with open('template.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Remove old search bar
html = html.replace('''
    <!-- Global Search Bar -->
    <div class="search-bar-top" id="search">
        <div class="container" style="position:relative;">
            <input type="text" class="search-bar" id="search-input" placeholder="搜索歌曲、观众或日期..." oninput="doSearch()">
            <div class="search-results" id="search-results"></div>
        </div>
    </div>

''', '\n')

# 2. Update nav CSS - remove old search-bar-top, add nav search styles
old_css = '''        /* Feature 14: Search bar (top) */
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

new_css = '''        /* Feature 14: Nav Search */
        .nav-search { position: relative; margin-left: 0.5rem; }
        .nav-search-btn { background: none; border: none; cursor: pointer; font-size: 1.1rem; color: var(--muted-fg); padding: 0.25rem; transition: color var(--dur); }
        .nav-search-btn:hover { color: var(--accent); }
        .nav-search-input { position: absolute; right: 0; top: 50%; transform: translateY(-50%); width: 0; padding: 0; border: none; font-family: var(--font-body); font-size: 0.85rem; background: var(--bg); color: var(--text); outline: none; transition: width 0.4s, padding 0.4s, border 0.4s; border-radius: 0; border-bottom: 1px solid transparent; overflow: hidden; }
        .nav-search-input.open { width: 200px; padding: 0.3rem 0.5rem; border-bottom-color: var(--accent-dim); }
        .nav-search-input:focus { border-bottom-color: var(--accent); }
        .search-results { position: absolute; right: 0; top: 100%; width: 320px; max-height: 360px; margin-top: 0.5rem; background: var(--bg); border: 1px solid var(--accent-dim); border-radius: 0; box-shadow: 0 8px 32px rgba(0,0,0,0.1); overflow-y: auto; z-index: 100; display: none; }
        .search-results.open { display: block; }
        .search-result-item { padding: 0.65rem 1rem; border-bottom: 1px solid rgba(212,175,55,0.08); cursor: pointer; transition: background var(--dur); }
        .search-result-item:hover { background: rgba(212,175,55,0.06); }
        .search-result-item:last-child { border-bottom: none; }
        .search-result-item .sr-type { font-size: 0.6rem; letter-spacing: 0.15em; text-transform: uppercase; color: var(--accent); margin-bottom: 0.1rem; }
        .search-result-item .sr-name { font-family: var(--font-display); font-size: 0.95rem; color: var(--text); }
        .search-result-item .sr-meta { font-size: 0.7rem; color: var(--muted-fg); margin-top: 0.1rem; }
        .search-empty { text-align: center; color: var(--muted-fg); padding: 1.5rem; font-style: italic; font-size: 0.8rem; }'''

html = html.replace(old_css, new_css)

# 3. Add search icon to nav (right side of nav-inner, after ul)
old_nav_end = '''            </ul>
        </div>
    </nav>'''

new_nav_end = '''            </ul>
            <div class="nav-search">
                <button class="nav-search-btn" id="nav-search-btn" onclick="toggleNavSearch()" title="搜索">🔍</button>
                <input type="text" class="nav-search-input" id="search-input" placeholder="搜索..." oninput="doSearch()">
                <div class="search-results" id="search-results"></div>
            </div>
        </div>
    </nav>'''

html = html.replace(old_nav_end, new_nav_end)

# 4. Update doSearch to open/close results
old_do_search = '''        function doSearch() {
            var q = (document.getElementById('search-input').value || '').trim().toLowerCase();
            var container = document.getElementById('search-results');
            if (!q || q.length < 1) { container.innerHTML = ''; return; }'''

new_do_search = '''        function toggleNavSearch() {
            var input = document.getElementById('search-input');
            var results = document.getElementById('search-results');
            if (input.classList.contains('open')) {
                input.classList.remove('open');
                results.classList.remove('open');
                input.value = '';
                results.innerHTML = '';
            } else {
                input.classList.add('open');
                setTimeout(function() { input.focus(); }, 400);
            }
        }
        function doSearch() {
            var q = (document.getElementById('search-input').value || '').trim().toLowerCase();
            var container = document.getElementById('search-results');
            if (!q || q.length < 1) { container.classList.remove('open'); container.innerHTML = ''; return; }
            container.classList.add('open');'''

html = html.replace(old_do_search, new_do_search)

# 5. Fix heatmap: move month labels to bottom, improve visibility
old_heatmap_html = '''            <div class="heatmap-months" id="heatmap-months"></div>
            <div class="heatmap-wrap" id="heatmap-container"></div>
            <div class="heatmap-nav">
                <button class="heatmap-nav-btn" id="heatmap-prev" onclick="heatmapScroll(-1)" disabled>&larr;</button>
                <button class="heatmap-nav-btn" id="heatmap-next" onclick="heatmapScroll(1)">&rarr;</button>
            </div>
            <div class="heatmap-legend">
                <span>少</span><span class="hl-cell l0"></span><span class="hl-cell l1"></span><span class="hl-cell l2"></span><span class="hl-cell l3"></span><span class="hl-cell l4"></span><span>多</span>
            </div>'''

new_heatmap_html = '''            <div class="heatmap-wrap" id="heatmap-container"></div>
            <div class="heatmap-months" id="heatmap-months"></div>
            <div class="heatmap-nav">
                <button class="heatmap-nav-btn" id="heatmap-prev" onclick="heatmapScroll(-1)" disabled>&larr;</button>
                <button class="heatmap-nav-btn" id="heatmap-next" onclick="heatmapScroll(1)">&rarr;</button>
            </div>
            <div class="heatmap-legend">
                <span>少</span><span class="hl-cell l0"></span><span class="hl-cell l1"></span><span class="hl-cell l2"></span><span class="hl-cell l3"></span><span class="hl-cell l4"></span><span>多</span>
            </div>'''

html = html.replace(old_heatmap_html, new_heatmap_html)

# 6. Fix heatmap CSS - reposition months below grid
html = html.replace(
    '.heatmap-months { display: flex; margin: 0 0.25rem 0.5rem; font-size: 0.6rem; letter-spacing: 0.1em; text-transform: uppercase; color: var(--bg); opacity: 0.6; overflow: hidden; white-space: nowrap; }',
    '.heatmap-months { display: flex; margin: 0.5rem 0 0; font-size: 0.6rem; letter-spacing: 0.1em; text-transform: uppercase; color: var(--bg); opacity: 0.7; overflow: hidden; white-space: nowrap; justify-content: flex-start; }'
)

# 7. Fix heatmap month label rendering - more visible labels with proper positioning
old_label_render = '''            // Render Month labels
            var mlHtml = '<div style="display:flex;gap:0;">';
            var displayedCol = heatmapPage * heatmapColsPerPage;
            for (var i = 0; i < monthLabels.length; i++) {
                var ml = monthLabels[i];
                if (ml.col >= displayedCol && ml.col < displayedCol + heatmapColsPerPage) {
                    mlHtml += '<span style="flex:1;text-align:left;min-width:0;">' + ml.label + '</span>';
                }
            }
            mlHtml += '</div>';
            monthsEl.innerHTML = mlHtml;'''

new_label_render = '''            // Render Month labels at bottom
            var displayedCol = heatmapPage * heatmapColsPerPage;
            var totalWidth = container.parentElement.offsetWidth - 32;
            var cellW = 14 + 3; // cell width + gap
            var colsShown = Math.min(heatmapColsPerPage, totalCols - displayedCol);
            var mlHtml = '<div style="display:flex;width:' + totalWidth + 'px;margin:0 auto;position:relative;">';
            for (var i = 0; i < monthLabels.length; i++) {
                var ml = monthLabels[i];
                if (ml.col >= displayedCol && ml.col < displayedCol + colsShown) {
                    var leftPx = (ml.col - displayedCol) * cellW;
                    mlHtml += '<span style="position:absolute;left:' + leftPx + 'px;font-size:0.6rem;letter-spacing:0.1em;text-transform:uppercase;">' + ml.label + '</span>';
                }
            }
            mlHtml += '</div>';
            monthsEl.innerHTML = mlHtml;'''

html = html.replace(old_label_render, new_label_render)

with open('template.html', 'w', encoding='utf-8') as f:
    f.write(html)

print('Nav search + heatmap fixes applied')
