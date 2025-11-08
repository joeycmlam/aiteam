import os
import requests
import subprocess
import json
from typing import Dict, Optional
import ollama
from dotenv import load_dotenv

load_dotenv()

class LLMManager:
    """Manages LLM calls using GitHub Copilot CLI, Ollama, or other providers"""
    
    def __init__(self, provider: str = None):
        self.provider = provider or os.getenv('LLM_PROVIDER', 'ollama')
        self.github_token = os.getenv('GITHUB_TOKEN')
        self.ollama_host = os.getenv('OLLAMA_HOST', 'http://localhost:11434')
        self.ollama_model = os.getenv('OLLAMA_MODEL', 'llama3.2')
        
        print(f"🤖 LLM Manager initialized with provider: {self.provider}")
        
        # Check if gh CLI is available for github_copilot_cli provider
        if self.provider == 'github_copilot_cli':
            try:
                result = subprocess.run(['gh', '--version'], capture_output=True, text=True)
                if result.returncode == 0:
                    print(f"✅ GitHub CLI detected: {result.stdout.split()[2]}")
                else:
                    print("⚠️  GitHub CLI not found. Install with: brew install gh")
            except FileNotFoundError:
                print("⚠️  GitHub CLI not found. Install with: brew install gh")
    
    def generate(self, prompt: str, system_message: str = None, max_tokens: int = 4000) -> str:
        """Generate text using configured LLM"""
        
        if self.provider == 'github_copilot_cli':
            return self._generate_with_github_copilot_cli(prompt, system_message)
        elif self.provider == 'github_copilot':
            return self._generate_with_github_copilot(prompt, system_message)
        else:
            return self._generate_with_ollama(prompt, system_message)
    
    def _generate_with_github_copilot(self, prompt: str, system_message: str = None) -> str:
        """
        Use GitHub Copilot API
        Note: This uses Copilot's completion API which is part of your subscription
        """
        try:
            # GitHub Copilot uses a special API endpoint
            # For now, we'll use Ollama as primary since Copilot API is mainly for IDE
            print("ℹ️  GitHub Copilot works best in the IDE. Using Ollama for programmatic access...")
            return self._generate_with_ollama(prompt, system_message)
            
        except Exception as e:
            print(f"⚠️  GitHub Copilot API error: {e}")
            print("   Falling back to Ollama...")
            return self._generate_with_ollama(prompt, system_message)
    
    def _generate_with_github_copilot_cli(self, prompt: str, system_message: str = None) -> str:
        """Use GitHub Copilot CLI (gh copilot)"""
        try:
            # Combine system message and prompt
            full_prompt = prompt
            if system_message:
                full_prompt = f"{system_message}\n\n{prompt}"
            
            # Use gh copilot suggest command interactively
            # The gh copilot extension uses stdin/stdout for interaction
            print("   🤖 Calling GitHub Copilot CLI...")
            
            result = subprocess.run(
                ['gh', 'copilot', 'suggest', '--target', 'shell'],
                input=full_prompt,
                capture_output=True,
                text=True,
                timeout=60
            )
            
            if result.returncode == 0:
                # Extract the suggestion from the output
                output = result.stdout.strip()
                
                # gh copilot suggest returns formatted output, extract the actual suggestion
                # It usually has markers like "Suggestion:" or code blocks
                if output:
                    # Try to extract code block if present
                    if '```' in output:
                        parts = output.split('```')
                        if len(parts) >= 3:
                            # Get content between first pair of ```
                            code = parts[1]
                            # Remove language identifier if present
                            lines = code.split('\n')
                            if lines[0].strip() in ['python', 'bash', 'sh', 'javascript', 'typescript']:
                                code = '\n'.join(lines[1:])
                            return code.strip()
                    
                    return output
                else:
                    print("⚠️  Empty response from GitHub Copilot CLI")
                    print("   Falling back to Ollama...")
                    return self._generate_with_ollama(prompt, system_message)
            else:
                error_msg = result.stderr.strip()
                
                # Check for specific error conditions
                if 'not logged in' in error_msg.lower() or 'authentication' in error_msg.lower():
                    print("⚠️  GitHub CLI not authenticated")
                    print("   Run: gh auth login")
                    print("   Falling back to Ollama...")
                elif 'extension not installed' in error_msg.lower() or 'unknown command' in error_msg.lower():
                    print("⚠️  GitHub Copilot extension not installed")
                    print("   Install with: gh extension install github/gh-copilot")
                    print("   Falling back to Ollama...")
                else:
                    print(f"⚠️  GitHub Copilot CLI error: {error_msg[:200]}")
                    print("   Falling back to Ollama...")
                
                return self._generate_with_ollama(prompt, system_message)
                
        except FileNotFoundError:
            print("⚠️  GitHub CLI (gh) not found")
            print("   Install with: brew install gh")
            print("   Then run: gh auth login")
            print("   And install extension: gh extension install github/gh-copilot")
            print("   Falling back to Ollama...")
            return self._generate_with_ollama(prompt, system_message)
        except subprocess.TimeoutExpired:
            print("⚠️  GitHub Copilot CLI timeout (>60s)")
            print("   Falling back to Ollama...")
            return self._generate_with_ollama(prompt, system_message)
        except Exception as e:
            print(f"⚠️  GitHub Copilot CLI error: {type(e).__name__}: {e}")
            print("   Falling back to Ollama...")
            return self._generate_with_ollama(prompt, system_message)
    
    def _generate_with_ollama(self, prompt: str, system_message: str = None) -> str:
        """Use Ollama local LLM"""
        try:
            # Build the full prompt
            full_prompt = prompt
            if system_message:
                full_prompt = f"{system_message}\n\n{prompt}"
            
            # Call Ollama
            response = ollama.generate(
                model=self.ollama_model,
                prompt=full_prompt
            )
            
            return response['response']
            
        except ConnectionError as e:
            print(f"⚠️  Ollama connection error: {e}")
            print("   Make sure Ollama is running: ollama serve")
            return f"[LLM unavailable - manual review needed]\n\nPrompt was: {prompt[:200]}..."
        except KeyError as e:
            print(f"⚠️  Unexpected Ollama response format: {e}")
            return f"[LLM response error - manual review needed]"
        except Exception as e:
            print(f"⚠️  Unexpected error: {type(e).__name__}: {e}")
            # Return a fallback response
            return f"[LLM unavailable - manual review needed]\n\nPrompt was: {prompt[:200]}..."
    
    def analyze_code(self, code: str, question: str) -> str:
        """Analyze code with specific question"""
        prompt = f"""Analyze this code:

```
{code[:2000]}
```

Question: {question}

Provide a concise analysis:"""
        
        return self.generate(prompt, system_message="You are a senior software architect.")
    
    def generate_code(self, requirements: str, language: str = "python") -> str:
        """Generate code from requirements"""
        prompt = f"""Generate {language} code for these requirements:

{requirements}

Provide clean, production-ready code with:
- Error handling
- Documentation
- Type hints (if applicable)

Code:"""
        
        return self.generate(prompt, system_message=f"You are an expert {language} developer.")
