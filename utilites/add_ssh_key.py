from fabrictestbed_extensions.fablib.fablib import FablibManager as fablib_manager
import os
from dotenv import load_dotenv


def get_chosen_node(fablib: fablib_manager):
    # Get slices
    print("Available slices:")
    slices = fablib.get_slices()

    for i, slice in enumerate(slices):
        print(f"Slice {i}")
        print(slice)
    print("=" * 50)

    # Retry until valid slice choice
    chosen_slice = None
    while chosen_slice is None:
        try:
            choice = int(input("Which slice do you want to add the SSH key to? (0, 1, 2, ...): "))
            chosen_slice = slices[choice]
        except (ValueError, IndexError):
            print("Invalid choice. Please enter a valid slice index.")

    print(f"Chosen slice: \n{chosen_slice}")

    # Get nodes
    print("Available nodes:")
    nodes = chosen_slice.get_nodes()

    print("Nodes:")
    for i, node in enumerate(nodes):
        print(f"Node {i} - {node.get_name()} IP: {node.get_management_ip()}")

    print("Enter -1 to add the SSH key to all nodes.")

    # Retry until valid node choice
    chosen_nodes = None
    while chosen_nodes is None:
        try:
            choice = int(input("Which node do you want to add the SSH key to? (0, 1, 2, ... or -1 for all nodes): "))
            if choice == -1:
                chosen_nodes = nodes  # All nodes
            else:
                chosen_nodes = [nodes[choice]]  # Single node
        except (ValueError, IndexError):
            print("Invalid choice. Please enter a valid node index or -1 for all nodes.")

    if len(chosen_nodes) == len(nodes):
        print("All nodes selected.")
    else:
        print(f"Chosen node: {chosen_nodes[0].get_name()}")

    return chosen_nodes


def add_ssh_key_to_node(node, ssh_key_path):
    # Add SSH key to the node
    print(f"Adding SSH key from {ssh_key_path} to node {node.get_name()}...")
    
    # Read the SSH key from the file
    with open(ssh_key_path, 'r') as f:
        ssh_key = f.read()

    node.add_public_key(sliver_public_key=ssh_key)
    print("Sliver key added successfully.")


if __name__ == "__main__":
    # Load environment variables from .env file
    load_dotenv()

    token_location = os.getenv("TOKEN_LOCATION")
    sliver_key_path = os.getenv("SLIVER_KEY_LOCATION")
    
    if not token_location or not os.path.exists(token_location):
        print(f"Error: Token file not found at {token_location}")
        exit(1)

    if not sliver_key_path or not os.path.exists(sliver_key_path):
        print(f"Error: Sliver key file not found at {sliver_key_path}")
        exit(1)

    print(f"Using token location: {token_location}")
    print(f"Using sliver key location: {sliver_key_path}")

    # Fablib object
    fablib = fablib_manager(token_location=token_location)

    # Get chosen nodes
    nodes = get_chosen_node(fablib)
    if not nodes:
        print("No valid nodes selected. Exiting.")
        exit(1)

    # Add SSH key to each chosen node
    for node in nodes:
        add_ssh_key_to_node(node, sliver_key_path)




