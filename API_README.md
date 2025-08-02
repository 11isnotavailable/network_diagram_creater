# 网络拓扑图生成API服务

这个API服务允许通过HTTP请求生成网络拓扑图，支持JSON格式的配置数据。

## 开始使用

### 安装依赖

```bash
pip install flask pillow diagrams pyyaml
```

### 启动服务

```bash
python api_service.py
```

默认情况下，服务将在 http://localhost:5000 上运行。

## API端点

### 生成网络拓扑图

**请求**:
- 方法: `POST`
- URL: `/generate`
- Content-Type: `application/json`
- 请求体: JSON格式的拓扑图配置

**响应**:
- 成功: 返回包含文件信息的JSON对象
- 失败: 返回包含错误信息的JSON对象和相应的HTTP状态码

### 健康检查

**请求**:
- 方法: `GET`
- URL: `/health`

**响应**:
- 成功: 返回JSON `{"status": "healthy", "service": "network diagram generator"}`

## 使用示例

### 使用curl发送请求

```bash
curl -X POST http://localhost:5000/generate \
     -H "Content-Type: application/json" \
     -d @your_config.json
```

### 使用Python发送请求

```python
import requests
import json

# 加载配置文件
with open('your_config.json', 'r') as f:
    config = json.load(f)

# 发送请求
response = requests.post(
    'http://localhost:5000/generate',
    json=config
)

# 处理返回结果
if response.status_code == 200:
    result = response.json()
    print(f'图表生成成功: {result["file_name"]}')
    print(f'文件路径: {result["file_path"]}')
    print(f'文件格式: {result["format"]}')
else:
    print(f'错误: {response.json()}')
```

### 响应格式示例

成功响应:
```json
{
  "success": true,
  "message": "图表生成成功",
  "file_path": "D:/network_diagrams/diagram_ad5989e7-3965-45b8-a2f2-2f9681367395.svg",
  "file_name": "diagram_ad5989e7-3965-45b8-a2f2-2f9681367395.svg",
  "format": "svg"
}
```

失败响应:
```json
{
  "error": "错误信息描述"
}
```

## JSON配置格式

### 节点配置

每个节点可以包含以下字段：

- `id`: 节点的唯一标识符（必需）
- `label`: 节点的显示标签（必需）
- `icon`: 节点的图标类型（必需）
- `ip`: 节点的IP地址（可选）- 如果提供，将显示在节点标签下方
- `image`: Docker镜像名称（可选）- 如果提供，将显示在IP地址下方

### 配置示例

```json
{
  "title": "企业网络拓扑",
  "outformat": "png",  // 可选: "png", "jpg", "svg", "pdf"
  "direction": "TB",   // 方向: "TB"(从上到下), "LR"(从左到右), "BT"(从下到上), "RL"(从右到左)
  
  "graph_attr": {
    "fontsize": "12",
    "bgcolor": "transparent",
    "splines": "ortho"
  },
  
  "node_attr": {
    "fontsize": "20",
    "height": "0.8",
    "width": "0.8",
    "fixedsize": "true",
    "imagescale": "true"
  },
  
  "nodes": [
    {
      "id": "internet",
      "label": "Internet",
      "icon": "internet"
    },
    {
      "id": "web_server",
      "label": "Web服务器",
      "icon": "server",
      "ip": "192.168.1.10",
      "image": "nginx:latest"
    }
  ],
  
  "clusters": [
    {
      "name": "内部网络",
      "subnet": "10.0.0.0/24",
      "nodes": [
        {
          "id": "server1",
          "label": "服务器",
          "icon": "server",
          "ip": "192.168.1.10",
          "image": "ubuntu:20.04"
        }
      ]
    }
  ],
  
  "connections": [
    {
      "from": "internet",
      "to": "server1",
      "color": "black",
      "style": "solid",
      "bidirectional": false
    }
  ]
}
```

## 在Docker中运行

创建Dockerfile:

```dockerfile
FROM python:3.9-slim

WORKDIR /app

# 安装Graphviz依赖
RUN apt-get update && apt-get install -y graphviz

# 复制项目文件
COPY . .

# 安装Python依赖
RUN pip install --no-cache-dir flask pillow diagrams pyyaml

# 设置环境变量
ENV PORT=5000

# 暴露端口
EXPOSE 5000

# 运行服务
CMD ["python", "api_service.py"]
```

构建并运行Docker容器:

```bash
docker build -t network-diagram-api .
docker run -p 5000:5000 network-diagram-api
```

## 生产环境部署

对于生产环境，建议:

1. 在api_service.py中将`debug=True`改为`debug=False`
2. 使用Gunicorn或uWSGI作为WSGI服务器
3. 设置适当的日志记录和错误处理
4. 考虑添加API密钥认证
5. 设置HTTPS

示例使用Gunicorn:

```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 api_service:app
```

## 高级配置

### 自定义临时文件目录

默认情况下，生成的图像文件存储在系统临时目录下的`network_diagrams`文件夹中。可以通过环境变量`OUTPUT_DIR`自定义此路径:

```bash
export OUTPUT_DIR=/path/to/custom/directory
python api_service.py
```

### 更改默认端口

```bash
export PORT=8080
python api_service.py
``` 