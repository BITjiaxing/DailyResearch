# UAV + 轮足机器人空地协同具身智能专题报告

日期：2026-05-18  
主题：UAV + 轮足机器人空地协同的具身智能：搜索、导航、验证与安全部署  
面向对象：博士研究选题、论文路线规划、课题组硬件条件匹配  
已知硬件基础：多架无人机、试验场地、Unitree Go2-W 轮足式机器狗、ROS2 可集成；本地算力约 RTX 4070 Ti Super + i7-14700F，预算有限但可租算力。

## 1. 结论先行

在你的条件下，最优博士方向不是泛泛做“具身大模型”，也不是继续强化“无人机集群/军工对抗”标签，而是：

```text
面向真实场地的空地异构具身协同：
UAV 负责快速全局搜索/建图/目标发现/通信中继，
Go2-W 负责地面接近/局部验证/复杂地形导航/近距离感知，
二者通过 ROS2 和语义地图/任务状态共享完成搜索、导航、验证与失败恢复。
```

这个题同时满足四点：

1. **贴合组内硬件。** 你们有大量 UAV、真实试验场地和一台 Go2-W，这是很多纯 AI/具身智能组没有的优势。
2. **符合具身智能趋势。** 研究对象是具有真实物理身体的异构机器人，任务需要感知、规划、行动、反馈和通信。
3. **保留多智能体特色。** UAV 与 Go2-W 是天然异构多智能体系统，存在任务分配、协同搜索、通信受限和失败恢复问题。
4. **就业叙事更友好。** 可包装为 multi-robot coordination、robot learning、field robotics、sim-to-real、inspection / search / rescue，而不是军事无人机控制。

建议博士主线：

```text
Embodied Air-Ground Robot Learning for Search, Navigation, Verification and Reliable Deployment
```

中文表述：

```text
面向搜索-导航-验证任务的空地异构具身机器人协同学习与可靠部署
```

## 2. 任务定义

### 2.1 系统组成

| 角色 | 平台 | 主要能力 | 主要短板 |
|---|---|---|---|
| 空中机器人 | 四旋翼 UAV | 高空快速搜索、全局视野、建图、目标发现、通信中继 | 续航短、载荷有限、近距离交互能力弱 |
| 地面机器人 | Unitree Go2-W | 地面接近、复杂地形移动、近距离观察、目标验证、携带传感器 | 全局视野差、速度较慢、易受地形遮挡影响 |
| 通信与协调 | ROS2 / DDS / Wi-Fi / 自组网 | 状态共享、地图共享、任务指令、心跳监测 | 丢包、延迟、覆盖范围有限 |
| 高层智能 | 任务规划 / MARL / LLM planner | 目标分配、路径选择、失败恢复、语义指令理解 | 需要低层控制器保证执行安全 |
| 低层执行 | PX4 / Go2 SDK / Nav2 / MPC / 传统控制器 | 实时稳定执行 | 对复杂任务缺少全局语义和协同能力 |

### 2.2 推荐任务场景

优先选择民用、产业友好的任务语义：

- 灾后搜索与验证：UAV 搜索疑似目标，Go2-W 到达并近距离确认。
- 园区 / 工厂巡检：UAV 建图并发现异常点，Go2-W 做地面复核。
- 野外目标搜索：UAV 快速覆盖，Go2-W 处理遮挡、树林、低矮障碍。
- 仓储 / 园区安全巡检：UAV 提供鸟瞰视角，Go2-W 进行地面移动检查。
- 通信中继任务：UAV 作为临时通信中继，帮助 Go2-W 在遮挡环境中完成导航。

避免把任务命名为：

- 蜂群作战
- 对抗侦察
- 目标打击
- 电子战
- 协同压制

同一套技术可以用在民用场景里，论文和简历应优先使用中性表述。

## 3. 研究问题拆解

这个方向不是一个单点算法，而是一个系统型研究问题。建议拆成六个模块。

### 3.1 UAV 全局搜索与语义建图

问题：

- UAV 如何快速覆盖未知区域。
- 如何把航拍图像转为可供 Go2-W 使用的语义地图。
- 如何标注目标、障碍、可通行区域和风险区域。
- 如何在 GPS 弱/无 GPS 场景下提供相对定位参考。

可用方法：

- 语义分割 + 正射地图 / BEV map。
- semantic-metric map。
- frontier exploration。
- active mapping。
- aerial-to-ground cross-view localization。

### 3.2 Go2-W 地面导航与局部验证

问题：

- Go2-W 如何基于 UAV 地图规划地面路径。
- 如何在地形不确定、遮挡、坡道、碎石、草地中安全行进。
- 如何到达目标点后做近距离确认。
- 如何在局部传感器失效或定位漂移时请求 UAV 重新观测。

可用方法：

- Nav2 / local planner。
- traversability estimation。
- visual-inertial odometry / LiDAR SLAM。
- semantic waypoint navigation。
- failure prediction and replanning。

### 3.3 空地任务分配与调度

问题：

- UAV 发现多个疑似目标时，Go2-W 先验证哪个。
- UAV 是继续搜索，还是返回为 Go2-W 提供中继/重新建图。
- 目标验证失败后如何重分配。
- 电量、距离、通信质量如何进入决策。

可用方法：

- rule-based task allocator。
- behavior tree。
- POMDP。
- MAPPO / MADDPG。
- graph neural network + MARL。
- LLM planner + symbolic constraints。

### 3.4 通信受限协同

问题：

- UAV 和 Go2-W 不能假设全程高带宽通信。
- 地面遮挡、距离、建筑物和地形会造成丢包。
- 地图不宜完整频繁传输，应传语义增量、目标状态、关键 waypoint。

可用方法：

- delta map sharing。
- episodic spatial memory。
- event-triggered communication。
- goal broadcasting。
- opportunistic communication。
- low-bandwidth semantic state sharing。

### 3.5 失败恢复

这是比单纯“安全避碰”更有论文价值的部分。

典型失败：

- UAV 发现目标但 Go2-W 无法到达。
- Go2-W 定位漂移。
- UAV 电量不足，需要返航。
- 通信中断。
- 目标误检。
- Go2-W 路径被障碍阻断。
- 地面验证发现目标不符合任务要求。

建议把失败恢复作为核心指标，而不是只统计 success rate。

### 3.6 真实部署评测

你的组内优势在真实场地和硬件。论文必须体现这一点。

建议指标：

| 指标 | 含义 |
|---|---|
| mission success rate | 搜索-到达-验证完整成功率 |
| time to first detection | UAV 首次发现目标时间 |
| time to verification | Go2-W 完成近距离验证时间 |
| map update latency | UAV 地图到 Go2-W 可用的延迟 |
| communication cost | 传输字节数、通信频率、断链时间 |
| replanning count | 重规划次数 |
| recovery success rate | 失败后恢复成功率 |
| human intervention count | 人工接管次数 |
| safety violation | 碰撞、越界、危险距离、姿态异常 |
| sim-to-real gap | 仿真与真实性能差距 |

## 4. 代表性高水平论文与相关工作

下面按与你课题的相关程度组织。标注“强相关”的论文应重点精读。

### 4.1 空地语义协同与真实场地系统

#### 论文 1：Stronger Together: Air-Ground Robotic Collaboration Using Semantics

- 作者：Ian D. Miller, Fernando Cladera, Trey Smith, Camillo J. Taylor, Vijay Kumar
- 类型：IEEE RA-L / IROS 相关，Kumar Robotics 系统工作
- 链接：https://arxiv.org/abs/2206.14289
- 相关度：★★★★★

核心内容：

这篇论文提出端到端异构空地机器人系统：高空四旋翼实时创建语义地图，地面机器人基于该地图定位、规划和导航。地面机器人还能用语义匹配进行 aerial-ground cross-view localization，并在没有外部基础设施的情况下进行 opportunistic distributed communication。论文报告了真实环境中超过 6 km 的地面机器人自主行驶，以及仿真中超过 96 km 的无干预运行。

对你的启发：

这是你要做的系统雏形。你的 Go2-W 可以对应其中的地面机器人；UAV 负责语义地图和全局视角。你可以在这个基础上加入“搜索-验证”任务和学习型调度策略。

可借鉴模块：

- UAV 语义地图。
- UGV 基于鸟瞰地图导航。
- cross-view localization。
- opportunistic communication。
- 真实场地验证写法。

不足与可创新点：

- 主要是工程系统和语义地图协同，学习成分较弱。
- 搜索-验证任务链不够突出。
- 失败恢复和通信受限下的策略学习仍可加强。

#### 论文 2：Air-Ground Collaboration with SPOMP: Semantic Panoramic Online Mapping and Planning

- 作者：Ian D. Miller, Fernando Cladera, Trey Smith, Camillo J. Taylor, Vijay Kumar
- 期刊：IEEE Transactions on Field Robotics, 2024
- DOI：https://doi.org/10.1109/TFR.2024.3424748
- 链接：https://arxiv.org/abs/2407.09902
- 相关度：★★★★★

核心内容：

SPOMP 面向户外 2.5D 环境中的空地协同，强调 semantic panoramic online mapping and planning。论文认为地图不仅要表达几何，还要表达语义，因为语义地图是多机器人协作中的通信媒介。系统支持复杂协同任务、GPS-denied 场景定位，并重点做真实场地实验和大规模仿真。

对你的启发：

这篇是“空地协同 + 语义地图 + 真实部署”的高水平标杆。你如果想发机器人系统类论文，应把它作为核心 baseline 和写作参照。

可借鉴模块：

- semantic-metric map 作为空地共享状态。
- 地面机器人基于 UAV 语义地图规划。
- 真实通信、导航、感知约束下评测。
- 大规模仿真 + 小规模真实实验结合。

可创新点：

- 从语义地图规划扩展到任务验证。
- 加入 Go2-W 轮足平台的地形适应能力。
- 引入多智能体学习做目标分配和失败恢复。

#### 论文 3：Air-Ground Collaboration for Language-Specified Missions in Unknown Environments

- 作者：Fernando Cladera, Zachary Ravichandran, Jason Hughes, Varun Murali, Carlos Nieto-Granda, M. Ani Hsieh, George J. Pappas, Camillo J. Taylor, Vijay Kumar
- 平台：arXiv 2025，项目页显示 Field Robots / AI-enabled Robotics / Multi-Robot Systems 相关
- 链接：https://arxiv.org/abs/2505.09108
- 项目页：https://tfr-air-ground.fcladera.com/
- 相关度：★★★★★

核心内容：

论文提出 UAV + UGV 能够执行自然语言指定任务的空地协同系统。系统使用 LLM-enabled planner 对在线构建并共享的 semantic-metric maps 进行推理，能够在未知城乡环境中根据语言任务进行导航，并对任务变化进行响应。论文报告了七种自然语言任务，在 ground-only 和 air-ground teaming 实验中达到 kilometer-scale navigation。

对你的启发：

这是“具身智能”味道最强的空地协同工作。你可以不从零训练 VLA/LLM，而是把 LLM 作为高层任务解释器，底层仍然由 UAV/Go2-W 控制器和学习策略执行。

可借鉴模块：

- 语言任务 -> 语义地图推理 -> 机器人执行。
- LLM 只做高层，不直接控制电机。
- 语义地图在线共享。
- 任务变化和重规划。

可创新点：

- 把语言任务中的“验证”做成核心：find and verify。
- 引入 Go2-W 轮足机器人，强调复杂地面环境。
- 加入通信中断、电量限制和失败恢复指标。

### 4.2 UAV 辅助 UGV / Go2-W 导航

#### 论文 4：ColAG: A Collaborative Air-Ground Framework for Perception-Limited UGVs' Navigation

- 作者：Zhehan Li, Rui Mao, Nanhe Chen, Chao Xu, Fei Gao, Yanjun Cao
- 会议：ICRA 2024
- FAST Lab 页面：https://zju-fast-lab.github.io/publication/conference-paper/colag/
- arXiv：https://arxiv.org/abs/2310.13324
- 相关度：★★★★★

核心内容：

ColAG 研究一个非常实际的问题：一组感知能力有限甚至“盲”的 UGV 如何在一个具备完整感知能力的 UAV 协助下安全导航。UAV 使用 SLAM 获得里程计和地图，通过有限相对位姿估计把地图分享给 UGV；UGV 在接收地图中规划路径，并预测轮式里程计误差和未知危险区域带来的失败。UAV 动态调度 waypoint 以避免 UGV 碰撞，问题被建模成带时间窗的车辆路径问题。论文包含最多 7 个 UGV 的仿真和 3 个 UGV 的真实实验。

对你的启发：

这篇和你的硬件条件高度吻合。你的 Go2-W 并不是“盲”机器人，但仍然会受限于地面视野、地形遮挡和局部感知范围。UAV 可以承担“高价值感知节点”的角色。

可直接借鉴：

- UAV 作为唯一/主要全局感知者。
- 地面机器人接收 UAV 地图导航。
- 失败预测。
- UAV 动态调度辅助地面机器人。
- 仿真 + 真实 UGV 实验组合。

可创新点：

- 把 UGV 换成 Go2-W 轮足机器人，引入复杂地形通行性。
- 从导航扩展到搜索-验证任务。
- 用学习策略处理“何时让 UAV 去搜索，何时返回给 Go2-W 支援”。

#### 论文 5：Air-Ground Cooperative Multi-Target Searching under an Unknown Urban Environment

- 作者：Chaochun Huang, Bin Du, Mou Chen
- 期刊：Transactions of the Institute of Measurement and Control, 2025
- DOI：https://doi.org/10.1177/01423312241239386
- 链接：https://journals.sagepub.com/doi/10.1177/01423312241239386
- 相关度：★★★★

核心内容：

论文提出未知城市场景下的空地协同多目标搜索框架。UAV 提供引导，多组 UGV 执行目标搜索任务，强调异构机器人互补能力对系统冗余、自主性和鲁棒性的提升。

对你的启发：

这篇适合作为“任务定义”背景。你的任务可以进一步具体化为 UAV 先发现疑似目标，Go2-W 再进行近距离验证。

### 4.3 UAV + 四足 / 轮足机器人协同与 MARL

#### 论文 6：Multi-stage Hierarchical Multi-Agent Reinforcement Learning for UAV-Quadruped Completing Search and Rescue

- 作者：Chuan Chen, Shuhan Yan, Xinliang Zhou, Jiaping Xiao
- 期刊：Discover Robotics, 2026
- 链接：https://www.researchgate.net/publication/403765351_Multi-stage_hierarchical_multi-agent_reinforcement_learning_for_UAV-quadruped_completing_search_and_rescue
- 相关度：★★★★★

核心内容：

论文构建 UAV + ANYmal-C 机器狗的异构多智能体 SAR 任务。UAV 负责搜索和到达目标，四足机器人跟随 UAV 完成地面救援任务。方法采用 multi-stage hierarchical MARL，底层分别训练 UAV 到达目标和机器狗速度跟踪，再把两者合并为 DirectMARL 环境，使用 MAPPO 和 staged learning 提升训练稳定性。实验环境基于 Isaac Lab 1.4.1 和 Isaac Sim 4.2.0。

对你的启发：

这是与你提出的 UAV + Go2-W 方向最直接的近期论文。它说明“UAV 引导机器狗完成 SAR”已经有前人开始做，但仍有明显可扩展空间。

可借鉴：

- Isaac Lab 中异构机器人合并为 DirectMARL Env。
- 分阶段训练：先单体技能，再协同任务。
- MAPPO / CTDE。
- UAV 目标到达 + quadruped velocity tracking。

不足与可创新点：

- 使用 ANYmal-C 仿真，不是 Go2-W 真实硬件。
- 任务更像“UAV 引导机器狗跟随”，搜索、验证、语义地图、通信受限不够完整。
- 没有真实场地实验。
- 没有强任务失败恢复机制。

你可以把它作为直接 baseline，并把贡献升级为：

```text
从 UAV-guided dog following
升级为 UAV-Go2-W semantic search-navigation-verification with real deployment.
```

#### 论文 7：Target Search and Navigation in Heterogeneous Robot Systems with Deep Reinforcement Learning

- 作者：Yun Chen, Jiaping Xiao
- 平台：arXiv 2023
- 链接：https://arxiv.org/abs/2308.00331
- 相关度：★★★★

核心内容：

论文设计 UAV + UGV 异构机器人系统，在未知矿井式迷宫环境中完成目标搜索和导航。作者提出 multi-stage reinforcement learning 和 curiosity module，缓解同时训练时协作奖励难以获得的问题。

对你的启发：

这篇适合支持“分阶段训练”的合理性。你的系统也不应一开始端到端训练 UAV + Go2-W，而应先训练/验证单体能力，再训练任务协同。

#### 论文 8：Autonomous and Adaptive Role Selection for Multi-Robot Collaborative Area Search Based on Deep Reinforcement Learning

- 平台：arXiv 2023
- 链接：https://arxiv.org/abs/2312.01747
- 相关度：★★★★

核心内容：

论文把多机器人区域搜索分为探索和覆盖角色，使用分层多智能体强化学习进行角色选择和局部策略执行。其思路可迁移到 UAV-Go2-W：UAV 可在“搜索/中继/复查”之间切换，Go2-W 可在“导航/验证/等待/回撤”之间切换。

对你的启发：

你可以把角色定义为：

- UAV-searcher
- UAV-relay
- UAV-reobserver
- Go2-navigator
- Go2-verifier
- Go2-safe-wait

高层策略学习角色切换，低层控制器执行动作。

### 4.4 空地协同路径规划、续航与中继

#### 论文 9：An Attention-Aware Deep Reinforcement Learning Framework for UAV-UGV Collaborative Route Planning

- 作者：Md Safwan Mondal, Subramanian Ramasamy, James D. Humann, James M. Dotterweich, Jean-Paul F. Reddinger, Marshal A. Childers, Pranav Bhounsule
- 会议：IROS 2024
- PDF：https://pab47.github.io/papers/2024Mondal_attention.pdf
- 相关度：★★★★

核心内容：

论文研究 fuel-constrained UAV-UGV cooperative routing：UAV 需要访问多个任务点，但续航有限；UGV 作为移动充电站，二者必须规划 rendezvous 和任务点访问顺序。方法使用带 multi-head attention 的 DRL encoder-decoder 架构，学习生成 UAV 和 UGV 的协同路线，并支持动态任务点出现后的在线重规划。

对你的启发：

你的 UAV + Go2-W 任务也会遇到续航、汇合点、任务点排序和在线重规划问题。虽然 Go2-W 未必给 UAV 充电，但可以作为移动地面验证节点，决策问题很相似。

可迁移：

- attention-based route policy。
- rendezvous planning。
- dynamic mission points。
- online replanning。
- energy-aware decision。

#### 论文 10：Cooperative Routing for an Air-Ground Vehicle Team: Exact Algorithm, Transformation Method, and Heuristics

- 期刊：IEEE Transactions on Automation Science and Engineering, 2019
- DOI 可从 IROS 2024 论文参考文献追溯
- 相关度：★★★

核心内容：

这类工作把 UAV-UGV 协同建模为 routing / vehicle routing / fuel-constrained planning 问题，是传统优化路线的代表。

对你的启发：

在论文里不能只和 MARL 比。应把传统 route planning / heuristic / MILP / VRP-D 作为基线，否则审稿人会质疑“为什么需要学习”。

#### 论文 11：Cooperative Aerial-Ground Vehicle Route Planning with Fuel Constraints for Coverage Applications

- 期刊：IEEE Transactions on Aerospace and Electronic Systems, 2019
- 相关度：★★★

核心内容：

研究燃料约束下 UAV 与地面车协同覆盖任务，强调大范围覆盖时 UAV 续航和地面平台支持的耦合。

对你的启发：

可作为任务调度和续航约束背景文献。

### 4.5 多机器人鲁棒搜索、通信攻击与安全部署

#### 论文 12：Robust Multi-Robot Active Target Tracking Against Sensing and Communication Attacks

- 作者：Lifeng Zhou, Vijay Kumar
- 期刊：IEEE Transactions on Robotics, 2023
- arXiv：https://arxiv.org/abs/2109.09838
- 相关度：★★★★★

核心内容：

论文研究多机器人主动目标跟踪中的感知和通信失效/攻击。它形式化了在固定数量最坏情况 sensing attacks 和 communication attacks 下的 robust active target tracking 问题，并提出 RATT 算法，对跟踪质量提供理论保证。

对你的启发：

这里的“攻击”可以在你的课题中中性化为：

- 传感器失效
- 通信中断
- 地图更新丢失
- Go2-W 局部定位失败

这篇论文可支撑你把 failure recovery 和 communication loss 作为严肃研究问题，而不是工程补丁。

#### 论文 13：Multi-Robot Adversarial Resilience using Control Barrier Functions

- 作者：Matthew Cavorsi, Lorenzo Sabattini, Stephanie Gil 等
- 会议：RSS 2022，后续 IEEE Transactions on Robotics 2023/2024
- RSS PDF：https://www.roboticsproceedings.org/rss18/p053.pdf
- REACT Lab：https://react.seas.harvard.edu/publications/multi-robot-adversarial-resilience-using-control-barrier-functions-0
- 相关度：★★★★★

核心内容：

论文用 CBF 构造多机器人网络韧性控制器，使机器人队伍在存在异常/对抗个体时仍能保持网络连通和任务可行，同时兼顾碰撞和障碍避让等约束。该工作曾获 RSS 2022 Best Paper Award nomination。

对你的启发：

这不是让你做“军事对抗”，而是告诉你：多机器人系统的 resilience 可以用严肃控制理论建模。你的系统可把通信中断、个体失效、地面不可达视作非对抗故障，设计安全和恢复层。

#### 论文 14：Safe Multi-Agent Drone Control using Control Barrier Functions and Acceleration Fields

- 期刊：Robotics and Autonomous Systems, 2024
- DOI：https://doi.org/10.1016/j.robot.2023.104601
- 链接：https://www.sciencedirect.com/science/article/abs/pii/S0921889023002403
- 相关度：★★★★

核心内容：

论文提出轻量级多无人机安全控制方案，使用 CBF 和 QP 生成目标加速度，在避免障碍和机器人间碰撞的同时到达目标，并做了仿真和真实实验验证。

对你的启发：

对于真实 UAV + Go2-W 场地实验，不应让学习策略直接承担安全责任。建议使用 CBF / QP / rule-based safety layer 保护低层执行。

#### 论文 15：Cooperative Target Search and Tracking for Multi-UAVs based on Control Barrier Functions

- 期刊：Transactions of the Institute of Measurement and Control, 2023
- DOI：https://doi.org/10.1177/01423312231158677
- 链接：https://journals.sagepub.com/doi/10.1177/01423312231158677
- 相关度：★★★

核心内容：

论文结合信息地图、Lyapunov guidance vector field、CBF 和 QP，实现多 UAV 搜索与跟踪中的避碰和队形约束。

对你的启发：

可作为“搜索任务中安全约束如何与 nominal controller 结合”的参考。

### 4.6 具身智能、多智能体与语言/视觉规划

#### 论文 16：Open X-Embodiment: Robotic Learning Datasets and RT-X Models

- 机构：Google DeepMind 等
- 平台：arXiv 2023
- 链接：https://arxiv.org/abs/2310.08864
- 相关度：★★★★

核心内容：

Open X-Embodiment 聚合跨机器人本体的数据，推动跨平台机器人策略学习。它代表了具身智能的“大数据 + 跨本体泛化”路线。

对你的启发：

你不适合从零做 foundation model，但可以借鉴“跨本体共享表示”的思想：UAV 和 Go2-W 的任务状态可以统一成语义地图、目标状态、可达性和任务阶段，而不是直接统一底层动作。

#### 论文 17：RT-2: Vision-Language-Action Models Transfer Web Knowledge to Robotic Control

- 机构：Google DeepMind
- 项目页：https://deepmind.google/discover/blog/rt-2-new-model-translates-vision-and-language-into-action/
- 相关度：★★★

核心内容：

RT-2 将视觉-语言模型扩展到机器人动作输出，是 VLA 路线代表。

对你的启发：

你的系统不应从零训练 RT-2 类模型，但可把 VLM/LLM 用作高层语义任务解释器。例如“检查红色车辆旁的异常物体”，由 VLM 识别目标，任务层生成 UAV/Go2-W 行动计划。

#### 论文 18：Gemini Robotics: Bringing AI into the Physical World

- 机构：Google DeepMind
- 官方页：https://deepmind.google/blog/gemini-robotics-brings-ai-into-the-physical-world/
- 技术报告：https://arxiv.org/abs/2503.20020
- 相关度：★★★★

核心内容：

Gemini Robotics 将 Gemini 多模态推理能力扩展到机器人，强调视觉、语言、动作和物理世界理解。

对你的启发：

高层可用现有 VLM/LLM 做任务理解和语义推理，低层仍用控制器、规划器和学习策略。这样符合你的算力和硬件条件。

#### 论文 19：CaPo: Cooperative Plan Optimization for Efficient Embodied Multi-Agent Cooperation

- 会议：ICLR 2025
- OpenReview：https://openreview.net/forum?id=KRv9NubipP
- 相关度：★★★★

核心内容：

CaPo 关注 LLM-based embodied agents 的多智能体合作规划，指出直接临场执行容易造成冗余步骤和失败，尤其在 search-and-rescue 任务中需要长期协作计划。

对你的启发：

可以作为 LLM 高层任务规划参考。但你的论文不应只做仿真语言 agent，应落到真实 UAV + Go2-W 系统。

#### 论文 20：VIKI-R: Coordinating Embodied Multi-Agent Cooperation via Reinforcement Learning

- 平台：OpenReview 2025
- 链接：https://openreview.net/forum?id=lg8CvV2hqB
- 相关度：★★★

核心内容：

VIKI-R 提出面向 embodied multi-agent cooperation 的层级 benchmark，并使用 VLM + Chain-of-Thought demonstration + RL 做多层级协作。

对你的启发：

可借鉴它的三层结构：agent activation、task planning、trajectory perception。你可改造成：

- UAV/Go2-W 角色激活。
- 搜索/导航/验证任务规划。
- 真实机器人轨迹执行与反馈。

### 4.7 综述类文献

#### 论文 21：Heterogeneous Agents, Unified Missions: A Survey and Taxonomy on Air-Ground Cooperative Systems

- 期刊：Robotics and Autonomous Systems, 2026
- DOI：https://doi.org/10.1016/j.robot.2026.105514
- 链接：https://www.sciencedirect.com/science/article/pii/S0921889026001879
- 相关度：★★★★★

核心内容：

综述将 air-ground heterogeneous systems 分为 decision-making、implementation、application 三层，讨论 UAV/UGV 平台、关键技术、部署分类和未来方向，包括自治性、可扩展性和复杂环境鲁棒性。

对你的启发：

这是写开题报告和绪论时应重点引用的最新综述。

#### 论文 22：A Comprehensive Review of UAV-UGV Collaboration: Advancements and Challenges

- 期刊：Journal of Sensor and Actuator Networks, 2024
- DOI：https://doi.org/10.3390/jsan13060081
- 链接：https://www.mdpi.com/2224-2708/13/6/81
- 相关度：★★★★

核心内容：

综述 UAV-UGV collaboration 的应用、通信协调、多 UAV/UGV 协同、挑战和未来趋势。

对你的启发：

适合补充背景，但期刊影响力不如 T-RO / TFR / RAS。可作为泛综述引用。

#### 论文 23：Collaborative Multi-Robot Systems for Search and Rescue: Coordination and Perception

- 平台：arXiv 2020
- 链接：https://arxiv.org/abs/2008.12610
- 相关度：★★★★

核心内容：

综述 SAR 多机器人系统中的规划、协同、感知、active vision 等问题。

对你的启发：

适合支撑“搜索-验证”任务的合理性。

## 5. 你的可行研究路线

### 5.1 不建议做的路线

不建议：

```text
从零训练一个 UAV-Go2-W 大模型 / VLA。
```

原因：

- 4070 Ti Super 不足以支持大规模 VLA/世界模型预训练。
- 机器人数据量不足。
- 没有机械臂/人形平台，难以追 DeepMind/NVIDIA/Physical Intelligence 那类路线。

不建议：

```text
纯仿真 MAPPO 空地协同。
```

原因：

- 前人已有 UAV-quadruped + MAPPO / MHMARL。
- 如果没有真实硬件验证，创新性不足。

不建议：

```text
军事对抗语义的 UAV swarm / dog robot 协同。
```

原因：

- 会强化你想规避的军工标签。
- 对大厂/私企就业叙事不友好。

### 5.2 推荐路线：系统 + 学习 + 真实验证

推荐博士主线：

```text
UAV-Go2-W 空地异构具身系统：
语义搜索 -> 地面导航 -> 近距验证 -> 失败恢复 -> 真实场地部署。
```

算法贡献控制在中等复杂度，系统贡献和真实部署做扎实。

可拆为三层：

```text
高层：任务规划 / 角色分配 / 失败恢复
中层：语义地图 / 目标状态 / 通信受限协同
低层：PX4 / Go2 SDK / Nav2 / CBF / rule-based safety
```

## 6. 可能的论文选题

### 选题 A：UAV-Go2-W Semantic Search and Verification

推荐度：★★★★★

题目示例：

```text
Semantic Air-Ground Search and Verification with a UAV and a Wheel-Legged Robot
```

核心问题：

UAV 在大范围内搜索疑似目标并构建语义地图，Go2-W 根据语义地图到达目标位置并进行近距离验证。

贡献设计：

1. 构建 UAV-Go2-W search-navigation-verification 真实系统。
2. 设计语义地图共享机制：目标、障碍、可通行区域、风险区域。
3. 设计任务状态机或行为树：search、assign、navigate、verify、recover。
4. 在真实场地验证多种目标、遮挡和通信条件。

baseline：

- UAV-only search。
- Go2-only search。
- UAV + Go2 with manual task assignment。
- UAV + Go2 with rule-based task assignment。
- 你的 semantic task manager。

指标：

- verification success rate。
- time to verification。
- false detection recovery。
- communication cost。
- human intervention count。

适合投：

- ICRA / IROS system paper。
- IEEE RA-L。
- IEEE Transactions on Field Robotics。
- Field Robotics。

### 选题 B：Communication-Constrained Air-Ground Coordination

推荐度：★★★★

题目示例：

```text
Communication-Constrained Air-Ground Coordination for Search and Verification
```

核心问题：

UAV 和 Go2-W 之间不能高频共享完整地图，只能共享低带宽语义增量和目标状态。如何在通信受限下完成任务？

贡献设计：

1. 设计 delta semantic map sharing。
2. 设计 event-triggered communication。
3. 设计 goal broadcasting protocol。
4. 比较 full map sharing、periodic sharing、event-triggered sharing。

可用算法：

- rule-based event trigger。
- graph memory。
- small RL policy for communication decisions。
- episodic spatial memory。

相关文献：

- MemoryMesh: Shared Episodic Spatial Memory for Ground-Air Cooperative Search, OpenReview 2026
  https://openreview.net/forum?id=PwiDtJ1Icn

适合投：

- IROS / ICRA。
- AAMAS if MARL 成分更强。
- RA-L。

### 选题 C：Hierarchical MARL for UAV-Go2-W Search, Navigation and Recovery

推荐度：★★★★

题目示例：

```text
Hierarchical Multi-Agent Reinforcement Learning for UAV-Wheel-Legged Robot Search and Recovery
```

核心问题：

高层学习任务角色和阶段切换，低层使用已有控制器执行。

角色：

- UAV-search。
- UAV-relay。
- UAV-reobserve。
- Go2-navigate。
- Go2-verify。
- Go2-wait/recover。

贡献设计：

1. 分阶段训练：单体能力 -> 协作任务 -> 故障恢复。
2. CTDE 训练，decentralized execution。
3. 加入通信质量、电量、目标置信度、地形可达性作为 observation。
4. 仿真大规模训练，真实场地小规模验证。

baseline：

- direct end-to-end MAPPO。
- rule-based hierarchy。
- MHMARL-style staged training。
- no-recovery policy。

适合投：

- AAMAS。
- ICRA/IROS。
- CoRL workshop / robot learning workshop。

风险：

- 多智能体训练不稳定。
- 真实硬件部署学习策略需要谨慎。
- 建议学习只做高层离散决策，不直接输出底层速度控制。

### 选题 D：Failure-Aware Air-Ground Embodied Deployment

推荐度：★★★★

题目示例：

```text
Failure-Aware Air-Ground Robot Teaming for Reliable Field Deployment
```

核心问题：

任务失败不是异常情况，而是实际部署中的常态。系统应显式检测、分类和恢复失败。

失败类型：

- UAV target false positive。
- Go2-W path blocked。
- communication dropout。
- map stale。
- localization drift。
- low battery。
- unsafe terrain。

贡献设计：

1. 定义 UAV-Go2-W 失败分类体系。
2. 设计 failure monitor。
3. 设计 recovery policy。
4. 真实场地测试 failure injection。

这条路线更像系统论文，创新点不是单个算法，而是工程闭环和评测协议。

适合投：

- Field Robotics。
- IEEE Transactions on Field Robotics。
- ICRA/IROS。

### 选题 E：LLM-Assisted Air-Ground Mission Planning

推荐度：★★★

题目示例：

```text
LLM-Assisted Air-Ground Mission Planning with Semantic Maps and Reliable Low-Level Execution
```

核心问题：

用户用自然语言指定任务，高层 LLM 解析任务，低层 UAV-Go2-W 系统执行。

建议定位：

- LLM 只做高层任务解释。
- 不做端到端 VLA。
- 所有动作都必须经过规则/安全/可达性检查。

适合做博士后期扩展，不建议作为第一篇主线。

## 7. 推荐系统架构

```text
User / Mission Input
        |
        v
Task Manager / Behavior Tree / LLM Planner
        |
        +------------------+
        |                  |
        v                  v
UAV Mission Node      Go2-W Mission Node
        |                  |
        v                  v
UAV Perception        Go2 Local Perception
        |                  |
        +-------> Shared Semantic Map <------+
                         |
                         v
        Target Belief / Traversability / Risk Map
                         |
                         v
        Assignment / Replanning / Recovery Policy
                         |
        +----------------+----------------+
        |                                 |
        v                                 v
PX4 / UAV Controller             Go2 SDK / Nav2 / Local Planner
        |                                 |
        +---------- Safety Monitor -------+
```

### 7.1 ROS2 节点建议

| 节点 | 功能 |
|---|---|
| `/uav/perception_node` | 目标检测、语义分割、BEV 投影 |
| `/uav/mapping_node` | 构建局部/全局语义地图 |
| `/uav/mission_node` | UAV 搜索、复查、中继任务执行 |
| `/go2/localization_node` | Go2-W 定位 / SLAM |
| `/go2/navigation_node` | Nav2 或自定义局部规划 |
| `/go2/verification_node` | 近距离目标确认 |
| `/shared/semantic_map_server` | 共享语义地图和目标状态 |
| `/coordination/task_manager` | 任务分配、状态机、重规划 |
| `/coordination/recovery_node` | 失败检测与恢复 |
| `/safety/safety_monitor` | 电量、通信、越界、碰撞、人工接管 |

### 7.2 学习模块放在哪里

不要让学习模块直接接管底层控制。推荐学习模块只做：

- 目标分配。
- 角色切换。
- 通信触发。
- 路径候选选择。
- 失败恢复策略。

低层继续由：

- PX4。
- Go2 SDK。
- Nav2。
- MPC / PID / CBF / rule-based safety。

这样更容易真实部署，也更符合审稿人对安全机器人系统的预期。

## 8. 数据与实验设计

### 8.1 仿真阶段

推荐工具：

- Isaac Lab：训练 UAV / Go2-W 高层策略。
- Isaac Sim：构建可视化仿真场景。
- Gazebo / PX4 SITL：验证 UAV 飞控闭环。
- ROS2：统一通信接口。

你的 4070 Ti Super 能做：

- 中小规模 Isaac Lab RL。
- UAV + Go2-W 简化任务。
- MAPPO / PPO / SAC。
- GNN 小模型。
- VLM/LLM API 调用或小模型推理。

不建议本地做：

- 大规模 VLA 训练。
- 大世界模型训练。
- 大规模多机器人仿真。

### 8.2 真实阶段

真实实验应分三档：

| 档位 | 实验内容 |
|---|---|
| Level 1 | UAV 建图，Go2-W 离线接收地图并导航 |
| Level 2 | UAV 在线更新目标和地图，Go2-W 在线导航验证 |
| Level 3 | 加入通信中断、误检、路径阻断、电量限制和失败恢复 |

每个实验都要有可量化指标，避免只做 demo。

### 8.3 场地设计

推荐场景：

- 开阔场地 + 障碍物。
- 半结构化园区道路。
- 草地 / 土地 / 轻微坡道。
- 遮挡目标点。
- 多个疑似目标。
- 通信弱区。

## 9. 与高水平论文的差异化定位

| 相关工作 | 已解决 | 你的可创新点 |
|---|---|---|
| Stronger Together | UAV 语义地图辅助 UGV 导航 | 加入 Go2-W、搜索-验证任务、失败恢复 |
| SPOMP | 语义全景在线建图与规划 | 加入学习型任务分配、目标验证、轮足平台 |
| Language-Specified Missions | LLM + 空地语义任务 | 强化真实 Go2-W 执行与可靠部署 |
| ColAG | UAV 辅助感知受限 UGV 导航 | 扩展到目标搜索、验证、复杂地形和通信中断 |
| MHMARL UAV-Quadruped | UAV 引导机器狗 SAR 仿真 | 加入真实 Go2-W、语义地图、通信受限、验证任务 |
| IROS 2024 UAV-UGV DRL Routing | 续航/汇合/路径规划 | 接入真实机器人与语义搜索任务 |
| T-RO robust tracking | 感知/通信失效鲁棒跟踪 | 落到空地具身系统的 failure recovery |
| RSS/T-RO CBF resilience | 多机器人韧性控制 | 作为安全层而非唯一主贡献 |

## 10. 建议论文路线图

### 第一阶段：系统跑通与基线论文

时间：博士第 1 年

论文题目：

```text
Semantic Air-Ground Search and Verification with a UAV and a Wheel-Legged Robot
```

目标：

- UAV 能生成语义地图。
- Go2-W 能基于地图导航到目标点。
- 系统能完成搜索-到达-验证闭环。
- 真实场地至少完成 10-20 组实验。

投稿：

- ICRA / IROS。
- RA-L。

### 第二阶段：通信受限与失败恢复

时间：博士第 2 年

论文题目：

```text
Failure-Aware Communication-Constrained Air-Ground Robot Teaming
```

目标：

- 加入通信中断、误检、路径阻断。
- 设计 event-triggered semantic sharing。
- 加入 recovery policy。
- 比较 no-recovery、rule-based recovery、learned recovery。

投稿：

- IEEE Transactions on Field Robotics。
- Field Robotics。
- IROS / ICRA。

### 第三阶段：多智能体学习与泛化

时间：博士第 3-4 年

论文题目：

```text
Hierarchical Multi-Agent Learning for Embodied Air-Ground Coordination
```

目标：

- 加入多 UAV 或多个目标。
- 高层 MAPPO/GNN 做任务分配和角色切换。
- 仿真扩展，真实小规模验证。

投稿：

- AAMAS。
- ICRA / IROS。
- CoRL workshop / RA-L。

### 第四阶段：语言任务与具身智能扩展

时间：博士后期

论文题目：

```text
Language-Specified Air-Ground Missions with Semantic Maps and Reliable Execution
```

目标：

- 用户自然语言指定任务。
- LLM 解析目标和约束。
- UAV-Go2-W 系统执行。
- 加入安全与可达性检查，避免 LLM 直接控制。

投稿：

- ICRA / IROS。
- CoRL。
- RA-L。

## 11. 就业导向价值

这个方向对就业的好处是，它既能服务研究所，也能服务私企和大厂。

### 11.1 研究所

匹配岗位：

- 智能无人系统。
- 多机器人协同。
- 空地协同。
- 自主搜索与巡检。
- 仿真与实装验证。

优势：

- 你有北理工机电 / 兵器学科背景。
- 有真实 UAV 和机器人实验。
- 多智能体和具身协同都符合研究所需求。

### 11.2 互联网大厂 / 自动驾驶 / 机器人公司

匹配岗位：

- robot learning。
- embodied AI。
- multi-robot coordination。
- autonomous inspection。
- closed-loop simulation。
- planning and decision。
- safety evaluation。
- sim-to-real。

优势：

- 你能把论文包装成民用机器人和具身智能。
- UAV + Go2-W 是真实机器人系统，不是纯仿真。
- ROS2、Isaac、PX4、Go2 SDK 都是工业可理解的技能。

### 11.3 科创公司

匹配方向：

- 巡检机器人。
- 四足/轮足机器人。
- 工业园区机器人。
- 低空经济。
- 仓储/物流多机器人。
- 无人配送。
- 安防巡检。

你的项目经历可以写成：

```text
构建 UAV + 轮足机器人空地异构具身系统，
实现语义搜索、地面导航、目标验证和通信受限下的任务重规划，
并在真实场地完成闭环部署。
```

这比“军工无人机强化学习控制”更适合私企和大厂。

## 12. 推荐精读清单

第一批必须精读：

1. Stronger Together: Air-Ground Robotic Collaboration Using Semantics  
   https://arxiv.org/abs/2206.14289

2. Air-Ground Collaboration with SPOMP  
   https://arxiv.org/abs/2407.09902

3. Air-Ground Collaboration for Language-Specified Missions  
   https://arxiv.org/abs/2505.09108

4. ColAG: A Collaborative Air-Ground Framework for Perception-Limited UGVs' Navigation  
   https://arxiv.org/abs/2310.13324

5. Multi-stage Hierarchical MARL for UAV-Quadruped SAR  
   https://www.researchgate.net/publication/403765351_Multi-stage_hierarchical_multi-agent_reinforcement_learning_for_UAV-quadruped_completing_search_and_rescue

6. An Attention-Aware DRL Framework for UAV-UGV Collaborative Route Planning  
   https://pab47.github.io/papers/2024Mondal_attention.pdf

第二批方法支撑：

7. Robust Multi-Robot Active Target Tracking Against Sensing and Communication Attacks  
   https://arxiv.org/abs/2109.09838

8. Multi-Robot Adversarial Resilience using Control Barrier Functions  
   https://www.roboticsproceedings.org/rss18/p053.pdf

9. Safe Multi-Agent Drone Control using Control Barrier Functions and Acceleration Fields  
   https://www.sciencedirect.com/science/article/abs/pii/S0921889023002403

10. Cooperative Target Search and Tracking for Multi-UAVs based on CBFs  
    https://journals.sagepub.com/doi/10.1177/01423312231158677

第三批具身智能扩展：

11. Open X-Embodiment  
    https://arxiv.org/abs/2310.08864

12. Gemini Robotics  
    https://arxiv.org/abs/2503.20020

13. CaPo: Cooperative Plan Optimization for Embodied Multi-Agent Cooperation  
    https://openreview.net/forum?id=KRv9NubipP

14. VIKI-R: Coordinating Embodied Multi-Agent Cooperation via Reinforcement Learning  
    https://openreview.net/forum?id=lg8CvV2hqB

综述：

15. Heterogeneous Agents, Unified Missions: A Survey and Taxonomy on Air-Ground Cooperative Systems  
    https://www.sciencedirect.com/science/article/pii/S0921889026001879

16. A Comprehensive Review of UAV-UGV Collaboration  
    https://www.mdpi.com/2224-2708/13/6/81

17. Collaborative Multi-Robot Systems for Search and Rescue  
    https://arxiv.org/abs/2008.12610

## 13. 最终建议

你这个方向最有价值的不是“安全”两个字，也不是“MARL”一个算法，而是：

```text
真实硬件条件下，异构具身机器人如何可靠地完成搜索-导航-验证任务。
```

建议你把博士课题定位为：

```text
面向真实部署的空地异构具身协同学习与任务执行
```

其中：

- UAV 提供全局感知和快速搜索。
- Go2-W 提供地面接近和目标验证。
- ROS2 提供通信与系统集成。
- 语义地图作为空地共享记忆。
- 学习模块处理高层决策、角色切换、通信触发和失败恢复。
- 安全层保证真实场地部署可控。

最适合作为第一篇论文的题目：

```text
Semantic Air-Ground Search and Verification with a UAV and a Wheel-Legged Robot
```

最适合作为博士主线的英文题目：

```text
Embodied Air-Ground Robot Learning for Search, Navigation, Verification and Reliable Deployment
```

这条路线能最大化利用你们组的无人机、Go2-W 和试验场地，同时又能把你的简历从“军工无人机 RL”转向“具身智能、多机器人协同、机器人学习与真实部署”。
