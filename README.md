# Fabric testbed setup

Repository for setting up a slice in [FABRIC testbed](https://portal.fabric-testbed.net/) with 2 nodes with a GPU on one node 1. 

Note:
    - This repository assumes you are already part of a fabric project.
    - The current implementation doesn't configure any network communication between the two nodes.
    - GPU model isn't specified. The first GPU available from a list of GPUs (see configure.py) will be used.
    - As of April 16, 2025, fabric_extensions API only works with Python 3.11.x. [See related github issue](https://github.com/fabric-testbed/fabrictestbed-extensions/issues/418#issuecomment-2810304953)
    

# Prerequisite Readings (Recommended)
Make sure you read fabric's documentation on
1. Using SSH keys to access their VM's.
2. [Fabric extension API documentation's first page](https://fabric-fablib.readthedocs.io/en/latest/index.html)


## Setup
1. Create *two pairs* ssh keys using keygen add them to fabric [here](https://portal.fabric-testbed.net/experiments#sshKeys)
    Note: Save the keys in a location (not ~/.ssh/). I recommend `~/fabric/`

2. Get a Token from [Fabric credential manager](https://cm.fabric-testbed.net/)

2. Create a `.env` file with the following environment variables:
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

*Note: You might see a directory named `'$HOME'`. It's unclear why that's being created. It isn't important so I recommend deleting it to keep the directory clean.*

## Slice Information

- Node setup: Two Ubuntu 22.04 nodes
- GPU: The script attempts to add a GPU (Tesla T4, RTX6000, A30, or A40) to node_1

## Troubleshooting

If you cannot connect to nodes, verify:
- You've added the bastion key and sliver key into [fabric ssh keys](https://portal.fabric-testbed.net/experiments#sshKeys).
- The paths in your `.env` file are correct

## Utilities

The repository includes several utility scripts:

- `get_ssh_command.py`: Interactive tool to get SSH commands for nodes
- `connect.sh`: Script to connect to nodes (in development, keys can be in any location)
- `utilites/check_slice.py`: Display details about your slice and node attributes

