# Setup Guide - SecureDeploy Guardrail

Complete setup instructions for deploying the AI-powered SecureDeploy Guardrail system.

## Prerequisites

### Required Accounts
1. **GitHub Account** - For repository and Actions
2. **AWS Account** - Account ID: `955409238877`, Region: `us-west-2`
3. **OpenAI Account** - For AI guardrail analysis

### Required Tools (for local setup)
- Git
- Terraform >= 1.0
- AWS CLI v2
- Python 3.11+

---

## Step 1: GitHub Repository Setup

### 1.1 Create/Clone Repository

```bash
git clone https://github.com/vshivanna-create/ai-innovation.git
cd ai-innovation
```

### 1.2 Configure GitHub Secrets

Go to repository **Settings → Secrets and variables → Actions** and add:

| Secret Name | Description | How to Get |
|-------------|-------------|-----------|
| `OPENAI_API_KEY` | OpenAI API key | https://platform.openai.com/api-keys |
| `AWS_ACCESS_KEY_ID` | AWS access key | AWS Console → IAM → Users → Security credentials |
| `AWS_SECRET_ACCESS_KEY` | AWS secret key | AWS Console → IAM → Users → Security credentials |

**Security Note:**
- Never commit AWS credentials to the repository
- Use environment-specific secrets for production
- Consider using OIDC instead of access keys for production

---

## Step 2: AWS Infrastructure Setup

### 2.1 Configure AWS CLI

```bash
aws configure
# Enter your AWS Access Key ID
# Enter your AWS Secret Access Key
# Default region: us-west-2
# Default output format: json
```

### 2.2 Deploy Infrastructure with Terraform

```bash
cd infrastructure

# Initialize Terraform
terraform init

# Review the plan
terraform plan

# Apply the configuration
terraform apply
```

**Expected Resources Created:**
- S3 bucket for website hosting
- S3 bucket for access logs
- CloudFront distribution
- IAM roles for GitHub Actions
- OIDC provider for GitHub
- CloudWatch log groups

### 2.3 Note the Outputs

After apply completes, note the outputs:

```bash
terraform output
```

You'll see:
- `website_url` - Direct S3 website URL
- `cloudfront_url` - CloudFront CDN URL (recommended)
- `github_actions_role_arn` - IAM role for GitHub Actions

---

## Step 3: OpenAI API Setup

### 3.1 Get API Key

1. Go to https://platform.openai.com
2. Sign up or log in
3. Navigate to **API Keys**
4. Click **Create new secret key**
5. Name it: "SecureDeploy-Guardrail"
6. Copy the key (starts with `sk-proj-...`)

### 3.2 Configure Billing

- Add payment method in OpenAI dashboard
- Set spending limits (recommend $5/month for demos)
- Monitor usage at https://platform.openai.com/usage

**Cost Estimate:**
- GPT-4o-mini: ~$0.0001-0.0003 per analysis
- 100 deployments: ~$0.01-0.03
- Essentially free for demos!

---

## Step 4: Test the Pipeline

### 4.1 Initial Push

```bash
git add .
git commit -m "Initial SecureDeploy Guardrail setup"
git push origin main
```

### 4.2 Monitor GitHub Actions

1. Go to repository → **Actions** tab
2. Click on the running workflow
3. Watch the jobs execute:
   - ✅ Security Scanning
   - ✅ AI Guardrail Analysis
   - ✅ Deploy to AWS

### 4.3 Verify Deployment

Once complete, visit your website:

```bash
# Get URL from Terraform outputs
terraform output website_url

# Or use CloudFront URL
terraform output cloudfront_url
```

---

## Step 5: Configuration Options

### 5.1 Adjust Security Thresholds

Edit `.github/workflows/secure-deploy.yml`:

```yaml
# Modify AI decision criteria
env:
  BLOCK_ON_HIGH: true
  BLOCK_ON_MEDIUM: false
```

### 5.2 Customize Security Rules

**Gitleaks:** Edit `.gitleaks.toml`
```toml
[[rules]]
id = "custom-api-key"
description = "Custom API Key Pattern"
regex = '''your-pattern-here'''
```

**Semgrep:** Edit `.semgrep/rules.yaml`
```yaml
rules:
  - id: custom-security-check
    pattern: your-pattern
    message: "Custom security message"
    severity: ERROR
```

**OPA:** Edit `policies/deployment.rego`
```rego
deny[msg] {
    input.kind == "aws_s3_bucket"
    # Your custom policy
}
```

### 5.3 Change AI Model

Edit `guardrail/ai_analyzer.py`:

```python
# Use different model
model = "gpt-4o-mini"  # Default (cheapest)
# model = "gpt-4o"     # More capable
# model = "gpt-4-turbo" # Most capable
```

---

## Step 6: Testing Security Features

### 6.1 Test Secret Detection

Create a test file with a fake secret:

```bash
echo 'AWS_KEY = "AKIAIOSFODNN7EXAMPLE"' > test-secret.txt
git add test-secret.txt
git commit -m "Test: Add secret"
git push
```

**Expected:** Gitleaks detects it, AI blocks deployment

### 6.2 Test Code Security

Add insecure code:

```javascript
// website/test.js
eval(userInput); // Security issue
```

**Expected:** Semgrep detects it, AI evaluates severity

### 6.3 Test Policy Violation

Modify `infrastructure/main.tf` to remove encryption:

```hcl
# Comment out encryption configuration
# resource "aws_s3_bucket_server_side_encryption_configuration" "website" { ... }
```

**Expected:** OPA/Conftest detects policy violation, AI blocks

---

## Troubleshooting

### GitHub Actions Failures

**Issue:** `OPENAI_API_KEY not found`
- **Fix:** Verify secret is added to GitHub repository settings

**Issue:** `AWS credentials not valid`
- **Fix:** Check AWS access keys in GitHub secrets
- Verify IAM user has necessary permissions

**Issue:** `Terraform state locked`
- **Fix:** Wait for concurrent runs to complete
- Or manually unlock: `terraform force-unlock LOCK_ID`

### AI Guardrail Issues

**Issue:** AI always blocks deployment
- **Fix:** Check OpenAI API quota/billing
- Review prompt in `guardrail/ai_analyzer.py`
- Check security scan results for actual issues

**Issue:** `openai module not found`
- **Fix:** Ensure Python dependencies are installed:
  ```bash
  pip install -r guardrail/requirements.txt
  ```

### AWS Deployment Issues

**Issue:** S3 bucket already exists
- **Fix:** Bucket names must be globally unique
- Change `bucket_name` in `infrastructure/variables.tf`

**Issue:** CloudFront distribution creation slow
- **Fix:** This is normal, can take 10-20 minutes
- Monitor in AWS Console → CloudFront

---

## Cost Monitoring

### AWS Free Tier Limits

| Service | Free Tier | After Free Tier |
|---------|-----------|----------------|
| S3 | 5 GB storage | $0.023/GB |
| CloudFront | 1 TB data transfer | $0.085/GB |
| Lambda | 1M requests | $0.20/1M |

### OpenAI Usage

Monitor at: https://platform.openai.com/usage

- Set monthly budget alerts
- Review token usage per request
- Optimize prompts if needed

### Total Monthly Cost (Demo)

| Component | Cost |
|-----------|------|
| AWS Services | $0 (free tier) |
| OpenAI API | ~$0.03 (100 runs) |
| **Total** | **~$0.03** |

---

## Next Steps

1. ✅ Review [ARCHITECTURE.md](ARCHITECTURE.md) for system design
2. ✅ Follow [DEMO.md](DEMO.md) for demo scenarios
3. ✅ Customize security rules for your needs
4. ✅ Set up monitoring and alerts
5. ✅ Consider OIDC instead of access keys for production

## Support

For issues:
1. Check GitHub Actions logs
2. Review AWS CloudWatch logs
3. Check OpenAI usage dashboard
4. Open issue on GitHub repository

---

**Built with ❤️ for secure, intelligent deployments**

