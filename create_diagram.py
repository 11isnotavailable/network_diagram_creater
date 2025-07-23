import os
from diagrams import Diagram, Cluster, Edge
from diagrams.custom import Custom

print("--- 开始使用本地SVG图标生成半复杂网络拓扑图 ---")

# --- 定义指向本地图标资源的路径 ---
script_dir = os.path.dirname(os.path.abspath(__file__))
icons_dir = os.path.join(script_dir, "my_icons")

# --- 为每个图标定义变量 ---
internet_icon = os.path.join(icons_dir, "internet.svg")
router_icon = os.path.join(icons_dir, "router.svg")
firewall_icon = os.path.join(icons_dir, "firewall.svg")
switch_icon = os.path.join(icons_dir, "switch.svg")
waf_icon = os.path.join(icons_dir, "waf.svg")
server_icon = os.path.join(icons_dir, "server.svg")
ad_icon = os.path.join(icons_dir, "activedirectory.svg")
dns_icon = os.path.join(icons_dir, "coredns.svg")
smtp_icon = os.path.join(icons_dir, "smtp_server.svg")
client_icon = os.path.join(icons_dir, "client.svg")
user_icon = os.path.join(icons_dir, "user.svg")
users_icon = os.path.join(icons_dir, "users.svg")
portal_icon = os.path.join(icons_dir, "portal.svg")
# --- 路径定义完成 ---

output_filename_without_ext = os.path.join(script_dir, "complex_topology_local")
graph_attr = {"fontsize": "12", "bgcolor": "transparent", "splines": "ortho"}
# --- 调整节点属性以缩小图标，增大文字 ---
node_attr = {
    "fontsize": "20",      # 将字体稍微增大，使其更清晰
    "height": "0.8",       # 将节点高度减小
    "width": "0.8",        # 将节点宽度减小
    "fixedsize": "true", # 关键：强制节点严格使用上面设定的宽高
    "imagescale": "true" # 关键：强制图标缩放以适应节点大小
}

try:
    with Diagram("企业网络拓扑 (半复杂版-本地图标)", show=False, filename=output_filename_without_ext, outformat="svg", graph_attr=graph_attr, node_attr=node_attr, direction="TB"):

        internet = Custom("公网 / Internet", icon_path=internet_icon)

        with Cluster("边界区 (192.168.1.0/24)"):
            firewall = Custom("主防火墙", icon_path=firewall_icon)
            nat_gateway = Custom("NAT网关", icon_path=switch_icon)
            internet >> firewall >> nat_gateway

        core_router = Custom("核心路由器", icon_path=router_icon)
        nat_gateway >> core_router

        with Cluster("内部网络 (10.0.0.0/8)"):
            core_switch = Custom("核心交换机 (三层)", icon_path=switch_icon)
            core_router >> core_switch

            with Cluster("内部网络 基础服务 (10.0.0.0/22)"):
                ad_dc = Custom("AD DC", icon_path=ad_icon)
                dns_server = Custom("DNS Server", icon_path=dns_icon)
                smtp_server = Custom("SMTP Server", icon_path=smtp_icon)
                jump_server = Custom("Jump Server\n(堡垒机)", icon_path=server_icon)
                core_switch >> Edge(color="darkgreen") >> [ad_dc, dns_server, smtp_server, jump_server]

            with Cluster("内部网络 内部服务 (10.8.1.0/24)"):
                waf = Custom("WAF / 反代", icon_path=waf_icon)
                app_server = Custom("应用服务器", icon_path=server_icon)
                db_server = Custom("数据库服务器", icon_path=server_icon)
                core_switch >> Edge(color="blue") >> waf >> app_server >> db_server

            with Cluster("内部网络 办公区 (10.16.1.0/24)"):
                office_switch = Custom("办公区接入交换机", icon_path=switch_icon)
                pc = Custom("办公电脑", icon_path=client_icon)
                user = Custom("员工", icon_path=user_icon)
                core_switch >> Edge(color="purple") >> office_switch >> pc
                user - pc

        with Cluster("访客网络 (172.16.0.0/14)"):
            visitor_firewall = Custom("访客区防火墙", icon_path=firewall_icon)
            portal = Custom("Portal认证", icon_path=portal_icon)
            wifi_ap = Custom("WiFi AP", icon_path=switch_icon)
            visitors = Custom("访客", icon_path=users_icon)
            core_router >> visitor_firewall >> portal >> wifi_ap
            wifi_ap - visitors

    print(f"✅ 更复杂的网络拓扑图已成功生成!")
    print(f"   请在以下路径查看 'complex_topology_local.svg' 文件: {script_dir}")

except Exception as e:
    print(f"❌ 生成图表时发生错误: {e}")

print("--- 流程结束 ---")