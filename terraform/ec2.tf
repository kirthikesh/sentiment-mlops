data "aws_ami" "ubuntu" {
  most_recent = true
  owners      = ["099720109477"] # Canonical

  filter {
    name   = "name"
    values = ["ubuntu/images/hvm-ssd/ubuntu-jammy-22.04-amd64-server-*"]
  }
}

resource "aws_instance" "node" {
  ami                         = data.aws_ami.ubuntu.id
  instance_type               = var.instance_type
  subnet_id                   = aws_subnet.public.id
  vpc_security_group_ids      = [aws_security_group.node.id]
  key_name                    = aws_key_pair.default.key_name
  associate_public_ip_address = true
  user_data                   = file("${path.module}/cloud-init.yaml")

  root_block_device {
    volume_size = 8 # gp3, within the free-tier 30GB allowance
    volume_type = "gp3"
  }

  tags = {
    Name    = var.node_name
    Project = "sentiment-mlops"
  }
}
