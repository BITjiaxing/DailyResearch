#!/usr/bin/env python3
"""
DailyResearch - 科研热点追踪辅助工具
生成结构化搜索提示词，管理报告和日志。
实际的 Web 搜索由 Claude Code 的 WebSearch/WebFetch 工具执行。
"""

import json
import sys
import argparse
import logging
from datetime import datetime, timedelta
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
CONFIG_FILE = PROJECT_ROOT / "config" / "topics.json"
OUTPUT_DIR = PROJECT_ROOT / "output"
LOG_DIR = PROJECT_ROOT / "logs"

OUTPUT_DIR.mkdir(exist_ok=True)
LOG_DIR.mkdir(exist_ok=True)


def setup_logging(date_str=None):
    if date_str is None:
        date_str = datetime.now().strftime("%Y-%m-%d")
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=[
            logging.FileHandler(LOG_DIR / f"research_{date_str}.log", encoding="utf-8"),
            logging.StreamHandler(sys.stdout),
        ],
    )
    return logging.getLogger(__name__)


def load_config():
    if not CONFIG_FILE.exists():
        raise FileNotFoundError(f"Config file not found: {CONFIG_FILE}")
    with open(CONFIG_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def validate_config(config):
    errors = []
    if "research_domains" not in config:
        errors.append("Missing 'research_domains' in config")
    elif not isinstance(config["research_domains"], list) or len(config["research_domains"]) == 0:
        errors.append("'research_domains' must be a non-empty list")

    for i, domain in enumerate(config.get("research_domains", [])):
        for field in ["name", "keywords", "focus"]:
            if field not in domain:
                errors.append(f"Domain {i}: missing '{field}'")
        if "keywords" in domain and (not isinstance(domain["keywords"], list) or len(domain["keywords"]) == 0):
            errors.append(f"Domain '{domain.get('name', i)}': keywords must be a non-empty list")

    if "search_settings" not in config:
        errors.append("Missing 'search_settings' in config")
    return errors


def get_date_range(days_back=7):
    today = datetime.now()
    week_ago = today - timedelta(days=days_back)
    return week_ago.strftime("%Y-%m-%d"), today.strftime("%Y-%m-%d")


def _en_keywords(keywords, count=5):
    """Filter to English keywords only."""
    en = [k for k in keywords if not any('一' <= c <= '鿿' for c in k)]
    if len(en) < 2:
        en = keywords
    return en[:count]


def generate_search_queries(config):
    """为每个研究领域生成搜索查询列表，包含 arXiv 预印本和期刊论文两类。"""
    all_queries = []
    year = datetime.now().year
    prev_year = year - 1

    for domain in config["research_domains"]:
        keywords = domain["keywords"]
        primary = _en_keywords(keywords, 5)
        top2 = " ".join(primary[:2])
        top3 = " ".join(primary[:3])

        arxiv_queries = [
            f'site:arxiv.org {top2}',
            f'{top3} latest research {year}',
        ]
        if "conferences" in domain:
            confs = " OR ".join(f'"{c}"' for c in domain["conferences"][:3])
            arxiv_queries.append(f'({confs}) {primary[0]} {year}')

        journal_queries = [
            f'{top2} site:ieeexplore.ieee.org {prev_year} {year}',
            f'{top2} site:sciencedirect.com {prev_year} {year}',
            f'{primary[0]} journal published {year}',
        ]
        if "journals" in domain:
            j = " OR ".join(f'"{jrn}"' for jrn in domain["journals"][:2])
            journal_queries.append(f'{primary[0]} ({j}) {year}')

        all_queries.append({
            "domain": domain["name"],
            "keywords": keywords,
            "arxiv_queries": arxiv_queries,
            "journal_queries": journal_queries,
            "focus": domain.get("focus", []),
        })

    for theme in config.get("cross_cutting_themes", []):
        kw = " ".join(theme["keywords"][:4])
        all_queries.append({
            "domain": f"[交叉] {theme['name']}",
            "keywords": theme["keywords"],
            "arxiv_queries": [f'site:arxiv.org {kw}', f'{kw} {year}'],
            "journal_queries": [f'{kw} site:ieeexplore.ieee.org {prev_year} {year}'],
            "focus": [theme.get("relevance", "")],
        })
    return all_queries


def build_research_prompt(config, date_str=None):
    """构建完整的研究提示词，供 Claude Code 使用"""
    if date_str is None:
        date_str = datetime.now().strftime("%Y-%m-%d")
    date_from, date_to = get_date_range(config["search_settings"].get("time_range_days", 7))

    domains = config["research_domains"]
    settings = config.get("search_settings", {})
    queries = generate_search_queries(config)

    prompt_parts = [
        f"# DailyResearch - 每日科研热点追踪任务\n",
        f"**日期：** {date_str}",
        f"**覆盖周期：** {date_from} 至 {date_to}",
        f"**每主题最多结果数：** {settings.get('max_results_per_topic', 15)}\n",
        "---\n",
        "## 搜索任务清单\n",
    ]

    for i, q in enumerate(queries, 1):
        prompt_parts.append(f"### {i}. {q['domain']}\n")
        prompt_parts.append(f"**关注点：** {', '.join(q['focus'][:5])}\n")
        prompt_parts.append("**arXiv 预印本查询：**\n")
        for sq in q["arxiv_queries"]:
            prompt_parts.append(f"- `{sq}`\n")
        prompt_parts.append("**期刊/会议论文查询：**\n")
        for sq in q["journal_queries"]:
            prompt_parts.append(f"- `{sq}`\n")
        prompt_parts.append("\n")

    prompt_parts.append("---\n")
    prompt_parts.append("## 执行说明\n\n")
    prompt_parts.append("请按照 CLAUDE.md 中的完整工作流程执行：\n")
    prompt_parts.append("1. 使用 WebSearch 对上述每个查询执行搜索（至少 30 次搜索）\n")
    prompt_parts.append("2. 使用 WebFetch 获取有价值的论文/项目详情（至少 15 次获取）\n")
    prompt_parts.append("3. 交叉搜索：基于发现进行补充搜索\n")
    prompt_parts.append("4. 按 CLAUDE.md 指定的报告结构生成完整报告\n")
    prompt_parts.append(f"5. 将报告保存到 output/daily_research_{date_str}.md\n")
    prompt_parts.append("\n**质量标准：** 所有论文信息必须经 WebFetch 验证真实，禁止编造。\n")

    return "".join(prompt_parts)


def save_report(content, date_str=None, filename=None):
    if date_str is None:
        date_str = datetime.now().strftime("%Y-%m-%d")
    if filename is None:
        filename = f"daily_research_{date_str}.md"
    filepath = OUTPUT_DIR / filename
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)
    return filepath


def cmd_queries(args):
    config = load_config()
    queries = generate_search_queries(config)
    print(json.dumps(queries, ensure_ascii=False, indent=2))


def cmd_prompt(args):
    config = load_config()
    prompt = build_research_prompt(config, args.date)
    print(prompt)


def cmd_validate(args):
    config = load_config()
    errors = validate_config(config)
    if errors:
        print(f"Config validation FAILED ({len(errors)} errors):")
        for e in errors:
            print(f"  - {e}")
        sys.exit(1)
    else:
        print(f"Config OK: {len(config['research_domains'])} domains, "
              f"{len(config.get('cross_cutting_themes', []))} cross-cutting themes")


def cmd_log(args):
    logger = setup_logging()
    logger.info(args.message)


def cmd_save(args):
    content = sys.stdin.read()
    if not content.strip():
        print("Error: no content provided on stdin", file=sys.stderr)
        sys.exit(1)
    filepath = save_report(content, args.date, args.filename)
    print(f"Report saved: {filepath}")


def cmd_stats(args):
    reports = sorted(OUTPUT_DIR.glob("daily_research_*.md"), reverse=True)
    print(f"Total reports: {len(reports)}")
    print(f"Output directory: {OUTPUT_DIR}")
    if reports:
        print(f"\nLast 5 reports:")
        for r in reports[:5]:
            size_kb = r.stat().st_size / 1024
            print(f"  {r.name}  ({size_kb:.1f} KB)")


def main():
    parser = argparse.ArgumentParser(description="DailyResearch 科研热点追踪辅助工具")
    subparsers = parser.add_subparsers(dest="command", help="子命令")

    p_queries = subparsers.add_parser("queries", help="输出搜索查询 JSON")
    p_queries.set_defaults(func=cmd_queries)

    p_prompt = subparsers.add_parser("prompt", help="输出完整研究提示词")
    p_prompt.add_argument("--date", help="日期 YYYY-MM-DD", default=None)
    p_prompt.set_defaults(func=cmd_prompt)

    p_validate = subparsers.add_parser("validate", help="验证配置文件")
    p_validate.set_defaults(func=cmd_validate)

    p_log = subparsers.add_parser("log", help="记录日志消息")
    p_log.add_argument("message", help="日志消息")
    p_log.set_defaults(func=cmd_log)

    p_save = subparsers.add_parser("save", help="从 stdin 保存报告")
    p_save.add_argument("--date", help="日期 YYYY-MM-DD", default=None)
    p_save.add_argument("--filename", help="自定义文件名", default=None)
    p_save.set_defaults(func=cmd_save)

    p_stats = subparsers.add_parser("stats", help="查看报告统计")
    p_stats.set_defaults(func=cmd_stats)

    args = parser.parse_args()
    if args.command is None:
        parser.print_help()
        sys.exit(1)
    args.func(args)


if __name__ == "__main__":
    main()
