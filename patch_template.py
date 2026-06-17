import re

with open('template.html', 'r', encoding='utf-8') as f:
    html = f.read()

# ========================
# NEW CSS (before </style>)
# ========================
new_css = '''
        /* Feature 3: Number Animation */
        .stat-num { display: inline-block; }
        .stat-num.animating { color: var(--accent); }

        /* Feature 14: Search */
        .search-bar-wrap { display: flex; justify-content: center; margin: 2rem auto 0; max-width: 520px; }
        .search-bar { width: 100%; padding: 0.75rem 1.25rem; font-family: var(--font-body); font-size: 0.95rem; border: 1px solid var(--accent-dim); border-radius: 999px; background: rgba(255,255,255,0.5); color: var(--text); outline: none; transition: all var(--dur); backdrop-filter: blur(10px); }
        .search-bar:focus { border-color: var(--accent); box-shadow: 0 0 0 3px rgba(212,175,55,0.12); }
        .search-results { margin: 1.5rem auto 0; max-width: 640px; }
        .search-result-item { padding: 0.75rem 1rem; border-bottom: 1px solid var(--accent-dim); cursor: pointer; transition: background var(--dur); }
        .search-result-item:hover { background: rgba(212,175,55,0.06); }
        .search-result-item .sr-type { font-size: 0.7rem; letter-spacing: 0.15em; text-transform: uppercase; color: var(--accent); margin-bottom: 0.15rem; }
        .search-result-item .sr-name { font-family: var(--font-display); font-size: 1.1rem; }
        .search-result-item .sr-meta { font-size: 0.8rem; color: var(--muted-fg); margin-top: 0.15rem; }
        .search-empty { text-align: center; color: var(--muted-fg); padding: 2rem; font-style: italic; }
        .search-highlight { background: rgba(212,175,55,0.2); padding: 0.05em 0.15em; border-radius: 2px; }

        /* Feature 1: Calendar Heatmap */
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
        .heatmap-months { display: flex; justify-content: center; gap: 0; margin-bottom: 0.25rem; font-size: 0.65rem; letter-spacing: 0.08em; text-transform: uppercase; color: var(--muted-fg); }

        /* Feature 2: Song Network */
        .network-container { position: relative; width: 100%; height: 450px; background: var(--bg); border-radius: var(--radius); overflow: hidden; }
        .network-container canvas { display: block; }
        .network-legend { text-align: center; margin-top: 0.5rem; font-size: 0.7rem; color: var(--muted-fg); letter-spacing: 0.1em; text-transform: uppercase; }

        /* Feature 5: Achievement Cards */
        .achievements-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(260px, 1fr)); gap: 1.25rem; margin-top: 1rem; }
        .ach-card { background: linear-gradient(135deg, rgba(212,175,55,0.06), rgba(212,175,55,0.01)); border: 1px solid var(--accent-dim); border-radius: var(--radius); padding: 1.5rem; text-align: center; transition: all var(--dur); position: relative; overflow: hidden; }
        .ach-card::before { content: ''; position: absolute; top: 0; left: 0; right: 0; height: 2px; background: var(--accent); opacity: 0; transition: opacity var(--dur); }
        .ach-card:hover { transform: translateY(-3px); box-shadow: 0 8px 24px rgba(0,0,0,0.08); border-color: var(--accent); }
        .ach-card:hover::before { opacity: 1; }
        .ach-card .ach-emoji { font-size: 2.5rem; margin-bottom: 0.5rem; }
        .ach-card .ach-name { font-family: var(--font-display); font-size: 1.2rem; color: var(--text); margin-bottom: 0.4rem; }
        .ach-card .ach-desc { font-size: 0.85rem; color: var(--muted-fg); line-height: 1.5; }
        .ach-card .ach-badge { display: inline-block; margin-top: 0.75rem; padding: 0.2em 0.8em; border: 1px solid var(--accent); border-radius: 999px; font-size: 0.65rem; letter-spacing: 0.15em; text-transform: uppercase; color: var(--accent); }

        /* Feature 6: Level Badges */
        .lb-level { display: inline-flex; align-items: center; gap: 0.3em; margin-left: 0.4em; padding: 0.1em 0.5em; border-radius: 999px; font-size: 0.6rem; letter-spacing: 0.08em; font-weight: 600; }
        .lb-level.lv1 { background: #e8e8e8; color: #888; }
        .lb-level.lv2 { background: #d4e8d4; color: #5a8a5a; }
        .lb-level.lv3 { background: #c4d4f0; color: #4a6a9a; }
        .lb-level.lv4 { background: #e8d4f0; color: #7a4a9a; }
        .lb-level.lv5 { background: linear-gradient(135deg, #D4AF37, #F5D76E); color: #5a3a00; }
'''

html = html.replace('    </style>', new_css + '\n    </style>')

# ========================
# NEW HTML SECTIONS (before footer)
# ========================
new_html = '''
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

    <!-- Feature 1: Calendar Heatmap -->
    <section class="section" id="heatmap">
        <div class="container">
            <span class="section-label">Heatmap</span>
            <h2 class="section-title">日历热图</h2>
            <div class="heatmap-wrap" id="heatmap-container"></div>
            <div class="heatmap-legend">
                <span>少</span><span class="hl-cell l0"></span><span class="hl-cell l1"></span><span class="hl-cell l2"></span><span class="hl-cell l3"></span><span class="hl-cell l4"></span><span>多</span>
            </div>
        </div>
    </section>

    <!-- Feature 2: Song Relationship Network -->
    <section class="section-dark" id="network">
        <div class="container">
            <span class="section-label">Network</span>
            <h2 class="section-title">歌曲关系网络</h2>
            <div class="network-container" id="network-container">
                <canvas id="network-canvas"></canvas>
            </div>
            <div class="network-legend">节点大小 = 点歌次数 · 连线 = 被同一位观众点过</div>
        </div>
    </section>

    <!-- Feature 5: Achievements -->
    <section class="section" id="achievements">
        <div class="container">
            <span class="section-label">Achievements</span>
            <h2 class="section-title">成就殿堂</h2>
            <div class="achievements-grid" id="achievements-grid"></div>
        </div>
    </section>
'''

html = html.replace('    <!-- Footer -->', new_html + '\n    <!-- Footer -->')

# ========================
# NEW JS FUNCTIONS (before </script>)
# ========================
new_js = '''
        // ==== Feature 3: Number Animation ====
        function animateNumber(el, target, duration) {
            if (!el || target === undefined) return;
            duration = duration || 1500;
            var start = 0;
            var startTime = null;
            var prefix = el.textContent.match(/[^0-9]+$/) ? el.textContent.match(/[^0-9]+$/)[0] : '';
            function step(ts) {
                if (!startTime) startTime = ts;
                var progress = Math.min((ts - startTime) / duration, 1);
                var eased = 1 - Math.pow(1 - progress, 3);
                el.textContent = Math.floor(eased * target) + prefix;
                if (progress < 1) requestAnimationFrame(step);
                else el.textContent = target + prefix;
            }
            requestAnimationFrame(step);
        }

        // ==== Feature 14: Global Search ====
        function doSearch() {
            var q = (document.getElementById('search-input').value || '').trim().toLowerCase();
            var container = document.getElementById('search-results');
            if (!q || q.length < 1) { container.innerHTML = ''; return; }
            var results = [];
            var idx = appData.search_index;
            // Search songs
            for (var i = 0; i < idx.songs.length; i++) {
                var s = idx.songs[i];
                if (s.toLowerCase().indexOf(q) >= 0) results.push({type: '歌曲', name: s, highlight: s});
            }
            // Search audiences
            for (var i = 0; i < idx.audiences.length; i++) {
                var a = idx.audiences[i];
                if (a.toLowerCase().indexOf(q) >= 0) {
                    var lv = appData.audience_levels[a];
                    results.push({type: '观众', name: a, meta: (lv ? 'Lv.' + lv.level + ' · ' + lv.count + ' 次点歌' : '')});
                }
            }
            // Search dates
            for (var i = 0; i < idx.dates.length; i++) {
                var d = idx.dates[i];
                if (d.indexOf(q) >= 0) {
                    var dc = 0;
                    for (var j = 0; j < appData.heatmap_data.length; j++) {
                        if (appData.heatmap_data[j].date === d) { dc = appData.heatmap_data[j].count; break; }
                    }
                    results.push({type: '日期', name: d, meta: dc + ' 次点歌'});
                }
            }
            results = results.slice(0, 20);
            if (results.length === 0) {
                container.innerHTML = '<p class="search-empty">没有找到匹配的结果</p>';
            } else {
                container.innerHTML = results.map(function(r) {
                    return '<div class="search-result-item"><div class="sr-type">' + r.type + '</div><div class="sr-name">' + r.name + '</div>' + (r.meta ? '<div class="sr-meta">' + r.meta + '</div>' : '') + '</div>';
                }).join('');
            }
        }

        // ==== Feature 1: Calendar Heatmap ====
        function renderHeatmap() {
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
        }

        // ==== Feature 2: Song Network ====
        function renderNetwork() {
            var network = appData.song_network;
            if (!network || !network.nodes || !network.edges) return;
            var canvas = document.getElementById('network-canvas');
            var container = document.getElementById('network-container');
            canvas.width = container.offsetWidth;
            canvas.height = container.offsetHeight;
            var ctx = canvas.getContext('2d');
            var nodes = network.nodes;
            var edges = network.edges;
            var W = canvas.width, H = canvas.height;
            var cx = W / 2, cy = H / 2;
            var rx = W * 0.42, ry = H * 0.4;
            // Position nodes in a spiral/ring
            var nodePos = {};
            var maxCount = nodes[0] ? nodes[0].count : 1;
            for (var i = 0; i < nodes.length; i++) {
                var angle = (i / nodes.length) * Math.PI * 2;
                var rad = 0.4 + (Math.random() * 0.2);
                var x = cx + Math.cos(angle) * rx * rad;
                var y = cy + Math.sin(angle) * ry * rad;
                nodePos[nodes[i].id] = {x: x, y: y, count: nodes[i].count};
            }
            // Draw edges
            for (var i = 0; i < edges.length; i++) {
                var e = edges[i];
                var s = nodePos[e.source], t = nodePos[e.target];
                if (!s || !t) continue;
                var alpha = Math.min(0.6, e.weight / 8 * 0.6);
                ctx.beginPath();
                ctx.moveTo(s.x, s.y);
                ctx.lineTo(t.x, t.y);
                ctx.strokeStyle = 'rgba(212,175,55,' + alpha + ')';
                ctx.lineWidth = Math.max(0.5, e.weight / 4);
                ctx.stroke();
            }
            // Draw nodes
            for (var i = 0; i < nodes.length; i++) {
                var n = nodes[i];
                var p = nodePos[n.id];
                if (!p) continue;
                var r = 4 + (n.count / maxCount) * 14;
                ctx.beginPath();
                ctx.arc(p.x, p.y, r, 0, Math.PI * 2);
                ctx.fillStyle = 'rgba(212,175,55,0.85)';
                ctx.fill();
                ctx.strokeStyle = '#fff';
                ctx.lineWidth = 1.5;
                ctx.stroke();
                // Label (only for top nodes)
                if (i < 15) {
                    ctx.fillStyle = 'var(--text)';
                    ctx.font = '9px Inter, system-ui, sans-serif';
                    ctx.fillText(n.id.length > 8 ? n.id.slice(0,7)+'...' : n.id, p.x + r + 3, p.y + 4);
                }
            }
        }

        // ==== Feature 5: Achievements ====
        function renderAchievements() {
            var ach = appData.achievements || [];
            var grid = document.getElementById('achievements-grid');
            if (!ach.length) { grid.innerHTML = '<p style="color:var(--muted-fg);text-align:center;">暂无成就</p>'; return; }
            grid.innerHTML = ach.map(function(a) {
                return '<div class="ach-card"><div class="ach-emoji">' + a.emoji + '</div><div class="ach-name">' + a.name + '</div><div class="ach-desc">' + a.desc + '</div><div class="ach-badge">UNLOCKED</div></div>';
            }).join('');
        }

        // ==== Feature 6: Level Badges in leaderboard ====
        function getLevelBadge(audience) {
            var lv = appData.audience_levels && appData.audience_levels[audience];
            if (!lv) return '';
            return '<span class="lb-level lv' + lv.level + '">Lv.' + lv.level + '</span>';
        }
'''

# Find the </script> tag and insert before it
html = html.replace('\n    </script>', new_js + '\n    </script>')

# Also need to update the hero stat rendering and lb-name to show levels
# Let the main initApp function handle calling new renderers

with open('template.html', 'w', encoding='utf-8') as f:
    f.write(html)

print('Template updated with all 6 creative features')
