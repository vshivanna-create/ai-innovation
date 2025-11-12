using System;
using System.IO;
using System.Runtime.Serialization.Formatters.Binary;
using Microsoft.AspNetCore.Mvc;

namespace SecureDeployTest.Examples
{
    /// <summary>
    /// SAMPLE C# CODE FOR TESTING SECURITY GUARDRAIL
    /// Contains XSS and deserialization vulnerabilities - DO NOT use in production!
    /// </summary>
    public class SecurityExamples : Controller
    {
        // ❌ VULNERABILITY: Cross-Site Scripting (XSS)
        public IActionResult RenderUserInput(string userInput)
        {
            // BAD: Html.Raw() with user input can lead to XSS
            ViewBag.UserContent = userInput;

            // In the view: @Html.Raw(ViewBag.UserContent)
            // This would allow script injection!
            return View();
        }

        // ❌ VULNERABILITY: Unsafe Deserialization
        public object DeserializeData(byte[] data)
        {
            // BAD: BinaryFormatter is unsafe and can lead to RCE
            using (MemoryStream ms = new MemoryStream(data))
            {
                BinaryFormatter formatter = new BinaryFormatter();
                return formatter.Deserialize(ms);
            }
        }

        // ❌ VULNERABILITY: Path Traversal
        public IActionResult DownloadFile(string filename)
        {
            // BAD: Unvalidated file path allows path traversal
            // User could pass: "../../etc/passwd"
            string filePath = $"/uploads/{filename}";
            return File.ReadAllText(filePath) as IActionResult;
        }

        // ❌ VULNERABILITY: SSL Certificate Validation Disabled
        public void DisableSSLValidation()
        {
            // BAD: This bypasses SSL certificate validation
            System.Net.ServicePointManager.ServerCertificateValidationCallback =
                (sender, certificate, chain, sslPolicyErrors) => true;
        }

        // ✅ SECURE: HTML Encoded Output
        public IActionResult RenderUserInputSafe(string userInput)
        {
            // GOOD: Using Html.Encode() prevents XSS
            ViewBag.UserContent = System.Web.HttpUtility.HtmlEncode(userInput);
            return View();
        }

        // ✅ SECURE: Safe Deserialization
        public object DeserializeDataSafe(string jsonData)
        {
            // GOOD: Using JSON deserialization (safer than BinaryFormatter)
            return System.Text.Json.JsonSerializer.Deserialize<object>(jsonData);
        }

        // ✅ SECURE: Path Validation
        public IActionResult DownloadFileSafe(string filename)
        {
            // GOOD: Validate and sanitize filename
            if (filename.Contains("..") || filename.Contains("/") || filename.Contains("\\"))
            {
                return BadRequest("Invalid filename");
            }

            string basePath = Path.GetFullPath("/uploads/");
            string filePath = Path.GetFullPath(Path.Combine(basePath, filename));

            // Ensure the resolved path is still within the base directory
            if (!filePath.StartsWith(basePath))
            {
                return BadRequest("Invalid path");
            }

            return PhysicalFile(filePath, "application/octet-stream");
        }
    }

    // ❌ VULNERABILITY: Missing CSRF Protection
    [ApiController]
    [Route("api/[controller]")]
    public class UnsafeFormController : ControllerBase
    {
        // BAD: POST action without CSRF protection
        [HttpPost("submit")]
        public IActionResult SubmitForm([FromBody] FormData data)
        {
            // Process form...
            return Ok("Form submitted");
        }
    }

    // ✅ SECURE: CSRF Protection Enabled
    [ApiController]
    [Route("api/[controller]")]
    public class SafeFormController : ControllerBase
    {
        // GOOD: CSRF token validation
        [HttpPost("submit")]
        [ValidateAntiForgeryToken]
        public IActionResult SubmitForm([FromBody] FormData data)
        {
            // Process form...
            return Ok("Form submitted");
        }
    }

    public class FormData
    {
        public string Name { get; set; }
        public string Email { get; set; }
    }
}

