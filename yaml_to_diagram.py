#!/usr/bin/env python
import os
import sys
import json
import yaml
import tempfile
from generate_from_json import generate_diagram

def load_yaml_config(yaml_path):
    """Load diagram configuration from a YAML file"""
    try:
        with open(yaml_path, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)
    except Exception as e:
        print(f"❌ Failed to load YAML configuration: {e}")
        sys.exit(1)

def main():
    if len(sys.argv) != 2:
        print("Usage: python yaml_to_diagram.py <yaml_config_file>")
        sys.exit(1)
    
    yaml_path = sys.argv[1]
    print(f"Loading YAML configuration from {yaml_path}")
    
    # Load YAML configuration
    config = load_yaml_config(yaml_path)
    
    # Generate diagram directly from the loaded configuration
    print("Generating diagram...")
    generate_diagram(config)

if __name__ == "__main__":
    main() 