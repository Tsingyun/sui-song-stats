// Logic-level test for the new esc() + delegated click router.
// No jsdom available, so we extract the REAL source out of index.html and drive it
// with a minimal fake DOM. If the router mis-routes, the whole site's clicks die.
const fs = require('fs');
const path = require('path');
const html = fs.readFileSync(path.join(__dirname, '..', 'index.html'), 'utf8');

function balanced(src, from) {
  const i = src.indexOf('{', from);
  let d = 0;
  for (let k = i; k < src.length; k++) {
    if (src[k] === '{') d++;
    else if (src[k] === '}') { d--; if (d === 0) return src.slice(i, k + 1); }
  }
  return null;
}

const escStart = html.indexOf('function esc(s) {');
const escSrc = 'function esc(s) ' + balanced(html, escStart);
const delStart = html.indexOf("document.addEventListener('click', function(e) {");
const delSrc = 'var __handler = function(e) ' + balanced(html, delStart);

// ---- fake DOM ----
function parseSel(sel) {
  const m = /^([a-z]*)(?:\[([a-zA-Z-]+)(?:="([^"]*)")?\])?$/.exec(sel);
  if (!m) throw new Error('unsupported selector in test: ' + sel);
  return { tag: m[1] || null, attr: m[2] || null, val: m[3] === undefined ? null : m[3] };
}
class El {
  constructor(attrs, parent, tag) { this.attrs = attrs; this.parent = parent; this.tag = tag || 'div'; }
  getAttribute(k) { return k in this.attrs ? this.attrs[k] : null; }
  closest(sel) {
    const s = parseSel(sel);
    let n = this;
    while (n) {
      const tagOk = !s.tag || n.tag === s.tag;
      const attrOk = !s.attr || (s.attr in n.attrs && (s.val === null || n.attrs[s.attr] === s.val));
      if (tagOk && attrOk) return n;
      n = n.parent;
    }
    return null;
  }
}

const calls = [];
const rec = (n) => (...a) => calls.push([n, ...a]);
const sandbox = {
  document: { addEventListener: (t, fn) => { sandbox.__registered = fn; } },
  showDetail: rec('showDetail'),
  showSongDetail: rec('showSongDetail'),
  toggleExpand: rec('toggleExpand'),
  copyUserInfo: rec('copyUserInfo'),
  closeTimeFilterDirect: rec('closeTimeFilterDirect'),
  showStreakTooltipInner: rec('showStreakTooltipInner'),
  console,
};
sandbox.window = sandbox;

const fn = new Function('document', 'showDetail', 'showSongDetail', 'toggleExpand',
  'copyUserInfo', 'closeTimeFilterDirect', 'showStreakTooltipInner', 'console',
  escSrc + '\n' + delSrc + '\nreturn { esc: esc, handler: __handler };');
const api = fn(sandbox.document, sandbox.showDetail, sandbox.showSongDetail, sandbox.toggleExpand,
  sandbox.copyUserInfo, sandbox.closeTimeFilterDirect, sandbox.showStreakTooltipInner, console);

let pass = 0, fail = 0;
function ok(cond, msg) { if (cond) { pass++; console.log('  PASS ' + msg); } else { fail++; console.log('  FAIL ' + msg); } }

console.log('=== esc() ===');
ok(api.esc("Don't Look Back In Anger") === 'Don&#39;t Look Back In Anger', "单引号转义");
ok(api.esc('<img src=x onerror=alert(1)>') === '&lt;img src=x onerror=alert(1)&gt;', '< > 转义（XSS 防护）');
ok(api.esc('A & B "q"') === 'A &amp; B &quot;q&quot;', '& 与双引号转义');
ok(api.esc(null) === '' && api.esc(undefined) === '', 'null/undefined 安全');
ok(api.esc(123) === '123', '数字安全');

console.log('\n=== 委托路由 ===');
const handler = api.handler;
function click(el) { calls.length = 0; handler({ target: el, preventDefault(){}, stopPropagation(){} }); }

// 1. audience row
click(new El({ 'data-aud': 'Vaserkia' }, null));
ok(calls.length === 1 && calls[0][0] === 'showDetail' && calls[0][1] === 'Vaserkia', 'data-aud -> showDetail(名字)');

// 2. song row (含危险字符的名字必须原样还原)
click(new El({ 'data-song': "Don't Look Back In Anger" }, null));
ok(calls.length === 1 && calls[0][0] === 'showSongDetail' && calls[0][1] === "Don't Look Back In Anger", 'data-song -> showSongDetail（含单引号名原样）');

// 3. expand
click(new El({ 'data-act': 'expand', 'data-target': 'songs-leaderboard' }, null));
ok(calls[0][0] === 'toggleExpand' && calls[0][1] === 'songs-leaderboard', 'data-act=expand -> toggleExpand');

// 4. copy
click(new El({ 'data-act': 'copy', 'data-name': '仙布着急唱灭歌' }, null));
ok(calls[0][0] === 'copyUserInfo' && calls[0][2] === '仙布着急唱灭歌', 'data-act=copy -> copyUserInfo');

// 5. nested: streak badge inside a clickable row must win
const row = new El({ 'data-aud': 'Vaserkia' }, null);
const badge = new El({ 'data-act': 'streak', 'data-streak': JSON.stringify({ chain: ['2026-09-01'], songs: [['A']], length: 2 }) }, row);
click(badge);
ok(calls.length === 1 && calls[0][0] === 'showStreakTooltipInner', '嵌套：🔥徽章优先于所在行（不误触发详情）');
ok(calls[0][2] && calls[0][2].chain[0] === '2026-09-01', '  └ streak 对象从 data 属性正确还原');

// 6. time-filter row: close then detail
click(new El({ 'data-aud': '阿一古a1g', 'data-close-tf': '1' }, null));
ok(calls.length === 2 && calls[0][0] === 'closeTimeFilterDirect' && calls[1][0] === 'showDetail', '时间筛选行：先关闭弹层再开详情');

// 7. 无 data 属性 -> 不应有任何调用
click(new El({}, null));
ok(calls.length === 0, '无 data 属性的点击不触发任何动作');

console.log('\n=== 构建产物静态检查 ===');
ok(!/onclick="[^"]*showDetail\(/.test(html), '无残留 onclick="showDetail(...)"');
ok(!/onclick="[^"]*showSongDetail\(/.test(html), '无残留 onclick="showSongDetail(...)"');
ok(!/onclick="[^"]*toggleExpand\(/.test(html), '无残留 onclick="toggleExpand(...)"');
ok(/var step = rows\.length > 24 \? 0 : 60;/.test(html), '大列表取消了逐行延时（step=0）');
ok(/buildSearchIndex/.test(html) && /_searchTimer/.test(html), '搜索索引与防抖已接入');
ok(/requestIdleCallback/.test(html), '首屏之外渲染已延后');
// Only a real <script src=...> tag blocks first paint; the URL now lives in a
// constant for on-demand loading, so match the tag, not the string.
const blockingLibs = /<script[^>]+(?:html2canvas|xlsx)[^>]*>/i.test(html);
ok(!blockingLibs, '两个导出库不再随首屏同步加载（无阻塞 <script> 标签）');
ok(/function loadLib\(/.test(html) && /LIB_H2C/.test(html) && /LIB_XLSX/.test(html), '导出库改为按需加载（loadLib）');

console.log(`\n结果：${pass} 通过 / ${fail} 失败`);
process.exit(fail ? 1 : 0);
