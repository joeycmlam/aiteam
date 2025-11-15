#!/usr/bin/env python3
"""
Test Architect Agent integration with BA Agent output
Tests the BA → Architect flow for system architecture design
"""

import os
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from agents.architect_agent import ArchitectAgent

def test_architect_with_ba_output():
    """Test Architect Agent reading BA output and designing architecture"""
    
    print("=" * 80)
    print("🧪 Testing Architect Agent with BA Analysis Output")
    print("=" * 80)
    
    # Initialize Architect Agent
    llm_config = {
        'provider': os.getenv('LLM_PROVIDER', 'github_copilot_cli'),
        'model': os.getenv('GITHUB_MODEL', 'gpt-4o'),
        'temperature': 0.7
    }
    
    architect = ArchitectAgent(llm_config)
    
    # Path to BA Agent's output
    ba_output_path = '/Users/joeylam/repo/pps/requirements/analysis/requirements_structured.json'
    
    # Output directory for architecture
    output_dir = '/Users/joeylam/repo/pps/architecture'
    
    # Test 1: Read BA Analysis
    print("\n" + "=" * 80)
    print("TEST 1: Reading BA Analysis")
    print("=" * 80)
    
    try:
        ba_analysis = architect.read_ba_analysis(ba_output_path)
        print(f"✅ Successfully read BA analysis")
        print(f"   - Has raw requirements: {bool(ba_analysis.get('raw_requirements'))}")
        print(f"   - Has AI analysis: {bool(ba_analysis.get('ai_analysis'))}")
        print(f"   - Has scenarios: {bool(ba_analysis.get('scenarios'))}")
        print(f"   - User stories count: {len(ba_analysis.get('user_stories', []))}")
    except Exception as e:
        print(f"❌ Failed to read BA analysis: {e}")
        return False
    
    # Test 2: Design System Architecture
    print("\n" + "=" * 80)
    print("TEST 2: Designing System Architecture")
    print("=" * 80)
    
    try:
        architecture = architect.design_system_architecture(
            ba_analysis=ba_output_path,
            output_dir=output_dir
        )
        
        print(f"✅ Successfully generated architecture design")
        print(f"   - Generated at: {architecture.get('generated_at')}")
        print(f"   - Source analysis from: {architecture['source_analysis'].get('generated_at')}")
        print(f"   - Architecture markdown length: {len(architecture.get('architecture_markdown', ''))} chars")
        
        # Show first 500 chars of architecture
        arch_preview = architecture.get('architecture_markdown', '')[:500]
        print(f"\n📄 Architecture Preview (first 500 chars):")
        print("-" * 80)
        print(arch_preview)
        print("-" * 80)
        
    except Exception as e:
        print(f"❌ Failed to design architecture: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    # Test 3: Test with dict input (context passing)
    print("\n" + "=" * 80)
    print("TEST 3: Architecture Design with Dict Input (Context Passing)")
    print("=" * 80)
    
    try:
        architecture2 = architect.design_system_architecture(
            ba_analysis=ba_analysis,  # Pass dict directly
            output_dir=None  # Don't save this time
        )
        
        print(f"✅ Successfully generated architecture from dict context")
        print(f"   - Generated at: {architecture2.get('generated_at')}")
        
    except Exception as e:
        print(f"❌ Failed with dict input: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    print("\n" + "=" * 80)
    print("✅ ALL TESTS PASSED")
    print("=" * 80)
    print(f"\n📁 Check outputs at: {output_dir}")
    print(f"   - system_architecture.md (human-readable)")
    print(f"   - architecture_structured.json (machine-readable)")
    
    return True

if __name__ == '__main__':
    success = test_architect_with_ba_output()
    sys.exit(0 if success else 1)
