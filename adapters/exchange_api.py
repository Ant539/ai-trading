#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
交易所API适配器
支持币安(Binance)交易所
"""

import os
from typing import Dict, List, Optional
from dotenv import load_dotenv
from binance.spot import Spot
from binance.error import ClientError, ServerError

# 加载环境变量
load_dotenv()


class ExchangeAPI:
    """交易所API封装类"""

    def __init__(self):
        """初始化币安API客户端"""
        api_key = os.getenv('BINANCE_API_KEY')
        api_secret = os.getenv('BINANCE_API_SECRET')

        try:
            if api_key and api_secret:
                self.client = Spot(api_key=api_key, api_secret=api_secret)
                self.is_authenticated = True
                print("✅ 币安 API客户端初始化成功（已认证）")
            else:
                self.client = Spot()
                self.is_authenticated = False
                print("✅ 币安 API客户端初始化成功（公开接口）")
        except Exception as e:
            print(f"❌ 币安 API客户端初始化失败: {e}")
            self.client = None
            self.is_authenticated = False

    def get_current_price(self, symbol: str) -> float:
        """
        获取指定交易对的当前价格

        Args:
            symbol: 交易对符号，例如 'BTCUSDT'

        Returns:
            float: 当前价格，失败返回 0.0
        """
        if self.client is None:
            return 0.0

        try:
            result = self.client.ticker_price(symbol)
            price = float(result['price'])
            return price
        except (ClientError, ServerError) as e:
            print(f"❌ 获取{symbol}价格失败: {e}")
            return 0.0
        except Exception as e:
            print(f"❌ 获取{symbol}价格失败: {e}")
            return 0.0

    def get_single_price(self, symbol: str) -> float:
        """
        获取单个代币的价格（与get_current_price功能相同，为保持接口一致性）

        Args:
            symbol: 代币符号，如'BTCUSDT'

        Returns:
            价格
        """
        return self.get_current_price(symbol)

    def get_latest_prices(self, symbols: List[str]) -> Dict[str, float]:
        """
        获取多个代币的最新价格

        Args:
            symbols: 代币符号列表，如['BTCUSDT', 'ETHUSDT']

        Returns:
            价格字典，格式为{symbol: price}
        """
        if self.client is None:
            print("❌ API客户端未初始化")
            return {symbol: 0.0 for symbol in symbols}

        prices = {}

        # 方法1：批量获取（推荐，效率更高）
        try:
            # 币安支持不带参数获取所有交易对价格
            all_prices = self.client.ticker_price()
            price_dict = {item['symbol']: float(item['price']) for item in all_prices}

            # 提取需要的交易对
            for symbol in symbols:
                if symbol in price_dict:
                    prices[symbol] = price_dict[symbol]
                    print(f"✅ {symbol}: ${price_dict[symbol]:.4f}")
                else:
                    print(f"⚠️ {symbol} 未找到")
                    prices[symbol] = 0.0

        except Exception as e:
            print(f"⚠️ 批量获取价格失败，切换到单个获取: {e}")
            # 方法2：单个获取（降级方案）
            for symbol in symbols:
                try:
                    price = self.get_current_price(symbol)
                    prices[symbol] = price
                    if price > 0:
                        print(f"✅ {symbol}: ${price:.4f}")
                except Exception as e:
                    print(f"❌ 获取{symbol}价格失败: {e}")
                    prices[symbol] = 0.0

        return prices

    def is_available(self) -> bool:
        """
        检查API是否可用

        Returns:
            bool: API可用返回True，否则返回False
        """
        if self.client is None:
            return False

        try:
            # 方法1: 尝试获取BTC价格（最可靠的方式）
            result = self.client.ticker_price('BTCUSDT')
            return 'price' in result and float(result['price']) > 0
        except Exception as e:
            print(f"⚠️ API可用性检查失败: {e}")

            # 方法2: 降级到time接口（仅公开模式可能有效）
            try:
                self.client.time()
                return True
            except Exception:
                return False

    def test_connection(self) -> bool:
        """
        测试API连接是否正常（与is_available功能相同，保留兼容性）

        Returns:
            bool: 连接成功返回 True，否则返回 False
        """
        return self.is_available()


# 测试代码
# if __name__ == "__main__":
#     print("🧪 测试币安API...")
#     print("=" * 50)
#
#     # 初始化API
#     api = ExchangeAPI()
#
#     # 测试连接
#     print("\n📡 测试连接...")
#     if api.is_available():
#         print("✅ API连接正常")
#     else:
#         print("❌ API连接失败")
#         exit(1)
#
#     # 测试单个价格获取
#     print("\n💰 测试单个价格获取...")
#     btc_price = api.get_single_price('BTCUSDT')
#     if btc_price > 0:
#         print(f"✅ BTC价格: ${btc_price:,.2f}")
#     else:
#         print("❌ 获取BTC价格失败")
#
#     # 测试批量价格获取
#     print("\n📊 测试批量价格获取...")
#     symbols = ['BTCUSDT', 'ETHUSDT', 'BNBUSDT', 'SOLUSDT']
#     prices = api.get_latest_prices(symbols)
#
#     print("\n📈 价格汇总:")
#     print("-" * 50)
#     success_count = 0
#     for symbol, price in prices.items():
#         if price > 0:
#             print(f"   {symbol:10s}: ${price:>12,.2f}")
#             success_count += 1
#         else:
#             print(f"   {symbol:10s}: 获取失败")
#
#     print("-" * 50)
#     print(f"✅ 成功获取 {success_count}/{len(symbols)} 个价格")
#
#     if success_count == len(symbols):
#         print("\n🎉 所有测试通过！")
#     else:
#         print("\n⚠️ 部分测试失败")
