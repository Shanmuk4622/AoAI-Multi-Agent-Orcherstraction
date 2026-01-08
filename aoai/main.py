"""
AoAI — Agent of Agents Infrastructure
Main entry point for the multi-agent animation pipeline
"""
import sys
import os
import argparse
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Import LLM clients
from llm.groq_client import GroqClient
from llm.gemini_client import GeminiClient

# Import agents
from agents.logician_agent import LogicianAgent
from agents.director_agent import DirectorAgent
from agents.engineer_agent import EngineerAgent
from agents.fixer_agent import FixerAgent
from agents.narrator_agent import NarratorAgent

# Import pipeline
from pipeline.orchestrator import Orchestrator
from pipeline.execution_sandbox import ExecutionSandbox
from pipeline.retry_manager import RetryManager


def main():
    """CLI entry point"""
    parser = argparse.ArgumentParser(
        description="AoAI — Generate math animations from natural language"
    )
    parser.add_argument(
        "prompt",
        type=str,
        help="Math concept to visualize (e.g., 'Explain derivatives')"
    )
    parser.add_argument(
        "--no-logs",
        action="store_true",
        help="Disable saving intermediate logs"
    )
    parser.add_argument(
        "--execute",
        action="store_true",
        help="Execute Manim rendering after code generation (requires manim installed)"
    )
    parser.add_argument(
        "--debug",
        action="store_true",
        help="Enable verbose debug output"
    )
    
    args = parser.parse_args()
    
    # Print banner
    print("\n" + "="*60)
    print("  🎬 AoAI — Agent of Agents Infrastructure")
    print("  Multi-Agent Math Animation Pipeline")
    print("="*60 + "\n")
    
    try:
        # Check for API keys
        if not os.getenv("GROQ_API_KEY"):
            print("❌ Error: GROQ_API_KEY not found in environment")
            print("   Please set it in .env file or environment variables")
            return 1
        
        if not os.getenv("GEMINI_API_KEY"):
            print("❌ Error: GEMINI_API_KEY not found in environment")
            print("   Please set it in .env file or environment variables")
            return 1
        
        # Initialize LLM clients
        print("📡 Initializing API clients...")
        groq_client = GroqClient()
        gemini_client = GeminiClient()
        
        # Initialize agents (using Groq for all due to Gemini compatibility issues)
        print("\n🤖 Initializing agents...")
        logician = LogicianAgent(groq_client)
        director = DirectorAgent(groq_client)
        engineer = EngineerAgent(groq_client)  # Using Groq instead of Gemini
        fixer = FixerAgent(groq_client)
        narrator = NarratorAgent(groq_client)
        
        # Initialize pipeline components
        print("\n⚙️  Initializing pipeline...")
        storage_path = Path(__file__).parent / "storage"
        sandbox = ExecutionSandbox(storage_path)
        retry_manager = RetryManager(fixer, sandbox)
        
        # Create orchestrator
        orchestrator = Orchestrator(
            agents={
                'logician': logician,
                'director': director,
                'engineer': engineer,
                'fixer': fixer,
                'narrator': narrator
            },
            storage_path=storage_path,
            sandbox=sandbox,
            retry_manager=retry_manager
        )
        
        # Run pipeline
        result = orchestrator.run(args.prompt, save_logs=not args.no_logs, execute=args.execute)
        
        # Print final result
        print("\n" + "="*60)
        if result["success"]:
            print("✅ PIPELINE COMPLETED SUCCESSFULLY")
            if result["code_path"]:
                print(f"📄 Code: {result['code_path']}")
            if result.get("video_path"):
                print(f"📹 Video: {result['video_path']}")
            print(f"📊 Logs: {storage_path / 'logs'}")
        else:
            print("❌ PIPELINE FAILED")
            print(f"Error: {result.get('error', 'Unknown error')}")
        print("="*60 + "\n")
        
        return 0 if result["success"] else 1
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Pipeline interrupted by user")
        return 130
        
    except Exception as e:
        print(f"\n❌ Fatal error: {str(e)}")
        if args.debug:
            import traceback
            traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
