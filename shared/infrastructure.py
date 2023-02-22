from typing import Any

from aws_cdk import Stack
from aws_cdk import aws_ec2 as ec2
from aws_cdk import aws_ecs as ecs
from aws_cdk import aws_servicediscovery as servicediscovery
from constructs import Construct

VPC_MAX_AZS = 2
NAMESPACE_NAME = "onebox"


class Shared(Stack):
    def __init__(
        self,
        scope: Construct,
        id_: str,
        **kwargs: Any,
    ):
        super().__init__(scope, id_, **kwargs)

        self.vpc = self.__create_vpc()
        self.ecs_cluster = self.__create_ecs_cluster(self.vpc)
        self.namespace = self.__create_servicediscovery_namespace(self.vpc)

    def __create_vpc(self) -> ec2.Vpc:
        vpc = ec2.Vpc(
            self,
            "Vpc",
            max_azs=VPC_MAX_AZS,
        )
        return vpc

    def __create_ecs_cluster(self, vpc: ec2.Vpc) -> ecs.Cluster:
        cluster = ecs.Cluster(
            self,
            "Cluster",
            enable_fargate_capacity_providers=True,
            vpc=vpc,
        )
        return cluster

    def __create_servicediscovery_namespace(
        self, vpc: ec2.Vpc
    ) -> servicediscovery.PrivateDnsNamespace:
        namespace = servicediscovery.PrivateDnsNamespace(
            self,
            "Namespace",
            name=NAMESPACE_NAME,
            vpc=vpc,
        )
        return namespace
