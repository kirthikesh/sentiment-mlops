resource "aws_key_pair" "default" {
  key_name   = "sentiment-mlops-key"
  public_key = file(pathexpand(var.ssh_public_key_path))
}
