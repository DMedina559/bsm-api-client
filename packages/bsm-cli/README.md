<div style="text-align: center;">
    <img src="https://raw.githubusercontent.com/DMedina559/bsm-frontend/main/frontend/public/image/icon/favicon.svg" alt="BSM Logo" width="150">
</div>

# bsm-cli

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

`bsm-cli` is a command-line interface tool for managing Minecraft Bedrock Dedicated Servers via the Bedrock Server Manager API.

## Features

*   Full CLI interface using `click` and `questionary`.
*   Interactive menus for server management.
*   Realtime server state updates via WebSocket.
*   Seamlessly manages configuration for server and backups.

## Installation

Install the library using pip:

```bash
pip install bsm-cli
```

## Quick Start

You can invoke the CLI using:

```bash
bsm-cli
```

Which will trigger the interactive menu allowing you to manage and configure your Bedrock Dedicated Servers.
