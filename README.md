# 网络拓扑图生成工具

这个工具可以根据JSON或YAML配置文件生成网络拓扑图，使用Python的diagrams库和自定义图标。

特别注意：当前只支持输出格式为svg，输出格式为png时拓补图中组件会渲染失败

## 快速开始

最简单的方式是使用一键启动脚本：

```bash
python start_service.py
```

这个脚本将：
1. 启动API服务（端口5000）
2. 启动一个简单的Web服务器（端口8000）
3. 在默认浏览器中打开Web界面

## 使用方法

### Web界面（最简单）

![Web界面预览](web_interface_preview.png)

我们提供了一个友好的Web界面，支持：
- JSON编辑器（带语法高亮）
- 预设模板选择
- 可视化预览
- 一键下载生成的图片

使用方法：
1. 启动API服务：`python api_service.py`
2. 在浏览器中打开 `web_interface.html` 文件
3. 编辑JSON配置或选择预设模板
4. 点击"生成拓扑图"按钮

### 命令行工具（本地生成）

#### 统一入口（推荐）

基本用法:

```bash
python generate_diagram.py your_config.json  # JSON格式
```

或

```bash
python generate_diagram.py your_config.yaml  # YAML格式
```

支持的命令行参数:

```bash
python generate_diagram.py your_config.yaml --title "自定义标题" --output my_diagram --format png --direction LR
```

参数说明:
- `--title` / `--title="自定义标题"`: 设置图表标题（覆盖配置中的设置）
- `-o` / `--output`: 设置输出文件名（不含扩展名，覆盖配置中的设置）
- `-f` / `--format`: 设置输出格式，可选项: svg, png, jpg, pdf（覆盖配置中的设置）
- `-d` / `--direction`: 设置图表方向，可选项: TB（从上到下）, LR（从左到右）, BT（从下到上）, RL（从右到左）（覆盖配置中的设置）
- `-h` / `--help`: 显示帮助信息

#### 专用脚本

也可以使用针对特定格式的专用脚本：

##### JSON格式

```bash
python generate_from_json.py your_config.json
```

##### YAML格式

```bash
python yaml_to_diagram.py your_config.yaml
```

### API服务方式（HTTP请求生成）

我们也提供了一个API服务，允许通过HTTP请求生成网络拓扑图。

#### 启动API服务

```bash
python api_service.py
```

默认情况下，服务将在 http://localhost:5000 上运行。

#### 使用API生成图表

**使用客户端工具**:

```bash
python client_example.py your_config.json
python client_example.py your_config.yaml -o output_diagram -u http://localhost:5000/generate
```

**使用curl**:

```bash
curl -X POST http://localhost:5000/generate \
     -H "Content-Type: application/json" \
     -d @your_config.json \
     --output network_diagram.png
```

更多关于API服务的详细信息，请参考 [API_README.md](API_README.md)。

## 配置文件格式

配置文件可以是JSON或YAML格式，两种格式的结构相同，但YAML格式更易于编写和维护。

### 基本配置

```yaml
title: "网络拓扑图标题"
output_filename: "输出文件名（不含扩展名）"
outformat: "svg"  # 可选: "png", "jpg", "svg" 等
direction: "TB"   # 方向: "TB"(从上到下), "LR"(从左到右), "BT"(从下到上), "RL"(从右到左)

# 图表属性
graph_attr:
  fontsize: "12"
  bgcolor: transparent
  splines: ortho  # 线条类型：ortho(直角), spline(曲线)

# 节点属性
node_attr:
  fontsize: "20"
  height: "0.8"
  width: "0.8"
  fixedsize: "true"
  imagescale: "true"
```

### 节点定义

在主层级定义的节点:

```yaml
nodes:
  - id: internet           # 唯一ID，用于连接引用
    label: 公网 / Internet  # 显示的文本
    icon: internet         # 图标名称（对应my_icons目录下的svg文件名，不含扩展名）
  - id: router1
    label: 路由器
    icon: router
```

### 集群（网络区域）定义

```yaml
clusters:
  - name: 边界区              # 区域名称
    subnet: 192.168.1.0/24   # 子网信息（可选）
    nodes:                   # 区域内的节点
      - id: firewall
        label: 防火墙
        icon: firewall
    clusters: []             # 嵌套的子区域（可选）
```

### 连接定义

```yaml
connections:
  - from: internet          # 起始节点ID
    to: firewall            # 终止节点ID
    color: black            # 连线颜色（可选）
    style: solid            # 线型（可选）: "solid", "dashed", "dotted"
    bidirectional: false    # 是否双向连线（可选）
```

## 支持的图标

图标文件位于 `my_icons` 目录下，包括:

- activedirectory.svg
- client.svg
- coredns.svg
- firewall.svg
- internet.svg
- portal.svg
- router.svg
- server.svg
- smtp_server.svg
- switch.svg
- user.svg
- users.svg
- waf.svg

如果需要添加新的图标，只需将SVG文件放入 `my_icons` 目录，并在配置中的 `icon` 字段中使用文件名（不含扩展名）。

## 完整示例

- 查看 `sample_network.json` 文件获取完整的JSON示例配置
- 查看 `sample_network.yaml` 文件获取完整的YAML示例配置（推荐）

## 高级功能

### 嵌套区域

可以在区域内定义子区域：

```yaml
clusters:
  - name: 主区域
    clusters:
      - name: 子区域
        nodes: [...]
```

### 自定义连线样式

```yaml
connections:
  - from: server1
    to: server2
    color: red
    style: dashed
    bidirectional: true
```

## 依赖安装

安装所需的Python库：

```bash
pip install diagrams pyyaml flask flask-cors requests
```

## 项目结构

```
├── create_diagram.py        # 原始脚本（保持不变）
├── generate_diagram.py      # 统一命令行工具
├── generate_from_json.py    # JSON解析和图表生成核心
├── yaml_to_diagram.py       # YAML格式支持
├── api_service.py           # API服务
├── client_example.py        # API客户端示例
├── web_interface.html       # Web界面
├── start_service.py         # 一键启动脚本
├── README.md                # 主文档
├── API_README.md            # API文档
├── sample_network.json      # JSON示例
├── sample_network.yaml      # YAML示例
└── my_icons/                # 自定义图标目录
    ├── internet.svg
    ├── router.svg
    └── ...
```

## Docker支持

### 本地命令行工具

```dockerfile
FROM python:3.9-slim

WORKDIR /app

# 安装Graphviz依赖
RUN apt-get update && apt-get install -y graphviz

# 复制项目文件
COPY . .

# 安装Python依赖
RUN pip install --no-cache-dir diagrams pyyaml

# 运行示例
CMD ["python", "generate_diagram.py", "sample_network.yaml"]
```

### API服务

请参考 [API_README.md](API_README.md) 了解如何在Docker中运行API服务。

## 故障排除

- 确保所有的节点ID都是唯一的
- 确保所有在连接中引用的节点都已定义
- 确保图标文件存在于 `my_icons` 目录中
- 如使用YAML，确保YAML语法正确
- 如使用API服务，确保服务正在运行并且URL正确
- 如使用Web界面，可能需要处理浏览器的跨域限制：
  - 方法1: 使用 `start_service.py` 脚本启动服务
  - 方法2: 使用浏览器插件禁用CORS限制
  - 方法3: 使用服务器提供静态文件（如Nginx或Apache） 
