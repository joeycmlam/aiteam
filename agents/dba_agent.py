"""
DBA Agent - Database design, schema management, and optimization

Responsibilities:
- Database schema design from requirements
- Migration script generation
- Query optimization and indexing
- Data modeling and normalization
- Database testing strategies
- Performance analysis and tuning
"""

from typing import Dict, List, Optional, Any
import os
import json
from shared.llm_manager import LLMManager


class DBAAgent:
    """Database Administrator Agent for schema design and optimization"""
    
    def __init__(self, llm_config: Dict, output_dir: str = "output"):
        self.llm_config = llm_config
        self.llm = LLMManager()
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
        
        print("🗄️  Database Administrator Agent initialized")
    
    def design_schema(self, requirements: Dict, architecture: Dict = None) -> Dict:
        """
        Design database schema from requirements
        
        Args:
            requirements: Structured requirements from BA
            architecture: Architecture design from Architect
            
        Returns:
            Schema design with tables, relationships, and constraints
        """
        print("\n🗄️  Designing database schema...")
        
        # Prepare context for LLM
        context = self._prepare_schema_context(requirements, architecture)
        
        prompt = f"""
You are a senior database architect. Design a comprehensive database schema for the following requirements:

Requirements:
{json.dumps(requirements, indent=2)}

Architecture Context:
{json.dumps(architecture or {}, indent=2)}

Provide a database schema design including:

1. Tables: Define all necessary tables with columns, data types, and constraints
2. Primary Keys: Define primary keys for each table
3. Foreign Keys: Define relationships and foreign key constraints
4. Indexes: Recommend indexes for performance
5. Constraints: Check constraints, unique constraints, etc.
6. Normalization: Ensure proper normalization (3NF or higher)
7. Data Types: Choose appropriate data types for each column
8. Sample Data: Provide sample data structure

Return the schema as JSON with this structure:
{{
    "tables": [
        {{
            "name": "table_name",
            "columns": [
                {{
                    "name": "column_name",
                    "type": "data_type",
                    "nullable": true/false,
                    "primary_key": true/false,
                    "unique": true/false,
                    "default": "default_value"
                }}
            ],
            "indexes": [
                {{
                    "name": "index_name",
                    "columns": ["col1", "col2"],
                    "unique": true/false
                }}
            ],
            "constraints": [
                {{
                    "name": "constraint_name",
                    "type": "check/foreign_key/unique",
                    "definition": "constraint definition"
                }}
            ]
        }}
    ],
    "relationships": [
        {{
            "from_table": "table1",
            "to_table": "table2",
            "type": "one-to-many/many-to-many",
            "foreign_key": "fk_column"
        }}
    ],
    "recommendations": ["optimization recommendations"]
}}
"""
        
        system_message = """You are a senior database architect with expertise in:
- Relational database design and normalization
- Performance optimization and indexing strategies
- Data integrity and constraint management
- PostgreSQL, MySQL, SQL Server, and Oracle
- NoSQL databases when appropriate
- Scalability and partitioning strategies"""
        
        try:
            response = self.llm.generate(
                prompt=prompt,
                system_message=system_message,
                max_tokens=3000,
                temperature=0.3
            )
            
            schema = self._parse_schema_response(response)
            
            # Save schema design
            output_file = os.path.join(self.output_dir, 'database_schema.json')
            with open(output_file, 'w') as f:
                json.dump(schema, f, indent=2)
            
            print(f"   ✅ Schema designed with {len(schema.get('tables', []))} tables")
            print(f"   📄 Saved to: {output_file}")
            
            return schema
            
        except Exception as e:
            print(f"   ⚠️  Error designing schema: {e}")
            return self._get_default_schema()
    
    def generate_migrations(self, current_schema: Dict, new_requirements: Dict) -> Dict:
        """
        Generate migration scripts to evolve database schema
        
        Args:
            current_schema: Existing database schema
            new_requirements: New requirements requiring schema changes
            
        Returns:
            Migration scripts and rollback procedures
        """
        print("\n🔄 Generating database migrations...")
        
        prompt = f"""
You are a database migration expert. Generate migration scripts to evolve the database.

Current Schema:
{json.dumps(current_schema, indent=2)}

New Requirements:
{json.dumps(new_requirements, indent=2)}

Generate:
1. Up Migration: SQL to apply changes
2. Down Migration: SQL to rollback changes
3. Data Migration: Scripts to migrate existing data if needed
4. Impact Analysis: What will be affected
5. Risk Assessment: Potential issues and mitigation

Return as JSON:
{{
    "migrations": [
        {{
            "version": "001",
            "description": "Add user authentication tables",
            "up_sql": ["CREATE TABLE...", "ALTER TABLE..."],
            "down_sql": ["DROP TABLE...", "ALTER TABLE..."],
            "data_migration": ["INSERT INTO...", "UPDATE..."]
        }}
    ],
    "impact_analysis": {{
        "affected_tables": ["table1", "table2"],
        "breaking_changes": ["description of breaking changes"],
        "estimated_downtime": "minimal/moderate/high"
    }},
    "risks": [
        {{
            "risk": "description",
            "severity": "low/medium/high",
            "mitigation": "mitigation strategy"
        }}
    ]
}}
"""
        
        try:
            response = self.llm.generate(
                prompt=prompt,
                system_message="You are a database migration specialist.",
                max_tokens=2500
            )
            
            migrations = self._parse_migration_response(response)
            
            # Save migrations
            output_file = os.path.join(self.output_dir, 'database_migrations.json')
            with open(output_file, 'w') as f:
                json.dump(migrations, f, indent=2)
            
            print(f"   ✅ Generated {len(migrations.get('migrations', []))} migrations")
            print(f"   📄 Saved to: {output_file}")
            
            return migrations
            
        except Exception as e:
            print(f"   ⚠️  Error generating migrations: {e}")
            return {"migrations": [], "impact_analysis": {}, "risks": []}
    
    def optimize_queries(self, code_analysis: Dict) -> Dict:
        """
        Analyze queries and provide optimization recommendations
        
        Args:
            code_analysis: Code analysis with database queries
            
        Returns:
            Optimization recommendations and improved queries
        """
        print("\n⚡ Analyzing query performance...")
        
        queries = code_analysis.get('database_queries', [])
        
        if not queries:
            print("   ℹ️  No queries found to optimize")
            return {"optimizations": [], "recommendations": []}
        
        prompt = f"""
Analyze these database queries and provide optimization recommendations:

Queries:
{json.dumps(queries, indent=2)}

For each query, provide:
1. Performance Analysis: Identify potential bottlenecks
2. Optimized Query: Rewritten query with improvements
3. Index Recommendations: Indexes to add for better performance
4. Explain Plan: Expected execution plan insights
5. Best Practices: Query optimization tips

Return as JSON with optimizations array.
"""
        
        try:
            response = self.llm.generate(
                prompt=prompt,
                system_message="You are a database performance tuning expert.",
                max_tokens=2000
            )
            
            optimizations = self._parse_optimization_response(response)
            
            print(f"   ✅ Analyzed {len(queries)} queries")
            print(f"   💡 Generated {len(optimizations.get('optimizations', []))} recommendations")
            
            return optimizations
            
        except Exception as e:
            print(f"   ⚠️  Error optimizing queries: {e}")
            return {"optimizations": [], "recommendations": []}
    
    def create_indexes(self, schema: Dict, performance_requirements: Dict) -> List[str]:
        """
        Generate index creation scripts based on performance requirements
        
        Args:
            schema: Database schema
            performance_requirements: Performance requirements (query patterns, load)
            
        Returns:
            List of CREATE INDEX statements
        """
        print("\n📊 Generating index recommendations...")
        
        prompt = f"""
Based on the database schema and performance requirements, recommend indexes:

Schema:
{json.dumps(schema, indent=2)}

Performance Requirements:
{json.dumps(performance_requirements, indent=2)}

Provide CREATE INDEX statements with explanations for:
1. Foreign key columns
2. Frequently queried columns
3. Composite indexes for common query patterns
4. Unique indexes for business constraints
5. Covering indexes for performance-critical queries

Return as JSON array of index definitions.
"""
        
        try:
            response = self.llm.generate(
                prompt=prompt,
                system_message="You are a database indexing expert.",
                max_tokens=1500
            )
            
            indexes = self._parse_index_response(response)
            
            print(f"   ✅ Generated {len(indexes)} index recommendations")
            
            return indexes
            
        except Exception as e:
            print(f"   ⚠️  Error generating indexes: {e}")
            return []
    
    def review_data_model(self, architecture: Dict) -> Dict:
        """
        Review data model for best practices and potential issues
        
        Args:
            architecture: Architecture design including data model
            
        Returns:
            Review findings and recommendations
        """
        print("\n🔍 Reviewing data model...")
        
        prompt = f"""
Review this data model for best practices, normalization, and potential issues:

Architecture:
{json.dumps(architecture, indent=2)}

Review for:
1. Normalization: Is the model properly normalized?
2. Denormalization: Are there justified cases for denormalization?
3. Scalability: Will this scale with growth?
4. Performance: Are there performance concerns?
5. Maintainability: Is it easy to maintain and evolve?
6. Data Integrity: Are constraints properly defined?
7. Security: Are there security considerations?

Return findings as JSON with issues, recommendations, and approval status.
"""
        
        try:
            response = self.llm.generate(
                prompt=prompt,
                system_message="You are a data modeling expert and reviewer.",
                max_tokens=2000
            )
            
            review = self._parse_review_response(response)
            
            issues = review.get('issues', [])
            print(f"   ✅ Review complete: {len(issues)} issues found")
            
            return review
            
        except Exception as e:
            print(f"   ⚠️  Error reviewing data model: {e}")
            return {"issues": [], "recommendations": [], "approved": False}
    
    # Helper methods
    
    def _prepare_schema_context(self, requirements: Dict, architecture: Dict) -> str:
        """Prepare context for schema design"""
        context = []
        
        if requirements:
            context.append(f"Requirements: {json.dumps(requirements, indent=2)}")
        
        if architecture:
            tech_stack = architecture.get('technology_stack', {})
            if tech_stack:
                context.append(f"Technology Stack: {json.dumps(tech_stack, indent=2)}")
        
        return "\n\n".join(context)
    
    def _parse_schema_response(self, response: str) -> Dict:
        """Parse LLM response for schema design"""
        try:
            # Try to extract JSON from response
            start = response.find('{')
            end = response.rfind('}') + 1
            if start >= 0 and end > start:
                return json.loads(response[start:end])
        except:
            pass
        
        return self._get_default_schema()
    
    def _parse_migration_response(self, response: str) -> Dict:
        """Parse LLM response for migrations"""
        try:
            start = response.find('{')
            end = response.rfind('}') + 1
            if start >= 0 and end > start:
                return json.loads(response[start:end])
        except:
            pass
        
        return {"migrations": [], "impact_analysis": {}, "risks": []}
    
    def _parse_optimization_response(self, response: str) -> Dict:
        """Parse LLM response for query optimizations"""
        try:
            start = response.find('{')
            end = response.rfind('}') + 1
            if start >= 0 and end > start:
                return json.loads(response[start:end])
        except:
            pass
        
        return {"optimizations": [], "recommendations": []}
    
    def _parse_index_response(self, response: str) -> List[str]:
        """Parse LLM response for index recommendations"""
        try:
            start = response.find('[')
            end = response.rfind(']') + 1
            if start >= 0 and end > start:
                return json.loads(response[start:end])
        except:
            pass
        
        return []
    
    def _parse_review_response(self, response: str) -> Dict:
        """Parse LLM response for data model review"""
        try:
            start = response.find('{')
            end = response.rfind('}') + 1
            if start >= 0 and end > start:
                return json.loads(response[start:end])
        except:
            pass
        
        return {"issues": [], "recommendations": [], "approved": True}
    
    def _get_default_schema(self) -> Dict:
        """Default schema structure for fallback"""
        return {
            "tables": [
                {
                    "name": "users",
                    "columns": [
                        {"name": "id", "type": "INTEGER", "primary_key": True},
                        {"name": "email", "type": "VARCHAR(255)", "unique": True},
                        {"name": "created_at", "type": "TIMESTAMP"}
                    ]
                }
            ],
            "relationships": [],
            "recommendations": ["Review requirements and regenerate schema"]
        }


if __name__ == "__main__":
    # Demo usage
    print("DBA Agent Demo\n")
    
    dba = DBAAgent({"provider": "ollama", "model": "llama3.2"})
    
    # Design schema
    requirements = {
        "features": ["User authentication", "Product catalog", "Order management"],
        "entities": ["User", "Product", "Order", "OrderItem"]
    }
    
    schema = dba.design_schema(requirements)
    print(f"\n✅ Schema: {len(schema.get('tables', []))} tables")
    
    # Review data model
    review = dba.review_data_model({"data_model": schema})
    print(f"\n✅ Review: {len(review.get('issues', []))} issues found")
