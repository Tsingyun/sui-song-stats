#!/usr/bin/env python3
"""Fix the JS after incomplete regex replacement - remove leftover old code, fix syntax."""

import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Extract <script>...</script> block
script_match = re.search(r'(<script>)([\s\S]*?)(</script>)', html)
if not script_match:
    print("ERROR: No script tag found!")
    exit(1)

script_open = script_match.group(1)
old_js = script_match.group(2)
script_close = script_match.group(3)

# ===== Strategy: Rebuild the JS cleanly =====
# Keep: const appData = {...};  (the data block)
# Replace everything after appData with clean function code

# Find end of appData data
appdata_end = re.search(r'^\};', old_js, re.MULTILINE)
if not appdata_end:
    print("ERROR: Could not find end of appData!")
    exit(1)

data_block = old_js[:appdata_end.end()]

# New clean JS functions (all properly formatted)
new_functions = r'''
        // Initialize on DOM ready
        document.addEventListener('DOMContentLoaded', function() {
            renderStats();
            renderTotalLeaderboard();
            renderMonthlyTabs();
            renderQuarterlyTabs();
            renderYearlyTabs();
            renderSongLeaderboard();
            renderAudienceGrid();
            renderTrendChart();
            setupScrollAnimations();
            setupNavScroll();
        });

        function renderStats() {
            const stats = [
                { num: appData.metadata.total_records, label: '总点歌记录' },
                { num: appData.metadata.unique_audiences, label: '位饼干岁' },
                { num: appData.metadata.unique_songs, label: '首歌曲' }
            ];
            document.getElementById('stats').innerHTML = stats.map(s => 
                `<div class="stat-card fade-in"><div class="stat-number">${s.num}</div><div class="stat-label">${s.label}</div></div>`
            ).join('');
        }

        // --- Total Leaderboard ---
        function renderTotalLeaderboard() {
            const c = document.getElementById('total-leaderboard');
            c.innerHTML = '<div>';
            (appData.total_leaderboard || []).slice(0, 20).forEach((item, i) => {
                c.innerHTML += `<div class="leaderboard-item fade-in ${i<3?'top-3':''}" style="transition-delay:${i*100}ms" onclick="showAudienceDetail('${item.audience}')"><div class="rank">${item.rank}</div><div class="leaderboard-name">${item.audience}</div><div class="leaderboard-count">${item.count} 次</div></div>`;
            });
            c.innerHTML += '</div>';
        }

        // --- Monthly Picker (headline style) ---
        let currentMonth = '';
        function renderMonthlyTabs() {
            const c = document.getElementById('monthly-tabs');
            const periods = Object.keys(appData.monthly_leaderboard).sort().reverse();
            currentMonth = periods[0] || '';

            c.innerHTML =
                '<div class="time-picker">' +
                    '<button class="time-nav-btn" onclick="navigateMonth(-1)" aria-label="上个月">&#10094;</button>' +
                    '<div class="time-current" id="month-display">' + currentMonth + '</div>' +
                    '<button class="time-nav-btn" onclick="navigateMonth(1)" aria-label="下个月">&#10095;</button>' +
                    '<div class="time-jump"><select class="time-jump-select" onchange="showMonth(this.value)" aria-label="跳转到月份">' +
                        periods.map(function(p){ return '<option value="' + p + '"' + (p===currentMonth ? ' selected' : '') + '>' + p + '</option>'; }).join('') +
                    '</select></div>' +
                '</div>';
            renderMonthlyLeaderboard();
        }

        function showMonth(m) {
            currentMonth = m;
            var disp = document.getElementById('month-display');
            if (disp) disp.textContent = m;
            var sel = document.querySelector('#monthly-tabs .time-jump select');
            if (sel) sel.value = m;
            renderMonthlyLeaderboard();
        }

        function navigateMonth(delta) {
            var periods = Object.keys(appData.monthly_leaderboard).sort();
            var idx = periods.indexOf(currentMonth);
            if (idx === -1) return;
            var revIdx = periods.length - 1 - idx;
            var newRevIdx = Math.max(0, Math.min(periods.length - 1, revIdx + delta));
            showMonth(periods[periods.length - 1 - newRevIdx]);
        }

        function renderMonthlyLeaderboard() {
            var c = document.getElementById('monthly-leaderboard');
            var d = appData.monthly_leaderboard[currentMonth] || [];
            c.innerHTML = d.map(function(item, i) {
                return '<div class="leaderboard-item fade-in" style="transition-delay:' + (i*100) + 'ms" onclick="showAudienceDetail(\'' + item.audience + '\')"><div class="rank">' + item.rank + '</div><div class="leaderboard-name">' + item.audience + '</div><div class="leaderboard-count">' + item.count + ' 次</div></div>';
            }).join('');
        }

        // --- Quarterly Picker ---
        let currentQuarter = '';
        function renderQuarterlyTabs() {
            const c = document.getElementById('quarterly-tabs');
            const periods = Object.keys(appData.quarterly_leaderboard).sort().reverse();
            currentQuarter = periods[0] || '';

            c.innerHTML =
                '<div class="time-picker">' +
                    '<button class="time-nav-btn" onclick="navigateQuarter(-1)" aria-label="上一季度">&#10094;</button>' +
                    '<div class="time-current" id="quarter-display">' + currentQuarter + '</div>' +
                    '<button class="time-nav-btn" onclick="navigateQuarter(1)" aria-label="下一季度">&#10095;</button>' +
                    '<div class="time-jump"><select class="time-jump-select" onchange="showQuarter(this.value)" aria-label="跳转到季度">' +
                        periods.map(function(p){ return '<option value="' + p + '"' + (p===currentQuarter ? ' selected' : '') + '>' + p + '</option>'; }).join('') +
                    '</select></div>' +
                '</div>';
            renderQuarterlyLeaderboard();
        }

        function showQuarter(q) {
            currentQuarter = q;
            var disp = document.getElementById('quarter-display');
            if (disp) disp.textContent = q;
            var sel = document.querySelector('#quarterly-tabs .time-jump select');
            if (sel) sel.value = q;
            renderQuarterlyLeaderboard();
        }

        function navigateQuarter(delta) {
            var periods = Object.keys(appData.quarterly_leaderboard).sort();
            var idx = periods.indexOf(currentQuarter);
            if (idx === -1) return;
            var revIdx = periods.length - 1 - idx;
            var newRevIdx = Math.max(0, Math.min(periods.length - 1, revIdx + delta));
            showQuarter(periods[periods.length - 1 - newRevIdx]);
        }

        function renderQuarterlyLeaderboard() {
            var c = document.getElementById('quarterly-leaderboard');
            var d = appData.quarterly_leaderboard[currentQuarter] || [];
            c.innerHTML = d.map(function(item, i) {
                return '<div class="leaderboard-item fade-in" style="transition-delay:' + (i*100) + 'ms" onclick="showAudienceDetail(\'' + item.audience + '\')"><div class="rank">' + item.rank + '</div><div class="leaderboard-name">' + item.audience + '</div><div class="leaderboard-count">' + item.count + ' 次</div></div>';
            }).join('');
        }

        // --- Yearly Picker ---
        let currentYear = '';
        function renderYearlyTabs() {
            const c = document.getElementById('yearly-tabs');
            const periods = Object.keys(appData.yearly_leaderboard).sort().reverse();
            currentYear = periods[0] || '';

            c.innerHTML =
                '<div class="time-picker">' +
                    '<button class="time-nav-btn" onclick="navigateYear(-1)" aria-label="上一年">&#10094;</button>' +
                    '<div class="time-current" id="year-display">' + currentYear + '</div>' +
                    '<button class="time-nav-btn" onclick="navigateYear(1)" aria-label="下一年">&#10095;</button>' +
                    '<div class="time-jump"><select class="time-jump-select" onchange="showYear(this.value)" aria-label="跳转到年份">' +
                        periods.map(function(p){ return '<option value="' + p + '"' + (p===currentYear ? ' selected' : '') + '>' + p + '</option>'; }).join('') +
                    '</select></div>' +
                '</div>';
            renderYearlyLeaderboard();
        }

        function showYear(y) {
            currentYear = y;
            var disp = document.getElementById('year-display');
            if (disp) disp.textContent = y;
            var sel = document.querySelector('#yearly-tabs .time-jump select');
            if (sel) sel.value = y;
            renderYearlyLeaderboard();
        }

        function navigateYear(delta) {
            var periods = Object.keys(appData.yearly_leaderboard).sort();
            var idx = periods.indexOf(currentYear);
            if (idx === -1) return;
            var revIdx = periods.length - 1 - idx;
            var newRevIdx = Math.max(0, Math.min(periods.length - 1, revIdx + delta));
            showYear(periods[periods.length - 1 - newRevIdx]);
        }

        function renderYearlyLeaderboard() {
            var c = document.getElementById('yearly-leaderboard');
            var d = appData.yearly_leaderboard[currentYear] || [];
            c.innerHTML = d.map(function(item, i) {
                return '<div class="leaderboard-item fade-in" style="transition-delay:' + (i*100) + 'ms" onclick="showAudienceDetail(\'' + item.audience + '\')"><div class="rank">' + item.rank + '</div><div class="leaderboard-name">' + item.audience + '</div><div class="leaderboard-count">' + item.count + ' 次</div></div>';
            }).join('');
        }

        // --- Songs ---
        function renderSongLeaderboard() {
            const c = document.getElementById('song-leaderboard');
            c.innerHTML = (appData.song_leaderboard || []).slice(0, 20).map(function(item, i) {
                return '<div class="leaderboard-item fade-in" style="transition-delay:' + (i*100) + 'ms"><div class="rank">' + item.rank + '</div><div class="leaderboard-name">' + item.song + '</div><div class="leaderboard-count">' + item.count + ' 次</div></div>';
            }).join('');
        }

        // --- Audience Grid ---
        function renderAudienceGrid() {
            const top = (appData.total_leaderboard || []).slice(0, 9);
            const grid = document.getElementById('audience-grid');
            grid.innerHTML = top.map(function(aud, i) {
                var detail = appData.audience_details[aud.audience] || {};
                var songs = Object.entries(detail).filter(function(kv){ return typeof kv[1]==='object'; })
                    .sort(function(a,b){ return b[1].count - a[1].count; }).slice(0,5);
                return '<div class="audience-card fade-in" style="transition-delay:' + (i*80) + 'ms" onclick="showAudienceDetail(\'' + aud.audience + '\')">' +
                    '<div class="audience-name">' + aud.audience + ' <span class="song-count">' + aud.count + '首</span></div>' +
                    songs.map(function(s){ return '<div class="audience-song">' + s[0] + ' <span class="song-count">' + s[1].count + '次</span></div>'; }).join('') +
                    '</div>';
            }).join('');
        }

        // --- Trend Chart ---
        function renderTrendChart() {
            const trends = appData.trends || {};
            const months = Object.keys(trends).sort();
            const maxVal = Math.max.apply(null, months.map(function(m){return trends[m];}));
            var html = '';
            months.forEach(function(m){
                var pct = (trends[m]/maxVal)*100;
                html += '<div class="chart-bar-item"><div class="chart-label">'+m+'</div><div class="chart-bar-bg"><div class="chart-bar-fill accent" style="width:'+pct+'%"></div></div><div class="chart-value">'+trends[m]+'</div></div>';
            });
            document.getElementById('trend-chart').innerHTML = html;
            setTimeout(function(){
                document.querySelectorAll('#trend-chart .chart-bar-fill').forEach(function(el){ el.style.width=el.style.width; });
            }, 300);
        }

        // --- Modal ---
        window.showAudienceDetail = function(name) {
            var detail = appData.audience_details[name];
            if (!detail) return;
            var songs = Object.entries(detail).filter(function(kv){ return typeof kv[1]==='object'; })
                .sort(function(a,b){ return b[1].count - a[1].count; });
            var totalSongs = songs.reduce(function(sum,s){ return sum+s[1].count;},0);
            var modal = document.getElementById('audience-modal');
            document.getElementById('modal-title').textContent = name;
            document.getElementById('modal-subtitle').textContent = totalSongs + ' 首歌曲';
            document.getElementById('modal-song-list').innerHTML = songs.map(function(s){
                return '<div class="modal-song-item"><div class="modal-song-name">'+s[0]+'<span class="song-count">x'+s[1].count+'</span></div><div class="modal-song-date">'+s[1].dates.join(', ')+'</div></div>';
            }).join('');
            modal.classList.add('active');
        };
        window.closeModal = function(){ document.getElementById('audience-modal').classList.remove('active'); };
        document.addEventListener('keydown',function(e){ if(e.key==='Escape') closeModal(); });

        // --- Scroll Animations & Nav ---
        function setupScrollAnimations() {
            var observer = new IntersectionObserver(function(entries){
                entries.forEach(function(entry){ if(entry.isIntersecting) entry.target.classList.add('visible'); });
            },{ threshold: 0.1 });
            document.querySelectorAll('.fade-in').forEach(function(el){ observer.observe(el); });
        }

        function setupNavScroll() {
            var nav = document.getElementById('nav');
            var heroHeight = document.getElementById('hero').offsetHeight;
            window.addEventListener('scroll', function(){
                nav.classList.toggle('visible', window.scrollY > heroHeight * 0.6);
            });
        }'''

new_js = data_block + new_functions

new_html = html[:script_match.start(2)] + new_js + html[script_match.end(2):]

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(new_html)

# Validate JS
import subprocess
result = subprocess.run(
    ['C:/Users/Tsing/.workbuddy/binaries/node/versions/22.22.2/node.exe',
     '-e',
     "const fs=require('fs');const h=fs.readFileSync('index.html','utf8');"
     "const m=h.match(/<script>([\\s\\S]*?)<\\/script>/);"
     "if(m){try{new Function(m[1]);console.log('JS OK')}catch(e){console.log('JS ERROR:',e.message)}}"],
    capture_output=True, text=True
)
print(result.stdout.strip())
if result.stderr.strip():
    print('STDERR:', result.stderr.strip())
