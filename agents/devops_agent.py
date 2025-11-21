"""
DevOps Agent - CI/CD, Infrastructure, and Deployment automation

Responsibilities:
- CI/CD pipeline design and implementation
- Infrastructure as Code (IaC) generation
- Container and orchestration configuration
- Deployment strategy planning
- Monitoring and alerting setup
- Cloud platform integration (Azure, AWS, GCP)
"""

from typing import Dict, List, Optional, Any
import os
import json
from shared.llm_manager import LLMManager


class DevOpsAgent:
    """DevOps Engineer Agent for infrastructure and deployment automation"""
    
    def __init__(self, llm_config: Dict, output_dir: str = "output"):
        self.llm_config = llm_config
        self.llm = LLMManager()
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
        
        # Supported platforms
        self.platforms = ['azure', 'aws', 'gcp', 'kubernetes', 'docker']
        self.ci_cd_tools = ['github_actions', 'azure_devops', 'jenkins', 'gitlab_ci']
        
        print("🚀 DevOps Engineer Agent initialized")
    
    def design_cicd_pipeline(self, project_info: Dict) -> Dict:
        """
        Design CI/CD pipeline for the project
        
        Args:
            project_info: Project information including tech stack and requirements
            
        Returns:
            CI/CD pipeline configuration and workflow files
        """
        print("\n🔄 Designing CI/CD pipeline...")
        
        tech_stack = project_info.get('technology_stack', {})
        requirements = project_info.get('requirements', {})
        
        prompt = f"""
Design a comprehensive CI/CD pipeline for this project:

Technology Stack:
{json.dumps(tech_stack, indent=2)}

Requirements:
{json.dumps(requirements, indent=2)}

Design a pipeline that includes:

1. Build Stage:
   - Dependency installation
   - Compilation/transpilation
   - Asset optimization
   
2. Test Stage:
   - Unit tests
   - Integration tests
   - Code coverage
   - Security scanning
   
3. Quality Gates:
   - Code quality checks (linting, formatting)
   - Vulnerability scanning
   - Performance benchmarks
   
4. Deployment Stages:
   - Development environment
   - Staging environment
   - Production environment (with approval)
   
5. Post-Deployment:
   - Smoke tests
   - Health checks
   - Notifications

Return as JSON:
{{
    "pipeline_name": "CI/CD Pipeline",
    "trigger": {{
        "branches": ["main", "develop"],
        "events": ["push", "pull_request"]
    }},
    "stages": [
        {{
            "name": "build",
            "jobs": [
                {{
                    "name": "job_name",
                    "steps": ["step1", "step2"],
                    "depends_on": []
                }}
            ]
        }}
    ],
    "environments": [
        {{
            "name": "production",
            "approval_required": true,
            "variables": ["VAR1", "VAR2"]
        }}
    ],
    "notifications": {{
        "on_success": ["email", "slack"],
        "on_failure": ["email", "slack", "pagerduty"]
    }}
}}
"""
        
        system_message = """You are a senior DevOps engineer with expertise in:
- CI/CD pipeline design and optimization
- GitHub Actions, Azure DevOps, Jenkins
- Docker and containerization
- Kubernetes orchestration
- Infrastructure as Code (Terraform, ARM, CloudFormation)
- Monitoring and observability
- Security and compliance automation"""
        
        try:
            response = self.llm.generate(
                prompt=prompt,
                system_message=system_message,
                max_tokens=3000,
                temperature=0.3
            )
            
            pipeline = self._parse_pipeline_response(response)
            
            # Save pipeline design
            output_file = os.path.join(self.output_dir, 'cicd_pipeline.json')
            with open(output_file, 'w') as f:
                json.dump(pipeline, f, indent=2)
            
            print(f"   ✅ Pipeline designed with {len(pipeline.get('stages', []))} stages")
            print(f"   📄 Saved to: {output_file}")
            
            return pipeline
            
        except Exception as e:
            print(f"   ⚠️  Error designing pipeline: {e}")
            return self._get_default_pipeline()
    
    def generate_dockerfile(self, tech_stack: Dict) -> str:
        """
        Generate optimized Dockerfile for the project
        
        Args:
            tech_stack: Technology stack information
            
        Returns:
            Dockerfile content
        """
        print("\n🐳 Generating Dockerfile...")
        
        language = tech_stack.get('language', 'python')
        framework = tech_stack.get('framework', '')
        
        prompt = f"""
Generate an optimized production-ready Dockerfile for:

Language: {language}
Framework: {framework}
Tech Stack: {json.dumps(tech_stack, indent=2)}

Requirements:
1. Use multi-stage builds for smaller image size
2. Implement proper caching strategies
3. Run as non-root user for security
4. Include health checks
5. Optimize layer ordering
6. Use specific version tags (no 'latest')
7. Include security best practices
8. Add labels for metadata

Return the complete Dockerfile content.
"""
        
        try:
            response = self.llm.generate(
                prompt=prompt,
                system_message="You are a Docker and containerization expert.",
                max_tokens=1500
            )
            
            dockerfile = self._extract_dockerfile(response)
            
            # Save Dockerfile
            output_file = os.path.join(self.output_dir, 'Dockerfile')
            with open(output_file, 'w') as f:
                f.write(dockerfile)
            
            print(f"   ✅ Dockerfile generated")
            print(f"   📄 Saved to: {output_file}")
            
            return dockerfile
            
        except Exception as e:
            print(f"   ⚠️  Error generating Dockerfile: {e}")
            return self._get_default_dockerfile(language)
    
    def create_kubernetes_manifests(self, architecture: Dict) -> Dict[str, str]:
        """
        Generate Kubernetes manifests for the application
        
        Args:
            architecture: Application architecture and requirements
            
        Returns:
            Dictionary of manifest files (deployment, service, ingress, etc.)
        """
        print("\n☸️  Generating Kubernetes manifests...")
        
        prompt = f"""
Generate Kubernetes manifests for this application:

Architecture:
{json.dumps(architecture, indent=2)}

Generate YAML manifests for:
1. Deployment - with proper resource limits, health checks, rolling updates
2. Service - to expose the application
3. ConfigMap - for configuration
4. Secret - for sensitive data (template)
5. Ingress - for external access
6. HorizontalPodAutoscaler - for auto-scaling
7. NetworkPolicy - for security

Return as JSON with file names and content:
{{
    "deployment.yaml": "yaml content",
    "service.yaml": "yaml content",
    ...
}}
"""
        
        try:
            response = self.llm.generate(
                prompt=prompt,
                system_message="You are a Kubernetes expert.",
                max_tokens=3500
            )
            
            manifests = self._parse_k8s_response(response)
            
            # Save manifests
            k8s_dir = os.path.join(self.output_dir, 'kubernetes')
            os.makedirs(k8s_dir, exist_ok=True)
            
            for filename, content in manifests.items():
                filepath = os.path.join(k8s_dir, filename)
                with open(filepath, 'w') as f:
                    f.write(content)
            
            print(f"   ✅ Generated {len(manifests)} Kubernetes manifests")
            print(f"   📁 Saved to: {k8s_dir}/")
            
            return manifests
            
        except Exception as e:
            print(f"   ⚠️  Error generating manifests: {e}")
            return {}
    
    def setup_monitoring(self, application_requirements: Dict) -> Dict:
        """
        Set up monitoring and alerting configuration
        
        Args:
            application_requirements: Application requirements and SLAs
            
        Returns:
            Monitoring configuration and alert rules
        """
        print("\n📊 Setting up monitoring and alerts...")
        
        prompt = f"""
Design monitoring and alerting setup for:

Requirements:
{json.dumps(application_requirements, indent=2)}

Provide configuration for:
1. Application Metrics:
   - Request rate, latency, error rate
   - Resource usage (CPU, memory, disk)
   - Custom business metrics
   
2. Infrastructure Metrics:
   - Server health
   - Database performance
   - Cache hit rates
   
3. Alert Rules:
   - Error rate thresholds
   - Latency SLA violations
   - Resource saturation
   - Availability checks
   
4. Dashboards:
   - Overview dashboard
   - Application performance
   - Infrastructure health
   
5. Tools:
   - Prometheus/Grafana configuration
   - Azure Monitor / CloudWatch
   - Log aggregation (ELK stack)

Return as JSON configuration.
"""
        
        try:
            response = self.llm.generate(
                prompt=prompt,
                system_message="You are a monitoring and observability expert.",
                max_tokens=2500
            )
            
            monitoring = self._parse_monitoring_response(response)
            
            # Save monitoring config
            output_file = os.path.join(self.output_dir, 'monitoring_config.json')
            with open(output_file, 'w') as f:
                json.dump(monitoring, f, indent=2)
            
            print(f"   ✅ Monitoring configured with {len(monitoring.get('alerts', []))} alert rules")
            print(f"   📄 Saved to: {output_file}")
            
            return monitoring
            
        except Exception as e:
            print(f"   ⚠️  Error setting up monitoring: {e}")
            return {"metrics": [], "alerts": [], "dashboards": []}
    
    def generate_github_actions_workflow(self, pipeline_design: Dict) -> str:
        """
        Generate GitHub Actions workflow file from pipeline design
        
        Args:
            pipeline_design: Pipeline design configuration
            
        Returns:
            GitHub Actions workflow YAML content
        """
        print("\n⚙️  Generating GitHub Actions workflow...")
        
        prompt = f"""
Convert this pipeline design into a GitHub Actions workflow:

Pipeline Design:
{json.dumps(pipeline_design, indent=2)}

Generate a complete .github/workflows/ci-cd.yml file with:
1. Proper triggers (push, pull_request)
2. Build and test jobs
3. Matrix strategy for multiple versions if needed
4. Caching for dependencies
5. Artifact uploads
6. Deployment jobs with environment protection
7. Secrets and environment variables
8. Proper error handling

Return the complete YAML workflow file.
"""
        
        try:
            response = self.llm.generate(
                prompt=prompt,
                system_message="You are a GitHub Actions expert.",
                max_tokens=2500
            )
            
            workflow = self._extract_yaml(response)
            
            # Save workflow
            workflow_dir = os.path.join(self.output_dir, '.github', 'workflows')
            os.makedirs(workflow_dir, exist_ok=True)
            
            workflow_file = os.path.join(workflow_dir, 'ci-cd.yml')
            with open(workflow_file, 'w') as f:
                f.write(workflow)
            
            print(f"   ✅ GitHub Actions workflow generated")
            print(f"   📄 Saved to: {workflow_file}")
            
            return workflow
            
        except Exception as e:
            print(f"   ⚠️  Error generating workflow: {e}")
            return self._get_default_github_workflow()
    
    def generate_terraform_config(self, infrastructure: Dict) -> Dict[str, str]:
        """
        Generate Terraform/IaC configuration
        
        Args:
            infrastructure: Infrastructure requirements
            
        Returns:
            Dictionary of Terraform files
        """
        print("\n🏗️  Generating Infrastructure as Code...")
        
        prompt = f"""
Generate Terraform configuration for:

Infrastructure:
{json.dumps(infrastructure, indent=2)}

Generate:
1. main.tf - Main infrastructure resources
2. variables.tf - Input variables
3. outputs.tf - Output values
4. providers.tf - Provider configuration
5. terraform.tfvars.example - Example variables

Include resources for:
- Compute resources
- Networking (VPC, subnets, security groups)
- Database instances
- Storage
- Load balancers
- Monitoring

Return as JSON with file names and content.
"""
        
        try:
            response = self.llm.generate(
                prompt=prompt,
                system_message="You are a Terraform and IaC expert.",
                max_tokens=3000
            )
            
            terraform_files = self._parse_terraform_response(response)
            
            # Save Terraform files
            terraform_dir = os.path.join(self.output_dir, 'terraform')
            os.makedirs(terraform_dir, exist_ok=True)
            
            for filename, content in terraform_files.items():
                filepath = os.path.join(terraform_dir, filename)
                with open(filepath, 'w') as f:
                    f.write(content)
            
            print(f"   ✅ Generated {len(terraform_files)} Terraform files")
            print(f"   📁 Saved to: {terraform_dir}/")
            
            return terraform_files
            
        except Exception as e:
            print(f"   ⚠️  Error generating Terraform: {e}")
            return {}
    
    # Helper methods
    
    def _parse_pipeline_response(self, response: str) -> Dict:
        """Parse LLM response for pipeline design"""
        try:
            start = response.find('{')
            end = response.rfind('}') + 1
            if start >= 0 and end > start:
                return json.loads(response[start:end])
        except:
            pass
        
        return self._get_default_pipeline()
    
    def _parse_k8s_response(self, response: str) -> Dict[str, str]:
        """Parse LLM response for Kubernetes manifests"""
        try:
            start = response.find('{')
            end = response.rfind('}') + 1
            if start >= 0 and end > start:
                return json.loads(response[start:end])
        except:
            pass
        
        return {
            "deployment.yaml": "# Kubernetes deployment manifest\n# Generate manually",
            "service.yaml": "# Kubernetes service manifest\n# Generate manually"
        }
    
    def _parse_monitoring_response(self, response: str) -> Dict:
        """Parse LLM response for monitoring config"""
        try:
            start = response.find('{')
            end = response.rfind('}') + 1
            if start >= 0 and end > start:
                return json.loads(response[start:end])
        except:
            pass
        
        return {"metrics": [], "alerts": [], "dashboards": []}
    
    def _parse_terraform_response(self, response: str) -> Dict[str, str]:
        """Parse LLM response for Terraform files"""
        try:
            start = response.find('{')
            end = response.rfind('}') + 1
            if start >= 0 and end > start:
                return json.loads(response[start:end])
        except:
            pass
        
        return {}
    
    def _extract_dockerfile(self, response: str) -> str:
        """Extract Dockerfile content from response"""
        # Look for Dockerfile content markers
        lines = response.split('\n')
        dockerfile_lines = []
        in_dockerfile = False
        
        for line in lines:
            if 'FROM' in line and not in_dockerfile:
                in_dockerfile = True
            if in_dockerfile:
                dockerfile_lines.append(line)
        
        if dockerfile_lines:
            return '\n'.join(dockerfile_lines)
        
        return response
    
    def _extract_yaml(self, response: str) -> str:
        """Extract YAML content from response"""
        # Look for YAML content
        lines = response.split('\n')
        yaml_lines = []
        in_yaml = False
        
        for line in lines:
            if line.strip().startswith('name:') and not in_yaml:
                in_yaml = True
            if in_yaml:
                yaml_lines.append(line)
        
        if yaml_lines:
            return '\n'.join(yaml_lines)
        
        return response
    
    def _get_default_pipeline(self) -> Dict:
        """Default pipeline structure"""
        return {
            "pipeline_name": "CI/CD Pipeline",
            "stages": [
                {"name": "build", "jobs": []},
                {"name": "test", "jobs": []},
                {"name": "deploy", "jobs": []}
            ],
            "environments": []
        }
    
    def _get_default_dockerfile(self, language: str) -> str:
        """Default Dockerfile template"""
        if language.lower() == 'python':
            return """FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 8000
CMD ["python", "app.py"]
"""
        return "FROM alpine:latest\nCMD [\"echo\", \"Configure Dockerfile\"]"
    
    def _get_default_github_workflow(self) -> str:
        """Default GitHub Actions workflow"""
        return """name: CI/CD Pipeline
on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Build
        run: echo "Configure build steps"
"""


if __name__ == "__main__":
    # Demo usage
    print("DevOps Agent Demo\n")
    
    devops = DevOpsAgent({"provider": "ollama", "model": "llama3.2"})
    
    # Design CI/CD pipeline
    project_info = {
        "technology_stack": {
            "language": "python",
            "framework": "fastapi",
            "database": "postgresql"
        },
        "requirements": {
            "environments": ["dev", "staging", "prod"],
            "testing": ["unit", "integration"]
        }
    }
    
    pipeline = devops.design_cicd_pipeline(project_info)
    print(f"\n✅ Pipeline: {len(pipeline.get('stages', []))} stages")
    
    # Generate Dockerfile
    dockerfile = devops.generate_dockerfile(project_info['technology_stack'])
    print(f"\n✅ Dockerfile: {len(dockerfile.split(chr(10)))} lines")
