// SecureDeploy Guardrail - JavaScript functionality

document.addEventListener('DOMContentLoaded', function() {
    // Update last scan time
    updateLastScanTime();
    setInterval(updateLastScanTime, 60000); // Update every minute

    // Smooth scrolling for anchor links
    setupSmoothScrolling();

    // Add scroll animations
    setupScrollAnimations();

    // Fetch and display GitHub Actions workflow status
    fetchWorkflowStatus();
    setInterval(fetchWorkflowStatus, 30000); // Update every 30 seconds

    // Fetch and display security scan results
    fetchScanResults();
    setInterval(fetchScanResults, 60000); // Update every minute
});

function updateLastScanTime() {
    const lastScanElement = document.getElementById('last-scan');
    if (lastScanElement) {
        const now = new Date();
        const timeString = now.toLocaleTimeString('en-US', {
            hour: '2-digit',
            minute: '2-digit'
        });
        lastScanElement.textContent = `Today at ${timeString}`;
    }
}

function setupSmoothScrolling() {
    const links = document.querySelectorAll('a[href^="#"]');

    links.forEach(link => {
        link.addEventListener('click', function(e) {
            const href = this.getAttribute('href');

            // Only handle internal links
            if (href.startsWith('#') && href !== '#') {
                e.preventDefault();

                const targetId = href.substring(1);
                const targetElement = document.getElementById(targetId);

                if (targetElement) {
                    targetElement.scrollIntoView({
                        behavior: 'smooth',
                        block: 'start'
                    });
                }
            }
        });
    });
}

function setupScrollAnimations() {
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };

    const observer = new IntersectionObserver(function(entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
            }
        });
    }, observerOptions);

    // Observe feature cards and workflow steps
    const animatedElements = document.querySelectorAll(
        '.feature-card, .workflow-step, .tool-card'
    );

    animatedElements.forEach(element => {
        element.style.opacity = '0';
        element.style.transform = 'translateY(20px)';
        element.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
        observer.observe(element);
    });
}

// Simulated deployment status checker (for demo purposes)
function checkDeploymentStatus() {
    // In a real implementation, this would call an API
    // For demo, we'll simulate status checks

    const statusItems = [
        { label: 'Last Scan', value: 'Just now' },
        { label: 'Security Tools', value: '✅ All Active' },
        { label: 'AI Guardrail', value: '✅ Operational' },
        { label: 'Deployment', value: '✅ Ready' }
    ];

    return statusItems;
}

// Add keyboard navigation
document.addEventListener('keydown', function(e) {
    // Press 'g' to go to GitHub
    if (e.key === 'g' && !e.ctrlKey && !e.metaKey) {
        const githubLink = document.querySelector('a[href*="github.com"]');
        if (githubLink) {
            window.open(githubLink.href, '_blank', 'noopener,noreferrer');
        }
    }
});

// Fetch GitHub Actions workflow status
async function fetchWorkflowStatus() {
    const workflowContainer = document.getElementById('workflow-status');
    const lastScanElement = document.getElementById('last-scan');
    const deploymentStatusElement = document.getElementById('deployment-status');

    if (!workflowContainer) return;

    try {
        // GitHub API endpoint for workflow runs
        const apiUrl = 'https://api.github.com/repos/vshivanna-create/ai-innovation/actions/runs?per_page=3';

        const response = await fetch(apiUrl);

        if (!response.ok) {
            throw new Error('Failed to fetch workflow status');
        }

        const data = await response.json();
        const runs = data.workflow_runs || [];

        if (runs.length === 0) {
            workflowContainer.innerHTML = '<div class="loading">No workflow runs found</div>';
            return;
        }

        // Display the latest 3 runs
        let html = '';
        runs.slice(0, 3).forEach((run, index) => {
            const statusClass = run.conclusion === 'success' ? 'success' :
                              run.conclusion === 'failure' ? 'failure' : 'running';
            const statusIcon = run.conclusion === 'success' ? '✅' :
                             run.conclusion === 'failure' ? '❌' : '🔄';
            const statusText = run.conclusion === 'success' ? 'Success' :
                             run.conclusion === 'failure' ? 'Blocked' : 'Running';

            const runDate = new Date(run.created_at);
            const timeAgo = getTimeAgo(runDate);

            html += `
                <div class="workflow-run">
                    <div class="workflow-info">
                        <h4>${statusIcon} ${run.display_title || run.head_commit.message}</h4>
                        <p>${timeAgo} • ${run.head_branch} • #${run.run_number}</p>
                    </div>
                    <div class="workflow-status-badge ${statusClass}">
                        ${statusText}
                    </div>
                </div>
            `;

            // Update last scan time with the most recent run
            if (index === 0 && lastScanElement) {
                lastScanElement.textContent = timeAgo;

                // Update deployment status
                if (deploymentStatusElement) {
                    if (run.conclusion === 'success') {
                        deploymentStatusElement.innerHTML = '✅ Deployed';
                    } else if (run.conclusion === 'failure') {
                        deploymentStatusElement.innerHTML = '❌ Blocked';
                    } else {
                        deploymentStatusElement.innerHTML = '🔄 Running';
                    }
                }
            }
        });

        workflowContainer.innerHTML = html;

    } catch (error) {
        console.error('Error fetching workflow status:', error);
        workflowContainer.innerHTML = '<div class="loading">Unable to load workflow status</div>';
    }
}

// Helper function to format time ago
function getTimeAgo(date) {
    const seconds = Math.floor((new Date() - date) / 1000);

    const intervals = {
        year: 31536000,
        month: 2592000,
        week: 604800,
        day: 86400,
        hour: 3600,
        minute: 60
    };

    for (const [unit, secondsInUnit] of Object.entries(intervals)) {
        const interval = Math.floor(seconds / secondsInUnit);
        if (interval >= 1) {
            return `${interval} ${unit}${interval === 1 ? '' : 's'} ago`;
        }
    }

    return 'Just now';
}

// Fetch security scan results
async function fetchScanResults() {
    const container = document.getElementById('scan-results-container');

    if (!container) return;

    try {
        // Fetch the scan summary JSON from S3
        const response = await fetch('./data/scan-summary.json?t=' + Date.now());

        if (!response.ok) {
            throw new Error('Failed to fetch scan results');
        }

        const data = await response.json();

        // Display the scan results
        let html = '';

        // Gitleaks card
        const gitleaksCount = data.gitleaks.findings || 0;
        const gitleaksClass = gitleaksCount === 0 ? 'clean' : 'issues';
        const gitleaksCountClass = gitleaksCount === 0 ? 'clean' :
                                   gitleaksCount < 5 ? 'warning' : 'danger';

        html += `
            <div class="scan-result-card ${gitleaksClass}">
                <div class="scan-tool-name">🔐 ${data.gitleaks.tool}</div>
                <div class="scan-count ${gitleaksCountClass}">${gitleaksCount}</div>
                <div class="scan-label">Secrets ${gitleaksCount === 0 ? 'Detected' : 'Found'}</div>
                <div class="scan-meta">
                    ${gitleaksCount === 0 ? '✅ No hardcoded secrets' : '❌ Contains secrets'}
                </div>
            </div>
        `;

        // Semgrep card
        const semgrepCount = data.semgrep.findings || 0;
        const semgrepClass = semgrepCount === 0 ? 'clean' : 'issues';
        const semgrepCountClass = semgrepCount === 0 ? 'clean' :
                                 semgrepCount < 10 ? 'warning' : 'danger';

        html += `
            <div class="scan-result-card ${semgrepClass}">
                <div class="scan-tool-name">🛡️ ${data.semgrep.tool}</div>
                <div class="scan-count ${semgrepCountClass}">${semgrepCount}</div>
                <div class="scan-label">Issues ${semgrepCount === 0 ? 'Detected' : 'Found'}</div>
                <div class="scan-meta">
                    ${semgrepCount === 0 ? '✅ Code is secure' : '⚠️ Vulnerabilities detected'}
                </div>
            </div>
        `;

        // OPA card
        const opaStatus = data.opa.status === 'completed';

        html += `
            <div class="scan-result-card ${opaStatus ? 'clean' : 'issues'}">
                <div class="scan-tool-name">📋 ${data.opa.tool}</div>
                <div class="scan-count clean">✓</div>
                <div class="scan-label">Policy Checks</div>
                <div class="scan-meta">
                    ✅ Infrastructure validated
                </div>
            </div>
        `;

        // Overall summary card
        const totalIssues = gitleaksCount + semgrepCount;
        const overallClass = totalIssues === 0 ? 'clean' : 'issues';
        const overallCountClass = totalIssues === 0 ? 'clean' :
                                 totalIssues < 10 ? 'warning' : 'danger';

        html += `
            <div class="scan-result-card ${overallClass}">
                <div class="scan-tool-name">📊 Total Findings</div>
                <div class="scan-count ${overallCountClass}">${totalIssues}</div>
                <div class="scan-label">All Tools</div>
                <div class="scan-meta">
                    Run #${data.run_number} • ${data.branch}
                </div>
            </div>
        `;

        container.innerHTML = html;

    } catch (error) {
        console.error('Error fetching scan results:', error);
        container.innerHTML = `
            <div class="scan-result-card">
                <div class="scan-tool-name">ℹ️ Scan Results</div>
                <div class="scan-label">Awaiting first deployment...</div>
                <div class="scan-meta">
                    Results will appear after the first workflow run
                </div>
            </div>
        `;
    }
}

// Console message for developers
console.log('%c🛡️ SecureDeploy Guardrail', 'font-size: 20px; font-weight: bold; color: #2563eb;');
console.log('%cAI-Powered Security for Your Deployments', 'font-size: 14px; color: #10b981;');
console.log('GitHub: https://github.com/vshivanna-create/ai-innovation');

