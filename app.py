#!/usr/bin/env python3
import os

import aws_cdk as cdk

from infra.agent_smith_stack import AgentSmithStack


app = cdk.App()
AgentSmithStack(app,
                "AgentSmithStack",
                env=cdk.Environment(
                    account=os.getenv('CDK_DEFAULT_ACCOUNT'),
                    region=os.getenv('CDK_DEFAULT_REGION')
                )
    )

app.synth()
