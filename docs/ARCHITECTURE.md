# Architecture - SecureDeploy Guardrail

Deep dive into the system architecture, design decisions, and technical implementation.

## Table of Contents
1. [System Overview](#system-overview)
2. [Component Architecture](#component-architecture)
3. [Data Flow](#data-flow)
4. [Security Design](#security-design)
5. [AI Integration](#ai-integration)
6. [Infrastructure](#infrastructure)
7. [Scalability & Performance](#scalability--performance)

---

## System Overview

### High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     GitHub Repository                        │
│  ┌─────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │   Source    │  │     IaC      │  │   Policies   │      │
│  │    Code     │  │  (Terraform) │  │  (OPA/YAML)  │      │
│  └─────────────┘  └──────────────┘  └──────────────┘      │
└───────────────────────────┬─────────────────────────────────┘
                            │ Push Event
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                    GitHub Actions Runner                     │
│  ┌──────────────────────────────────────────────────────┐  │
│  │              Security Scanning Phase                  │  │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────────┐      │  │
│  │  │ Gitleaks │  │ Semgrep  │  │ OPA/Conftest │      │  │
│  │  │ (Secrets)│  │  (Code)  │  │  (Policy)    │      │  │
│  │  └────┬─────┘  └────┬─────┘  └──────┬───────┘      │  │
│  │       │             │                 │               │  │
│  │       └─────────────┼─────────────────┘               │  │
│  │                     │                                 │  │
│  │                     ▼                                 │  │
│  │            ┌─────────────────┐                       │  │
│  │            │ Scan Artifacts  │                       │  │
│  │            │   (JSON Files)  │                       │  │
│  │            └────────┬────────┘                       │  │
│  └─────────────────────┼──────────────────────────────┘  │
│                        │                                  │
│  ┌─────────────────────┼──────────────────────────────┐  │
│  │          AI Guardrail Analysis Phase              │  │
│  │                     ▼                               │  │
│  │         ┌───────────────────────┐                  │  │
│  │         │  Python AI Analyzer   │                  │  │
│  │         │  - Aggregate findings │                  │  │
│  │         │  - Create AI prompt   │                  │  │
│  │         └──────────┬────────────┘                  │  │
│  │                    │                                │  │
│  │                    ▼                                │  │
│  │         ┌───────────────────────┐                  │  │
│  │         │   OpenAI API Call     │────────┐        │  │
│  │         │   (gpt-4o-mini)       │        │        │  │
│  │         └──────────┬────────────┘        │        │  │
│  │                    │                      │        │  │
│  │                    ▼                      │        │  │
│  │         ┌───────────────────────┐        │        │  │
│  │         │  Decision Engine      │        │        │  │
│  │         │  SAFE / BLOCK         │        │        │  │
│  │         └──────────┬────────────┘        │        │  │
│  └────────────────────┼─────────────────────┘        │  │
│                       │                               │  │
│                       ▼                               │  │
│  ┌─────────────────────────────────────────┐        │  │
│  │      Conditional Deployment Phase       │        │  │
│  │                                          │        │  │
│  │  If SAFE:                                │        │  │
│  │  ┌────────────────────────────┐         │        │  │
│  │  │  Deploy to AWS S3          │         │        │  │
│  │  │  Invalidate CloudFront     │         │        │  │
│  │  │  Post success comment      │         │        │  │
│  │  └────────────────────────────┘         │        │  │
│  │                                          │        │  │
│  │  If BLOCK:                               │        │  │
│  │  ┌────────────────────────────┐         │        │  │
│  │  │  Stop pipeline             │         │        │  │
│  │  │  Post detailed report      │         │        │  │
│  │  │  Exit with error           │         │        │  │
│  │  └────────────────────────────┘         │        │  │
│  └──────────────────────────────────────────┘        │  │
└────────────────────────────┬──────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────┐
│                         AWS Cloud                            │
│  ┌──────────────┐  ┌───────────────┐  ┌─────────────┐     │
│  │  S3 Bucket   │→ │  CloudFront   │→ │   Users     │     │
│  │  (Website)   │  │  (CDN)        │  │             │     │
│  └──────────────┘  └───────────────┘  └─────────────┘     │
└─────────────────────────────────────────────────────────────┘
```

---

## Component Architecture

### 1. Security Scanning Layer

#### Gitleaks (Secret Detection)
- **Purpose:** Detect hardcoded secrets, credentials, API keys
- **Technology:** Go-based pattern matching
- **Output:** JSON with findings and line numbers
- **Configuration:** `.gitleaks.toml`

**Key Features:**
- Pre-commit and CI scanning
- Custom regex patterns
- Entropy detection for random strings
- Historical commit scanning

#### Semgrep (Static Code Analysis)
- **Purpose:** Detect security vulnerabilities in code
- **Technology:** Pattern-based static analysis
- **Output:** JSON with code issues and severity
- **Configuration:** `.semgrep/rules.yaml`

**Key Features:**
- Language-agnostic rules
- Custom rule creation
- IDE integration support
- Low false positive rate

#### OPA/Conftest (Policy as Code)
- **Purpose:** Validate infrastructure against policies
- **Technology:** Rego policy language
- **Output:** JSON with policy violations
- **Configuration:** `policies/deployment.rego`

**Key Features:**
- Declarative policy definitions
- Terraform plan validation
- Kubernetes manifest checking
- Custom policy enforcement

### 2. AI Guardrail Layer

#### AI Analyzer (`guardrail/ai_analyzer.py`)

**Core Functions:**

```python
class SecurityAnalyzer:
    def load_scan_results()      # Load all tool outputs
    def aggregate_findings()     # Combine and categorize
    def create_ai_prompt()       # Generate intelligent prompt
    def analyze_with_ai()        # Call OpenAI API
    def generate_report()        # Create markdown report
```

**Decision Logic:**

```
1. Aggregate all findings by severity
2. Create context-aware prompt for AI
3. Send to OpenAI with specific criteria:
   - BLOCK if critical issues (secrets)
   - BLOCK if high severity + risk
   - APPROVE WITH WARNINGS for medium
   - APPROVE if clean or low severity
4. Parse AI response and extract:
   - Decision (SAFE/BLOCK)
   - Reasoning
   - Recommendations
   - Risk level
```

**Fallback Mechanism:**
If OpenAI API fails, use rule-based decision:
- Critical issues → BLOCK
- High severity count > threshold → BLOCK
- Otherwise → evaluate medium severity

### 3. Deployment Layer

#### GitHub Actions Workflow

**Job Dependencies:**
```yaml
security-scan → ai-guardrail → deploy → report
     ↓               ↓            ↓        ↓
  (parallel)    (sequential)  (conditional)  (always)
```

**Key Features:**
- Artifact passing between jobs
- Conditional execution based on AI decision
- PR comment integration
- Summary generation

#### AWS Deployment

**S3 Website Hosting:**
- Static website hosting enabled
- Public read access for demo
- Versioning for rollback
- Lifecycle policies for cost

**CloudFront Distribution:**
- Global CDN for performance
- HTTPS enforcement
- Custom error pages
- Origin access identity

---

## Data Flow

### 1. Scan Results Flow

```
Source Files
    ↓
Security Tools (parallel execution)
    ↓
JSON Artifacts
    ├── gitleaks-report.json
    ├── semgrep-report.json
    └── opa-report.json
    ↓
Upload to GitHub Artifacts
    ↓
Download in AI job
    ↓
Python AI Analyzer
```

### 2. AI Analysis Flow

```
JSON Scan Results
    ↓
Aggregate by severity
    ↓
Create structured prompt
    ↓
OpenAI API (gpt-4o-mini)
    ↓
Parse response
    ├── Decision: SAFE_TO_DEPLOY / BLOCK_DEPLOYMENT
    ├── Reasoning: [explanation]
    ├── Recommendations: [fixes]
    └── Risk Level: [NONE to CRITICAL]
    ↓
Generate markdown report
    ↓
Set GitHub Actions outputs
    ↓
Upload report artifact
```

### 3. Deployment Flow

```
AI Decision Output
    ↓
Check: decision == "SAFE_TO_DEPLOY"
    ↓
Yes → Deploy Job
    ├── Configure AWS credentials
    ├── Create S3 bucket (if needed)
    ├── Sync website files
    ├── Update CloudFront (optional)
    └── Post success message
    ↓
No → Block Job
    ├── Exit with error
    ├── Post detailed report
    └── Comment on PR
```

---

## Security Design

### Secrets Management

**GitHub Secrets (Encrypted at rest):**
- `OPENAI_API_KEY` - AI guardrail access
- `AWS_ACCESS_KEY_ID` - AWS authentication
- `AWS_SECRET_ACCESS_KEY` - AWS authentication

**Best Practices:**
- Rotate credentials regularly
- Use least-privilege IAM roles
- Enable AWS CloudTrail for auditing
- Monitor GitHub Actions logs

### Access Control

**GitHub:**
- Protected branches (main)
- Required status checks
- PR reviews before merge
- Actions secrets access control

**AWS:**
- IAM roles with minimal permissions
- S3 bucket policies
- CloudFront origin access identity
- VPC endpoints (optional)

### Data Protection

**At Rest:**
- S3 server-side encryption (AES-256)
- Versioning for data recovery
- Access logging to separate bucket

**In Transit:**
- HTTPS enforcement via CloudFront
- TLS 1.2+ for all API calls
- Encrypted GitHub Actions artifacts

---

## AI Integration

### OpenAI API Usage

**Model Selection:**
- **gpt-4o-mini** - Chosen for cost/performance balance
- Cost: ~$0.15/1M input tokens, ~$0.60/1M output tokens
- Response time: ~1-3 seconds
- Accuracy: Excellent for security analysis

**Prompt Engineering:**

```
System Prompt:
"You are an expert security engineer reviewing deployment readiness.
Be thorough but practical in your analysis."

User Prompt:
- Deployment context (branch, commit, repo)
- Security scan summary (tool, counts)
- Detailed findings (critical, high, medium, low)
- Decision criteria
- Output format specification
```

**Token Optimization:**
- Limit findings to top 5 per severity
- Summarize medium/low severity
- Use structured format for parsing
- Temperature: 0.3 for consistency

### Decision Criteria

**BLOCK_DEPLOYMENT:**
1. ANY critical issues (secrets detected)
2. High-severity security vulnerabilities
3. Policy violations requiring immediate fix
4. Regulatory compliance failures

**SAFE_TO_DEPLOY:**
1. No critical or high issues
2. Only low/informational findings
3. Medium severity with acceptable risk
4. All policies passing

---

## Infrastructure

### AWS Architecture

```
Internet
    ↓
Route 53 (optional)
    ↓
CloudFront Distribution
    ├── Cache behaviors
    ├── Security headers
    └── SSL/TLS certificate
    ↓
S3 Bucket (Origin)
    ├── Static website files
    ├── Versioning enabled
    ├── Encryption at rest
    └── Access logging
    ↓
S3 Logs Bucket
    └── Access logs
```

### Terraform State Management

**Local State (for demo):**
- `terraform.tfstate` - Current state
- Stored locally (not committed)

**Remote State (production):**
- S3 backend with locking
- DynamoDB for state locking
- Versioning enabled
- Encryption at rest

---

## Scalability & Performance

### Current Capacity

| Component | Limit | Notes |
|-----------|-------|-------|
| GitHub Actions | 2,000 min/month | Free tier |
| S3 Storage | 5 GB | Free tier |
| CloudFront Transfer | 1 TB/month | Free tier |
| OpenAI API | Rate limited | ~3 req/min for free |

### Performance Metrics

**Workflow Execution:**
- Security scan: ~30-60 seconds
- AI analysis: ~5-10 seconds
- AWS deployment: ~10-20 seconds
- **Total: ~2-3 minutes**

**Optimization Opportunities:**
1. Cache security scan results
2. Parallel tool execution (already done)
3. Incremental scans (file changes only)
4. CDN caching for static assets

### Scaling Considerations

**For Production:**
1. **Multiple environments**
   - Dev, staging, production workflows
   - Environment-specific secrets
   - Separate AWS accounts

2. **High-volume deployments**
   - GitHub Actions self-hosted runners
   - AWS Organizations for multi-account
   - OpenAI API tier upgrade

3. **Global distribution**
   - Multi-region S3 replication
   - CloudFront edge locations
   - Route 53 for DNS routing

---

## Technology Stack Summary

| Layer | Technology | Purpose |
|-------|-----------|---------|
| **Source Control** | GitHub | Code repository |
| **CI/CD** | GitHub Actions | Workflow orchestration |
| **Secret Detection** | Gitleaks | Find hardcoded secrets |
| **Code Analysis** | Semgrep | Security vulnerabilities |
| **Policy Validation** | OPA/Conftest | Infrastructure policies |
| **AI Decision** | OpenAI GPT-4o-mini | Intelligent analysis |
| **Infrastructure** | Terraform | AWS resource management |
| **Hosting** | AWS S3 | Static website storage |
| **CDN** | AWS CloudFront | Global content delivery |
| **Monitoring** | CloudWatch | Logging and metrics |

---

## Design Decisions

### Why GitHub Actions?
- ✅ Integrated with GitHub
- ✅ Free tier sufficient for demos
- ✅ Easy secret management
- ✅ Rich marketplace of actions

### Why OpenAI GPT-4o-mini?
- ✅ Best cost/performance ratio
- ✅ Excellent reasoning capabilities
- ✅ Fast response times
- ✅ Reliable API

### Why S3 + CloudFront?
- ✅ Serverless (no maintenance)
- ✅ Highly scalable
- ✅ Cost-effective for static sites
- ✅ Global CDN included

### Why Terraform?
- ✅ Infrastructure as code
- ✅ State management
- ✅ Plan before apply
- ✅ Wide AWS support

---

**Built with ❤️ for secure, intelligent deployments**

