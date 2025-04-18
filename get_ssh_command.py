from fabrictestbed_extensions.fablib.fablib import FablibManager as fablib_manager
import os
from dotenv import load_dotenv

def display_all(fablib: fablib_manager):
    slices = fablib.get_slices()

    # print slice names
    if slices:
        for i, slice in enumerate(slices):
            print(f"Slice {i} - {slice.get_name()}")

            # Get nodes
            print("Nodes:")
            nodes = slice.get_nodes()
            
            for j, node in enumerate(nodes):
                print(f"Node {j} - {node.get_name()} SSH command: {node.get_ssh_command()}")
    else:
        print("No slices found")

def get_slice_names(fablib: fablib_manager):
    slices = fablib.get_slices()
    slice_names: dict = {i: slice.get_name() for i, slice in enumerate(slices)}

    return slice_names

def _get_ssh_command(fablib: fablib_manager, 
                     slice_names: dict, 
                     ssh_config_path: str, 
                     sliver_key_path: str) -> str:

    # Print available slices
    print(f"Available slices")
    for i, name in slice_names.items():
        print(f"{i}: {name}")
    
    # Get slice choice
    chosen_slice_idx = int(input("Which slice do you want to get the node IPs from? (0, 1, 2, ...): "))
    slice_name = slice_names[chosen_slice_idx]
    print(f"Chosen slice: {slice_name}")
    
    # Print available nodes
    slice = fablib.get_slice(slice_name)
    nodes = slice.get_nodes()
    print("Nodes:")
    for i, node in enumerate(nodes):
        print(f"Node {i} - {node.get_name()} IP: {node.get_management_ip()}")

    # Get node choice
    chosen_node_idx = int(input("Which node do you want to SSH into? (0, 1, 2, ...): "))
    node = nodes[chosen_node_idx]
    print(f"Chosen node: {node.get_name()}")

    # Construct SSH command
    user_name = node.get_username()
    node_ip = node.get_management_ip()
    ssh_command = f"ssh -F {ssh_config_path} -i {sliver_key_path} {user_name}@{node_ip}"
    
    print(f"SSH command: {ssh_command}")
    return ssh_command


# Get slices
# slices = fablib.get_slices()
# if slices:
#     slice = slices[0]
#     print(f'Slice name: {slice.get_name()}')
    
#     # Get nodes
#     print('Nodes:')
#     nodes = slice.get_nodes()
#     for node in nodes:
#         print(f'Node {node.get_name()} SSH command: {node.get_ssh_command()}')
# else:
#     print("No slices found")

if __name__ == "__main__":
    # Load environment variables
    load_dotenv()
    ssh_config_path = os.getenv("SSH_CONFIG")
    sliver_key_path = os.getenv("SLIVER_KEY_LOCATION_PRIVATE")

    # Initialize FablibManager
    token_location = os.path.expanduser('~/fabric/.token.json')
    fablib = fablib_manager(token_location=token_location)

    slice_names = get_slice_names(fablib)
    ssh_command = _get_ssh_command(fablib, slice_names, ssh_config_path, sliver_key_path)    

    # save ssh command to file
    save_path = 'ssh_command.txt'
    with open(save_path, 'w') as f:
        f.write(ssh_command)