variable "aws_region" {
  description = "AWS region. eu-west-1 (Ireland) keeps latency low and matches most free-tier setups."
  type        = string
  default     = "eu-west-1"
}

variable "instance_type" {
  description = "EC2 instance type. t3.micro is free-tier eligible (750 hrs/month for 12 months)."
  type        = string
  default     = "t3.micro"
}

variable "node_name" {
  type    = string
  default = "sentiment-mlops-node"
}

variable "ssh_public_key_path" {
  description = "Path to your local SSH public key, imported into AWS and installed on the instance."
  type        = string
  default     = "~/.ssh/id_rsa.pub"
}

variable "allowed_ssh_cidrs" {
  description = "CIDRs allowed to reach SSH (22) and the k3s API (6443). Restrict to your own IP for anything beyond a short demo."
  type        = list(string)
  default     = ["0.0.0.0/0"]
}

variable "vpc_cidr" {
  type    = string
  default = "10.0.0.0/16"
}

variable "public_subnet_cidr" {
  type    = string
  default = "10.0.1.0/24"
}
