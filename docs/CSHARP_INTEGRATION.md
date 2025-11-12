# 🔷 C# Static Code Analysis Integration

This guide shows how to use the **SecureDeploy Guardrail** with C#/.NET projects.

---

## 🎯 Overview

The SecureDeploy Guardrail now includes comprehensive C# security analysis:

- ✅ **Semgrep C# Rules** - Security vulnerability detection
- ✅ **Security Code Scan** - .NET-specific security analyzer
- ✅ **AI-Powered Analysis** - GPT-4o-mini reviews findings
- ✅ **Automatic Blocking** - Prevents insecure deployments

---

## 🚀 Quick Start

### 1️⃣ Add a C# Project to Your Repo

```bash
# Example: Add a .NET Web API project
mkdir MySecureAPI
cd MySecureAPI
dotnet new webapi
cd ..
git add .
git commit -m "Add C# Web API project"
git push
```

### 2️⃣ Automatic Scanning

The workflow **automatically detects** `.csproj` files and runs:
- Semgrep with C# security rules
- Security Code Scan analyzer
- AI guardrail review

---

## 🛡️ What Gets Scanned

### Security Vulnerabilities Detected

| Category | Example Issues |
|----------|----------------|
| **SQL Injection** | Unsafe string concatenation in queries |
| **Command Injection** | Unsanitized `Process.Start()` calls |
| **XSS** | `@Html.Raw()` with user input |
| **Insecure Crypto** | MD5, SHA1, weak random numbers |
| **Hardcoded Secrets** | Passwords in source code |
| **Deserialization** | Unsafe `BinaryFormatter` usage |
| **Path Traversal** | Unvalidated file paths |
| **CSRF** | Missing `[ValidateAntiForgeryToken]` |
| **SSL Bypass** | Disabled certificate validation |

---

## 📋 Example C# Vulnerabilities

### ❌ Bad: SQL Injection

```csharp
// This will be BLOCKED by the AI Guardrail
string userId = Request["userId"];
string sql = $"SELECT * FROM Users WHERE Id = '{userId}'";
SqlCommand cmd = new SqlCommand(sql, connection);
```

### ✅ Good: Parameterized Query

```csharp
// This will PASS
string userId = Request["userId"];
string sql = "SELECT * FROM Users WHERE Id = @UserId";
SqlCommand cmd = new SqlCommand(sql, connection);
cmd.Parameters.AddWithValue("@UserId", userId);
```

---

### ❌ Bad: Hardcoded Secrets

```csharp
// This will be BLOCKED
string apiKey = "sk-1234567890abcdef";
string password = "P@ssw0rd123!";
```

### ✅ Good: Configuration

```csharp
// This will PASS
string apiKey = Configuration["ApiKey"];
string password = Environment.GetEnvironmentVariable("DB_PASSWORD");
```

---

### ❌ Bad: Weak Cryptography

```csharp
// This will be FLAGGED (WARNING)
var hash = MD5.Create().ComputeHash(data);
```

### ✅ Good: Strong Cryptography

```csharp
// This will PASS
var hash = SHA256.Create().ComputeHash(data);
```

---

## 🧪 Testing the Integration

### Test 1: Introduce a SQL Injection

Create `Controllers/TestController.cs`:

```csharp
using Microsoft.AspNetCore.Mvc;

[ApiController]
[Route("api/[controller]")]
public class TestController : ControllerBase
{
    // BAD: SQL Injection vulnerability
    [HttpGet("{userId}")]
    public IActionResult GetUser(string userId)
    {
        string sql = $"SELECT * FROM Users WHERE Id = '{userId}'";
        // This will trigger the AI Guardrail!
        return Ok(sql);
    }
}
```

**Expected Result:**
```
❌ Deployment BLOCKED
🔴 Critical: SQL Injection detected
📝 AI Decision: BLOCK_DEPLOYMENT
```

---

### Test 2: Hardcoded API Key

Create `Services/ApiService.cs`:

```csharp
public class ApiService
{
    // BAD: Hardcoded secret
    private const string ApiKey = "sk-proj-1234567890abcdef";

    public void CallApi()
    {
        // Use ApiKey...
    }
}
```

**Expected Result:**
```
❌ Deployment BLOCKED
🔴 Critical: Hardcoded credentials detected
```

---

## 📊 AI Guardrail Decision Examples

### Scenario 1: Critical Issues (BLOCKS)

**Finding:**
```
- [Semgrep] SQL injection in UserController.cs
- [Gitleaks] API key in ApiService.cs
```

**AI Decision:**
```
DECISION: BLOCK_DEPLOYMENT
RISK LEVEL: CRITICAL

REASONING:
Found 2 critical security vulnerabilities: SQL injection and
hardcoded credentials. These pose immediate security risks and
must be fixed before deployment.

RECOMMENDATIONS:
- Use parameterized queries for database access
- Move credentials to secure configuration
- Review all user input handling
```

---

### Scenario 2: Medium Issues (WARNS but may APPROVE)

**Finding:**
```
- [Semgrep] MD5 hash usage in PasswordHelper.cs
- [Semgrep] Missing CSRF token on POST endpoint
```

**AI Decision:**
```
DECISION: SAFE_TO_DEPLOY
RISK LEVEL: MEDIUM

REASONING:
Found 2 medium-severity issues. No critical vulnerabilities or
secrets detected. Issues should be addressed in next sprint.

RECOMMENDATIONS:
- Upgrade MD5 to SHA256
- Add [ValidateAntiForgeryToken] to POST actions
```

---

## 🔧 Customizing C# Rules

### Add Custom Semgrep Rule

Edit `.semgrep/csharp-rules.yaml`:

```yaml
rules:
  - id: my-custom-rule
    pattern: |
      public class $CLASS
      {
        public string Password;
      }
    message: "Don't expose passwords as public fields!"
    severity: ERROR
    languages: [csharp]
```

### Configure Security Code Scan

Add `.editorconfig` to your C# project:

```ini
[*.cs]

# Enable all Security Code Scan rules
dotnet_diagnostic.SCS0001.severity = error  # Command Injection
dotnet_diagnostic.SCS0002.severity = error  # SQL Injection
dotnet_diagnostic.SCS0003.severity = error  # XPath Injection
dotnet_diagnostic.SCS0004.severity = error  # Certificate Validation Disabled
```

---

## 📈 Viewing Results

### GitHub Actions Output

```
Security Scan Summary
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ Gitleaks: 0 findings
⚠️  Semgrep: 3 findings (C# rules)
✅ OPA: Policy checks passed
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

AI Guardrail Analysis
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
❌ DECISION: BLOCK_DEPLOYMENT
🔴 RISK LEVEL: HIGH
📋 ISSUES: 3 security vulnerabilities
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### Website Dashboard

Your website at `https://your-cloudfront-url.com` will show:

```
Latest Security Scan Results
┌────────────────┐  ┌────────────────┐  ┌────────────────┐
│  🔐 Gitleaks   │  │  🛡️ Semgrep    │  │  📋 OPA        │
│                │  │                │  │                │
│      0         │  │      3         │  │      ✓         │
│  No Secrets    │  │  Issues Found  │  │  Policy OK     │
└────────────────┘  └────────────────┘  └────────────────┘
```

---

## 🔄 Workflow Integration

### The Complete Flow

```
Push C# Code
    ↓
Gitleaks Scan (secrets)
    ↓
Semgrep Scan (C# security rules)
    ↓
Security Code Scan (.NET analyzer)
    ↓
AI Guardrail Analysis (GPT-4o-mini)
    ↓
┌─────────────────────────────────┐
│ Decision: SAFE_TO_DEPLOY?       │
│                                  │
│ YES → Deploy to AWS              │
│ NO  → Block & Create Report      │
└─────────────────────────────────┘
```

---

## 💰 Cost Considerations

| Component | Cost |
|-----------|------|
| **Semgrep** | $0 (Open Source) |
| **Security Code Scan** | $0 (Open Source) |
| **GitHub Actions** | $0 (2,000 free minutes/month) |
| **OpenAI API** | ~$0.001 per scan (GPT-4o-mini) |
| **Total** | **~$0** for prototype/demo |

---

## 🚨 Common Issues & Fixes

### Issue 1: "No .csproj files found"

**Solution:** Ensure your C# project has a `.csproj` file:

```bash
cd MyProject
dotnet new console  # or webapi, mvc, etc.
```

---

### Issue 2: "Semgrep C# rules not loading"

**Solution:** Verify file exists:

```bash
ls -la .semgrep/csharp-rules.yaml
```

If missing, recreate it from this guide.

---

### Issue 3: "False positives in test files"

**Solution:** Add test paths to `.gitleaks.toml` allowlist:

```toml
[allowlist]
paths = [
  '''Tests/''',
  '''.*\.Tests/''',
  '''.*\.Test\.cs'''
]
```

---

## 📚 Additional Resources

- [Semgrep C# Rules](https://semgrep.dev/r?lang=csharp)
- [Security Code Scan](https://security-code-scan.github.io/)
- [OWASP Top 10 for .NET](https://owasp.org/www-project-top-ten/)
- [Microsoft Security Best Practices](https://learn.microsoft.com/en-us/dotnet/standard/security/)

---

## ✅ Checklist for C# Projects

Before deploying:

- [ ] No SQL injection vulnerabilities
- [ ] No hardcoded secrets/passwords
- [ ] Strong cryptography (SHA256+, not MD5/SHA1)
- [ ] CSRF protection on POST endpoints
- [ ] Input validation on all user data
- [ ] SSL certificate validation enabled
- [ ] No unsafe deserialization
- [ ] Proper error handling (no stack traces exposed)

---

## 🎯 Next Steps

1. **Add a C# project** to test the integration
2. **Introduce a test vulnerability** to see blocking in action
3. **Fix the issue** and watch deployment proceed
4. **View results** on your live website dashboard

---

**Questions or issues?** Check the main [README.md](../README.md) or GitHub Actions logs.

