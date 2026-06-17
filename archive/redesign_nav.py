#!/usr/bin/env python3
"""Redesign the tab navigation to a compact month grid with current month highlighted."""

import re

# Read the HTML file
with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# ===== 1. Replace the old .tabs and .tab CSS with new month-grid design =====
old_tabs_css = """        .tabs { display: flex; gap: 0; border-bottom: 1px solid rgba(26, 26, 26, 0.1); margin-bottom: 3rem; overflow-x: auto; }
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
        .section-dark .tab.active { color: var(--bg-primary); opacity: 1; }"""

new_tabs_css = """        /* --- Time period picker (month/quarter/year grid) --- */
        .time-picker {
            display: flex; flex-wrap: wrap; gap: 0.5rem 0.75rem;
            margin-bottom: 3rem; justify-content: flex-start; align-items: stretch;
        }
        .time-chip {
            font-family: var(--font-sans); font-size: 0.7rem; text-transform: uppercase;
            letter-spacing: 0.15em; padding: 0.55rem 1rem;
            background: none; border: 1px solid rgba(26, 26, 26, 0.12);
            color: var(--text-muted); cursor: pointer;
            transition: all 0.5s cubic-bezier(0.25, 0.46, 0.45, 0.94);
            white-space: nowrap; position: relative; overflow: hidden;
        }
        .time-chip::after {
            content: ''; position: absolute; inset: 0;
            background-color: var(--accent); transform: scaleX(0);
            transform-origin: left; z-index: -1;
            transition: transform 0.6s cubic-bezier(0.25, 0.46, 0.45, 0.94);
        }
        .time-chip:hover { color: var(--text-primary); border-color: rgba(26, 26, 26, 0.35); }
        .section-dark .time-chip {
            border-color: rgba(249, 248, 246, 0.12); color: var(--bg-muted); opacity: 0.55;
        }
        .section-dark .time-chip:hover {
            color: var(--bg-primary); opacity: 1; border-color: rgba(249, 248, 246, 0.3);
        }

        /* Current / active chip — large & golden */
        .time-chip.current {
            font-size: 0.85rem; font-weight: 500; letter-spacing: 0.18em;
            padding: 0.7rem 1.4rem; border-color: var(--accent);
            color: var(--text-primary) !important; opacity: 1 !important;
            background: linear-gradient(135deg, rgba(212, 175, 55, 0.06), rgba(212, 175, 55, 0.02));
        }
        .section-dark .time-chip.current {
            color: var(--accent) !important;
            background: linear-gradient(135deg, rgba(212, 175, 55, 0.12), rgba(212, 175, 55, 0.05));
        }
        .time-chip.current::after { transform: scaleX(0); }
        .time-chip.current:hover { border-color: var(--accent); box-shadow: 0 0 20px rgba(212, 175, 55, 0.12); }

        /* Non-current chips in dark section */
        .section-dark .time-chip:not(.current):hover { border-color: var(--accent); opacity: 0.85; }"""

html = html.replace(old_tabs_css, new_tabs_css)

# ===== 2. Update mobile responsive rule for new class =====
html = html.replace(
    '.tab { padding: 0.75rem 1rem; font-size: 0.625rem; }',
    '.time-chip { padding: 0.4rem 0.7rem; font-size: 0.6rem; } .time-chip.current { padding: 0.5rem 1rem; font-size: 0.72rem; }'
)

# ===== 3. Replace renderMonthlyTabs JS function =====
old_monthly_js = '''function renderMonthlyTabs() {
    const c = document.getElementById('monthly-tabs');
    const months = Object.keys(appData.monthly_leaderboard).sort().reverse();
    currentMonth = months[0] || '';
    c.innerHTML = months.map(m => `<button class="tab ${m===currentMonth?'active':''}" onclick="showMonth('${m}')">${m}</button>`).join('');
    renderMonthlyLeaderboard();
}'''

new_monthly_js = '''function renderMonthlyTabs() {
    const c = document.getElementById('monthly-tabs');
    const months = Object.keys(appData.monthly_leaderboard).sort().reverse();
    currentMonth = months[0] || '';
    c.innerHTML = '<div class="time-picker">' +
        months.map(m => `<button class="time-chip ${m===currentMonth?'current':''}" onclick="showMonth('${m}')">${m}</button>`).join('') +
        '</div>';
    renderMonthlyLeaderboard();
}'''

html = html.replace(old_monthly_js, new_monthly_js)

# ===== 4. Replace showMonth JS (update class toggle selector) =====
old_show_month = '''function showMonth(m) {
    currentMonth = m;
    document.querySelectorAll('#monthly-tabs .tab').forEach(t => t.classList.toggle('active', t.textContent.trim() === m));
    renderMonthlyLeaderboard();
}'''

new_show_month = '''function showMonth(m) {
    currentMonth = m;
    document.querySelectorAll('#monthly-tabs .time-chip').forEach(t => {
        t.classList.toggle('current', t.textContent.trim() === m);
    });
    renderMonthlyLeaderboard();
}'''

html = html.replace(old_show_month, new_show_month)

# ===== 5. Same for quarterly =====
old_quarterly_tabs = '''function renderQuarterlyTabs() {
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
        }'''

new_quarterly_tabs = '''function renderQuarterlyTabs() {
    const c = document.getElementById('quarterly-tabs');
    const qs = Object.keys(appData.quarterly_leaderboard).sort().reverse();
    currentQuarter = qs[0] || '';
    c.innerHTML = '<div class="time-picker">' +
        qs.map(q => `<button class="time-chip ${q===currentQuarter?'current':''}" onclick="showQuarter('${q}')">${q}</button>`).join('') +
        '</div>';
    renderQuarterlyLeaderboard();
}
        function showQuarter(q) {
            currentQuarter = q;
            document.querySelectorAll('#quarterly-tabs .time-chip').forEach(t => {
                t.classList.toggle('current', t.textContent.trim() === q);
            });
            renderQuarterlyLeaderboard();
        }'''

html = html.replace(old_quarterly_tabs, new_quarterly_tabs)

# ===== 6. Same for yearly =====
old_yearly_tabs = '''function renderYearlyTabs() {
            const c = document.getElementById('yearly-tabs');
            const years = Object.keys(appData.yearly_leaderboard).sort().reverse();
            currentYear = years[0] || '';
            c.innerHTML = years.map(y => `<button class="tab ${y===currentYear?'active':''}" onclick="showYear('${y}')">${y}</button>`).join('');
            renderYearlyLeaderboard();
        }
        function showYear(y) {
            currentYear = y;
            document.querySelectorAll('#yearly-tabs .tab').forEach(t => t.classList.toggle('active', t.textContent.trim() === y));
            renderYearlyLeaderboard();
        }'''

new_yearly_tabs = '''function renderYearlyTabs() {
            const c = document.getElementById('yearly-tabs');
            const years = Object.keys(appData.yearly_leaderboard).sort().reverse();
            currentYear = years[0] || '';
            c.innerHTML = '<div class="time-picker">' +
                years.map(y => `<button class="time-chip ${y===currentYear?'current':''}" onclick="showYear('${y}')">${y}</button>`).join('') +
                '</div>';
            renderYearlyLeaderboard();
        }
        function showYear(y) {
            currentYear = y;
            document.querySelectorAll('#yearly-tabs .time-chip').forEach(t => {
                t.classList.toggle('current', t.textContent.trim() === y);
            });
            renderYearlyLeaderboard();
        }'''

html = html.replace(old_yearly_tabs, new_yearly_tabs)

# Write back
with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Done! Navigation redesigned to time-chip grid layout.")
