# Big Data Principles Coursework

Repository for managing FABRIC testbed infrastructure for the Big Data Principles course.

## Overview

This repository contains scripts and configurations for setting up a distributed computing environment on the [FABRIC testbed](https://fabric-testbed.net/). It provisions Ubuntu 22.04 nodes with GPU capabilities and provides scripts for SSH access.

## Prerequisites

- FABRIC testbed account and project
- Python 3.6+ with pip
- FABRIC CLI credentials
- SSH keys (can be in any location)

## Installation

Install required packages:
```bash
pip install -r requirements.txt
```

## Setup

1. Create a `.env` file with the following environment variables:
   - `FABRIC_RC`: Path to FABRIC RC file
   - `BASTION_KEY_LOCATION`: Path to FABRIC bastion key
   - `PROJECT_ID`: Your FABRIC project ID
   - `TOKEN_LOCATION`: Path to FABRIC token file
   - `SLIVER_KEY_LOCATION`: Path to your *public* SSH key
   - `SLIVER_KEY_LOCATION_PRIVATE`: Path to your *private* SSH key
   - `SSH_CONFIG`: Path to your SSH config file

2. Run the configuration script to create your slice with Ubuntu nodes:
   ```bash
   python configure.py
   ```

3. The `connect.sh` script is currently in development. For now, use the manual SSH command:
   ```bash
   python get_ssh_command.py
   ```
   Then follow the interactive prompts to select your slice and node.

## Slice Information

- Default slice name: `8540_project`
- Node setup: Two Ubuntu 22.04 nodes
- GPU: The script attempts to add a GPU (Tesla T4, RTX6000, A30, or A40) to node_1

## Troubleshooting

If you cannot connect to nodes, verify:
- Your SSH keys are properly configured
- The paths in your `.env` file are correct
- The slice is in the "Active" state
- The nodes' reservation status is "Active"

## Utilities

The repository includes several utility scripts:

- `get_ssh_command.py`: Interactive tool to get SSH commands for nodes
- `connect.sh`: Script to connect to nodes (in development, keys can be in any location)
- `utilites/check_slice.py`: Display details about your slice and node attributes
