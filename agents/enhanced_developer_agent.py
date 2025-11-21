"""
Developer Agent - Enhanced with Agent Framework
Developer agent for code implementation following technical specifications
"""
import os
import sys
from pathlib import Path
from typing import Dict, Any, Optional, List

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from shared.agent_framework import Agent
from shared.llm_manager import LLMManager


class EnhancedDeveloperAgent(Agent):
    """
    Enhanced Developer Agent using the agent framework
    Implements code based on technical specifications
    """
    
    def __init__(self, 
                 output_dir: str = "implementation",
                 config_path: Optional[str] = None):
        super().__init__(
            name="Developer",
            role="Software Developer - Code implementation and testing",
            output_dir=output_dir,
            config_path=config_path or "config/agents/developer.yaml"
        )
        
        self.llm_manager = LLMManager()
    
    def process(self, input_data: Any) -> Dict[str, Any]:
        """
        Process technical specifications to generate code
        
        Args:
            input_data: Dictionary with 'technical_structure' and 'tasks' or file paths
            
        Returns:
            Dictionary with implementation results
        """
        self.log_action("start_processing", {"input_type": type(input_data).__name__})
        
        # Load inputs
        if isinstance(input_data, dict):
            technical_structure = input_data.get('technical_structure', '')
            tasks = input_data.get('tasks', '')
        else:
            technical_structure = str(input_data)
            tasks = ""
        
        self.set_context('technical_structure', technical_structure)
        self.set_context('tasks', tasks)
        
        # Generate code modules
        code_modules = self.generate_code_modules(technical_structure, tasks)
        
        # Generate tests
        tests = self.generate_tests(technical_structure, code_modules)
        
        # Create documentation
        documentation = self.create_documentation(code_modules)
        
        # Save outputs
        files_created = []
        
        # Save code modules
        for module_name, module_code in code_modules.items():
            filepath = self.save_output(f"{module_name}.py", module_code, subdir="src")
            files_created.append(filepath)
        
        # Save tests
        for test_name, test_code in tests.items():
            filepath = self.save_output(f"{test_name}.py", test_code, subdir="tests")
            files_created.append(filepath)
        
        # Save documentation
        doc_file = self.save_output("README.md", documentation, subdir="docs")
        files_created.append(doc_file)
        
        result = {
            'code_modules': code_modules,
            'tests': tests,
            'documentation': documentation,
            'files': files_created
        }
        
        self.log_action("completed", {"files_created": len(files_created)})
        
        return result
    
    def generate_code_modules(self, technical_structure: str, tasks: str) -> Dict[str, str]:
        """Generate code modules based on technical structure"""
        self.log_action("generate_code_modules")
        
        prompt = f"""As an expert Software Developer, implement code modules based on this technical structure:

{technical_structure}

Tasks to implement:
{tasks if tasks else "Implement all core modules"}

Generate production-ready Python code with:
- Clear class and function names
- Type hints
- Comprehensive docstrings
- Error handling
- Logging
- Input validation
- SOLID principles
- Clean code practices

Return modules as a dictionary: {{"module_name": "code_content"}}

For each module:
1. Imports
2. Class/function definitions
3. Documentation
4. Error handling
5. Logging setup

Focus on:
- portfolio_manager.py (main business logic)
- transaction_handler.py (transaction processing)
- data_models.py (data structures)
- utils.py (helper functions)"""

        response = self.llm_manager.generate(
            prompt=prompt,
            max_tokens=4000
        )
        
        # Parse response into modules (simplified - in real implementation, parse properly)
        modules = self._parse_modules_from_response(response)
        
        return modules
    
    def generate_tests(self, technical_structure: str, code_modules: Dict[str, str]) -> Dict[str, str]:
        """Generate test cases for code modules"""
        self.log_action("generate_tests")
        
        test_modules = {}
        
        for module_name, module_code in code_modules.items():
            prompt = f"""As an expert Software Developer, write comprehensive unit tests for this module:

Module: {module_name}
Code:
{module_code}

Generate pytest test cases with:
- Test fixtures
- Happy path tests
- Edge case tests
- Error condition tests
- Mock external dependencies
- Clear test names
- Assertions with messages
- >80% code coverage

Use pytest best practices."""

            response = self.llm_manager.generate(
                prompt=prompt,
                max_tokens=2000
            )
            
            test_name = f"test_{module_name.replace('.py', '')}"
            test_modules[test_name] = response
        
        return test_modules
    
    def create_documentation(self, code_modules: Dict[str, str]) -> str:
        """Create implementation documentation"""
        self.log_action("create_documentation")
        
        modules_summary = "\n".join([f"- {name}" for name in code_modules.keys()])
        
        prompt = f"""As a Software Developer, create comprehensive README documentation for this implementation:

Modules implemented:
{modules_summary}

Include:

# Project Implementation

## Overview
Brief description of what was implemented

## Modules

### Module 1: [Name]
- Purpose
- Key classes/functions
- Usage examples

## Setup Instructions
1. Installation
2. Configuration
3. Running the application

## Usage Examples
```python
# Example code
```

## Testing
How to run tests

## Architecture
High-level architecture diagram (text)

## API Documentation
Key APIs and their usage

Format as Markdown."""

        response = self.llm_manager.generate(
            prompt=prompt,
            max_tokens=2000
        )
        
        return response
    
    def _parse_modules_from_response(self, response: str) -> Dict[str, str]:
        """Parse module code from LLM response"""
        # Simplified parsing - in production, use proper parsing
        modules = {}
        
        # For now, create placeholder modules
        modules["portfolio_manager"] = self._create_portfolio_manager_code()
        modules["transaction_handler"] = self._create_transaction_handler_code()
        modules["data_models"] = self._create_data_models_code()
        
        return modules
    
    def _create_portfolio_manager_code(self) -> str:
        """Create portfolio manager module code"""
        return '''"""
Portfolio Manager Module
Manages portfolio operations and calculations
"""
from typing import List, Dict, Any
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class PortfolioManager:
    """
    Manages investment portfolio operations
    
    Attributes:
        user_id: Unique identifier for the user
        transactions: List of portfolio transactions
    """
    
    def __init__(self, user_id: str):
        """
        Initialize Portfolio Manager
        
        Args:
            user_id: Unique user identifier
        """
        self.user_id = user_id
        self.transactions: List[Dict[str, Any]] = []
        logger.info(f"Portfolio Manager initialized for user {user_id}")
    
    def add_transaction(self, transaction: Dict[str, Any]) -> bool:
        """
        Add a transaction to the portfolio
        
        Args:
            transaction: Transaction details (type, asset, quantity, price, date)
            
        Returns:
            True if successful, False otherwise
            
        Raises:
            ValueError: If transaction data is invalid
        """
        required_fields = ['type', 'asset', 'quantity', 'price', 'date']
        
        try:
            # Validate transaction
            for field in required_fields:
                if field not in transaction:
                    raise ValueError(f"Missing required field: {field}")
            
            # Add transaction
            self.transactions.append(transaction)
            logger.info(f"Transaction added: {transaction['type']} {transaction['asset']}")
            
            return True
            
        except Exception as e:
            logger.error(f"Failed to add transaction: {e}")
            raise
    
    def calculate_total_value(self) -> float:
        """
        Calculate total portfolio value
        
        Returns:
            Total portfolio value
        """
        try:
            total = sum(
                t['quantity'] * t['price'] 
                for t in self.transactions 
                if t['type'] == 'buy'
            )
            logger.info(f"Total portfolio value calculated: {total}")
            return total
        except Exception as e:
            logger.error(f"Error calculating total value: {e}")
            raise
    
    def get_position(self, asset: str) -> Dict[str, Any]:
        """
        Get current position for a specific asset
        
        Args:
            asset: Asset symbol/identifier
            
        Returns:
            Position details (quantity, average_price, current_value)
        """
        try:
            asset_transactions = [
                t for t in self.transactions 
                if t['asset'] == asset
            ]
            
            if not asset_transactions:
                return {'quantity': 0, 'average_price': 0, 'current_value': 0}
            
            total_quantity = sum(
                t['quantity'] if t['type'] == 'buy' else -t['quantity']
                for t in asset_transactions
            )
            
            total_cost = sum(
                t['quantity'] * t['price']
                for t in asset_transactions
                if t['type'] == 'buy'
            )
            
            avg_price = total_cost / total_quantity if total_quantity > 0 else 0
            
            return {
                'asset': asset,
                'quantity': total_quantity,
                'average_price': avg_price,
                'current_value': total_quantity * avg_price
            }
            
        except Exception as e:
            logger.error(f"Error getting position for {asset}: {e}")
            raise
'''
    
    def _create_transaction_handler_code(self) -> str:
        """Create transaction handler module code"""
        return '''"""
Transaction Handler Module
Handles transaction validation and processing
"""
from typing import Dict, Any
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class TransactionHandler:
    """Validates and processes portfolio transactions"""
    
    VALID_TRANSACTION_TYPES = ['buy', 'sell', 'dividend', 'split']
    
    @staticmethod
    def validate_transaction(transaction: Dict[str, Any]) -> bool:
        """
        Validate transaction data
        
        Args:
            transaction: Transaction to validate
            
        Returns:
            True if valid
            
        Raises:
            ValueError: If validation fails
        """
        if transaction['type'] not in TransactionHandler.VALID_TRANSACTION_TYPES:
            raise ValueError(f"Invalid transaction type: {transaction['type']}")
        
        if transaction['quantity'] <= 0:
            raise ValueError("Quantity must be positive")
        
        if transaction['price'] < 0:
            raise ValueError("Price cannot be negative")
        
        return True
    
    @staticmethod
    def process_transaction(transaction: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process and enrich transaction
        
        Args:
            transaction: Raw transaction data
            
        Returns:
            Processed transaction with metadata
        """
        try:
            TransactionHandler.validate_transaction(transaction)
            
            processed = transaction.copy()
            processed['processed_at'] = datetime.now().isoformat()
            processed['total_value'] = transaction['quantity'] * transaction['price']
            
            logger.info(f"Transaction processed: {processed['type']} {processed['asset']}")
            
            return processed
            
        except Exception as e:
            logger.error(f"Transaction processing failed: {e}")
            raise
'''
    
    def _create_data_models_code(self) -> str:
        """Create data models module code"""
        return '''"""
Data Models Module
Defines data structures for the portfolio system
"""
from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class Transaction:
    """Transaction data model"""
    type: str
    asset: str
    quantity: float
    price: float
    date: datetime
    transaction_id: Optional[str] = None
    notes: Optional[str] = None
    
    def __post_init__(self):
        if self.transaction_id is None:
            self.transaction_id = f"{self.asset}_{int(self.date.timestamp())}"


@dataclass
class Position:
    """Position data model"""
    asset: str
    quantity: float
    average_price: float
    current_price: float
    
    @property
    def market_value(self) -> float:
        """Calculate market value"""
        return self.quantity * self.current_price
    
    @property
    def cost_basis(self) -> float:
        """Calculate cost basis"""
        return self.quantity * self.average_price
    
    @property
    def profit_loss(self) -> float:
        """Calculate profit/loss"""
        return self.market_value - self.cost_basis


@dataclass
class Portfolio:
    """Portfolio data model"""
    user_id: str
    name: str
    created_at: datetime
    updated_at: datetime
'''


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Enhanced Developer Agent")
    parser.add_argument('--technical-structure', '-t', required=True,
                       help='Technical structure file')
    parser.add_argument('--tasks', help='Development tasks file')
    parser.add_argument('--output-dir', '-o', default='implementation',
                       help='Output directory')
    parser.add_argument('--config', '-c', help='Config file path')
    
    args = parser.parse_args()
    
    # Initialize agent
    developer = EnhancedDeveloperAgent(
        output_dir=args.output_dir,
        config_path=args.config
    )
    
    # Prepare input
    input_data = {}
    
    if os.path.exists(args.technical_structure):
        input_data['technical_structure'] = developer.load_input(args.technical_structure)
    else:
        input_data['technical_structure'] = args.technical_structure
    
    if args.tasks and os.path.exists(args.tasks):
        input_data['tasks'] = developer.load_input(args.tasks)
    
    # Process
    results = developer.process(input_data)
    
    # Print summary
    print("\n" + "="*70)
    print("📊 DEVELOPER AGENT SUMMARY")
    print("="*70)
    print(f"✅ Code modules generated: {len(results['code_modules'])}")
    print(f"✅ Test modules generated: {len(results['tests'])}")
    print(f"✅ Total files created: {len(results['files'])}")
    print("\nFiles:")
    for filepath in results['files']:
        print(f"   - {filepath}")
    
    # Save history
    developer.save_history()
