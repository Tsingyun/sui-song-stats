#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
match_name.py — 录入前先匹配资料库

岁己点歌统计录入时，OCR 容易把观众名/歌名识别错字（如「昕宝」→「所宝」、
日文歌名整段识别错）。本工具在写入新记录之前，先把 OCR 得到的候选名
和 song_data_processed.json 里已有的标准名做模糊匹配，返回最可能的
已有标准写法，避免重复造名 / 误判新观众新歌。

用法：
  # 单条候选
  python match_name.py --type audience "所宝yoake-"
  python match_name.py --type song "才二十三"

  # 批量（从命令行一次传多个）
  python match_name.py --type audience "所宝yoake-" "earth今天仍在迷路"

  # 批量（从 stdin，每行一个候选）
  cat ocr_names.txt | python match_name.py --type audience

  # 打印全部标准名单（带出现次数），用于人工对照
  python match_name.py --type audience --list
  python match_name.py --type song --list

  # 重新生成 master 名单文本文件（audience_master.txt / song_master.txt）
  python match_name.py --rebuild

匹配策略（按顺序，命中即提示）：
  1. 精确相等
  2. 归一化后相等（去空格/标点/全半角/大小写）
  3. 包含关系（候选⊂标准 或 标准⊂候选）
  4. difflib 模糊相似度 Top-K（ratio >= 阈值才报）
"""
import json
import re
import sys
import argparse
import difflib
import os

HERE = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(HERE, "..", "song_data_processed.json")
AUD_MASTER = os.path.join(HERE, "audience_master.txt")
SONG_MASTER = os.path.join(HERE, "song_master.txt")

PUNCT = re.compile(r"[\s\-_－—。、，,．.・·!'\"()（）\[\]【】/\\|]")


def norm(s: str) -> str:
    """归一化：去标点/空白/全半角差异，转小写。"""
    s = s.strip()
    s = PUNCT.sub("", s)
    s = s.replace("（", "(").replace("）", ")")
    return s.lower()


def load_data():
    with open(DATA_PATH, encoding="utf-8") as f:
        return json.load(f)


def build_master(data, key):
    """返回 [(name, count), ...] 按出现次数降序。"""
    from collections import Counter
    c = Counter(e[key] for e in data["raw_data"])
    return c.most_common()


def match_one(candidate, master_names, threshold=0.6):
    """对单条候选，返回 (best_name_or_None, reason, top3_list)。"""
    cand = candidate.strip()
    if not cand:
        return None, "empty", []
    # 1. 精确
    if cand in master_names:
        return cand, "exact", [(cand, 1.0)]
    # 2. 归一化
    nc = norm(cand)
    for n in master_names:
        if norm(n) == nc:
            return n, "normalized", [(n, 1.0)]
    # 3. 包含关系
    contain = []
    for n in master_names:
        nn = norm(n)
        if nn and (nn in nc or nc in nn):
            # 相似度用包含比例近似
            ratio = len(min(nn, nc, key=len)) / len(max(nn, nc, key=len))
            contain.append((n, ratio))
    if contain:
        contain.sort(key=lambda x: -x[1])
        return contain[0][0], "contains", contain[:3]
    # 4. 模糊
    sims = []
    for n in master_names:
        r = difflib.SequenceMatcher(None, nc, norm(n)).ratio()
        if r >= threshold:
            sims.append((n, r))
    sims.sort(key=lambda x: -x[1])
    if sims:
        return sims[0][0], "fuzzy", sims[:3]
    return None, "no-match", []


def render(candidate, res):
    best, reason, top3 = res
    print(f"\n候选: {candidate!r}")
    if best is None:
        print(f"  → 资料库中无相似项（视为真正的新名，请确认）")
        return
    tag = {"exact": "✓ 精确匹配", "normalized": "✓ 归一化匹配",
           "contains": "≈ 包含关系", "fuzzy": "≈ 模糊相似"}[reason]
    print(f"  → {tag} => 标准名: {best!r}")
    if len(top3) > 1:
        print("    候选对比:")
        for n, r in top3:
            print(f"      {r:.2f}  {n}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--type", choices=["audience", "song"], required=False,
                    help="匹配类型：audience=观众名, song=歌名")
    ap.add_argument("--list", action="store_true", help="打印全部标准名单")
    ap.add_argument("--rebuild", action="store_true", help="重新生成 master 文本文件")
    ap.add_argument("candidates", nargs="*", help="待匹配候选名（可多个）")
    args = ap.parse_args()

    data = load_data()
    if args.rebuild:
        for key, path in (("audience", AUD_MASTER), ("song", SONG_MASTER)):
            master = build_master(data, key)
            with open(path, "w", encoding="utf-8") as f:
                for name, cnt in master:
                    f.write(f"{cnt}\t{name}\n")
            print(f"rebuilt {path}: {len(master)} entries")
        return

    if args.type is None:
        ap.error("--type audience|song required (unless --rebuild)")

    key = "audience" if args.type == "audience" else "song"
    master = build_master(data, key)
    master_names = [n for n, _ in master]

    if args.list:
        for name, cnt in master:
            print(f"{cnt}\t{name}")
        return

    cands = list(args.candidates)
    if not cands and not sys.stdin.isatty():
        cands = [l.strip() for l in sys.stdin if l.strip()]

    if not cands:
        ap.error("no candidates given (pass args or pipe via stdin)")

    for c in cands:
        render(c, match_one(c, master_names))


if __name__ == "__main__":
    main()
