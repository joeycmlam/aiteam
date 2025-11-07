import os
from typing import Dict
from shared.llm_manager import LLMManager

class QAAgent:
    """Builds Cucumber/Gherkin tests"""
    
    def __init__(self, llm_config: Dict):
        self.llm_config = llm_config
        self.llm = LLMManager()
        print("🧪 QA Agent initialized")
    
    def create_feature_files(self, requirements: Dict, output_dir: str):
        """Creates Cucumber feature files from requirements"""
        print(f"\n📄 Creating feature files in: {output_dir}")
        
        os.makedirs(output_dir, exist_ok=True)
        
        for story in requirements.get('user_stories', []):
            feature_content = self._generate_feature_with_llm(story)
            
            filename = f"{story['ticket_id'].lower().replace('-', '_')}.feature"
            filepath = os.path.join(output_dir, filename)
            
            with open(filepath, 'w') as f:
                f.write(feature_content)
            
            print(f"   ✅ Created: {filename}")
    
    def _generate_feature_with_llm(self, story: Dict) -> str:
        """Generates Gherkin feature content using LLM"""
        
        prompt = f"""Create a Cucumber/Gherkin feature file for:

Title: {story['title']}
Description: {story['description']}

Generate complete Gherkin syntax with:
- Feature description
- Background (if needed)
- At least 2 scenarios (happy path + error case)
- Use proper Given-When-Then format"""

        try:
            llm_response = self.llm.generate(
                prompt,
                system_message="You are a QA engineer expert in BDD and Gherkin syntax."
            )
            return llm_response
        except:
            # Fallback template
            feature = f"""Feature: {story['title']}
  {story['description']}

  Background:
    Given the system is initialized
    And test data is loaded

  Scenario: Happy path implementation
    Given valid input data
    When the feature is executed
    Then it should complete successfully
    And meet all acceptance criteria
    
  Scenario: Error handling
    Given invalid input is provided
    When the feature is executed
    Then it should handle errors gracefully
    And return appropriate error message
"""
            return feature
