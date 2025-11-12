using System;
using System.Security.Cryptography;
using System.Text;

namespace SecureDeployTest.Helpers
{
    /// <summary>
    /// SAMPLE C# CODE FOR TESTING SECURITY GUARDRAIL
    /// Contains weak cryptography examples - DO NOT use in production!
    /// </summary>
    public class CryptoHelper
    {
        // ❌ VULNERABILITY: Weak Hash Algorithm (MD5)
        public static string HashPasswordMD5(string password)
        {
            // BAD: MD5 is cryptographically broken
            using (MD5 md5 = MD5.Create())
            {
                byte[] inputBytes = Encoding.UTF8.GetBytes(password);
                byte[] hashBytes = md5.ComputeHash(inputBytes);
                return Convert.ToBase64String(hashBytes);
            }
        }

        // ❌ VULNERABILITY: Weak Hash Algorithm (SHA1)
        public static string HashPasswordSHA1(string password)
        {
            // BAD: SHA1 is deprecated
            using (SHA1 sha1 = SHA1.Create())
            {
                byte[] inputBytes = Encoding.UTF8.GetBytes(password);
                byte[] hashBytes = sha1.ComputeHash(inputBytes);
                return Convert.ToBase64String(hashBytes);
            }
        }

        // ❌ VULNERABILITY: Weak Random Number Generator
        public static string GenerateToken()
        {
            // BAD: System.Random is not cryptographically secure
            Random random = new Random();
            byte[] tokenBytes = new byte[32];
            random.NextBytes(tokenBytes);
            return Convert.ToBase64String(tokenBytes);
        }

        // ✅ SECURE: Strong Hash Algorithm (SHA256)
        public static string HashPasswordSecure(string password)
        {
            // GOOD: SHA256 is secure
            using (SHA256 sha256 = SHA256.Create())
            {
                byte[] inputBytes = Encoding.UTF8.GetBytes(password);
                byte[] hashBytes = sha256.ComputeHash(inputBytes);
                return Convert.ToBase64String(hashBytes);
            }
        }

        // ✅ SECURE: Cryptographically Secure Random
        public static string GenerateTokenSecure()
        {
            // GOOD: Using RNGCryptoServiceProvider
            using (RNGCryptoServiceProvider rng = new RNGCryptoServiceProvider())
            {
                byte[] tokenBytes = new byte[32];
                rng.GetBytes(tokenBytes);
                return Convert.ToBase64String(tokenBytes);
            }
        }
    }
}

