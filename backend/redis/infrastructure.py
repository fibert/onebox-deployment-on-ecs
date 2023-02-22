from typing import Any

from aws_cdk import aws_ecs as ecs
from aws_cdk import aws_servicediscovery as servicediscovery
from constructs import Construct

from shared.constructs.ecs_services.backend_fargate_service import BackendFargateService

SERVICE_NAME = "yelb-redis"
SERVICE_PORT = 6379
SERVICE_DESIRED_COUNT = 1
SERVICE_CPU = 512
SERVICE_MEMORY = 2048
SERVICE_IMAGE = "redis:4.0.2"
SERVICE_LOG_PREFIX = "yelb-redis"


class Redis(BackendFargateService):
    # pylint: disable=R0913z
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
