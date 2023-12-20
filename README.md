# S3BlobSync

**S3BlobSync** provides a seamless way to operate between two of the major cloud platforms: AWS S3 and Azure Blob Storage. With a focus on data transfer and synchronization, this tool simplifies cloud operations, making it easier for developers and administrators to manage their resources across different platforms.

## Features

- **Data Download**: Easily download data from Azure or AWS S3.
- **Data Transfer**: Transfer data seamlessly from AWS S3 to Azure Blob.

## Configuration

To set up S3BlobSync, you need to configure your AWS and Azure credentials. Use the `.env.example` as a reference to create your `.env`.

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

## Advanced Usage

You can use the `--patterns` argument to filter the files you want to download based on their names. This argument accepts a list of patterns. Files that match any of the patterns will be downloaded. 

For example, to download all files that have names containing "foo", "bar", or "baz", and end with ".gz", you can run:

```bash
python3 download_blob.py --patterns *foo*.gz *bar*.gz *baz*.gz
```

The * character is a wildcard that matches any sequence of characters. So *foo*.gz will match any file name that contains "foo" and ends with ".gz".

Note: The --patterns argument is available in download_blob.py.

## Dependencies

- `boto3`: For AWS operations.
- `azure-storage-blob`: For Azure blob storage operations.
- `tqdm`: For Download Progress Bars
- `python-dotenv`: Environment Variables

Install the dependencies using:

```bash
pip install boto3 azure-storage-blob tqdm python-dotenv
```

## Contributing

Pull requests are welcome! For major changes, please open an issue first to discuss what you'd like to change.

## License

[MIT](https://choosealicense.com/licenses/mit/)