variable "project_name" {
  type = string
}

variable "environment" {
  type = string
}

variable "github_org" {
  type = string
}

variable "github_repo" {
  type = string
}

variable "uploads_bucket_arn" {
  type = string
}

variable "frontend_bucket_arn" {
  type = string
}

variable "users_table_arn" {
  type = string
}

variable "transactions_table_arn" {
  type = string
}

variable "files_table_arn" {
  type = string
}

variable "cloudfront_distribution_arn" {
  type = string
}
