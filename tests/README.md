# Test Scenarios for SecureDeploy Guardrail

This directory contains test files to demonstrate different security scanning scenarios.

## ⚠️ IMPORTANT

**These files contain intentional security issues for testing purposes.**
- DO NOT remove the `.example` extension and commit in a production environment
- DO NOT use these patterns in real code
- These are for demonstration and testing only

## Test Files

### 1. Secret Detection Test
**File:** `test-secret.example`

Contains fake credentials to test Gitleaks:
- AWS access keys
- OpenAI API keys
- GitHub tokens
- Generic API keys

**Expected Result:** Gitleaks detects all secrets, AI blocks deployment with CRITICAL risk.

### 2. Code Security Test
**File:** `test-insecure-code.example.js`

Contains JavaScript security issues to test Semgrep:
- `eval()` usage (code injection)
- `innerHTML` usage (XSS)
- Insecure random generation
- `document.write()` usage
- Hardcoded passwords

**Expected Result:** Semgrep detects multiple issues, AI evaluates severity and may block or warn.

### 3. Policy Violation Test
**File:** `test-policy-violation.example.tf`

Contains Terraform misconfigurations to test OPA/Conftest:
- S3 bucket without encryption
- Public read/write access
- Missing versioning
- Missing logging
- CloudFront without HTTPS enforcement

**Expected Result:** OPA detects policy violations, AI blocks deployment with HIGH risk.

## How to Run Tests

### Test 1: Clean Deployment (Baseline)

```bash
# No changes needed - current codebase should be clean
git add .
git commit -m "Test: Clean deployment"
git push origin main
```

**Expected:** All scans pass, AI approves deployment.

### Test 2: Secret Detection

```bash
# Activate the secret test file
cp tests/test-secret.example test-secret.txt
git add test-secret.txt
git commit -m "Test: Add secrets"
git push origin main
```

**Expected:** Gitleaks catches secrets, AI blocks deployment.

**Cleanup:**
```bash
git rm test-secret.txt
git commit -m "Test: Remove secrets"
git push origin main
```

### Test 3: Code Security Issue

```bash
# Activate the insecure code test
cp tests/test-insecure-code.example.js website/insecure.js
git add website/insecure.js
git commit -m "Test: Add insecure code"
git push origin main
```

**Expected:** Semgrep detects issues, AI evaluates and likely blocks.

**Cleanup:**
```bash
git rm website/insecure.js
git commit -m "Test: Remove insecure code"
git push origin main
```

### Test 4: Policy Violation

```bash
# Activate the policy violation test
cp tests/test-policy-violation.example.tf infrastructure/test-violation.tf
git add infrastructure/test-violation.tf
git commit -m "Test: Add policy violations"
git push origin main
```

**Expected:** OPA detects violations, AI blocks deployment.

**Cleanup:**
```bash
git rm infrastructure/test-violation.tf
git commit -m "Test: Remove policy violations"
git push origin main
```

### Test 5: Multiple Issues

```bash
# Activate all test files at once
cp tests/test-secret.example test-secret.txt
cp tests/test-insecure-code.example.js website/insecure.js
cp tests/test-policy-violation.example.tf infrastructure/test-violation.tf

git add test-secret.txt website/insecure.js infrastructure/test-violation.tf
git commit -m "Test: Multiple security issues"
git push origin main
```

**Expected:** All tools detect issues, AI analyzes comprehensively and blocks with detailed report.

**Cleanup:**
```bash
git rm test-secret.txt website/insecure.js infrastructure/test-violation.tf
git commit -m "Test: Cleanup all issues"
git push origin main
```

## Automated Test Suite

For CI/CD testing, you can create a script:

```bash
#!/bin/bash
# run-tests.sh

echo "Running SecureDeploy Guardrail Tests..."

# Test 1: Clean deployment
echo "Test 1: Clean deployment"
git commit --allow-empty -m "Test: Clean deployment"
git push origin main
sleep 180  # Wait for workflow to complete

# Test 2: Secret detection
echo "Test 2: Secret detection"
cp tests/test-secret.example test-secret.txt
git add test-secret.txt
git commit -m "Test: Secret detection"
git push origin main
sleep 180

# Cleanup
git rm test-secret.txt
git commit -m "Cleanup: Remove test file"
git push origin main

# Add more tests as needed...
```

## Verification Checklist

After each test, verify:

- [ ] GitHub Actions workflow triggered
- [ ] Security scan job completed
- [ ] Appropriate tool detected the issue
- [ ] AI Guardrail analyzed correctly
- [ ] Deployment decision matches expected
- [ ] Report contains specific findings
- [ ] Recommendations are actionable

## Expected Metrics

| Test Scenario | Gitleaks | Semgrep | OPA | AI Decision | Risk Level |
|---------------|----------|---------|-----|-------------|------------|
| Clean Deployment | 0 | 0 | 0 | SAFE | NONE/LOW |
| Secret Detection | 4+ | 0 | 0 | BLOCK | CRITICAL |
| Code Security | 0 | 5+ | 0 | BLOCK/WARN | HIGH/MEDIUM |
| Policy Violation | 0 | 0 | 4+ | BLOCK | HIGH |
| Multiple Issues | 4+ | 5+ | 4+ | BLOCK | CRITICAL |

## Notes

- Test execution time: ~2-3 minutes per test
- Always cleanup test files after testing
- Monitor OpenAI API usage during tests
- Review GitHub Actions logs for details
- Check AWS costs remain in free tier

## Troubleshooting

**Issue:** Tests not triggering workflow
- **Solution:** Ensure `.github/workflows/secure-deploy.yml` exists and is valid

**Issue:** Tools not detecting issues
- **Solution:** Verify configuration files are present and correct

**Issue:** AI not analyzing correctly
- **Solution:** Check `OPENAI_API_KEY` secret is set and valid

**Issue:** Cleanup not working
- **Solution:** Use `git rm -f` to force removal

---

**Remember:** These tests are for demonstration only. Never commit real secrets or insecure code!

