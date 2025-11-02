import psycopg2

try:
    # 连接数据库
    conn = psycopg2.connect(
        host="localhost",
        database="trading_system",
        user="alpha_trading",
        password="123456"  # 替换成你的密码
    )
    
    print("✅ 数据库连接成功！")
    
    # 测试查询
    cursor = conn.cursor()
    cursor.execute("SELECT version();")
    version = cursor.fetchone()
    print(f"PostgreSQL 版本: {version[0]}")
    
    # 关闭连接
    cursor.close()
    conn.close()
    
except Exception as e:
    print(f"❌ 连接失败: {e}")
