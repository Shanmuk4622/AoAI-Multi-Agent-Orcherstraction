"""
Test the Narrator Agent
"""
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

from agents.narrator_agent import NarratorAgent
from llm.groq_client import GroqClient
from dotenv import load_dotenv

load_dotenv()

# Initialize
client = GroqClient()
narrator = NarratorAgent(client)

# Test data
reasoning = {
    "concept": "Pythagorean Theorem",
    "steps": [
        "Visualize a right-angled triangle with sides a, b, and hypotenuse c",
        "Create squares on each side to show area relationships",
        "Demonstrate that a² + b² = c²"
    ]
}

scene_manifest = {
    "scenes": [
        {
            "title": "Introduction to Right Triangle",
            "objects": ["Triangle", "Text"],
            "animations": ["FadeIn", "Write"]
        },
        {
            "title": "Building Squares",
            "objects": ["Square", "Square", "Square"],
            "animations": ["Create", "Transform"]
        },
        {
            "title": "The Formula",
            "objects": ["Text", "Equation"],
            "animations": ["Write", "Highlight"]
        }
    ]
}

# Generate narration
print("\n" + "="*60)
print("TESTING NARRATOR AGENT")
print("="*60)

result = narrator.process(scene_manifest, reasoning)

print("\n" + "="*60)
print("GENERATED NARRATION")
print("="*60)
print(f"\nTotal narrations: {len(result['narrations'])}\n")

for i, narr in enumerate(result['narrations']):
    print(f"Scene {narr['scene_index']}: {narr['text']}")
    print(f"Duration: {narr['duration']}s\n")
