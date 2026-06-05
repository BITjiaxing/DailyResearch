#!/usr/bin/env python3
"""
DailyResearch 工具函数
支持报告格式化、日期处理、统计分析和 Markdown 辅助函数。
"""

import re
from datetime import datetime, timedelta
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
OUTPUT_DIR = PROJECT_ROOT / "output"


def ensure_output_dir():
    OUTPUT_DIR.mkdir(exist_ok=True)
    return OUTPUT_DIR


def format_report_header(date_str=None):
    if date_str is None:
        date_str = datetime.now().strftime("%Y-%m-%d")
    date_from = (datetime.strptime(date_str, "%Y-%m-%d") - timedelta(days=7)).strftime("%Y-%m-%d")
    return (
        f"# 每日科研热点追踪报告\n\n"
        f"**报告日期：** {date_str}\n"
        f"**覆盖周期：** {date_from} 至 {date_str}\n"
        f"**生成工具：** DailyResearch v2.0\n\n---\n"
    )


def extract_arxiv_ids(text):
    """从文本中提取 arXiv ID（支持新旧格式）"""
    patterns = [
        r'arxiv\.org/abs/(\d{4}\.\d{4,5})',
        r'arxiv:(\d{4}\.\d{4,5})',
        r'arXiv:(\d{4}\.\d{4,5})',
    ]
    ids = set()
    for p in patterns:
        ids.update(re.findall(p, text, re.IGNORECASE))
    return sorted(ids)


def extract_github_repos(text):
    """从文本中提取 GitHub 仓库链接"""
    pattern = r'github\.com/([\w.-]+/[\w.-]+)'
    repos = set()
    for match in re.findall(pattern, text):
        repos.add(match.rstrip("/"))
    return sorted(repos)


def count_papers_in_report(content):
    """统计报告中的论文数量（按 arXiv ID 去重）"""
    ids = extract_arxiv_ids(content)
    return len(ids)


def validate_report(content):
    """验证报告完整性，返回 (is_valid, issues)"""
    issues = []
    checks = [
        ("领域概览", "## 1. 领域概览" not in content and "领域概览" not in content),
        ("重要论文", "重要论文" not in content),
        ("总结展望", "总结" not in content),
        ("研究启发", "研究启发" not in content and "## 11" not in content),
    ]
    for name, missing in checks:
        if missing:
            issues.append(f"可能缺少章节: {name}")

    arxiv_ids = extract_arxiv_ids(content)
    if len(arxiv_ids) < 5:
        issues.append(f"论文数量不足（检测到 {len(arxiv_ids)} 篇，建议 ≥ 10）")

    if len(content) < 5000:
        issues.append(f"报告可能过短（{len(content)} 字符）")

    return len(issues) == 0, issues


def compare_reports(report_a_path, report_b_path):
    """比较两天报告的差异，返回新增论文"""
    a_ids = set()
    b_ids = set()
    for path, id_set in [(report_a_path, a_ids), (report_b_path, b_ids)]:
        if Path(path).exists():
            a_ids.update(extract_arxiv_ids(Path(path).read_text(encoding="utf-8")))
    if not a_ids:
        return list(b_ids)
    return list(b_ids - a_ids)


def format_arxiv_link(arxiv_id):
    return f"https://arxiv.org/abs/{arxiv_id}"


def format_github_link(repo):
    return f"https://github.com/{repo}"


def heat_level(n):
    """热度等级 1-5 转为 🔥 字符串"""
    return "🔥" * max(1, min(5, n))


def week_boundaries(date_str=None):
    """返回本周起止日期"""
    if date_str is None:
        date_str = datetime.now().strftime("%Y-%m-%d")
    dt = datetime.strptime(date_str, "%Y-%m-%d")
    monday = dt - timedelta(days=dt.weekday())
    sunday = monday + timedelta(days=6)
    return monday.strftime("%Y-%m-%d"), sunday.strftime("%Y-%m-%d")


def list_reports(sort_by="date"):
    """列出所有报告文件"""
    reports = list(OUTPUT_DIR.glob("daily_research_*.md"))
    if sort_by == "date":
        reports.sort(reverse=True)
    elif sort_by == "size":
        reports.sort(key=lambda p: p.stat().st_size, reverse=True)
    return reports
