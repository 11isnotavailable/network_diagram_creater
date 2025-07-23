#!/usr/bin/env python
import os
import sys
import json
import yaml
import argparse
from generate_from_json import generate_diagram

def load_config(config_path):
    """加载配置文件，自动检测JSON或YAML格式"""
    try:
        file_ext = os.path.splitext(config_path)[1].lower()
        
        with open(config_path, 'r', encoding='utf-8') as f:
            if file_ext in ['.yml', '.yaml']:
                print(f"检测到YAML格式配置文件: {config_path}")
                return yaml.safe_load(f)
            elif file_ext == '.json':
                print(f"检测到JSON格式配置文件: {config_path}")
                return json.load(f)
            else:
                # 尝试按JSON格式加载
                try:
                    content = f.read()
                    return json.loads(content)
                except json.JSONDecodeError:
                    # 如果JSON解析失败，尝试YAML格式
                    try:
                        return yaml.safe_load(content)
                    except yaml.YAMLError:
                        raise ValueError(f"无法识别文件格式: {config_path}，请使用.json或.yaml/.yml后缀")
    except Exception as e:
        print(f"❌ 加载配置文件失败: {e}")
        sys.exit(1)

def main():
    # 创建命令行参数解析器
    parser = argparse.ArgumentParser(description='根据配置文件生成网络拓扑图')
    parser.add_argument('config_file', help='配置文件路径 (.json, .yaml 或 .yml)')
    parser.add_argument('-o', '--output', help='输出文件名（不含扩展名，覆盖配置中的设置）')
    parser.add_argument('-f', '--format', choices=['svg', 'png', 'jpg', 'pdf'], 
                        help='输出文件格式（覆盖配置中的设置）')
    parser.add_argument('-d', '--direction', choices=['TB', 'LR', 'BT', 'RL'],
                        help='图表方向: TB=从上到下, LR=从左到右, BT=从下到上, RL=从右到左（覆盖配置中的设置）')
    parser.add_argument('--title', help='图表标题（覆盖配置中的设置）')
    
    # 解析命令行参数
    args = parser.parse_args()
    
    config_path = args.config_file
    
    # 检查文件是否存在
    if not os.path.exists(config_path):
        print(f"❌ 文件不存在: {config_path}")
        sys.exit(1)
        
    # 加载配置
    print(f"正在加载配置文件: {config_path}")
    config = load_config(config_path)
    
    # 应用命令行参数覆盖配置中的设置
    if args.output:
        config['output_filename'] = args.output
    if args.format:
        config['outformat'] = args.format
    if args.direction:
        config['direction'] = args.direction
    if args.title:
        config['title'] = args.title
    
    # 生成图表
    print("正在生成网络拓扑图...")
    generate_diagram(config)
    
    output_filename = config.get('output_filename', 'network_topology')
    output_format = config.get('outformat', 'svg')
    print(f"✅ 完成! 输出文件: {output_filename}.{output_format}")

if __name__ == "__main__":
    main() 