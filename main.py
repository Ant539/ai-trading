#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Alpha Arena MVP - 主程序
最简化的AI交易决策对比系统
"""

import os
import sys
from datetime import datetime
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# 添加当前目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from core.market import MarketData
from core.decision import DecisionMaker
from adapters.qwen_adapter import QwenAdapter


def main():
    """主函数"""
    print("🚀 Alpha Arena - 最简化MVP")
    print("=" * 50)
    print(f"📅 运行时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()

    try:
        # 初始化市场数据管理器
        print("📊 初始化市场数据管理器...")
        market_data = MarketData()

        if not market_data.is_api_available():
            print("❌ 交易所API不可用，请检查配置")
            return

        # 获取实时价格
        print("💰 获取实时价格...")
        prices = market_data.get_current_prices()

        print("\n📈 当前市场价格:")
        print(market_data.format_prices_for_display(prices))

        # 检查是否有有效价格
        valid_prices = {k: v for k, v in prices.items() if v > 0}
        if not valid_prices:
            print("❌ 没有获取到有效价格，请检查网络连接")
            return

        # 初始化LLM适配器
        print("\n🤖 初始化AI模型...")

        # Qwen适配器
        try:
            qwen_adapter = QwenAdapter(model="qwen3-max")
            qwen_decision_maker = DecisionMaker(qwen_adapter)
            print(f"✅ Qwen ({qwen_adapter.get_model_name()}) 初始化成功")
        except Exception as e:
            print(f"❌ Qwen初始化失败: {e}")
            qwen_decision_maker = None

        # Deepseek适配器
        try:
            deepseek_adapter = QwenAdapter(model="deepseek-v3.1")
            deepseek_decision_maker = DecisionMaker(deepseek_adapter)
            print(f"✅ Deepseek ({deepseek_adapter.get_model_name()}) 初始化成功")
        except Exception as e:
            print(f"❌ Deepseek初始化失败: {e}")
            deepseek_decision_maker = None

        if not qwen_decision_maker and not deepseek_decision_maker:
            print("❌ 没有可用的AI模型，请检查API密钥配置")
            return

        # 获取AI决策
        print("\n🧠 获取AI交易决策...")

        decisions = {}

        # Qwen决策
        if qwen_decision_maker:
            print("\n🤖 Qwen决策:")
            try:
                qwen_decision = qwen_decision_maker.get_decision(prices)
                decisions['Qwen'] = qwen_decision
                print(qwen_decision_maker.format_decision_for_display(qwen_decision))
            except Exception as e:
                print(f"❌ Qwen决策获取失败: {e}")

        # Deepseek-决策
        if deepseek_decision_maker:
            print("\n🤖 Deepseek决策:")
            try:
                deepseek_decision = deepseek_decision_maker.get_decision(prices)
                decisions['Deepseek'] = deepseek_decision
                print(deepseek_decision_maker.format_decision_for_display(deepseek_decision))
            except Exception as e:
                print(f"❌ Deepseek决策获取失败: {e}")

        # 决策对比
        if len(decisions) >= 2:
            print("\n📊 决策对比:")
            print("-" * 30)

            for model_name, decision in decisions.items():
                symbol = decision.get('symbol', 'None')
                action = decision.get('action', 'HOLD')
                print(f"   {model_name}: {action} {symbol}")

            # 检查是否一致
            if len(decisions) == 2:
                qwen_decision = decisions.get('Qwen', {})
                deepseek_decision = decisions.get('Deepseek', {})

                if (qwen_decision.get('symbol') == deepseek_decision.get('symbol') and
                        qwen_decision.get('action') == deepseek_decision.get('action')):
                    print("   🎯 两个AI达成一致！")
                else:
                    print("   ⚡ 两个AI意见分歧")

        print("\n✅ 运行完成！")

    except KeyboardInterrupt:
        print("\n\n⏹️ 用户中断程序")
    except Exception as e:
        print(f"\n❌ 程序运行出错: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
