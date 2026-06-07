# DailyResearch — 智能科研热点追踪

基于 Claude Code 的科研热点追踪工具。指定研究方向后，自动搜索最新论文（arXiv 预印本 + 期刊已发表），生成结构化分析报告。

## 核心功能

- **真实搜索** — Claude Code 的 WebSearch/WebFetch 工具执行网络搜索，非模型幻觉
- **双源覆盖** — arXiv 预印本（最新动态）+ IEEE/Elsevier 期刊（同行评审成果）
- **深度分析** — 每篇论文含技术贡献、实验数据、与自有项目的关联分析
- **选题启发** — 基于最新进展自动生成研究 Idea，含可行性评估和时间线建议
- **可定制** — 研究方向、关键词、关注会议/期刊全部通过配置文件定义

## 快速安装

**前提条件：** [Claude Code](https://docs.anthropic.com/en/docs/claude-code/overview)、Python 3.8+、ANTHROPIC_API_KEY

```bash
git clone https://github.com/BITjiaxing/DailyResearch.git
cd DailyResearch
pip install -r requirements.txt
python scripts/research_agent.py validate
```

## 使用方式

在 Claude Code 中打开项目目录，输入：

```
请按照 CLAUDE.md 的定义执行科研热点追踪任务
```

Claude Code 将自动搜索、获取详情、生成报告并保存到 `output/`。

**辅助命令：**

```bash
python scripts/research_agent.py prompt    # 生成搜索提示词
python scripts/research_agent.py queries   # 输出搜索查询 JSON
python scripts/research_agent.py stats     # 查看报告统计
python scripts/research_agent.py validate  # 验证配置文件
```

## 适配你的研究方向

项目默认以**强化学习 + 无人机**为例配置了搜索策略。使用时需要修改两个文件以适配你自己的方向：

### 1. 修改研究主题 — `config/topics.json`

每个领域包含以下字段：

```json
{
  "name": "领域名称",
  "keywords": ["英文关键词1", "英文关键词2", ...],
  "focus": ["关注点1", "关注点2", ...],
  "conferences": ["顶会1", "顶会2", ...],
  "journals": ["顶刊1", "顶刊2", ...]
}
```

- 增删领域、修改关键词即可
- `keywords` 建议用英文（搜索覆盖更广）
- `conferences` 和 `journals` 填写本领域的顶会顶刊
- 脚本会自动根据关键词和期刊名生成 arXiv + 期刊两类搜索查询

改完后运行 `python scripts/research_agent.py validate` 验证。

### 2. 修改关联项目 — `CLAUDE.md`

打开 `CLAUDE.md` 顶部，找到 `## 关联项目` 部分，替换为自己的项目。这会直接影响报告中的"与本课题关联分析"和"研究 Idea"部分。

也可以保留为示例（仅影响报告中的关联分析），不影响搜索功能本身。

## 报告结构

生成的报告包含以下章节：

- **领域概览** — 各方向进展摘要 + 热度评估
- **各领域详细报告** — 重要论文分析（标题、摘要、技术贡献、实验数据、关联分析）
- **交叉主题** — 跨领域的共性技术进展
- **开源项目动态** — 相关代码仓库更新
- **总结与展望** — 关键进展 + 关注优先级
- **研究启发与选题分析** — 趋势洞察、潜在研究 Idea（含实现方案）、时间线建议
- **附录** — 论文总表、会议投稿截止日期

示例报告见 `output/sample_report.md`。

## 文件结构

```
DailyResearch/
├── CLAUDE.md              # 智能体定义（搜索策略、执行流程、质量标准）
├── README.md              # 本文件
├── config/
│   └── topics.json        # 研究主题配置（领域、关键词、会议、期刊）
├── scripts/
│   ├── research_agent.py  # 查询生成、报告管理、配置验证
│   ├── utils.py           # 报告验证、arXiv ID 提取等工具函数
│   ├── run_daily.bat      # Windows 批处理启动脚本
│   └── run_daily.ps1      # Windows PowerShell 启动脚本
└── output/                # 报告输出目录
```

## 依赖

- Python 3.8+
- Claude Code
- ANTHROPIC_API_KEY 环境变量

## 平台

Windows / Linux / macOS 均支持。

## 许可证

MIT License
