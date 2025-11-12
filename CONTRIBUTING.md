# Contributing to SecureDeploy Guardrail

Thank you for your interest in contributing to the AI-powered SecureDeploy Guardrail project!

## 🎯 Project Goals

This project demonstrates:
1. AI-powered security analysis for CI/CD pipelines
2. Integration of multiple security tools (Gitleaks, Semgrep, OPA)
3. Intelligent deployment decisions based on context
4. Cost-effective security automation using free tiers

## 🛠️ Development Setup

### Prerequisites
- Git
- Python 3.11+
- Terraform >= 1.0
- AWS Account
- OpenAI API Key
- GitHub Account

### Local Development

```bash
# Clone repository
git clone https://github.com/vshivanna-create/ai-innovation.git
cd ai-innovation

# Set up Python environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r guardrail/requirements.txt

# Configure environment variables
cp .env.example .env
# Edit .env with your API keys (never commit this file!)

# Test the AI analyzer locally
python guardrail/ai_analyzer.py tests/
```

## 📝 How to Contribute

### Reporting Issues

Before creating an issue, please:
1. Check existing issues to avoid duplicates
2. Use the issue template if available
3. Include detailed reproduction steps
4. Provide relevant logs and screenshots

### Suggesting Enhancements

We welcome enhancement suggestions! Please:
1. Clearly describe the feature and its benefits
2. Explain the use case
3. Consider backwards compatibility
4. Be open to discussion and feedback

### Pull Requests

#### Process

1. **Fork the repository**
   ```bash
   # Click "Fork" on GitHub
   git clone https://github.com/YOUR_USERNAME/ai-innovation.git
   cd ai-innovation
   git remote add upstream https://github.com/vshivanna-create/ai-innovation.git
   ```

2. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   # or
   git checkout -b fix/your-bug-fix
   ```

3. **Make your changes**
   - Follow the code style guidelines
   - Write clear commit messages
   - Add tests if applicable
   - Update documentation

4. **Test your changes**
   ```bash
   # Run local tests
   python guardrail/ai_analyzer.py tests/

   # Test security configurations
   gitleaks detect --source .
   semgrep --config .semgrep/rules.yaml .
   conftest test infrastructure/ --policy policies/
   ```

5. **Commit your changes**
   ```bash
   git add .
   git commit -m "feat: Add new feature description"
   # or
   git commit -m "fix: Fix bug description"
   ```

6. **Push to your fork**
   ```bash
   git push origin feature/your-feature-name
   ```

7. **Create Pull Request**
   - Go to the original repository on GitHub
   - Click "New Pull Request"
   - Select your feature branch
   - Fill out the PR template
   - Link related issues

#### PR Guidelines

- ✅ Clear, descriptive title
- ✅ Detailed description of changes
- ✅ Reference related issues
- ✅ Include screenshots/demos if UI changes
- ✅ Tests pass in GitHub Actions
- ✅ Documentation updated
- ✅ No merge conflicts

## 🎨 Code Style

### Python

Follow PEP 8 guidelines:
```python
# Good
def analyze_security_findings(findings: Dict[str, Any]) -> str:
    """Analyze security findings and generate report."""
    pass

# Bad
def analyzeSecurityFindings(findings):
    pass
```

### JavaScript

Follow standard JavaScript conventions:
```javascript
// Good
function displayMessage(message) {
    const element = document.getElementById('output');
    element.textContent = message;
}

// Bad
function displaymessage(msg) {
    document.getElementById('output').innerHTML = msg;
}
```

### Terraform

Follow HashiCorp's style guide:
```hcl
# Good
resource "aws_s3_bucket" "website" {
  bucket = var.bucket_name

  tags = {
    Environment = var.environment
    Project     = "SecureDeploy"
  }
}

# Bad
resource "aws_s3_bucket" "website" {
bucket=var.bucket_name
tags={Environment=var.environment,Project="SecureDeploy"}
}
```

## 🧪 Testing

### Manual Testing

Use the test scenarios in `tests/` directory:
```bash
# Test secret detection
cp tests/test-secret.example test-secret.txt
# Commit and push to trigger workflow
```

### Automated Testing

GitHub Actions will automatically:
1. Run security scans
2. Execute AI guardrail analysis
3. Test deployment (on main branch)

## 📚 Documentation

When contributing, please update:

- **README.md** - For user-facing changes
- **docs/SETUP.md** - For setup process changes
- **docs/ARCHITECTURE.md** - For architectural changes
- **docs/DEMO.md** - For new demo scenarios
- **Code comments** - For complex logic

## 🏷️ Commit Message Convention

We follow [Conventional Commits](https://www.conventionalcommits.org/):

```
<type>: <description>

[optional body]

[optional footer]
```

**Types:**
- `feat:` New feature
- `fix:` Bug fix
- `docs:` Documentation changes
- `style:` Code style changes (formatting)
- `refactor:` Code refactoring
- `test:` Adding or updating tests
- `chore:` Maintenance tasks

**Examples:**
```bash
feat: Add support for Azure deployment
fix: Correct OPA policy for S3 encryption
docs: Update setup guide with OIDC instructions
refactor: Simplify AI prompt generation
test: Add test case for multiple security issues
```

## 🔒 Security

### Reporting Security Issues

**DO NOT** open public issues for security vulnerabilities.

Instead:
1. Email the maintainers directly
2. Provide detailed description
3. Include steps to reproduce
4. Suggest potential fixes if known

### Security Guidelines

- Never commit secrets or credentials
- Use `.gitignore` for sensitive files
- Rotate keys if accidentally exposed
- Follow principle of least privilege
- Keep dependencies updated

## 🎯 Areas for Contribution

### High Priority
- [ ] Add support for more security tools (Trivy, Snyk, etc.)
- [ ] Implement caching for scan results
- [ ] Add Slack/Teams notification integration
- [ ] Create web dashboard for reports
- [ ] Add support for Azure/GCP deployments

### Medium Priority
- [ ] Improve AI prompt engineering
- [ ] Add more OPA policies
- [ ] Create Semgrep custom rules
- [ ] Add metrics and monitoring
- [ ] Implement rollback mechanism

### Good First Issues
- [ ] Improve documentation
- [ ] Add more test scenarios
- [ ] Enhance error messages
- [ ] Add code comments
- [ ] Fix typos

## 📜 License

By contributing, you agree that your contributions will be licensed under the MIT License.

## 🤝 Code of Conduct

### Our Standards

- ✅ Be respectful and inclusive
- ✅ Welcome newcomers
- ✅ Accept constructive criticism
- ✅ Focus on what's best for the community
- ✅ Show empathy towards others

### Unacceptable Behavior

- ❌ Harassment or discriminatory language
- ❌ Trolling or insulting comments
- ❌ Personal or political attacks
- ❌ Publishing others' private information
- ❌ Unprofessional conduct

## 💬 Communication

- **GitHub Issues** - Bug reports, feature requests
- **GitHub Discussions** - General questions, ideas
- **Pull Requests** - Code contributions

## 🙏 Recognition

Contributors will be:
- Listed in the project README
- Mentioned in release notes
- Credited in documentation

## 📞 Getting Help

If you need help:
1. Check the documentation (README, docs/)
2. Search existing issues
3. Ask in GitHub Discussions
4. Create a new issue with details

---

**Thank you for contributing to SecureDeploy Guardrail!** 🛡️

Every contribution, no matter how small, makes this project better for everyone.

