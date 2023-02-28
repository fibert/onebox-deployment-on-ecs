#!/usr/bin/env python3
import os

from aws_cdk import App
from aws_cdk import Environment

from backend.components import Backend
from frontend.components import Frontend
from shared.infrastructure import Shared

app = App()

shared = Shared(
    app,
    "SharedInfrastructure",
    env=Environment(
        account=os.environ["CDK_DEFAULT_ACCOUNT"],
        region=os.environ["CDK_DEFAULT_REGION"],
    ),
)

backend = Backend(
    app,
    "Backend",
    ecs_cluster=shared.ecs_cluster,
    namespace=shared.namespace,
    env=Environment(
        account=os.environ["CDK_DEFAULT_ACCOUNT"],
        region=os.environ["CDK_DEFAULT_REGION"],
    ),
)

frontend = Frontend(
    app,
    "Frontend",
    ecs_cluster=shared.ecs_cluster,
    namespace=shared.namespace,
    backend_endpoint=backend.appserver_service_endpoint,
    env=Environment(
        account=os.environ["CDK_DEFAULT_ACCOUNT"],
        region=os.environ["CDK_DEFAULT_REGION"],
    ),
)
frontend.node.add_dependency(backend)


app.synth()
