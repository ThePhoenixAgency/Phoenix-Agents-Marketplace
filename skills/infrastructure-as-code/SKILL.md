---
name: infrastructure-as-code
description: Terraform, IaC patterns, state management
---
# Infrastructure as Code
## Terraform
```hcl
resource "aws_instance" "app" {
  ami           = "ami-0c55b159cbfafe1f0"
  instance_type = "t3.medium"
  tags = { Name = "app-server", Environment = "production" }
}
resource "aws_security_group" "app" {
  name = "app-sg"
  ingress {
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
}
```
## State Management
- Remote state (S3 + DynamoDB lock)
- State locking pour eviter les conflits
- Imports pour les ressources existantes
## Modules
```hcl
module "vpc" {
  source = "./modules/vpc"
  cidr   = "10.0.0.0/16"
  azs    = ["eu-west-1a", "eu-west-1b"]
}
```
## Checklist
- [ ] Remote state configure
- [ ] Plan avant apply
- [ ] Modules reutilisables
- [ ] Variables et outputs documentes
- [ ] Pas de secrets en dur
