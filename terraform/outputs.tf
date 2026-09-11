output "instance_public_ip" {
  value       = aws_instance.node.public_ip
  description = "Public IP of the k3s node"
}

output "ssh_command" {
  value       = "ssh ubuntu@${aws_instance.node.public_ip}"
  description = "SSH into the node (default AMI user is 'ubuntu', not 'root')"
}

output "fetch_kubeconfig_command" {
  value       = "scp ubuntu@${aws_instance.node.public_ip}:/etc/rancher/k3s/k3s.yaml ~/.kube/sentiment-mlops-config && sed -i '' 's/127.0.0.1/${aws_instance.node.public_ip}/' ~/.kube/sentiment-mlops-config"
  description = "Run this after apply to pull the kubeconfig down and point it at the instance's public IP"
}
