from typing import Any

from aws_cdk import aws_ecs as ecs
from aws_cdk import aws_servicediscovery as servicediscovery
from constructs import Construct

from shared.constructs.ecs_services.backend_fargate_service import BackendFargateService

SERVICE_NAME = "yelb-appserver"
SERVICE_PORT = 4567
SERVICE_DESIRED_COUNT = 2
SERVICE_CPU = 512
SERVICE_MEMORY = 2048
SERVICE_IMAGE = "mreferre/yelb-appserver:0.7"
SERVICE_LOG_PREFIX = "yelb-appserver"


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
            image_name=SERVICE_IMAGE,
            **kwargs,
        )
