# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

```bash
# Install dependencies
pip install -r requirements.txt
pip install -r requirements-dev.txt

# CDK
cdk synth       # Synthesize CloudFormation template
cdk diff        # Compare deployed vs local stack
cdk deploy      # Deploy to AWS (account: 548931596365, region: eu-central-1)

# Tests
pytest                          # Run all tests
pytest tests/unit/test_foo.py   # Run a single test file

# Security
bandit -r . -ll   # Python security scan
```

CI runs Bandit and Gitleaks on push/PR to `main`.

## Architecture

This is an AWS CDK project that deploys an AI chat API backed by Amazon Bedrock.

**Request flow:**
```
Client → API Gateway (IAM auth) → Lambda (src/chat/handler.py) → Bedrock Nova Lite → Response
```

**Key components:**

- `infra/agent_smith_stack.py` — Single CDK stack defining all infrastructure: Lambda, API Gateway REST API, Bedrock guardrails (hate/violence/sexual/insults/misconduct/prompt-attack), and IAM permissions.
- `src/chat/handler.py` — Lambda handler that parses the POST body, calls Bedrock (`eu.amazon.nova-lite-v1:0`), and returns the model response. Uses AWS Lambda Powertools for structured logging. Receives `MODEL_ID`, `GUARDRAIL_ID`, and `GUARDRAIL_VERSION` via environment variables set by the CDK stack.
- `app.py` — CDK app entry point; instantiates `AgentSmithStack` with hardcoded account/region.

Lambda Powertools is provided as a layer (ARN reference), not bundled — `src/chat/requirements.txt` is intentionally empty.
