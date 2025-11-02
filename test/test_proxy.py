import subprocess
import requests
import sys

def get_windows_ip():
    """获取 Windows 宿主机 IP"""
    try:
        # 方法1：通过默认网关获取（推荐）
        result = subprocess.run(
            ['ip', 'route', 'show', 'default'],
            capture_output=True,
            text=True
        )
        
        if result.returncode == 0:
            # 输出格式: default via 172.18.48.1 dev eth0
            for line in result.stdout.split('\n'):
                if 'default via' in line:
                    ip = line.split()[2]
                    return ip
        
        # 方法2：备用方案 - 从 /etc/resolv.conf 获取（不推荐）
        # with open('/etc/resolv.conf', 'r') as f:
        #     for line in f:
        #         if 'nameserver' in line:
        #             return line.split()[1]
        
        return None
    except Exception as e:
        print(f"❌ 获取 Windows IP 失败: {e}")
        return None

def test_proxy():
    """测试代理连接"""
    print("🔍 环境诊断")
    print("=" * 60)
    
    # 1. Python 版本
    print(f"1️⃣ Python 版本: {sys.version}")
    print()
    
    # 2. 获取 Windows IP
    print("2️⃣ 检查 Windows 宿主机 IP:")
    windows_ip = get_windows_ip()
    
    if not windows_ip:
        print("   ❌ 无法获取 Windows IP")
        return
    
    print(f"   ✅ 检测到 IP: {windows_ip}")
    print()
    
    # 3. 测试端口连通性
    print("3️⃣ 检查代理端口连通性:")
    port = 7897
    
    result = subprocess.run(
        ['timeout', '3', 'bash', '-c', f'echo > /dev/tcp/{windows_ip}/{port}'],
        capture_output=True
    )
    
    if result.returncode == 0:
        print(f"   ✅ 端口 {windows_ip}:{port} 可访问")
    else:
        print(f"   ❌ 端口 {windows_ip}:{port} 不可访问")
        print(f"   提示: 请确保 Clash Verge 已启用 allow-lan")
        return
    print()
    
    # 4. 测试不使用代理
    print("4️⃣ 测试 requests 库:")
    print("   🔄 测试不使用代理访问百度...")
    try:
        response = requests.get('https://www.baidu.com', timeout=10)
        print(f"   ✅ 百度访问成功 (状态码: {response.status_code})")
    except Exception as e:
        print(f"   ❌ 百度访问失败: {e}")
    print()
    
    # 5. 测试使用代理
    print("5️⃣ 测试通过代理访问:")
    proxies = {
        'http': f'http://{windows_ip}:{port}',
        'https': f'http://{windows_ip}:{port}'
    }
    print(f"   代理配置: {proxies}")
    
    # 测试 Google
    print("   🔄 测试访问 Google...")
    try:
        response = requests.get('https://www.google.com', proxies=proxies, timeout=10)
        print(f"   ✅ Google 访问成功 (状态码: {response.status_code})")
    except Exception as e:
        print(f"   ❌ Google 访问失败: {type(e).__name__}: {e}")
    print()
    
    # 测试 Binance
    print("   🔄 测试访问 Binance API...")
    try:
        response = requests.get('https://api.binance.com/api/v3/ping', proxies=proxies, timeout=10)
        print(f"   ✅ Binance API 访问成功 (状态码: {response.status_code})")
        print(f"   响应内容: {response.json()}")
    except Exception as e:
        print(f"   ❌ Binance API 访问失败: {type(e).__name__}: {e}")
    
    print()
    print("=" * 60)
    print("✅ 诊断完成")
    print()
    print("💡 在代码中使用代理:")
    print(f"""
proxies = {{
    'http': 'http://{windows_ip}:{port}',
    'https': 'http://{windows_ip}:{port}'
}}

# 使用 requests
response = requests.get('https://api.binance.com/api/v3/ping', proxies=proxies)

# 使用 binance-connector
from binance.spot import Spot
client = Spot(proxies=proxies)
""")

if __name__ == "__main__":
    test_proxy()
