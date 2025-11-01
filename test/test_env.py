#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""测试环境变量加载"""

import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

print("🔍 检查环境变量")
print("=" * 50)

# 检查 QWEN_API_KEY
qwen_key = os.getenv('QWEN_API_KEY')
if qwen_key:
    # 只显示前后几位，保护隐私
    masked_key = f"{qwen_key[:8]}...{qwen_key[-4:]}" if len(qwen_key) > 12 else "***"
    print(f"✅ QWEN_API_KEY: {masked_key}")
else:
    print("❌ QWEN_API_KEY: 未设置")

print("\n💡 提示：")
print("   - .env 文件应该在项目根目录")
print("   - 确保 .env 文件格式正确（KEY=VALUE）")
print("   - 确保没有多余的空格或引号")
