# 岁己 SUI · 点歌统计

虚拟主播**岁己SUI**的点歌数据可视化网站，以 **Endfield** 美学风格展示自 2024 年 6 月以来的全部点歌记录。

## 访问地址

在线版：[https://stats.suijisui.uk](https://stats.suijisui.uk)

本地使用：双击 `index.html` 即可在浏览器中打开。

## 数据概览

基于岁己SUI自 **2024年6月** 至今的全部点歌记录，共 **819 条记录、81 位观众、499 首歌曲**。

## 设计系统

网站采用 **Endfield** 美学风格（参考 [endfield.hypergryph.com](https://endfield.hypergryph.com/)），以 ark-ui 设计语言为框架：

| 元素 | 规格 |
|------|------|
| 标题字体 | Jost（宽体几何，匹配 Novecento Sans Wide） |
| 技术字体 | Space Grotesk（UI）+ IBM Plex Mono（数据/标签） |
| 中文字体 | Noto Sans SC |
| 背景色 | `#191919` 墨黑 / `#131313` 深墨，深色主导 |
| 强调色 | `#fffa00` 信号黄，仅用于激活态/进度/皇冠/角括号 |
| 状态色 | `#00ffa2` 验证绿，用于 Lv.4 徽章 |
| 文字层级 | `rgba(255,255,255,1 / .85 / .55 / .4)` 四级 |
| 动画时长 | 240ms（交互）/ 650ms（显现）/ 1.8s（脉冲） |
| 圆角 | 0-2px，直角为主 |
| 装饰元素 | 校准圆环、角括号、斜条纹底纹、黄色装饰线 |

设计 token 定义在 `:root` CSS 变量中，通过 `data-ark-theme="endfield"` 和 `data-ark-depth="complex"` 控制。

## 观众等级系统

| 等级 | 条件 | 徽章样式 |
|------|------|---------|
| Lv.1 | 1 - 10 次 | 暗灰边框 + 暗灰文字 |
| Lv.2 | 11 - 30 次 | 灰边框 + 灰文字 |
| Lv.3 | 31 - 60 次 | 亮白边框 + 亮白文字 |
| Lv.4 | 61 - 100 次 | 验证绿边框 + 绿文字 |
| Lv.5 | 100+ 次 | 信号黄填充 + 墨黑文字 |

## 功能一览

### 排行榜
- **月度点歌榜** — 25 个月份可切换，左右箭头 + 下拉菜单
- **季度点歌榜** — 按季度统计
- **年度点歌榜** — 2024 / 2025 / 2026
- **总点歌榜** — 所有时间累计排行（含等级徽章）
- **热门歌曲榜** — 被点次数最多的歌曲排行

### 数据可视化
- **点歌趋势** — 柱状图展示每月点歌活跃度
- **观众喜好分析** — TOP 12 观众的偏好歌曲

### 创意功能
- **Hero 校准仪器** — 深色开场 + 三层校准圆环 + //SUI-STAT 品牌宣言 + 黄色进度时间线
- **数字动画** — 进入页面时统计数字从 0 滚动到真实数值
- **观众等级系统** — Lv.1 ~ Lv.5 五级徽章，统一设计亮度递进
- **成就殿堂** — 点歌之王成就卡片 + 彩纸庆祝动画
- **跨月冠军追踪** — 连续多月霸榜记录
- **观众相似度** — 点击观众可见品味最相近的 3 人及重叠歌曲数
- **全局搜索** — 顶栏搜索图标，支持搜索歌曲 / 观众 / 日期
- **彩蛋** — 搜索"谁是点歌大王？"触发庆祝动画
- **B站主页直跳** — 已知 UID 一键跳转 B站个人空间
- **月度连续点歌** — 当月连续点歌的用户标记 🔥
- **一键复制** — 复制观众名、上次点歌日期、本月点歌数
- **时间范围筛选** — 自定义起止日期查看区间内统计
- **导出功能** — 每个榜单支持导出 PNG 高清截图、XLSX、CSV、JSON

### 交互细节
- 左侧固定导航栏（移动端转底部滚动条），滚动时高亮当前区段
- 榜单默认显示前 10 名，点击「展开全部」查看完整排名
- 点击观众/歌曲名字弹出详情面板（四角黄色角括号装饰）
- 观众详情显示「上一次点到歌距今 X 天」及「品味相近」
- 黄色皇冠标识每个观众榜单的冠军（歌曲榜不加皇冠）
- 信号黄仅用于激活态、进度条、皇冠、角括号——不用作正文 hover

## 技术栈

- 纯静态 HTML + CSS + JavaScript，无构建工具
- 数据以 JSON 格式内嵌到 HTML 中，双击即可运行
- 数据处理使用 Python（openpyxl 读取 Excel、pypinyin 拼音、difflib 模糊匹配）
- 截图导出依赖 html2canvas（CDN）
- 数据导出依赖 SheetJS（CDN）
- 部署于 GitHub Pages

## 项目结构

```
.
├── index.html                 # 主网站（自包含，双击运行）
├── template.html              # HTML 模板（含 {{APPDATA}} 占位符）
├── build_html.py              # 构建脚本：模板 + JSON → index.html
├── song_data_processed.json   # 唯一数据源（raw_data + metadata + 衍生数据）
├── changelog.html             # 更新日志页
├── README.md                  # 项目说明
├── tools/
│   ├── process_features.py    # 数据处理主脚本（重算所有 Feature + metadata）
│   ├── match_name.py          # 录入前 OCR 候选名模糊匹配工具
│   ├── audience_master.txt    # 标准观众名清单（81人）
│   ├── song_master.txt        # 标准歌名清单（499首）
│   └── rename_user.py         # 用户更名工具
└── .gitignore
```

## 本地开发

```bash
# 修改 template.html 后重建
python build_html.py

# 启动本地服务器测试
python -m http.server 8899
# 访问 http://localhost:8899/index.html

# 提交到 GitHub
git add template.html index.html changelog.html
git commit -m "..."
git push
```

## 数据维护

数据更新流程：
1. 获取新的点歌记录截图
2. OCR 识别后，先用 `tools/match_name.py` 匹配资料库标准名（避免错字造新名）
3. 追加到 `song_data_processed.json` 的 `raw_data` 数组中
4. 运行 `python tools/process_features.py` 重新计算所有榜单和衍生数据
5. 运行 `python build_html.py` 重建 `index.html`
6. 提交并推送到 GitHub
