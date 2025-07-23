#!/usr/bin/env python
import requests
import json
import argparse
import os
import sys

def send_diagram_request(config_file, api_url="http://localhost:5000/generate", output_file=None):
    """
    发送拓扑图生成请求到API服务
    
    参数:
        config_file (str): 配置文件路径，可以是JSON或YAML格式
        api_url (str): API服务的URL
        output_file (str): 输出文件名，如不指定则自动生成
    
    返回:
        bool: 是否成功
    """
    try:
        # 确定文件格式
        file_ext = os.path.splitext(config_file)[1].lower()
        
        # 加载配置文件
        with open(config_file, 'r', encoding='utf-8') as f:
            if file_ext in ['.yml', '.yaml']:
                import yaml
                config = yaml.safe_load(f)
            else:
                config = json.load(f)
        
        # 确定输出格式和文件名
        output_format = config.get('outformat', 'png')
        if not output_file:
            base_name = os.path.splitext(os.path.basename(config_file))[0]
            output_file = f"{base_name}_diagram.{output_format}"
        elif not os.path.splitext(output_file)[1]:
            # 如果提供的输出文件没有扩展名，添加一个
            output_file = f"{output_file}.{output_format}"
        
        print(f"正在发送请求到 {api_url} ...")
        
        # 发送请求
        response = requests.post(
            api_url,
            json=config,
            stream=True  # 使用流式处理大文件
        )
        
        # 处理响应
        if response.status_code == 200:
            # 保存图像
            with open(output_file, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            
            print(f"✅ 成功! 拓扑图已保存为: {output_file}")
            return True
        else:
            print(f"❌ 错误 ({response.status_code}): {response.text}")
            return False
    
    except Exception as e:
        print(f"❌ 发生错误: {e}")
        return False

def main():
    """命令行入口点"""
    parser = argparse.ArgumentParser(description='通过API服务生成网络拓扑图')
    parser.add_argument('config_file', help='配置文件路径 (.json, .yaml 或 .yml)')
    parser.add_argument('-u', '--url', default='http://localhost:5000/generate',
                      help='API服务的URL (默认: http://localhost:5000/generate)')
    parser.add_argument('-o', '--output', help='输出文件名')
    
    args = parser.parse_args()
    
    # 检查文件是否存在
    if not os.path.exists(args.config_file):
        print(f"❌ 文件不存在: {args.config_file}")
        sys.exit(1)
    
    # 发送请求
    success = send_diagram_request(args.config_file, args.url, args.output)
    
    sys.exit(0 if success else 1)

if __name__ == '__main__':
    main() 