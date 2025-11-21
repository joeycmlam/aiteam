#!/bin/bash
# Quick Test Script for Agent Framework

echo "=========================================="
echo "🧪 Agent Framework Quick Test"
echo "=========================================="
echo ""

# Set working directory
cd /Users/joeylam/repo/aiteam

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}Test 1: BA Agent${NC}"
echo "------------------------------------------"
python3 agents/enhanced_ba_agent.py \
  --input /Users/joeylam/repo/pps/requirements/user_01.md \
  --output-dir /tmp/framework_test/requirements

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ BA Agent test passed${NC}"
else
    echo "❌ BA Agent test failed"
    exit 1
fi

echo ""
echo -e "${BLUE}Test 2: Tech Lead Agent${NC}"
echo "------------------------------------------"
python3 agents/enhanced_tech_lead_agent.py \
  --ba-analysis /tmp/framework_test/requirements/requirements_analysis.md \
  --output-dir /tmp/framework_test/technical

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ Tech Lead Agent test passed${NC}"
else
    echo "❌ Tech Lead Agent test failed"
    exit 1
fi

echo ""
echo -e "${BLUE}Test 3: Developer Agent${NC}"
echo "------------------------------------------"
python3 agents/enhanced_developer_agent.py \
  --technical-structure /tmp/framework_test/technical/technical_structure.md \
  --output-dir /tmp/framework_test/implementation

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ Developer Agent test passed${NC}"
else
    echo "❌ Developer Agent test failed"
    exit 1
fi

echo ""
echo "=========================================="
echo "✅ All agent tests passed!"
echo "=========================================="
echo ""
echo "📁 Test outputs saved to: /tmp/framework_test"
echo ""
echo "To view outputs:"
echo "  ls -R /tmp/framework_test"
echo ""
echo "To test complete workflow:"
echo "  python3 workflows/complete_workflow.py \\"
echo "    --requirements /Users/joeylam/repo/pps/requirements/user_01.md \\"
echo "    --output /tmp/complete_workflow_test"
