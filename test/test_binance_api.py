#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
币安API测试脚本
测试 Binance Spot API 是否可用
"""

import os
import sys
import subprocess
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()


def get_proxy_config():
    """获取代理配置"""
    try:
        # 方法1：从环境变量读取
        http_proxy = os.getenv('http_proxy') or os.getenv('HTTP_PROXY')
        if http_proxy:
            return {
                'http': http_proxy,
                'https': http_proxy
            }
        
        # 方法2：动态获取 Windows IP
        result = subprocess.run(
            ['ip', 'route', 'show', 'default'],
            capture_output=True,
            text=True
        )
        
        for line in result.stdout.split('\n'):
            if 'default via' in line:
                ip = line.split()[2]
                proxy_url = f'http://{ip}:7897'
                return {
                    'http': proxy_url,
                    'https': proxy_url
                }
        
        return None
    except Exception as e:
        print(f"   ⚠️ 获取代理配置失败: {e}")
        return None


def check_env_variables():
    """检查环境变量配置"""
    print("🧪 测试0: 检查环境变量配置")
    print("=" * 50)

    api_key = os.getenv('BINANCE_API_KEY')
    api_secret = os.getenv('BINANCE_API_SECRET')

    print("\n📋 环境变量检查:")

    if api_key:
        masked_key = f"{api_key[:8]}...{api_key[-4:]}" if len(api_key) > 12 else "***"
        print(f"   ✅ BINANCE_API_KEY: {masked_key}")
    else:
        print(f"   ⚠️ BINANCE_API_KEY: 未设置（公开数据不需要）")

    if api_secret:
        masked_secret = f"{api_secret[:8]}...{api_secret[-4:]}" if len(api_secret) > 12 else "***"
        print(f"   ✅ BINANCE_API_SECRET: {masked_secret}")
    else:
        print(f"   ⚠️ BINANCE_API_SECRET: 未设置（公开数据不需要）")

    # 检查代理配置
    proxies = get_proxy_config()
    if proxies:
        print(f"   ✅ 代理配置: {proxies.get('http', 'N/A')}")
    else:
        print(f"   ⚠️ 代理配置: 未设置")

    print("\n💡 说明:")
    print("   - 获取公开市场价格：不需要API密钥")
    print("   - 查询账户信息/下单：需要API密钥")
    print("   - 当前测试只获取价格，可以不配置密钥")
    print("   - 国内访问币安需要代理")

    return True


def test_binance_import():
    """测试是否能导入币安SDK"""
    print("\n🧪 测试1: 检查币安SDK是否已安装")
    print("=" * 50)

    try:
        from binance.spot import Spot
        print("✅ 币安SDK导入成功")
        return True
    except ImportError as e:
        print("❌ 币安SDK未安装")
        print(f"   错误: {e}")
        print("\n💡 解决方法:")
        print("   pip install binance-connector")
        return False


def test_binance_connection_public():
    """测试币安API连接（公开数据，不需要密钥）"""
    print("\n🧪 测试2: 测试币安API连接（公开数据）")
    print("=" * 50)

    try:
        from binance.spot import Spot

        # 获取代理配置
        proxies = get_proxy_config()
        
        # 初始化客户端（不传API密钥，但传入代理）
        print("\n1️⃣ 初始化币安客户端（公开模式）...")
        if proxies:
            print(f"   🔄 使用代理: {proxies.get('http', 'N/A')}")
            client = Spot(proxies=proxies)
        else:
            print("   ⚠️ 未使用代理（可能无法连接）")
            client = Spot()
        
        print("   ✅ 客户端初始化成功")

        # 测试服务器时间（最简单的连接测试）
        print("\n2️⃣ 测试服务器连接...")
        server_time = client.time()
        print(f"   ✅ 服务器连接成功")
        print(f"   📅 服务器时间戳: {server_time['serverTime']}")

        # 转换时间戳为可读格式
        from datetime import datetime
        readable_time = datetime.fromtimestamp(server_time['serverTime'] / 1000)
        print(f"   🕐 本地时间: {readable_time.strftime('%Y-%m-%d %H:%M:%S')}")

        return True

    except Exception as e:
        print(f"   ❌ 连接失败: {e}")
        print("\n💡 可能的原因:")
        print("   1. 代理未启动或配置错误")
        print("   2. 币安服务暂时不可用")
        print("   3. 防火墙限制")
        print("\n💡 解决方法:")
        print("   1. 确保 Clash Verge 正在运行")
        print("   2. 运行: source ~/.bashrc  # 加载代理环境变量")
        print("   3. 测试代理: curl --proxy http://172.18.48.1:7897 https://api.binance.com/api/v3/time")
        return False


def test_binance_connection_authenticated():
    """测试币安API连接（认证模式，需要密钥）"""
    print("\n🧪 测试3: 测试币安API连接（认证模式）")
    print("=" * 50)

    api_key = os.getenv('BINANCE_API_KEY')
    api_secret = os.getenv('BINANCE_API_SECRET')

    if not api_key or not api_secret:
        print("   ⚠️ 未配置API密钥，跳过认证测试")
        print("   💡 如需测试认证功能，请在.env中配置:")
        print("      BINANCE_API_KEY=your_api_key")
        print("      BINANCE_API_SECRET=your_api_secret")
        return None  # None表示跳过

    try:
        from binance.spot import Spot

        # 获取代理配置
        proxies = get_proxy_config()

        print("\n1️⃣ 初始化币安客户端（认证模式）...")
        if proxies:
            print(f"   🔄 使用代理: {proxies.get('http', 'N/A')}")
            client = Spot(api_key=api_key, api_secret=api_secret, proxies=proxies)
        else:
            client = Spot(api_key=api_key, api_secret=api_secret)
        
        print("   ✅ 客户端初始化成功")

        print("\n2️⃣ 测试账户连接...")
        # 获取账户信息（需要认证）
        account_info = client.account()
        print("   ✅ 账户连接成功")
        print(f"   📊 账户类型: {account_info.get('accountType', 'N/A')}")
        print(f"   🔐 是否可交易: {account_info.get('canTrade', False)}")

        return True

    except Exception as e:
        print(f"   ❌ 认证失败: {e}")
        print("\n💡 可能的原因:")
        print("   1. API密钥错误")
        print("   2. API密钥权限不足")
        print("   3. IP未加入白名单")
        return False


def test_get_single_price():
    """测试获取单个代币价格"""
    print("\n🧪 测试4: 获取单个代币价格")
    print("=" * 50)

    try:
        from binance.spot import Spot
        
        # 获取代理配置
        proxies = get_proxy_config()
        client = Spot(proxies=proxies) if proxies else Spot()

        # 测试BTC价格
        symbol = 'BTCUSDT'
        print(f"\n1️⃣ 获取 {symbol} 价格...")

        result = client.ticker_price(symbol)
        price = float(result['price'])

        print(f"   ✅ 获取成功")
        print(f"   💰 {symbol}: ${price:,.2f}")
        print(f"   📦 原始数据: {result}")

        return True

    except Exception as e:
        print(f"   ❌ 获取失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_get_multiple_prices():
    """测试获取多个代币价格"""
    print("\n🧪 测试5: 获取多个代币价格")
    print("=" * 50)

    try:
        from binance.spot import Spot
        
        # 获取代理配置
        proxies = get_proxy_config()
        client = Spot(proxies=proxies) if proxies else Spot()

        # 测试多个代币
        symbols = ['BTCUSDT', 'ETHUSDT', 'BNBUSDT', 'SOLUSDT']

        print(f"\n1️⃣ 获取 {len(symbols)} 个代币价格...")

        prices = {}
        for symbol in symbols:
            try:
                result = client.ticker_price(symbol)
                price = float(result['price'])
                prices[symbol] = price
                print(f"   ✅ {symbol}: ${price:,.2f}")
            except Exception as e:
                print(f"   ❌ {symbol}: 获取失败 - {e}")
                prices[symbol] = 0.0

        # 统计
        success_count = sum(1 for p in prices.values() if p > 0)
        print(f"\n📊 统计: 成功 {success_count}/{len(symbols)}")

        return success_count > 0

    except Exception as e:
        print(f"   ❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_get_all_prices():
    """测试获取所有交易对价格（可选）"""
    print("\n🧪 测试6: 获取所有交易对价格（批量）")
    print("=" * 50)

    try:
        from binance.spot import Spot
        
        # 获取代理配置
        proxies = get_proxy_config()
        client = Spot(proxies=proxies) if proxies else Spot()

        print("\n1️⃣ 获取所有交易对价格...")

        # 不传参数，获取所有交易对
        all_prices = client.ticker_price()

        print(f"   ✅ 获取成功")
        print(f"   📊 总共 {len(all_prices)} 个交易对")

        # 显示前5个USDT交易对
        print("\n   📈 部分USDT交易对价格:")
        usdt_pairs = [p for p in all_prices if p['symbol'].endswith('USDT')][:5]
        for pair in usdt_pairs:
            symbol = pair['symbol']
            price = float(pair['price'])
            print(f"      {symbol}: ${price:,.4f}")

        return True

    except Exception as e:
        print(f"   ❌ 获取失败: {e}")
        return False


def test_error_handling():
    """测试错误处理"""
    print("\n🧪 测试7: 错误处理")
    print("=" * 50)

    try:
        from binance.spot import Spot
        
        # 获取代理配置
        proxies = get_proxy_config()
        client = Spot(proxies=proxies) if proxies else Spot()

        # 测试无效的交易对
        print("\n1️⃣ 测试无效交易对...")
        try:
            result = client.ticker_price('INVALIDUSDT')
            print(f"   ⚠️ 意外成功: {result}")
        except Exception as e:
            print(f"   ✅ 正确捕获错误: {type(e).__name__}")
            print(f"   📝 错误信息: {str(e)[:100]}")

        return True

    except Exception as e:
        print(f"   ❌ 测试失败: {e}")
        return False


def main():
    """主测试函数"""
    print("🚀 币安API测试套件")
    print("=" * 50)
    print()

    results = []

    # 测试0: 环境变量检查
    check_env_variables()
    results.append(("环境变量检查", True))

    # 测试1: 导入检查
    if not test_binance_import():
        print("\n❌ 请先安装币安SDK:")
        print("   pip install binance-connector")
        print_summary(results)
        return

    results.append(("SDK导入检查", True))

    # 测试2: 公开连接测试
    connection_ok = test_binance_connection_public()
    results.append(("公开API连接", connection_ok))

    if not connection_ok:
        print("\n⚠️ 网络连接失败，跳过后续测试")
        print_summary(results)
        return

    # 测试3: 认证连接测试（可选）
    auth_result = test_binance_connection_authenticated()
    if auth_result is not None:
        results.append(("认证API连接", auth_result))

    # 测试4: 单个价格
    results.append(("单个价格", test_get_single_price()))

    # 测试5: 多个价格
    results.append(("多个价格", test_get_multiple_prices()))

    # 测试6: 所有价格（可选）
    results.append(("批量价格", test_get_all_prices()))

    # 测试7: 错误处理
    results.append(("错误处理", test_error_handling()))

    # 打印总结
    print_summary(results)


def print_summary(results):
    """打印测试总结"""
    print("\n" + "=" * 50)
    print("📊 测试总结")
    print("=" * 50)

    for test_name, success in results:
        status = "✅" if success else "❌"
        print(f"{status} {test_name}")

    success_count = sum(1 for _, success in results if success)
    total_count = len(results)

    print("\n" + "=" * 50)
    print(f"总计: {success_count}/{total_count} 通过")

    if success_count == total_count:
        print("🎉 所有测试通过！可以使用币安API")
    elif success_count > 0:
        print("⚠️ 部分测试通过，请检查失败的测试")
    else:
        print("❌ 所有测试失败，请检查网络和配置")

    print("=" * 50)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⏹️ 测试被用户中断")
    except Exception as e:
        print(f"\n❌ 测试过程出错: {e}")
        import traceback
        traceback.print_exc()
