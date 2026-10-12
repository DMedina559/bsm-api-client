<div style="text-align: center;">
    <img src="https://raw.githubusercontent.com/DMedina559/bsm-frontend/main/frontend/public/image/icon/favicon.svg" alt="BSM Logo" width="150">
</div>

# bsm-api-client

<p align="center">
  <a href="https://github.com/DMedina559/bsm-api-client/releases">
    <img alt="Stable" src="https://img.shields.io/github/v/release/DMedina559/bsm-api-client?label=Stable&color=blue">
  </a>
  <a href="https://github.com/DMedina559/bsm-api-client/releases">
    <img alt="Pre-Release" src="https://img.shields.io/github/v/release/DMedina559/bsm-api-client?include_prereleases&label=Pre-Release&color=red">
  </a>
  <a href="https://github.com/DMedina559/bsm-api-client/actions">
    <img alt="Tests" src="https://img.shields.io/github/actions/workflow/status/DMedina559/bsm-api-client/build-test.yml?label=Tests&event=push">
  </a>
</p>

## Introduction

This repository is a monorepo containing the following Python packages for interacting with the Bedrock Server Manager API:

*   [`bsm-api-client`](packages/bsm-api-client/README.md): An asynchronous Python client library.
*   [`bsm-cli`](packages/bsm-cli/README.md): A command-line interface tool for managing servers via the API.

## Installation

Install the library using pip:

```bash
pip install bsm-api-client
```

Or if you wish to use the Command Line Interface CLI:

```bash
pip install bsm-cli
```

## OpenAPI contract

In a separate contract-tooling environment, install `bedrock-server-manager` from the target backend checkout. Export with `python scripts/export_bsm_openapi.py --output packages/bsm-api-client/src/bsm_api_client/generated/openapi.json`, then run `python scripts/generate_models.py` and `python scripts/generate_client.py packages/bsm-api-client/src/bsm_api_client/generated/openapi.json`. CI compares the complete document with backend `dev` using the backend-owned exporter and its declared dependencies.
