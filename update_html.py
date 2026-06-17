#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
更新HTML文件，添加年度排行榜并修复排序问题
"""

import json

# 读取数据
with open('song_data_processed.json', 'r', encoding='utf-8') as f:
    app_data = json.load(f)

# 读取原始HTML模板
with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. 修复趋势图排序问题（第386行）- 将 .sort() 改为 .sort().reverse()
html = html.replace(
    'const months = Object.keys(trends).sort(), maxCount = Math.max(...Object.values(trends));',
    'const months = Object.keys(trends).sort().reverse(), maxCount = Math.max(...Object.values(trends));'
)

# 2. 在季度排行榜部分之后添加年度排行榜部分
# 找到季度排行榜的结束位置（观众的喜好分析部分之前）
yearly_section = '''
        </div>
    </section>

    <!-- 年度排行榜 -->
    <section id="yearly" style="padding: 8rem 0;">
        <div class="container">
            <div class="vertical-label">YEARLY · 年度排行</div>
            <div class="overline" style="margin-bottom: 1rem;">LEADERBOARD</div>
            <h2 class="section-title" style="margin-bottom: 3rem;">年度排行榜</h2>
            <div class="tabs" id="yearly-tabs" style="margin-bottom: 3rem;"></div>
            <div class="leaderboard" id="yearly-leaderboard"></div>
        </div>
    </section>
'''

# 在季度排行榜section结束后插入年度排行榜
html = html.replace(
    '</div>\n    </section>\n\n    <!-- 观众喜好分析 -->',
    '</div>\n    </section>' + yearly_section + '\n    <!-- 观众喜好分析 -->'
)

# 3. 添加年度排行榜的JavaScript函数
# 在 renderQuarterlyLeaderboard 函数之后添加
yearly_js = '''
        function renderYearlyTabs() {
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
        }
        function renderYearlyLeaderboard() {
            const c = document.getElementById('yearly-leaderboard'), d = appData.yearly_leaderboard[currentYear] || [];
            c.innerHTML = d.map((item,i) => `<div class="leaderboard-item fade-in" style="transition-delay:${i*100}ms" onclick="showAudienceDetail('${item.audience}')"><div class="rank">${item.rank}</div><div class="leaderboard-name">${item.audience}</div><div class="leaderboard-count">${item.count} 次</div></div>`).join('');
        }
'''

# 在 renderQuarterlyLeaderboard 函数之后插入
html = html.replace(
    'function renderSongLeaderboard() {',
    yearly_js + '\n        function renderSongLeaderboard() {'
)

# 4. 在初始化部分添加年度排行榜的调用
# 找到 renderQuarterlyTabs 调用之后
html = html.replace(
    'renderQuarterlyTabs();',
    'renderQuarterlyTabs();\n        renderYearlyTabs();'
)

# 5. 添加 currentYear 变量定义
html = html.replace(
    "let currentMonth = null, currentQuarter = null;",
    "let currentMonth = null, currentQuarter = null, currentYear = null;"
)

# 6. 将数据内嵌到HTML中（替换旧的fetch部分）
# 找到数据加载的部分并替换
data_str = json.dumps(app_data, ensure_ascii=False)

# 找到 "// ========== DATA LOADING ==========" 部分并替换
start_marker = "// ========== DATA LOADING =========="
end_marker = "// ========== APP INIT =========="

start_idx = html.find(start_marker)
end_idx = html.find(end_marker)

if start_idx != -1 and end_idx != -1:
    new_data_section = f"""// ========== DATA LOADING ==========
        const appData = {data_str};
        // Process raw data for audience details
        const rawData = {{}};
        appData.raw_data.forEach(record => {{
            if (!rawData[record.audience]) rawData[record.audience] = [];
            rawData[record.audience].push({{ song: record.song, date: record.date }});
        }});
        for (const a in rawData) rawData[a].sort((a, b) => b.date.localeCompare(a.date));

"""
    html = html[:start_idx] + new_data_section + html[end_idx:]

# 保存更新后的HTML
with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("✅ HTML文件更新完成！")
print("  - 已修复趋势图排序问题（改为倒序）")
print("  - 已添加年度排行榜部分")
print("  - 已将最新数据内嵌到HTML中")
