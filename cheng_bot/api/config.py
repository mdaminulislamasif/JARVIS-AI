"""
Configuration file loader for the Jarvis-Cheng Bot Integration API.

This module handles loading and validating configuration from config.yaml,
with support for environment variable substitution.
"""

import os
import yaml
from typing import Dict, Any, Optional
from pathlib import Path
import structlog

logger = structlog.get_logger(__name__)


class ConfigLoader:
    """Loads and manages configuration from config.yaml."""
    
    def __init__(self, config_path: str = ".cheng_bot/config.yaml"):
        """
        Initialize the configuration loader.
        
        Args:
            config_path: Path to the configuration file
        """
        self.config_path = Path(config_path)
        self._config: Optional[Dict[str, Any]] = None
    
    def load(self) -> Dict[str, Any]:
        """
        Load configuration from file with environment variable substitution.
        
        Returns:
            Dictionary containing configuration values
            
        Raises:
            FileNotFoundError: If config file doesn't exist
            yaml.YAMLError: If config file is invalid YAML
        """
        if not self.config_path.exists():
            logger.warning(
                "config_file_not_found",
                path=str(self.config_path),
                using_defaults=True
            )
            return self._get_default_config()
        
        try:
            with open(self.config_path, 'r') as f:
                config_text = f.read()
                # Substitute environment variables
                config_text = self._substitute_env_vars(config_text)
                self._config = yaml.safe_load(config_text)
                
            logger.info("config_loaded", path=str(self.config_path))
            return self._config
            
        except yaml.YAMLError as e:
            logger.error("config_parse_error", error=str(e))
            raise
    
    def _substitute_env_vars(self, text: str) -> str:
        """
        Replace ${VAR_NAME} patterns with environment variable values.
        
        Args:
            text: Text containing environment variable references
            
        Returns:
            Text with environment variables substituted
        """
        import re
        
        def replace_env_var(match):
            var_name = match.group(1)
            value = os.environ.get(var_name)
            if value is None:
                logger.warning(
                    "env_var_not_found",
                    variable=var_name,
                    using_empty_string=True
                )
                return ""
            return value
        
        return re.sub(r'\$\{([^}]+)\}', replace_env_var, text)
    
    def _get_default_config(self) -> Dict[str, Any]:
        """
        Get default configuration values.
        
        Returns:
            Dictionary with default configuration
        """
        return {
            "api": {
                "host": "0.0.0.0",
                "port": 8080,
                "cors_origins": ["*"]
            },
            "authentication": {
                "api_key_file": ".cheng_bot/api_keys.json",
                "jwt_secret": os.environ.get("JWT_SECRET", "change-me-in-production"),
                "jwt_expiration_hours": 24,
                "rate_limit_per_minute": 100
            },
            "sessions": {
                "timeout_minutes": 30,
                "max_concurrent": 100
            },
            "commands": {
                "default_timeout_seconds": 30,
                "max_async_timeout_seconds": 300,
                "queue_size": 1000,
                "worker_pool_size": 10
            },
            "logging": {
                "log_dir": ".cheng_bot/logs",
                "max_size_mb": 100,
                "retention_days": 30
            },
            "security": {
                "workspace_root": ".",
                "allowed_shell_commands": [
                    "ls", "cat", "grep", "find", "git",
                    "npm", "pip", "python", "node",
                    "pytest", "jest", "cargo", "go"
                ],
                "enforce_whitelist": True
            }
        }
    
    def get(self, key_path: str, default: Any = None) -> Any:
        """
        Get a configuration value by dot-separated key path.
        
        Args:
            key_path: Dot-separated path to config value (e.g., "api.port")
            default: Default value if key not found
            
        Returns:
            Configuration value or default
        """
        if self._config is None:
            self.load()
        
        keys = key_path.split('.')
        value = self._config
        
        for key in keys:
            if isinstance(value, dict) and key in value:
                value = value[key]
            else:
                return default
        
        return value
    
    def reload(self) -> Dict[str, Any]:
        """
        Reload configuration from file.
        
        Returns:
            Updated configuration dictionary
        """
        self._config = None
        return self.load()


# Global configuration instance
_config_loader: Optional[ConfigLoader] = None


def get_config_loader(config_path: str = ".cheng_bot/config.yaml") -> ConfigLoader:
    """
    Get the global configuration loader instance.
    
    Args:
        config_path: Path to configuration file
        
    Returns:
        ConfigLoader instance
    """
    global _config_loader
    if _config_loader is None:
        _config_loader = ConfigLoader(config_path)
    return _config_loader


def get_config(key_path: str = None, default: Any = None) -> Any:
    """
    Get configuration value(s).
    
    Args:
        key_path: Optional dot-separated path to specific value
        default: Default value if key not found
        
    Returns:
        Configuration value or entire config dict if key_path is None
    """
    loader = get_config_loader()
    if key_path is None:
        return loader.load()
    return loader.get(key_path, default)
