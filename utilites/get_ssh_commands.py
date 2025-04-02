from fabrictestbed_extensions.fablib.fablib import FablibManager as fablib_manager
import os

# Initialize FablibManager
token_location = os.path.expanduser('~/fabric/.token.json')
fablib = fablib_manager(token_location=token_location)

# Get slices
slices = fablib.get_slices()
if slices:
    slice = slices[0]
    print(f'Slice name: {slice.get_name()}')
    
    # Get nodes
    print('Nodes:')
    nodes = slice.get_nodes()
    for node in nodes:
        print(f'Node {node.get_name()} SSH command: {node.get_ssh_command()}')
else:
    print("No slices found")