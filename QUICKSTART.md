# Quick Start Guide - SecureDeploy Guardrail

Get up and running in 15 minutes! ⚡

## Prerequisites

- GitHub account
- AWS account (Account ID: `955409238877`, Region: `us-west-2`)
- OpenAI API key

## Step 1: Get Your API Keys (5 minutes)

### OpenAI API Key
1. Go to https://platform.openai.com/api-keys
2. Click "Create new secret key"
3. Copy the key (starts with `sk-proj-...`)

### AWS Credentials
1. Go to AWS Console → IAM → Users
2. Select your user → Security credentials
3. Create access key → Copy both keys

## Step 2: Setup GitHub Secrets (2 minutes)

Go to your repository: https://github.com/vshivanna-create/ai-innovation/settings/secrets/actions

Add these 3 secrets:

| Name | Value |
|------|-------|
| `OPENAI_API_KEY` | Your OpenAI key |
| `AWS_ACCESS_KEY_ID` | Your AWS access key |
| `AWS_SECRET_ACCESS_KEY` | Your AWS secret key |

## Step 3: Deploy Infrastructure (5 minutes)

```bash
# Clone repository
git clone https://github.com/vshivanna-create/ai-innovation.git
cd ai-innovation

# Deploy AWS infrastructure
cd infrastructure
terraform init
terraform apply -auto-approve

# Note the outputs
terraform output
```

## Step 4: Test the System (3 minutes)

```bash
# Make a simple change
cd ..
echo "<!-- Updated -->" >> website/index.html

# Commit and push
git add .
git commit -m "Test deployment"
git push origin main
```

## Step 5: Watch It Work! 🎉

1. Go to GitHub → Actions tab
2. Watch your workflow run
3. See the AI analyze security
4. Watch deployment succeed
5. Visit your website!

## What's Next?

- 📖 Read the full [Setup Guide](docs/SETUP.md)
- 🏗️ Explore the [Architecture](docs/ARCHITECTURE.md)
- 🎯 Try the [Demo Scenarios](docs/DEMO.md)
- 🧪 Run [Test Cases](tests/README.md)

## Troubleshooting

### Workflow fails with "OPENAI_API_KEY not found"
➡️ Check that you added the secret to GitHub (Settings → Secrets)

### AWS deployment fails
➡️ Verify your AWS credentials are correct and have necessary permissions

### AI always blocks deployment
➡️ Check there are no real security issues in your code!

## Need Help?

- 📚 Check [docs/SETUP.md](docs/SETUP.md) for detailed instructions
- 🐛 Open an issue on GitHub
- 💬 Start a discussion

---

**That's it! You're now running an AI-powered security guardrail!** 🛡️✨

