from fabrictestbed_extensions.fablib.fablib import FablibManager as fablib_manager
import os

# Initialize FablibManager
token_location = os.path.expanduser('~/fabric/.token.json')
fablib = fablib_manager(token_location=token_location)

# Get slices
slices = fablib.get_slices()

