from typing import Any

from aws_cdk import aws_ecs as ecs
from aws_cdk import aws_ecs_patterns as ecs_patterns
from aws_cdk import aws_servicediscovery as servicediscovery
from constructs import Construct


class FrontendFargateService(Construct):
    def __init__(
        self,
        scope: Construct,
        id_: str,
        ecs_cluster: ecs.Cluster,
        namespace: servicediscovery.PrivateDnsNamespace,
        name: str,
        port: int,
        desired_count: int,
        cpu: int,
        memory: int,
        container_image: ecs.ContainerImage,
        container_environment: list[str, str] = {},
        health_check_path: str = "/",
        **kwargs: Any,
    ):
        super().__init__(scope, id_, **kwargs)

        self.ecs_cluster = ecs_cluster
        self.namespace = namespace
        self.name = name
        self.port = port
        self.desired_count = desired_count
        self.cpu = cpu
        self.memory = memory
        self.container_image = container_image
        self.log_prefix = name
        self.container_environment = container_environment
        self.health_check_path = health_check_path

        self.task_definition = self.__create_task_definition()

        self.__add_container_to_task_definition()
        self.service = self.__create_ecs_service()

    def __create_task_definition(self) -> ecs.FargateTaskDefinition:
        task_definition = ecs.FargateTaskDefinition(
            self,
            "TaskDefinition",
            memory_limit_mib=self.memory,
            cpu=self.cpu,
        )
        return task_definition

    def __add_container_to_task_definition(self) -> ecs.ContainerDefinition:
        container = self.task_definition.add_container(
            "Container",
            image=self.container_image,
            memory_limit_mib=self.memory,
            cpu=self.cpu,
            environment=self.container_environment,
            logging=ecs.LogDriver.aws_logs(stream_prefix=self.name),
        )

        http_port_mapping = ecs.PortMapping(container_port=self.port)
        container.add_port_mappings(http_port_mapping)

        return container

    def __create_ecs_service(self) -> ecs.FargateService:
        cloud_map_options = ecs.CloudMapOptions(
            cloud_map_namespace=self.namespace,
            dns_record_type=servicediscovery.DnsRecordType.A,
        )

        alb_fargate_service_pattern = (
            ecs_patterns.ApplicationLoadBalancedFargateService(
                self,
                "Service",
                cluster=self.ecs_cluster,
                task_definition=self.task_definition,
                desired_count=self.desired_count,
                public_load_balancer=True,
                cloud_map_options=cloud_map_options,
            )
        )
        
        alb_fargate_service_pattern.target_group.configure_health_check(
            path=self.health_check_path
        )

        return alb_fargate_service_pattern.service
