# 每日科研热点追踪报告

**生成日期：** 2026-05-27
**时间范围：** 2026-05-20 ~ 2026-05-27（最近一周）
**项目关联：** xmd_rl (四旋翼RL任务包) / PX4-Autopilot / Isaac Lab

---

## 目录

1. [领域概览](#1-领域概览)
2. [各领域详细报告](#2-各领域详细报告)
   - [2.1 强化学习算法](#21-强化学习算法)
   - [2.2 分层强化学习](#22-分层强化学习)
   - [2.3 多智能体强化学习](#23-多智能体强化学习)
   - [2.4 无人机飞行控制](#24-无人机飞行控制)
   - [2.5 无人机集群](#25-无人机集群)
   - [2.6 空地协同](#26-空地协同)
3. [交叉主题](#3-交叉主题)
4. [开源项目动态](#4-开源项目动态)
5. [总结与展望](#5-总结与展望)
6. [研究启发与选题分析](#6-研究启发与选题分析)
7. [附录](#7-附录)

---

## 1. 领域概览

### 本周热度评估

| 研究领域 | 热度 | 趋势 | 与本课题关联度 | 备注 |
|---------|------|------|:---:|------|
| 强化学习算法 | 🔥🔥🔥🔥🔥 | ↗️ | ⭐⭐⭐⭐ | PPO/SAC算法改进活跃，ETH提出SAC在IsaacLab上匹敌PPO |
| 分层强化学习 | 🔥🔥🔥🔥 | ↗️ | ⭐⭐⭐⭐⭐ | LLM辅助skill discovery、神经符号选项框架成为新热点 |
| 多智能体RL | 🔥🔥🔥🔥🔥 | ↗️ | ⭐⭐⭐⭐⭐ | LLM+MARL、通信感知MARL、图注意力架构集中爆发 |
| 无人机飞行控制 | 🔥🔥🔥🔥🔥 | ↗️ | ⭐⭐⭐⭐⭐ | Foundation Policy控制10种无人机、MPC+RL混合控制成趋势 |
| 无人机集群 | 🔥🔥🔥🔥 | ➡️ | ⭐⭐⭐⭐ | 自适应编队、分布式优化、事件触发控制持续活跃 |
| 空地协同 | 🔥🔥🔥🔥 | ↗️ | ⭐⭐⭐⭐⭐ | 学习+优化混合规划、基础设施无关定位、能耗感知探索 |

### 本周核心主题词云

**PPO↔SAC收敛 | Foundation Policy | LLM+MARL | Isaac Lab 3.0开源 | MPC+RL混合 | Sim-to-Real安全保障 | 通信感知MARL | 离线RL新范式**

---

## 2. 各领域详细报告

### 2.1 强化学习算法

#### 重要论文

---

**论文 1: Bridging the Gap: Enabling SAC for High Performance Legged Locomotion**

- **作者/机构：** ETH Zurich (RSL-RL团队)
- **发表平台：** arXiv:2605.24975 (Technical Report, 2026-05-24)
- **链接：** https://arxiv.org/html/2605.24975v1
- **代码：** 随RSL-RL-SAC开源发布

**摘要：**
ETH Zurich RSL-RL团队系统分析了为什么SAC在大规模并行仿真环境（如Isaac Lab/Isaac Gym）中长期表现不及PPO。通过识别三个关键瓶颈：策略初始化不当、超时感知的critic目标缺失、多步回报利用不足，该工作提出了一套简单但高效的修复方案。在7种不同的腿式机器人平台上验证，修复后的SAC完全弥合了与PPO的性能差距，甚至在某些任务上超越PPO。这项工作意味着"PPO是并行仿真训练唯一选择"的认知将被打破，拓宽了on-policy和off-policy算法在机器人学习中的选择空间。

**关键技术贡献：**
1. 系统性诊断SAC在massively parallel sim中的失败原因
2. 三修复方案：策略初始化 + timeout-aware critic + multi-step returns
3. 7平台上与PPO性能完全持平

**与本课题（xmd_rl）关联分析：** 🔴 **高关联** — 直接涉及IsaacLab平台上的RL训练。xmd_rl当前基于PPO训练四旋翼控制策略，如果能将SAC也引入训练流程，可在off-policy样本效率、exploration策略等方面获得更多选择。建议在xmd_rl中复现这套SAC改进方案，对比PPO和SAC在四旋翼飞行任务上的表现差异。

---

**论文 2: REFLEX: Reinforcement Learning with Reflection Symmetry Exploitation**

- **作者/机构：** (未公布)
- **发表平台：** arXiv:2605.23415 (2026-05-22)
- **链接：** https://export.arxiv.org/abs/2605.23415

**摘要：**
提出利用物理系统的反射对称性（轴向对称和双侧对称）来提升连续控制RL的样本效率。通过在PPO和SAC中集成对称性约束，策略网络能够自动利用环境中的对称结构，显著减少需要探索的状态-动作空间。在OpenAI Gym和DeepMind Control Suite基准测试上取得了一致的性能提升。

**关键技术贡献：**
1. 反射对称性的形式化建模（轴向 + 双侧）
2. 对称性约束与PPO/SAC的无缝集成
3. 连续控制基准上显著样本效率提升

**与本课题关联分析：** 🟡 **中关联** — 四旋翼飞行器具有天然的对称性结构（旋翼布局、机身几何），可以利用反射对称性进行数据增强或策略正则化，减少训练所需的环境交互步数。

---

**论文 3: TOPPO: Rethinking PPO for Multi-Task RL with Critic Balancing**

- **作者/机构：** (未公布)
- **发表平台：** arXiv:2605.11473 (2026-05-12)
- **链接：** https://arxiv.org/abs/2605.11473

**摘要：**
TOPPO (Tail-Optimized PPO) 针对多任务RL中PPO的critic侧梯度病态条件问题，提出了重新设计的critic平衡策略。在Meta-World+等多任务基准上，TOPPO以更少参数匹配甚至超越SAC基线，挑战了"多任务RL必须用off-policy算法"的传统认知。

**与本课题关联分析：** 🟡 **中关联** — xmd_rl未来有多任务扩展需求（如多姿态稳定、多轨迹跟踪），TOPPO提供了一种不依赖SAC的参数高效多任务PPO方案。

---

**论文 4: Approximate Next Policy Sampling (ANPS/SV-PPO)**

- **发表平台：** arXiv:2605.05481 (2026-05-06)
- **链接：** https://arxiv.org/abs/2605.05481

**摘要：**
提出通过修改训练分布而非约束策略更新来替换保守策略更新的新范式。SV-PPO在Atari和MuJoCo上匹配或超越PPO性能，同时支持更大的策略更新步长，意味着更快的训练收敛。

**与本课题关联分析：** 🟢 **低关联** — 算法改进偏理论，短期内对xmd_rl的直接影响有限，但值得关注其样本效率提升潜力。

---

**论文 5: AdaGamma: State-Dependent Discounting for Temporal Adaptation**

- **发表平台：** arXiv:2605.06149 (2026-05-07)
- **链接：** https://arxiv.org/abs/2605.06149

**摘要：**
学习状态依赖的折扣函数γ(s)，配合return-consistency正则化器防止TD-error崩溃。在SAC和PPO中均有效，在连续控制基准上取得提升，并在京东物流的真实A/B测试中验证。

**关键技术贡献：**
1. 状态依赖γ(s)代替全局固定γ
2. Return-consistency防止训练不稳定
3. 工业级验证（京东物流）

**与本课题关联分析：** 🟡 **中关联** — 四旋翼飞行的不同阶段（起飞、巡航、着陆、避障）可能需要不同的时间视野，AdaGamma可以在同一策略中自适应调整。

---

#### 技术趋势分析

| 趋势 | 描述 | 成熟度 |
|------|------|:---:|
| PPO↔SAC算法收敛 | 两种算法互相借鉴优势，在并行仿真中的性能差距正在消失 | 🟢 即将成熟 |
| PPO多任务扩展 | PPO通过critic平衡、tail optimization等技术拓展到多任务场景 | 🟡 快速发展 |
| 结构化先验注入RL | 对称性、折扣函数、动力学先验被形式化集成到RL算法中 | 🟡 快速发展 |
| 大规模LLM+RL | LLM智能体的RL训练（RLVR）成为独立研究方向 | 🔴 爆发期 |

---

### 2.2 分层强化学习

#### 重要论文

---

**论文 1: CODE-SHARP — Continuous Open-ended Discovery and Evolution of Skills as Hierarchical Reward Programs**

- **作者/机构：** Imperial College London & Sony Interactive Entertainment
- **发表平台：** arXiv:2602.10085 (最新修订 2026-05)
- **链接：** https://arxiv.org/html/2602.10085v3

**摘要：**
CODE-SHARP是一个利用基础模型开放式增长技能库的框架。每个技能被编码为Python函数形式的"SHARP"（Skills as Hierarchical Reward Programs），包含成功条件判断和一个依赖链（前置技能由之前发现的SHARP承担）。在Craftax-Classic上比基线高6倍，在XLand上高2.6倍，是唯一能打造铁器工具和开采钻石的智能体。在Craftax-Extended上零样本发现90+个SHARP，与使用真值奖励训练的智能体表现匹配。

**关键技术贡献：**
1. FM驱动的开放式技能发现（无需人工定义skill）
2. Python代码作为层次化奖励程序的可执行表示
3. 自动构建技能依赖图（前驱后继关系）
4. 零样本迁移到未见任务

**与本课题关联分析：** 🔴 **高关联** — 这是HRL+LLM方向的标杆性工作。无人机飞行是一系列层次化子任务（起降、悬停、轨迹跟踪、避障、着陆），CODE-SHARP的skill自动发现+组合范式可以直接应用于四旋翼操作技能库的构建。

---

**论文 2: PASD — Partner-Aware Skill Discovery for Human-AI Collaboration**

- **作者/机构：** Deakin University & Monash University
- **发表平台：** arXiv:2605.24352 (2026-05)
- **链接：** https://arxiv.org/html/2605.24352v1

**摘要：**
提出Partner-Aware Skill Discovery (PASD)，一种去中心化HRL框架。通过对比内在奖励将技能表示与相似合作伙伴对齐，学习以合作伙伴行为为条件的技能。在Overcooked-AI中与多样化合作伙伴群体和人类代理模型进行评估，一致优于基于群体和层次化的基线。

**与本课题关联分析：** 🟡 **中关联** — 无人机集群中个体需要感知队友状态调整行为，PASD的partner-aware机制可以用于多无人机协作的技能学习。

---

**论文 3: H²RL — Hybrid Hierarchical RL with Logical Options Pretraining**

- **发表平台：** arXiv:2603.06565 (2026-03)
- **链接：** https://arxiv.org/abs/2603.06565

**摘要：**
两阶段神经符号框架。第一阶段通过逻辑选项预训练注入符号结构，引导策略远离短视奖励循环导向目标导向行为；第二阶段通过标准环境交互进行微调。在长时域任务上一致优于纯神经网络、纯符号和神经符号基线。

**与本课题关联分析：** 🔴 **高关联** — 神经符号方法特别适合无人机飞行控制场景，因为飞行控制本身有明确的数学结构（动力学、稳定性条件），可以编码为逻辑选项。

---

**论文 4: AgentOWL — Joint Learning of Hierarchical Neural Options & Abstract World Model**

- **发表平台：** arXiv:2602.02799 (2026-02)
- **链接：** https://arxiv.org/abs/2602.02799

**摘要：**
联合学习抽象世界模型（跨状态和时间抽象）和层次化神经选项。在Object-Centric Atari上仅需H-DQN、HIRO、Option-Critic 1/5到1/3的环境步数即可学习更多技能。

---

**论文 5: ARISE — Agent Reasoning with Intrinsic Skill Evolution in HRL**

- **发表平台：** arXiv:2603.16060 (2026-03)
- **链接：** https://arxiv.org/abs/2603.16060

**摘要：**
两层HRL系统：Manager维护一个通过蒸馏成功解轨迹更新技能描述的分层技能库；Worker执行选定技能。使用策略驱动的技能选择（而非纯嵌入相似度），在7个基准上一致提升，在out-of-distribution任务上提升最大。

---

#### 技术趋势分析

| 趋势 | 描述 |
|------|------|
| LLM/FM驱动Skill发现 | 从手工设计skill转向基础模型自动发现和编码技能（CODE-SHARP, LLMHRL） |
| 神经符号选项框架 | 将逻辑/符号结构与神经网络结合（H²RL） |
| 世界模型+选项协同学习 | 抽象世界模型与层次选项的联合优化（AgentOWL） |
| 开放式技能进化 | 技能库在训练中持续增长和优化（ARISE, CODE-SHARP） |
| 多智能体/人机协作技能 | 技能学习考虑交互伙伴（PASD） |

---

### 2.3 多智能体强化学习

#### 重要论文

---

**论文 1: Communication-Aware MARL for Decentralized Cooperative UAV Deployment**

- **发表平台：** arXiv:2603.16141 (2026-03-17)
- **链接：** https://arxiv.org/abs/2603.16141

**摘要：**
提出基于图的MARL框架，采用CTDE架构，在部分观测和间歇性通信条件下进行UAV集群部署。使用agent-entity attention + neighbor self-attention在距离受限通信图上运行。在DroneConnect（协同中继部署）和DroneCombat（对抗性交战）上测试，5架UAV和10个节点达成74%覆盖，并泛化到未见过的团队规模无需微调。

**关键技术贡献：**
1. 通信图上的双重注意力机制（entity + neighbor）
2. CTDE下的间歇性通信鲁棒策略
3. 零样本团队规模泛化

**与本课题关联分析：** 🔴 **高关联** — 直接解决无人机集群在通信受限条件下的协作问题。xmd_rl可以扩展为多无人机环境，集成此通信感知MARL框架。

---

**论文 2: RALLY — Role-Adaptive LLM-Driven Yoked Navigation for UAV Swarms**

- **发表平台：** IEEE Open Journal of Vehicular Technology, Vol. 6 (2026)
- **链接：** https://trid.trb.org/View/2658682

**摘要：**
将LLM与MARL结合用于UAV集群控制。创新性地引入动态角色切换机制（指挥官、协调员、执行者），使用Role-value Mixing Network (RMIX)将LLM离线先验与MARL在线策略融合。在MPE和SITL平台上优于传统方法，在覆盖范围、收敛速度和泛化能力上均有提升。

**关键技术贡献：**
1. LLM先验 + MARL在线策略的融合架构
2. 动态角色切换（commander/coordinator/executor）
3. RMIX混合网络实现价值分解与角色融合

**与本课题关联分析：** 🔴 **高关联** — RALLY是LLM+MARL在UAV集群领域的标杆工作，展示了LLM如何提供高层推理和角色分配，而MARL负责底层执行。

---

**论文 3: GA-GAT-PPO — Geometry-Aware Graph Attention for Multi-UAV Decision-Making**

- **发表平台：** Drones (MDPI), Vol. 10, Issue 5 (2026-04-22)
- **链接：** https://www.mdpi.com/2504-446X/10/5/313

**摘要：**
分层框架将底层机动控制与高层协作分配解耦。GA-GAT（Geometry-Aware Graph Attention Network）通过门控模块将运动学可行性约束嵌入注意力机制。使用Transformer + Actor-memory模块处理时间依赖性，展示了对非对称UAV场景的零样本可扩展性。

**与本课题关联分析：** 🔴 **高关联** — 运动学感知的注意力机制可以直接集成到xmd_rl的多无人机扩展中。

---

**论文 4: EMARL — Explainable Multi-Agent RL for Secure UAV Swarm Communication**

- **发表平台：** Scientific Reports, Vol. 16 (2026)
- **链接：** https://www.nature.com/articles/s41598-026-39366-x

**摘要：**
提出可解释MARL框架用于安全FANET通信。结合MADDPG与基于信任的安全机制以及XAI组件（SHAP、LIME、注意力可视化）。在干扰和Sybil攻击下超越AODV、Q-Routing和标准MARL。通过NS-3 + AirSim + Python MARL引擎联合验证。

---

**论文 5: Tri-Hierarchical Swarm Learning — Bounded Coupled AI Dynamics**

- **发表平台：** arXiv:2603.20333 (2026-03-20)
- **链接：** https://arxiv.org/abs/2603.20333

**摘要：**
研究三时间尺度学习系统：Hebbian在线学习（10-100ms）→ MARL战术协调（1-10s）→ MAML战略适应（10-100s）。证明了四个定理：有界总误差、有界表示漂移、元级兼容性、误差非累积。

---

#### 技术趋势分析

| 趋势 | 描述 |
|------|------|
| LLM+MARL融合 | LLM提供高层推理和角色分配，MARL执行底层控制（RALLY） |
| 图神经网络MARL | GNN嵌入通信拓扑和运动学约束（Comm-Aware, GA-GAT-PPO） |
| 可解释MARL | XAI工具引入MARL决策透明化（EMARL） |
| 多时间尺度学习 | 从毫秒级控制到秒级协调的层次化学习（Tri-Hierarchical） |
| 零样本泛化 | 训练好的MARL策略泛化到不同规模的团队 |

---

### 2.4 无人机飞行控制

#### 重要论文

---

**论文 1: RAPTOR — A Foundation Policy for Quadrotor Control (Science Robotics!)**

- **作者/机构：** (多机构合作)
- **发表平台：** Science Robotics (2026)
- **链接：** 参见网易报道 https://www.163.com/dy/article/KT14U2LM05568W0A.html

**摘要：**
⭐ **本周最重要论文之一！** 一个仅含2,084个参数的GRU神经网络，零样本控制10种完全不同的真实四旋翼（32g微型到2.4kg大型），覆盖PX4、Betaflight、Crazyflie三种飞控固件。RMSE轨迹跟踪误差0.07-0.29m，抗风能力7-10m/s。核心技术：元模仿学习将1,000个SAC教师策略的知识蒸馏到一个学生策略中，通过隐藏状态实现隐式系统辨识——无需对新型号无人机进行重新调参。

**关键技术贡献：**
1. 单策略控制10种不同无人机（真正的Foundation Policy）
2. 2,084参数GRU实现（极度轻量，可部署在MCU级别硬件）
3. 元模仿学习蒸馏1000个SAC教师
4. 隐式系统辨识（通过RNN隐藏状态自适应不同动力学）
5. 跨飞控固件（PX4/Betaflight/Crazyflie）泛化

**与本课题关联分析：** 🔴🔴🔴 **极高关联！** 这可能是2026年无人机RL领域最重要的论文。
- 直接相关：xmd_rl的四旋翼RL训练可以直接借鉴其元模仿学习框架
- 启示：能否训练一个"Foundation Policy"同时控制多种四旋翼配置？
- 技术路径：在Isaac Lab中随机化无人机参数（质量、臂长、电机特性），用元学习训练统一策略

---

**论文 2: FO-MPC + Deep RL Adaptive Control for Quadrotor**

- **发表平台：** Aerospace Science and Technology, Vol. 172 (2026-05)
- **链接：** https://www.sciencedirect.com (Shuguang Li)

**摘要：**
结合分数阶MPC（捕获记忆/遗传效应）和最大熵actor-critic深度RL。分数阶MPC处理系统的历史依赖特性，deep RL提供自适应能力。结果：跟踪误差降低45%，能效提升35%。在非线性6DoF四旋翼模型上验证，包括高斯噪声和强扰动条件。

**与本课题关联分析：** 🔴 **高关联** — MPC+RL混合控制是xmd_rl可以尝试的重要方向。可以先用RL训练基础策略，再用MPC提供安全保证和精细调节。

---

**论文 3: RSL-RL-SAC — 在IsaacLab上弥合SAC与PPO差距** (见2.1论文1)

**与本课题关联分析：** 🔴🔴 **极高关联** — 直接涉及IsaacLab平台，xmd_rl当前基于PPO，引入SAC后可大幅拓展算法选择空间。

---

**论文 4: T2S-MPC — Time-Embedded Online Adaptive MPC**

- **发表平台：** arXiv:2605.24852 (2026-05)
- **链接：** https://arxiv.org/html/2605.24852v1
- **代码：** https://github.com/Zeyuu0920/T2S_MPC

**摘要：**
在线学习残差动力学模型，使用结构化时间嵌入。双时间尺度更新方案支持快速适应+稳定学习。在2D四旋翼上验证，在线性漂移和周期性扰动下超越经典MPC和标准神经MPC。

---

**论文 5: RL + Lyapunov-Guaranteed Adaptive MPC Tuning**

- **发表平台：** EGU General Assembly 2026
- **链接：** https://meetingorganizer.copernicus.org/EGU26/EGU26-11383.html

**摘要：**
RL智能体在线调整MPC权重矩阵；Lyapunov边界硬裁剪增益到可证明稳定区域。在4种UAV平台（27g到5.5kg）上验证，跟踪改善22-27%，60次试验零稳定性违规。序列迁移学习减少75%的逐平台训练时间。

---

**论文 6: TD3-ADRC — RL-Tuned Active Disturbance Rejection Control on PX4**

- **发表平台：** Drones, 10(2), 110 (2026-02)
- **链接：** https://www.mdpi.com (parameterized tanh function)

**摘要：**
将自抗扰控制(ADRC)与TD3强化学习结合。参数化tanh函数用于设计跟踪微分器和ESO。在PX4飞控硬件上进行台架测试，在自适应性上超越传统PID、ADRC和DDPG。

---

#### 技术趋势分析

| 趋势 | 描述 |
|------|------|
| **Foundation Policy** | 单模型控制多种无人机平台，零样本泛化（RAPTOR） |
| **MPC+RL混合** | RL调优MPC参数/残差，MPC提供安全保证（多篇论文） |
| **在线自适应** | 时变动力学在线学习和适应（T2S-MPC） |
| **PX4硬件部署** | RL/MPC控制器在真实PX4飞控上运行（TD3-ADRC, Jetson MPC） |
| **安全认证学习** | Lyapunov/CBF约束的学习控制器 |
| **元学习+RL** | 跨平台快速适应的元学习范式 |

---

### 2.5 无人机集群

#### 重要论文

---

**论文 1: Adaptive Formation Control for Multi-UAV Swarms in Cluttered Environments**

- **发表平台：** Actuators, 15(3), 163 (2026-03-12)
- **链接：** https://www.mdpi.com/2076-0825/15/3/163

**摘要：**
Leader-follower分布式架构 + SFC约束Bezier轨迹规划。创新性的动态编队缩放机制：集群在通过狭窄通道时自适应收缩/扩展。非线性分布式一致性估计器处理有向切换图和有界延迟。Max-min收缩分析建立了不需要持续连接的实际收敛性。

**与本课题关联分析：** 🔴 **高关联** — 编队缩放机制是xmd_rl多机扩展的重要参考。RL策略可以学习何时缩放编队以及如何安全通过狭窄空间。

---

**论文 2: Hierarchical Target Tracking for UAV Swarms with Distributed Optimization and Affine Control**

- **发表平台：** Drones, 10(5), 366 (2026-05-11)
- **链接：** https://www.mdpi.com/2504-446X/10/5/366

**摘要：**
两层架构：Leader层（分布式时变优化做跟踪决策）+ Follower层（仿射变换控制）。双积分预测-校正协议实时跟踪高机动性目标群。仿射控制支持缩放、旋转和剪切，提供卓越的环境适应性。支持大规模集群的可扩展节点添加。

---

**论文 3: Dynamic Event-Triggered Control for UAV Swarm Adaptive Target Enclosing**

- **发表平台：** Sensors, 26(2), 655 (2026-01-18)
- **链接：** https://www.mdpi.com/1424-8220/26/2/655

**摘要：**
几何变换参数集统一描述编队平移、旋转和缩放。分布式动态事件触发控制器在保证稳定性的同时降低通信频率。自适应目标包围（等距→变距）统一框架。正式证明无Zeno行为。

---

**论文 4: Cooperative Autonomy of UAS — Comprehensive Book Chapter**

- **发表平台：** IntechOpen (2026-05-05)
- **链接：** https://www.intechopen.com/online-first/1249128

**摘要：**
综合综述章节，涵盖分布式决策、通信感知协调、冲突避免。覆盖leader-follower、虚拟结构、优化方法、MPC和MARL方法。强调弹性——容错、自适应角色重分配、编队重构。未来方向：可解释AI、数字孪生、人集群交互。

---

#### 技术趋势分析

| 趋势 | 描述 |
|------|------|
| 自适应编队缩放 | 编队根据环境动态调整形状和大小 |
| 事件触发通信 | 减少通信频率同时保持稳定性 |
| 仿射编队控制 | 超越刚性编队，支持缩放、旋转、剪切 |
| 分布式优化+控制 | 优化与控制统一在分布式框架中 |
| 集群安全性 | 容错重构、内生安全、网络攻击鲁棒性 |

---

### 2.6 空地协同

#### 重要论文

---

**论文 1: Learning-Accelerated Optimization-based Trajectory Planning for Cooperative Aerial-Ground Handover Missions**

- **发表平台：** arXiv:2605.19562, RoManSy 2026 (Accepted)
- **链接：** https://arxiv.org/abs/2605.19562

**摘要：**
提出神经代理规划器，使用LSTM编码器-解码器网络生成协调的UAV-UGV交接轨迹预测。实现3倍加速和100%优化成功率（对比冷启动方法）。将数据驱动推理与基于模型的精细化结合，实现实时能力。这是学习+优化混合范式在空地协同中的代表性工作。

**与本课题关联分析：** 🔴 **高关联** — 空地协同是xmd_rl未来扩展的重要方向。学习加速优化的范式可以用于UAV-UGV协调任务的实时规划。

---

**论文 2: Heterogeneous Agents, Unified Missions — Survey and Taxonomy on Air-Ground Cooperative Systems**

- **发表平台：** Robotics and Autonomous Systems (2026)
- **链接：** https://www.sciencedirect.com/science/article/abs/pii/S0921889026001879

**摘要：**
2015-2025年空地异构系统(AGHS)的全面综述。提出三层架构：决策层→实现层→应用层。系统部署分类：L1（高度集中协调）→ L2（集中-分布混合）→ L3（高度分布式自治）。覆盖SAR、物流配送、农业管理应用。

---

**论文 3: Fly, Track, Land — Infrastructure-less Magnetic Localization for UAV-UGV Teaming**

- **发表平台：** arXiv:2603.08926, Submitted to IEEE T-RO (2026-03)
- **链接：** https://arxiv.org/abs/2603.08926

**摘要：**
轻量UAV自主悬停、跟踪并以厘米精度降落在移动四足UGV上。使用磁感应(MI)定位——无需GPS、无外部锚点。静态3D位置RMSE 5cm，动态跟踪和着陆RMSE 7.2cm。20Hz相对位姿估计完全在机载运行。

---

**论文 4: Energy-Aware Collaborative Exploration for UAV-UGV Team**

- **发表平台：** arXiv:2603.22507 (2026-03)
- **链接：** https://arxiv.org/html/2603.22507v1

**摘要：**
UAV能量约束建模为最大飞行时间限制。UGV同时作为主动探索者和移动充电站。构建密度感知分层概率路线图(PRM)耦合空中和地面配置。将协调路径选择形式化为耦合定向问题(OPs)。通过仿真、基准测试和真实实验验证。

---

**论文 5: Hierarchical Cooperative Trajectory Planning in Communication-Constrained Urban Canyons**

- **发表平台：** Machines, 14(6), 594 (2026-05)
- **链接：** https://www.mdpi.com/2075-1702/14/6/594

**摘要：**
解决城市峡谷中UAV作为通信中继的问题。两层层次化框架：上层使用启发式搜索引导RL求初始解；下层使用基于优化的求解器配走廊约束。改善碰撞避免、通信可靠性和轨迹平滑度。

---

#### 技术趋势分析

| 趋势 | 描述 |
|------|------|
| 学习+优化混合 | 神经网络热启动传统优化器，实现实时规划 |
| 基础设施无关操作 | GPS拒止、无锚点定位（磁感应、视觉） |
| 能耗感知规划 | 能量作为一阶约束，UGV作为移动充电站 |
| 统一框架 | 单一算法同时处理任务分配+规划+控制 |
| 真实世界验证 | 从纯仿真转向硬件实验的明显趋势 |
| 角色专业化 | 多UAV各司其职，支持单一UGV |

---

## 3. 交叉主题

### 3.1 Sim-to-Real 迁移

#### 重要进展

| 工作 | 核心方法 | 亮点 |
|------|---------|------|
| **DexSim2Real (arXiv:2605.05241)** | FM-DR: VLM作为"视觉真实感评判"优化域随机化参数 | 6个灵巧操作任务78.2%成功率，sim-to-real gap仅8.3% |
| **SPiDR (NeurIPS 2025)** | Pessimistic Domain Randomization: 动力学集成不确定性作为安全惩罚 | 可证明安全保证的DR |
| **E-DROPO (arXiv:2506.10133)** | Offline DR: 从真实数据拟合仿真参数分布 | O(M)倍更紧的sim-to-real误差界 |
| **DRIS (arXiv:2605.09789)** | 多实例同时传播：10个随机实例并行 | 零样本反应性接球任务成功 |
| **RAPTOR (Science Robotics)** | 元模仿学习: 1000 SAC教师→1个GRU学生 | 零样本控制10种无人机 |

**Sim-to-Real趋势总结：**
1. 从手动调参→自动化DR（VLM/LLM辅助）
2. 从无安全保证→可证明安全边界
3. 从单一实例→多假设同时跟踪
4. 从仿真到真实的一次性迁移→元学习驱动的零样本泛化

**与本课题关联分析：** 🔴🔴 **极高关联** — xmd_rl的核心挑战就是sim-to-real。RAPTOR的元模仿学习、DexSim2Real的FM-DR、SPiDR的安全DR都是可以直接借鉴的方法。

---

### 3.2 安全强化学习

#### 重要进展

| 工作 | 核心方法 | 亮点 |
|------|---------|------|
| **SB-TRPO (arXiv:2512.23770)** | Safety-Biased TRPO: 奖励+成本自然梯度的凸组合 | 硬约束（零违反）下有最优安全-性能平衡 |
| **CRAPO (Pattern Recognition, 2026-05)** | 修正差分乘子法 + CVaR风险规避 | 解决折扣安全成本与实际约束不匹配 |
| **SafeVLA (NeurIPS 2025 Spotlight)** | VLA策略 + CMDP min-max优化 | 安全违反降低83.58%，任务成功率+3.85% |
| **PbCRL (arXiv:2603.23565)** | 从人类偏好推断安全约束 | Dead zone机制鼓励重尾成本分布 |
| **Budget-Conditioned Reachability (ICAPS 2026)** | 预算条件安全可达性分析 | 无需不稳定min-max/Lagrangian优化 |

**与本课题关联分析：** 🔴🔴 **极高关联** — 无人机飞行安全是硬需求。CRAPO的CVaR风险规避和SB-TRPO的硬约束保证可以直接应用于xmd_rl的安全飞行策略训练。

---

### 3.3 仿真平台动态

#### ⭐ Isaac Sim 6.0 开源 & Isaac Lab 3.0 Beta — 2026年最大生态变化！

| 更新 | 详情 |
|------|------|
| **Isaac Sim 6.0 开源** | Apache 2.0许可，GitHub: [`isaac-sim/IsaacSim`](https://github.com/isaac-sim/IsaacSim) |
| **Isaac Lab 3.0 Beta** | 多物理后端（PhysX + Newton/MuJoCo-Warp），可脱离Isaac Sim运行 |
| **Newton物理后端** | Kit-less模式，支持articulations、rigid objects、contact sensors、CUDA graphs |
| **Warp Native Data** | `.data.*`属性返回`wp.array`替代`torch.Tensor`，GPU融合kernel |
| **Pluggable渲染器** | RTX / OVRTX(kit-less) / Newton Warp 三种可选 |
| **Pluggable可视化器** | Omniverse Kit / Newton OpenGL / Rerun / Viser |
| **Quaternion: WXYZ→XYZW** | ⚠️ Breaking change! 与Warp, PhysX, Newton统一 |
| **训练GPU扩展** | 支持非RTX GPU（L40s, H100, H200, B200） |
| **ROS2 Jazzy** | 原生Python 3.12支持，H.264压缩图像发布 |

**对xmd_rl的影响：** 🔴🔴🔴
- Isaac Lab 3.0的Newton后端可以在H100等非RTX GPU上训练，大幅降低硬件成本
- Warp原生数据管道可提升训练速度
- 迁移时注意quaternion格式变更（WXYZ→XYZW）
- ROS2 Jazzy原生支持简化与PX4的集成

---

## 4. 开源项目动态

| 项目 | 动态 | 与本课题关联 |
|------|------|:---:|
| **RSL-RL-SAC** | ETH开源SAC在IsaacLab上的改进实现 | 🔴 可直接在xmd_rl中测试 |
| **Isaac Sim 6.0** | 完全开源（Apache 2.0）| 🔴 核心仿真平台 |
| **Isaac Lab 3.0 Beta** | 多后端架构，脱离Isaac Sim运行 | 🔴 核心训练平台 |
| **Newton Physics** | MuJoCo-Warp后端，Kit-less | 🟡 替代物理引擎 |
| **T2S-MPC** | 在线自适应MPC代码开源 | 🟡 可集成到PX4控制 |
| **CODE-SHARP** | 技能发现框架（ICL/Sony）| 🟡 HRL参考实现 |

---

## 5. 总结与展望

### 5.1 本周关键进展 Top 5

1. ⭐ **RAPTOR (Science Robotics):** Foundation Policy单模型零样本控制10种无人机 — 无人机RL的"GPT时刻"
2. ⭐ **ISAAC SIM 6.0 开源 + ISAAC LAB 3.0 BETA:** 生态系统的彻底变革，训练成本降低，架构模块化
3. ⭐ **RSL-RL-SAC (ETH):** SAC在IsaacLab上匹敌PPO — 算法选择空间的范式转变
4. ⭐ **RALLY (IEEE OJVT):** LLM+MARL的UAV集群控制 — LLM与集群智能的首次深度融合
5. ⭐ **CODE-SHARP (ICL/Sony):** LLM驱动的开放式技能发现 — HRL新范式

### 5.2 建议关注方向

- **Foundation Policy for Quadrotor:** RAPTOR的成功表明单个小型网络可以泛化到多种无人机，xmd_rl可以朝这个方向努力
- **Isaac Lab 3.0迁移:** 评估向Isaac Lab 3.0/Isaac Sim 6.0迁移的时机和工作量
- **SAC+PPO混合策略:** 利用RSL-RL-SAC的发现，探索xmd_rl中同时使用两种算法的可能性
- **LLM+RL融合:** RALLY和CODE-SHARP展示了LLM与RL在高层推理和技能发现中的协同效应
- **安全RL:** SB-TRPO和CRAPO为无人机安全飞行提供了可证明的约束保证

### 5.3 下周关注点

- ICML 2026 论文列表即将公布（关注RL和Robotics方向录用论文）
- RSS 2026 进行中（关注无人机和空地协同最新工作）
- Isaac Lab 3.0稳定版发布时间线
- RAPTOR的代码/模型是否开源

---

## 6. 研究启发与选题分析

### 6.1 研究趋势洞察

**趋势 1: Foundation Policy for Robotics**
RAPTOR在Science Robotics上的发表标志着"机器人Foundation Policy"方向的确立。这类似于CV领域的ImageNet预训练或NLP领域的GPT——一个在多样化环境中预训练的通用策略，零样本泛化到新平台。xmd_rl有天然优势跟进这个方向。

**趋势 2: LLM as High-Level Reasoner + RL as Low-Level Executor**
RALLY和CODE-SHARP同时展示了这种分层架构的威力。LLM处理语义理解、任务分解、角色分配；RL处理毫秒级的运动控制。这是目前最promising的LLM+Robotics范式。

**趋势 3: Safety-Certified Learning**
从SPiDR到SB-TRPO到Lyapunov-constrained RL，安全学习从"best effort"走向"provable guarantee"。这对无人机飞行这种安全关键应用至关重要。

**趋势 4: Multi-Backend, Modular Simulation**
Isaac Lab 3.0的多后端架构代表了仿真平台的未来方向——不锁定在单一物理引擎或渲染器上，而是提供可插拔的模块化设计。

**趋势 5: Learning + Optimization Hybrid**
从空地协同的运动规划到无人机MPC控制，学习+优化的混合方法在各种任务中一致优于纯学习方法或纯优化方法。

### 6.2 潜在研究 Idea

---

#### **Idea 1: RAPTOR-style Foundation Policy for Quadrotor Control in Isaac Lab**

- **切入点：** RAPTOR (Science Robotics 2026) 展示了Foundation Policy在真实无人机上的可行性，但其训练使用的是SAC教师+元模仿学习。xmd_rl可以在Isaac Lab中复现并改进这个框架。
- **核心思路：** 在Isaac Lab中构建一个高度多样化的四旋翼训练环境（随机化质量、臂长、电机常数、惯量矩、气动系数），使用元学习（MAML/Reptile）或上下文RL训练一个GRU-based统一策略，使其通过隐藏状态自适应不同无人机配置。
- **创新点：**
  1. 首次在纯仿真环境（Isaac Lab）中探究Foundation Policy的scaling law（需要多少环境多样性才能泛化？）
  2. 对比元模仿学习 vs 域随机化+上下文RL两种技术路线
  3. 引入quadrotor-specific inductive bias（如对称性、动力学结构）进一步提升样本效率
- **预期贡献：** 为无人机RL的Foundation Policy方向建立仿真基准和分析框架
- **目标会议/期刊：** ICRA 2027 / Science Robotics / IEEE T-RO
- **实现方案：**
  - 技术路线：Isaac Lab + RSL-RL/RSL-RL-SAC → domain randomization → meta-RL training → zero-shot evaluation
  - 需要工具：Isaac Lab 2.x/3.0, RSL-RL, PyTorch, Weights & Biases
  - 预估工作量：4-6人月
  - 关键风险：仿真多样性是否足够支撑真实泛化（sim-to-real gap）
- **实现难度：** ⭐⭐⭐⭐
- **可行性分析：** 高。xmd_rl已有四旋翼RL训练基础，Isaac Lab提供完善的域随机化API。主要挑战在于大规模实验的计算资源和超参调优。

---

#### **Idea 2: LLM-Guided Hierarchical Skill Learning for Quadrotor Autonomous Flight**

- **切入点：** CODE-SHARP的skill自动发现 + RALLY的LLM角色分配 + xmd_rl的四旋翼控制基础
- **核心思路：** 使用LLM将四旋翼飞行任务（起降、悬停、轨迹跟踪、避障、着陆）分解为层次化技能库，每个技能由RL训练并编码为可复用的option。LLM作为高层规划器，根据任务描述和当前状态选择合适的技能序列。对于新任务，LLM可以组合已有技能或请求学习新技能。
- **创新点：**
  1. 首次将LLM-guided HRL应用于四旋翼飞行领域
  2. 技能以Python代码形式编码（借鉴CODE-SHARP），支持可解释和可验证
  3. LLM作为"飞行教练"，提供高层指导而非直接控制
- **预期贡献：** 实现四旋翼在复杂、长时域任务中的自主飞行能力（如"搜索并跟踪目标"、"在未知环境中安全导航到GPS坐标"）
- **目标会议/期刊：** ICRA 2027 / IROS 2026 / RA-L
- **实现方案：**
  - 技术路线：LLM API (Claude/GPT) → 任务分解 → Isaac Lab RL训练skills → skill库 → LLM规划+RL执行
  - 需要工具：Isaac Lab, PX4 SITL, LLM API
  - 预估工作量：5-7人月
  - 关键风险：LLM规划与RL执行的接口设计、sim-to-real for composed skills
- **实现难度：** ⭐⭐⭐⭐⭐
- **可行性分析：** 中高。技术栈分散（LLM+RL+飞控），但xmd_rl已有RL和飞控基础，LLM部分可以渐进集成。

---

#### **Idea 3: Safe RL with Lyapunov-Constrained Policy Optimization for Quadrotor**

- **切入点：** SB-TRPO的硬约束安全RL + Lyapunov-guaranteed MPC tuning + xmd_rl四旋翼
- **核心思路：** 将Lyapunov稳定性约束直接嵌入RL策略优化中。在训练时，维护一个Lyapunov函数（可学习或基于简化动力学），将策略更新约束在保证稳定性的区域内。这样训练出的策略天然满足稳定性保证，无需额外的安全层或后处理。
- **创新点：**
  1. 首次将hard Lyapunov constraints集成到quadrotor RL训练中
  2. 对比Lagrangian方法、safety layer方法和Lyapunov约束方法的实际效果
  3. 探索Lyapunov函数从简化模型到全动力学模型的迁移
- **预期贡献：** 解决RL训练的无人机策略在不稳定区域的探索安全问题
- **目标会议/期刊：** ICRA 2027 / CoRL 2026 / IEEE T-RO
- **实现方案：**
  - 技术路线：在PPO/SAC的policy loss中加入Lyapunov约束项 → Isaac Lab训练 → sim-to-real验证
  - 需要工具：Isaac Lab, PyTorch, control theory libraries
  - 预估工作量：3-5人月
  - 关键风险：Lyapunov函数设计（对四旋翼非线性系统），过约束导致性能下降
- **实现难度：** ⭐⭐⭐⭐
- **可行性分析：** 高。四旋翼有成熟的简化动力学模型可构造Lyapunov函数，xmd_rl的训练框架可以直接扩展。

---

#### **Idea 4: Communication-Aware Multi-UAV RL with Graph Attention in Isaac Lab**

- **切入点：** GA-GAT-PPO + Communication-Aware MARL + xmd_rl多机扩展
- **核心思路：** 在xmd_rl基础上构建multi-quadrotor环境（2-8架），实现GA-GAT-PPO或Comm-Aware MARL。核心挑战是：在通信带宽受限、延迟不确定、拓扑动态变化的条件下，学习分布式协同策略（编队保持、协同避障、目标分配）。
- **创新点：**
  1. 运动学约束嵌入graph attention（geometry-aware），使注意力权重自动反映物理可行性
  2. 通信预算约束下的自适应通信策略（何时传、传什么）
  3. 从2机训练泛化到N机部署（zero-shot scalability）
- **预期贡献：** 为多旋翼集群提供通信高效的分布式协同策略
- **目标会议/期刊：** IROS 2026 / ICRA 2027 / Drones (MDPI)
- **实现方案：**
  - 技术路线：扩展xmd_rl → multi-quadrotor env → implement GA-GAT-PPO → communication constraints → evaluation
  - 需要工具：Isaac Lab (multi-env support), PyTorch Geometric, PX4 multi-SITL
  - 预估工作量：4-6人月
  - 关键风险：多机训练的算力需求、CTDE架构在真实场景的通信要求
- **实现难度：** ⭐⭐⭐⭐
- **可行性分析：** 中高。Isaac Lab原生支持多环境并行，多机扩展相对直接。GA-GAT-PPO有开源参考。

---

#### **Idea 5: Learning-Accelerated MPC for Quadrotor Trajectory Tracking (RL warm-starts MPC)**

- **切入点：** 学习加速优化 (RoManSy 2026) + T2S-MPC + FO-MPC+RL (AST 2026)
- **核心思路：** 使用RL训练的神经网络作为MPC的热启动求解器。具体来说，训练一个LSTM策略网络，给定当前状态和参考轨迹，输出MPC优化问题的初始猜测。这个初始猜测足够好，使得MPC只需少量迭代即可收敛到高质量解。实际上是"RL提建议，MPC做决策并保证安全"的协作模式。
- **创新点：**
  1. RL生成MPC热启动猜测（而非直接输出控制），保留MPC的安全保证
  2. LSTM编码历史信息助力非线性非凸MPC问题求解
  3. 展示RL辅助下MPC可在嵌入式平台（Jetson/PX4）上实时运行复杂非线性MPC
- **预期贡献：** 使非线性MPC在PX4等级的嵌入式计算平台上实时运行成为可能
- **目标会议/期刊：** ICRA 2027 / IEEE T-RO / ACC 2027
- **实现方案：**
  - 技术路线：Isaac Lab训练warm-start策略 → 部署到PX4 SITL → 真实飞行验证
  - 需要工具：Isaac Lab, PX4, acados/OSQP求解器, Jetson
  - 预估工作量：5-7人月
  - 关键风险：warm-start质量在分布外数据上的退化、实时约束
- **实现难度：** ⭐⭐⭐⭐⭐
- **可行性分析：** 中。涉及RL、优化、嵌入式部署三个技术栈，集成复杂度高。但每个子模块都有成熟工具支持。

---

### 6.3 本周最值得关注的研究启发

#### 🏆 **首推：Idea 1 — Foundation Policy for Quadrotor Control**

**为什么这是本周最重要的方向：**

RAPTOR在Science Robotics的发表是一个里程碑事件。它证明了一个关键事实：**即使只有2,084个参数的微型网络，也可以通过元模仿学习获得跨平台泛化能力**。这意味着Foundation Policy不是大模型的专利——小模型也可以在物理世界中实现令人印象深刻的泛化。

**与xmd_rl项目的结合路径：**

1. **第一阶段 (1-2周)：** 在Isaac Lab中创建多样化四旋翼环境集（5-10种不同参数配置）
2. **第二阶段 (2-4周)：** 实现RAPTOR的元模仿学习框架（先训练多个SAC教师，再蒸馏为单一GRU策略）
3. **第三阶段 (1-2月)：** 在PX4 SITL中测试泛化性能，对比baseline（单一配置训练的PPO策略）
4. **第四阶段 (可选)：** 如果有真实无人机，进行sim-to-real零样本迁移测试

**竞争优势分析：**
- xmd_rl基于Isaac Lab，与RAPTOR的技术栈高度兼容
- 四旋翼（对比腿式机器人）动力学更简单，Foundation Policy更容易实现
- 这个方向目前竞争者少（RAPTOR刚发表），有先发优势窗口

**建议的下一步行动：**
1. 仔细阅读RAPTOR论文全文（特别是元模仿学习的实现细节）
2. 在xmd_rl中创建3-5个不同参数的四旋翼配置文件
3. 先复现最简版本：2种配置的SAC教师→1个GRU学生的蒸馏实验
4. 评估Isaac Lab 3.0 Beta是否适合此项目（Warp原生数据管道可能显著加速训练）

---

### 6.4 研究时间线建议

#### 短期（1-2周）— 快速验证实验

| 实验 | 描述 | 预期产出 |
|------|------|---------|
| SAC vs PPO on xmd_rl | 用RSL-RL-SAC在四旋翼悬停/轨迹跟踪上对比PPO | 确定哪种算法更适合四旋翼任务 |
| Multi-quad DR env | 创建3-5种不同参数四旋翼的Isaac Lab环境 | 支撑Foundation Policy实验 |
| LLM task decomposition test | 用Claude/GPT分解"定点着陆"任务为子技能 | 验证LLM引导HRL的可行性 |

#### 中期（1-3月）— 可产出论文的核心工作

| 项目 | 优先级 | 目标产出 |
|------|:---:|------|
| **Foundation Policy for Quadrotor** | 🔴 最高 | ICRA 2027 / IROS 2026 投稿 |
| **GA-GAT-PPO Multi-UAV** | 🟡 高 | 多机协同demo + 论文初稿 |
| **Safe RL w/ Lyapunov** | 🟡 高 | 安全性验证实验 + RA-L短文 |

#### 长期（3-6月）— 有潜力形成完整故事线

| 方向 | 描述 |
|------|------|
| **Foundation Policy + LLM-HRL** | Foundation Policy拓展到任务级泛化（不仅是跨平台） |
| **Full-stack Multi-UAV System** | MARL + 通信感知 + Sim2Real + PX4部署 |
| **Safe Foundation Policy** | 将安全保障嵌入Foundation Policy框架 |

---

## 7. 附录

### 7.1 本周论文列表

| 序号 | 论文 | 平台 | 日期 | 关联度 |
|:---:|------|------|------|:---:|
| 1 | RAPTOR: Foundation Policy for Quadrotor Control | Science Robotics | 2026 | 🔴🔴🔴 |
| 2 | RSL-RL-SAC: Bridging the Gap for Legged Locomotion | arXiv | 05-24 | 🔴🔴 |
| 3 | CODE-SHARP: Skill Discovery as Hierarchical Reward Programs | arXiv | 05-2026 | 🔴🔴 |
| 4 | RALLY: Role-Adaptive LLM-Driven Yoked Navigation | IEEE OJVT | 2026 | 🔴🔴 |
| 5 | Communication-Aware MARL for UAV Deployment | arXiv | 03-17 | 🔴🔴 |
| 6 | GA-GAT-PPO: Geometry-Aware Graph Attention for Multi-UAV | Drones | 04-22 | 🔴 |
| 7 | Learning-Accelerated Planning for Aerial-Ground Handover | RoManSy 2026 | 05-2026 | 🔴 |
| 8 | FO-MPC + Deep RL Adaptive Control for Quadrotor | AST 172 | 05-2026 | 🔴 |
| 9 | T2S-MPC: Time-Embedded Online Adaptive MPC | arXiv | 05-2026 | 🟡 |
| 10 | RL + Lyapunov-Guaranteed Adaptive MPC Tuning | EGU 2026 | 2026 | 🔴 |
| 11 | TD3-ADRC: RL-Tuned ADRC on PX4 | Drones | 02-2026 | 🔴 |
| 12 | PASD: Partner-Aware Skill Discovery for Human-AI | arXiv | 05-2026 | 🟡 |
| 13 | H²RL: Hybrid Hierarchical RL with Logical Options | arXiv | 03-2026 | 🔴 |
| 14 | AgentOWL: Joint Learning Options & World Model | arXiv | 02-2026 | 🟡 |
| 15 | ARISE: Agent Reasoning with Intrinsic Skill Evolution | arXiv | 03-2026 | 🟡 |
| 16 | EMARL: Explainable MARL for UAV Swarm Security | Scientific Reports | 2026 | 🟡 |
| 17 | Tri-Hierarchical Swarm Learning | arXiv | 03-20 | 🟡 |
| 18 | Adaptive Formation Control in Cluttered Environments | Actuators | 03-12 | 🔴 |
| 19 | Hierarchical Target Tracking with Distributed Optimization | Drones | 05-11 | 🟡 |
| 20 | Dynamic Event-Triggered UAV Swarm Target Enclosing | Sensors | 01-18 | 🟡 |
| 21 | Infrastructure-less Magnetic Localization for UAV-UGV | arXiv/T-RO | 03-2026 | 🟡 |
| 22 | Energy-Aware Collaborative Exploration UAV-UGV | arXiv | 03-2026 | 🟡 |
| 23 | DexSim2Real: FM-Guided Sim-to-Real Transfer | arXiv | 05-2026 | 🟡 |
| 24 | SPiDR: Zero-Shot Safety in Sim-to-Real Transfer | NeurIPS 2025 | 2025 | 🔴 |
| 25 | SB-TRPO: Safe RL with Hard Constraints | arXiv | 05-2026 | 🔴 |
| 26 | CRAPO: Constrained Risk-Aware Policy Optimization | Pattern Recognition | 05-2026 | 🔴 |
| 27 | SafeVLA: Safety Alignment of VLA Model | NeurIPS 2025 | 2025 | 🟡 |
| 28 | PbCRL: Preference-based Constrained RL | arXiv | 05-2026 | 🟡 |
| 29 | TOPPO: Rethinking PPO for Multi-Task RL | arXiv | 05-12 | 🟡 |
| 30 | REFLEX: RL with Reflection Symmetry Exploitation | arXiv | 05-22 | 🟡 |

### 7.2 相关会议时间

| 会议 | 时间 | 备注 |
|------|------|------|
| **RSS 2026** | 2026年5-6月 | 进行中，关注无人机和空地协同 |
| **ICML 2026** | 2026年7月 | 论文列表即将公布 |
| **Robotics: Science and Systems** | 2026 | 关注Foundation Policy方向 |
| **ICRA 2027** | 2027年5月 | 投稿截止约2026年9月 |
| **IROS 2026** | 2026年10月 | 投稿截止约2026年3月（已过） |
| **CoRL 2026** | 2026年11月 | 投稿截止约2026年6-7月 |
| **NeurIPS 2026** | 2026年12月 | 投稿截止约2026年5月（已过） |

### 7.3 推荐阅读

1. **必读：** RAPTOR (Science Robotics) — 无人机RL的里程碑
2. **必读：** Isaac Lab 3.0 Migration Guide — 为迁移做准备
3. **推荐：** RSL-RL-SAC Technical Report — 了解SAC在IsaacLab的改进
4. **推荐：** Air-Ground Cooperative Systems Survey (RAS 2026) — 全面了解空地协同
5. **关注：** CODE-SHARP v3 (arXiv:2602.10085) — HRL+LLM标杆

---

> 📅 报告生成时间：2026-05-27 | 🤖 生成工具：DailyResearch Agent (Claude)
> 
> ⚠️ 免责声明：本报告基于公开网络资源自动生成，论文信息以原文为准。部分预印本未经同行评审。
