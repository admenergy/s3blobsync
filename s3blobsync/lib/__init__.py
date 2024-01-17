# lib/__init__.py content

# Import all functions from blob.py
from .blob import (
    upload_to_azure,
    download_from_azure,
    transfer_s3_to_azure,
)

# Import all functions from common.py
from .common import (
    read_processed_files_list,
)

# Import all functions from s3.py
from .s3 import (
    assume_role,
    get_s3_client,
    download_from_s3,
)
