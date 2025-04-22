from fabrictestbed_extensions.fablib.fablib import FablibManager as fablib_manager
import os
from dotenv import load_dotenv
import tomllib

load_dotenv(interpolate=True)

choice_to_column = {
    "GPU_RTX6000": "rtx6000_available",
    "GPU_TeslaT4": "tesla_t4_available",
    "GPU_A30": "a30_available",
    "GPU_A40": "a40_available"
}

if __name__ == "__main__":
    # Set up project in fabric
    fabric_rc_location = os.getenv("FABRIC_RC")
    bastion_key_location = os.getenv("BASTION_KEY_LOCATION")
    project_id = os.getenv("PROJECT_ID")
    token_location = os.getenv("TOKEN_LOCATION")
    sliver_key_location = os.getenv("SLIVER_KEY_LOCATION")    
    config_file_path = 'config.toml'

    # Expand ~ to absolute path
    # if fabric_rc_location and fabric_rc_location.startswith('~'):
    #    fabric_rc_location = os.path.expanduser(fabric_rc_location)
    #if bastion_key_location and bastion_key_location.startswith('~'):
    #    bastion_key_location = os.path.expanduser(bastion_key_location)
    #if token_location and token_location.startswith('~'):
    #    token_location = os.path.expanduser(token_location)
    
    print(f"fabric rc location: {fabric_rc_location}")
    print(f"Using token location: {token_location}")
    
    try:
        fablib = fablib_manager(fabric_rc=fabric_rc_location,
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
    save_path = 'fabric_config.txt'
    fablib.config_file_path = save_path
    fablib.save_config()

    print("fablib config:\n")
    print(fablib.show_config(output='text'))
    
    # Load config
    with open(config_file_path, 'rb') as f:
        config = tomllib.load(f)
        print("config: \n", config)
    
    gpu = config.get('gpu', 'Unknown')
    if gpu.lower() == 'unknown':
        raise NameError("gpu name can't be blank")

    num_gpus = config.get('num_gpus', 1)
    ram = config.get('ram', 16)
    disk = config.get('disk', 50)
    

    # Find site with available resources
    column_name = choice_to_column[gpu]
    try:
        site = fablib.get_random_site(filter_function=lambda x: x[column_name] >= 4)
    except Exception as e:
        print("Couldn't find site with specified resources.")
        print(e)

    print(f"Site with specified resources found. Site: {site}")

    # Create slice and nodes
    print("Creating slice and nodes...")
    print("Available images:")
    print(fablib.get_image_names())
    slice_name = config.get('slice_name', 'new_slice')
    slice = fablib.new_slice(name=slice_name)
    print("specified slice")
    
    # Create nodes
    node1 = slice.add_node(name="node_1", site=site, image='default_ubuntu_22', disk=disk, ram=ram)
    print("specified nodes")

    # Add components (GPU)
    viable_gpus = ['GPU_TeslaT4', 'GPU_RTX6000', 'GPU_A30', 'GPU_A40']
    
    for i in range(num_gpus):
        node1.add_component(model=gpu, name=f"gpu_{i}_{gpu}")
        print(f"Added {i} gpus to node1")

    # Submit slice and save
    try:
        slice.submit(wait=True, progress=True)
        slice.save('slice.graphml')
    except Exception as e:
        print("exception: ", e)
    
    # wait until slice nodes are ready for ssh
    slice.wait_ssh()

    # Add sliver key to nodes
    try:
        with open(sliver_key_location, 'r') as f:
            sliver_key = f.read()
            print("sliver key:\n", sliver_key)
    except Exception as e:
        print("Exception occured: ", e)

    try:
        node1 = slice.get_node("node_1")
        node1.add_public_key(sliver_public_key=sliver_key)
        print("Added sliver_key.pub to node1")
    except Exception as e:
        print("Exception occured: ", e)
    try:
        node2 = slice.get_node("node_2")
        node2.add_public_key(sliver_public_key=sliver_key)
        print("Added sliver_key.pub to node2")
    except Exception as e:
        print("Exception occured: ", e)

    print(50 * "-")
    print("Slice created successfully!")
    print("Slice details:")
    print(slice.show(output='text'))
