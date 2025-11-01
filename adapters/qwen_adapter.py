#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Qwen适配器
调用阿里云通义千问模型进行交易决策
"""

import os
from typing import Dict, Any
from .llm_base import LLMAdapter

try:
    from openai import OpenAI
except ImportError:
    print("❌ 请安装openai: pip install openai")
    OpenAI = None


class QwenAdapter(LLMAdapter):
    """Qwen适配器"""

    def __init__(self, api_key: str = None, model: str = "qwen-plus"):
        """
        初始化Qwen适配器

        Args:
            api_key: Qwen API密钥，如果为None则从环境变量获取
            model: 使用的模型名称，默认为qwen-plus
        """
        if api_key is None:
            api_key = os.getenv('QWEN_API_KEY')

        if not api_key:
            raise ValueError("Qwen API密钥未设置，请设置QWEN_API_KEY环境变量")

        super().__init__(api_key)

        self.model = model

        # 初始化OpenAI兼容客户端
        if OpenAI:
            self.client = OpenAI(
                api_key=self.api_key,
                base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
            )
        else:
            raise ImportError("OpenAI库未安装")

    def call(self, prompt: str) -> str:
        """
        调用Qwen API

        Args:
            prompt: 输入提示词

        Returns:
            Qwen响应文本
        """
        try:
            completion = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "你是一个专业的量化交易分析师，请根据市场数据给出交易决策。"},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=500,
                temperature=0.7
            )

            return completion.choices[0].message.content.strip()

        except Exception as e:
            print(f"❌ Qwen API调用失败: {e}")
            return '{"symbol": null, "action": "HOLD", "confidence": 0.0, "rationale": "API调用失败"}'

    def get_model_name(self) -> str:
        """获取模型名称"""
        return f"self.model"
