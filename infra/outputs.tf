output "frontend_url" {
  description = "CloudFront distribution URL"
  value       = module.cloudfront.distribution_url
}

output "api_url" {
  description = "API Gateway URL"
  value       = module.api_gateway.api_url
}

output "frontend_bucket" {
  description = "S3 bucket for frontend"
  value       = module.s3.frontend_bucket_name
}

output "cloudfront_distribution_id" {
  description = "CloudFront distribution ID (for cache invalidation)"
  value       = module.cloudfront.distribution_id
}
