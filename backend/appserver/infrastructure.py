import pathlib
from typing import Any

from aws_cdk import aws_ecs as ecs
from aws_cdk import aws_servicediscovery as servicediscovery
from constructs import Construct

from shared.constructs.ecs_services.backend_fargate_service import BackendFargateService

SERVICE_NAME = "compliment-appserver"
SERVICE_PORT = 5000
SERVICE_DESIRED_COUNT = 2
SERVICE_CPU = 512
SERVICE_MEMORY = 2048
SERVICE_LOG_PREFIX = "compliment-appserver"

RUNTIME_DIRECTORY = "runtime"


class AppServer(BackendFargateService):
    # pylint: disable=R0913
    def __init__(
        self,
        scope: Construct,
        id_: str,
        ecs_cluster: ecs.Cluster,
        namespace: servicediscovery.PrivateDnsNamespace,
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
            container_image=AppServer.__get_container_image(),
            **kwargs,
        )

    @staticmethod
    def __get_container_image() -> ecs.ContainerImage:
        directory_path = str(
            pathlib.Path(__file__).parent.joinpath(RUNTIME_DIRECTORY).resolve()
        )
        container_image = ecs.AssetImage.from_asset(directory=directory_path)
        return container_image
