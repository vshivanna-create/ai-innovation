# Demo Script - SecureDeploy Guardrail

Step-by-step demo scenarios to showcase the AI-powered security guardrail in action.

## Table of Contents
1. [Demo Setup](#demo-setup)
2. [Scenario 1: Clean Deployment](#scenario-1-clean-deployment-✅)
3. [Scenario 2: Secret Detection](#scenario-2-secret-detection-❌)
4. [Scenario 3: Code Security Issue](#scenario-3-code-security-issue-⚠️)
5. [Scenario 4: Policy Violation](#scenario-4-policy-violation-❌)
6. [Scenario 5: Multiple Issues](#scenario-5-multiple-issues-❌)
7. [Presentation Tips](#presentation-tips)

---

## Demo Setup

### Prerequisites
- ✅ GitHub repository set up
- ✅ AWS infrastructure deployed
- ✅ All secrets configured
- ✅ Initial deployment successful

### Demo Environment Check

```bash
# Verify GitHub Actions workflow exists
ls .github/workflows/secure-deploy.yml

# Verify all security configs
ls .gitleaks.toml .semgrep/rules.yaml policies/deployment.rego

# Verify infrastructure
cd infrastructure && terraform output

# Check website is live
curl -I $(terraform output -raw website_url)
```

---

## Scenario 1: Clean Deployment ✅

**Objective:** Show a successful deployment with AI approval

### Steps

1. **Make a clean code change**
   ```bash
   # Update website content
   sed -i 's/AI-Powered Security/AI-Powered Security v2.0/' website/index.html
   ```

2. **Commit and push**
   ```bash
   git add website/index.html
   git commit -m "Update website title"
   git push origin main
   ```

3. **Monitor GitHub Actions**
   - Go to Actions tab
   - Click on the running workflow
   - Watch each job execute

4. **Expected Results**
   ```
   ✅ Security Scan
      - Gitleaks: 0 findings
      - Semgrep: 0 findings
      - OPA: All policies passing

   ✅ AI Guardrail
      - Decision: SAFE_TO_DEPLOY
      - Risk Level: NONE or LOW
      - Reasoning: "No security issues detected"

   ✅ Deploy
      - Website updated on S3
      - CloudFront cache invalidated
      - Success notification posted
   ```

5. **Verify deployment**
   ```bash
   curl $(cd infrastructure && terraform output -raw website_url) | grep "v2.0"
   ```

### Demo Talking Points
- "Notice how all three security tools run in parallel"
- "The AI analyzes the results and provides reasoning"
- "Deployment happens automatically when approved"
- "Total time: ~2-3 minutes from push to live"

---

## Scenario 2: Secret Detection ❌

**Objective:** Demonstrate blocking deployment when secrets are detected

### Steps

1. **Introduce a hardcoded secret**
   ```bash
   # Create a file with AWS credentials
   cat > test-config.js << 'EOF'
   // Configuration file
   const config = {
     aws_access_key: "AKIAIOSFODNN7EXAMPLE",
     aws_secret_key: "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY",
     region: "us-west-2"
   };

   export default config;
   EOF
   ```

2. **Commit and push**
   ```bash
   git add test-config.js
   git commit -m "Add configuration file"
   git push origin main
   ```

3. **Watch GitHub Actions**
   - Security scan detects credentials
   - Gitleaks marks as CRITICAL
   - AI Guardrail analyzes

4. **Expected Results**
   ```
   ✅ Security Scan (completes with findings)
      - Gitleaks: 2 findings (AWS credentials)
      - Severity: CRITICAL

   ❌ AI Guardrail
      - Decision: BLOCK_DEPLOYMENT
      - Risk Level: CRITICAL
      - Reasoning: "Hardcoded AWS credentials detected.
                    These must be removed immediately as they
                    pose a direct security risk."
      - Recommendations:
        * Remove hardcoded credentials from test-config.js
        * Use environment variables or AWS Secrets Manager
        * Rotate compromised credentials if already committed

   ⏭️  Deploy (skipped)
      - Conditional job not executed
   ```

5. **View detailed report**
   - Check Actions → Workflow run → Summary
   - See full AI analysis
   - Note specific file and line numbers

### Demo Talking Points
- "Gitleaks immediately caught the hardcoded credentials"
- "AI understood this is CRITICAL and must block"
- "Notice the specific, actionable recommendations"
- "Deployment was automatically blocked"

### Cleanup
```bash
git rm test-config.js
git commit -m "Remove test configuration file"
git push origin main
```

---

## Scenario 3: Code Security Issue ⚠️

**Objective:** Show AI handling medium-severity issues

### Steps

1. **Add code with security warning**
   ```bash
   # Create JavaScript with potential XSS
   cat > website/form-handler.js << 'EOF'
   function displayMessage(message) {
     // Potentially unsafe - using innerHTML
     document.getElementById('output').innerHTML = message;
   }

   function handleSubmit(event) {
     event.preventDefault();
     const userInput = document.getElementById('input').value;
     displayMessage(userInput);
   }
   EOF
   ```

2. **Commit and push**
   ```bash
   git add website/form-handler.js
   git commit -m "Add form handler"
   git push origin main
   ```

3. **Expected Results**
   ```
   ✅ Security Scan
      - Semgrep: 1 finding
      - Type: innerHTML usage (XSS risk)
      - Severity: WARNING (medium)

   ⚠️ AI Guardrail
      - Decision: SAFE_TO_DEPLOY (with warnings)
      - Risk Level: MEDIUM
      - Reasoning: "Found potential XSS vulnerability using innerHTML.
                    While this should be fixed, it's in a new file
                    and doesn't affect existing functionality.
                    Deployment approved with recommendation to fix."
      - Recommendations:
        * Replace innerHTML with textContent
        * Or use DOMPurify for sanitization
        * Add input validation

   ✅ Deploy (proceeds with warnings)
   ```

### Demo Talking Points
- "AI understands context - this is new code, not breaking existing features"
- "Makes intelligent decision: approve with warnings"
- "Provides specific fix recommendations"
- "Balance between security and velocity"

### Cleanup
```bash
# Fix the security issue
cat > website/form-handler.js << 'EOF'
function displayMessage(message) {
  // Safe - using textContent
  document.getElementById('output').textContent = message;
}

function handleSubmit(event) {
  event.preventDefault();
  const userInput = document.getElementById('input').value;
  displayMessage(userInput);
}
EOF

git add website/form-handler.js
git commit -m "Fix XSS vulnerability"
git push origin main
```

---

## Scenario 4: Policy Violation ❌

**Objective:** Demonstrate infrastructure policy enforcement

### Steps

1. **Modify Terraform to violate policy**
   ```bash
   # Create a non-compliant S3 bucket configuration
   cat > infrastructure/test-bucket.tf << 'EOF'
   resource "aws_s3_bucket" "test" {
     bucket = "test-bucket-insecure"
   }

   # Note: No encryption, no versioning, no logging
   EOF
   ```

2. **Commit and push**
   ```bash
   git add infrastructure/test-bucket.tf
   git commit -m "Add test bucket"
   git push origin main
   ```

3. **Expected Results**
   ```
   ✅ Security Scan
      - OPA/Conftest: 3 violations
        * S3 bucket encryption not enabled
        * S3 bucket versioning not enabled
        * S3 bucket logging not enabled

   ❌ AI Guardrail
      - Decision: BLOCK_DEPLOYMENT
      - Risk Level: HIGH
      - Reasoning: "Infrastructure configuration violates security
                    policies. S3 bucket lacks encryption, versioning,
                    and logging - all required for compliance."
      - Recommendations:
        * Add server_side_encryption_configuration
        * Enable versioning for data protection
        * Configure access logging
        * Review S3 security best practices

   ⏭️  Deploy (blocked)
   ```

### Demo Talking Points
- "OPA enforces infrastructure policies as code"
- "AI interprets policy violations in security context"
- "Compliance requirements are automatically checked"
- "Prevents insecure infrastructure from being deployed"

### Cleanup
```bash
git rm infrastructure/test-bucket.tf
git commit -m "Remove non-compliant bucket"
git push origin main
```

---

## Scenario 5: Multiple Issues ❌

**Objective:** Show AI handling complex scenarios with multiple findings

### Steps

1. **Introduce multiple issues at once**
   ```bash
   # Secret in code
   echo 'const API_KEY = "sk-proj-abc123example";' > website/api.js

   # Insecure code
   echo 'function exec(cmd) { eval(cmd); }' >> website/api.js

   # Policy violation
   cat > infrastructure/bad-config.tf << 'EOF'
   resource "aws_s3_bucket" "public" {
     bucket = "totally-public-bucket"
   }

   resource "aws_s3_bucket_acl" "public" {
     bucket = aws_s3_bucket.public.id
     acl    = "public-read-write"
   }
   EOF

   git add website/api.js infrastructure/bad-config.tf
   git commit -m "Multiple changes"
   git push origin main
   ```

2. **Expected Results**
   ```
   ✅ Security Scan (multiple tools triggered)
      - Gitleaks: 1 critical (API key)
      - Semgrep: 1 high (eval usage)
      - OPA: 2 violations (public bucket, no encryption)

   ❌ AI Guardrail
      - Decision: BLOCK_DEPLOYMENT
      - Risk Level: CRITICAL
      - Reasoning: "Multiple severe security issues detected:
        1. Hardcoded API key in source code
        2. Dangerous eval() function usage
        3. S3 bucket configured for public write access

        This combination presents immediate security risks
        including credential exposure, code injection, and
        data breach vulnerabilities. All issues must be
        resolved before deployment."

      - Recommendations:
        * Remove API key from website/api.js
        * Replace eval() with safe alternatives
        * Remove public-read-write ACL from S3 bucket
        * Add encryption and access controls
        * Review security training for best practices

   ⏭️  Deploy (blocked)
   ```

### Demo Talking Points
- "AI can handle multiple security issues across different tools"
- "Provides holistic analysis, not just individual findings"
- "Prioritizes issues by risk level"
- "Gives comprehensive remediation plan"

### Cleanup
```bash
git rm website/api.js infrastructure/bad-config.tf
git commit -m "Remove all insecure code"
git push origin main
```

---

## Presentation Tips

### Pre-Demo Checklist
- [ ] All secrets configured in GitHub
- [ ] AWS infrastructure deployed and verified
- [ ] Clean initial state (no pending issues)
- [ ] Browser tabs prepared:
  - GitHub repository
  - GitHub Actions
  - AWS S3 Console
  - Website URL
- [ ] Terminal ready with repository cloned

### Demo Flow Recommendations

**5-Minute Demo:**
1. Show clean deployment (Scenario 1) - 2 min
2. Demonstrate secret blocking (Scenario 2) - 2 min
3. Show website live - 1 min

**10-Minute Demo:**
1. Clean deployment (Scenario 1) - 2 min
2. Secret detection (Scenario 2) - 3 min
3. Code security (Scenario 3) - 3 min
4. Show architecture diagram - 2 min

**15-Minute Demo:**
1. System overview - 2 min
2. All 5 scenarios - 10 min
3. Q&A and architecture - 3 min

### Key Messages to Emphasize

1. **Automation**
   - "Zero manual intervention required"
   - "Runs on every commit automatically"

2. **Intelligence**
   - "AI understands context, not just rules"
   - "Provides reasoning, not just pass/fail"

3. **Speed**
   - "Complete analysis in under 3 minutes"
   - "Faster than manual security review"

4. **Cost**
   - "Essentially free using AWS and OpenAI free tiers"
   - "Under $0.03 for 100 deployments"

5. **Comprehensive**
   - "Three security tools in one pipeline"
   - "Covers secrets, code, and infrastructure"

### Common Questions & Answers

**Q: What if OpenAI API is down?**
A: We have a fallback rule-based system that still blocks critical issues.

**Q: Can this work with other cloud providers?**
A: Yes! The security scanning is cloud-agnostic. Only deployment step needs adjustment.

**Q: How do you prevent false positives?**
A: The AI understands context and can distinguish between test code, examples, and real issues.

**Q: What about performance at scale?**
A: Currently ~3 minutes per deployment. Can optimize with caching and incremental scans.

**Q: Can it integrate with Slack/Teams?**
A: Yes! GitHub Actions can post to any webhook. Just add notification step.

---

## Metrics to Track

During demo, highlight these metrics:

| Metric | Value |
|--------|-------|
| Time to deploy (clean) | ~2-3 minutes |
| Time to detect issue | ~30-60 seconds |
| False positive rate | <5% (with AI) |
| Cost per deployment | ~$0.0003 |
| Security tools | 3 (Gitleaks, Semgrep, OPA) |
| Lines of custom code | ~300 (Python AI analyzer) |

---

## After Demo

### Follow-Up Materials
- Share GitHub repository link
- Provide architecture diagram
- Send cost breakdown
- Offer to help with implementation

### Next Steps for Interested Parties
1. Fork the repository
2. Set up their own AWS account
3. Configure secrets
4. Customize security rules
5. Deploy to their environment

---

**Built with ❤️ for secure, intelligent deployments**

Good luck with your demo! 🎯

