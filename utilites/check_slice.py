from fabrictestbed_extensions.fablib.fablib import FablibManager as fablib_manager
import os

# Initialize FablibManager
token_location = os.path.expanduser('~/fabric/.token.json')
fablib = fablib_manager(token_location=token_location)

# Get slices
slices = fablib.get_slices()
if slices:
    slice = slices[0]
    # Print all properties of the slice
    print(f'Slice details:')
    print(dir(slice))
    print(f'Slice attributes:')
    for attr in dir(slice):
        if not attr.startswith('__'):
            try:
                value = getattr(slice, attr)
                if not callable(value):
                    print(f'{attr}: {value}')
            except:
                print(f'{attr}: Unable to access')
    
    # Get nodes
    print('\nNodes:')
    try:
        nodes = slice.get_nodes()
        for node in nodes:
            print(f'Node: {node}')
            print(f'Node properties: {dir(node)}')
            
            # Try to get SSH info
            try:
                ssh_command = node.get_ssh_command()
                print(f'SSH command: {ssh_command}')
            except Exception as e:
                print(f'Error getting SSH command: {e}')
    except Exception as e:
        print(f'Error getting nodes: {e}')
else:
    print("No slices found")