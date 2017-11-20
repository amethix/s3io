s3io Package
--------

# Install 

```python3 setup.py build```

```python3 setup.py install```

# Usage 

To use, simply import in any Python project

    >>> import s3io as s3


## Create connector

    >>> conn = s3.Connector(ACCESS_KEY, SECRET_KEY)


## List all buckets attached to credentials

    >>> ll = conn.listAllBuckets()
    >>> print(ll)



## List all files of bucket BUCKET_NAME
    >>> files = conn.listFiles('BUCKET_NAME')
    >>> for f in files:
          ...print('%s\t%s'%(f['name'], f['size']))



## Download file
    >>> filename = '06e7e5a8727aa8f5173d0046b8f8f29b'
    >>> conn.downloadFile('BUCKET_NAME', 'REMOTE_PATH', filename)


## Create file test1.txt from string 
    >>> conn.createFileFromString('BUCKET_NAME', '/', 'test1.txt', 'another string here')

## Upload file myfile.dat to BUCKET_NAME/test
    >>> conn.uploadFile('BUCKET_NAME', 'test', 'myfile.dat')
