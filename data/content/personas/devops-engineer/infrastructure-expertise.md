# Infrastructure as Code (IaC)

## Overview

Infrastructure as Code enables declarative infrastructure management through code, providing version control, repeatability, and automation for infrastructure provisioning, configuration management, and deployment across cloud and on-premises environments using tools like Terraform, Ansible, and CloudFormation.

## Terraform Infrastructure Management

### Modular Infrastructure Design

**Terraform Module Structure:**
```hcl
# modules/vpc/main.tf - Reusable VPC module
terraform {
  required_version = ">= 1.5"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

variable "name" {
  description = "Name prefix for resources"
  type        = string
}

variable "cidr" {
  description = "CIDR block for VPC"
  type        = string
  validation {
    condition     = can(cidrhost(var.cidr, 0))
    error_message = "CIDR must be a valid IPv4 CIDR block."
  }
}

variable "availability_zones" {
  description = "List of availability zones"
  type        = list(string)
  validation {
    condition     = length(var.availability_zones) >= 2
    error_message = "At least 2 availability zones must be specified for high availability."
  }
}

variable "enable_nat_gateway" {
  description = "Enable NAT Gateway for private subnets"
  type        = bool
  default     = true
}

variable "enable_dns_hostnames" {
  description = "Enable DNS hostnames in VPC"
  type        = bool
  default     = true
}

variable "tags" {
  description = "Tags to apply to all resources"
  type        = map(string)
  default     = {}
}

locals {
  public_subnet_cidrs  = [for i, az in var.availability_zones : cidrsubnet(var.cidr, 8, i)]
  private_subnet_cidrs = [for i, az in var.availability_zones : cidrsubnet(var.cidr, 8, i + 10)]
  
  common_tags = merge(
    var.tags,
    {
      ManagedBy = "terraform"
      Module    = "vpc"
    }
  )
}

# VPC
resource "aws_vpc" "main" {
  cidr_block           = var.cidr
  enable_dns_support   = true
  enable_dns_hostnames = var.enable_dns_hostnames

  tags = merge(local.common_tags, {
    Name = "${var.name}-vpc"
  })
}

# Internet Gateway
resource "aws_internet_gateway" "main" {
  vpc_id = aws_vpc.main.id

  tags = merge(local.common_tags, {
    Name = "${var.name}-igw"
  })
}

# Public Subnets
resource "aws_subnet" "public" {
  count = length(var.availability_zones)

  vpc_id                  = aws_vpc.main.id
  cidr_block              = local.public_subnet_cidrs[count.index]
  availability_zone       = var.availability_zones[count.index]
  map_public_ip_on_launch = true

  tags = merge(local.common_tags, {
    Name = "${var.name}-public-${var.availability_zones[count.index]}"
    Type = "public"
  })
}

# Private Subnets
resource "aws_subnet" "private" {
  count = length(var.availability_zones)

  vpc_id            = aws_vpc.main.id
  cidr_block        = local.private_subnet_cidrs[count.index]
  availability_zone = var.availability_zones[count.index]

  tags = merge(local.common_tags, {
    Name = "${var.name}-private-${var.availability_zones[count.index]}"
    Type = "private"
  })
}

# Elastic IPs for NAT Gateways
resource "aws_eip" "nat" {
  count = var.enable_nat_gateway ? length(var.availability_zones) : 0

  domain = "vpc"
  
  depends_on = [aws_internet_gateway.main]

  tags = merge(local.common_tags, {
    Name = "${var.name}-nat-eip-${count.index + 1}"
  })
}

# NAT Gateways
resource "aws_nat_gateway" "main" {
  count = var.enable_nat_gateway ? length(var.availability_zones) : 0

  allocation_id = aws_eip.nat[count.index].id
  subnet_id     = aws_subnet.public[count.index].id

  tags = merge(local.common_tags, {
    Name = "${var.name}-nat-${var.availability_zones[count.index]}"
  })

  depends_on = [aws_internet_gateway.main]
}

# Route Tables
resource "aws_route_table" "public" {
  vpc_id = aws_vpc.main.id

  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.main.id
  }

  tags = merge(local.common_tags, {
    Name = "${var.name}-public-rt"
    Type = "public"
  })
}

resource "aws_route_table" "private" {
  count = length(var.availability_zones)

  vpc_id = aws_vpc.main.id

  dynamic "route" {
    for_each = var.enable_nat_gateway ? [1] : []
    content {
      cidr_block     = "0.0.0.0/0"
      nat_gateway_id = aws_nat_gateway.main[count.index].id
    }
  }

  tags = merge(local.common_tags, {
    Name = "${var.name}-private-rt-${var.availability_zones[count.index]}"
    Type = "private"
  })
}

# Route Table Associations
resource "aws_route_table_association" "public" {
  count = length(var.availability_zones)

  subnet_id      = aws_subnet.public[count.index].id
  route_table_id = aws_route_table.public.id
}

resource "aws_route_table_association" "private" {
  count = length(var.availability_zones)

  subnet_id      = aws_subnet.private[count.index].id
  route_table_id = aws_route_table.private[count.index].id
}

# VPC Flow Logs
resource "aws_flow_log" "vpc" {
  iam_role_arn    = aws_iam_role.flow_log.arn
  log_destination = aws_cloudwatch_log_group.vpc_flow_log.arn
  traffic_type    = "ALL"
  vpc_id          = aws_vpc.main.id
}

resource "aws_cloudwatch_log_group" "vpc_flow_log" {
  name              = "/aws/vpc/flowlogs/${var.name}"
  retention_in_days = 14

  tags = local.common_tags
}

resource "aws_iam_role" "flow_log" {
  name = "${var.name}-vpc-flow-log-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "vpc-flow-logs.amazonaws.com"
        }
      }
    ]
  })
}

resource "aws_iam_role_policy" "flow_log" {
  name = "${var.name}-vpc-flow-log-policy"
  role = aws_iam_role.flow_log.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = [
          "logs:CreateLogGroup",
          "logs:CreateLogStream",
          "logs:PutLogEvents",
          "logs:DescribeLogGroups",
          "logs:DescribeLogStreams"
        ]
        Effect   = "Allow"
        Resource = "*"
      }
    ]
  })
}

# Outputs
output "vpc_id" {
  description = "ID of the VPC"
  value       = aws_vpc.main.id
}

output "vpc_cidr_block" {
  description = "CIDR block of the VPC"
  value       = aws_vpc.main.cidr_block
}

output "public_subnet_ids" {
  description = "List of IDs of the public subnets"
  value       = aws_subnet.public[*].id
}

output "private_subnet_ids" {
  description = "List of IDs of the private subnets"
  value       = aws_subnet.private[*].id
}

output "internet_gateway_id" {
  description = "ID of the Internet Gateway"
  value       = aws_internet_gateway.main.id
}

output "nat_gateway_ids" {
  description = "List of IDs of the NAT Gateways"
  value       = aws_nat_gateway.main[*].id
}
```

**EKS Cluster Module:**
```hcl
# modules/eks/main.tf - Production EKS cluster
variable "cluster_name" {
  description = "Name of the EKS cluster"
  type        = string
}

variable "cluster_version" {
  description = "Kubernetes version"
  type        = string
  default     = "1.28"
}

variable "vpc_id" {
  description = "VPC ID where EKS cluster will be deployed"
  type        = string
}

variable "subnet_ids" {
  description = "List of subnet IDs for EKS cluster"
  type        = list(string)
}

variable "node_groups" {
  description = "Map of EKS managed node group definitions"
  type = map(object({
    instance_types = list(string)
    capacity_type  = string
    min_size      = number
    max_size      = number
    desired_size  = number
    disk_size     = number
    ami_type      = string
    labels        = map(string)
    taints = list(object({
      key    = string
      value  = string
      effect = string
    }))
  }))
  default = {}
}

variable "enable_irsa" {
  description = "Enable IAM Roles for Service Accounts"
  type        = bool
  default     = true
}

variable "tags" {
  description = "Tags to apply to resources"
  type        = map(string)
  default     = {}
}

locals {
  common_tags = merge(
    var.tags,
    {
      ManagedBy = "terraform"
      Module    = "eks"
    }
  )
}

# EKS Cluster IAM Role
resource "aws_iam_role" "cluster" {
  name = "${var.cluster_name}-cluster-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "eks.amazonaws.com"
        }
      }
    ]
  })

  tags = local.common_tags
}

resource "aws_iam_role_policy_attachment" "cluster_amazon_eks_cluster_policy" {
  policy_arn = "arn:aws:iam::aws:policy/AmazonEKSClusterPolicy"
  role       = aws_iam_role.cluster.name
}

# EKS Cluster
resource "aws_eks_cluster" "main" {
  name     = var.cluster_name
  version  = var.cluster_version
  role_arn = aws_iam_role.cluster.arn

  vpc_config {
    subnet_ids              = var.subnet_ids
    endpoint_private_access = true
    endpoint_public_access  = true
    public_access_cidrs     = ["0.0.0.0/0"]
  }

  encryption_config {
    provider {
      key_arn = aws_kms_key.eks.arn
    }
    resources = ["secrets"]
  }

  enabled_cluster_log_types = ["api", "audit", "authenticator", "controllerManager", "scheduler"]

  depends_on = [
    aws_iam_role_policy_attachment.cluster_amazon_eks_cluster_policy,
    aws_cloudwatch_log_group.cluster
  ]

  tags = local.common_tags
}

# KMS Key for EKS encryption
resource "aws_kms_key" "eks" {
  description             = "EKS Secret Encryption Key"
  deletion_window_in_days = 7
  enable_key_rotation     = true

  tags = local.common_tags
}

resource "aws_kms_alias" "eks" {
  name          = "alias/${var.cluster_name}-eks"
  target_key_id = aws_kms_key.eks.key_id
}

# CloudWatch Log Group
resource "aws_cloudwatch_log_group" "cluster" {
  name              = "/aws/eks/${var.cluster_name}/cluster"
  retention_in_days = 7

  tags = local.common_tags
}

# Node Group IAM Role
resource "aws_iam_role" "node_group" {
  name = "${var.cluster_name}-node-group-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "ec2.amazonaws.com"
        }
      }
    ]
  })

  tags = local.common_tags
}

resource "aws_iam_role_policy_attachment" "node_group_amazon_eks_worker_node_policy" {
  policy_arn = "arn:aws:iam::aws:policy/AmazonEKSWorkerNodePolicy"
  role       = aws_iam_role.node_group.name
}

resource "aws_iam_role_policy_attachment" "node_group_amazon_eks_cni_policy" {
  policy_arn = "arn:aws:iam::aws:policy/AmazonEKS_CNI_Policy"
  role       = aws_iam_role.node_group.name
}

resource "aws_iam_role_policy_attachment" "node_group_amazon_ec2_container_registry_read_only" {
  policy_arn = "arn:aws:iam::aws:policy/AmazonEC2ContainerRegistryReadOnly"
  role       = aws_iam_role.node_group.name
}

# Managed Node Groups
resource "aws_eks_node_group" "main" {
  for_each = var.node_groups

  cluster_name    = aws_eks_cluster.main.name
  node_group_name = each.key
  node_role_arn   = aws_iam_role.node_group.arn
  subnet_ids      = var.subnet_ids
  
  instance_types = each.value.instance_types
  capacity_type  = each.value.capacity_type
  ami_type       = each.value.ami_type
  disk_size      = each.value.disk_size

  scaling_config {
    desired_size = each.value.desired_size
    max_size     = each.value.max_size
    min_size     = each.value.min_size
  }

  update_config {
    max_unavailable_percentage = 25
  }

  labels = each.value.labels

  dynamic "taint" {
    for_each = each.value.taints
    content {
      key    = taint.value.key
      value  = taint.value.value
      effect = taint.value.effect
    }
  }

  depends_on = [
    aws_iam_role_policy_attachment.node_group_amazon_eks_worker_node_policy,
    aws_iam_role_policy_attachment.node_group_amazon_eks_cni_policy,
    aws_iam_role_policy_attachment.node_group_amazon_ec2_container_registry_read_only,
  ]

  tags = merge(local.common_tags, {
    Name = "${var.cluster_name}-${each.key}"
  })
}

# OIDC Identity Provider
data "tls_certificate" "cluster" {
  url = aws_eks_cluster.main.identity[0].oidc[0].issuer
}

resource "aws_iam_openid_connect_provider" "cluster" {
  count = var.enable_irsa ? 1 : 0

  client_id_list  = ["sts.amazonaws.com"]
  thumbprint_list = [data.tls_certificate.cluster.certificates[0].sha1_fingerprint]
  url             = aws_eks_cluster.main.identity[0].oidc[0].issuer

  tags = local.common_tags
}

# Outputs
output "cluster_id" {
  description = "EKS cluster ID"
  value       = aws_eks_cluster.main.id
}

output "cluster_arn" {
  description = "EKS cluster ARN"
  value       = aws_eks_cluster.main.arn
}

output "cluster_endpoint" {
  description = "EKS cluster endpoint"
  value       = aws_eks_cluster.main.endpoint
}

output "cluster_security_group_id" {
  description = "EKS cluster security group ID"
  value       = aws_eks_cluster.main.vpc_config[0].cluster_security_group_id
}

output "oidc_issuer_url" {
  description = "The URL on the EKS cluster OIDC Issuer"
  value       = aws_eks_cluster.main.identity[0].oidc[0].issuer
}
```

### Environment-Specific Configurations

**Production Environment:**
```hcl
# environments/production/main.tf
terraform {
  required_version = ">= 1.5"
  
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
    kubernetes = {
      source  = "hashicorp/kubernetes"
      version = "~> 2.23"
    }
    helm = {
      source  = "hashicorp/helm"
      version = "~> 2.11"
    }
  }

  backend "s3" {
    bucket         = "company-terraform-state"
    key            = "production/terraform.tfstate"
    region         = "us-east-1"
    encrypt        = true
    dynamodb_table = "terraform-state-lock"
  }
}

provider "aws" {
  region = var.aws_region

  default_tags {
    tags = {
      Environment = "production"
      Project     = "myapp"
      Owner       = "platform-team"
      ManagedBy   = "terraform"
    }
  }
}

# Data sources
data "aws_availability_zones" "available" {
  state = "available"
  filter {
    name   = "zone-type"
    values = ["availability-zone"]
  }
}

data "aws_caller_identity" "current" {}

# Local values
locals {
  name = "myapp-production"
  region = var.aws_region
  azs    = slice(data.aws_availability_zones.available.names, 0, 3)
  
  tags = {
    Environment = "production"
    Project     = "myapp"
  }
}

# VPC Module
module "vpc" {
  source = "../../modules/vpc"

  name               = local.name
  cidr               = "10.0.0.0/16"
  availability_zones = local.azs
  enable_nat_gateway = true
  
  tags = local.tags
}

# EKS Module
module "eks" {
  source = "../../modules/eks"

  cluster_name    = "${local.name}-cluster"
  cluster_version = "1.28"
  
  vpc_id     = module.vpc.vpc_id
  subnet_ids = module.vpc.private_subnet_ids

  node_groups = {
    general = {
      instance_types = ["m6i.large"]
      capacity_type  = "ON_DEMAND"
      min_size      = 3
      max_size      = 10
      desired_size  = 5
      disk_size     = 50
      ami_type      = "AL2_x86_64"
      labels = {
        role = "general"
      }
      taints = []
    }
    
    compute = {
      instance_types = ["c6i.xlarge"]
      capacity_type  = "SPOT"
      min_size      = 0
      max_size      = 20
      desired_size  = 3
      disk_size     = 50
      ami_type      = "AL2_x86_64"
      labels = {
        role = "compute-optimized"
      }
      taints = [{
        key    = "workload-type"
        value  = "compute-optimized"
        effect = "NO_SCHEDULE"
      }]
    }
  }

  enable_irsa = true
  tags       = local.tags
}

# RDS Database
resource "aws_db_subnet_group" "main" {
  name       = "${local.name}-db-subnet-group"
  subnet_ids = module.vpc.private_subnet_ids

  tags = merge(local.tags, {
    Name = "${local.name}-db-subnet-group"
  })
}

resource "aws_security_group" "rds" {
  name_prefix = "${local.name}-rds-"
  vpc_id      = module.vpc.vpc_id

  ingress {
    from_port       = 5432
    to_port         = 5432
    protocol        = "tcp"
    security_groups = [module.eks.cluster_security_group_id]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = merge(local.tags, {
    Name = "${local.name}-rds-sg"
  })
}

resource "aws_db_instance" "main" {
  identifier = "${local.name}-database"
  
  engine         = "postgres"
  engine_version = "15.4"
  instance_class = "db.r6g.large"
  
  allocated_storage     = 100
  max_allocated_storage = 1000
  storage_type         = "gp3"
  storage_encrypted    = true
  
  db_name  = "myapp"
  username = "myapp"
  password = var.db_password
  
  vpc_security_group_ids = [aws_security_group.rds.id]
  db_subnet_group_name   = aws_db_subnet_group.main.name
  
  backup_retention_period = 7
  backup_window          = "03:00-04:00"
  maintenance_window     = "sun:04:00-sun:05:00"
  
  skip_final_snapshot = false
  final_snapshot_identifier = "${local.name}-final-snapshot-${formatdate("YYYY-MM-DD-hhmm", timestamp())}"
  
  performance_insights_enabled = true
  monitoring_interval         = 60
  monitoring_role_arn         = aws_iam_role.rds_enhanced_monitoring.arn
  
  enabled_cloudwatch_logs_exports = ["postgresql", "upgrade"]

  tags = merge(local.tags, {
    Name = "${local.name}-database"
  })
}

# RDS Enhanced Monitoring Role
resource "aws_iam_role" "rds_enhanced_monitoring" {
  name = "${local.name}-rds-enhanced-monitoring"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "monitoring.rds.amazonaws.com"
        }
      }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "rds_enhanced_monitoring" {
  role       = aws_iam_role.rds_enhanced_monitoring.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AmazonRDSEnhancedMonitoringRole"
}

# Application Load Balancer
resource "aws_lb" "main" {
  name               = "${local.name}-alb"
  internal           = false
  load_balancer_type = "application"
  security_groups    = [aws_security_group.alb.id]
  subnets           = module.vpc.public_subnet_ids

  enable_deletion_protection = true
  enable_http2              = true
  enable_waf_fail_open      = false

  access_logs {
    bucket  = aws_s3_bucket.alb_logs.bucket
    prefix  = "alb"
    enabled = true
  }

  tags = merge(local.tags, {
    Name = "${local.name}-alb"
  })
}

resource "aws_security_group" "alb" {
  name_prefix = "${local.name}-alb-"
  vpc_id      = module.vpc.vpc_id

  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = merge(local.tags, {
    Name = "${local.name}-alb-sg"
  })
}

# S3 Bucket for ALB Access Logs
resource "aws_s3_bucket" "alb_logs" {
  bucket = "${local.name}-alb-logs-${random_id.bucket_suffix.hex}"
  
  tags = local.tags
}

resource "random_id" "bucket_suffix" {
  byte_length = 4
}

resource "aws_s3_bucket_versioning" "alb_logs" {
  bucket = aws_s3_bucket.alb_logs.id
  versioning_configuration {
    status = "Enabled"
  }
}

resource "aws_s3_bucket_server_side_encryption_configuration" "alb_logs" {
  bucket = aws_s3_bucket.alb_logs.id

  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
  }
}

resource "aws_s3_bucket_lifecycle_configuration" "alb_logs" {
  bucket = aws_s3_bucket.alb_logs.id

  rule {
    id     = "log_lifecycle"
    status = "Enabled"

    expiration {
      days = 90
    }

    noncurrent_version_expiration {
      noncurrent_days = 30
    }
  }
}

# Variables
variable "aws_region" {
  description = "AWS region"
  type        = string
  default     = "us-east-1"
}

variable "db_password" {
  description = "Database password"
  type        = string
  sensitive   = true
}

# Outputs
output "vpc_id" {
  description = "ID of the VPC"
  value       = module.vpc.vpc_id
}

output "eks_cluster_id" {
  description = "EKS cluster ID"
  value       = module.eks.cluster_id
}

output "eks_cluster_endpoint" {
  description = "EKS cluster endpoint"
  value       = module.eks.cluster_endpoint
  sensitive   = true
}

output "database_endpoint" {
  description = "RDS instance endpoint"
  value       = aws_db_instance.main.endpoint
  sensitive   = true
}

output "load_balancer_dns" {
  description = "DNS name of the load balancer"
  value       = aws_lb.main.dns_name
}
```

## Ansible Configuration Management

### Playbook Structure and Best Practices

**Multi-Environment Ansible Configuration:**
```yaml
# site.yml - Main playbook
---
- name: Deploy web servers
  hosts: webservers
  become: yes
  roles:
    - common
    - security
    - nginx
    - application
    - monitoring

- name: Deploy database servers
  hosts: databases
  become: yes
  roles:
    - common
    - security
    - postgresql
    - monitoring

- name: Deploy load balancers
  hosts: loadbalancers
  become: yes
  roles:
    - common
    - security
    - haproxy
    - monitoring

# roles/common/tasks/main.yml
---
- name: Update system packages
  package:
    name: "*"
    state: latest
  when: ansible_os_family == "RedHat"

- name: Update apt cache
  apt:
    update_cache: yes
    cache_valid_time: 3600
  when: ansible_os_family == "Debian"

- name: Install essential packages
  package:
    name: "{{ common_packages }}"
    state: present

- name: Configure timezone
  timezone:
    name: "{{ timezone | default('UTC') }}"
  notify: restart rsyslog

- name: Configure NTP
  template:
    src: ntp.conf.j2
    dest: /etc/ntp.conf
    owner: root
    group: root
    mode: '0644'
  notify: restart ntp

- name: Start and enable NTP service
  service:
    name: "{{ ntp_service_name }}"
    state: started
    enabled: yes

- name: Create application user
  user:
    name: "{{ app_user }}"
    system: yes
    shell: /bin/false
    home: "{{ app_home }}"
    create_home: yes
    state: present

- name: Set up log rotation
  template:
    src: logrotate.conf.j2
    dest: "/etc/logrotate.d/{{ app_name }}"
    owner: root
    group: root
    mode: '0644'

# roles/security/tasks/main.yml
---
- name: Install security packages
  package:
    name: "{{ security_packages }}"
    state: present

- name: Configure SSH hardening
  template:
    src: sshd_config.j2
    dest: /etc/ssh/sshd_config
    owner: root
    group: root
    mode: '0600'
    backup: yes
  notify: restart ssh

- name: Configure firewall rules
  ufw:
    rule: "{{ item.rule }}"
    port: "{{ item.port | default(omit) }}"
    proto: "{{ item.proto | default(omit) }}"
    src: "{{ item.src | default(omit) }}"
    dest: "{{ item.dest | default(omit) }}"
  loop: "{{ firewall_rules }}"
  notify: reload ufw

- name: Enable firewall
  ufw:
    state: enabled
    policy: deny
    direction: incoming

- name: Configure fail2ban
  template:
    src: "{{ item }}.j2"
    dest: "/etc/fail2ban/{{ item }}"
    owner: root
    group: root
    mode: '0644'
  loop:
    - jail.local
    - filter.d/nginx-limit-req.conf
  notify: restart fail2ban

- name: Install and configure AIDE
  block:
    - name: Install AIDE
      package:
        name: aide
        state: present
    
    - name: Initialize AIDE database
      command: aide --init
      args:
        creates: /var/lib/aide/aide.db.new
    
    - name: Move AIDE database
      command: mv /var/lib/aide/aide.db.new /var/lib/aide/aide.db
      args:
        creates: /var/lib/aide/aide.db
    
    - name: Schedule AIDE checks
      cron:
        name: "AIDE integrity check"
        minute: "0"
        hour: "3"
        job: "/usr/bin/aide --check"

# roles/application/tasks/main.yml
---
- name: Create application directories
  file:
    path: "{{ item }}"
    state: directory
    owner: "{{ app_user }}"
    group: "{{ app_group }}"
    mode: '0755'
  loop:
    - "{{ app_home }}"
    - "{{ app_home }}/releases"
    - "{{ app_home }}/shared"
    - "{{ app_home }}/shared/logs"
    - "{{ app_home }}/shared/config"

- name: Deploy application
  block:
    - name: Download application archive
      get_url:
        url: "{{ app_download_url }}"
        dest: "{{ app_home }}/releases/{{ app_version }}.tar.gz"
        owner: "{{ app_user }}"
        group: "{{ app_group }}"
        mode: '0644'

    - name: Extract application
      unarchive:
        src: "{{ app_home }}/releases/{{ app_version }}.tar.gz"
        dest: "{{ app_home }}/releases/"
        owner: "{{ app_user }}"
        group: "{{ app_group }}"
        remote_src: yes
        creates: "{{ app_home }}/releases/{{ app_version }}"

    - name: Create application configuration
      template:
        src: app.conf.j2
        dest: "{{ app_home }}/releases/{{ app_version }}/config/app.conf"
        owner: "{{ app_user }}"
        group: "{{ app_group }}"
        mode: '0640'

    - name: Create systemd service file
      template:
        src: app.service.j2
        dest: "/etc/systemd/system/{{ app_name }}.service"
        owner: root
        group: root
        mode: '0644'
      notify:
        - reload systemd
        - restart application

    - name: Create symlink to current release
      file:
        src: "{{ app_home }}/releases/{{ app_version }}"
        dest: "{{ app_home }}/current"
        state: link
        owner: "{{ app_user }}"
        group: "{{ app_group }}"
      notify: restart application

    - name: Start and enable application service
      service:
        name: "{{ app_name }}"
        state: started
        enabled: yes

- name: Clean up old releases
  shell: |
    cd {{ app_home }}/releases
    ls -1 | head -n -{{ keep_releases | default(5) }} | xargs rm -rf
  become_user: "{{ app_user }}"
  when: cleanup_old_releases | default(true)

# group_vars/production.yml
---
# Common configuration
timezone: "America/New_York"
app_user: "myapp"
app_group: "myapp"
app_name: "myapp"
app_home: "/opt/myapp"
keep_releases: 5

# Security configuration
security_packages:
  - fail2ban
  - ufw
  - aide
  - rkhunter
  - logwatch

firewall_rules:
  - rule: allow
    port: "22"
    proto: tcp
    src: "10.0.0.0/16"
  - rule: allow
    port: "80"
    proto: tcp
  - rule: allow
    port: "443"
    proto: tcp
  - rule: allow
    port: "9100"
    proto: tcp
    src: "10.0.1.0/24"

# Application configuration
app_version: "{{ ansible_date_time.epoch }}"
app_download_url: "https://releases.company.com/myapp/{{ app_version }}.tar.gz"

# Database configuration
database:
  host: "{{ hostvars['db-server']['ansible_default_ipv4']['address'] }}"
  port: 5432
  name: "myapp_production"
  user: "myapp"
  password: "{{ vault_db_password }}"

# Monitoring
monitoring_enabled: true
prometheus_node_exporter_port: 9100
```

### Ansible Vault Integration

**Secure Secrets Management:**
```bash
#!/bin/bash
# scripts/deploy-with-vault.sh

set -e

ENVIRONMENT=${1:-staging}
VAULT_PASSWORD_FILE="~/.ansible/vault-${ENVIRONMENT}"

# Check if vault password file exists
if [[ ! -f "$VAULT_PASSWORD_FILE" ]]; then
    echo "Vault password file not found: $VAULT_PASSWORD_FILE"
    echo "Please create the file with appropriate permissions (600)"
    exit 1
fi

# Validate vault files
echo "Validating vault files..."
ansible-vault view --vault-password-file="$VAULT_PASSWORD_FILE" \
    "group_vars/$ENVIRONMENT/vault.yml" > /dev/null

# Run syntax check
echo "Running syntax check..."
ansible-playbook --syntax-check \
    --vault-password-file="$VAULT_PASSWORD_FILE" \
    -i "inventories/$ENVIRONMENT/hosts.yml" \
    site.yml

# Run deployment
echo "Starting deployment to $ENVIRONMENT..."
ansible-playbook \
    --vault-password-file="$VAULT_PASSWORD_FILE" \
    -i "inventories/$ENVIRONMENT/hosts.yml" \
    --limit "$ENVIRONMENT" \
    --diff \
    site.yml

echo "Deployment completed successfully!"
```

```yaml
# group_vars/production/vault.yml - Encrypted with ansible-vault
$ANSIBLE_VAULT;1.1;AES256
66386439653834336464396139313833303434323637663936383834376633373735376138333031
3330336463383131353262313464316131626162636432390a663332623435656262636161366163
38653665353834663535343863663834646134613263313734373537646334346465383934346438
6630306463646536390a313431373938316434646232663131353731303536633233326631326536
37353932663565613434663339616131613265383432613964316462313863623762626131383363
35366331613566646631646336393066363364663862353136643435396365366139346237343736
37383534363163663563376566616165636436393331653663303230646161613139
```

This comprehensive Infrastructure as Code framework provides systematic infrastructure management, configuration automation, and secure deployment practices that ensure consistent, reproducible, and maintainable infrastructure across all environments.