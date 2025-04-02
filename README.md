# Big Data Principles Coursework

Repository for managing FABRIC testbed infrastructure for the Big Data Principles course.

## Overview

This repository contains scripts and configurations for setting up a distributed computing environment on the [FABRIC testbed](https://fabric-testbed.net/). It manages the creation of virtual machines, network configuration, and SSH access to nodes.

## Prerequisites

- FABRIC testbed account and project
- Python 3.6+
- FABRIC CLI credentials
- SSH keys configured in `$HOME/fabric/`

## Setup

1. Set environment variables (either in your shell or using a `.env` file):
   - `FABRIC_RC`: Path to FABRIC RC file
   - `BASTION_KEY_LOCATION`: Path to FABRIC bastion key
   - `PROJECT_ID`: Your FABRIC project ID
   - `TOKEN_LOCATION`: Path to FABRIC token file
   - `SLIVER_KEY_LOCATION`: Path to your sliver SSH key

2. Run the configuration script:
   ```
   python configure.py
   ```

3. Use the utilities to verify your nodes are running:
   ```
   python utilities/check_nodes.py
   ```

4. Connect to your nodes using the SSH command template:
   ```
   ssh -F ~/.ssh/fabric_ssh_config -i <private sliver key file> centos@<node IP>
   ```

## Troubleshooting

If you cannot connect to nodes, verify:
- Your SSH keys are properly configured
- The slice is in the "Active" state
- The nodes' reservation status is "Active"

Use `utilities/check_slice.py` for detailed diagnostics.
