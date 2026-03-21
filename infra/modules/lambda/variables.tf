variable "project_name" {
  type = string
}

variable "environment" {
  type = string
}

variable "lambda_role_arn" {
  type = string
}

variable "uploads_bucket" {
  type = string
}

variable "users_table" {
  type = string
}

variable "transactions_table" {
  type = string
}

variable "files_table" {
  type = string
}

variable "aws_region" {
  type = string
}
