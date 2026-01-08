"""
File I/O Utilities
Helper functions for saving logs, code, and outputs
"""
import json
from pathlib import Path
from datetime import datetime
from typing import Dict, Any


def save_json_log(data: Dict[str, Any], log_dir: Path, prefix: str):
    """
    Save JSON data to timestamped log file.
    
    Args:
        data: Dictionary to save
        log_dir: Directory to save in
        prefix: Filename prefix (e.g., 'logician', 'director')
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{prefix}_{timestamp}.json"
    filepath = log_dir / filename
    
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2)
    
    print(f"💾 Saved log: {filepath}")


def save_code(code: str, output_dir: Path, filename: str = "scene.py"):
    """
    Save generated code to file.
    
    Args:
        code: Python script content
        output_dir: Directory to save in
        filename: Output filename
        
    Returns:
        Path to saved file
    """
    filepath = output_dir / filename
    filepath.write_text(code, encoding='utf-8')
    
    print(f"💾 Saved code: {filepath}")
    return filepath


def read_error_log(log_path: Path) -> str:
    """
    Read error log from file.
    
    Args:
        log_path: Path to log file
        
    Returns:
        Log contents as string
    """
    if not log_path.exists():
        return ""
    
    return log_path.read_text(encoding='utf-8')
