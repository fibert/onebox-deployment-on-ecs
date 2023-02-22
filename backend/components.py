from typing import Any

from aws_cdk import Stack
from aws_cdk import aws_ecs as ecs
from aws_cdk import aws_servicediscovery as servicediscovery
from constructs import Construct

from backend.appserver.infrastructure import AppServer
from backend.database.infrastructure import Database
from backend.redis.infrastructure import Redis


class Backend(Stack):
    # pylint: disable=R0913
    def __init__(
        self,
        scope: Construct,
        id_: str,
        ecs_cluster: ecs.Cluster,
        namespace: servicediscovery.PrivateDnsNamespace,
        **kwargs: Any,
    ):
        super().__init__(scope, id_, **kwargs)

        appserver = AppServer(
            self,
            "AppServer",
            ecs_cluster=ecs_cluster,
            namespace=namespace,
        )
        self.appserver_service_endpoint = f"http://{appserver.service.cloud_map_service.service_name}:{appserver.port}"

        Database(
            self,
            "Database",
            ecs_cluster=ecs_cluster,
            namespace=namespace,
        )

        Redis(
            self,
            "Redis",
            ecs_cluster=ecs_cluster,
            namespace=namespace,
        )
