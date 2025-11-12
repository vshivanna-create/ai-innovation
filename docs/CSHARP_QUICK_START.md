# 🚀 C# Security Scanning - Quick Start

Get C# static code analysis running in **5 minutes**!

---

## ⚡ Quick Steps

### 1. Already Done! ✅
If you're using this repo, C# scanning is **already configured**:
- ✅ Semgrep C# rules loaded
- ✅ Security Code Scan ready
- ✅ Workflow auto-detects `.csproj` files
- ✅ AI Guardrail analyzes C# findings

### 2. Test It!

```bash
# Copy a test vulnerable file
cp tests/csharp-samples/VulnerableController.cs .

# Push to trigger scan
git add VulnerableController.cs
git commit -m "test: Add C# test file"
git push
```

### 3. Watch It Block! 🚫

```
GitHub Actions → Security Scan
  🔍 Gitleaks: Found hardcoded API key
  🛡️ Semgrep: Found SQL injection
  🤖 AI Guardrail: BLOCK_DEPLOYMENT

❌ Deployment blocked! See guardrail-report.md
```

### 4. Fix and Deploy ✅

```bash
# Remove vulnerable file
git rm VulnerableController.cs
git commit -m "fix: Remove test vulnerability"
git push
```

```
GitHub Actions → Security Scan
  ✅ Gitleaks: No secrets
  ✅ Semgrep: No issues
  🤖 AI Guardrail: SAFE_TO_DEPLOY

✅ Deployed to AWS!
```

---

## 🧪 Test Scenarios

### Scenario 1: SQL Injection

```csharp
// Create: BadController.cs
[HttpGet("{id}")]
public IActionResult Get(string id)
{
    string sql = $"SELECT * FROM Users WHERE Id = '{id}'";
    // ^ This will be BLOCKED
}
```

**Result:** 🔴 **BLOCKED** - SQL Injection detected

---

### Scenario 2: Hardcoded Secret

```csharp
// Create: ApiClient.cs
public class ApiClient
{
    private const string ApiKey = "sk-proj-ABC123XYZ789";
    // ^ This will be BLOCKED
}
```

**Result:** 🔴 **BLOCKED** - Secret detected by Gitleaks

---

### Scenario 3: Weak Crypto (Warning)

```csharp
// Create: HashHelper.cs
public string Hash(string input)
{
    return MD5.Create().ComputeHash(Encoding.UTF8.GetBytes(input));
    // ^ This will be WARNED
}
```

**Result:** 🟡 **WARNING** - Weak algorithm (may still deploy)

---

## 📊 What You'll See

### GitHub Actions Output
```
Run Semgrep (C# Rules)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Scanning with C# security rules...
  ✓ Loaded .semgrep/csharp-rules.yaml
  ✓ Found 12 rules
  ⚠️ Detected 3 findings:
     - SQL Injection in BadController.cs
     - Hardcoded secret in ApiClient.cs
     - Weak crypto in HashHelper.cs

AI Guardrail Analysis
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Analyzing findings with GPT-4o-mini...

DECISION: BLOCK_DEPLOYMENT
RISK LEVEL: CRITICAL
FINDINGS: 3 security issues

Deployment: BLOCKED ❌
```

### Your Website Dashboard
```
┌─────────────────────────────────────────┐
│  Latest Security Scan Results           │
├─────────────────────────────────────────┤
│  🔐 Gitleaks        🛡️ Semgrep          │
│       1                  3               │
│  Secret Found      Issues Found         │
│                                          │
│  ❌ Deployment Blocked                   │
│  🔴 Risk: CRITICAL                       │
└─────────────────────────────────────────┘
```

---

## 🎯 Common Use Cases

### Use Case 1: New C# Project

```bash
# Add your C# project
mkdir MySecureAPI
cd MySecureAPI
dotnet new webapi
cd ..

git add .
git commit -m "Add C# API project"
git push
# → Automatic security scan!
```

---

### Use Case 2: Existing .NET Solution

```bash
# Your existing solution
MySolution/
  ├── MyAPI/
  │   └── MyAPI.csproj
  ├── MyLib/
  │   └── MyLib.csproj
  └── MySolution.sln

# Just push - scans automatically!
git push
# → All .csproj files scanned
```

---

### Use Case 3: Mono Repo (Multiple Languages)

```bash
project/
  ├── frontend/         # JavaScript/React
  ├── backend/          # C# .NET API
  ├── infrastructure/   # Terraform
  └── .github/workflows/

# Push triggers scans for ALL languages!
git push
# → JS + C# + IaC all scanned together
```

---

## 🔧 Configuration (Optional)

### Add More C# Rules

Edit `.semgrep/csharp-rules.yaml`:

```yaml
rules:
  - id: my-custom-rule
    pattern: |
      public class $CLASS
      {
        public string ApiKey = "...";
      }
    message: "Don't expose API keys as public fields!"
    severity: ERROR
    languages: [csharp]
```

### Adjust AI Sensitivity

The AI automatically adjusts decisions based on:
- **Critical** (secrets, injections) → Always BLOCKS
- **High** (crypto, validation) → Usually BLOCKS
- **Medium** (warnings, best practices) → Usually APPROVES with warnings

---

## 📚 Full Documentation

- [Complete C# Integration Guide](CSHARP_INTEGRATION.md)
- [C# Test Samples](../tests/csharp-samples/)
- [Main Project README](../README.md)

---

## 💡 Pro Tips

1. **Test first** with sample files before your real code
2. **Check workflow logs** to see what was detected
3. **View report** in `scan-results/guardrail-report.md`
4. **Monitor dashboard** on your deployed website

---

## ❓ Troubleshooting

**Q: C# scan not running?**
```bash
# Check if .csproj exists
find . -name "*.csproj"

# If none found, scan won't run (by design)
```

**Q: Too many false positives?**
```bash
# Add to .gitleaks.toml allowlist
[allowlist]
paths = [
  '''MyProject/Generated/''',  # Auto-generated code
  '''**/obj/''',               # Build artifacts
]
```

**Q: Want to see what Semgrep found?**
```bash
# Download scan-results artifact from GitHub Actions
# Look at: scan-results/semgrep-report.json
```

---

**You're all set!** Push some C# code and watch the magic happen! 🚀

