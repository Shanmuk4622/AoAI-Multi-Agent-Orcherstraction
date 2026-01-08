# AoAI — Agent of Agents Infrastructure

**Multi-Agent Math Animation Pipeline**

Generates educational math videos from natural language using orchestrated LLM agents.

**Text** :"cd ..; .\.venv\Scripts\python.exe -m manim -pql .\aoai\storage\outputs\scene.py GeneratedScene"
---

## 🏗 Architecture

```
User Prompt
    ↓
[Agent A: Logician] → Math Reasoning (Groq)
    ↓
[Agent B: Director] → Scene Planning (Groq)
    ↓
[Agent C: Engineer] → Manim Code (Gemini)
    ↓
[Execution Sandbox] → Render Video
    ↓ (if error)
[Agent D: Fixer] → Patch Code (Groq)
    ↓
Final Video Output
```

---

## 📦 Requirements

```bash
pip install groq google-generativeai manim
```

---

## 🔑 Environment Setup

Create `.env` file:

```
GROQ_API_KEY=your_groq_key_here
GEMINI_API_KEY=your_gemini_key_here
```

---

## 🚀 Usage

```bash
cd aoai
python main.py "Explain the derivative concept"
```

Output:
- Video: `storage/outputs/`
- Logs: `storage/logs/`

---

## 📁 Directory Structure

```
aoai/
 ├─ agents/          # 4 agent modules (Logician, Director, Engineer, Fixer)
 ├─ llm/             # API clients (Groq, Gemini)
 ├─ pipeline/        # Orchestrator + Sandbox + Retry Manager
 ├─ storage/         # outputs/ logs/ temp/
 ├─ utils/           # Prompts, validators, file I/O
 └─ main.py          # CLI entry point
```

---

## 🔄 Implementation Status

- [x] Step 1: Folder structure + base files
- [ ] Step 2: Groq + Gemini API clients
- [ ] Step 3: Agent prompts & validators
- [ ] Step 4: Orchestrator pipeline
- [ ] Step 5: Execution sandbox
- [ ] Step 6: Retry + fixer loop
- [ ] Step 7: CLI entrypoint
- [ ] Step 8: First test animation

---

## 📝 Development

Each module includes console logging (`print` statements) for troubleshooting.

To test individual components:

```python
from agents.logician_agent import LogicianAgent
from llm.groq_client import GroqClient

client = GroqClient()
agent = LogicianAgent(client)
result = agent.process("Explain derivatives")
```

---

## 🎯 Next Steps

1. Implement actual API calls in `groq_client.py` and `gemini_client.py`
2. Connect agents to LLM clients with prompt templates
3. Add JSON validation between stages
4. Implement Manim execution in sandbox
5. Test full pipeline end-to-end
