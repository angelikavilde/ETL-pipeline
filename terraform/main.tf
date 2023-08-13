resource "aws_ecs_cluster" "cluster" {
  name = "c8-angela-ecs-cluster-tf"

  setting {
    name  = "containerInsights"
    value = "disabled"
  }
}

resource "aws_ecs_task_definition" "ecs_task_definition" {
  family                   = "c8-angela-pipeline-ecs-task-tf"
  execution_role_arn       = var.execution_role
  network_mode             = "awsvpc"
  cpu                      = 1024
  memory                   = 3072
  requires_compatibilities = ["FARGATE"]

  container_definitions = jsonencode([
    {
      name   = "c8-angela-container-dashboard-tf"
      image  = var.ecr_image
      memory = 3072
      "portMappings" : [
        {
          "name" : "c8-angela-truck-pipeline-live-80-tcp",
          "containerPort" : 80,
          "hostPort" : 80,
          "protocol" : "tcp",
          "appProtocol" : "http"
        }
      ],
      essential = true,
      environment = [
        {
          "name" : "SECRET_KEY",
          "value" : var.secret_key
        },
        {
          "name" : "DB_PORT",
          "value" : var.port
        },
        {
          "name" : "DB_PASSWORD",
          "value" : var.password
        },
        {
          "name" : "DB_HOST",
          "value" : var.host
        },
        {
          "name" : "ACCESS_KEY",
          "value" : var.access_key
        },
        {
          "name" : "DB_NAME",
          "value" : var.db_name
        },
        {
          "name" : "DB_USER",
          "value" : var.username
        }
      ]
    }
  ])
}

resource "aws_ecs_service" "ecs_service" {
  name            = "c8-angela-ecs-service"
  cluster         = aws_ecs_cluster.cluster.id
  task_definition = aws_ecs_task_definition.ecs_task_definition.arn
  launch_type     = "FARGATE"
  desired_count   = 1

  network_configuration {
    subnets          = var.public_subnet_ids
    security_groups  = [var.sec_group_id]
    assign_public_ip = true
  }
}

resource "aws_ecs_task_definition" "ecs_task_definition_2" {
  family                   = "c8-angela-dashboard-ecs-task-tf"
  execution_role_arn       = var.execution_role
  network_mode             = "awsvpc"
  cpu                      = 1024
  memory                   = 3072
  requires_compatibilities = ["FARGATE"]

  container_definitions = jsonencode([
    {
      name   = "c8-angela-container-dashboard-tf"
      image  = var.ecr_image2
      memory = 3072
    }
  ])
}