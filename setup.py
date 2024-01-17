from setuptools import setup, find_packages

setup(
    name='s3blobsync',
    version='0.2',
    author='Ala Arab',
    author_email='ala.arab@admenergy.com',
    description='Provides a seamless way to operate between AWS S3 and Azure Blob Storage', 
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/admenergy/s3blobsync',
    packages=find_packages(),
    install_requires=[
        'boto3',
        'azure-storage-blob',
        'tqdm',
        'python-dotenv',
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',  # Update the license as appropriate
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.10',  # Minimum version requirement of the Python for your project
)
