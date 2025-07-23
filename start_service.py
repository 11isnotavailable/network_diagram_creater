#!/usr/bin/env python
import os
import sys
import subprocess
import threading
import time
import webbrowser
from http.server import HTTPServer, SimpleHTTPRequestHandler

def start_api_server():
    """启动API服务器"""
    print("正在启动API服务器...")
    # 检查是否安装了flask_cors
    try:
        import flask_cors
    except ImportError:
        print("安装必要的依赖...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "flask-cors"])
    
    # 启动API服务
    if os.name == 'nt':  # Windows
        subprocess.Popen([sys.executable, "api_service.py"], creationflags=subprocess.CREATE_NEW_CONSOLE)
    else:  # Linux/Mac
        subprocess.Popen([sys.executable, "api_service.py"])
    
    print("API服务器已启动，监听端口5000")
    time.sleep(2)  # 等待API服务启动

def start_web_server():
    """启动简单的HTTP服务器提供静态文件"""
    print("启动Web服务器...")
    server_address = ('', 8000)
    httpd = HTTPServer(server_address, SimpleHTTPRequestHandler)
    
    # 在单独的线程中运行HTTP服务器
    server_thread = threading.Thread(target=httpd.serve_forever)
    server_thread.daemon = True
    server_thread.start()
    
    print("Web服务器已启动，监听端口8000")
    return httpd

def open_web_interface():
    """在默认浏览器中打开Web界面"""
    web_interface_url = "http://localhost:8000/web_interface.html"
    print(f"在浏览器中打开Web界面: {web_interface_url}")
    webbrowser.open(web_interface_url)

def update_web_interface():
    """更新web_interface.html中的API地址"""
    try:
        with open("web_interface.html", "r", encoding="utf-8") as f:
            content = f.read()
        
        # 如果API地址是localhost:5000，则不需要更改
        if "http://localhost:5000/generate" in content:
            return
        
        # 否则更新API地址
        content = content.replace("const apiUrl = '", "const apiUrl = 'http://localhost:5000/generate")
        
        with open("web_interface.html", "w", encoding="utf-8") as f:
            f.write(content)
    
    except Exception as e:
        print(f"更新Web界面时出错: {e}")

def main():
    print("=" * 50)
    print("网络拓扑图生成器 - 启动器")
    print("=" * 50)
    print("这个脚本将启动API服务和Web服务器，并在浏览器中打开Web界面。")
    print("-" * 50)
    
    # 检查必要文件是否存在
    required_files = ["api_service.py", "generate_from_json.py", "web_interface.html"]
    for file in required_files:
        if not os.path.exists(file):
            print(f"错误: 缺少必要的文件 '{file}'")
            sys.exit(1)
    
    # 更新Web界面中的API地址
    update_web_interface()
    
    # 启动API服务器
    start_api_server()
    
    # 启动Web服务器
    httpd = start_web_server()
    
    # 打开Web界面
    open_web_interface()
    
    print("-" * 50)
    print("服务已启动:")
    print("1. API服务: http://localhost:5000")
    print("2. Web界面: http://localhost:8000/web_interface.html")
    print("-" * 50)
    print("按Ctrl+C停止Web服务器...")
    
    try:
        # 保持脚本运行
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n正在关闭Web服务器...")
        httpd.shutdown()
        print("服务已停止。API服务器可能仍在运行，请手动关闭它。")

if __name__ == "__main__":
    main() 