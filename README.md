# S3BlobSync

**S3BlobSync** provides a seamless way to operate between two of the major cloud platforms: AWS S3 and Azure Blob Storage. With a focus on data transfer and synchronization, this tool simplifies cloud operations, making it easier for developers and administrators to manage their resources across different platforms.

## Features

- **Data Download**: Easily download data from Azure or AWS S3.
- **Data Transfer**: Transfer data seamlessly from AWS S3 to Azure Blob.

## Installation

Install S3BlobSync easily via pip:

```bash
pip install s3blobsync
```

## Configuration

Create a `.env` file for AWS and Azure credentials, referencing `.env.example`.

## Command-Line Entry Points

Post-installation, the following command-line tools are available:

- **Sync Data**: `s3blobsync`
- **Download from AWS S3**: `download_s3`
- **Download from Azure Blob Storage**: `download_blob`
- **List S3 Bucket Contents**: `list_s3`

Usage examples:

```bash
s3blobsync --env-file <path_to_env_file>
list_s3 --env-file <path_to_env_file>
download_s3 --patterns 'foo*.gz,bar*.gz' --env-file <path_to_env_file>
download_blob --patterns 'foo*.gz,bar*.gz' --env-file <path_to_env_file>
```

## Dependencies

These dependencies are automatically installed with pip:

- `boto3`
- `azure-storage-blob`
- `tqdm`
- `python-dotenv`

## Using S3BlobSync in Scripts

After installing via pip, S3BlobSync can be used as a library in your Python scripts:

### Syncing Data from AWS S3 to Azure Blob Storage

```python
from s3blobsync import s3blobsync
s3blobsync(env_file='path_to_your_env_file')
```

### Downloading Data from AWS S3

```python
from s3blobsync import download_s3
download_s3(patterns=['foo*.gz', 'bar*.gz'], env_file='path_to_your_env_file')
```

### Downloading Data from Azure Blob Storage

```python
from s3blobsync import download_blob
download_blob(patterns=['foo*.gz', 'bar*.gz'], env_file='path_to_your_env_file')
```

### Listing Contents of S3 Bucket

```python
from s3blobsync import list_s3
list_s3(env_file='path_to_your_env_file')
```

## Alternative Installation and Usage

For a more manual approach, clone the GitHub repository and install the dependencies. When running scripts directly, use the module execution method to avoid relative import issues:

```bash
python3 -m s3blobsync.s3blobsync --env-file <path_to_env_file>
python3 -m s3blobsync.download_s3 --patterns 'foo*.gz,bar*.gz' --env-file <path_to_env_file>
python3 -m s3blobsync.download_blob --patterns 'foo*.gz,bar*.gz' --env-file <path_to_env_file>
python3 -m s3blobsync.list_s3 --env-file <path_to_env_file>
```

## Advanced Usage

- **Pattern Filtering**: Apply `--patterns` for file name filtering (comma-separated).
- **Custom Environment File**: Use `--env-file` to specify a custom `.env` file (defaults to '.env').

## Contributing

Contributions are welcome. Please open an issue first for significant changes.

## License

S3BlobSync is under the [MIT License](https://choosealicense.com/licenses/mit/).
