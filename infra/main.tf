module "s3" {
  source       = "./modules/s3"
  project_name = var.project_name
  environment  = var.environment
}

module "cloudfront" {
  source                 = "./modules/cloudfront"
  project_name           = var.project_name
  frontend_bucket_arn    = module.s3.frontend_bucket_arn
  frontend_bucket_domain = module.s3.frontend_bucket_regional_domain
  frontend_bucket_id     = module.s3.frontend_bucket_id
}

module "dynamodb" {
  source       = "./modules/dynamodb"
  project_name = var.project_name
  environment  = var.environment
}

module "iam" {
  source             = "./modules/iam"
  project_name       = var.project_name
  environment        = var.environment
  uploads_bucket_arn = module.s3.uploads_bucket_arn
  users_table_arn    = module.dynamodb.users_table_arn
  transactions_table_arn = module.dynamodb.transactions_table_arn
  files_table_arn    = module.dynamodb.files_table_arn
}

module "lambda" {
  source             = "./modules/lambda"
  project_name       = var.project_name
  environment        = var.environment
  lambda_role_arn    = module.iam.lambda_role_arn
  uploads_bucket     = module.s3.uploads_bucket_name
  users_table        = module.dynamodb.users_table_name
  transactions_table = module.dynamodb.transactions_table_name
  files_table        = module.dynamodb.files_table_name
  aws_region         = var.aws_region
}

module "api_gateway" {
  source              = "./modules/api_gateway"
  project_name        = var.project_name
  environment         = var.environment
  lambda_function_arn = module.lambda.function_arn
  lambda_invoke_arn   = module.lambda.invoke_arn
  aws_region          = var.aws_region
}
