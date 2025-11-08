import os
import requests
import subprocess
import json
from typing import Dict, Optional
import ollama
from dotenv import load_dotenv

# Load .env file with override=True to ensure .env values take precedence
load_dotenv(override=True)

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
    
    def _fallback_to_ollama(self, prompt: str, system_message: str = None, reason: str = None) -> str:
        """Helper method to fallback to Ollama with consistent messaging"""
        if reason:
            print(f"⚠️  {reason}")
        print("   Falling back to Ollama...")
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
            return self._fallback_to_ollama(prompt, system_message, f"GitHub Copilot API error: {e}")
    
    def _generate_with_github_copilot_cli(self, prompt: str, system_message: str = None) -> str:
        """
        Use GitHub Models API (available with Copilot subscription)
        
        Provides access to GPT-4o and other models through GitHub Models API.
        Included with GitHub Copilot subscription.
        
        Available models: gpt-4o, gpt-4o-mini, mistral-large
        (Claude models are NOT available)
        
        Requires: GITHUB_TOKEN in .env file with 'read:user' scope
        """
        # Check if GitHub token is configured
        if not self.github_token:
            print("   GITHUB_TOKEN not found in .env file")
            print("   Get your token from: https://github.com/settings/tokens")
            print("   Add to .env: GITHUB_TOKEN=your_token_here")
            return self._fallback_to_ollama(prompt, system_message)
        
        try:            
            print("   🤖 Calling GitHub Models API (GPT-4o)...")
            
            # Build messages
            messages = []
            if system_message:
                messages.append({"role": "system", "content": system_message})
            messages.append({"role": "user", "content": prompt})
            
            # API request
            response = requests.post(
                "https://models.inference.ai.azure.com/chat/completions",
                json={
                    "messages": messages,
                    "model": "gpt-4o",  # Options: gpt-4o, gpt-4o-mini, mistral-large
                    "temperature": 0.3,
                    "max_tokens": 4000,
                    "top_p": 1.0
                },
                headers={
                    "Content-Type": "application/json",
                    "Authorization": f"Bearer {self.github_token}"
                },
                timeout=60
            )
            
            # Handle successful response
            if response.status_code == 200:
                content = response.json()['choices'][0]['message']['content']
                print(f"   ✅ GitHub Models API response received")
                return content
            
            # Handle specific error codes
            error_messages = {
                401: ("GitHub token is invalid or expired",
                      "Get a new token from: https://github.com/settings/tokens",
                      "Scopes needed: 'read:user'"),
                403: ("GitHub Models API access denied",
                      "This feature requires GitHub Copilot subscription",
                      "Check: https://github.com/settings/copilot"),
                429: ("GitHub Models API rate limit exceeded",
                      "Wait a few minutes and try again",
                      "")
            }
            
            if response.status_code in error_messages:
                for msg in error_messages[response.status_code]:
                    if msg:
                        print(f"   {msg}")
            else:
                error_msg = response.text[:200] if response.text else "Unknown error"
                print(f"   GitHub Models API error (status {response.status_code})")
                print(f"   {error_msg}")
            
            return self._fallback_to_ollama(prompt, system_message)
                
        except requests.exceptions.Timeout:
            return self._fallback_to_ollama(prompt, system_message, 
                                           "GitHub Models API timeout (>60s)")
        
        except requests.exceptions.ConnectionError as e:
            print(f"   Connection error: {e}")
            print("   Check your internet connection")
            return self._fallback_to_ollama(prompt, system_message)
        
        except Exception as e:
            return self._fallback_to_ollama(prompt, system_message,
                                           f"Unexpected error: {type(e).__name__}: {e}")
    
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
