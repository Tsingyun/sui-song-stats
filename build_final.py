"""Generate a completely self-contained, clean HTML file."""
import json

# Read the processed data
with open('song_data_processed.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Build the complete HTML file
html = '''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>岁己SUI · 点歌统计</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,300;0,400;0,500;0,600;1,400&family=Inter:wght@300;400;500;600&display=swap" rel="stylesheet">
    <style>
        :root {
            --bg-primary: #F9F8F6;
            --bg-muted: #EBE5DE;
            --text-primary: #1A1A1A;
            --text-muted: #6C6863;
            --accent: #D4AF37;
            --font-serif: 'Playfair Display', Georgia, serif;
            --font-sans: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
        }
        * { margin: 0; padding: 0; box-sizing: border-box; }
        html { scroll-behavior: smooth; }
        body {
            font-family: var(--font-sans);
            background-color: var(--bg-primary);
            color: var(--text-primary);
            line-height: 1.625;
            -webkit-font-smoothing: antialiased;
            overflow-x: hidden;
        }
        .paper-texture {
            position: fixed; top: 0; left: 0; width: 100%; height: 100%;
            pointer-events: none; z-index: 50; opacity: 0.02;
            background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 256 256' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noise'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noise)'/%3E%3C/svg%3E");
        }
        .grid-lines {
            position: fixed; top: 0; left: 0; width: 100%; height: 100%;
            pointer-events: none; z-index: 1; display: none;
        }
        @media (min-width: 1024px) { .grid-lines { display: block; } }
        .grid-line {
            position: absolute; top: 0; width: 1px; height: 100%;
            background-color: rgba(26, 26, 26, 0.08);
        }
        .grid-line:nth-child(1) { left: 8%; } .grid-line:nth-child(2) { left: 36%; }
        .grid-line:nth-child(3) { left: 64%; } .grid-line:nth-child(4) { left: 92%; }

        h1, h2, h3, h4 { font-family: var(--font-serif); font-weight: 400; line-height: 0.9; }
        .overline { font-family: var(--font-sans); font-size: 0.75rem; text-transform: uppercase; letter-spacing: 0.25em; color: var(--text-muted); }
        .hero-title { font-size: clamp(3rem, 8vw, 7rem); letter-spacing: -0.02em; margin-bottom: 1rem; }
        .section-title { font-size: clamp(2rem, 5vw, 4rem); letter-spacing: -0.01em; margin-bottom: 2rem; }

        .container { max-width: 1600px; margin: 0 auto; padding: 0 2rem; position: relative; z-index: 2; }
        @media (min-width: 768px) { .container { padding: 0 4rem; } }
        section { padding: 8rem 2rem; position: relative; }

        .hero { min-height: 100vh; display: flex; align-items: flex-end; padding-bottom: 6rem; position: relative; }
        .hero-meta { display: flex; gap: 2rem; margin-bottom: 2rem; align-items: center; }
        .hero-line { width: 3rem; height: 1px; background-color: var(--text-primary); }
        .hero-description { font-size: 1.125rem; color: var(--text-muted); max-width: 32rem; margin-top: 2rem; line-height: 1.625; }

        .vertical-label {
            position: absolute; right: 2rem; top: 50%; transform: translateY(-50%);
            writing-mode: vertical-rl; text-orientation: mixed;
            font-family: var(--font-sans); font-size: 0.625rem;
            text-transform: uppercase; letter-spacing: 0.3em; color: var(--text-muted); display: none;
        }
        @media (min-width: 1024px) { .vertical-label { display: block; } }

        .stats-grid { display: grid; grid-template-columns: repeat(2, 1fr); gap: 2rem; margin-top: 4rem; }
        @media (min-width: 768px) { .stats-grid { grid-template-columns: repeat(4, 1fr); } }
        .stat-card { border-top: 1px solid rgba(26, 26, 26, 0.2); padding-top: 1.5rem; transition: all 0.7s ease-out; }
        .stat-card:hover { border-top-color: var(--accent); }
        .stat-number { font-family: var(--font-serif); font-size: clamp(2.5rem, 5vw, 4rem); line-height: 1; margin-bottom: 0.5rem; }
        .stat-label { font-size: 0.75rem; text-transform: uppercase; letter-spacing: 0.2em; color: var(--text-muted); }

        .section-dark { background-color: var(--text-primary); color: var(--bg-primary); }
        .section-dark .overline { color: var(--bg-muted); opacity: 0.8; }
        .section-dark .stat-card { border-top-color: rgba(249, 248, 246, 0.2); }
        .section-dark .stat-card:hover { border-top-color: var(--accent); }

        .tabs { display: flex; gap: 0; border-bottom: 1px solid rgba(26, 26, 26, 0.1); margin-bottom: 3rem; overflow-x: auto; }
        .section-dark .tabs { border-bottom-color: rgba(249, 248, 246, 0.1); }
        .tab {
            font-family: var(--font-sans); font-size: 0.75rem; text-transform: uppercase;
            letter-spacing: 0.2em; padding: 1rem 1.5rem; background: none; border: none;
            border-bottom: 2px solid transparent; color: var(--text-muted);
            cursor: pointer; transition: all 0.5s ease; white-space: nowrap;
        }
        .section-dark .tab { color: var(--bg-muted); opacity: 0.6; }
        .tab:hover { color: var(--text-primary); }
        .section-dark .tab:hover { color: var(--bg-primary); opacity: 1; }
        .tab.active { color: var(--text-primary); border-bottom-color: var(--accent); }
        .section-dark .tab.active { color: var(--bg-primary); opacity: 1; }

        .leaderboard { width: 100%; }
        .leaderboard-item {
            display: grid; grid-template-columns: 3rem 1fr auto; gap: 1.5rem;
            padding: 1.5rem 0; border-top: 1px solid rgba(26, 26, 26, 0.1);
            transition: all 0.7s ease; align-items: center; cursor: pointer;
        }
        .section-dark .leaderboard-item { border-top-color: rgba(249, 248, 246, 0.1); }
        .leaderboard-item:hover { padding-left: 1rem; border-top-color: var(--accent); }
        .leaderboard-item:first-child { border-top: none; }
        .rank { font-family: var(--font-serif); font-size: 1.5rem; color: var(--text-muted); font-weight: 300; }
        .top-3 .rank { color: var(--accent); font-weight: 400; }
        .leaderboard-name { font-family: var(--font-serif); font-size: 1.25rem; transition: color 0.5s ease; }
        .leaderboard-item:hover .leaderboard-name { color: var(--accent); }
        .leaderboard-count { font-family: var(--font-serif); font-size: 1.5rem; color: var(--text-muted); }
        .section-dark .leaderboard-count { color: var(--bg-muted); }

        .audience-grid { display: grid; grid-template-columns: 1fr; gap: 2rem; }
        @media (min-width: 768px) { .audience-grid { grid-template-columns: repeat(2, 1fr); } }
        @media (min-width: 1024px) { .audience-grid { grid-template-columns: repeat(3, 1fr); } }
        .audience-card { border-top: 1px solid rgba(26, 26, 26, 0.2); padding: 2rem 0; transition: all 0.7s ease; cursor: pointer; }
        .audience-card:hover { border-top-color: var(--accent); padding-left: 1rem; }
        .audience-name { font-family: var(--font-serif); font-size: 1.5rem; margin-bottom: 1rem; }
        .audience-song { font-size: 0.875rem; color: var(--text-muted); padding: 0.5rem 0; border-bottom: 1px solid rgba(26, 26, 26, 0.05); }
        .song-count { float: right; font-family: var(--font-serif); color: var(--accent); }

        .chart-container { margin-top: 3rem; }
        .chart-bar-item { display: flex; align-items: center; gap: 1rem; margin-bottom: 1rem; }
        .chart-label { min-width: 8rem; font-family: var(--font-serif); font-size: 0.875rem; text-align: right; }
        .chart-bar-bg { flex: 1; height: 2rem; background-color: rgba(26, 26, 26, 0.05); position: relative; overflow: hidden; }
        .section-dark .chart-bar-bg { background-color: rgba(249, 248, 246, 0.05); }
        .chart-bar-fill { height: 100%; background-color: var(--text-primary); transition: width 1.5s cubic-bezier(0.25, 0.46, 0.45, 0.94); width: 0; }
        .section-dark .chart-bar-fill { background-color: var(--bg-primary); }
        .chart-bar-fill.accent { background-color: var(--accent); }
        .chart-value { min-width: 3rem; font-family: var(--font-serif); font-size: 1.25rem; }

        .modal-overlay {
            position: fixed; top: 0; left: 0; width: 100%; height: 100%;
            background-color: rgba(26, 26, 26, 0.8); z-index: 1000;
            display: flex; align-items: center; justify-content: center;
            opacity: 0; visibility: hidden; transition: all 0.7s ease;
        }
        .modal-overlay.active { opacity: 1; visibility: visible; }
        .modal {
            background-color: var(--bg-primary); max-width: 800px; width: 90%;
            max-height: 80vh; overflow-y: auto; padding: 3rem; position: relative;
            transform: translateY(2rem); transition: transform 0.7s ease;
        }
        .modal-overlay.active .modal { transform: translateY(0); }
        .modal-close {
            position: absolute; top: 1.5rem; right: 1.5rem; background: none;
            border: 1px solid var(--text-primary); width: 2.5rem; height: 2.5rem;
            display: flex; align-items: center; justify-content: center;
            cursor: pointer; font-size: 1.25rem; transition: all 0.5s ease;
        }
        .modal-close:hover { background-color: var(--text-primary); color: var(--bg-primary); }
        .modal-title { font-family: var(--font-serif); font-size: 2rem; margin-bottom: 0.5rem; }
        .modal-subtitle { font-size: 0.75rem; text-transform: uppercase; letter-spacing: 0.2em; color: var(--text-muted); margin-bottom: 2rem; }
        .modal-song-list { border-top: 1px solid rgba(26, 26, 26, 0.1); }
        .modal-song-item { display: grid; grid-template-columns: 1fr auto; padding: 1rem 0; border-bottom: 1px solid rgba(26, 26, 26, 0.05); }
        .modal-song-name { font-family: var(--font-serif); font-size: 1.125rem; }
        .modal-song-date { font-size: 0.75rem; color: var(--text-muted); text-transform: uppercase; letter-spacing: 0.1em; }

        .nav {
            position: fixed; top: 0; left: 0; right: 0; z-index: 100;
            padding: 1.5rem 2rem; display: flex; justify-content: space-between;
            align-items: center; background-color: rgba(249, 248, 246, 0.9);
            backdrop-filter: blur(10px); border-bottom: 1px solid rgba(26, 26, 26, 0.1);
            transform: translateY(-100%); transition: transform 0.7s ease;
        }
        .nav.visible { transform: translateY(0); }
        .nav-brand { font-family: var(--font-serif); font-size: 1.25rem; }
        .nav-links { display: flex; gap: 2rem; list-style: none; }
        .nav-link { font-size: 0.75rem; text-transform: uppercase; letter-spacing: 0.2em; color: var(--text-muted); text-decoration: none; transition: color 0.5s ease; }
        .nav-link:hover { color: var(--text-primary); }

        .footer { padding: 4rem 2rem; border-top: 1px solid rgba(26, 26, 26, 0.1); text-align: center; }
        .footer-text { font-size: 0.75rem; text-transform: uppercase; letter-spacing: 0.2em; color: var(--text-muted); }

        .fade-in { opacity: 0; transform: translateY(2rem); transition: opacity 1.5s ease, transform 1.5s ease; }
        .fade-in.visible { opacity: 1; transform: translateY(0); }

        .drop-cap::first-letter { float: left; font-family: var(--font-serif); font-size: 4.5rem; line-height: 0.8; margin-right: 0.75rem; margin-top: 0.25rem; color: var(--accent); }
        .divider { width: 3rem; height: 1px; background-color: var(--accent); margin: 2rem 0; }

        @media (max-width: 768px) { section { padding: 5rem 1.5rem; } .hero { padding-bottom: 4rem; } .tab { padding: 0.75rem 1rem; font-size: 0.625rem; } .leaderboard-item { grid-template-columns: 2rem 1fr auto; gap: 1rem; } }
    </style>
</head>
<body>
    <div class="paper-texture"></div>
    <div class="grid-lines"><div class="grid-line"></div><div class="grid-line"></div><div class="grid-line"></div><div class="grid-line"></div></div>

    <nav class="nav" id="nav">
        <div class="nav-brand">岁己SUI</div>
        <ul class="nav-links">
            <li><a href="#overview" class="nav-link">概览</a></li>
            <li><a href="#total" class="nav-link">总榜</a></li>
            <li><a href="#monthly" class="nav-link">月度</a></li>
            <li><a href="#quarterly" class="nav-link">季度</a></li>
            <li><a href="#audiences" class="nav-link">观众</a></li>
        </ul>
    </nav>

    <section class="hero">
        <div class="vertical-label">Editorial · Song Requests · 2024-2026</div>
        <div class="container">
            <div class="hero-content">
                <div class="hero-meta"><div class="hero-line"></div><span class="overline">Virtual Streamer · 岁己SUI</span></div>
                <h1 class="hero-title">点歌<br><em>统计</em></h1>
                <p class="hero-description drop-cap">收录了虚拟主播岁己SUI自2024年7月至今的所有点歌记录。每一位"饼干岁"的心意，都化作了一首首动人的旋律。点击观众名字，查看他们点过的所有歌曲。</p>
                <div class="stats-grid" id="overview-stats">
                    <div class="stat-card fade-in"><div class="stat-number" id="stat-total">0</div><div class="stat-label">总点歌次数</div></div>
                    <div class="stat-card fade-in"><div class="stat-number" id="stat-audiences">0</div><div class="stat-label">独立观众</div></div>
                    <div class="stat-card fade-in"><div class="stat-number" id="stat-songs">0</div><div class="stat-label">不同歌曲</div></div>
                    <div class="stat-card fade-in"><div class="stat-number" id="stat-duration">0</div><div class="stat-label">统计月数</div></div>
                </div>
            </div>
        </div>
    </section>

    <section id="total">
        <div class="container">
            <div class="fade-in"><span class="overline">Total Leaderboard</span><h2 class="section-title">总排行榜</h2><div class="divider"></div>
            <p style="color: var(--text-muted); max-width: 32rem; margin-bottom: 2rem;">点击任意观众名字，查看他们点过的所有歌曲。</p></div>
            <div class="leaderboard" id="total-leaderboard"></div>
        </div>
    </section>

    <section class="section-dark" id="monthly">
        <div class="container">
            <div class="fade-in"><span class="overline">Monthly Rankings</span><h2 class="section-title">月度<span style="font-style: italic; color: var(--accent);">排行榜</span></h2><div class="divider" style="background-color: var(--accent);"></div></div>
            <div class="tabs" id="monthly-tabs"></div>
            <div class="leaderboard" id="monthly-leaderboard"></div>
        </div>
    </section>

    <section id="quarterly">
        <div class="container">
            <div class="fade-in"><span class="overline">Quarterly Rankings</span><h2 class="section-title">季度<span style="font-style: italic; color: var(--accent);">排行榜</span></h2><div class="divider"></div></div>
            <div class="tabs" id="quarterly-tabs"></div>
            <div class="leaderboard" id="quarterly-leaderboard"></div>
        </div>
    </section>

    <section class="section-dark" id="songs">
        <div class="container">
            <div class="fade-in"><span class="overline">Popular Songs</span><h2 class="section-title">热门<span style="font-style: italic;">歌曲</span></h2><div class="divider" style="background-color: var(--accent);"></div></div>
            <div class="leaderboard" id="song-leaderboard"></div>
        </div>
    </section>

    <section id="audiences">
        <div class="container">
            <div class="fade-in"><span class="overline">Audience Preferences</span><h2 class="section-title">观众<span style="font-style: italic; color: var(--accent);">喜好</span></h2><div class="divider"></div>
            <p style="color: var(--text-muted); max-width: 32rem; margin-bottom: 3rem;">每一位观众都有自己钟爱的歌曲。以下是点歌次数最多的观众及其偏好歌曲。</p></div>
            <div class="audience-grid" id="audience-preferences"></div>
        </div>
    </section>

    <section class="section-dark" id="trends">
        <div class="container">
            <div class="fade-in"><span class="overline">Monthly Trends</span><h2 class="section-title">点歌<span style="font-style: italic;">趋势</span></h2><div class="divider" style="background-color: var(--accent);"></div></div>
            <div class="chart-container" id="trends-chart"></div>
        </div>
    </section>

    <footer class="footer">
        <p class="footer-text">岁己SUI · 点歌统计 · <span id="current-year"></span></p>
        <p class="footer-text" style="margin-top: 0.5rem; font-size: 0.625rem;">Designed with Elegance · Luxury Editorial Style</p>
    </footer>

    <div class="modal-overlay" id="modal-overlay">
        <div class="modal">
            <button class="modal-close" onclick="closeModal()">&times;</button>
            <div class="modal-title" id="modal-title"></div>
            <div class="modal-subtitle" id="modal-subtitle"></div>
            <div class="modal-song-list" id="modal-song-list"></div>
        </div>
    </div>

    <script>
// ========== EMBEDDED DATA ==========
const appData = ''' + json.dumps(data, ensure_ascii=False) + ''';

// Process raw data for modal
const rawData = {};
appData.raw_data.forEach(record => {
    if (!rawData[record.audience]) rawData[record.audience] = [];
    rawData[record.audience].push({ song: record.song, date: record.date });
});
for (const a in rawData) rawData[a].sort((a, b) => b.date.localeCompare(a.date));

// ========== APP INIT ==========
let currentMonth = null, currentQuarter = null;

function initApp() {
    updateOverviewStats();
    renderTotalLeaderboard();
    renderMonthlyTabs();
    renderQuarterlyTabs();
    renderSongLeaderboard();
    renderAudiencePreferences();
    renderTrendsChart();
    initScrollAnimations();
    initNavigation();
}

function updateOverviewStats() {
    const m = appData.metadata;
    animateNumber('stat-total', m.total_records);
    animateNumber('stat-audiences', m.unique_audiences);
    animateNumber('stat-songs', m.unique_songs);
    animateNumber('stat-duration', Object.keys(appData.monthly_trends).length);
}

function animateNumber(id, target) {
    const el = document.getElementById(id);
    const start = performance.now();
    function tick(now) {
        const p = Math.min((now - start) / 2000, 1), e = 1 - Math.pow(1-p, 3);
        el.textContent = Math.floor(e * target);
        if (p < 1) requestAnimationFrame(tick); else el.textContent = target;
    }
    requestAnimationFrame(tick);
}

function renderTotalLeaderboard() {
    const c = document.getElementById('total-leaderboard');
    c.innerHTML = '<div>';
    (appData.total_leaderboard || []).slice(0, 20).forEach((item, i) => {
        c.innerHTML += `<div class="leaderboard-item fade-in ${i<3?'top-3':''}" style="transition-delay:${i*100}ms" onclick="showAudienceDetail('${item.audience}')"><div class="rank">${item.rank}</div><div class="leaderboard-name">${item.audience}</div><div class="leaderboard-count">${item.count} 次</div></div>`;
    });
    c.innerHTML += '</div>';
}

function renderMonthlyTabs() {
    const c = document.getElementById('monthly-tabs');
    const months = Object.keys(appData.monthly_leaderboard).sort().reverse();
    currentMonth = months[0] || '';
    c.innerHTML = months.map(m => `<button class="tab ${m===currentMonth?'active':''}" onclick="showMonth('${m}')">${m}</button>`).join('');
    renderMonthlyLeaderboard();
}
function showMonth(m) {
    currentMonth = m;
    document.querySelectorAll('#monthly-tabs .tab').forEach(t => t.classList.toggle('active', t.textContent.trim() === m));
    renderMonthlyLeaderboard();
}
function renderMonthlyLeaderboard() {
    const c = document.getElementById('monthly-leaderboard'), d = appData.monthly_leaderboard[currentMonth] || [];
    c.innerHTML = d.map((item,i) => `<div class="leaderboard-item fade-in" style="transition-delay:${i*100}ms" onclick="showAudienceDetail('${item.audience}')"><div class="rank">${item.rank}</div><div class="leaderboard-name">${item.audience}</div><div class="leaderboard-count">${item.count} 次</div></div>`).join('');
}

function renderQuarterlyTabs() {
    const c = document.getElementById('quarterly-tabs');
    const qs = Object.keys(appData.quarterly_leaderboard).sort().reverse();
    currentQuarter = qs[0] || '';
    c.innerHTML = qs.map(q => `<button class="tab ${q===currentQuarter?'active':''}" onclick="showQuarter('${q}')">${q}</button>`).join('');
    renderQuarterlyLeaderboard();
}
function showQuarter(q) {
    currentQuarter = q;
    document.querySelectorAll('#quarterly-tabs .tab').forEach(t => t.classList.toggle('active', t.textContent.trim() === q));
    renderQuarterlyLeaderboard();
}
function renderQuarterlyLeaderboard() {
    const c = document.getElementById('quarterly-leaderboard'), d = appData.quarterly_leaderboard[currentQuarter] || [];
    c.innerHTML = d.map((item,i) => `<div class="leaderboard-item fade-in" style="transition-delay:${i*100}ms" onclick="showAudienceDetail('${item.audience}')"><div class="rank">${item.rank}</div><div class="leaderboard-name">${item.audience}</div><div class="leaderboard-count">${item.count} 次</div></div>`).join('');
}

function renderSongLeaderboard() {
    const c = document.getElementById('song-leaderboard');
    c.innerHTML = (appData.song_leaderboard || []).slice(0, 20).map((item, i) =>
        `<div class="leaderboard-item fade-in" style="transition-delay:${i*100}ms"><div class="rank">${item.rank}</div><div class="leaderboard-name">${item.song}</div><div class="leaderboard-count">${item.count} 次</div></div>`
    ).join('');
}

function renderAudiencePreferences() {
    const c = document.getElementById('audience-preferences');
    let html = '', count = 0;
    for (const [aud, songs] of Object.entries(appData.audience_preferences)) {
        if (count >= 9) break;
        html += `<div class="audience-card fade-in" style="transition-delay:${count*150}ms" onclick="showAudienceDetail('${aud}')">
            <div class="audience-name">${aud}</div>${songs.map(s => `<div class="audience-song">${s.song}<span class="song-count">${s.count} 次</span></div>`).join('')}
        </div>`;
        count++;
    }
    c.innerHTML = html;
}

function renderTrendsChart() {
    const c = document.getElementById('trends-chart');
    const trends = appData.monthly_trends;
    const months = Object.keys(trends).sort(), maxCount = Math.max(...Object.values(trends));
    c.innerHTML = months.map((m, i) => {
        const pct = (trends[m] / maxCount) * 100;
        return `<div class="chart-bar-item fade-in" style="transition-delay:${i*50}ms">
            <div class="chart-label">${m}</div>
            <div class="chart-bar-bg"><div class="chart-bar-fill ${i===months.length-1?'accent':''}" data-width="${pct}"></div></div>
            <div class="chart-value">${trends[m]}</div>
        </div>`;
    }).join('');
    setTimeout(() => document.querySelectorAll('.chart-bar-fill').forEach(b => b.style.width = b.dataset.width + '%'), 500);
}

function showAudienceDetail(name) {
    const songs = rawData[name] || [], uniqueSongs = new Set(songs.map(s => s.song)).size;
    document.getElementById('modal-title').textContent = name;
    document.getElementById('modal-subtitle').textContent = `共点歌 ${songs.length} 次 · ${uniqueSongs} 首不同歌曲`;
    const sc = {}, sd = {};
    songs.forEach(r => { sc[r.song] = (sc[r.song]||0)+1; if(!sd[r.song]) sd[r.song]=[]; sd[r.song].push(r.date); });
    const sorted = Object.entries(sc).sort((a,b) => b[1]-a[1]);
    document.getElementById('modal-song-list').innerHTML = sorted.map(([s,c]) =>
        `<div class="modal-song-item"><div><div class="modal-song-name">${s}</div><div class="modal-song-date">最近点歌: ${sd[s][0]}</div></div><div style="font-family:var(--font-serif);font-size:1.5rem;color:var(--accent)">${c} 次</div></div>`
    ).join('');
    const overlay = document.getElementById('modal-overlay');
    overlay.classList.add('active');
    overlay.onclick = e => { if(e.target===overlay) closeModal(); };
}
function closeModal() { document.getElementById('modal-overlay').classList.remove('active'); }
document.addEventListener('keydown', e => { if(e.key==='Escape') closeModal(); });

function initScrollAnimations() {
    const obs = new IntersectionObserver(entries => entries.forEach(e => { if(e.isIntersecting) e.target.classList.add('visible'); }), { threshold: 0.1, rootMargin: '0px 0px -50px 0px' });
    document.querySelectorAll('.fade-in').forEach(el => obs.observe(el));
}
function initNavigation() {
    const nav = document.getElementById('nav');
    window.addEventListener('scroll', () => { nav.classList.toggle('visible', window.pageYOffset > 100); });
    document.getElementById('current-year').textContent = new Date().getFullYear();
}

initApp();
    </script>
</body>
</html>'''

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print(f"Done! Generated self-contained index.html ({len(html)} bytes)")
