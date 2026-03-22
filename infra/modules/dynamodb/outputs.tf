output "users_table_name" {
  value = aws_dynamodb_table.users.name
}

output "users_table_arn" {
  value = aws_dynamodb_table.users.arn
}

output "transactions_table_name" {
  value = aws_dynamodb_table.transactions.name
}

output "transactions_table_arn" {
  value = aws_dynamodb_table.transactions.arn
}

output "files_table_name" {
  value = aws_dynamodb_table.files.name
}

output "files_table_arn" {
  value = aws_dynamodb_table.files.arn
}
