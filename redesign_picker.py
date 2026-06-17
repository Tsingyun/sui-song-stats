#!/usr/bin/env python3
"""Replace the messy time-chip grid with an elegant headline-style picker:
- Large serif display of current period (like a sub-headline)
- Subtle prev/next arrows
- Discreet dropdown for quick jump
"""

import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# ===== 1. Replace the time-picker / time-chip CSS with elegant headline picker =====
old_picker_css = r'''        \/\* --- Time period picker \(month/quarter/year grid\) --- \*/
        .time-picker \{.*?\}
        .time-chip \{.*?\}
        .time-chip::after \{.*?\}
        .time-chip:hover \{.*?\}
        .section-dark .time-chip \{.*?\}
        .time-chip.current \{.*?\}
        .section-dark .time-chip.current \{.*?\}
        .time-chip.current::after \{ transform: scaleX\(0\); \}
        .time-chip.current:hover \{.*?\}
        .section-dark .time-chip:not\(.current\):hover \{.*?\}'''

new_picker_css = '''        /* --- Elegant headline-style time picker --- */
        .time-picker {
            display: flex; align-items: center; gap: 1.5rem;
            margin-bottom: 3rem; padding-bottom: 2rem;
            border-bottom: 1px solid rgba(26, 26, 26, 0.08);
        }
        .section-dark .time-picker {
            border-bottom-color: rgba(249, 248, 246, 0.08);
        }

        /* Prev / Next arrow buttons */
        .time-nav-btn {
            width: 2.5rem; height: 2.5rem;
            background: none; border: 1px solid rgba(26, 26, 26, 0.15);
            color: var(--text-muted); font-size: 1rem; font-family: var(--font-sans);
            cursor: pointer;
            transition: all 0.5s cubic-bezier(0.25, 0.46, 0.45, 0.94);
            display: flex; align-items: center; justify-content: center;
            flex-shrink: 0;
        }
        .time-nav-btn:hover {
            color: var(--accent); border-color: var(--accent);
            background-color: rgba(212, 175, 55, 0.04);
        }
        .section-dark .time-nav-btn {
            border-color: rgba(249, 248, 246, 0.15);
            color: var(--bg-muted); opacity: 0.6;
        }
        .section-dark .time-nav-btn:hover {
            color: var(--accent); opacity: 1;
            border-color: var(--accent);
            background-color: rgba(212, 175, 55, 0.08);
        }

        /* Current period - large serif headline */
        .time-current {
            flex: 1; text-align: center;
            font-family: var(--font-serif); font-size: clamp(1.75rem, 3vw, 2.5rem);
            font-weight: 400; letter-spacing: 0.05em;
            color: var(--text-primary);
            min-width: 8rem;
            line-height: 1;
        }
        .section-dark .time-current {
            color: #F9F8F6;
        }

        /* Jump-to dropdown */
        .time-jump {
            position: relative; flex-shrink: 0;
        }
        .time-jump-select {
            appearance: none; -webkit-appearance: none;
            font-family: var(--font-sans); font-size: 0.7rem;
            text-transform: uppercase; letter-spacing: 0.12em;
            padding: 0.55rem 2rem 0.55rem 0.85rem;
            border: 1px solid rgba(26, 26, 26, 0.12);
            color: var(--text-muted); background: transparent;
            cursor: pointer;
            transition: all 0.5s ease;
            max-width: 10rem;
        }
        .time-jump-select:hover,
        .time-jump-select:focus {
            border-color: var(--accent); color: var(--text-primary);
            outline: none;
        }
        .section-dark .time-jump-select {
            border-color: rgba(249, 248, 246, 0.12);
            color: var(--bg-muted); opacity: 0.6;
        }
        .section-dark .time-jump-select:hover,
        .section-dark .time-jump-select:focus {
            border-color: var(--accent); color: var(--bg-primary); opacity: 1;
        }

        /* Dropdown chevron indicator */
        .time-jump::after {
            content: '';
            position: absolute; right: 0.7rem; top: 50%; transform: translateY(-50%);
            width: 4px; height: 4px;
            border-right: 1.5px solid var(--text-muted);
            border-bottom: 1.5px solid var(--text-muted);
            transform: translateY(-70%) rotate(45deg);
            pointer-events: none;
            transition: border-color 0.5s ease;
        }
        .section-dark .time-jump::after {
            border-color: var(--bg-muted);
        }'''

html = re.sub(old_picker_css, new_picker_css, html)

# Update mobile responsive rule too
html = html.replace(
    '.time-chip { padding: 0.4rem 0.7rem; font-size: 0.6rem; } .time-chip.current { padding: 0.5rem 1rem; font-size: 0.72rem; }',
    '.time-current { font-size: 1.25rem !important; } .time-nav-btn { width: 2rem; height: 2rem; } .time-jump-select { font-size: 0.625rem; padding: 0.4rem 1.6rem 0.4rem 0.65rem; }'
)

# ===== 2. Replace renderMonthlyTabs JS =====
old_monthly_js = r'''function renderMonthlyTabs\(\) \{
    const c = document\.getElementById\('monthly-tabs'\);\s*
    const months = Object\.keys\(appData\.monthly_leaderboard\)\.sort\(\)\.reverse\(\);\s*
    currentMonth = months\[0\] \|| '';\s*
    c\.innerHTML = '<div class="time-picker">' \+
        months\.map\(m => `<button class="time-chip \$\{m===currentMonth\?'current':''\}" onclick="showMonth\('\$m'\)">\$m</button>`\)\.join\(''\) \+
        '</div>';\s*
    renderMonthlyLeaderboard\(\);\s*\}'''

new_monthly_js = '''function renderMonthlyTabs() {
    const c = document.getElementById('monthly-tabs');
    const periods = Object.keys(appData.monthly_leaderboard).sort().reverse();
    currentMonth = periods[0] || '';

    c.innerHTML = `
        <div class="time-picker">
            <button class="time-nav-btn" onclick="navigateMonth(-1)" aria-label="上个月">&#10094;</button>
            <div class="time-current" id="month-display">${currentMonth}</div>
            <button class="time-nav-btn" onclick="navigateMonth(1)" aria-label="下个月">&#10095;</button>
            <div class="time-jump">
                <select class="time-jump-select" onchange="showMonth(this.value)" aria-label="跳转到指定月份">
                    ${periods.map(p => `<option value="${p}" ${p===currentMonth?'selected':''}>${p}</option>`).join('')}
                </select>
            </div>
        </div>`;
    renderMonthlyLeaderboard();
}'''

html = re.sub(old_monthly_js, new_monthly_js, html)

# Add navigateMonth function after showMonth
old_show_month = r'''function showMonth\(m\) \{
    currentMonth = m;\s*
    document\.querySelectorAll\('#monthly-tabs \.time-chip'\)\.forEach\(t => \{
        t\.classList\.toggle\('current', t\.textContent\.trim\(\) === m\);\s*\}\);\s*
    renderMonthlyLeaderboard\(\);\s*\}'''

new_show_month = '''function showMonth(m) {
    currentMonth = m;
    const disp = document.getElementById('month-display');
    if (disp) disp.textContent = m;
    // Sync the select dropdown
    const sel = document.querySelector('#monthly-tabs .time-jump select');
    if (sel) sel.value = m;
    renderMonthlyLeaderboard();
}

function navigateMonth(delta) {
    const periods = Object.keys(appData.monthly_leaderboard).sort();
    const idx = periods.indexOf(currentMonth);
    if (idx === -1) return;
    // periods are ascending, but we want reverse order navigation
    const revIdx = periods.length - 1 - idx;
    const newRevIdx = Math.max(0, Math.min(periods.length - 1, revIdx + delta));
    showMonth(periods[periods.length - 1 - newRevIdx]);
}'''

html = re.sub(old_show_month, new_show_month, html)

# ===== 3. Same for quarterly =====
old_quarterly_js = r'''function renderQuarterlyTabs\(\) \{
    const c = document\.getElementById\('quarterly-tabs'\);\s*
    const qs = Object\.keys\(appData\.quarterly_leaderboard\)\.sort\(\)\.reverse\(\);\s*
    currentQuarter = qs\[0\] \|| '';\s*
    c\.innerHTML = '<div class="time-picker">' \+
        qs\.map\(q => `<button class="time-chip \$\{q===currentQuarter\?'current':''\}" onclick="showQuarter\('\$q'\)">\$q</button>`\)\.join\(''\) \+
        '</div>';\s*
    renderQuarterlyLeaderboard\(\);\s*\}
        function showQuarter\(q\) \{
            currentQuarter = q;\s*
            document\.querySelectorAll\('#quarterly-tabs \.time-chip'\)\.forEach\(t => \{
                t\.classList\.toggle\('current', t\.textContent\.trim\(\) === q\);\s*\}\);\s*
            renderQuarterlyLeaderboard\(\);\s*\}'''

new_quarterly_js = '''function renderQuarterlyTabs() {
    const c = document.getElementById('quarterly-tabs');
    const periods = Object.keys(appData.quarterly_leaderboard).sort().reverse();
    currentQuarter = periods[0] || '';

    c.innerHTML = `
        <div class="time-picker">
            <button class="time-nav-btn" onclick="navigateQuarter(-1)" aria-label="上一季度">&#10094;</button>
            <div class="time-current" id="quarter-display">${currentQuarter}</div>
            <button class="time-nav-btn" onclick="navigateQuarter(1)" aria-label="下一季度">&#10095;</button>
            <div class="time-jump">
                <select class="time-jump-select" onchange="showQuarter(this.value)" aria-label="跳转到指定季度">
                    ${periods.map(p => `<option value="${p}" ${p===currentQuarter?'selected':''}>${p}</option>`).join('')}
                </select>
            </div>
        </div>`;
    renderQuarterlyLeaderboard();
}

        function showQuarter(q) {
            currentQuarter = q;
            const disp = document.getElementById('quarter-display');
            if (disp) disp.textContent = q;
            const sel = document.querySelector('#quarterly-tabs .time-jump select');
            if (sel) sel.value = q;
            renderQuarterlyLeaderboard();
        }

        function navigateQuarter(delta) {
            const periods = Object.keys(appData.quarterly_leaderboard).sort();
            const idx = periods.indexOf(currentQuarter);
            if (idx === -1) return;
            const revIdx = periods.length - 1 - idx;
            const newRevIdx = Math.max(0, Math.min(periods.length - 1, revIdx + delta));
            showQuarter(periods[periods.length - 1 - newRevIdx]);
        }'''

html = re.sub(old_quarterly_js, new_quarterly_js, html)

# ===== 4. Same for yearly =====
old_yearly_js = r'''function renderYearlyTabs\(\) \{\s*
            const c = document\.getElementById\('yearly-tabs'\);\s*
            const years = Object\.keys\(appData\.yearly_leaderboard\)\.sort\(\)\.reverse\(\);\s*
            currentYear = years\[0\] \|| '';\s*
            c\.innerHTML = '<div class="time-picker">' \+
                years\.map\(y => `<button class="time-chip \$\{y===currentYear\?'current':''\}" onclick="showYear\('\$y'\)">\$y</button>`\)\.join\(''\) \+
                '</div>';\s*
            renderYearlyLeaderboard\(\);\s*\}
        function showYear\(y\) \{
            currentYear = y;\s*
            document\.querySelectorAll\('#yearly-tabs \.time-chip'\)\.forEach\(t => \{
                t\.classList\.toggle\('current', t\.textContent\.trim\(\) === y\);\s*\}\);\s*
            renderYearlyLeaderboard\(\);\s*\}'''

new_yearly_js = '''function renderYearlyTabs() {
            const c = document.getElementById('yearly-tabs');
            const periods = Object.keys(appData.yearly_leaderboard).sort().reverse();
            currentYear = periods[0] || '';

            c.innerHTML = `
                <div class="time-picker">
                    <button class="time-nav-btn" onclick="navigateYear(-1)" aria-label="上一年">&#10094;</button>
                    <div class="time-current" id="year-display">${currentYear}</div>
                    <button class="time-nav-btn" onclick="navigateYear(1)" aria-label="下一年">&#10095;</button>
                    <div class="time-jump">
                        <select class="time-jump-select" onchange="showYear(this.value)" aria-label="跳转到指定年份">
                            ${periods.map(p => `<option value="${p}" ${p===currentYear?'selected':''}>${p}</option>`).join('')}
                        </select>
                    </div>
                </div>`;
            renderYearlyLeaderboard();
        }

        function showYear(y) {
            currentYear = y;
            const disp = document.getElementById('year-display');
            if (disp) disp.textContent = y;
            const sel = document.querySelector('#yearly-tabs .time-jump select');
            if (sel) sel.value = y;
            renderYearlyLeaderboard();
        }

        function navigateYear(delta) {
            const periods = Object.keys(appData.yearly_leaderboard).sort();
            const idx = periods.indexOf(currentYear);
            if (idx === -1) return;
            const revIdx = periods.length - 1 - idx;
            const newRevIdx = Math.max(0, Math.min(periods.length - 1, revIdx + delta));
            showYear(periods[periods.length - 1 - newRevIdx]);
        }'''

html = re.sub(old_yearly_js, new_yearly_js, html)

# Write back
with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Done! Replaced chip grid with elegant headline-style picker.")
