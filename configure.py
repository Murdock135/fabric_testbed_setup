from fabrictestbed_extensions.fablib.fablib import FablibManager as fablib_manager
import os
from dotenv import load_dotenv

load_dotenv(interpolate=True)

if __name__ == "__main__":
    # Set up project in fabric
    fabric_rc_location = os.getenv("FABRIC_RC")
    bastion_key_location = os.getenv("BASTION_KEY_LOCATION")
    project_id = os.getenv("PROJECT_ID")
    token_location = os.getenv("TOKEN_LOCATION")
    
    # Expand ~ to absolute path
    if fabric_rc_location and fabric_rc_location.startswith('~'):
        fabric_rc_location = os.path.expanduser(fabric_rc_location)
    if bastion_key_location and bastion_key_location.startswith('~'):
        bastion_key_location = os.path.expanduser(bastion_key_location)
    if token_location and token_location.startswith('~'):
        token_location = os.path.expanduser(token_location)
    
    print(f"Using token location: {token_location}")
    
    try:
        fablib = fablib_manager(fabric_rc_location=fabric_rc_location,
                                bastion_key_location=bastion_key_location,
                                project_id=project_id,
                                token_location=token_location
        )
    except Exception as e:
        print("exception: ", e)
    
    try:
        fablib.verify_and_configure()
    except Exception as e:
        print("saving configuration faild. exception: ", e)
    
    # if configuration was successfully applied, save it. Note that this doesn't mean that the slice was created yet.
    save_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "fablib_config.txt"))
    fablib.config_file_path = save_path
    fablib.save_config()

    print(fablib.show_config(output='text'))

    # # Create slice and nodes
    print("Creating slice and nodes...")
    # print("Available images:")
    print(fablib.get_image_names())
    slice_name = "8540_project"
    slice = fablib.new_slice(name=slice_name)
    print("specified slice")

    # # Create node
    node1 = slice.add_node(name="node_1", image='default_ubuntu_22')
    node2 = slice.add_node(name="node_2", image='default_ubuntu_22')
    print("specified nodes")

    # # Submit slice
    try:
        slice.submit()
    except Exception as e:
        print("exception: ", e)

    print(0)

