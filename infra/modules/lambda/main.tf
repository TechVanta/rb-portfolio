resource "aws_lambda_function" "api" {
  function_name = "${var.project_name}-api-${var.environment}"
  role          = var.lambda_role_arn
  handler       = "lambda_handler.handler"
  runtime       = "python3.12"
  timeout       = 60
  memory_size   = 512

  # Placeholder — CI/CD will deploy actual code
  filename         = data.archive_file.placeholder.output_path
  source_code_hash = data.archive_file.placeholder.output_base64sha256

  environment {
    variables = {
      APP_NAME           = var.project_name
      DEBUG              = "false"
      LOG_LEVEL          = "INFO"
      ALLOWED_ORIGINS    = "*"
      JWT_SECRET         = var.jwt_secret
      AWS_REGION_NAME    = var.aws_region
      S3_BUCKET          = var.uploads_bucket
      USERS_TABLE        = var.users_table
      TRANSACTIONS_TABLE = var.transactions_table
      FILES_TABLE        = var.files_table
      LLM_PROVIDER       = var.llm_provider
      OPENAI_API_KEY     = var.openai_api_key
    }
  }

  lifecycle {
    ignore_changes = [filename, source_code_hash]
  }
}

# Placeholder zip for initial deploy
data "archive_file" "placeholder" {
  type        = "zip"
  output_path = "${path.module}/placeholder.zip"

  source {
    content  = "def handler(event, context): return {'statusCode': 200, 'body': 'placeholder'}"
    filename = "lambda_handler.py"
  }
}

resource "aws_lambda_function_url" "api" {
  function_name      = aws_lambda_function.api.function_name
  authorization_type = "NONE"

  cors {
    allow_credentials = true
    allow_headers     = ["*"]
    allow_methods     = ["*"]
    allow_origins     = ["*"]
    max_age           = 3600
  }
}
