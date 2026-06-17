import re

with open('template.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Remove network section HTML
html = html.replace('''
    <!-- Feature 2: Song Relationship Network -->
    <section class="section" id="network">
        <div class="container">
            <span class="section-label">Network</span>
            <h2 class="section-title">歌曲关系网络</h2>
            <div class="network-container" id="network-container">
                <canvas id="network-canvas"></canvas>
            </div>
            <div class="network-legend">节点大小 = 点歌次数 · 连线 = 被同一位观众点过</div>
        </div>
    </section>

''', '\n')

# 2. Remove network nav link
html = html.replace('''
                <li><a href="#network" class="nav-link">网络</a></li>''', '')

# 3. Remove network CSS
old_net_css = '''        /* Feature 2: Song Network */
        .network-container { position: relative; width: 100%; height: 450px; background: var(--bg); border-radius: var(--radius); overflow: hidden; }
        .network-container canvas { display: block; }
        .network-legend { text-align: center; margin-top: 0.5rem; font-size: 0.7rem; color: var(--muted-fg); letter-spacing: 0.1em; text-transform: uppercase; }'''
html = html.replace(old_net_css, '')

# 4. Remove network JS
old_net_js = '''
        // ==== Feature 2: Song Network ====
        function renderNetwork() {'''
# find from renderNetwork to next function
start = html.find('        // ==== Feature 2: Song Network ====')
end = html.find('        // ==== Feature 5: Achievements ====', start)
if start >= 0 and end > start:
    html = html[:start] + html[end:]

# 5. Remove renderNetwork call from initApp
html = html.replace('''            setTimeout(function() { renderNetwork(); }, 500);
''', '')

# 6. Fix section alternation: trend→dark, achievements→dark
html = html.replace('''    <section class="section" id="trend">
        <div class="container">
            <span class="section-label">Trend Chart</span>
            <h2 class="section-title">点歌趋势</h2>''', '''    <section class="section-dark" id="trend">
        <div class="container">
            <span class="section-label">Trend Chart</span>
            <h2 class="section-title">点歌趋势</h2>''')

html = html.replace('''    <section class="section" id="achievements">
        <div class="container">
            <span class="section-label">Achievements</span>
            <h2 class="section-title">成就殿堂</h2>''', '''    <section class="section-dark" id="achievements">
        <div class="container">
            <span class="section-label">Achievements</span>
            <h2 class="section-title">成就殿堂</h2>''')

# 7. Fallthrough: ensure alternating is now correct
# Hero(hero) → Monthly(light) → Quarterly(dark) → Yearly(light) → Total(dark) 
# → Songs(light) → Audiences(dark) → Trend(dark) ... PROBLEM!
# Trend is now dark, but Audiences is also dark. Need to fix.

# Trend needs to be light if Audiences is dark
html = html.replace('''    <section class="section-dark" id="trend">
        <div class="container">
            <span class="section-label">Trend Chart</span>
            <h2 class="section-title">点歌趋势</h2>''', '''    <section class="section" id="trend">
        <div class="container">
            <span class="section-label">Trend Chart</span>
            <h2 class="section-title">点歌趋势</h2>''')

# But wait - let me recalculate:
# Hero(hero) → Monthly(light) → Quarterly(dark) → Yearly(light) → Total(dark) 
# → Songs(light) → Audiences(dark) → Trend(light?) → Heatmap(light?) → Achievements(dark?)
# Trend and Heatmap would both be light. That's the original problem.
# 
# Better approach: make Trend dark, Heatmap light, Achievements dark
# Hero(hero) → Monthly(light) → Quarterly(dark) → Yearly(light) → Total(dark) 
# → Songs(light) → Audiences(dark) → Trend(dark) → Heatmap(light) → Achievements(dark)
#
# Hmm, Audiences(dark) then Trend(dark) is also back-to-back dark. 
# Let me flip the issue differently:
# The issue was: Trend(light) → Heatmap(light) → Achievements(light) all light
# 
# Better alternation:
# Hero(hero) → Monthly(light) → Quarterly(dark) → Yearly(light) → Total(dark) 
# → Songs(light) → Audiences(dark) → Trend(light) would be wrong (Audiences dark → Trend light = ok!)
# → Heatmap(dark) → Achievements(light)
#
# Actually: Audiences(dark) → Trend(light) → Heatmap(dark) → Achievements(light) = perfect!
# 
# So: Trend stays light, Heatmap becomes dark, Achievements stays light!

# Undo my previous change (trend stays light)
html = html.replace('''    <section class="section-dark" id="trend">
        <div class="container">
            <span class="section-label">Trend Chart</span>
            <h2 class="section-title">点歌趋势</h2>''', '''    <section class="section" id="trend">
        <div class="container">
            <span class="section-label">Trend Chart</span>
            <h2 class="section-title">点歌趋势</h2>''')

# Make heatmap dark
html = html.replace('''    <section class="section" id="heatmap">
        <div class="container">
            <span class="section-label">Heatmap</span>
            <h2 class="section-title">日历热图</h2>''', '''    <section class="section-dark" id="heatmap">
        <div class="container">
            <span class="section-label">Heatmap</span>
            <h2 class="section-title">日历热图</h2>''')

# Undo achievements dark, keep light
html = html.replace('''    <section class="section-dark" id="achievements">
        <div class="container">
            <span class="section-label">Achievements</span>
            <h2 class="section-title">成就殿堂</h2>''', '''    <section class="section" id="achievements">
        <div class="container">
            <span class="section-label">Achievements</span>
            <h2 class="section-title">成就殿堂</h2>''')

# Final alternation check:
# Hero(hero) → Monthly(light) → Quarterly(dark) → Yearly(light) → Total(dark) 
# → Songs(light) → Audiences(dark) → Trend(light) → Heatmap(dark) → Achievements(light)
# ✓ Perfect alternating!

# 8. Fix heatmap legend colors for dark background
html = html.replace(
    '.heatmap-legend { display: flex; align-items: center; justify-content: center; gap: 0.5rem; margin-top: 0.5rem; font-size: 0.7rem; letter-spacing: 0.1em; text-transform: uppercase; color: var(--muted-fg); }',
    '.heatmap-legend { display: flex; align-items: center; justify-content: center; gap: 0.5rem; margin-top: 0.5rem; font-size: 0.7rem; letter-spacing: 0.1em; text-transform: uppercase; color: var(--bg); opacity: 0.7; }'
)

# Fix heatmap month labels for dark bg
html = html.replace(
    '.heatmap-months { display: flex; margin: 0 0.25rem 0.5rem; font-size: 0.6rem; letter-spacing: 0.1em; text-transform: uppercase; color: var(--muted-fg); overflow: hidden; white-space: nowrap; }',
    '.heatmap-months { display: flex; margin: 0 0.25rem 0.5rem; font-size: 0.6rem; letter-spacing: 0.1em; text-transform: uppercase; color: var(--bg); opacity: 0.6; overflow: hidden; white-space: nowrap; }'
)

# Fix l0 cell for dark bg (empty cells should be dark-translucent)
html = html.replace(
    '.heatmap-cell.l0 { background: var(--bg); border: 1px solid var(--accent-dim); }',
    '.heatmap-cell.l0 { background: rgba(249,248,246,0.08); border: 1px solid rgba(212,175,55,0.15); }'
)

with open('template.html', 'w', encoding='utf-8') as f:
    f.write(html)

print('All changes applied: network removed, section alternation fixed')
