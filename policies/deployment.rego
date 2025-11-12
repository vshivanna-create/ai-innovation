# OPA Policy for AWS S3 and CloudFront Deployment
# Enforces security best practices for infrastructure

package main

# Default deny
deny[msg] {
    input.kind == "aws_s3_bucket"
    not encryption_enabled
    msg := "S3 bucket must have server-side encryption enabled"
}

deny[msg] {
    input.kind == "aws_s3_bucket"
    not versioning_enabled
    msg := "S3 bucket must have versioning enabled for data protection"
}

deny[msg] {
    input.kind == "aws_s3_bucket"
    public_access_allowed
    msg := "S3 bucket must not allow public access unless explicitly required"
}

deny[msg] {
    input.kind == "aws_s3_bucket"
    not logging_enabled
    msg := "S3 bucket must have access logging enabled for audit trails"
}

deny[msg] {
    input.kind == "aws_cloudfront_distribution"
    not https_only
    msg := "CloudFront distribution must enforce HTTPS only"
}

deny[msg] {
    input.kind == "aws_cloudfront_distribution"
    not security_headers_configured
    msg := "CloudFront distribution must include security headers (HSTS, X-Frame-Options, etc.)"
}

# Helper rules
encryption_enabled {
    input.resource.server_side_encryption_configuration
}

versioning_enabled {
    input.resource.versioning[_].enabled == true
}

public_access_allowed {
    input.resource.acl == "public-read"
}

public_access_allowed {
    input.resource.acl == "public-read-write"
}

logging_enabled {
    input.resource.logging
}

https_only {
    input.resource.viewer_protocol_policy == "redirect-to-https"
}

https_only {
    input.resource.viewer_protocol_policy == "https-only"
}

security_headers_configured {
    input.resource.custom_headers
    has_security_header("X-Frame-Options")
    has_security_header("X-Content-Type-Options")
}

has_security_header(header_name) {
    input.resource.custom_headers[_].header_name == header_name
}

# Warning rules (non-blocking)
warn[msg] {
    input.kind == "aws_s3_bucket"
    not lifecycle_policy_configured
    msg := "Consider configuring lifecycle policies for cost optimization"
}

warn[msg] {
    input.kind == "aws_cloudfront_distribution"
    not waf_enabled
    msg := "Consider enabling AWS WAF for additional protection"
}

lifecycle_policy_configured {
    input.resource.lifecycle_rule
}

waf_enabled {
    input.resource.web_acl_id
}

