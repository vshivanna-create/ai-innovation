# Deployment Checklist - SecureDeploy Guardrail

Use this checklist to ensure everything is properly configured before your demo.

## Pre-Deployment Setup

### GitHub Repository
- [ ] Repository created: `vshivanna-create/ai-innovation`
- [ ] Repository cloned locally
- [ ] All files committed and pushed

### GitHub Secrets Configuration
- [ ] `OPENAI_API_KEY` added to repository secrets
- [ ] `AWS_ACCESS_KEY_ID` added to repository secrets
- [ ] `AWS_SECRET_ACCESS_KEY` added to repository secrets
- [ ] Secrets are accessible (no typos in names)

### AWS Account
- [ ] AWS account accessible (ID: 955409238877)
- [ ] Region set to `us-west-2`
- [ ] IAM user has necessary permissions:
  - [ ] S3 full access
  - [ ] CloudFront access
  - [ ] IAM role creation (for OIDC)
  - [ ] CloudWatch logs access

### OpenAI Account
- [ ] OpenAI account created
- [ ] API key generated
- [ ] Billing method added (if required)
- [ ] Usage limits set (optional but recommended)

## Infrastructure Deployment

### Terraform Setup
- [ ] Terraform installed (v1.0+)
- [ ] AWS CLI configured
- [ ] Navigated to `infrastructure/` directory
- [ ] Ran `terraform init` successfully
- [ ] Ran `terraform plan` (review output)
- [ ] Ran `terraform apply` successfully
- [ ] Noted output values:
  - [ ] `website_url`
  - [ ] `cloudfront_url`
  - [ ] `github_actions_role_arn`

### Infrastructure Verification
- [ ] S3 bucket created and accessible
- [ ] CloudFront distribution created (may take 10-20 min)
- [ ] IAM roles created
- [ ] OIDC provider configured
- [ ] CloudWatch log group created

## GitHub Actions Workflow

### Workflow File
- [ ] `.github/workflows/secure-deploy.yml` exists
- [ ] Workflow is valid YAML (no syntax errors)
- [ ] All jobs are properly configured
- [ ] Conditional logic is correct

### Security Tools Configuration
- [ ] `.gitleaks.toml` exists and configured
- [ ] `.semgrep/rules.yaml` exists and configured
- [ ] `policies/deployment.rego` exists and configured
- [ ] `policies/conftest.toml` exists and configured

### AI Guardrail
- [ ] `guardrail/ai_analyzer.py` exists
- [ ] `guardrail/requirements.txt` exists
- [ ] Python dependencies are correct
- [ ] Script has execute permissions

## Initial Deployment Test

### First Push
- [ ] Made a small change to test
- [ ] Committed changes
- [ ] Pushed to `main` branch
- [ ] GitHub Actions workflow triggered

### Workflow Execution
- [ ] Security scan job completed
  - [ ] Gitleaks ran successfully
  - [ ] Semgrep ran successfully
  - [ ] OPA/Conftest ran successfully
- [ ] AI guardrail job completed
  - [ ] Scan results downloaded
  - [ ] Python script executed
  - [ ] OpenAI API called successfully
  - [ ] Decision made and output set
- [ ] Deploy job completed
  - [ ] AWS credentials configured
  - [ ] Files synced to S3
  - [ ] Website accessible

### Verification
- [ ] Workflow completed successfully (green checkmark)
- [ ] Website URL is accessible
- [ ] Website displays correctly
- [ ] No errors in workflow logs

## Demo Preparation

### Browser Tabs
- [ ] GitHub repository page
- [ ] GitHub Actions page
- [ ] AWS S3 Console
- [ ] AWS CloudFront Console
- [ ] Website URL
- [ ] OpenAI usage dashboard

### Terminal Setup
- [ ] Repository cloned and ready
- [ ] Git configured with name and email
- [ ] Can push commits
- [ ] Test files ready in `tests/` directory

### Test Scenarios Ready
- [ ] Clean deployment (baseline)
- [ ] Secret detection test file ready
- [ ] Code security test file ready
- [ ] Policy violation test file ready
- [ ] Know how to activate each test

### Documentation
- [ ] README.md reviewed
- [ ] QUICKSTART.md reviewed
- [ ] docs/DEMO.md reviewed
- [ ] Talking points prepared

## Cost Monitoring

### AWS Free Tier
- [ ] S3 usage < 5GB
- [ ] CloudFront usage < 1TB
- [ ] No unexpected charges
- [ ] Billing alerts set up (optional)

### OpenAI API
- [ ] Usage dashboard checked
- [ ] No unexpected API calls
- [ ] Cost per analysis < $0.001
- [ ] Monthly limit set (optional)

### Total Cost Check
- [ ] Expected cost: ~$0 for demo
- [ ] Actual cost monitored
- [ ] No surprises

## Security Check

### Secrets Management
- [ ] No secrets committed to repository
- [ ] `.gitignore` includes sensitive files
- [ ] `.env` file not committed
- [ ] AWS credentials CSV file deleted
- [ ] OpenAI key stored securely

### Access Control
- [ ] Repository visibility is appropriate (private/public)
- [ ] GitHub Actions logs don't expose secrets
- [ ] AWS resources have proper permissions
- [ ] S3 bucket policy is appropriate for demo

## Backup Plan

### Troubleshooting Resources
- [ ] docs/SETUP.md for detailed setup
- [ ] docs/ARCHITECTURE.md for system design
- [ ] GitHub Actions logs accessible
- [ ] AWS Console accessible for manual checks
- [ ] OpenAI dashboard for API issues

### Rollback Plan
- [ ] Know how to revert commits
- [ ] Can re-run Terraform apply
- [ ] Can manually delete resources if needed
- [ ] Have backup of working state

## Demo Day Checklist

### 30 Minutes Before
- [ ] Verify website is accessible
- [ ] Check GitHub Actions history (recent successful run)
- [ ] Verify all browser tabs are ready
- [ ] Terminal is ready with repo
- [ ] Screen sharing tested (if virtual)

### 5 Minutes Before
- [ ] Close unnecessary applications
- [ ] Notifications silenced
- [ ] Internet connection stable
- [ ] Backup internet available
- [ ] Water/coffee ready 😊

### During Demo
- [ ] Stay calm
- [ ] Explain as you go
- [ ] Show AI reasoning clearly
- [ ] Highlight cost savings
- [ ] Be ready for questions

### After Demo
- [ ] Answer questions
- [ ] Share repository link
- [ ] Offer to help with setup
- [ ] Get feedback
- [ ] Cleanup test files

## Post-Demo Cleanup

### Optional Cleanup (if not continuing)
- [ ] Delete test files
- [ ] Run `terraform destroy` to remove AWS resources
- [ ] Revoke AWS access keys
- [ ] Rotate OpenAI API key
- [ ] Archive repository (optional)

### If Continuing Development
- [ ] Document lessons learned
- [ ] Note improvement ideas
- [ ] Plan next features
- [ ] Update documentation
- [ ] Commit any changes

## Success Criteria

Your demo is ready when:
- ✅ All checklist items above are completed
- ✅ Can successfully deploy clean code
- ✅ Can demonstrate blocking deployment with test cases
- ✅ AI provides clear reasoning and recommendations
- ✅ Website is live and accessible
- ✅ Total cost is within free tier
- ✅ Feel confident explaining the system

## Quick Reference

### Important URLs
- Repository: https://github.com/vshivanna-create/ai-innovation
- AWS Region: us-west-2
- Account ID: 955409238877

### Key Commands
```bash
# Deploy infrastructure
cd infrastructure && terraform apply

# Test deployment
git add . && git commit -m "Test" && git push

# Check status
terraform output

# View website
curl $(terraform output -raw website_url)

# Cleanup
terraform destroy
```

### Emergency Contacts
- GitHub Support: https://support.github.com
- AWS Support: https://aws.amazon.com/support
- OpenAI Support: https://help.openai.com

---

**Good luck with your demo! 🚀**

You've got this! 💪

