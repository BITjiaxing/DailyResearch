# DailyResearch — 智能科研热点追踪

一个 AI 驱动的科研热点追踪工具。指定研究方向后，自动搜索最新论文（arXiv 预印本 + 期刊已发表），生成结构化分析报告。

## 支持的 AI 工具

本项目的核心是 `CLAUDE.md`（智能体行为定义） + `config/topics.json`（研究方向配置）。任何支持读取项目级指令文件并拥有 Web 搜索能力的 AI 编程工具均可使用：

| 工具 | 后端 API | 说明 |
|------|----------|------|
| **Claude Code**（原生） | Anthropic API | 原生支持，无需额外配置 |
| **Claude Code + cc-switch** | DeepSeek / MIMO / 其他 | 国内推荐方案，低成本替代 |
| **Codex**（OpenAI） | GPT Plus 订阅 | 需将 CLAUDE.md 内容作为系统指令导入 |

> 核心逻辑：工具读取 `CLAUDE.md` → 按照定义的搜索策略使用 WebSearch/WebFetch → 生成报告保存到 `output/`。

---

## 快速安装

```bash
git clone https://github.com/BITjiaxing/DailyResearch.git
cd DailyResearch
pip install -r requirements.txt
python scripts/research_agent.py validate
```

---

## 配置 AI 工具

### 方案 A：Claude Code + Anthropic API（官方原生）

1. 安装 [Claude Code](https://docs.anthropic.com/en/docs/claude-code/overview)
2. 在 [Anthropic Console](https://console.anthropic.com/) 申请 API Key
3. 设置环境变量：
   ```bash
   # Windows (PowerShell)
   $env:ANTHROPIC_API_KEY = "sk-ant-..."

   # Linux / macOS
   export ANTHROPIC_API_KEY="sk-ant-..."
   ```

### 方案 B：Claude Code + DeepSeek / MIMO API（国内推荐）

通过社区工具将 Claude Code 接入国产大模型，成本远低于 Anthropic 官方 API。

**步骤 1：申请 API Key**

- **DeepSeek**：[platform.deepseek.com](https://platform.deepseek.com/) → 注册 → API Keys → 创建
- **MIMO**：[mimo.chat](https://mimo.chat/) → 注册 → 开发者中心 → 获取 Key
- 两者均赠送新用户免费额度，DeepSeek 定价约为 Anthropic 的 1/20

**步骤 2：安装 cc-switch**

```bash
npm install -g cc-switch
```

或从 GitHub 安装：

```bash
git clone https://github.com/user/cc-switch.git
cd cc-switch && npm install && npm link
```

**步骤 3：配置 API 后端**

```bash
# 配置 DeepSeek
cc-switch config --provider deepseek --api-key "sk-xxx" --model deepseek-chat

# 配置 MIMO  
cc-switch config --provider mimo --api-key "sk-xxx" --model mimo-chat
```

配置完成后 Claude Code 会自动通过 cc-switch 路由到指定的后端 API。

### 方案 C：Codex（OpenAI GPT Plus 用户）

1. 确保已订阅 [ChatGPT Plus](https://chat.openai.com/)（$20/月）
2. 安装 [Codex CLI](https://github.com/openai/codex)
3. 将 `CLAUDE.md` 的内容复制到 Codex 的会话指令中，或直接进入项目目录让 Codex 读取

> Codex 对 CLAUDE.md 格式兼容良好，核心的搜索策略和报告结构均能正常工作。

---

## 使用方式

在 AI 工具中打开项目目录，输入：

```
请按照 CLAUDE.md 的定义执行科研热点追踪任务
```

工具将自动搜索、获取详情、生成报告并保存到 `output/`。

**辅助命令：**

```bash
python scripts/research_agent.py prompt    # 生成搜索提示词
python scripts/research_agent.py queries   # 输出搜索查询 JSON
python scripts/research_agent.py stats     # 查看报告统计
python scripts/research_agent.py validate  # 验证配置文件
```

---

## 适配你的研究方向

项目默认以**强化学习 + 无人机**为例配置了搜索策略。使用时需要修改两个文件：

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
- `keywords` 建议用英文（搜索覆盖面更广）
- `conferences` 和 `journals` 填写本领域的顶会顶刊
- 脚本会自动根据关键词和期刊名生成 arXiv + 期刊两类搜索查询

改完后运行 `python scripts/research_agent.py validate` 验证。

### 2. 修改关联项目 — `CLAUDE.md`

打开 `CLAUDE.md` 顶部，找到 `## 关联项目` 部分，替换为自己的项目。这会直接影响报告中的"与本课题关联分析"和"研究 Idea"部分。

---

## 报告结构

- **领域概览** — 各方向进展摘要 + 热度评估
- **各领域详细报告** — 重要论文分析（标题、摘要、技术贡献、实验数据、关联分析）
- **交叉主题** — 跨领域的共性技术进展
- **开源项目动态** — 相关代码仓库更新
- **总结与展望** — 关键进展 + 关注优先级
- **研究启发与选题分析** — 趋势洞察、研究 Idea（含实现方案）、时间线建议
- **附录** — 论文总表、会议投稿截止日期

示例报告见 `output/sample_report.md`。

---

## 文件结构

```
DailyResearch/
├── CLAUDE.md              # 智能体定义（搜索策略、执行流程、质量标准）
├── README.md              # 本文件
├── config/
│   └── topics.json        # 研究主题配置
├── scripts/
│   ├── research_agent.py  # 查询生成、报告管理、配置验证
│   ├── utils.py           # 报告验证、arXiv ID 提取等
│   ├── run_daily.bat      # Windows 启动脚本
│   └── run_daily.ps1      # Windows PowerShell 启动脚本
└── output/                # 报告输出目录
```

## 依赖

- Python 3.8+
- 任一支持的 AI 工具（Claude Code / Codex / cc-switch 等）
- 对应后端的 API Key 或订阅

## 平台

Windows / Linux / macOS 均支持。

## 许可证

MIT License
