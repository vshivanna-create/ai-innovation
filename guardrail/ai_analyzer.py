#!/usr/bin/env python3
"""
AI-Powered Security Guardrail Analyzer
Aggregates security scan results and uses OpenAI to make intelligent deployment decisions.
"""

import json
import os
import sys
from typing import Dict, List, Any, Tuple
from pathlib import Path
import openai
from datetime import datetime


class SecurityAnalyzer:
    """Analyzes security scan results using AI to make deployment decisions."""

    def __init__(self, api_key: str, model: str = "gpt-4o-mini"):
        """
        Initialize the analyzer with OpenAI credentials.

        Args:
            api_key: OpenAI API key
            model: Model to use (default: gpt-4o-mini for cost efficiency)
        """
        self.client = openai.OpenAI(api_key=api_key)
        self.model = model
        self.scan_results = {}

    def load_scan_results(self, results_dir: str) -> None:
        """
        Load all security scan results from JSON files.

        Args:
            results_dir: Directory containing scan result files
        """
        results_path = Path(results_dir)

        # Load Gitleaks results
        gitleaks_file = results_path / "gitleaks-report.json"
        if gitleaks_file.exists():
            with open(gitleaks_file) as f:
                content = f.read().strip()
                self.scan_results['gitleaks'] = json.loads(content) if content else []
        else:
            self.scan_results['gitleaks'] = []

        # Load Semgrep results
        semgrep_file = results_path / "semgrep-report.json"
        if semgrep_file.exists():
            with open(semgrep_file) as f:
                content = f.read().strip()
                self.scan_results['semgrep'] = json.loads(content) if content else {"results": []}
        else:
            self.scan_results['semgrep'] = {"results": []}

        # Load OPA/Conftest results
        opa_file = results_path / "opa-report.json"
        if opa_file.exists():
            with open(opa_file) as f:
                content = f.read().strip()
                self.scan_results['opa'] = json.loads(content) if content else []
        else:
            self.scan_results['opa'] = []

    def aggregate_findings(self) -> Dict[str, Any]:
        """
        Aggregate and structure findings from all security tools.

        Returns:
            Dictionary with aggregated findings and statistics
        """
        findings = {
            'critical': [],
            'high': [],
            'medium': [],
            'low': [],
            'info': [],
            'statistics': {
                'total_issues': 0,
                'critical_count': 0,
                'high_count': 0,
                'medium_count': 0,
                'low_count': 0,
                'tools_run': []
            }
        }

        # Process Gitleaks results (secrets)
        gitleaks_results = self.scan_results.get('gitleaks', [])
        if gitleaks_results:
            findings['statistics']['tools_run'].append('Gitleaks')
            for finding in gitleaks_results:
                issue = {
                    'tool': 'Gitleaks',
                    'type': 'Secret Detection',
                    'description': finding.get('Description', 'Secret detected'),
                    'file': finding.get('File', 'unknown'),
                    'line': finding.get('StartLine', 'unknown'),
                    'severity': 'critical',
                    'rule': finding.get('RuleID', 'unknown')
                }
                findings['critical'].append(issue)
                findings['statistics']['critical_count'] += 1

        # Process Semgrep results (code security)
        semgrep_results = self.scan_results.get('semgrep', {}).get('results', [])
        if semgrep_results:
            findings['statistics']['tools_run'].append('Semgrep')
            for finding in semgrep_results:
                severity_map = {
                    'ERROR': 'high',
                    'WARNING': 'medium',
                    'INFO': 'low'
                }
                severity = severity_map.get(finding.get('extra', {}).get('severity', 'INFO'), 'low')

                issue = {
                    'tool': 'Semgrep',
                    'type': 'Code Security',
                    'description': finding.get('extra', {}).get('message', 'Security issue detected'),
                    'file': finding.get('path', 'unknown'),
                    'line': finding.get('start', {}).get('line', 'unknown'),
                    'severity': severity,
                    'rule': finding.get('check_id', 'unknown')
                }
                findings[severity].append(issue)
                findings['statistics'][f'{severity}_count'] += 1

        # Process OPA/Conftest results (policy violations)
        opa_results = self.scan_results.get('opa', [])
        if opa_results:
            findings['statistics']['tools_run'].append('OPA/Conftest')
            for result in opa_results:
                # Handle both array of failures and structured results
                failures = result.get('failures', []) if isinstance(result, dict) else []
                warnings = result.get('warnings', []) if isinstance(result, dict) else []

                for failure in failures:
                    issue = {
                        'tool': 'OPA/Conftest',
                        'type': 'Policy Violation',
                        'description': failure.get('msg', 'Policy violation detected'),
                        'file': result.get('filename', 'infrastructure'),
                        'severity': 'high',
                        'rule': 'policy-enforcement'
                    }
                    findings['high'].append(issue)
                    findings['statistics']['high_count'] += 1

                for warning in warnings:
                    issue = {
                        'tool': 'OPA/Conftest',
                        'type': 'Policy Warning',
                        'description': warning.get('msg', 'Policy warning'),
                        'file': result.get('filename', 'infrastructure'),
                        'severity': 'medium',
                        'rule': 'policy-warning'
                    }
                    findings['medium'].append(issue)
                    findings['statistics']['medium_count'] += 1

        # Calculate total issues
        findings['statistics']['total_issues'] = (
            findings['statistics']['critical_count'] +
            findings['statistics']['high_count'] +
            findings['statistics']['medium_count'] +
            findings['statistics']['low_count']
        )

        if not findings['statistics']['tools_run']:
            findings['statistics']['tools_run'] = ['All security tools']

        return findings

    def create_ai_prompt(self, findings: Dict[str, Any], context: Dict[str, str]) -> str:
        """
        Create an intelligent prompt for the AI to analyze findings.

        Args:
            findings: Aggregated security findings
            context: Deployment context (branch, commit, etc.)

        Returns:
            Formatted prompt string
        """
        stats = findings['statistics']

        prompt = f"""You are a security deployment reviewer for a CI/CD pipeline. Analyze the following security scan results and make a deployment decision.

DEPLOYMENT CONTEXT:
- Branch: {context.get('branch', 'main')}
- Commit: {context.get('commit', 'unknown')}[:8]
- Repository: {context.get('repository', 'ai-innovation')}

SECURITY SCAN SUMMARY:
- Tools Run: {', '.join(stats['tools_run'])}
- Total Issues: {stats['total_issues']}
- Critical: {stats['critical_count']}
- High: {stats['high_count']}
- Medium: {stats['medium_count']}
- Low: {stats['low_count']}

DETAILED FINDINGS:
"""

        # Add critical findings
        if findings['critical']:
            prompt += "\nCRITICAL ISSUES:\n"
            for issue in findings['critical'][:5]:  # Limit to 5 for token efficiency
                prompt += f"- [{issue['tool']}] {issue['description']}\n"
                prompt += f"  File: {issue['file']}, Line: {issue.get('line', 'N/A')}\n"

        # Add high findings
        if findings['high']:
            prompt += "\nHIGH SEVERITY ISSUES:\n"
            for issue in findings['high'][:5]:
                prompt += f"- [{issue['tool']}] {issue['description']}\n"
                prompt += f"  File: {issue['file']}\n"

        # Add medium findings summary
        if findings['medium']:
            prompt += f"\nMEDIUM SEVERITY: {len(findings['medium'])} issues found\n"
            if findings['medium']:
                prompt += f"Example: {findings['medium'][0]['description']}\n"

        # Add low findings summary
        if findings['low']:
            prompt += f"\nLOW SEVERITY: {len(findings['low'])} issues found\n"

        prompt += """
DECISION CRITERIA:
1. BLOCK deployment if there are ANY critical issues (secrets, credentials)
2. BLOCK deployment if there are high-severity issues that pose immediate security risks
3. APPROVE WITH WARNINGS if only medium/low severity issues exist
4. APPROVE if no significant issues are found

Provide your analysis in this EXACT format:

DECISION: [SAFE_TO_DEPLOY or BLOCK_DEPLOYMENT]

REASONING:
[2-3 sentences explaining your decision based on the findings]

RECOMMENDATIONS:
[Bullet points with specific remediation steps if blocking, or best practices if approving]

RISK LEVEL: [NONE, LOW, MEDIUM, HIGH, CRITICAL]
"""

        return prompt

    def analyze_with_ai(self, findings: Dict[str, Any], context: Dict[str, str]) -> Dict[str, Any]:
        """
        Use OpenAI to analyze findings and make deployment decision.

        Args:
            findings: Aggregated security findings
            context: Deployment context

        Returns:
            Dictionary with decision, reasoning, and recommendations
        """
        prompt = self.create_ai_prompt(findings, context)

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert security engineer reviewing deployment readiness. Be thorough but practical in your analysis."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.3,  # Lower temperature for more consistent decisions
                max_tokens=500
            )

            ai_response = response.choices[0].message.content

            # Parse the AI response
            decision = "BLOCK_DEPLOYMENT"
            if "SAFE_TO_DEPLOY" in ai_response:
                decision = "SAFE_TO_DEPLOY"

            # Extract sections
            reasoning = self._extract_section(ai_response, "REASONING:")
            recommendations = self._extract_section(ai_response, "RECOMMENDATIONS:")
            risk_level = self._extract_section(ai_response, "RISK LEVEL:")

            return {
                'decision': decision,
                'reasoning': reasoning.strip(),
                'recommendations': recommendations.strip(),
                'risk_level': risk_level.strip().split('\n')[0] if risk_level else 'UNKNOWN',
                'full_response': ai_response,
                'model_used': self.model,
                'timestamp': datetime.utcnow().isoformat()
            }

        except Exception as e:
            print(f"Error calling OpenAI API: {e}", file=sys.stderr)
            # Fallback to rule-based decision
            return self._fallback_decision(findings)

    def _extract_section(self, text: str, section_marker: str) -> str:
        """Extract a section from AI response."""
        if section_marker not in text:
            return ""

        start = text.find(section_marker) + len(section_marker)
        end = text.find("\n\n", start)
        if end == -1:
            # Try finding the next section marker
            for marker in ["REASONING:", "RECOMMENDATIONS:", "RISK LEVEL:"]:
                if marker != section_marker and marker in text[start:]:
                    end = text.find(marker, start)
                    break
            if end == -1:
                end = len(text)

        return text[start:end].strip()

    def _fallback_decision(self, findings: Dict[str, Any]) -> Dict[str, Any]:
        """Fallback rule-based decision if AI fails."""
        stats = findings['statistics']

        if stats['critical_count'] > 0:
            decision = "BLOCK_DEPLOYMENT"
            reasoning = f"Found {stats['critical_count']} critical security issues including potential secrets or credentials."
            risk_level = "CRITICAL"
        elif stats['high_count'] > 0:
            decision = "BLOCK_DEPLOYMENT"
            reasoning = f"Found {stats['high_count']} high-severity security issues that must be addressed."
            risk_level = "HIGH"
        elif stats['medium_count'] > 3:
            decision = "BLOCK_DEPLOYMENT"
            reasoning = f"Found {stats['medium_count']} medium-severity issues requiring attention."
            risk_level = "MEDIUM"
        else:
            decision = "SAFE_TO_DEPLOY"
            reasoning = "No critical or high-severity issues found. Deployment approved."
            risk_level = "LOW"

        return {
            'decision': decision,
            'reasoning': reasoning,
            'recommendations': 'Review and fix identified issues before next deployment.',
            'risk_level': risk_level,
            'full_response': 'Fallback rule-based decision (AI unavailable)',
            'model_used': 'fallback',
            'timestamp': datetime.utcnow().isoformat()
        }

    def generate_report(self, findings: Dict[str, Any], ai_decision: Dict[str, Any]) -> str:
        """
        Generate a markdown report for GitHub Actions.

        Args:
            findings: Aggregated security findings
            ai_decision: AI analysis results

        Returns:
            Markdown formatted report
        """
        stats = findings['statistics']
        decision_emoji = "✅" if ai_decision['decision'] == "SAFE_TO_DEPLOY" else "❌"

        report = f"""# {decision_emoji} SecureDeploy Guardrail Report

## Decision: {ai_decision['decision'].replace('_', ' ')}

**Risk Level:** {ai_decision['risk_level']}
**Analysis Time:** {ai_decision['timestamp']}
**AI Model:** {ai_decision['model_used']}

---

## 🤖 AI Analysis

### Reasoning
{ai_decision['reasoning']}

### Recommendations
{ai_decision['recommendations']}

---

## 📊 Security Scan Summary

| Severity | Count |
|----------|-------|
| 🔴 Critical | {stats['critical_count']} |
| 🟠 High | {stats['high_count']} |
| 🟡 Medium | {stats['medium_count']} |
| 🔵 Low | {stats['low_count']} |
| **Total** | **{stats['total_issues']}** |

**Tools Run:** {', '.join(stats['tools_run'])}

---

## 🔍 Detailed Findings

"""

        # Add critical findings
        if findings['critical']:
            report += "### 🔴 Critical Issues\n\n"
            for issue in findings['critical']:
                report += f"- **[{issue['tool']}]** {issue['description']}\n"
                report += f"  - File: `{issue['file']}`\n"
                report += f"  - Line: {issue.get('line', 'N/A')}\n\n"

        # Add high findings
        if findings['high']:
            report += "### 🟠 High Severity Issues\n\n"
            for issue in findings['high']:
                report += f"- **[{issue['tool']}]** {issue['description']}\n"
                report += f"  - File: `{issue['file']}`\n\n"

        # Add medium findings
        if findings['medium']:
            report += f"### 🟡 Medium Severity Issues ({len(findings['medium'])})\n\n"
            for issue in findings['medium'][:3]:  # Show first 3
                report += f"- **[{issue['tool']}]** {issue['description']}\n"
            if len(findings['medium']) > 3:
                report += f"\n*...and {len(findings['medium']) - 3} more*\n\n"

        # Add summary
        report += "\n---\n\n"
        if ai_decision['decision'] == "SAFE_TO_DEPLOY":
            report += "✅ **Deployment approved by AI Guardrail**\n"
        else:
            report += "❌ **Deployment blocked by AI Guardrail**\n"
            report += "\nPlease address the identified issues and push again.\n"

        return report

    def set_github_output(self, key: str, value: str) -> None:
        """Set GitHub Actions output variable."""
        github_output = os.getenv('GITHUB_OUTPUT')
        if github_output:
            with open(github_output, 'a') as f:
                f.write(f"{key}={value}\n")
        else:
            print(f"::set-output name={key}::{value}")


def main():
    """Main execution function."""
    # Get configuration from environment
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        print("ERROR: OPENAI_API_KEY environment variable not set", file=sys.stderr)
        sys.exit(1)

    results_dir = sys.argv[1] if len(sys.argv) > 1 else 'scan-results'

    # Initialize analyzer
    analyzer = SecurityAnalyzer(api_key)

    # Load scan results
    print(f"Loading scan results from {results_dir}...")
    analyzer.load_scan_results(results_dir)

    # Aggregate findings
    print("Aggregating security findings...")
    findings = analyzer.aggregate_findings()

    # Debug: Print what was found
    print(f"\n=== SCAN RESULTS DEBUG ===")
    print(f"Gitleaks findings: {len(analyzer.scan_results.get('gitleaks', []))}")
    print(f"Semgrep findings: {len(analyzer.scan_results.get('semgrep', {}).get('results', []))}")
    print(f"OPA findings: {len(analyzer.scan_results.get('opa', []))}")
    print(f"Total issues aggregated: {findings['statistics']['total_issues']}")
    print(f"Critical: {findings['statistics']['critical_count']}")
    print(f"High: {findings['statistics']['high_count']}")
    print(f"=== END DEBUG ===\n")

    # Get deployment context
    context = {
        'branch': os.getenv('GITHUB_REF_NAME', 'main'),
        'commit': os.getenv('GITHUB_SHA', 'unknown'),
        'repository': os.getenv('GITHUB_REPOSITORY', 'ai-innovation')
    }

    # Analyze with AI
    print("Analyzing with AI...")
    ai_decision = analyzer.analyze_with_ai(findings, context)

    # Generate report
    print("Generating report...")
    report = analyzer.generate_report(findings, ai_decision)

    # Save report
    report_file = Path(results_dir) / 'guardrail-report.md'
    report_file.write_text(report)
    print(f"Report saved to {report_file}")

    # Set GitHub Actions outputs
    analyzer.set_github_output('decision', ai_decision['decision'])
    analyzer.set_github_output('risk_level', ai_decision['risk_level'])
    analyzer.set_github_output('report_file', str(report_file))

    # Print summary
    print("\n" + "="*60)
    print(f"DECISION: {ai_decision['decision']}")
    print(f"RISK LEVEL: {ai_decision['risk_level']}")
    print(f"ISSUES FOUND: {findings['statistics']['total_issues']}")
    print("="*60 + "\n")

    # Exit with appropriate code
    if ai_decision['decision'] == "BLOCK_DEPLOYMENT":
        print(report)
        sys.exit(1)
    else:
        print(report)
        sys.exit(0)


if __name__ == '__main__':
    main()

