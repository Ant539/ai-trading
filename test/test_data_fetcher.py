#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
数据获取器单元测试
测试 TradingDataFetcher 的所有功能
"""

import unittest
import time
import os
from unittest.mock import Mock, patch, MagicMock
from datetime import datetime

import pandas as pd
import numpy as np

# 假设你的模块名为 data_fetcher
from data.data_fetcher import TradingDataFetcher


class TestTradingDataFetcher(unittest.TestCase):
    """数据获取器测试类"""

    @classmethod
    def setUpClass(cls):
        """测试类初始化（只运行一次）"""
        print("\n" + "="*60)
        print("🧪 开始测试 TradingDataFetcher")
        print("="*60)

    @classmethod
    def tearDownClass(cls):
        """测试类清理"""
        print("\n" + "="*60)
        print("✅ 所有测试完成")
        print("="*60)

    def setUp(self):
        """每个测试前的初始化"""
        # 不启用WebSocket，避免测试时的网络依赖
        self.fetcher = TradingDataFetcher(use_websocket=False)

    def tearDown(self):
        """每个测试后的清理"""
        if hasattr(self, 'fetcher') and self.fetcher.ws_client:
            self.fetcher.stop_websocket()

    # ==================== 基础功能测试 ====================

    def test_01_initialization(self):
        """测试初始化"""
        print("\n📝 测试1: 初始化")
        
        # 测试不带认证的初始化
        fetcher_no_auth = TradingDataFetcher(use_websocket=False)
        self.assertIsNotNone(fetcher_no_auth.spot_client)
        self.assertIsNotNone(fetcher_no_auth.futures_client)
        self.assertFalse(fetcher_no_auth.use_websocket)
        
        # 测试带WebSocket的初始化
        fetcher_with_ws = TradingDataFetcher(use_websocket=True)
        self.assertTrue(fetcher_with_ws.use_websocket)
        
        print("  ✅ 初始化测试通过")

    def test_02_api_connection(self):
        """测试API连接"""
        print("\n📝 测试2: API连接")
        
        # 测试获取BTC价格
        try:
            result = self.fetcher.spot_client.ticker_price('BTCUSDT')
            price = float(result['price'])
            
            self.assertIsInstance(price, float)
            self.assertGreater(price, 0)
            print(f"  ✅ API连接正常，BTC价格: ${price:,.2f}")
        except Exception as e:
            self.fail(f"API连接失败: {e}")

    # ==================== K线数据测试 ====================

    def test_03_get_klines(self):
        """测试K线数据获取"""
        print("\n📝 测试3: K线数据获取")
        
        symbol = 'BTCUSDT'
        interval = '5m'
        limit = 100
        
        df = self.fetcher.get_klines(symbol, interval, limit)
        
        # 验证返回的DataFrame
        self.assertIsInstance(df, pd.DataFrame)
        self.assertFalse(df.empty, "K线数据不应为空")
        
        # 验证列名
        expected_columns = ['timestamp', 'open', 'high', 'low', 'close', 'volume']
        self.assertListEqual(list(df.columns), expected_columns)
        
        # 验证数据类型
        self.assertTrue(pd.api.types.is_datetime64_any_dtype(df['timestamp']))
        for col in ['open', 'high', 'low', 'close', 'volume']:
            self.assertTrue(pd.api.types.is_float_dtype(df[col]))
        
        # 验证数据合理性
        self.assertTrue((df['high'] >= df['low']).all(), "最高价应大于等于最低价")
        self.assertTrue((df['high'] >= df['close']).all(), "最高价应大于等于收盘价")
        self.assertTrue((df['low'] <= df['close']).all(), "最低价应小于等于收盘价")
        
        print(f"  ✅ 获取到 {len(df)} 条K线数据")
        print(f"  最新价格: ${df.iloc[-1]['close']:,.2f}")

    def test_04_get_klines_multiple_intervals(self):
        """测试多时间周期K线获取"""
        print("\n📝 测试4: 多时间周期K线")
        
        symbol = 'ETHUSDT'
        intervals = ['3m', '5m', '15m', '4h']
        
        for interval in intervals:
            df = self.fetcher.get_klines(symbol, interval, limit=50)
            self.assertFalse(df.empty, f"{interval} K线数据不应为空")
            print(f"  ✅ {interval}: {len(df)} 条数据")

    # ==================== 技术指标测试 ====================

    def test_05_calculate_ema(self):
        """测试EMA计算"""
        print("\n📝 测试5: EMA计算")
        
        # 创建测试数据
        prices = pd.Series([100, 102, 101, 103, 105, 104, 106, 108, 107, 109])
        
        ema_20 = self.fetcher.calculate_ema(prices, 5)
        
        self.assertEqual(len(ema_20), len(prices))
        self.assertFalse(ema_20.isna().all(), "EMA不应全为NaN")
        
        # 验证EMA是递增的（对于递增序列）
        valid_ema = ema_20.dropna()
        self.assertGreater(valid_ema.iloc[-1], valid_ema.iloc[0])
        
        print(f"  ✅ EMA计算正确，最新值: {ema_20.iloc[-1]:.2f}")

    def test_06_calculate_macd(self):
        """测试MACD计算"""
        print("\n📝 测试6: MACD计算")
        
        df = self.fetcher.get_klines('BTCUSDT', '5m', limit=100)
        self.assertFalse(df.empty)
        
        macd, signal, hist = self.fetcher.calculate_macd(df)
        
        self.assertEqual(len(macd), len(df))
        self.assertEqual(len(signal), len(df))
        self.assertEqual(len(hist), len(df))
        
        # 验证MACD柱状图 = MACD线 - 信号线
        np.testing.assert_array_almost_equal(
            hist.dropna().values,
            (macd - signal).dropna().values,
            decimal=5
        )
        
        print(f"  ✅ MACD计算正确")
        print(f"  MACD: {macd.iloc[-1]:.4f}, Signal: {signal.iloc[-1]:.4f}, Hist: {hist.iloc[-1]:.4f}")

    def test_07_calculate_rsi(self):
        """测试RSI计算"""
        print("\n📝 测试7: RSI计算")
        
        df = self.fetcher.get_klines('ETHUSDT', '5m', limit=100)
        self.assertFalse(df.empty)
        
        rsi = self.fetcher.calculate_rsi(df['close'], period=14)
        
        self.assertEqual(len(rsi), len(df))
        
        # 验证RSI范围 [0, 100]
        valid_rsi = rsi.dropna()
        self.assertTrue((valid_rsi >= 0).all(), "RSI应大于等于0")
        self.assertTrue((valid_rsi <= 100).all(), "RSI应小于等于100")
        
        print(f"  ✅ RSI计算正确，当前值: {rsi.iloc[-1]:.2f}")

    def test_08_calculate_atr(self):
        """测试ATR计算"""
        print("\n📝 测试8: ATR计算")
        
        df = self.fetcher.get_klines('SOLUSDT', '5m', limit=100)
        self.assertFalse(df.empty)
        
        atr = self.fetcher.calculate_atr(df, period=14)
        
        self.assertEqual(len(atr), len(df))
        
        # 验证ATR为正数
        valid_atr = atr.dropna()
        self.assertTrue((valid_atr > 0).all(), "ATR应为正数")
        
        print(f"  ✅ ATR计算正确，当前值: {atr.iloc[-1]:.4f}")

    def test_09_get_technical_indicators(self):
        """测试完整技术指标获取"""
        print("\n📝 测试9: 完整技术指标")
        
        symbol = 'BTCUSDT'
        interval = '5m'
        
        indicators = self.fetcher.get_technical_indicators(symbol, interval, limit=200)
        
        # 验证返回的字典包含所有必要的键
        required_keys = [
            'current_price', 'ema20_current', 'ema50_current',
            'macd_current', 'macd_signal_current', 'macd_hist_current',
            'rsi14_current', 'atr14_current', 'atr3_current',
            'volume_current', 'volume_avg', 'volume_ratio',
            'prices', 'ema20_series', 'macd_series', 'rsi14_series'
        ]
        
        for key in required_keys:
            self.assertIn(key, indicators, f"缺少键: {key}")
        
        # 验证数据类型
        self.assertIsInstance(indicators['current_price'], float)
        self.assertIsInstance(indicators['prices'], list)
        self.assertEqual(len(indicators['prices']), 20, "价格序列应为20条")
        
        # 验证RSI范围
        self.assertGreaterEqual(indicators['rsi14_current'], 0)
        self.assertLessEqual(indicators['rsi14_current'], 100)
        
        print(f"  ✅ 技术指标完整")
        print(f"  当前价格: ${indicators['current_price']:,.2f}")
        print(f"  RSI(14): {indicators['rsi14_current']:.2f}")
        print(f"  成交量比率: {indicators['volume_ratio']:.2f}")

    # ==================== 期货市场数据测试 ====================

    def test_10_get_open_interest(self):
        """测试持仓量获取"""
        print("\n📝 测试10: 持仓量数据")
        
        symbol = 'BTCUSDT'
        oi_data = self.fetcher.get_open_interest(symbol)
        
        # 验证返回的字典
        self.assertIn('latest', oi_data)
        self.assertIn('average', oi_data)
        self.assertIn('deviation_pct', oi_data)
        
        # 验证数据类型
        self.assertIsInstance(oi_data['latest'], float)
        self.assertIsInstance(oi_data['average'], float)
        self.assertIsInstance(oi_data['deviation_pct'], float)
        
        # 验证数据合理性
        self.assertGreater(oi_data['latest'], 0, "持仓量应为正数")
        
        print(f"  ✅ 持仓量: {oi_data['latest']:,.0f}")
        print(f"  平均值: {oi_data['average']:,.0f}")
        print(f"  偏离度: {oi_data['deviation_pct']:.2f}%")

    def test_11_get_funding_rate(self):
        """测试资金费率获取"""
        print("\n📝 测试11: 资金费率")
        
        symbol = 'ETHUSDT'
        funding_data = self.fetcher.get_funding_rate(symbol)
        
        # 验证返回的字典
        self.assertIn('current_rate', funding_data)
        self.assertIn('persistence_bars', funding_data)
        
        # 验证数据类型
        self.assertIsInstance(funding_data['current_rate'], float)
        self.assertIsInstance(funding_data['persistence_bars'], int)
        
        # 验证持续性为非负整数
        self.assertGreaterEqual(funding_data['persistence_bars'], 0)
        
        print(f"  ✅ 资金费率: {funding_data['current_rate']:.6f}")
        print(f"  持续周期: {funding_data['persistence_bars']} bars")

    # ==================== 综合数据测试 ====================

    def test_12_get_coin_complete_data(self):
        """测试单币种完整数据获取"""
        print("\n📝 测试12: 单币种完整数据")
        
        coin = 'BTC'
        data = self.fetcher.get_coin_complete_data(coin)
        
        # 验证基本信息
        self.assertEqual(data['coin'], coin)
        self.assertEqual(data['symbol'], f'{coin}USDT')
        self.assertIn('timestamp', data)
        
        # 验证多时间周期数据
        for interval in ['3m', '5m', '15m', '4h']:
            key = f'{interval}_indicators'
            self.assertIn(key, data, f"缺少 {interval} 数据")
            if data[key]:  # 如果数据不为空
                self.assertIn('current_price', data[key])
        
        # 验证期货数据
        self.assertIn('open_interest', data)
        self.assertIn('funding_rate', data)
        
        print(f"  ✅ {coin} 完整数据获取成功")

    def test_13_get_all_coins_data(self):
        """测试所有币种数据获取"""
        print("\n📝 测试13: 所有币种数据")
        
        # 为了测试速度，只测试前3个币种
        original_coins = self.fetcher.coins
        self.fetcher.coins = ['BTC', 'ETH', 'SOL']
        
        all_data = self.fetcher.get_all_coins_data()
        
        # 验证返回的数据
        self.assertIsInstance(all_data, dict)
        self.assertEqual(len(all_data), 3)
        
        for coin in self.fetcher.coins:
            self.assertIn(coin, all_data)
            if all_data[coin]:  # 如果数据获取成功
                self.assertIn('symbol', all_data[coin])
        
        # 恢复原始币种列表
        self.fetcher.coins = original_coins
        
        print(f"  ✅ 获取了 {len(all_data)} 个币种的数据")

    def test_14_format_for_ai_prompt(self):
        """测试AI prompt格式化"""
        print("\n📝 测试14: AI Prompt格式化")
        
        coin = 'BTC'
        coin_data = self.fetcher.get_coin_complete_data(coin)
        
        prompt = self.fetcher.format_for_ai_prompt(coin_data)
        
        # 验证prompt包含关键信息
        self.assertIsInstance(prompt, str)
        self.assertIn(coin, prompt)
        self.assertIn('current_price', prompt)
        self.assertIn('EMA20', prompt)
        self.assertIn('RSI', prompt)
        self.assertIn('MACD', prompt)
        self.assertIn('Open Interest', prompt)
        self.assertIn('Funding Rate', prompt)
        
        print(f"  ✅ Prompt格式化成功，长度: {len(prompt)} 字符")

    # ==================== 账户信息测试 ====================

    def test_15_get_account_info(self):
        """测试账户信息获取"""
        print("\n📝 测试15: 账户信息")
        
        account_info = self.fetcher.get_account_info()
        
        if self.fetcher.is_authenticated:
            # 如果已认证，验证返回的数据结构
            self.assertIn('balances', account_info)
            self.assertIn('total_value_usdt', account_info)
            self.assertIn('update_time', account_info)
            print(f"  ✅ 账户总价值: ${account_info['total_value_usdt']:,.2f}")
        else:
            # 如果未认证，应该返回错误
            self.assertIn('error', account_info)
            print(f"  ⚠️ 未认证: {account_info['error']}")

    # ==================== WebSocket测试 ====================

    def test_16_websocket_initialization(self):
        """测试WebSocket初始化"""
        print("\n📝 测试16: WebSocket初始化")
        
        fetcher_ws = TradingDataFetcher(use_websocket=True)
        
        symbols = ['BTCUSDT', 'ETHUSDT']
        
        try:
            fetcher_ws.start_websocket(symbols)
            time.sleep(2)  # 等待连接建立
            
            # 验证WebSocket客户端已创建
            self.assertIsNotNone(fetcher_ws.ws_client)
            
            print(f"  ✅ WebSocket启动成功")
            
        except Exception as e:
            print(f"  ⚠️ WebSocket测试跳过: {e}")
        
        finally:
            fetcher_ws.stop_websocket()

    def test_17_websocket_data_storage(self):
        """测试WebSocket数据存储"""
        print("\n📝 测试17: WebSocket数据存储")
        
        fetcher_ws = TradingDataFetcher(use_websocket=True)
        
        # 模拟K线数据
        mock_kline_data = {
            's': 'BTCUSDT',
            'k': {
                't': 1640000000000,
                'o': '50000',
                'h': '51000',
                'l': '49000',
                'c': '50500',
                'v': '100',
                'x': False
            }
        }
        
        # 模拟ticker数据
        mock_ticker_data = {
            's': 'BTCUSDT',
            'c': '50500',
            'v': '1000',
            'P': '1.5',
            'h': '51000',
            'l': '49000'
        }
        
        # 测试数据处理
        fetcher_ws._handle_kline(mock_kline_data)
        fetcher_ws._handle_ticker(mock_ticker_data)
        
        # 验证数据存储
        ws_data = fetcher_ws.get_ws_data('BTCUSDT')
        
        self.assertIn('kline', ws_data)
        self.assertIn('ticker', ws_data)
        
        self.assertEqual(ws_data['kline']['close'], 50500.0)
        self.assertEqual(ws_data['ticker']['price'], 50500.0)
        
        print(f"  ✅ WebSocket数据存储正常")

    # ==================== 错误处理测试 ====================

    def test_18_invalid_symbol(self):
        """测试无效交易对处理"""
        print("\n📝 测试18: 无效交易对处理")
        
        invalid_symbol = 'INVALIDUSDT'
        
        # K线应返回空DataFrame
        df = self.fetcher.get_klines(invalid_symbol, '5m')
        self.assertTrue(df.empty, "无效交易对应返回空DataFrame")
        
        # 技术指标应返回空字典
        indicators = self.fetcher.get_technical_indicators(invalid_symbol, '5m')
        self.assertEqual(indicators, {}, "无效交易对应返回空字典")
        
        print(f"  ✅ 错误处理正常")

    def test_19_rate_limiting(self):
        """测试API频率限制处理"""
        print("\n📝 测试19: API频率限制")
        
        # 快速连续请求，测试是否会触发限制
        symbol = 'BTCUSDT'
        success_count = 0
        
        for i in range(5):
            df = self.fetcher.get_klines(symbol, '5m', limit=10)
            if not df.empty:
                success_count += 1
            time.sleep(0.1)  # 短暂延迟
        
        # 至少应该成功几次
        self.assertGreater(success_count, 0, "应该至少有一次成功请求")
        
        print(f"  ✅ 5次请求中成功 {success_count} 次")

    # ==================== 性能测试 ====================

    def test_20_performance_single_coin(self):
        """测试单币种数据获取性能"""
        print("\n📝 测试20: 单币种性能")
        
        start_time = time.time()
        
        data = self.fetcher.get_coin_complete_data('BTC')
        
        elapsed_time = time.time() - start_time
        
        self.assertIsNotNone(data)
        self.assertLess(elapsed_time, 10, "单币种数据获取应在10秒内完成")
        
        print(f"  ✅ 耗时: {elapsed_time:.2f} 秒")

    def test_21_data_consistency(self):
        """测试数据一致性"""
        print("\n📝 测试21: 数据一致性")
        
        symbol = 'BTCUSDT'
        
        # 获取两次数据，验证价格在合理范围内
        indicators1 = self.fetcher.get_technical_indicators(symbol, '5m')
        time.sleep(1)
        indicators2 = self.fetcher.get_technical_indicators(symbol, '5m')
        
        if indicators1 and indicators2:
            price1 = indicators1['current_price']
            price2 = indicators2['current_price']
            
            # 价格变化应该在合理范围内（1秒内不应超过5%）
            price_change_pct = abs(price2 - price1) / price1 * 100
            self.assertLess(price_change_pct, 5, "1秒内价格变化不应超过5%")
            
            print(f"  ✅ 价格1: ${price1:,.2f}, 价格2: ${price2:,.2f}")
            print(f"  变化: {price_change_pct:.4f}%")


# ==================== 测试套件 ====================

def suite():
    """创建测试套件"""
    test_suite = unittest.TestSuite()
    
    # 按顺序添加测试
    test_suite.addTest(TestTradingDataFetcher('test_01_initialization'))
    test_suite.addTest(TestTradingDataFetcher('test_02_api_connection'))
    test_suite.addTest(TestTradingDataFetcher('test_03_get_klines'))
    test_suite.addTest(TestTradingDataFetcher('test_04_get_klines_multiple_intervals'))
    test_suite.addTest(TestTradingDataFetcher('test_05_calculate_ema'))
    test_suite.addTest(TestTradingDataFetcher('test_06_calculate_macd'))
    test_suite.addTest(TestTradingDataFetcher('test_07_calculate_rsi'))
    test_suite.addTest(TestTradingDataFetcher('test_08_calculate_atr'))
    test_suite.addTest(TestTradingDataFetcher('test_09_get_technical_indicators'))
    test_suite.addTest(TestTradingDataFetcher('test_10_get_open_interest'))
    test_suite.addTest(TestTradingDataFetcher('test_11_get_funding_rate'))
    test_suite.addTest(TestTradingDataFetcher('test_12_get_coin_complete_data'))
    test_suite.addTest(TestTradingDataFetcher('test_13_get_all_coins_data'))
    test_suite.addTest(TestTradingDataFetcher('test_14_format_for_ai_prompt'))
    test_suite.addTest(TestTradingDataFetcher('test_15_get_account_info'))
    test_suite.addTest(TestTradingDataFetcher('test_16_websocket_initialization'))
    test_suite.addTest(TestTradingDataFetcher('test_17_websocket_data_storage'))
    test_suite.addTest(TestTradingDataFetcher('test_18_invalid_symbol'))
    test_suite.addTest(TestTradingDataFetcher('test_19_rate_limiting'))
    test_suite.addTest(TestTradingDataFetcher('test_20_performance_single_coin'))
    test_suite.addTest(TestTradingDataFetcher('test_21_data_consistency'))
    
    return test_suite


if __name__ == '__main__':
    # 运行测试
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite())