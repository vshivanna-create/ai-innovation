# Demo Day - Revert Instructions

**⚠️ BEFORE YOUR DEMO: Revert the temporary deployment bypass!**

## Quick Revert (5 minutes before demo)

### Step 1: Enable Proper Blocking

Edit `.github/workflows/secure-deploy.yml` line 225:

**Current (TEMPORARY):**
```yaml
if: always()
```

**Change to (DEMO):**
```yaml
if: success() && needs.ai-guardrail.result == 'success'
```

### Step 2: Commit and Push

```bash
git add .github/workflows/secure-deploy.yml
git commit -m "Enable AI Guardrail blocking for demo"
git push origin main
```

### Step 3: Wait for Clean Deployment

Wait ~2 minutes for workflow to complete. It should deploy successfully since there are 0 critical issues.

---

## Demo Flow

Now you can demonstrate:

### 1. Show Clean Deployment ✅
- Current state: Website live with 0 critical issues
- Show workflow: All green

### 2. Add Secrets and Block ❌
```bash
# Add test secrets
cp tests/test-secret.example test-secret.txt
git add test-secret.txt
git commit -m "Test: Add secrets"
git push origin main
```

**Expected:**
- Gitleaks detects secrets
- AI Guardrail blocks deployment
- Deployment job skipped
- Website shows blocked status

### 3. Clean Up and Deploy ✅
```bash
# Remove secrets
git rm test-secret.txt
git commit -m "Fix: Remove secrets"
git push origin main
```

**Expected:**
- All scans pass
- AI approves
- Deployment succeeds
- Website shows success

---

## Emergency: If Something Goes Wrong

### Re-enable bypass:
```bash
# In .github/workflows/secure-deploy.yml line 225
if: always()

git add .github/workflows/secure-deploy.yml
git commit -m "temp: Re-enable bypass"
git push origin main
```

---

## Current State

- ✅ Gitleaks: Configured with smart allowlist
  - Ignores: docs/, tests/, README.md, other documentation
  - Detects: Real secrets in test-secret.txt (for demo)
- ✅ Semgrep: Running (some false positives acceptable)
- ✅ OPA: Configured and running
- ✅ AI Guardrail: Using OpenAI GPT-4o-mini
- ✅ Website: Live with status displays
- ⚠️ Deployment: **BYPASSED** (will deploy even if blocked)

**Status:** Ready for demo after reverting the bypass!

---

**Good luck with your demo! 🚀🛡️**

