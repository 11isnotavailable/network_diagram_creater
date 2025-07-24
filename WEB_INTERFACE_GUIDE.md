# 网络拓扑图生成器 Web界面使用指南

本文档详细说明如何在Web界面中使用网络拓扑图生成器，特别是JSON配置的构成和注意事项。

## 重要提示

**⚠️ 目前系统仅支持SVG格式正确渲染自定义图标**
- 请在JSON配置中设置 `"outformat": "svg"`
- 使用PNG或其他格式可能导致图标无法正确显示

## 使用前准备

1. 确保API服务已启动：`python api_service.py`
2. 在浏览器中打开Web界面 (`web_interface.html`)
3. 使用预设模板或自行编写JSON配置
4. **重要：** 确保JSON中的 `outformat` 设置为 `"svg"`

## JSON配置结构

一个完整的JSON配置由以下几个主要部分组成：

```json
{
  "title": "图表标题",
  "outformat": "svg",
  "direction": "TB",
  "graph_attr": { ... },
  "node_attr": { ... },
  "nodes": [ ... ],
  "clusters": [ ... ],
  "connections": [ ... ]
}
```

### 基本属性

| 属性 | 必填 | 说明 | 可选值 |
|------|------|------|--------|
| title | 是 | 图表标题 | 任意文本 |
| outformat | 是 | 输出格式 | **"svg"** (推荐), "png", "jpg", "pdf" |
| direction | 是 | 图表方向 | "TB" (上→下), "LR" (左→右), "BT" (下→上), "RL" (右→左) |

### 图表属性 (graph_attr)

控制整个图表的外观：

```json
"graph_attr": {
  "fontsize": "12",
  "bgcolor": "transparent",
  "splines": "ortho"
}
```

| 属性 | 说明 | 常用值 |
|------|------|--------|
| fontsize | 字体大小 | "12", "14", "16" |
| bgcolor | 背景颜色 | "transparent", "white", "#f5f5f5" |
| splines | 连线样式 | "ortho" (直角), "spline" (曲线) |

### 节点属性 (node_attr)

控制节点的默认外观：

```json
"node_attr": {
  "fontsize": "20",
  "height": "0.8",
  "width": "0.8",
  "fixedsize": "true",
  "imagescale": "true"
}
```

## 节点定义 (nodes)

定义图表中的独立节点：

```json
"nodes": [
  {
    "id": "internet",        // 唯一标识符 (必填)
    "label": "互联网",       // 显示的标签 (必填)
    "icon": "internet"       // 图标名称 (必填，不含扩展名)
  },
  {
    "id": "router1",
    "label": "边界路由器",
    "icon": "router"
  }
]
```

**必填字段：**
- **id**: 唯一标识符，用于在连接中引用
- **label**: 显示在节点下方的文本
- **icon**: 图标名称，对应 `my_icons` 目录中的SVG文件（不含扩展名）

## 集群/区域定义 (clusters)

定义包含多个节点的区域：

```json
"clusters": [
  {
    "name": "内部网络",                 // 区域名称 (必填)
    "subnet": "192.168.1.0/24",        // 子网信息 (可选)
    "nodes": [                         // 区域内节点 (可选)
      {
        "id": "server1",
        "label": "应用服务器",
        "icon": "server"
      }
    ],
    "clusters": [ ... ]                // 嵌套区域 (可选)
  }
]
```

**必填字段：**
- **name**: 区域名称
- **nodes** 或 **clusters**: 至少需要定义一个节点或子区域

**可选字段：**
- **subnet**: 显示在区域名称后的子网信息

## 连接定义 (connections)

定义节点之间的连接：

```json
"connections": [
  {
    "from": "internet",        // 起始节点ID (必填)
    "to": "router1",           // 目标节点ID (必填)
    "color": "blue",           // 连线颜色 (可选)
    "style": "solid",          // 连线样式 (可选)
    "bidirectional": false     // 是否双向连接 (可选)
  }
]
```

**必填字段：**
- **from**: 起始节点的ID
- **to**: 目标节点的ID

**可选字段：**
- **color**: 连线颜色，可以是命名颜色("blue", "red")或十六进制值("#0000FF")
- **style**: 连线样式，可选值："solid", "dashed", "dotted"
- **bidirectional**: 是否为双向连接，默认为false（单向）

## 支持的图标

以下是 `my_icons` 目录中可用的图标：

- activedirectory
- client
- coredns
- firewall
- internet
- portal
- router
- server
- smtp_server
- switch
- user
- users
- waf

使用时只需引用图标名称（不带扩展名），例如：`"icon": "server"`

## 完整示例

以下是一个完整可用的JSON配置示例：

```json
{
  "title": "简单网络拓扑",
  "outformat": "svg",
  "direction": "TB",
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
      "label": "互联网",
      "icon": "internet"
    },
    {
      "id": "router",
      "label": "路由器",
      "icon": "router"
    }
  ],
  "clusters": [
    {
      "name": "内部网络",
      "subnet": "192.168.1.0/24",
      "nodes": [
        {
          "id": "server",
          "label": "服务器",
          "icon": "server"
        },
        {
          "id": "client",
          "label": "客户端",
          "icon": "client"
        }
      ]
    }
  ],
  "connections": [
    {
      "from": "internet",
      "to": "router"
    },
    {
      "from": "router",
      "to": "server"
    },
    {
      "from": "client",
      "to": "server",
      "bidirectional": true
    }
  ]
}
```

## 常见问题

### 图标不显示或显示为方块

**问题**: 生成的图表中图标不显示或显示为方块
**解决方案**: 确保将输出格式设置为SVG: `"outformat": "svg"`

### 验证失败

**问题**: 点击"验证JSON"时报错
**解决方案**: 检查JSON格式是否正确，特别注意括号配对和逗号位置

### 连接不显示

**问题**: 节点之间的连接没有显示
**解决方案**: 确保连接中引用的节点ID存在且拼写正确

### 服务器错误

**问题**: 点击"生成拓扑图"后返回服务器错误
**解决方案**:
1. 确保API服务正在运行 (`python api_service.py`)
2. 检查JSON格式是否正确
3. 查看服务器控制台输出以获取详细错误信息 