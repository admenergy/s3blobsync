# S3BlobSync

**S3BlobSync** provides a seamless way to operate between two of the major cloud platforms: AWS S3 and Azure Blob Storage. With a focus on data transfer and synchronization, this tool simplifies cloud operations, making it easier for developers and administrators to manage their resources across different platforms.

## Features

- **Data Download**: Easily download data from Azure or AWS S3.
- **Data Transfer**: Transfer data seamlessly from AWS S3 to Azure Blob.

## Configuration

To set up S3BlobSync, you need to configure your AWS and Azure credentials. Use the `.env.example` as a reference to create your `.env`.

## Dependencies

- `boto3`: For AWS operations.
- `azure-storage-blob`: For Azure blob storage operations.
- `tqdm`: For Download Progress Bars
- `python-dotenv`: Environment Variables

Install the dependencies using:

```bash
pip install boto3 azure-storage-blob tqdm python-dotenv
```

## Usage

### Syncing Data from AWS S3 to Azure Blob Storage

```bash
python3 s3blobsync.py --env-file <path_to_env_file>
```

### Downloading Data

- From AWS S3:

  ```bash
  python3 download_s3.py --patterns <pattern1> <pattern2> --env-file <path_to_env_file>
  ```

- From Azure Blob Storage:

  ```bash
  python3 download_blob.py --patterns <pattern1> <pattern2> --env-file <path_to_env_file>
  ```

### Listing Contents of S3 Bucket

```bash
python3 list_s3.py --env-file <path_to_env_file>
```

## Command-Line Entry Points

After installation, you can use the following command-line entry points to execute the functionalities:

- **Sync Data**: `s3blobsync`
- **Download from AWS S3**: `download_s3`
- **Download from Azure Blob Storage**: `download_blob`
- **List S3 Bucket Contents**: `list_s3`

These commands can be used directly in the terminal. For example:

```bash
s3blobsync --env-file <path_to_env_file>
list_s3 --env-file <path_to_env_file>
download_s3 --patterns <pattern1> <pattern2> --env-file <path_to_env_file>
download_blob --patterns <pattern1> <pattern2> --env-file <path_to_env_file>
```

## Advanced Usage

- **Pattern Filtering**: Use the optional `--patterns` argument in download scripts to filter files by name. 
- **Custom Environment File**: Specify a custom `.env` file using the `--env-file` argument. Defaults to '.env'

## Module Usage

The scripts in the `S3BlobSync` library can be imported and used as modules in other Python scripts. This allows for greater flexibility and integration into larger projects. Here's how you can use each module:

### Syncing Data from AWS S3 to Azure Blob Storage

```python
from s3blobsync import s3blobsync

# Sync data
s3blobsync(env_file='path_to_your_env_file')
```

### Downloading Data from AWS S3

```python
from download_s3 import download_s3

# Download data with pattern filtering
download_s3(patterns=['pattern1', 'pattern2'], env_file='path_to_your_env_file')
```

### Downloading Data from Azure Blob Storage

```python
from download_blob import download_blob

# Download data with pattern filtering
download_blob(patterns=['pattern1', 'pattern2'], env_file='path_to_your_env_file')
```

### Listing Contents of S3 Bucket

```python
from list_s3 import list_s3

# List contents of S3 bucket
list_s3(env_file='path_to_your_env_file')
```

## Contributing

Pull requests are welcome! For major changes, please open an issue first to discuss what you'd like to change.

## License

[MIT](https://choosealicense.com/licenses/mit/)
