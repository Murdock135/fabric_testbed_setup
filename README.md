# FABRIC Test Environment Setup

A toolkit for creating and managing FABRIC testbed environments.

## Overview

This project provides scripts to create, configure, and connect to FABRIC testbed slices for distributed systems experiments and big data applications.

## Features

- Automated slice and node creation
- SSH configuration generation
- Node status checking utilities

## Requirements

- Python 3.6+
- FABRIC account credentials
- Environment variables configured

## Quick Start

1. Configure environment variables (create a `.env` file based on `fabric_config.txt`)
2. Run `python configure.py` to create slices and nodes
3. Use utilities in `utilities/` to check node status

## SSH Access

Once configured, access nodes using:
```
ssh -F ~/.ssh/fabric_ssh_config -i ~/fabric_config/sliver_key centos@<node-ip>
```

## Utilities

- `check_nodes.py`: Display available nodes and SSH commands
- `check_slice.py`: Get detailed slice information