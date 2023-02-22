from typing import Any

from aws_cdk import aws_ec2 as ec2
from aws_cdk import aws_ecs as ecs
from aws_cdk import aws_servicediscovery as servicediscovery
from constructs import Construct


class BackendFargateService(Construct):
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
        image_name: str,
        **kwargs: Any,
    ):
        super().__init__(scope, id_, **kwargs)

        self.name = name
        self.port = port
        self.desired_count = desired_count
        self.cpu = cpu
        self.memory = memory
        self.image_name = image_name
        self.log_prefix = name

        self.task_definition = self.__create_task_definition()
        self.__add_container_to_task_definition(namespace, self.task_definition)

        self.service = self.__create_ecs_service(
            ecs_cluster, namespace, self.task_definition
        )
        self.service.connections.allow_to_any_ipv4(ec2.Port.tcp(self.port))

    def __create_task_definition(self) -> ecs.FargateTaskDefinition:
        task_definition = ecs.FargateTaskDefinition(
            self,
            "TaskDefinition",
            memory_limit_mib=self.memory,
            cpu=self.cpu,
        )
        return task_definition

    def __add_container_to_task_definition(
        self,
        namespace: servicediscovery.PrivateDnsNamespace,
        task_definition: ecs.TaskDefinition,
    ) -> ecs.ContainerDefinition:
        container_environment = {"SEARCH_DOMAIN": namespace.namespace_name}

        container = task_definition.add_container(
            "Container",
            image=ecs.ContainerImage.from_registry(self.image_name),
            memory_limit_mib=self.memory,
            cpu=self.cpu,
            environment=container_environment,
            logging=ecs.LogDriver.aws_logs(stream_prefix=self.log_prefix),
        )

        return container

    def __create_ecs_service(
        self,
        ecs_cluster: ecs.Cluster,
        namespace: servicediscovery.PrivateDnsNamespace,
        task_definition: ecs.FargateTaskDefinition,
    ) -> ecs.FargateService:
        cloud_map_options = ecs.CloudMapOptions(
            cloud_map_namespace=namespace,
            dns_record_type=servicediscovery.DnsRecordType.A,
        )

        service = ecs.FargateService(
            self,
            "FargateService",
            cluster=ecs_cluster,
            task_definition=task_definition,
            desired_count=self.desired_count,
            # service_name=self.name,
            cloud_map_options=cloud_map_options,
        )

        return service
