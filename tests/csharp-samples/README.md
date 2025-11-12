# C# Security Test Samples

⚠️ **WARNING: These files contain INTENTIONAL security vulnerabilities for testing purposes!**

**DO NOT use any of this code in production applications!**

---

## Purpose

These C# code samples are designed to **test the AI-Powered SecureDeploy Guardrail** by introducing known security vulnerabilities that should be detected and blocked.

---

## Test Files

### 1. `VulnerableController.cs`
Tests detection of:
- ✅ SQL Injection (string concatenation in queries)
- ✅ Hardcoded API keys
- ✅ Command injection (unsafe `Process.Start()`)

**Expected Findings:**
- Semgrep: SQL injection vulnerability
- Gitleaks: Hardcoded secret (API key)
- AI Decision: **BLOCK_DEPLOYMENT**

---

### 2. `WeakCryptoHelper.cs`
Tests detection of:
- ✅ Weak hash algorithms (MD5, SHA1)
- ✅ Insecure random number generation

**Expected Findings:**
- Semgrep: Weak cryptography warnings
- AI Decision: **WARN** or **BLOCK** depending on context

---

### 3. `XSSandDeserializationExamples.cs`
Tests detection of:
- ✅ Cross-site scripting (XSS) via `Html.Raw()`
- ✅ Unsafe deserialization (`BinaryFormatter`)
- ✅ Path traversal vulnerabilities
- ✅ SSL certificate validation bypass
- ✅ Missing CSRF protection

**Expected Findings:**
- Semgrep: Multiple high-severity issues
- AI Decision: **BLOCK_DEPLOYMENT**

---

## How to Use

### Quick Test (Copy to Your Project)

1. **To test blocking:**
   ```bash
   # Copy a vulnerable file to trigger the guardrail
   cp tests/csharp-samples/VulnerableController.cs src/Controllers/
   git add .
   git commit -m "test: Add vulnerable controller"
   git push
   ```

   Expected Result: ❌ **Deployment BLOCKED**

2. **To test approval:**
   ```bash
   # Remove the vulnerable code
   git rm src/Controllers/VulnerableController.cs
   git commit -m "fix: Remove vulnerable code"
   git push
   ```

   Expected Result: ✅ **Deployment APPROVED**

---

## Vulnerability Examples

### SQL Injection

❌ **Bad:**
```csharp
string sql = $"SELECT * FROM Users WHERE Id = '{userId}'";
SqlCommand cmd = new SqlCommand(sql, connection);
```

✅ **Good:**
```csharp
string sql = "SELECT * FROM Users WHERE Id = @UserId";
SqlCommand cmd = new SqlCommand(sql, connection);
cmd.Parameters.AddWithValue("@UserId", userId);
```

---

### Hardcoded Secrets

❌ **Bad:**
```csharp
string apiKey = "sk-proj-1234567890abcdefghijklmnop";
```

✅ **Good:**
```csharp
string apiKey = Configuration["ApiKey"];
```

---

### Weak Cryptography

❌ **Bad:**
```csharp
using (MD5 md5 = MD5.Create())
{
    byte[] hash = md5.ComputeHash(data);
}
```

✅ **Good:**
```csharp
using (SHA256 sha256 = SHA256.Create())
{
    byte[] hash = sha256.ComputeHash(data);
}
```

---

### XSS Prevention

❌ **Bad:**
```csharp
@Html.Raw(userInput)  // Allows script injection!
```

✅ **Good:**
```csharp
@Html.Encode(userInput)  // Safe output
```

---

## Expected AI Guardrail Behavior

### High-Risk Code (BLOCKS Deployment)
```
=== SCAN RESULTS ===
🔴 Critical: 2 (Secrets + SQL Injection)
🟠 High: 1 (Command Injection)

=== AI DECISION ===
❌ BLOCK_DEPLOYMENT
🔴 RISK LEVEL: CRITICAL

REASONING:
Multiple critical security vulnerabilities detected including SQL
injection and hardcoded credentials. These pose immediate security
risks and must be fixed before deployment.

RECOMMENDATIONS:
- Use parameterized queries for database access
- Move secrets to secure configuration
- Validate all user inputs
```

### Medium-Risk Code (May WARN or APPROVE)
```
=== SCAN RESULTS ===
🟡 Medium: 3 (Weak crypto warnings)

=== AI DECISION ===
✅ SAFE_TO_DEPLOY (with warnings)
🟡 RISK LEVEL: MEDIUM

REASONING:
No critical vulnerabilities detected. Found weak cryptography usage
which should be addressed but doesn't block deployment.

RECOMMENDATIONS:
- Upgrade MD5/SHA1 to SHA256
- Review crypto library versions
```

---

## Cleanup

These test files are in the `tests/` directory and are **excluded from production builds**.

They are also **allowlisted** in `.gitleaks.toml` so test credentials don't trigger false positives:

```toml
[allowlist]
paths = [
  '''tests/''',
  '''.*Test\.cs''',
]
```

---

## Integration with CI/CD

The GitHub Actions workflow automatically:
1. Scans these files with Gitleaks, Semgrep, Security Code Scan
2. Aggregates findings
3. Sends to AI Guardrail for analysis
4. Makes deployment decision
5. Reports results on website dashboard

---

## See Also

- [C# Integration Guide](../../docs/CSHARP_INTEGRATION.md)
- [Main README](../../README.md)
- [Demo Script](../../docs/DEMO.md)

---

**Remember:** These are **intentionally vulnerable** examples for **testing only**! 🔒

