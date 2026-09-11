# terraform/ — sentiment-mlops cloud infra (AWS)

Provisions a small VPC (public subnet, internet gateway, route table), a
security group, and a single EC2 instance running k3s (lightweight
Kubernetes) that later phases (Jenkins, ArgoCD, the model-serving app)
deploy onto.

A single instance + k3s was chosen over EKS specifically to avoid EKS's
~$73/month control-plane fee. The instance itself uses the free-tier
`t3.micro` size; a 2GB swap file is added via cloud-init since 1GB of RAM
alone isn't enough headroom for k3s + the model.

## Prerequisites

- AWS account with an IAM user that has EC2/VPC permissions
- AWS CLI configured: `aws configure` (needs Access Key ID + Secret Access Key
  from IAM — never put these in this repo)
- Terraform: `brew install terraform`

## Setup

```bash
cp terraform.tfvars.example terraform.tfvars   # no secrets needed here
terraform init
terraform plan     # review — should show ~7 resources to create
terraform apply
```

Then pull the kubeconfig down (the exact command is in the `apply` output
as `fetch_kubeconfig_command`):

```bash
export KUBECONFIG=~/.kube/sentiment-mlops-config
kubectl get nodes   # should show one Ready node
```

## Teardown (avoid ongoing cost)

```bash
terraform destroy
```

## Remote state (optional, do later)

Currently uses local state (gitignored). To move to a remote backend:
create an S3 bucket + DynamoDB lock table, then add a `backend "s3" {}`
block in `main.tf`. Not required to get the cluster running.
