#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Qwen适配器单元测试
测试Qwen API调用是否正常
"""

import os
import sys
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# 添加父目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from adapters.qwen_adapter import QwenAdapter


def test_qwen_basic():
    """基础测试：测试Qwen是否可以正常调用"""
    print("🧪 开始测试 Qwen 适配器")
    print("=" * 50)

    try:
        # 初始化适配器
        print("\n1️⃣ 测试初始化...")
        adapter = QwenAdapter()
        print(f"   ✅ 初始化成功")
        print(f"   📝 模型名称: {adapter.get_model_name()}")

        # 测试简单调用
        print("\n2️⃣ 测试API调用...")
        test_prompt = "请用一句话介绍你自己。"
        response = adapter.call(test_prompt)

        print(f"   ✅ API调用成功")
        print(f"   📤 测试提示: {test_prompt}")
        print(f"   📥 响应内容: {response[:100]}..." if len(response) > 100 else f"   📥 响应内容: {response}")

        # 测试交易决策调用
        print("\n3️⃣ 测试交易决策...")
        market_prompt = """
当前市场价格:
- BTC/USDT: $65000
- ETH/USDT: $3200
- BNB/USDT: $580

请分析市场并给出交易建议，返回JSON格式：
{"symbol": "交易对", "action": "BUY/SELL/HOLD", "confidence": 0.0-1.0, "rationale": "理由"}
"""
        decision_response = adapter.call(market_prompt)

        print(f"   ✅ 交易决策调用成功")
        print(f"   📥 决策响应:\n{decision_response}")

        print("\n" + "=" * 50)
        print("✅ 所有测试通过！")
        return True

    except ValueError as e:
        print(f"\n❌ 配置错误: {e}")
        print("💡 请确保在 .env 文件中设置了 QWEN_API_KEY")
        return False

    except ImportError as e:
        print(f"\n❌ 依赖错误: {e}")
        print("💡 请运行: pip install openai")
        return False

    except Exception as e:
        print(f"\n❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_qwen_error_handling():
    """测试错误处理"""
    print("\n🧪 测试错误处理")
    print("=" * 50)

    try:
        # 测试无效API密钥
        print("\n1️⃣ 测试无效API密钥...")
        try:
            adapter = QwenAdapter(api_key="invalid_key")
            response = adapter.call("测试")
            # 应该返回错误JSON而不是抛出异常
            if "API调用失败" in response or "HOLD" in response:
                print("   ✅ 错误处理正常（返回默认HOLD决策）")
            else:
                print("   ⚠️ 可能存在问题，但未崩溃")
        except Exception as e:
            print(f"   ⚠️ 抛出异常: {e}")

        print("\n" + "=" * 50)
        print("✅ 错误处理测试完成")

    except Exception as e:
        print(f"\n❌ 错误处理测试失败: {e}")


if __name__ == "__main__":
    print("🚀 Qwen 适配器测试套件")
    print()

    # 运行基础测试
    success = test_qwen_basic()

    if success:
        # 如果基础测试通过，运行错误处理测试
        test_qwen_error_handling()

    print("\n🏁 测试结束")
