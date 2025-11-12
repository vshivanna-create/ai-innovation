# Variables for SecureDeploy Guardrail Infrastructure

variable "aws_region" {
  description = "AWS region for resources"
  type        = string
  default     = "us-west-2"
}

variable "bucket_name" {
  description = "Name of the S3 bucket for website hosting"
  type        = string
  default     = "ai-innovation-securedeploy-website"
}

variable "project_name" {
  description = "Project name for resource naming"
  type        = string
  default     = "securedeploy-guardrail"
}

variable "environment" {
  description = "Environment name (dev, staging, prod)"
  type        = string
  default     = "demo"
}

variable "github_repository" {
  description = "GitHub repository in format owner/repo"
  type        = string
  default     = "vshivanna-create/ai-innovation"
}

variable "enable_cloudfront" {
  description = "Enable CloudFront distribution"
  type        = bool
  default     = true
}

variable "enable_waf" {
  description = "Enable AWS WAF for CloudFront"
  type        = bool
  default     = false
}

