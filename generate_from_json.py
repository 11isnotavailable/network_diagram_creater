import os
import json
import sys
from diagrams import Diagram, Cluster, Edge
from diagrams.custom import Custom

def load_json_config(json_path):
    """Load diagram configuration from a JSON file"""
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"❌ Failed to load JSON configuration: {e}")
        sys.exit(1)

def generate_diagram(config):
    """Generate network diagram based on JSON configuration"""
    # Get base configuration
    title = config.get("title", "Network Topology")
    output_filename = config.get("output_filename", "network_topology")
    direction = config.get("direction", "TB")  # Top to Bottom by default
    
    # Get diagram attributes
    graph_attr = config.get("graph_attr", {"fontsize": "12", "bgcolor": "transparent", "splines": "ortho"})
    node_attr = config.get("node_attr", {
        "fontsize": "20", 
        "height": "0.8",
        "width": "0.8",
        "fixedsize": "true",
        "imagescale": "true"
    })
    
    # Get output format
    outformat = config.get("outformat", "svg")
    
    # Set up icon directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    icons_dir = os.path.join(script_dir, "my_icons")
    
    # Store all created nodes to reference when creating edges
    node_registry = {}
    
    try:
        # Create diagram
        with Diagram(title, show=False, filename=output_filename, outformat=outformat, 
                    graph_attr=graph_attr, node_attr=node_attr, direction=direction):
            
            # Process nodes
            for node_def in config.get("nodes", []):
                node_id = node_def.get("id")
                node_label = node_def.get("label", node_id)
                node_icon = node_def.get("icon")
                node_ip = node_def.get("ip", "")
                node_docker_image = node_def.get("image", "")
                
                # Skip nodes without ID or icon
                if not node_id or not node_icon:
                    print(f"⚠️ Skipping node with missing id or icon: {node_def}")
                    continue
                
                icon_path = os.path.join(icons_dir, f"{node_icon}.svg")
                
                # Check if icon exists
                if not os.path.exists(icon_path):
                    print(f"⚠️ Icon not found: {icon_path}, using default server.svg")
                    icon_path = os.path.join(icons_dir, "server.svg")
                
                # Create label with IP address and Docker image if provided
                display_parts = [node_label]
                if node_ip:
                    display_parts.append(node_ip)
                if node_docker_image:
                    display_parts.append(f"镜像: {node_docker_image}")
                
                display_label = "\n".join(display_parts)
                
                # Create the node
                node = Custom(display_label, icon_path=icon_path)
                node_registry[node_id] = node
            
            # Process clusters and their nodes
            for cluster_def in config.get("clusters", []):
                cluster_name = cluster_def.get("name", "Cluster")
                subnet = cluster_def.get("subnet", "")
                full_name = f"{cluster_name}{' (' + subnet + ')' if subnet else ''}"
                
                with Cluster(full_name):
                    # Process nodes inside this cluster
                    for node_def in cluster_def.get("nodes", []):
                        node_id = node_def.get("id")
                        node_label = node_def.get("label", node_id)
                        node_icon = node_def.get("icon")
                        node_ip = node_def.get("ip", "")
                        node_docker_image = node_def.get("image", "")
                        
                        # Skip nodes without ID or icon
                        if not node_id or not node_icon:
                            print(f"⚠️ Skipping node with missing id or icon: {node_def}")
                            continue
                        
                        icon_path = os.path.join(icons_dir, f"{node_icon}.svg")
                        
                        # Check if icon exists
                        if not os.path.exists(icon_path):
                            print(f"⚠️ Icon not found: {icon_path}, using default server.svg")
                            icon_path = os.path.join(icons_dir, "server.svg")
                        
                        # Create label with IP address and Docker image if provided
                        display_parts = [node_label]
                        if node_ip:
                            display_parts.append(node_ip)
                        if node_docker_image:
                            display_parts.append(f"镜像: {node_docker_image}")
                        
                        display_label = "\n".join(display_parts)
                        
                        # Create the node
                        node = Custom(display_label, icon_path=icon_path)
                        node_registry[node_id] = node
                    
                    # Process nested clusters
                    for nested_cluster in cluster_def.get("clusters", []):
                        process_nested_cluster(nested_cluster, icons_dir, node_registry)
            
            # Process connections
            for connection in config.get("connections", []):
                source_id = connection.get("from")
                target_id = connection.get("to")
                edge_color = connection.get("color", "black")
                edge_style = connection.get("style", "solid")
                
                # Skip connections with missing source or target
                if source_id not in node_registry or target_id not in node_registry:
                    print(f"⚠️ Skipping connection with invalid source or target: {connection}")
                    continue
                
                # Create edge with properties
                source = node_registry[source_id]
                target = node_registry[target_id]
                
                if connection.get("bidirectional", False):
                    source - Edge(color=edge_color, style=edge_style) - target
                else:
                    source >> Edge(color=edge_color, style=edge_style) >> target
        
        print(f"✅ Diagram successfully generated!")
        print(f"   Please check '{output_filename}.{outformat}' file in: {script_dir}")
        
    except Exception as e:
        print(f"❌ Error generating diagram: {e}")

def process_nested_cluster(cluster_def, icons_dir, node_registry):
    """Process a nested cluster recursively"""
    cluster_name = cluster_def.get("name", "Nested Cluster")
    subnet = cluster_def.get("subnet", "")
    full_name = f"{cluster_name}{' (' + subnet + ')' if subnet else ''}"
    
    with Cluster(full_name):
        # Process nodes inside this cluster
        for node_def in cluster_def.get("nodes", []):
            node_id = node_def.get("id")
            node_label = node_def.get("label", node_id)
            node_icon = node_def.get("icon")
            node_ip = node_def.get("ip", "")
            node_docker_image = node_def.get("image", "")
            
            # Skip nodes without ID or icon
            if not node_id or not node_icon:
                print(f"⚠️ Skipping node with missing id or icon: {node_def}")
                continue
            
            icon_path = os.path.join(icons_dir, f"{node_icon}.svg")
            
            # Check if icon exists
            if not os.path.exists(icon_path):
                print(f"⚠️ Icon not found: {icon_path}, using default server.svg")
                icon_path = os.path.join(icons_dir, "server.svg")
            
            # Create label with IP address and Docker image if provided
            display_parts = [node_label]
            if node_ip:
                display_parts.append(node_ip)
            if node_docker_image:
                display_parts.append(f"镜像: {node_docker_image}")
            
            display_label = "\n".join(display_parts)
            
            # Create the node
            node = Custom(display_label, icon_path=icon_path)
            node_registry[node_id] = node
        
        # Recursively process nested clusters
        for nested_cluster in cluster_def.get("clusters", []):
            process_nested_cluster(nested_cluster, icons_dir, node_registry)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python generate_from_json.py <json_config_file>")
        sys.exit(1)
    
    json_path = sys.argv[1]
    config = load_json_config(json_path)
    generate_diagram(config) 