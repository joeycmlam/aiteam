import os
import requests
from typing import Dict, Optional
import ollama
from dotenv import load_dotenv

load_dotenv()

class LLMManager:
    """Manages LLM calls using GitHub Copilot or Ollama"""
    
    def __init__(self, provider: str = None):
        self.provider = provider or os.getenv('LLM_PROVIDER', 'ollama')
        self.github_token = os.getenv('GITHUB_TOKEN')
        self.ollama_host = os.getenv('OLLAMA_HOST', 'http://localhost:11434')
        self.ollama_model = os.getenv('OLLAMA_MODEL', 'llama3.2')
        
        print(f"🤖 LLM Manager initialized with provider: {self.provider}")
    
    def generate(self, prompt: str, system_message: str = None, max_tokens: int = 4000) -> str:
        """Generate text using configured LLM"""
        
        if self.provider == 'github_copilot':
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
