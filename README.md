# S3BlobSync

**S3BlobSync** provides a seamless way to operate between two of the major cloud platforms: AWS S3 and Azure Blob Storage. With a focus on data transfer and synchronization, this tool simplifies cloud operations, making it easier for developers and administrators to manage their resources across different platforms.

## Features

- **Data Download**: Easily download data from Azure or AWS S3.
- **Data Transfer**: Transfer data seamlessly from AWS S3 to Azure Blob.

## Configuration

To set up S3BlobSync, you need to configure your AWS and Azure credentials. Use the `config.example.py` as a reference to create your `config.py`.

## Usage

1. **Transfer from AWS S3 to Azure**
   ```bash
   python3 s3blobsync.py
   ```

2. **Download from AWS S3**
   ```bash
   python3 download_from_s3.py
   ```

3. **Download from Azure**
   ```bash
   python3 download_from_azure.py
   ```

## Dependencies

- `boto3`: For AWS operations.
- `azure-storage-blob`: For Azure blob storage operations.
- `tqdm`: For Download Progress Bars

Install the dependencies using:

```bash
pip install boto3 azure-storage-blob tqdm
```

## Contributing

Pull requests are welcome! For major changes, please open an issue first to discuss what you'd like to change.

## License

[MIT](https://choosealicense.com/licenses/mit/)