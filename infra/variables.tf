variable "aws_region" {
  description = "AWS region for deployment"
  type        = string
  default     = "us-east-1"
}

variable "environment" {
  description = "Deployment environment"
  type        = string
  default     = "production"
}

variable "project_name" {
  description = "Project name used for resource naming"
  type        = string
  default     = "fintrack"
}

variable "domain_name" {
  description = "Custom domain name (optional)"
  type        = string
  default     = ""
}

variable "github_org" {
  description = "GitHub organization or user"
  type        = string
  default     = "geekyrbhalala"
}

variable "github_repo" {
  description = "GitHub repository name"
  type        = string
  default     = "rb-portfolio"
}
