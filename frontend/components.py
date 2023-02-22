from typing import Any

from aws_cdk import Stack
from aws_cdk import aws_ecs as ecs
from aws_cdk import aws_servicediscovery as servicediscovery
from constructs import Construct

from frontend.ui.infrastructure import UI


class Frontend(Stack):
    def __init__(
        self,
        scope: Construct,
        id_: str,
        ecs_cluster: ecs.Cluster,
        namespace: servicediscovery.PrivateDnsNamespace,
        appserver_service_endpoint: str,
        **kwargs: Any,
    ):
        super().__init__(scope, id_, **kwargs)

        # pylint: disable=C0103

        container_environment = {
            "SEARCH_DOMAIN": namespace.namespace_name,
            "YELB_APPSERVER_ENDPOINT": appserver_service_endpoint,
        }

        self.ui = UI(
            self,
            "UI",
            ecs_cluster=ecs_cluster,
            namespace=namespace,
            container_environment=container_environment,
        )
