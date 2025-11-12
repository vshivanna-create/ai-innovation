# Test File for OPA/Conftest Policy Validation
# This infrastructure configuration intentionally violates security policies
# DO NOT deploy this configuration!

# Violation 1: S3 bucket without encryption
resource "aws_s3_bucket" "insecure_bucket" {
  bucket = "test-insecure-bucket-example"

  # Missing: server_side_encryption_configuration
  # OPA policy should catch this
}

# Violation 2: Public read/write access
resource "aws_s3_bucket_acl" "public_access" {
  bucket = aws_s3_bucket.insecure_bucket.id
  acl    = "public-read-write"  # DANGEROUS: Public write access

  # This violates the policy against public access
}

# Violation 3: No versioning
# The bucket above doesn't have versioning enabled
# Policy requires versioning for data protection

# Violation 4: No logging
# The bucket above doesn't have access logging
# Policy requires logging for audit trails

# Violation 5: CloudFront without HTTPS enforcement
resource "aws_cloudfront_distribution" "insecure_cdn" {
  enabled = true

  origin {
    domain_name = aws_s3_bucket.insecure_bucket.bucket_regional_domain_name
    origin_id   = "insecure-origin"
  }

  default_cache_behavior {
    allowed_methods        = ["GET", "HEAD"]
    cached_methods         = ["GET", "HEAD"]
    target_origin_id       = "insecure-origin"
    viewer_protocol_policy = "allow-all"  # Should be "redirect-to-https"

    forwarded_values {
      query_string = false
      cookies {
        forward = "none"
      }
    }
  }

  restrictions {
    geo_restriction {
      restriction_type = "none"
    }
  }

  viewer_certificate {
    cloudfront_default_certificate = true
  }

  # Missing: Security headers configuration
}

# To test:
# 1. Remove ".example" from filename
# 2. Commit and push
# 3. Watch OPA/Conftest detect violations
# 4. See AI explain policy violations and block deployment

# COMPLIANT ALTERNATIVES:
# - Add aws_s3_bucket_server_side_encryption_configuration
# - Set bucket ACL to "private" or use bucket policies
# - Add aws_s3_bucket_versioning with enabled = true
# - Add aws_s3_bucket_logging configuration
# - Set viewer_protocol_policy = "redirect-to-https"
# - Add custom headers for security (HSTS, X-Frame-Options, etc.)

