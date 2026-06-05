# UAV-Go2-W、分层 UAV 任务 RL 与 LLM 空地任务规划调研报告

日期：2026-05-22  
关注方向：  
1. UAV-Go2-W 语义搜索与验证  
2. Hierarchical UAV Mission RL  
3. LLM-Assisted Air-Ground Mission Planning  

## 0. 结论先行

这三个方向都不是“完全没人做过”的空白题，但可以组合成一条很有价值的博士/论文路线：

```text
UAV-Go2-W 空地异构系统：
语义搜索与建图 -> 任务级分层决策 -> Go2-W 地面验证 -> LLM 高层任务接口 -> 真实场地闭环评测
```

最推荐的主线不是单独做 LLM，也不是单独做 HRL，而是：

```text
Semantic Air-Ground Search and Verification with Reliable Task-Level Autonomy
```

中文可表述为：

```text
面向真实部署的 UAV-Go2-W 语义搜索、地面验证与任务级自主决策
```

推荐优先级：

| 排名 | 方向 | 新颖性 | 可行性 | 论文价值 | 建议定位 |
|---:|---|---:|---:|---:|---|
| 1 | UAV-Go2-W 语义搜索与验证 | 中高 | 高 | 高 | 第一篇系统论文主线 |
| 2 | Hierarchical UAV Mission RL | 中 | 中高 | 中高 | 作为任务决策模块或第二篇 |
| 3 | LLM-Assisted Air-Ground Mission Planning | 中 | 中 | 中高 | 后期增强，不建议单独第一篇 |

核心判断：

- UAV + UGV 语义地图协同已有强相关工作，因此“UAV 给地面机器人一张语义地图”不是新 idea。
- “自然语言指定空地协同任务 + LLM planner + semantic-metric map”也已有近期工作，因此单纯加 LLM 不是新 idea。
- 仍有空间的是：用 Go2-W 轮足平台做真实搜索-导航-验证闭环，把任务阶段、语义地图、通信机会、低层可靠执行和评测指标统一起来。
- 最容易出成果的第一步是系统型论文，而不是重算法论文。先把真实系统做扎实，再逐步加入 HRL/LLM。

## 1. 已有相关工作梳理

### 1.1 空地语义协同

**Stronger Together: Air-Ground Robotic Collaboration Using Semantics**  
arXiv: https://arxiv.org/abs/2206.14289

该工作提出端到端异构空地系统：UAV 实时构建语义地图，地面机器人基于该地图定位、规划和导航。它还使用 aerial-ground cross-view localization 和分布式机会通信，在真实环境和仿真中都做了较大规模实验。

对你的启发：

- 语义地图是空地协同的核心通信媒介。
- UAV 的价值不只是拍照，而是把高空视角转成地面机器人可执行的任务信息。
- 如果你的论文只做“UAV 建图，Go2-W 用图导航”，会和这篇高度重合。

### 1.2 SPOMP：语义全景在线建图与规划

**Air-Ground Collaboration with SPOMP: Semantic Panoramic Online Mapping and Planning**  
arXiv: https://arxiv.org/abs/2407.09902

该工作强调地图不应只包含几何和视觉信息，而应成为多机器人协同中的语义通信介质。它面向户外 2.5D 环境，支持复杂协同任务、GPS-denied 定位和大规模真实/仿真实验。

对你的启发：

- 语义地图共享本身已经是明确研究线。
- 后续差异化要放在“任务闭环”和“平台约束”上，例如 Go2-W 的地形可达性、目标验证、通信不稳定、任务阶段切换。

### 1.3 Language-Specified Air-Ground Missions

**Air-Ground Collaboration for Language-Specified Missions in Unknown Environments**  
arXiv: https://arxiv.org/abs/2505.09108  
项目页: https://tfr-air-ground.fcladera.com/

该工作已经实现 UAV + UGV 根据自然语言任务协同执行。系统使用 LLM-enabled planner 对在线构建并机会共享的 semantic-metric maps 进行推理，并在城乡环境中演示了多种自然语言任务和公里级导航。

对你的启发：

- “LLM + 空地语义地图 + UAV/UGV 协同”已经不是空白。
- 你不能把创新点写成“首次把 LLM 用于空地协同任务规划”。
- 可做的新点应是更具体的任务、平台和可靠执行，例如 Go2-W 轮足机器人、搜索-验证任务、低层安全执行、任务失败处理、通信受限评测。

### 1.4 ColAG：UAV 辅助感知受限 UGV 导航

**ColAG: A Collaborative Air-Ground Framework for Perception-Limited UGVs' Navigation**  
arXiv: https://arxiv.org/abs/2310.13324  
代码: https://github.com/FAST-FIRE/ColAG

ColAG 关注一架具备完整感知能力的 UAV 如何帮助一组感知受限甚至“盲”的 UGV 在未知障碍环境中导航。UAV 进行 SLAM 和建图，通过有限相对位姿估计向 UGV 共享信息，UGV 在接收地图中规划路径，并预测可能失败区域。该系统包含仿真和真实实验。

对你的启发：

- UAV 辅助 UGV 导航已有系统工作，且有开源代码可借鉴。
- 差异化可以是：不是“盲 UGV 导航”，而是 Go2-W 的地面目标验证、复杂地形通过、语义目标状态确认。
- 可以把 ColAG 作为强 baseline 或工程参考。

### 1.5 UAV-Quadruped 分层 MARL 搜救

**Multi-stage hierarchical multi-agent reinforcement learning for UAV-quadruped completing search and rescue**  
Springer Discover Robotics, 2026: https://link.springer.com/article/10.1007/s44430-026-00026-4

该工作使用 UAV + ANYmal-C 机器狗完成搜救任务，基于 Isaac Lab，采用多阶段分层 MARL。论文中 UAV 负责搜索和引导，四足机器人完成跟随/救援。需要注意，它的“hierarchy”主要是分阶段训练和任务依赖，并不等同于经典 option/subgoal HRL。

对你的启发：

- UAV + 四足/轮足机器人 + SAR 已经有近期工作。
- 纯仿真 MAPPO/分阶段训练不够新。
- 如果你能用真实 Go2-W 和真实场地做语义搜索-验证，会比纯仿真 MHMARL 更有差异化。

### 1.6 UAV 任务级分层 RL

相关工作包括：

- **Rule-based High-Level Coaching for Goal-Conditioned RL in SAR UAV Missions**，arXiv 2026: https://arxiv.org/abs/2604.26833
- **Phase-Aware Hierarchical RL with Dynamic Human-AI Authority Allocation for Mountain SAR**，Drones 2026: https://www.mdpi.com/2504-446X/10/4/229
- **Energy-Aware Hierarchical RL for Search and Rescue Aerial Robots**，Drones 2024: https://www.mdpi.com/2504-446X/8/7/283/html
- **RESC: Search-to-Control Framework for Quadrotor Local Planning**，arXiv 2024: https://arxiv.org/abs/2408.00275

这些工作说明：UAV 任务级分层、SAR 阶段划分、规则高层指导、搜索到控制的桥接都已有基础。你的新颖性不应是“提出 HRL for UAV mission”，而应是：

- 面向真实 UAV-Go2-W 系统；
- 高层决策只处理任务阶段、目标选择、角色切换；
- 低层由 PX4/Nav2/Go2 SDK 等可靠执行；
- 使用真实场地指标验证任务链。

### 1.7 LLM 机器人任务规划

相关工作包括：

- **Air-Ground Collaboration for Language-Specified Missions**，空地系统方向最直接。
- **SayPlan: Grounding LLMs using 3D Scene Graphs for Scalable Task Planning**: https://huggingface.co/papers/2307.06135
- **DELTA: Decomposed Efficient Long-Term Robot Task Planning using LLMs**: https://delta-llm.github.io/

这类工作共同说明：LLM 适合做高层语义任务解析、场景图推理、长程任务分解，但必须接入形式化规划、经典路径规划或安全检查，不能让 LLM 直接输出底层控制。

## 2. Idea 1：UAV-Go2-W 语义搜索与验证

### 2.1 题目建议

英文题目：

```text
Semantic Air-Ground Search and Verification with a UAV and a Wheel-Legged Robot
```

中文题目：

```text
面向真实部署的 UAV-Go2-W 语义搜索与地面验证系统
```

### 2.2 核心问题

UAV 能快速获得全局视野，但无法近距离验证目标，也容易受到视角、遮挡和误检影响。Go2-W 能近距离观察和穿越地面复杂环境，但全局感知差、搜索效率低。

研究问题：

```text
如何让 UAV 的全局语义感知转化为 Go2-W 可执行的地面验证任务，
并在真实场地中可靠完成“搜索-导航-验证”的闭环？
```

### 2.3 是否是新的 idea

结论：**不是完全新，但有可做的新颖落点。**

已有工作已经覆盖：

- UAV 构建语义地图辅助 UGV 导航；
- 空地机器人共享 semantic-metric map；
- 自然语言指定空地任务；
- UAV + quadruped 搜救仿真。

你的潜在新颖性在于：

1. **Go2-W 轮足平台的真实部署。**  
   现有强相关工作多使用普通 UGV、ANYmal-C 仿真或特定实验平台。Go2-W 有轮足混合运动特性，适合强调地形可达性和近距离验证。

2. **任务从 navigation 扩展到 search-navigation-verification。**  
   不只是“到某个点”，而是 UAV 发现疑似目标，Go2-W 接近并确认目标真假，系统需要处理 false positive、遮挡、可达性和验证结果回传。

3. **语义地图加入任务状态。**  
   地图不只包含障碍和类别，还包含目标置信度、验证状态、Go2-W 可达性、风险区域、地图新鲜度。

4. **真实系统指标更完整。**  
   以 verification success rate、time to verification、human intervention count、communication cost、map latency 为核心指标，比单纯 navigation success 更有论文辨识度。

### 2.4 技术实现路线

推荐系统架构：

```text
Mission Input / Target Definition
        |
        v
Task Manager / Behavior Tree
        |
        +--------------------------+
        |                          |
        v                          v
UAV Perception Node          Go2-W Mission Node
        |                          |
        v                          v
Semantic Mapping Node <--> Shared Semantic Map <--> Go2-W Navigation / Verification
        |
        v
Target Queue / Verification State
```

#### 模块 A：UAV 语义搜索

输入：

- UAV 图像或视频；
- UAV 位姿；
- 地图坐标系；
- 目标类别或目标描述。

实现：

- 初期可用 YOLO / GroundingDINO / Segment Anything 做目标检测与分割。
- 通过 UAV 位姿和地面投影，把检测结果映射到全局 2.5D/栅格地图。
- 输出候选目标点：`target_id, class, confidence, geo_position, timestamp, image_crop`。

第一阶段不建议做复杂 3D 重建。2.5D 地图 + 语义目标点足够支撑第一篇。

#### 模块 B：共享语义地图

地图字段建议：

```text
cell:
  occupancy
  traversability
  semantic_label
  confidence
  risk_score
  last_update_time

target:
  target_id
  class / description
  confidence
  status: unverified / assigned / verified_true / verified_false / unreachable
  assigned_robot
  last_seen_time
```

实现方式：

- ROS2 topic/service 维护 semantic map；
- 地图可先用二维 grid + target list，后续再换 OctoMap / elevation map / semantic voxel；
- Go2-W 不需要接收完整原图，接收目标列表、局部地图和导航点即可。

#### 模块 C：Go2-W 地面导航与验证

输入：

- 目标点；
- 可通行地图；
- UAV 给出的目标截图或语义描述；
- Go2-W 本地感知。

实现：

- 底层导航优先用 Go2 SDK / Nav2 / 本地避障，不建议一开始用 RL 控制 Go2-W。
- Go2-W 到达目标附近后，使用本地相机进行近距离识别。
- 验证结果回写 semantic map。

验证任务可以简化成：

- 检查指定颜色/形状目标；
- 检查异常物体；
- 检查二维码/AprilTag；
- 检查模拟伤员/箱体/标志牌。

#### 模块 D：任务管理器

初期建议使用行为树或有限状态机，不要一开始上 MARL。

状态：

```text
UAV_SEARCH
TARGET_DETECTED
ASSIGN_GO2
GO2_NAVIGATE
GO2_VERIFY
UAV_REOBSERVE
TASK_COMPLETE
TASK_FAILED
```

决策逻辑：

- 多目标时选择高置信度、低距离、Go2 可达性高的目标；
- Go2 路径失败时，请求 UAV 重观察或换目标；
- UAV 发现更高优先级目标时重新排序；
- 地图过期时触发 UAV 更新。

### 2.5 实验设计

#### 场景设置

Level 1：离线地图  
UAV 先飞一圈生成地图，Go2-W 离线接收地图并导航验证。

Level 2：在线目标更新  
UAV 在线搜索，发现目标后实时下发给 Go2-W。

Level 3：遮挡与误检  
加入 false positive、遮挡目标、不可达目标。

Level 4：通信受限  
限制地图更新频率或消息大小。

#### Baseline

- UAV-only search：只由 UAV 搜索和判断。
- Go2-only search：Go2-W 自行搜索。
- Manual assignment：人工指定 Go2-W 目标。
- Rule-based nearest target：选择最近目标。
- Semantic task manager：你的方法。

#### 指标

| 指标 | 含义 |
|---|---|
| verification success rate | 真实目标被 Go2-W 正确验证的比例 |
| time to first verification | 首个目标完成验证时间 |
| total mission time | 完成全部目标验证时间 |
| false positive recovery | UAV 误检后系统纠正能力 |
| unreachable target handling | 不可达目标识别与重规划能力 |
| communication cost | 地图/目标状态传输数据量 |
| human intervention count | 人工介入次数 |
| map update latency | UAV 更新到 Go2-W 可用的延迟 |

### 2.6 风险评估

| 风险 | 严重性 | 缓解方式 |
|---|---:|---|
| 真实 UAV 定位和地图对齐不稳定 | 高 | 第一阶段用 AprilTag/GPS/已知场地坐标简化 |
| Go2-W 导航调试时间长 | 高 | 先用离线目标点和简单平地场景 |
| 语义检测误差影响系统 | 中 | 把误检作为任务变量，而不是试图完全消除 |
| 创新被认为偏系统集成 | 中 | 强化 search-navigation-verification 任务定义和指标体系 |

### 2.7 适合投稿

- ICRA / IROS system paper
- IEEE RA-L
- Field Robotics
- IEEE Transactions on Field Robotics

## 3. Idea 4：Hierarchical UAV Mission RL

### 3.1 题目建议

```text
Hierarchical Decision Making for Long-Horizon UAV Search-and-Return Missions
```

或更贴合你的主线：

```text
Task-Level Hierarchical Policy for UAV-Assisted Search and Ground Verification
```

### 3.2 核心问题

普通 UAV RL 常常只处理轨迹跟踪或避障，但真实任务是长程任务链：

```text
起飞 -> 搜索 -> 发现目标 -> 接近/重观察 -> 分配地面机器人 -> 中继/等待 -> 返航/降落
```

研究问题：

```text
如何把 UAV 的低层飞行控制和高层任务决策分离，
让学习模块只处理任务阶段、子目标和角色选择？
```

### 3.3 是否是新的 idea

结论：**单独做 HRL for UAV mission 不够新，但作为空地系统的任务决策模块有价值。**

已有工作已经覆盖：

- UAV SAR 的阶段划分；
- rule-based high-level coaching + low-level RL；
- 能量感知 HRL；
- 搜索/跟踪两阶段 DRL；
- UAV + quadruped 的分阶段 MARL。

可做的新颖点：

1. **任务级而非控制级 HRL。**  
   学习模块不输出电机或速度，而输出任务 mode、目标选择和 UAV-Go2-W 角色。

2. **与真实空地系统绑定。**  
   HRL 不是在 toy grid world 中追求 reward，而是服务真实 search-verification 系统。

3. **任务阶段可解释。**  
   将状态设计为 search、reobserve、relay、assign、return 等人可理解阶段，便于安全审查和系统调试。

4. **低层可替换。**  
   UAV 低层由 PX4/MPC/轨迹规划器执行，Go2-W 由 Nav2/Go2 SDK 执行，HRL 只管理任务。

### 3.4 技术路线

#### 层级结构

```text
High-Level Policy, 1-2 Hz
  action:
    mode: search / reobserve / relay / assign_go2 / return
    target_id
    waypoint region
    map_update_priority

Mid-Level Planner, 5-10 Hz
  action:
    waypoint / trajectory / coverage path

Low-Level Controller, 50-250 Hz
  PX4 / MPC / PID / Go2 SDK / Nav2
```

#### 状态设计

高层 observation：

```text
UAV:
  pose, battery, distance_to_home, coverage_ratio

Targets:
  top-k target confidence
  target age
  target distance
  verification status

Go2-W:
  pose, navigation state, availability, distance_to_target

Map:
  explored_area
  stale_area_ratio
  communication_quality
```

#### 动作设计

离散动作优先：

```text
SEARCH_REGION_i
REOBSERVE_TARGET_i
ASSIGN_GO2_TARGET_i
ACT_AS_RELAY
RETURN_HOME
WAIT
```

不建议直接输出连续控制，原因是：

- 训练难度高；
- 安全风险大；
- 与 PX4/Nav2 边界不清；
- 审稿人会质疑真实部署。

#### 算法选择

第一阶段：

- rule-based task manager；
- behavior tree；
- finite-state machine。

第二阶段：

- PPO / DQN 做离散高层策略；
- goal-conditioned RL；
- imitation learning from rule-based planner。

第三阶段：

- hierarchical policy + learned communication trigger；
- multi-agent extension：UAV policy + Go2-W task policy。

### 3.5 实验设计

仿真优先，真实验证小规模。

任务：

1. 单目标搜索验证。
2. 多目标排序与验证。
3. 目标误检与重观察。
4. Go2-W 正在导航时 UAV 继续搜索或中继。
5. 电量不足时返航决策。

Baseline：

- fixed search pattern + nearest target assignment；
- behavior tree；
- flat PPO；
- high-level PPO / DQN；
- oracle planner，作为上界。

指标：

- task success rate；
- mission time；
- verified targets per minute；
- unnecessary Go2 trips；
- UAV energy usage；
- map staleness；
- policy intervention count；
- sim-to-real behavior consistency。

### 3.6 风险评估

| 风险 | 严重性 | 缓解方式 |
|---|---:|---|
| HRL 容易被认为只是工程分层 | 中 | 明确学习高层任务策略，并做 behavior tree / flat policy 对比 |
| reward 设计复杂 | 中高 | 先用 imitation from rule-based，再 RL fine-tune |
| 仿真到真实差距 | 中 | 高层离散策略降低 sim-to-real 难度 |
| 单独成文创新不足 | 中 | 绑定 UAV-Go2-W search-verification 主线 |

### 3.7 推荐定位

不建议第一篇只写：

```text
Hierarchical RL for UAV Mission Planning
```

更建议作为第一篇系统论文中的一个模块，或第二篇论文扩展为：

```text
Task-Level Hierarchical Policy for Air-Ground Search and Verification
```

## 4. Idea 5：LLM-Assisted Air-Ground Mission Planning

### 4.1 题目建议

```text
LLM-Assisted Air-Ground Mission Planning with Semantic Maps and Reliable Low-Level Execution
```

更稳妥的题目：

```text
Language-Guided Air-Ground Search and Verification with Safety-Checked Task Execution
```

### 4.2 核心问题

用户希望用自然语言描述任务，例如：

```text
检查操场西侧红色帐篷附近是否有异常物体。
先让无人机搜索，再让 Go2-W 靠近确认。
如果路被挡住，让无人机重新观察附近区域。
```

研究问题：

```text
如何把自然语言任务转换为可验证、可执行、可回退的空地机器人任务计划？
```

### 4.3 是否是新的 idea

结论：**LLM + air-ground mission planning 已有直接相关工作，单独做不新；与 Go2-W 真实验证和安全执行结合仍有空间。**

已有工作已经覆盖：

- LLM-enabled planner；
- semantic-metric map reasoning；
- UAV/UGV language-specified mission；
- dynamic mission changes；
- scene graph grounded LLM planning；
- formal planner + LLM decomposition。

可做的新颖点：

1. **语言任务落到搜索-验证闭环。**  
   LLM 不只是规划路径，而要决定“哪些目标需要 UAV 搜索，哪些需要 Go2-W 近距验证”。

2. **LLM 输出中间表示，而不是直接控制。**  
   例如输出 DSL / JSON / PDDL-like task graph，再由任务管理器验证和执行。

3. **安全与可执行性检查。**  
   所有 LLM 计划必须经过地图可达性、机器人能力、任务前置条件和低层控制接口检查。

4. **真实场地失败处理。**  
   当 Go2-W 无法到达、UAV 地图过期、目标消失时，LLM/任务管理器需要重规划。

### 4.4 技术路线

#### LLM 不应做的事

不建议：

```text
LLM -> 直接输出速度 / 电机 / waypoint stream
```

原因：

- 实时性不足；
- 不可验证；
- 安全风险大；
- 实验不可控。

#### LLM 应做的事

推荐：

```text
Natural Language Mission
        |
        v
LLM Mission Parser
        |
        v
Task DSL / JSON Plan
        |
        v
Plan Validator
        |
        v
Behavior Tree / Task Manager
        |
        v
UAV + Go2-W Execution
```

#### 中间表示示例

```json
{
  "mission": "search_and_verify",
  "target_description": "red box near the west gate",
  "constraints": {
    "uav_first": true,
    "go2_verify_required": true,
    "avoid_regions": ["construction_area"],
    "max_mission_time_min": 15
  },
  "steps": [
    {
      "actor": "uav",
      "action": "search_region",
      "region": "west_gate"
    },
    {
      "actor": "uav",
      "action": "publish_candidate_targets",
      "min_confidence": 0.6
    },
    {
      "actor": "go2",
      "action": "navigate_and_verify",
      "target_selector": "highest_confidence_reachable"
    }
  ],
  "fallbacks": [
    {
      "condition": "go2_unreachable",
      "action": "uav_reobserve"
    },
    {
      "condition": "target_not_found",
      "action": "expand_search_region"
    }
  ]
}
```

#### Plan Validator

必须检查：

- 目标描述是否能映射到感知模型类别；
- 区域是否存在于地图；
- Go2-W 是否可达；
- UAV 电量是否足够；
- 任务步骤是否满足前置条件；
- fallback 是否定义完整。

#### 任务执行

LLM 输出计划后，由 behavior tree 执行。执行中如果状态变化，不一定每次都调用 LLM；优先由本地任务管理器处理常见异常。LLM 只在任务语义变化或需要重新解释用户意图时介入。

### 4.5 实验设计

任务集：

| 类型 | 示例 |
|---|---|
| 简单目标验证 | “检查 A 区域的红色箱子” |
| 多目标优先级 | “先检查靠近建筑入口的目标” |
| 条件任务 | “如果发现疑似目标，让 Go2-W 去确认” |
| 动态修改 | “不要检查东侧，改去西侧” |
| 失败恢复 | “如果 Go2-W 到不了，让 UAV 从低空重新观察” |

Baseline：

- manual scripted task；
- rule-based parser；
- LLM direct plan without validator；
- LLM + validator；
- LLM + validator + behavior tree feedback。

指标：

- language instruction success rate；
- executable plan rate；
- invalid action count；
- replanning count；
- task completion time；
- safety violation；
- human correction count；
- LLM token cost and latency。

### 4.6 风险评估

| 风险 | 严重性 | 缓解方式 |
|---|---:|---|
| 与 2025 language-specified air-ground work 太像 | 高 | 强调 Go2-W、search-verification、可靠执行和验证指标 |
| LLM demo 味太重 | 高 | 必须绑定真实机器人闭环和 quantitative experiments |
| LLM 输出不稳定 | 中 | 使用固定 DSL、schema validation、plan repair |
| API 延迟/网络依赖 | 中 | LLM 只低频调用，常见任务缓存模板 |

### 4.7 推荐定位

不建议作为第一篇主线。更适合作为：

- 第一篇系统论文的增强接口；
- 第二/第三篇扩展；
- demo 和就业包装亮点。

论文中应强调：

```text
LLM is a mission interface, not the autonomy core.
```

## 5. 三个方向如何组合成一条论文路线

### 5.1 第一阶段：系统基线论文

题目：

```text
Semantic Air-Ground Search and Verification with a UAV and a Wheel-Legged Robot
```

目标：

- 真实 UAV + Go2-W 跑通；
- UAV 生成语义目标；
- Go2-W 完成地面验证；
- 行为树/规则任务管理；
- 真实场地实验。

贡献：

1. UAV-Go2-W search-navigation-verification 系统。
2. 共享语义地图和目标验证状态表示。
3. 真实场地评测协议和 baseline。

### 5.2 第二阶段：任务级分层学习

题目：

```text
Task-Level Hierarchical Learning for Air-Ground Search and Verification
```

目标：

- 用高层 RL 替代部分规则任务管理；
- 学习目标排序、UAV 继续搜索/中继/重观察决策；
- 低层仍使用可靠控制器。

贡献：

1. 高层离散任务策略。
2. 与 behavior tree、flat policy、oracle planner 对比。
3. sim-to-real 高层策略迁移。

### 5.3 第三阶段：语言任务接口

题目：

```text
Language-Guided Air-Ground Search and Verification with Safety-Checked Execution
```

目标：

- 自然语言 -> DSL -> plan validation -> behavior tree；
- 支持任务动态修改；
- 支持失败后语义重规划。

贡献：

1. 面向空地搜索验证任务的语言任务表示。
2. LLM 计划验证与安全执行机制。
3. 真实场地语言任务 benchmark。

## 6. 推荐最小可行实验

### 6.1 4 周原型

目标：证明第一篇系统论文可行。

工作：

1. 搭建 ROS2 任务框架。
2. UAV 用离线航拍图或固定高度飞行图像生成目标点。
3. Go2-W 接收目标点并导航到附近。
4. Go2-W 本地摄像头验证目标。
5. 记录 time to verification、success rate、人工介入次数。

允许简化：

- UAV 可以先用手动飞行或预设轨迹；
- 地图可以先用 2D 场地坐标；
- 目标可以用 AprilTag/彩色物体；
- 语义检测可以先离线。

### 6.2 3 个月实验

目标：形成系统论文主体。

工作：

1. 在线 UAV 目标发现。
2. 共享 semantic target map。
3. 多目标排序和 Go2-W 任务分配。
4. 三组 baseline。
5. 真实场地 20-50 次任务测试。

### 6.3 6 个月扩展

目标：加入 HRL 或 LLM。

二选一：

- HRL：学习目标排序、重观察、中继、返航等高层决策。
- LLM：自然语言任务 -> DSL -> validator -> behavior tree。

不建议两个都同时做，容易失控。

## 7. 最终建议

如果你对 1、4、5 都感兴趣，最稳的路线是：

```text
第一篇：UAV-Go2-W 语义搜索与验证系统
第二篇：任务级分层学习，提高搜索-验证效率
第三篇：LLM 语言任务接口，提高人机交互和开放任务能力
```

现在最该做的不是先训练复杂模型，而是先把任务定义和系统闭环跑通：

```text
UAV 发现目标 -> 语义地图发布 -> Go2-W 接收目标 -> 地面导航 -> 近距验证 -> 结果回写
```

只要这个闭环能在真实场地稳定运行，后续 HRL 和 LLM 都有自然落点。反过来，如果没有这个闭环，单独做 HRL 或 LLM 很容易变成仿真 demo，论文说服力不足。

## 8. 参考链接

1. Stronger Together: Air-Ground Robotic Collaboration Using Semantics  
   https://arxiv.org/abs/2206.14289
2. Air-Ground Collaboration with SPOMP: Semantic Panoramic Online Mapping and Planning  
   https://arxiv.org/abs/2407.09902
3. Air-Ground Collaboration for Language-Specified Missions in Unknown Environments  
   https://arxiv.org/abs/2505.09108
4. Air-Ground Collaboration project page  
   https://tfr-air-ground.fcladera.com/
5. ColAG: A Collaborative Air-Ground Framework for Perception-Limited UGVs' Navigation  
   https://arxiv.org/abs/2310.13324
6. ColAG GitHub  
   https://github.com/FAST-FIRE/ColAG
7. Multi-stage hierarchical multi-agent reinforcement learning for UAV-quadruped completing search and rescue  
   https://link.springer.com/article/10.1007/s44430-026-00026-4
8. Rule-based High-Level Coaching for Goal-Conditioned RL in SAR UAV Missions  
   https://arxiv.org/abs/2604.26833
9. Phase-Aware Hierarchical Reinforcement Learning with Dynamic Human-AI Authority Allocation for Mountain SAR  
   https://www.mdpi.com/2504-446X/10/4/229
10. Energy-Aware Hierarchical Reinforcement Learning for SAR Aerial Robots  
    https://www.mdpi.com/2504-446X/8/7/283/html
11. RESC: A Reinforcement Learning Based Search-to-Control Framework for Quadrotor Local Planning  
    https://arxiv.org/abs/2408.00275
12. SayPlan: Grounding LLMs using 3D Scene Graphs for Scalable Task Planning  
    https://huggingface.co/papers/2307.06135
13. DELTA: Decomposed Efficient Long-Term Robot Task Planning using LLMs  
    https://delta-llm.github.io/
