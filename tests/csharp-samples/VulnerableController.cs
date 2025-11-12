using Microsoft.AspNetCore.Mvc;
using System.Data.SqlClient;

namespace SecureDeployTest.Controllers
{
    /// <summary>
    /// SAMPLE C# CODE FOR TESTING SECURITY GUARDRAIL
    /// This file contains INTENTIONAL vulnerabilities for demo purposes
    /// DO NOT use this code in production!
    /// </summary>
    [ApiController]
    [Route("api/[controller]")]
    public class VulnerableController : ControllerBase
    {
        // ❌ VULNERABILITY 1: SQL Injection
        [HttpGet("user/{userId}")]
        public IActionResult GetUserUnsafe(string userId)
        {
            // BAD: Direct string concatenation - SQL injection risk
            string sql = $"SELECT * FROM Users WHERE Id = '{userId}'";

            using (var connection = new SqlConnection("connection-string"))
            using (var command = new SqlCommand(sql, connection))
            {
                // This will be detected by Semgrep and blocked by AI Guardrail
                connection.Open();
                var reader = command.ExecuteReader();
                return Ok("User data");
            }
        }

        // ❌ VULNERABILITY 2: Hardcoded Secret
        [HttpGet("api-key")]
        public IActionResult GetApiKey()
        {
            // BAD: Hardcoded API key - will be caught by Gitleaks
            string apiKey = "sk-proj-1234567890abcdefghijklmnopqrstuvwxyz123456";
            return Ok(new { key = apiKey });
        }

        // ❌ VULNERABILITY 3: Command Injection
        [HttpPost("execute")]
        public IActionResult ExecuteCommand([FromBody] string command)
        {
            // BAD: Unsanitized command execution
            var process = System.Diagnostics.Process.Start("cmd.exe", $"/c {command}");
            return Ok("Command executed");
        }

        // ✅ SECURE: Parameterized Query (Good Example)
        [HttpGet("user-safe/{userId}")]
        public IActionResult GetUserSafe(string userId)
        {
            // GOOD: Using parameterized query
            string sql = "SELECT * FROM Users WHERE Id = @UserId";

            using (var connection = new SqlConnection("connection-string"))
            using (var command = new SqlCommand(sql, connection))
            {
                command.Parameters.AddWithValue("@UserId", userId);
                connection.Open();
                var reader = command.ExecuteReader();
                return Ok("User data");
            }
        }
    }
}

