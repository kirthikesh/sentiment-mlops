terraform {
  required_version = ">= 1.5"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = var.aws_region
  # Credentials are NOT set here. Terraform picks them up from the standard
  # AWS credential chain: `aws configure` (~/.aws/credentials), or the
  # AWS_ACCESS_KEY_ID / AWS_SECRET_ACCESS_KEY env vars. Never hardcode keys
  # in this repo.
}

data "aws_availability_zones" "available" {
  state = "available"
}
