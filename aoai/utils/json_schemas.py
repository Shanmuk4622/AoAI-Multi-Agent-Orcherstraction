"""
JSON Schema Validators
Validate agent outputs before passing to next stage
"""
import json
from typing import Dict, Any, Tuple, Union


def validate_logician_output(output: str) -> Tuple[bool, Union[Dict[str, Any], str]]:
    """
    Validate Logician Agent JSON output.
    
    Args:
        output: Raw string from LLM
        
    Returns:
        (is_valid, parsed_json_or_error_message)
    """
    try:
        data = json.loads(output)
        
        # Check required fields
        if "concept" not in data:
            return False, "Missing 'concept' field"
        
        if "steps" not in data:
            return False, "Missing 'steps' field"
        
        if not isinstance(data["steps"], list):
            return False, "'steps' must be a list"
        
        if len(data["steps"]) == 0:
            return False, "'steps' cannot be empty"
        
        return True, data
        
    except json.JSONDecodeError as e:
        return False, f"Invalid JSON: {str(e)}"


def validate_director_output(output: str) -> Tuple[bool, Union[Dict[str, Any], str]]:
    """
    Validate Director Agent JSON output.
    
    Args:
        output: Raw string from LLM
        
    Returns:
        (is_valid, parsed_json_or_error_message)
    """
    try:
        data = json.loads(output)
        
        if "scenes" not in data:
            return False, "Missing 'scenes' field"
        
        if not isinstance(data["scenes"], list):
            return False, "'scenes' must be a list"
        
        if len(data["scenes"]) == 0:
            return False, "'scenes' cannot be empty"
        
        # Validate each scene
        for i, scene in enumerate(data["scenes"]):
            if "title" not in scene:
                return False, f"Scene {i} missing 'title'"
            if "objects" not in scene:
                return False, f"Scene {i} missing 'objects'"
            if "animations" not in scene:
                return False, f"Scene {i} missing 'animations'"
            
            if not isinstance(scene["objects"], list):
                return False, f"Scene {i} 'objects' must be a list"
            if not isinstance(scene["animations"], list):
                return False, f"Scene {i} 'animations' must be a list"
        
        return True, data
        
    except json.JSONDecodeError as e:
        return False, f"Invalid JSON: {str(e)}"


def validate_engineer_output(code: str) -> Tuple[bool, str]:
    """
    Validate Engineer Agent code output (basic checks).
    
    Args:
        code: Generated Python script
        
    Returns:
        (is_valid, error_message_or_empty)
    """
    if not code.strip():
        return False, "Generated code is empty"
    
    if "from manim import" not in code:
        return False, "Missing Manim import statement"
    
    if "class GeneratedScene" not in code:
        return False, "Missing GeneratedScene class definition"
    
    if "def construct" not in code:
        return False, "Missing construct() method"
    
    # Check for basic Python syntax (naive check)
    try:
        compile(code, '<string>', 'exec')
        return True, ""
    except SyntaxError as e:
        return False, f"Syntax error: {str(e)}"


def validate_fixer_output(code: str) -> Tuple[bool, str]:
    """
    Validate Fixer Agent code output (same checks as Engineer).
    
    Args:
        code: Patched Python script
        
    Returns:
        (is_valid, error_message_or_empty)
    """
    return validate_engineer_output(code)
