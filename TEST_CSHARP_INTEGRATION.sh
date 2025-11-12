#!/bin/bash
# Test C# Security Scanning Integration
# This script demonstrates the C# static analysis capabilities

echo "=================================================="
echo "🔷 C# Security Scanning Integration Test"
echo "=================================================="
echo ""

# Test 1: Check if C# rules exist
echo "✓ Step 1: Checking C# security rules..."
if [ -f ".semgrep/csharp-rules.yaml" ]; then
    echo "  ✅ C# Semgrep rules found"
    rule_count=$(grep -c "^  - id:" .semgrep/csharp-rules.yaml)
    echo "     → $rule_count security rules loaded"
else
    echo "  ❌ C# rules not found!"
    exit 1
fi
echo ""

# Test 2: Check workflow configuration
echo "✓ Step 2: Checking workflow configuration..."
if grep -q "csharp-rules.yaml" .github/workflows/secure-deploy.yml; then
    echo "  ✅ Workflow configured for C# scanning"
else
    echo "  ❌ Workflow not configured!"
    exit 1
fi
echo ""

# Test 3: Check test samples
echo "✓ Step 3: Checking test samples..."
if [ -d "tests/csharp-samples" ]; then
    echo "  ✅ C# test samples found"
    sample_count=$(ls -1 tests/csharp-samples/*.cs 2>/dev/null | wc -l)
    echo "     → $sample_count test files available"
else
    echo "  ❌ Test samples not found!"
    exit 1
fi
echo ""

# Test 4: Check documentation
echo "✓ Step 4: Checking documentation..."
if [ -f "docs/CSHARP_INTEGRATION.md" ]; then
    echo "  ✅ C# integration guide exists"
fi
if [ -f "docs/CSHARP_QUICK_START.md" ]; then
    echo "  ✅ Quick start guide exists"
fi
echo ""

echo "=================================================="
echo "✅ C# Integration Setup: COMPLETE"
echo "=================================================="
echo ""
echo "📚 Next Steps:"
echo ""
echo "1. Quick test (triggers AI Guardrail blocking):"
echo "   $ cp tests/csharp-samples/VulnerableController.cs ."
echo "   $ git add VulnerableController.cs"
echo "   $ git commit -m 'test: C# security scan'"
echo "   $ git push"
echo ""
echo "2. View results:"
echo "   → GitHub Actions: Check workflow logs"
echo "   → Website: See live scan results"
echo ""
echo "3. Clean up:"
echo "   $ git rm VulnerableController.cs"
echo "   $ git commit -m 'clean: Remove test file'"
echo "   $ git push"
echo ""
echo "📖 Documentation:"
echo "   → Quick Start: docs/CSHARP_QUICK_START.md"
echo "   → Full Guide:  docs/CSHARP_INTEGRATION.md"
echo "   → Test Samples: tests/csharp-samples/README.md"
echo ""
echo "🎯 What Gets Scanned:"
echo "   ✓ SQL Injection"
echo "   ✓ Command Injection"
echo "   ✓ Hardcoded Secrets"
echo "   ✓ XSS Vulnerabilities"
echo "   ✓ Weak Cryptography"
echo "   ✓ Unsafe Deserialization"
echo "   ✓ Path Traversal"
echo "   ✓ CSRF Protection"
echo "   ✓ SSL Bypass"
echo ""
echo "🤖 AI Guardrail:"
echo "   → Analyzes all findings with GPT-4o-mini"
echo "   → Makes intelligent deployment decisions"
echo "   → Blocks critical vulnerabilities"
echo "   → Provides detailed remediation steps"
echo ""
echo "=================================================="

