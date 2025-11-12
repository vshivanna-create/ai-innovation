// SecureDeploy Guardrail - JavaScript functionality

document.addEventListener('DOMContentLoaded', function() {
    // Update last scan time
    updateLastScanTime();
    setInterval(updateLastScanTime, 60000); // Update every minute

    // Smooth scrolling for anchor links
    setupSmoothScrolling();

    // Add scroll animations
    setupScrollAnimations();
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

// Console message for developers
console.log('%c🛡️ SecureDeploy Guardrail', 'font-size: 20px; font-weight: bold; color: #2563eb;');
console.log('%cAI-Powered Security for Your Deployments', 'font-size: 14px; color: #10b981;');
console.log('GitHub: https://github.com/vshivanna-create/ai-innovation');

