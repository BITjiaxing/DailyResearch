# DailyResearch - 每日科研热点追踪智能体

## 项目简介

基于 Claude Code 的智能科研助手，使用 **WebSearch + WebFetch 工具**执行真实网络搜索，追踪以下方向的最新科研动态：

- **强化学习算法** - PPO, SAC, TD3, 离线 RL, 模型基础 RL
- **分层强化学习** - 选项框架, 技能发现, 时间抽象
- **多智能体强化学习** - MAPPO, QMIX, 通信学习, 可扩展 MARL
- **无人机飞行控制** - PX4, ArduPilot, MPC, 自适应控制
- **无人机集群** - 编队控制, 任务分配, 分布式决策
- **空地协同** - 异构机器人协作, 协同感知与建图

## 核心功能

- **真实搜索** — Claude Code WebSearch/WebFetch 工具执行搜索和获取，信息真实可验证
- **论文检索** — 检索 arXiv, 顶会, 顶刊最新论文
- **专利监控** — 追踪相关技术专利
- **每日报告** — 结构化的 Markdown 报告（包含研究 Idea 和选题分析）
- **关联分析** — 分析与 xmd_rl 等项目的关联度

## 新手安装（首次使用必读）

### 前提条件

1. **安装 Claude Code** — [官方安装指南](https://docs.anthropic.com/en/docs/claude-code/overview)
2. **配置 ANTHROPIC_API_KEY** — 在环境变量或 Claude Code 设置中配置 API 密钥
3. **安装 Python 3.8+** — 用于运行辅助脚本

### 安装步骤

```bash
# 1. 克隆项目
git clone <repo-url> DailyResearch
cd DailyResearch

# 2. 安装 Python 依赖（可选，辅助脚本需要）
pip install -r requirements.txt

# 3. 验证配置
python scripts/research_agent.py validate
```

### 配置权限（关键步骤）

项目已包含 `.claude/settings.json` 预配置了所需的 WebSearch/WebFetch 权限。首次运行 Claude Code 时，确认接受这些权限即可。

如果你想自定义研究方向和关键词，编辑 `config/topics.json`。

---

## 适配你的研究方向（给课题组师兄弟）

本项目默认追踪的是 **强化学习 + 无人机** 交叉方向。如果你研究的是其他方向，需要改两个文件：

### 第一步：修改研究主题 `config/topics.json`

这个文件定义了"搜什么"。每个领域包含：

```json
{
  "name": "强化学习算法",          // 领域名称
  "keywords": ["reinforcement learning", "PPO", "SAC", ...],  // 搜索关键词（英文为主）
  "focus": ["算法创新", "样本效率", ...],                    // 重点关注
  "conferences": ["NeurIPS", "ICML", ...],                   // 顶会
  "journals": ["JMLR", "Artificial Intelligence", ...]       // 顶刊
}
```

**怎么改：**
- 删掉不相关的领域，换成你自己的方向。比如做 CV 的改成目标检测、图像分割、3D 视觉等
- `keywords` 用英文（搜索覆盖面广），中英文混合也可以
- `conferences` 和 `journals` 填你领域的顶会顶刊

改完后运行验证：
```bash
python scripts/research_agent.py validate
```

> **搜索查询会自动适配**：脚本会根据你填的 keywords、conferences、journals 自动生成 arXiv 和期刊两类搜索查询。

### 第二步：修改关联项目 `CLAUDE.md`

打开 `CLAUDE.md`，找到最前面的这几行：

```
## 关联项目
- **xmd_rl** — 四旋翼强化学习任务包（基于 Isaac Lab / RSL-RL）
- **PX4-Autopilot** — 开源飞控系统
- ...
```

替换成你自己的项目。这个信息会影响报告中的"与本课题关联分析"和"研究 Idea"部分——Claude 会把搜到的新论文和你的项目做关联。

### 如果你不做这两个修改

师兄弟 clone 下来直接用，报告分析的还是 RL + 无人机的热点。**他们必须改 `topics.json` 和 `CLAUDE.md` 的关联项目**才能适配自己的方向。

---

## 快速开始

### 1. 配置

编辑 `config/topics.json` 调整研究领域和关键词。

验证配置：
```bash
python scripts/research_agent.py validate
```

### 2. 运行（在 Claude Code 中）

在 Claude Code 中打开本项目目录，输入：

```
请按照 CLAUDE.md 的定义执行每日科研热点追踪任务
```

Claude Code 将自动：
1. 使用 WebSearch 搜索各领域最新动态（arXiv 预印本 + IEEE/Elsevier 期刊）
2. 使用 WebFetch 获取论文和项目详情
3. 生成结构化报告并保存到 `output/`

### 3. 辅助命令

```bash
# 生成搜索查询列表
python scripts/research_agent.py queries

# 生成完整研究提示词
python scripts/research_agent.py prompt

# 查看报告统计
python scripts/research_agent.py stats

# 从 stdin 保存报告
echo "report content" | python scripts/research_agent.py save
```

### 4. Windows 快速启动

```powershell
# PowerShell
.\scripts\run_daily.ps1          # 生成提示词
.\scripts\run_daily.ps1 -Stats   # 查看统计
.\scripts\run_daily.ps1 -Validate # 验证配置
```

### 5. 定时任务

使用 Claude Code 的 `/schedule` 功能（跨平台）：
```
/schedule "每天早上9点运行科研热点追踪" cron="0 9 * * *"
```

## 文件结构

```
DailyResearch/
├── CLAUDE.md              # 研究智能体定义（工作流程、搜索策略、报告结构）
├── README.md              # 本文件
├── config/
│   └── topics.json        # 研究主题配置
├── scripts/
│   ├── research_agent.py  # 辅助工具（查询生成、报告管理、配置验证）
│   ├── utils.py           # 工具函数（报告验证、arXiv ID 提取等）
│   ├── run_daily.bat      # Windows 批处理启动脚本
│   └── run_daily.ps1      # Windows PowerShell 启动脚本
├── output/                # 每日报告输出
└── logs/                  # 运行日志
```

## 报告结构

1. 领域概览 — 各方向整体进展 + 热度表
2. 各领域详细报告 — 6 大领域 × 详细论文分析
3. 交叉主题 — Sim-to-Real、安全 RL、仿真平台
4. 开源项目动态
5. 总结与展望
6. **研究启发与选题分析** — 趋势洞察、研究 Idea、时间线建议
7. 附录 — 论文列表、会议时间

## 配置说明

`config/topics.json`:
- `research_domains`: 6 大研究领域（名称、关键词、关注点、会议、期刊）
- `cross_cutting_themes`: 交叉主题
- `search_settings`: 搜索设置（时间范围、结果数量、模型）
- `output_settings`: 输出设置

## 依赖

- Python 3.8+
- Claude Code（提供 WebSearch/WebFetch 工具）
- ANTHROPIC_API_KEY 环境变量

## 关联项目

- **xmd_rl** - 四旋翼强化学习任务包（Isaac Lab）
- **PX4-Autopilot** - 开源飞控系统
- **PegasusSimulator** - 仿真环境
- **spear_ws** - ROS2 工作空间

## 平台支持

- **Windows** ✓ — 主要支持，含 .bat 和 .ps1 启动脚本
- **Linux** ✓ — Python 脚本跨平台兼容
- **macOS** ✓ — Python 脚本跨平台兼容

## 许可证

MIT License
