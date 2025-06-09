"""
Configuration Manager for Fishtest Worker GUI
Handles saving and loading of user settings including password memory.
"""

import json
import os
from pathlib import Path
import base64

class ConfigManager:
    def __init__(self):
        self.config_file = Path.home() / ".fishtest_worker_config.json"
        
    def load_config(self):
        """Load configuration from file"""
        default_config = {
            'username': '',
            'password': '',
            'cores': str(max(1, os.cpu_count() - 1) if os.cpu_count() else 1)
        }
        
        if not self.config_file.exists():
            return default_config
            
        try:
            with open(self.config_file, 'r') as f:
                config = json.load(f)
                
            # Decode password if it exists
            if 'password' in config and config['password']:
                try:
                    config['password'] = base64.b64decode(config['password'].encode()).decode()
                except:
                    config['password'] = ''
                    
            # Ensure all required keys exist
            for key, default_value in default_config.items():
                if key not in config:
                    config[key] = default_value
                    
            return config
            
        except Exception as e:
            print(f"Error loading config: {e}")
            return default_config
            
    def save_config(self, config):
        """Save configuration to file"""
        try:
            # Create a copy to avoid modifying the original
            save_config = config.copy()
            
            # Encode password for basic security
            if 'password' in save_config and save_config['password']:
                save_config['password'] = base64.b64encode(save_config['password'].encode()).decode()
                
            with open(self.config_file, 'w') as f:
                json.dump(save_config, f, indent=2)
                
        except Exception as e:
            print(f"Error saving config: {e}")
            
    def clear_config(self):
        """Clear saved configuration"""
        try:
            if self.config_file.exists():
                self.config_file.unlink()
        except Exception as e:
            print(f"Error clearing config: {e}")
