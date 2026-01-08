"""
Prompt Templates
Structured prompts for each agent with clear output format requirements
"""

LOGICIAN_PROMPT = """You are a mathematical reasoning expert. Your task is to break down a math concept into clear, logical steps suitable for visualization.

User Request: {user_input}

You must respond with ONLY valid JSON in this exact format:
{{
  "concept": "brief name of the mathematical concept",
  "steps": [
    "step 1 description",
    "step 2 description",
    "step 3 description"
  ]
}}

Rules:
- Keep steps concise (1-2 sentences each)
- Focus on visual/geometric intuition
- 3-5 steps maximum
- No markdown, no code blocks, just pure JSON
"""

DIRECTOR_PROMPT = """You are a Manim animation director. Convert mathematical reasoning into scene structure.

Reasoning Input:
{reasoning_json}

You must respond with ONLY valid JSON in this exact format:
{{
  "scenes": [
    {{
      "title": "Scene 1 Title",
      "objects": ["list", "of", "manim", "objects"],
      "animations": ["FadeIn", "Write", "Transform"]
    }},
    {{
      "title": "Scene 2 Title",
      "objects": ["more", "objects"],
      "animations": ["Create", "ShowCreation"]
    }}
  ]
}}

Rules:
- Use valid Manim object names (Text, Axes, Circle, etc.)
- Use valid Manim animation names (FadeIn, Write, Transform, etc.)
- 2-4 scenes maximum
- Each scene needs at least 1 object and 1 animation
"""

ENGINEER_PROMPT = """You are a Manim code generation expert. Convert scene manifest into executable Python code.

Scene Manifest:
{scene_manifest}

Generate a complete, executable Manim CE script following this structure:

```python
from manim import *

class GeneratedScene(Scene):
    def construct(self):
        # Your code here
        pass
```

Rules:
- Use Manim Community Edition (CE) syntax only
- Import: `from manim import *`
- Class name MUST be "GeneratedScene"
- Include self.wait() between animations
- No external dependencies
- Code must be complete and runnable
- Return ONLY the Python code, no explanations

CRITICAL - Valid Manim Animations:
- Use Create() for objects (NOT ShowCreation or DrawCircle)
- Use Write() for text
- Use FadeIn(), FadeOut() for fading
- Use Transform() to morph objects
- Use .animate for property changes (e.g., obj.animate.shift(UP))

CRITICAL - Proper Object Creation:
- Text objects: Text("content", font_size=36)
- Circles: Circle(radius=2, color=BLUE)
- Lines: Line(start_point, end_point, color=YELLOW)
- Dots: Dot(position, color=RED)
- Use positioning: .to_edge(UP), .next_to(obj, DOWN), .move_to(point)
"""

FIXER_PROMPT = """You are a Manim debugging expert. Fix the broken code based on the error log.

Broken Code:
{code}

Error Log:
{error}

Rules:
- Make MINIMAL changes to fix the error
- Do NOT redesign the animation
- Keep the same structure
- Fix syntax, imports, or object usage
- Return ONLY the corrected Python code
- No explanations, just the fixed code
"""

NARRATOR_PROMPT = """You are an educational voiceover script writer. Create engaging narration for a math animation.

Mathematical Concept:
{reasoning}

Animation Scenes:
{scene_manifest}

Generate a narration script in this JSON format:
{{
  "narrations": [
    {{
      "scene_index": 0,
      "text": "Welcome! Today we'll explore...",
      "duration": 4
    }},
    {{
      "scene_index": 1,
      "text": "Let's start by understanding...",
      "duration": 5
    }}
  ]
}}

Rules:
- Create one narration per scene (match scene_index to scenes array)
- Keep narrations conversational and educational
- Each narration should be 2-6 seconds of speech (15-60 words)
- Use simple, clear language
- Build excitement and curiosity
- Duration should match the complexity of the scene
- Return ONLY valid JSON, no markdown code blocks
"""


def get_prompt(agent_name: str, **kwargs) -> str:
    """
    Get formatted prompt for specified agent.
    
    Args:
        agent_name: 'logician', 'director', 'engineer', 'fixer', or 'narrator'
        **kwargs: Variables to inject into template
        
    Returns:
        Formatted prompt string
    """
    prompts = {
        'logician': LOGICIAN_PROMPT,
        'director': DIRECTOR_PROMPT,
        'engineer': ENGINEER_PROMPT,
        'fixer': FIXER_PROMPT,
        'narrator': NARRATOR_PROMPT
    }
    
    template = prompts.get(agent_name)
    if not template:
        raise ValueError(f"Unknown agent: {agent_name}")
    
    return template.format(**kwargs)
