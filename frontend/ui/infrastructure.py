import pathlib
from typing import Any

from aws_cdk import aws_ecs as ecs
from aws_cdk import aws_ecs_patterns as ecs_patterns
from aws_cdk import aws_servicediscovery as servicediscovery
from constructs import Construct

from shared.constructs.ecs_services.frontend_fargate_service import (
    FrontendFargateService,
)

SERVICE_NAME = "compliment-ui"
SERVICE_PORT = 80
SERVICE_DESIRED_COUNT = 3
SERVICE_CPU = 512
SERVICE_MEMORY = 2048
SERVICE_LOG_PREFIX = "compliment-ui"
SERVICE_HEALTH_CHECK_PATH = "/health"

RUNTIME_DIRECTORY = "runtime"


class UI(FrontendFargateService):
    def __init__(
        self,
        scope: Construct,
        id_: str,
        ecs_cluster: ecs.Cluster,
        namespace: servicediscovery.PrivateDnsNamespace,
        container_environment: list[str, str] = {},
        **kwargs: Any,
    ):
        super().__init__(
            scope,
            id_,
            ecs_cluster=ecs_cluster,
            namespace=namespace,
            name=SERVICE_NAME,
            port=SERVICE_PORT,
            desired_count=SERVICE_DESIRED_COUNT,
            cpu=SERVICE_CPU,
            memory=SERVICE_MEMORY,
            container_image=self.__get_container_image(),
            container_environment=container_environment,
            health_check_path=SERVICE_HEALTH_CHECK_PATH,
            **kwargs,
        )

    def __get_container_image(self) -> ecs.ContainerImage:
        directory_path = str(
            pathlib.Path(__file__).parent.joinpath(RUNTIME_DIRECTORY).resolve()
        )
        container_image = ecs.AssetImage.from_asset(directory=directory_path)
        return container_image
