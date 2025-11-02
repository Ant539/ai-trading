## Alpha Arena MVP

最简化的 AI 交易决策对比系统，用于在同一份市场数据上对比多个大模型（如 Qwen、Deepseek）的交易建议，并输出一致性与差异。

引用与致谢：
- 本项目参考并部分借鉴自：https://github.com/AmadeusGB/alpha-arena

### 功能概述
- 实时拉取交易所价格数据并格式化展示
- 同时初始化多个 LLM 适配器（Qwen、Deepseek）
- 基于同一价格快照获取各模型的交易决策
- 输出模型间的决策对比与一致性提示
- 健壮的异常处理与可读性输出

### 目录与关键组件
- core/market.MarketData
  - is_api_available(): 检查交易所 API 可用性
  - get_current_prices(): 拉取实时价格
  - format_prices_for_display(): 终端友好展示
- core/decision.DecisionMaker
  - get_decision(prices): 基于价格让模型给出决策
  - format_decision_for_display(): 统一展示格式
- adapters/qwen_adapter.QwenAdapter
  - get_model_name(): 返回当前模型名（如 qwen3-max、deepseek-v3.1）

说明：Deepseek 目前通过同一 Adapter 初始化为 model="deepseek-v3.1"。

### 运行前准备
1) 安装依赖
- 请使用 Python 3.9+，并在虚拟环境中安装项目依赖。
- 确保已安装 python-dotenv 以及各自适配器需要的 SDK/依赖。

2) 配置环境变量
- 在项目根目录创建 .env，填写相应的 API Key/访问参数（示例，按你实际键名为准）：
- Qwen、Deepseek 的 Key，交易所 API Key/Secret 等

3) 网络要求
- 能正常访问模型与交易所 API（公司/校园网络或代理环境请正确配置证书与代理）。

### 快速开始
- 直接运行主程序：
- 首次运行会输出时间、当前价格、各模型决策与对比结果。

### 输出示例
- 启动横幅与时间戳
- 价格快照展示
- 模型初始化结果（成功/失败）
- 各模型的交易建议，例如：
  - Qwen: BUY BTC
  - Deepseek: HOLD BTC
- 一致性判断：
  - 两个AI达成一致！或 两个AI意见分歧

### 常见问题
- API 不可用：检查网络与 .env 配置
- 模型初始化失败：确认对应 API Key、模型名和配额
- 无有效价格：检查网络或交易所状态

### 许可证与引用
- 本项目参考并部分借鉴自开源仓库：
  - https://github.com/AmadeusGB/alpha-arena
- 如在此基础上修改与分发，请遵循原项目的许可证要求并保留引用。