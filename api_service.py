#!/usr/bin/env python
from flask import Flask, request, jsonify, send_file
from flask_cors import CORS  # 导入CORS支持
import io
import os
import tempfile
import json
import yaml
import uuid
from PIL import Image
from generate_from_json import generate_diagram

app = Flask(__name__)
CORS(app)  # 启用CORS支持，允许所有域的跨域请求

# 图像输出目录，临时存储生成的图像
OUTPUT_DIR = os.path.join(tempfile.gettempdir(), "network_diagrams")
os.makedirs(OUTPUT_DIR, exist_ok=True)

@app.route('/generate', methods=['POST'])
def generate_diagram_api():
    """API endpoint接收JSON数据并返回生成的图表图像"""
    try:
        # 获取请求数据
        request_data = request.get_json()
        if not request_data:
            return jsonify({"error": "请求体中未找到JSON数据"}), 400
        
        # 生成唯一的输出文件名
        unique_id = str(uuid.uuid4())
        output_filename = os.path.join(OUTPUT_DIR, f"diagram_{unique_id}")
        
        # 设置输出文件名
        request_data['output_filename'] = output_filename
        
        # 获取请求指定的输出格式，默认为PNG
        output_format = request_data.get('outformat', 'png')
        request_data['outformat'] = output_format
        
        # 生成图表
        generate_diagram(request_data)
        
        # 获取生成的文件路径
        output_file = f"{output_filename}.{output_format}"
        
        # 检查文件是否存在
        if not os.path.exists(output_file):
            return jsonify({"error": "图表生成失败"}), 500
        
        # 打开生成的图像文件并以二进制流返回
        return send_file(output_file, 
                        mimetype=f'image/{output_format}',
                        as_attachment=True,
                        download_name=f"network_diagram.{output_format}")
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/health', methods=['GET'])
def health_check():
    """健康检查端点"""
    return jsonify({"status": "healthy", "service": "network diagram generator"})

@app.route('/', methods=['GET'])
def index():
    """API服务主页，显示简单使用说明"""
    return '''
    <html>
        <head>
            <title>网络拓扑图生成服务</title>
            <style>
                body { font-family: Arial, sans-serif; margin: 40px; line-height: 1.6; }
                pre { background: #f4f4f4; padding: 10px; border-radius: 5px; }
                h1 { color: #333; }
                h2 { color: #444; margin-top: 20px; }
                .endpoint { background: #e9f7fe; padding: 10px; border-left: 4px solid #0099ff; margin: 15px 0; }
            </style>
        </head>
        <body>
            <h1>网络拓扑图生成API服务</h1>
            <p>该服务提供网络拓扑图的生成功能，通过HTTP POST请求提交JSON配置数据生成图表。</p>
            
            <div class="endpoint">
                <h2>API端点:</h2>
                <code>POST /generate</code>
                <p>提交JSON配置数据以生成网络拓扑图</p>
            </div>
            
            <h2>请求示例:</h2>
            <pre>
curl -X POST http://localhost:5000/generate \\
     -H "Content-Type: application/json" \\
     -d @your_config.json
            </pre>
            
            <h2>配置示例:</h2>
            <pre>
{
  "title": "企业网络拓扑",
  "outformat": "png",
  "direction": "TB",
  "nodes": [
    {
      "id": "internet",
      "label": "Internet",
      "icon": "internet"
    }
  ],
  "clusters": [
    {
      "name": "内部网络",
      "nodes": [
        {
          "id": "server1",
          "label": "服务器",
          "icon": "server"
        }
      ]
    }
  ],
  "connections": [
    {
      "from": "internet",
      "to": "server1"
    }
  ]
}
            </pre>
            
            <h2>状态检查:</h2>
            <code>GET /health</code>
            
            <h2>Web界面:</h2>
            <p>我们也提供了一个Web界面，您可以通过打开 <code>web_interface.html</code> 文件在浏览器中使用它。</p>
        </body>
    </html>
    '''

if __name__ == '__main__':
    # 默认端口5000
    port = int(os.environ.get('PORT', 5000))
    # 在开发环境中使用debug=True，生产环境中应设置为False
    app.run(host='0.0.0.0', port=port, debug=True) 