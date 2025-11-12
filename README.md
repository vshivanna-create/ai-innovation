# 🛡️ AI-Powered SecureDeploy Guardrail

An intelligent deployment security system that uses AI to analyze security scan results and make informed deployment decisions automatically.

## 🎯 Overview

This project demonstrates a **zero-cost, production-ready** security guardrail that:
- ✅ Scans code for secrets, vulnerabilities, and policy violations
- 🤖 Uses AI (OpenAI GPT-4o-mini) to intelligently interpret findings
- 🚦 Automatically approves or blocks deployments with detailed reasoning
- 📊 Provides comprehensive security reports on every deployment
- ☁️ Deploys a static website to AWS S3 + CloudFront

## 🏗️ Architecture

```
┌─────────────────┐
│   GitHub Push   │
└────────┬────────┘
         │
         ▼
┌─────────────────────────────────┐
│   GitHub Actions Workflow       │
│                                  │
│  ┌─────────────────────────┐   │
│  │ Security Scanning       │   │
│  │ • Gitleaks (secrets)    │   │
│  │ • Semgrep (code)        │   │
│  │ • OPA (policies)        │   │
│  └──────────┬──────────────┘   │
│             │                   │
│             ▼                   │
│  ┌─────────────────────────┐   │
│  │ AI Guardrail Analysis   │   │
│  │ • Aggregates findings   │   │
│  │ • OpenAI reasoning      │   │
│  │ • Decision: SAFE/BLOCK  │   │
│  └──────────┬──────────────┘   │
│             │                   │
│             ▼                   │
│  ┌─────────────────────────┐   │
│  │ Deployment Decision     │   │
│  │ • Deploy to S3/CF (✅)  │   │
│  │ • Block & Report (❌)   │   │
│  └─────────────────────────┘   │
└─────────────────────────────────┘
```

## 🚀 Quick Start

### Prerequisites

1. **GitHub Secrets** (already configured):
   - `OPENAI_API_KEY`
   - `AWS_ACCESS_KEY_ID`
   - `AWS_SECRET_ACCESS_KEY`

2. **AWS Account**: Account ID `955409238877`, Region `us-west-2`

### Installation

1. **Clone and setup:**
   ```bash
   git clone https://github.com/vshivanna-create/ai-innovation.git
   cd ai-innovation
   ```

2. **Create AWS infrastructure:**
   ```bash
   cd infrastructure
   terraform init
   terraform plan
   terraform apply
   ```

3. **Push code to trigger workflow:**
   ```bash
   git add .
   git commit -m "Initial deployment"
   git push origin main
   ```

4. **Watch the magic happen!**
   - Go to GitHub Actions tab
   - See security scans run
   - Watch AI analyze results
   - See deployment succeed/fail based on AI decision

## 📁 Project Structure

```
ai-innovation/
├── .github/
│   └── workflows/
│       └── secure-deploy.yml    # Main CI/CD workflow
├── guardrail/
│   ├── ai_analyzer.py           # AI decision engine
│   └── requirements.txt         # Python dependencies
├── policies/
│   ├── deployment.rego          # OPA policies
│   └── conftest.toml           # Conftest config
├── .semgrep/
│   └── rules.yaml              # Semgrep security rules
├── infrastructure/
│   ├── main.tf                 # Terraform for S3 + CloudFront
│   ├── variables.tf            # Terraform variables
│   └── outputs.tf              # Terraform outputs
├── website/
│   ├── index.html              # Demo static site
│   ├── styles.css              # Styling
│   └── script.js               # Demo JavaScript
├── docs/
│   ├── SETUP.md               # Detailed setup guide
│   ├── ARCHITECTURE.md        # System architecture
│   └── DEMO.md                # Demo script
├── .gitleaks.toml             # Gitleaks configuration
└── README.md                  # This file
```

## 🔒 Security Tools

### 1. Gitleaks
Scans for hardcoded secrets, API keys, and credentials.

### 2. Semgrep
Static analysis for security vulnerabilities in JavaScript and infrastructure code.

### 3. OPA/Conftest
Policy-as-code validation for infrastructure configurations:
- S3 bucket encryption
- CloudFront security headers
- Access control policies

## 🤖 AI Guardrail

The AI analyzer (`guardrail/ai_analyzer.py`) uses OpenAI's GPT-4o-mini to:
- Aggregate all security scan results
- Understand context and severity
- Make intelligent deployment decisions
- Provide human-readable explanations
- Suggest remediation steps

**Cost**: ~$0.0001-0.0003 per analysis (essentially free for demos)

## 📊 Demo Scenarios

### Scenario 1: Clean Deployment ✅
- No security issues found
- AI approves deployment
- Website goes live on S3 + CloudFront

### Scenario 2: Secret Detected ❌
- Gitleaks finds hardcoded API key
- AI blocks deployment
- Detailed report with fix suggestions

### Scenario 3: Policy Violation ❌
- OPA detects unencrypted S3 bucket
- AI blocks deployment
- Explains security implications

### Scenario 4: Low Severity Findings ⚠️
- Minor issues detected
- AI approves with warnings
- Deployment proceeds with recommendations

## 🎯 Success Metrics

- ✅ **Zero cost** for demo/prototype usage
- ✅ **~2-3 minute** workflow execution time
- ✅ **100% automated** decision making
- ✅ **Intelligent context** understanding via AI
- ✅ **Production-ready** architecture

## 📖 Documentation

- [Setup Guide](docs/SETUP.md) - Detailed AWS and GitHub setup
- [Architecture](docs/ARCHITECTURE.md) - System design deep-dive
- [Demo Script](docs/DEMO.md) - Step-by-step demo walkthrough

## 🛠️ Technologies

- **CI/CD**: GitHub Actions
- **AI**: OpenAI GPT-4o-mini
- **Security**: Gitleaks, Semgrep, OPA/Conftest
- **Infrastructure**: Terraform, AWS S3, CloudFront
- **Language**: Python 3.9+

## 💰 Cost Breakdown

| Service | Cost | Notes |
|---------|------|-------|
| GitHub Actions | $0 | 2,000 free minutes/month |
| OpenAI API | ~$0.03 | For 100 analyses |
| AWS S3 | $0 | Free tier (5GB storage) |
| AWS CloudFront | $0 | Free tier (1TB transfer) |
| **Total** | **~$0** | Perfect for demos! |

## 🤝 Contributing

This is a demo project for innovation sprint. Feel free to fork and enhance!

## 📄 License

MIT License - Use freely for your projects!

## 🎓 Learn More

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [OpenAI API Documentation](https://platform.openai.com/docs)
- [Open Policy Agent](https://www.openpolicyagent.org/)
- [Semgrep Rules](https://semgrep.dev/docs/)

---

**Built with ❤️ for secure, intelligent deployments**

