# 每日科研热点追踪报告

**报告日期：** 2026-06-05
**覆盖周期：** 2026-05-29 至 2026-06-05
**研究领域：** 强化学习、无人机控制、集群、分层RL、多智能体、空地协同
**生成工具：** DailyResearch v2.0

---

## 目录

1. [领域概览](#1-领域概览)
2. [强化学习算法](#2-强化学习算法)
3. [分层强化学习](#3-分层强化学习)
4. [多智能体强化学习](#4-多智能体强化学习)
5. [无人机飞行控制](#5-无人机飞行控制)
6. [无人机集群](#6-无人机集群)
7. [空地协同](#7-空地协同)
8. [交叉主题](#8-交叉主题)
9. [开源项目动态](#9-开源项目动态)
10. [本周总结与展望](#10-本周总结与展望)
11. [研究启发与选题分析](#11-研究启发与选题分析)
12. [附录](#12-附录)

---

## 1. 领域概览

本周（2026年5月29日–6月5日）各方向科研进展概览：

| 方向 | 热度 | 关键进展 |
|------|------|----------|
| 无人机飞行控制 | 🔥🔥🔥🔥🔥 | **RAPTOR 基础策略**（UC Berkeley）：单网络零样本适配10种四旋翼；NN-MPC 混合框架成熟；可微分仿真推动端到端训练 |
| 多智能体 + UAV 集群 | 🔥🔥🔥🔥🔥 | 异构角色架构成为主流；STAGE 图注意力策略、FOFE 灵活编码、LLM + MARL（RALLY）三条线同步突破 |
| Sim-to-Real 迁移 | 🔥🔥🔥🔥 | 域随机化被批判"过于保守"；自适应外环控制 + 残差动力学预测器成为新范式 |
| 安全强化学习 | 🔥🔥🔥🔥 | Koopman CBF + SAC 融合；事件触发显式 CBF 滤波大幅降低在线计算；CAPSULE 概率安全框架 |
| 分层强化学习 | 🔥🔥🔥🔥 | 多分辨率技能（MRS）缩小与平面 RL 精度差；Skill Discovery 走向"结构化"和"人机协作感知" |
| 强化学习算法 | 🔥🔥🔥 | 状态依赖折扣因子（AdaGamma）、单纯嵌入几何偏置、多步优先策略——三项独立创新同时提升 SAC/PPO |
| 空地协同 | 🔥🔥🔥🔥 | 能量感知探索、空地交接神经代理规划、UAV 可部署微型 UGV——从概念走向系统实现 |

**本周总体判断：无人机 + RL 交叉领域正处于 2018 年以来最热的阶段。** Foundation Policy（基础策略）、LLM + MARL、Koopman 安全滤波三条主线同步爆发，Sim-to-Real 方法论正在经历范式转移。

---

## 2. 强化学习算法

### 2.1 重要论文

#### 2.1.1 AdaGamma: State-Dependent Discounting for Temporal Adaptation in RL

- **作者：** 匿名（预印本）
- **发表：** arXiv 2605.06149 (2026-05-07)
- **链接：** https://arxiv.org/abs/2605.06149

**摘要：** 本文挑战了强化学习中固定折扣因子 γ 的基本假设，提出 AdaGamma——一种学习状态依赖折扣因子的方法。核心机制是学习一个 γ(s) 函数并使用回报一致性正则化器（return-consistency regularizer）约束，确保折扣因子在不同状态下既有灵活性又不破坏值函数的收敛性。方法以即插即用方式集成到 **SAC 和 PPO** 中，在连续控制基准测试上取得一致提升，并在京东物流的真实 A/B 测试中验证了实用性。

**关键技术贡献：**
1. 首次将状态依赖折扣因子形式化为可学习组件（非超参数）
2. 回报一致性正则化器保证值函数贝尔曼方程的一致性
3. 对 SAC 和 PPO 均有效——非架构特定改进
4. 真实工业场景（物流调度）验证

**实验结果：** MuJoCo 连续控制任务中 SAC 和 PPO 均有 3-8% 的性能提升；京东物流 A/B 测试中配送效率提升 7.2%。

**与本课题关联：** ⭐⭐⭐⭐ — 状态依赖折扣因子特别适合四旋翼飞行任务（不同飞行阶段对远期/近期奖励的偏好不同：悬停关注即时稳定性，导航关注远期目标）。可直接集成到 xmd_rl 的 SAC/PPO 训练流程中。

---

#### 2.1.2 Multi-Step First: PPO Outperforms TD3 and SAC Under Partial Observability

- **作者：** 已发表于 Neural Networks, Vol. 199, 2026
- **链接：** https://arxiv.org/html/2209.04999v3
- **DOI：** 10.1016/j.neunet.2025.108521

**摘要：** 这篇长期打磨的论文（arXiv 2022 → 期刊 2026）揭示了一个被忽视的重要发现：**在部分可观测环境中，PPO 的鲁棒性显著优于 TD3 和 SAC**——这与标准 MDP 设定下的算法排名完全相反。作者提出 MTD3 和 MSAC（Multi-Step 变体），通过多步回报估计恢复鲁棒性。论文提供了一个实际指导框架：当环境的可观测性不确定时，PPO 应作为首选算法。

**关键技术贡献：**
1. 发现并系统验证了 PPO 在 POMDP 下的鲁棒性优势
2. 提出多步变体 MTD3/MSAC 修复 TD3/SAC 的脆弱性
3. 提供了算法选择的实用决策框架

**与本课题关联：** ⭐⭐⭐⭐⭐ — 无人机实际部署中普遍存在部分可观测性（传感器噪声、遮挡、通信延迟）。该结论直接影响 xmd_rl 的算法选型：在真实飞行场景中，PPO 可能比 SAC 更可靠。

---

#### 2.1.3 Simplicial Embeddings Improve Sample Efficiency in Actor-Critic Agents

- **作者：** 预印本
- **发表：** arXiv 2510.13704 (v2: 2026-06-03)
- **链接：** https://export.arxiv.org/abs/2510.13704

**摘要：** 将状态嵌入约束到单纯形（simplex）几何结构上，作为一种轻量级几何归纳偏置。在 **FastSAC、PPO 和 FastTD3** 上一致提升了离散和连续控制任务的样本效率。该方法的优势在于：无需修改算法核心逻辑，仅改变嵌入层的约束方式即可获得 10-25% 的样本效率提升。

**关键技术贡献：**
1. 单纯嵌入作为通用几何偏置，跨算法有效
2. 实现极简：仅修改嵌入层约束，不改算法逻辑
3. 在离散和连续控制上均有效

**与本课题关联：** ⭐⭐⭐ — 轻量级改进，可直接应用于 xmd_rl 的任何 RL 算法。实现成本低、风险小。

---

#### 2.1.4 RLScale-Bench: When Does Deep RL Beat Calibrated Baselines?

- **作者：** 预印本
- **发表：** arXiv 2605.26418 (2026-05-26)
- **链接：** https://arxiv.org/abs/2605.26418

**摘要：** 在 Kubernetes 自适应资源控制场景中，精心校准的规则控制器（rule-based controller）在约束违反率上比 **PPO、SAC、DQN、A2C、TD3、DDPG** 低 1-2 个数量级。离散动作算法的表现普遍优于连续动作算法。这篇论文的价值在于提供了一个清醒的现实检验：**基准校准比算法选择更重要**。

**关键发现：**
1. 校准良好的规则控制器在约束违规上远超所有 DRL 方法
2. 离散动作空间在此类任务上显著优于连续动作
3. 奖励工程和基准校准比算法本身的改进更关键

**与本课题关联：** ⭐⭐ — 提醒我们在 xmd_rl 的奖励函数设计和基准对比中不要过度追求算法复杂度而忽视基础校准。

---

### 2.2 技术趋势

| 趋势 | 驱动力 | 潜力评估 |
|------|--------|----------|
| 状态依赖超参数（AdaGamma） | 固定超参数在非平稳任务中的不适配 | 🔥🔥 稳步增长 |
| 几何归纳偏置（Simplicial Embeddings） | 表示学习的几何视角 | 🔥🔥 新兴方向 |
| 部分可观测下的算法选择 | 真实部署的传感器不完美 | 🔥🔥🔥 刚需 |
| 现实基准测试 | 学术基准与工业落地的鸿沟 | 🔥🔥🔥 趋势确立 |

---

## 3. 分层强化学习

### 3.1 重要论文

#### 3.1.1 Multi-Resolution Skills for HRL Agents (MRS)

- **作者：** 预印本
- **发表：** arXiv 2505.21410 (v2: 2026-04)
- **链接：** https://arxiv.org/html/2505.21410v2

**摘要：** 提出 **MRS（Multi-Resolution Skills）**，学习多个固定时间尺度的目标预测模块，由一个元控制器（meta-controller）统一调度。核心创新在于：不同时间分辨率的技能对应不同的规划粒度，元控制器按需选择最合适的技能层级。在 DeepMind Control、Gym-Robotics 和 AntMaze 上，MRS **首次缩小了分层 RL 与平面（非分层）RL 方法之间的性能差距**。

**关键技术贡献：**
1. 多时间分辨率技能同时学习，无需预定义层级结构
2. 元控制器自动选择最合适的技能粒度
3. 首次实现 HRL 性能与平面 RL 持平

**与本课题关联：** ⭐⭐⭐⭐⭐ — MRS 的多分辨率思想与无人机集群的分层控制天然契合。低分辨率技能 = 集群宏观编队，中分辨率 = 子群协调，高分辨率 = 单机精细控制。这是本周最值得 xmd_rl 关注的分层 RL 论文。

---

#### 3.1.2 CARL: Contrastive Action-based Representations for Reusable Local Control

- **作者：** 预印本
- **发表：** arXiv 2605.26371 (2026-05-25)
- **链接：** https://arxiv.org/abs/2605.26371

**摘要：** 提出 **CARL（Contrastive Action-based Representations for Reusable Local Control）**——在离线 HRL 环境中通过对比学习聚类有意义的技能，提升技能的可复用性。与 HIQL 结合在 OGBench 上取得最先进结果。核心思路是通过 **动作空间的对比表示** 而非状态空间来定义技能边界，使得学到的技能在不同任务间更具迁移性。

**关键技术贡献：**
1. 动作空间对比学习（而非传统的状态空间聚类）
2. 离线设定下技能可复用性的大幅提升
3. 与 HIQL 结合达到 SOTA

**与本课题关联：** ⭐⭐⭐⭐ — 离线 RL + 技能复用是无人机 sim-to-real 的理想范式：在仿真中预训练技能库，在真实环境中复用和微调。

---

#### 3.1.3 SUSD: Structured Unsupervised Skill Discovery through State Factorization

- **作者：** 预印本
- **发表：** arXiv 2602.01619 (v2: 2026-06)
- **链接：** https://arxiv.org/html/2602.01619v2

**摘要：** 将状态空间分解为多个独立因子（components），并为每个因子分配独立的技能变量，使用自适应好奇心驱动的权重来平衡各因子的探索。在多目标环境中，**SUSD 显著优于基于互信息（MI）的方法和 DSD 方法**。关键洞见：技能发现不应该从整体状态中无结构地抽取，而应该显式建模状态的因子化结构。

**与本课题关联：** ⭐⭐⭐ — 状态因子化思想可应用于将无人机状态分解为位置、姿态、速度等独立因子，每类因子对应特定技能族。

---

#### 3.1.4 Unsupervised Hierarchical Skill Discovery (Harvey et al.)

- **作者：** Harvey et al.
- **发表：** arXiv 2601.23156 (2026-01-30)
- **链接：** https://arxiv.org/abs/2601.23156

**摘要：** 使用基于语法的轨迹分割和层次结构归纳，在 **Craftax 和完整 Minecraft** 环境中实现无监督分层技能发现。这是首个在如此复杂的开放式环境中成功运行的无监督 HRL 方法。语法引导的分割能够发现具有清晰语义边界的技能（如"采集木材"→"制作工具"→"建造房屋"）。

**与本课题关联：** ⭐⭐⭐⭐ — 语法引导的层次分割思想可应用于无人机复杂任务的自动分解（如"起飞侦察"→"目标识别"→"跟踪"→"返航"），尤其适合空地协同的长程任务规划。

---

### 3.2 技术趋势

| 方向 | 进展状态 | 关键挑战 |
|------|----------|----------|
| 多分辨率技能 | MRS 首次达到与平面 RL 相当的性能 | 技能粒度的最优选择仍靠经验 |
| 动作空间技能聚类 | CARL 离线设定创新 | 在线环境中的实时适应性 |
| 状态因子化技能发现 | SUSD 超越 MI 方法 | 因子化结构的人工设计依赖 |
| 语法引导层次分割 | Minecraft 上验证可行性 | 在物理控制任务中的适用性 |
| LLM + HRL 数学推理 | ARISE 超越 GRPO | 物理世界（非符号）环境的泛化 |

---

## 4. 多智能体强化学习

### 4.1 重要论文

#### 4.1.1 SCALE-COMM: Shared, Contrastively-Aligned Latent Embeddings for MARL Communication

- **作者：** 预印本
- **发表：** arXiv 2605.27532 (2026-05-26), IEEE IV 2026
- **链接：** https://arxiv.org/abs/2605.27532

**摘要：** **将通信学习与策略优化解耦**——这是 MARL 通信研究的一个重要范式转变。SCALE-COMM 使用对比对齐的潜在嵌入来学习智能体间的消息，这些消息捕获任务相关的规划和交通信息，而不直接依赖于当前策略。解耦设计带来了两个关键优势：消息学习的稳定性和样本效率的大幅提升。

**关键技术贡献：**
1. 通信学习与策略优化完全解耦
2. 对比学习对齐跨智能体的潜在空间
3. 消息内容捕获任务级规划信息（而非低级动作）
4. 训练稳定性显著优于端到端通信学习方法

**与本课题关联：** ⭐⭐⭐⭐⭐ — 通信-策略解耦对无人机集群至关重要：可以在仿真中用大量交互数据预训练通信协议，然后在实际部署中复用，大幅降低真实环境中的通信学习成本。

---

#### 4.1.2 SCoUT: Scalable Communication via Utility-Guided Temporal Grouping

- **作者：** Manav Vora et al.
- **发表：** arXiv 2603.04833 (2026-03-05)
- **链接：** https://arxiv.org/abs/2603.04833

**摘要：** 解决了 MARL 通信的两个基本问题：**何时通信**和**与谁通信**。SCoUT 使用时间抽象——通过 Gumbel-Softmax 每 K 步重新采样软智能体分组，并使用反事实通信优势（counterfactual communication advantages）进行精确的信用分配。这种时间分组机制大幅降低了通信开销，同时保持了协调质量。

**与本课题关联：** ⭐⭐⭐⭐⭐ — 无人机集群通信带宽是硬约束。SCoUT 的"何时通信+与谁通信"框架与集群场景完美匹配：无人机无需每步广播，只需在关键决策点与邻近无人机同步。

---

#### 4.1.3 CLOVER: Wireless Communication Enhanced Value Decomposition for MARL

- **作者：** Diyi Hu, Bhaskar Krishnamachari
- **发表：** arXiv 2604.08728 (2026-04-09)
- **链接：** https://arxiv.org/abs/2604.08728

**摘要：** 在真实的 **p-CSMA 无线信道**模型下，将集中式值分解器（mixer）条件化于实际通信图。使用 GNN 作为 mixer，配合置换等变超网络（permutation-equivariant hypernetwork），证明了 CLOVER 的表达能力 **严格强于 QMIX 风格的 mixer**。这是首个将物理层通信约束显式纳入值分解框架的工作。

**关键技术贡献：**
1. 首次将真实无线信道模型（p-CSMA）纳入 MARL 值分解
2. GNN mixer 的表达能力严格优于 QMIX
3. 置换等变超网络保证智能体数量变化时的泛化性

**与本课题关联：** ⭐⭐⭐⭐ — PX4 实际通信基于 MAVLink/Telemetry，CLOVER 的物理信道感知价值分解可直接指导实际集群通信协议的设计。

---

#### 4.1.4 MARL + Heterogeneous UAV Swarm 专题

本周在 MARL + UAV 集群交叉方向有大量高质量产出，反映了该方向的爆发态势：

| 论文 | 方法 | 核心创新 | 性能提升 |
|------|------|----------|----------|
| **HMUDRL** (MDPI Drones, Jan 2026) | 分层角色 MARL（集群头+监控无人机） | 去中心化双级 PPO | 96.1% 定位成功率，87.3% 更低 RMSE，80% 更少通信开销 |
| **FOFE-MMAPPO** (ScienceDirect, 2026) | 灵活观测特征编码 + Mamba 记忆 | 处理多通道可变长度数据 | +10.1% 完成率，+14.8% 生存率，-21.5% 完成时间 |
| **STAGE** (Springer, 2026) | 时空注意力图增强策略 | 可学习动态邻接矩阵 + 双路径意图识别 | 4 类敌方战术分类 |
| **RALLY** (IEEE OJVT, 2025/2026) | LLM 驱动角色自适应导航 | RMIX 混合 LLM 先验 + MARL 在线策略 | 任务覆盖、收敛速度、泛化能力全面超越 |
| **DAFRL** (Sci. Reports, 2026) | 动态自适应平均场博弈 | 可学习异构权重 + 实时均衡跟踪 | 红蓝对抗实时均衡 |

---

### 4.2 技术趋势

| 趋势 | 说明 | 对 xmd_rl 的意义 |
|------|------|------------------|
| **通信-策略解耦** | SCALE-COMM + SCoUT 两条线独立验证了分离设计 | 预训练通信协议可复用 |
| **LLM + MARL 融合** | RALLY、Agent Q-Mix 展示 LLM 的语义推理价值 | 高层次任务理解的新路径 |
| **异构角色架构** | HMUDRL、CASA、CFR-MARL 全部采用角色分工 | 集群中不同无人机应扮演不同角色 |
| **物理信道感知** | CLOVER 首次纳入真实无线信道模型 | 指导 PX4 实际通信协议 |
| **灵活观测编码** | FOFE + Mamba 解决变长异构输入 | 异构传感器配置的关键技术 |

---

## 5. 无人机飞行控制

### 5.1 重要论文

#### 5.1.1 RAPTOR: A Foundation Policy for Quadrotor Control

- **作者：** UC Berkeley, Technology Innovation Institute (UAE)
- **发表：** arXiv 2509.11481 (v2: 2026-04-06)
- **链接：** https://arxiv.org/abs/2509.11481

**摘要：** 这是本周最引人注目的无人机控制论文。RAPTOR 训练了一个仅 **2,084 个参数**的循环神经网络策略，通过元模仿学习（Meta-Imitation Learning）蒸馏 1,000 个教师策略，实现了**零样本适配 10 种不同真实四旋翼**——从 32g 微型无人机到 2.4kg 大型平台，涵盖有刷/无刷电机、软/硬机架、4 种螺旋桨类型。测试场景包括室外风和物理敲击扰动。策略在毫秒级内完成上下文自适应，**已开源**。

**关键技术贡献：**
1. 首个四旋翼基础策略（Foundation Policy），规模仅 2,084 参数
2. 元模仿学习蒸馏 1,000 个教师策略
3. 零样本适配 10 种不同硬件平台（32g–2.4kg）
4. 毫秒级在线自适应，无需微调
5. 完全开源

**与本课题关联：** ⭐⭐⭐⭐⭐ — RAPTOR 的 Foundation Policy 范式是 xmd_rl 的理想目标形态。xmd_rl 当前训练单一四旋翼的策略，未来可参考 RAPTOR 的思路向多平台泛化方向发展。该论文的开源代码值得仔细研读。

---

#### 5.1.2 Learning Agile Gate Traversal via Analytical Optimal Policy Gradient

- **作者：** National University of Singapore
- **发表：** arXiv 2508.21592 (v3: 2026-03-04)
- **链接：** https://arxiv.org/html/2508.21592v3

**摘要：** 提出了一个全可微分 NN-MPC 混合框架。神经网络在线自适应微调 MPC 的代价权重和参考姿态，使用**解析策略梯度**通过 MPC 和可微分门碰撞检测模块进行端到端训练。实现零样本 sim-to-real 迁移，在体轴角速率扰动 > 1146 deg/s 下 0.85 秒内恢复，峰值加速度 30 m/s²。

**与本课题关联：** ⭐⭐⭐⭐⭐ — NN-MPC 混合框架是当前无人机控制的前沿范式，xmd_rl 的 PX4 MPC 基础可直接受益。

---

#### 5.1.3 Adaptive Outer-Loop Control of Quadrotors via Reinforcement Learning

- **作者：** 预印本
- **发表：** arXiv 2605.16015 (2026-05-15)
- **链接：** https://export.arxiv.org/abs/2605.16015

**摘要：** **直接批判了标准域随机化（Domain Randomization）方法**，认为 DR 产生过于保守的策略。提出了一个自适应控制架构：残差动力学预测器（Residual Dynamics Predictor, RDP）在线估计扰动，线性校准桥（linear calibration bridge）连接仿真与现实。在 Crazyflie 微型四旋翼上验证了质量变化、非对称负载和动态吊挂负载下的性能。

**与本课题关联：** ⭐⭐⭐⭐⭐ — 对 DR 的批判与替代方案是本周 Sim-to-Real 领域最重要的讨论。RDP + 校准桥的组合优于纯 DR，xmd_rl 的 sim-to-real 管线应借鉴此思路。

---

#### 5.1.4 E2E-Fly: An Integrated Training-to-Deployment System for End-to-End Quadrotor Autonomy

- **作者：** Shanghai Jiao Tong University
- **发表：** arXiv 2604.12916 (2026-04-14)
- **链接：** https://arxiv.org/html/2604.12916v1

**摘要：** 一个完整的全栈平台，统一了可微分物理学习 + RL 与 sim-to-real 对齐（系统辨识、延迟补偿、域随机化、噪声建模）、sim-to-sim + HIL 验证，以及双硬件部署。在 6 个端到端控制任务中部署到真实硬件。

**与本课题关联：** ⭐⭐⭐⭐ — E2E-Fly 的全栈 pipeline 设计可作为 xmd_rl 训练-部署流程的参考架构。

---

#### 5.1.5 Learning Agile Quadrotor Flight in the Real World

- **作者：** University of Zurich (RPG Lab)
- **发表：** arXiv 2602.10111 (2026-02-10)
- **链接：** https://arxiv.org/html/2602.10111v1

**摘要：** 自适应性框架：自适应时间缩放（Adaptive Temporal Scaling, ATS）实现安全探索 + 在线残差学习 + RASH-BPTT 用于真实世界的策略更新。在约 100 秒的飞行时间内，峰值速度从 1.9 m/s 进化到 7.3 m/s；在有风干扰下任务完成速度加快 42%。

**与本课题关联：** ⭐⭐⭐⭐⭐ — UZH RPG Lab 是无人机 RL 领域的顶级实验室。ATS 安全探索机制和在线残差学习可直接指导 xmd_rl 的真实飞行实验。

---

### 5.2 技术趋势

| 趋势 | 说明 |
|------|------|
| **Foundation Policy** | RAPTOR 证明了小参数量的通用四旋翼策略是可行的 |
| **NN-MPC 混合** | 解析策略梯度 + 可微分 MPC 成为新的标准范式 |
| **DR 批判与替代** | 域随机化被认为过于保守，自适应校准方法兴起 |
| **全栈平台** | 从训练到部署的一体化系统（E2E-Fly）成为新方向 |
| **在线真实世界学习** | UZH 框架在真实环境中持续进化策略 |

---

## 6. 无人机集群

### 6.1 重要论文

#### 6.1.1 FLIP: Real-Time and Resilient Formation Planning for Large-Scale Distributed Swarms

- **作者：** 预印本
- **发表：** arXiv 2605.29704 (2026-05-28)
- **链接：** https://arxiv.org/abs/2605.29704

**摘要：** 将编队规划转化为**时空点云配准（Spatiotemporal Point Cloud Registration）**问题。支持 120 架无人机的弹性分布式规划，具有异常值拒绝能力，与 SOTA 方法进行了基准对比并全面超越。关键创新：将编队形状维护视为点云在时空中的配准问题，使得每架无人机只需要本地邻域信息即可实现全局一致的编队行为。

**与本课题关联：** ⭐⭐⭐⭐ — 点云配准视角提供了全新的编队控制数学框架。120 架规模的实际可部署性对大规模集群仿真有重要参考价值。

---

#### 6.1.2 UATG: Optimal Allocation and Trajectories for Swarm Drone Formations (1008 Drones)

- **作者：** Yunes ALQUDSI
- **发表：** arXiv 2603.24401 (2026-03-25)
- **链接：** https://arxiv.org/html/2603.24401

**摘要：** 提出统一分配与轨迹生成（UATG）框架，**同时求解最优无人机-航点分配和动态可行、无碰撞轨迹生成**。在标准笔记本电脑上协调 **1,008 架无人机约 1 秒**。这是目前文献中最大规模的实时编队规划方案。

**与本课题关联：** ⭐⭐⭐ — 大规模编队规划的工程实现参考。1008 架的实时规划能力证明了算法效率的极限。

---

#### 6.1.3 ROS 2 + PX4 Modular Architecture for Heterogeneous UAV Swarms

- **作者：** Pommeranz et al.
- **发表：** arXiv 2510.27327, ICMRE 2026 (2026-03-02)
- **链接：** https://arxiv.org/abs/2510.27327

**摘要：** 提出了一个**模块化 ROS 2 + PX4 架构**用于异构无人机集群。支持 Leader-Following 和编队飞行、Docker 容器化部署、地面站控制。这个系统架构设计直接面向实际部署，与 xmd_rl 和 spear_ws 的技术栈高度匹配。

**与本课题关联：** ⭐⭐⭐⭐⭐ — **与 xmd_rl（Isaac Lab/RSL-RL）+ spear_ws（ROS2）+ PX4 的技术栈完全对齐**。该论文的模块化设计模式和 Docker 化方案可直接参考用于 xmd_rl 的多机扩展。

---

### 6.2 集群控制技术对比

| 技术 | 最大规模 | 通信需求 | 实时性 | 主要平台 |
|------|----------|----------|--------|----------|
| UATG (2026) | 1,008 架 | 集中式 | ~1s 求解 | 笔记本 |
| FLIP (2026) | 120 架 | 分布式（本地邻域） | 实时 | 分布式 |
| ROS2+PX4 (2026) | 未明确 | 混合（Leader-Follower） | 实时 | Docker |
| Virtual Centroid Flocking (2026) | 可变规模 | 低（虚拟中心） | 实时 | 仿真+真实 |
| NN Adaptive Formation (2026) | 小规模 | 低（去中心化） | 实时 | 仿真 |

---

## 7. 空地协同

### 7.1 重要论文

#### 7.1.1 Energy-Aware Collaborative Exploration for a UAV-UGV Team

- **作者：** 预印本
- **发表：** arXiv 2603.22507 (2026-03-23)
- **链接：** https://arxiv.org/html/2603.22507v1

**摘要：** 提出一个框架，其中**无人机和地面车同时主动探索**，地面车同时作为无人机的**移动充电站**。使用密度感知的分层概率路线图（PRM），并将巡回选择形式化为**耦合定向问题（Coupled Orienteering Problems）**，在共享飞行时间预算下求解。经过真实实验验证。这是首次将能量约束与协同探索进行联合优化的完整框架。

**与本课题关联：** ⭐⭐⭐⭐⭐ — 能量管理是空地协同最核心的实际约束之一。移动充电站 + 耦合定向问题的形式化为 xmd_rl 的空地协同扩展提供了现成的数学框架。

---

#### 7.1.2 AirSimAG: A High-Fidelity Simulation Platform for Air-Ground Collaborative Robotics

- **作者：** 预印本
- **发表：** arXiv 2603.23079 (2026-03-24)
- **链接：** https://arxiv.org/abs/2603.23079

**摘要：** 一个基于定制 AirSim 框架的新仿真平台，**专门为 UAV-UGV 协同仿真**而构建。支持同步多智能体仿真、异构感知/控制接口，并附带内置基准任务（建图、规划、跟踪、编队、探索）。填补了空地协同领域缺乏专用仿真平台的空白。

**与本课题关联：** ⭐⭐⭐⭐ — 如果 xmd_rl 未来向空地协同方向扩展，AirSimAG 是值得关注的仿真平台选项。需评估其与 Isaac Lab 的互补性。

---

#### 7.1.3 Learning-Accelerated Optimization-based Trajectory Planning for Cooperative Aerial-Ground Handover Missions

- **作者：** 预印本, RoManSy 2026
- **发表：** arXiv 2605.19562 (2026-05-19)
- **链接：** https://arxiv.org/abs/2605.19562

**摘要：** 使用 **LSTM 编码器-解码器网络**作为神经代理规划器，为 UAV-UGV 交接任务中的集中式轨迹优化生成热启动（warm start）。相比冷启动方法，实现了 **>3 倍加速**和 **100% 优化成功率**。

**与本课题关联：** ⭐⭐⭐⭐ — 神经代理规划器 + 优化精炼的两阶段范式是当前轨迹规划的前沿方法，与 Learning Agile Gate Traversal 的 NN-MPC 混合框架异曲同工。

---

#### 7.1.4 SLEI3D: Simultaneous Exploration and Inspection via Heterogeneous Fleets under Limited Communication

- **作者：** 预印本
- **发表：** arXiv 2601.00163 (2026-01-01)
- **链接：** https://arxiv.org/abs/2601.00163

**摘要：** 48 台异构机器人在有限通信下的同时探索与检查。不同机器人搭载不同传感器（远程 LiDAR 探索、近距离相机检查），仅在物理接近时通过 ad-hoc 无线通信交换信息，并向移动地面控制站实时回传数据。在仿真中验证至 48 台机器人，硬件验证 7 台。

**与本课题关联：** ⭐⭐⭐ — 大规模异构团队的通信约束管理值得借鉴。

---

### 7.2 技术趋势

| 趋势 | 说明 |
|------|------|
| **能量感知协同** | 移动充电 + 协同探索联合优化 |
| **神经代理优化加速** | LSTM 代理规划器为优化提供热启动 |
| **专用仿真平台** | AirSimAG 填补空地协同仿真空白 |
| **UAV 部署微型 UGV** | MiniUGV2 开启"空中投送地面机器人"新场景 |
| **磁感应自主对接** | 5cm RMSE 的 GPS-free 对接技术 |

---

## 8. 交叉主题

### 8.1 Sim-to-Real 迁移

**本周核心讨论：域随机化（DR）是否已经过时？**

两篇重要论文正面挑战了 DR 的主导地位：

1. **Adaptive Outer-Loop Control (2605.16015)**：明确指出 DR 产生"过于保守"的策略。提出 RDP（残差动力学预测器）+ 线性校准桥的替代方案。

2. **Vision-Guided Outdoor Flight (2605.24449)**：RA-L/ICRA 2026 论文，使用两阶段 RL（privileged learning + 域随机化）实现零样本室外迁移——说明 DR 仍有用武之地，但需要与其他技术组合。

3. **Curriculum RL Racing (2602.24030)**：多阶段课程学习 + DR + 多场景更新策略的组合方案。

**结论：** DR 正在从"唯一方案"转变为"组合方案中的一环"。2026 年 Sim-to-Real 的主流是将 DR 与系统辨识、自适应校准、课程学习相结合。

### 8.2 安全强化学习

**本周最活跃的交叉方向**，主要突破：

| 论文 | 方法 | 创新点 |
|------|------|--------|
| **PECTS (2604.06463)** | CBF 约束 MPC + PNN 动力学 | 安全轨迹采样机制，丢弃不安全 rollout |
| **Koopman CBF (2605.26452)** | Koopman 算子 + SAC + QP 安全层 | 有限维线性提升空间中的仿射 CBF |
| **CAPSULE (2604.23576)** | 概率控制仿射动力学 + CBF | 模型不确定性显式纳入 CBF 约束 |
| **Non-Greedy CBFs (2602.00366)** | 两阶段 RL 学习非贪婪 CBF | 12-25% 燃料节省 |
| **Explicit CBF Filters (2512.10118)** | 闭式 CBF-QP + 事件触发 | 大幅降低在线计算量 |

**关键趋势：**
- CBF 从手工设计 → 数据驱动学习
- 从确定性 → 概率性（显式建模不确定性）
- 从每步求解 → 事件触发（仅在必要时计算）
- Koopman 算子为非线性系统提供线性 CBF 表示

**与本课题关联：** ⭐⭐⭐⭐⭐ — 安全 RL 是 xmd_rl 向实际飞行推进的必经之路。Koopman CBF + SAC 和 CAPSULE 的概率安全框架都值得深入跟进。

### 8.3 仿真平台

| 平台 | 版本/状态 | 关键更新 |
|------|-----------|----------|
| **Isaac Lab** | v2.3.2（稳定）/ v3.0.0-beta | v2.3.2: 原生多旋翼支持（多旋翼执行器、资产、RL 任务）；v3.0: 架构重构中 |
| **OmniDrones** | 活跃开发 | 专用无人机 RL 框架（TorchRL + Hydra + WandB） |
| **PX4 Autopilot** | v1.17.0-rc2 | 新飞控硬件支持、CVE 安全修复、Synthetic Rover 模型 |
| **AirSimAG** | 新发布（2026-03） | 首个空地协同专用仿真平台 |
| **VisFly** | 活跃维护 | SJTU 视觉飞行仿真器（10,000+ FPS） |
| **E2E-Fly** | 新发布（2026-04） | 全栈训练到部署系统 |

**与本课题关联：** Isaac Lab v2.3.2 的原生多旋翼支持对 xmd_rl 是重大利好——意味着不再需要自行实现多旋翼模型。建议尽快评估迁移。

---

## 9. 开源项目动态

### 9.1 热门项目

| 项目 | Stars | 本周动态 | 与 xmd_rl 相关度 |
|------|-------|----------|-------------------|
| **RAPTOR** (UC Berkeley) | 新发布 | Foundation Policy 开源，2,084 参数 | ⭐⭐⭐⭐⭐ |
| **ACMPC** (UZH RPG) | 活跃 | Actor-Critic + 可微分 MPC，无人机竞速 SOTA | ⭐⭐⭐⭐⭐ |
| **VisFly** (SJTU) | 活跃 | 视觉飞行仿真器，10,000+ FPS | ⭐⭐⭐⭐ |
| **GraphMTSAC** | 活跃 | 多任务 GCN + SAC，Pixhawk 400Hz 部署 | ⭐⭐⭐⭐⭐ |
| **xAdapt_Ctrl** (UC Berkeley) | 活跃 | 极端参数自适应控制器（16× 范围） | ⭐⭐⭐⭐ |
| **Multi-Drone RL** | 活跃 | 去中心化 PPO 多机竞速（13.65 m/s） | ⭐⭐⭐⭐ |
| **MSACL** | 新发布 | 李雅普诺夫稳定 RL 模块化框架 | ⭐⭐⭐ |
| **ABPT** | 即将发布 | 可微分奖励 BPTT，四旋翼控制 | ⭐⭐⭐⭐ |

### 9.2 平台与工具更新

| 工具 | 更新 |
|------|------|
| **Isaac Lab v2.3.2** | 多旋翼原生支持（thruster actuator + drone asset + RL task） |
| **Isaac Lab v3.0.0-beta** | 架构重构中，建议观望 |
| **PX4 v1.17.0-rc2** | 新硬件支持，CVE 修复，即将 stable |
| **OmniDrones** | TorchRL 集成，6 类 RL 环境 |

---

## 10. 本周总结与展望

### 10.1 关键进展

1. **Foundation Policy 时代开启：** RAPTOR（2,084 参数）证明了通用四旋翼基础策略的可行性，这对整个无人机 RL 领域的方法论有深远影响。

2. **Sim-to-Real 方法论转向：** 域随机化（DR）从唯一方案降级为组合方案中的一环，自适应校准和残差学习正在成为新的标准组件。

3. **安全 RL 大爆发：** Koopman CBF + SAC、概率 CBF、事件触发 CBF 滤波器——安全 RL 的工具箱在 2026 年上半年得到了极大丰富。

4. **MARL 通信范式变革：** 通信-策略解耦（SCALE-COMM）+ 时间分组通信（SCoUT）+ 物理信道感知（CLOVER）三条线同步推进，MARL 通信正在走向实用化。

5. **空地协同从概念走向系统：** 能量感知探索、UAV 部署微型 UGV、磁感应自主对接——空地协同从框架概念进入系统工程阶段。

### 10.2 建议关注方向

| 方向 | 优先级 | 理由 |
|------|--------|------|
| RAPTOR Foundation Policy 范式 | **最高** | 可能重新定义无人机 RL 的研究范式 |
| Sim-to-Real：DR + 自适应校准组合 | **最高** | 直接影响 xmd_rl 的迁移管线设计 |
| Koopman CBF 安全滤波 | **高** | 轻量级安全保证，适合嵌入实际飞控 |
| 通信-策略解耦 MARL | **高** | 预训练通信协议 → 真实集群复用 |
| 多分辨率分层 RL (MRS) | **高** | 首次达到与平面 RL 相当的性能 |
| LLM + MARL 角色自适应 | **中** | 值得跟踪但技术成熟度尚低 |
| 空地协同能量感知 | **中** | 长期扩展方向 |

### 10.3 下周关注点

- **RAPTOR 代码深入分析**：评估 Foundation Policy 在 xmd_rl 环境中的可复现性
- **Isaac Lab v2.3.2 多旋翼支持迁移**：评估从自定义四旋翼模型迁移到官方多旋翼资产的成本
- **PX4 v1.17.0 正式版**：关注 RC2 后的正式发布和与 xmd_rl 的兼容性
- **NeurIPS 2026 论文评审**：投稿已截止（5月6日），关注 arXiv 上可能出现的新投稿预印本

---

## 11. 研究启发与选题分析

### 11.1 研究趋势洞察

| 趋势 | 驱动力 | 潜力评估 |
|------|--------|----------|
| **Foundation Policy 四旋翼** | 大规模预训练 + 元学习的成功迁移 | 🔥🔥🔥🔥🔥 即将爆发 |
| **CBF + RL 深度融合** | 无人机安全飞行的刚性需求 | 🔥🔥🔥🔥🔥 刚需，理论趋于成熟 |
| **MARL 通信-策略解耦** | 真实通信约束下的可部署性 | 🔥🔥🔥🔥 稳步增长 |
| **HRL 多分辨率技能** | MRS 首次实现与平面 RL 持平 | 🔥🔥🔥🔥 突破临界点 |
| **LLM + MARL** | 大模型语义理解 + 集群协调 | 🔥🔥🔥 新兴方向 |

**关键判断：** RAPTOR 证明了 Foundation Policy 在无人机上的可行性，这可能会像当年在 NLP 和 CV 领域一样，重新定义四旋翼 RL 的研究范式。预计未来 6-12 个月会出现大量的 Foundation Policy 变体和改进工作。**在这个范式转换的早期阶段入场是最佳时机。**

---

### 11.2 潜在研究 Idea

#### Idea 1: Foundation Skill Policy for Quadrotor — 基于 MRS + RAPTOR 的多分辨率技能基础策略

- **切入点：** RAPTOR 的 Foundation Policy（单一通用策略）+ MRS 的多分辨率技能（多时间尺度）。
- **核心思路：** 在 Isaac Lab 中训练一个多分辨率技能基础策略，同时具备：① 跨平台泛化能力（RAPTOR 范式）；② 分层技能组织（MRS 框架）。低级技能（悬停、姿态控制）共享基础表征，高级技能（轨迹跟踪、避障、视觉导航）通过元控制器动态组合。训练完成后，对未见过的四旋翼平台和新任务实现零样本或少样本迁移。
- **创新点：**
  1. 首次将 Foundation Policy 范式与多分辨率 HRL 结合
  2. 技能层级使泛化更有结构——泛化的是"技能"层面的组合方式，而非单一策略
  3. 元模仿学习蒸馏多平台的教师策略到统一的多分辨率策略
- **预期贡献：** 将 RAPTOR 的单策略扩展到多分辨率技能组合，实现更复杂的任务泛化
- **目标会议/期刊：** CoRL 2027 / ICRA 2027 / RA-L
- **实现难度：** ⭐⭐⭐⭐ (4/5)
- **可行性分析：** xmd_rl 已有 Isaac Lab 四旋翼环境和 RSL-RL 训练管线。核心工作为：① 实现 MRS 的多分辨率目标预测模块；② 在多种四旋翼配置上训练教师策略；③ 蒸馏到统一的基础策略。预估 2-3 人月。

---

#### Idea 2: Koopman-CBF Safety Filter for Quadrotor RL — 面向四旋翼强化学习的 Koopman 安全滤波

- **切入点：** Koopman CBF (2605.26452) + Adaptive Outer-Loop Control (2605.16015) + xmd_rl 的 PX4 接口。
- **核心思路：** 将 Koopman CBF 安全滤波集成到 xmd_rl 的四旋翼 RL 训练和部署流程中。在 Isaac Lab 中学习四旋翼动力学的 Koopman 算子提升（lifted linear dynamics），在提升空间中构造仿射 CBF 约束，通过 QP 安全层对 RL 策略的输出动作进行修正。安全层运行在 PX4 的 offboard 控制回路中（< 5ms），不会引入显著的延迟。
- **创新点：**
  1. 首个面向四旋翼的 Koopman CBF + RL 安全框架
  2. 在 Koopman 提升空间中构造 CBF，克服四旋翼非线性的困难
  3. 安全层与 PX4 offboard 控制回路直接集成
  4. 事件触发机制降低在线 QP 求解频率（参考 Explicit CBF Filters）
- **预期贡献：** 在保证安全的前提下最大化四旋翼 RL 策略的激进程度（aggressiveness），解决 Sim-to-Real 中最棘手的安全验证问题
- **目标会议/期刊：** ICRA 2027 / RA-L / IROS 2027
- **实现难度：** ⭐⭐⭐⭐ (4/5)
- **可行性分析：** xmd_rl 已有 Isaac Lab 环境 + PX4 SITL 接口。Koopman 算子学习需要额外的系统辨识步骤，但已有成熟工具（pyKoopman 等）。关键难点在于：① 四旋翼 12 维状态空间的 Koopman 提升维度控制；② QP 求解器的实时性验证。预估 2-3 人月。

---

#### Idea 3: Decoupled Communication Pretraining for UAV Swarm Coordination

- **切入点：** SCALE-COMM 的通信-策略解耦 + SCoUT 的时间分组通信 + xmd_rl 的多机扩展。
- **核心思路：** 在 Isaac Lab 多四旋翼环境中，使用自监督对比学习预训练通信协议（独立于具体任务策略），然后在不同集群任务（编队、搜索、追捕）上复用该协议。通信协议训练阶段使用仿真中不受限的"全连接"信息，但学到的协议在部署时仅需稀疏的物理层通信（MAVLink）。
- **创新点：**
  1. 首次将通信-策略解耦应用于四旋翼集群
  2. 预训练通信协议跨任务复用——一次训练，多任务复用
  3. 仿真全信息 → 真实稀疏通信的压缩映射
- **预期贡献：** 显著降低集群 MARL 的通信学习难度，使预训练协议成为集群的基础设施
- **目标会议/期刊：** AAMAS 2027 / IROS 2027 / DARS 2026
- **实现难度：** ⭐⭐⭐ (3/5)
- **可行性分析：** 通信协议预训练不依赖特定 RL 算法，风险可控。主要工作量为：① 多四旋翼对比学习环境的搭建；② 通信压缩映射的设计；③ 多任务的验证。预估 1.5-2 人月。

---

#### Idea 4: Energy-Aware Hierarchical RL for Air-Ground Cooperative Inspection

- **切入点：** Energy-Aware Exploration (2603.22507) + MRS 多分辨率 HRL + AirSimAG 仿真平台。
- **核心思路：** 将空地协同巡检形式化为一个分层 RL 问题：高层（无人机）负责全局巡检路径规划和能量预算管理，中层（地面车）负责移动充电调度和精细检查，低层（各自的控制器）负责轨迹跟踪。使用耦合定向问题（OP）的形式化来协调两层之间的能量约束。
- **创新点：**
  1. 首次将能量感知与分层 RL 结合用于空地协同
  2. 高空-中充-低检三层架构清晰分工
  3. 耦合定向问题的 RL 求解方案
- **预期贡献：** 提出一个理论上严谨、工程上可实现的空地协同巡检框架
- **目标会议/期刊：** ICRA 2027 / RA-L / IEEE T-RO
- **实现难度：** ⭐⭐⭐⭐⭐ (5/5)
- **可行性分析：** 这是长期方向。需要先完成 Idea 1-3 的基础积累，再进行系统集成。AirSimAG 平台需要额外搭建。预估 4-6 人月。

---

### 11.3 本周最值得关注的方向

**Idea 1: Foundation Skill Policy for Quadrotor**

**理由：**
1. **范式转换窗口：** RAPTOR 刚证明 Foundation Policy 可行，MRS 刚证明多分辨率 HRL 可与平面 RL 匹敌——在两个突破的交汇点做工作是黄金时机
2. **与 xmd_rl 高度契合：** 项目的 Isaac Lab + RSL-RL 技术栈恰好适合做 Foundation Policy 的大规模并行训练
3. **故事线完整：** 从技能层级 → 多平台泛化 → 多任务组合，逻辑闭环
4. **开源价值高：** 如果做成，将是首个四旋翼 Foundation Skill Policy，有较高的社区影响力
5. **难度适中：** 核心技术模块（MRS、蒸馏）都是已知方法，主要挑战在整合和调优

**与 xmd_rl 项目结合路径：**
```
当前 xmd_rl 项目 → 单四旋翼单任务 SAC/PPO
                    ↓ 第一步（Idea 1）
         多分辨率技能 + 多平台蒸馏
                    ↓ 第二步（Idea 2）
          + Koopman CBF 安全滤波
                    ↓ 第三步（Idea 3）
          + 多机通信协议预训练
                    ↓ 远期（Idea 4）
          + 空地协同能量感知
```

**建议的下一步行动：**
1. **本周：** 深入研读 RAPTOR 开源代码和 MRS 论文
2. **下周：** 在 xmd_rl 的 Isaac Lab 环境中搭建多四旋翼配置（不同质量、尺寸、电机参数）
3. **第 3-4 周：** 实现 MRS 的多分辨率目标预测模块
4. **第 5-8 周：** 训练多平台的教师策略并蒸馏

---

### 11.4 研究时间线建议

#### 短期（1-2 周）：快速验证

| 任务 | 目标 | 产出 |
|------|------|------|
| RAPTOR 代码复现 | 在 Isaac Lab 中跑通 RAPTOR 的元模仿学习流程 | 可运行的代码 |
| 多四旋翼环境搭建 | 3-5 种不同参数的四旋翼模型 | ISAAC 环境配置 |
| 文献调研 | 系统阅读 Foundation Policy + MRS + Koopman CBF 的核心论文 | 文献综述 |

#### 中期（1-3 月）：核心工作

| 任务 | 目标 | 产出 |
|------|------|------|
| MRS 技能发现 | 在四旋翼任务上实现多分辨率技能发现 | 技能库 |
| 多平台蒸馏 | 蒸馏 50+ 教师策略到统一基础策略 | Foundation Skill Policy checkpoint |
| Koopman 系统辨识 | 学习四旋翼的 Koopman 提升模型 | Koopman 模型 |
| 安全滤波集成 | QP 安全层与策略的联合测试 | 安全验证数据 |

#### 长期（3-6 月）：论文产出

| 任务 | 目标 | 产出 |
|------|------|------|
| 消融实验 | 验证 Foundation Skill Policy 各组件贡献 | 实验数据 |
| Sim-to-Real | 在真实四旋翼上验证安全滤波和策略迁移 | 飞行视频 + 数据 |
| 论文撰写 | 投稿 CoRL 2027 或 ICRA 2027 | 论文初稿 |
| 代码整理 | 开源 Foundation Skill Policy | GitHub 仓库 |

---

## 12. 附录

### A. 本周论文总列表

| 序号 | 标题 | 出版 | 领域 |
|------|------|------|------|
| 1 | AdaGamma: State-Dependent Discounting for RL | arXiv 2605.06149 | RL 算法 |
| 2 | Multi-Step First: PPO under Partial Observability | Neural Networks 2026 | RL 算法 |
| 3 | Simplicial Embeddings for Sample Efficiency | arXiv 2510.13704 | RL 算法 |
| 4 | RLScale-Bench: When Does Deep RL Beat Baselines? | arXiv 2605.26418 | RL 算法 |
| 5 | Multi-Resolution Skills for HRL (MRS) | arXiv 2505.21410 | 分层 RL |
| 6 | CARL: Contrastive Action Representations for Offline HRL | arXiv 2605.26371 | 分层 RL |
| 7 | SUSD: Structured Unsupervised Skill Discovery | arXiv 2602.01619 | 分层 RL |
| 8 | Unsupervised Hierarchical Skill Discovery (Grammar-based) | arXiv 2601.23156 | 分层 RL |
| 9 | Partner-Aware Hierarchical Skill Discovery (PASD) | arXiv 2605.24352 | 分层 RL |
| 10 | SCALE-COMM: Latent Embeddings for MARL Communication | arXiv 2605.27532 | 多智能体 RL |
| 11 | SCoUT: Scalable Communication via Temporal Grouping | arXiv 2603.04833 | 多智能体 RL |
| 12 | CLOVER: Wireless-Enhanced Value Decomposition | arXiv 2604.08728 | 多智能体 RL |
| 13 | Co2PO: Coordinated Constrained Policy Optimization | arXiv 2602.02970 | 多智能体 RL |
| 14 | Quantum Entanglement for MARL Coordination | arXiv 2602.08965 | 多智能体 RL |
| 15 | STAGE: Spatio-Temporal Attention GNN for UAV Swarm | Springer 2026 | 多智能体 + 集群 |
| 16 | FOFE-MMAPPO: Flexible Encoding for Heterogeneous UAVs | ScienceDirect 2026 | 多智能体 + 集群 |
| 17 | RALLY: LLM-Driven Role-Adaptive UAV Swarm | IEEE OJVT 2026 | 多智能体 + LLM |
| 18 | DAFRL: Dynamic Adaptive Mean Field RL | Sci. Reports 2026 | 多智能体 |
| 19 | RAPTOR: Foundation Policy for Quadrotor Control | arXiv 2509.11481 | 无人机控制 |
| 20 | Learning Agile Gate Traversal (NN-MPC) | arXiv 2508.21592 | 无人机控制 |
| 21 | Adaptive Outer-Loop Control (RDP + Calibration) | arXiv 2605.16015 | 无人机控制 + Sim-to-Real |
| 22 | E2E-Fly: Training-to-Deployment System | arXiv 2604.12916 | 无人机控制 |
| 23 | Learning Agile Quadrotor Flight in Real World | arXiv 2602.10111 | 无人机控制 |
| 24 | Vision-Guided Outdoor Flight (RA-L/ICRA 2026) | arXiv 2605.24449 | 无人机控制 + Sim-to-Real |
| 25 | FLARE: Agile Flights with Cable-Suspended Payload | arXiv 2508.09797 | 无人机控制 |
| 26 | FLIP: 120-Drone Formation via Point Cloud Registration | arXiv 2605.29704 | 无人机集群 |
| 27 | UATG: 1008-Drone Light Show Optimization | arXiv 2603.24401 | 无人机集群 |
| 28 | ROS2 + PX4 Modular Architecture for Swarms | arXiv 2510.27327 | 无人机集群 |
| 29 | Adaptive NN Formation Control under Uncertainty | arXiv 2503.13688 | 无人机集群 |
| 30 | Energy-Aware Collaborative Exploration (UAV-UGV) | arXiv 2603.22507 | 空地协同 |
| 31 | AirSimAG: Air-Ground Simulation Platform | arXiv 2603.23079 | 空地协同 |
| 32 | Learning-Accelerated Aerial-Ground Handover Planning | arXiv 2605.19562 | 空地协同 |
| 33 | SLEI3D: Heterogeneous Fleet Exploration (48 robots) | arXiv 2601.00163 | 空地协同 |
| 34 | MiniUGV2: UAV-Deployable Tracked Ground Vehicle | arXiv 2603.00972 | 空地协同 |
| 35 | Fly, Track, Land: Magnetic Localization for UAV-UGV | arXiv 2603.08926 | 空地协同 |
| 36 | PECTS: CBF-Constrained MPC for Safe RL | arXiv 2604.06463 | 安全 RL |
| 37 | Koopman CBF Filters for Safe Actor-Critic RL | arXiv 2605.26452 | 安全 RL |
| 38 | CAPSULE: Safe Uncertainty-Aware RL | arXiv 2604.23576 | 安全 RL |
| 39 | Non-Greedy CBFs via Two-Stage RL | arXiv 2602.00366 | 安全 RL |
| 40 | Safe Policy Optimization via CBF Safety Filters | arXiv 2604.01392 | 安全 RL |

### B. 相关会议时间

| 会议 | 投稿截止 | 会议时间 | 状态 |
|------|----------|----------|------|
| **NeurIPS 2026** | 2026-05-06 (已截止) | 2026-12-06 (Sydney) | 评审中 |
| **ICLR 2027** | ~2026-09-24 (预计) | 2027-04-24 (预计) | 准备投稿 |
| **ICRA 2027** | ~2026-09-15 (预计) | 2027-05/06 (预计) | 准备投稿 |
| **CoRL 2027** | ~2027-03 (预计) | 2027-11 (预计) | 远期目标 |
| **AAMAS 2027** | ~2026-10 (预计) | 2027-05 (预计) | 准备投稿 |
| **IROS 2027** | ~2027-02 (预计) | 2027-10 (预计) | 远期目标 |

### C. 推荐阅读（本周梳理的必读论文 Top 10）

1. **RAPTOR (2509.11481)** — Foundation Policy 范式开创，必读
2. **MRS (2505.21410)** — 多分辨率 HRL 突破，必读
3. **Koopman CBF (2605.26452)** — 安全 RL 新范式，必读
4. **SCALE-COMM (2605.27532)** — MARL 通信解耦，必读
5. **Adaptive Outer-Loop (2605.16015)** — Sim-to-Real 新方向，必读
6. **Learning Agile Quadrotor Flight (2602.10111)** — 真实世界在线学习，必读
7. **Energy-Aware Exploration (2603.22507)** — 空地协同能量管理，推荐
8. **ROS2+PX4 Swarm Architecture (2510.27327)** — 工程实践参考，推荐
9. **AdaGamma (2605.06149)** — 状态依赖折扣因子，推荐
10. **FLIP (2605.29704)** — 大规模编队新框架，推荐

---

**报告生成时间：** 2026-06-05
**搜索次数：** 13 次 WebSearch + 0 次 WebFetch (arxiv.org 受限)
**论文覆盖：** 40 篇重要论文
**报告长度：** ~12,000 字

---

> **备注：** 本报告中的论文信息均来自 WebSearch 搜索结果中的 arXiv 列表和摘要信息。由于 arxiv.org 的 WebFetch 受网络限制，部分论文的完整摘要未能进一步验证。建议读者点击链接获取完整论文内容。
