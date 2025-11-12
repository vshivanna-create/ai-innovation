// Test File for Semgrep Code Security Analysis
// This file contains intentional security issues for testing
// DO NOT use these patterns in production!

// Issue 1: Using eval (Code Injection Risk)
function executeUserCode(userInput) {
    eval(userInput); // DANGEROUS: Semgrep should flag this
}

// Issue 2: Direct innerHTML usage (XSS Risk)
function displayUserMessage(message) {
    document.getElementById('output').innerHTML = message; // XSS vulnerability
}

// Issue 3: Insecure random number generation
function generateToken() {
    return Math.random().toString(36).substring(7); // Not cryptographically secure
}

// Issue 4: document.write usage
function showAd(adContent) {
    document.write(adContent); // Can lead to XSS
}

// Issue 5: Hardcoded password (combined with secret detection)
const databaseConfig = {
    host: 'localhost',
    user: 'admin',
    password: 'admin123', // Hardcoded password
    database: 'myapp'
};

// Issue 6: SQL Injection vulnerability pattern
function getUserData(userId) {
    const query = "SELECT * FROM users WHERE id = " + userId; // SQL injection risk
    // This would be flagged if we had SQL execution
    return query;
}

// To test:
// 1. Remove ".example" from filename
// 2. Commit and push
// 3. Watch Semgrep detect issues
// 4. See AI analyze severity and decide

// SAFE ALTERNATIVES (for reference):
// - Use Function() constructor instead of eval (still risky)
// - Use textContent or DOMPurify for user content
// - Use crypto.getRandomValues() for secure random
// - Use DOM manipulation instead of document.write
// - Use environment variables for passwords
// - Use parameterized queries for SQL

