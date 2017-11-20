"""
Copyright (c) 2017 Amethix Tech.
Amazon S3 bucket connector wrapper
"""

import math
import sys, os
import getopt
import boto
import boto.s3.connection
from filechunkio import FileChunkIO
try:
    import utils as ut
except ImportError:
    from . import utils as ut
    
# local filesystem path
LOCAL_PATH = './'


class Connector:

    def __init__(self, access_key, secret_key):
        self.access_key = access_key
        self.secret_key = secret_key
        self.connection = boto.connect_s3(
            aws_access_key_id = self.access_key,
            aws_secret_access_key = self.secret_key,
            #host = host,
            is_secure = False,   #uncomment if not ssl
            calling_format = boto.s3.connection.OrdinaryCallingFormat()
        )
        self.localPath = LOCAL_PATH


    def listAllBuckets(self):
        """
        Given an established connection
        Returns list of all buckets owned by these credentials
        """

        # Gracefully exit on exception
        try:
            all_buckets = self.connection.get_all_buckets()
        except:
            print('Cannot list all buckets with these credentials')
            return False

        buckets = []
        for bucket in all_buckets:
            """
            print "{name}\t{created}".format(
                name = bucket.name,
                created = bucket.creation_date,
            )
            """
            buckets.append(bucket.name)

        return buckets

    def listBucketFiles(self, bucket, verbose=False):
        """
        Given a bucket
        Returns list of all files
        """

        try:
            s3_bucket = self.connection.get_bucket(bucket)  # select bucket
        except:
            print('Bucket %s does not exist'%bucket)
            return False

        files = []
        for key in s3_bucket.list():
            file_ = {}
            file_['name'] = key.name
            file_['size'] = key.size
            file_['modified'] = key.last_modified

            files.append(file_)
            if verbose:
                print ("%s\t%s\t%s"%(key.name, key.size, key.last_modified))

        return files


    def createFileFromString(self, bucket, folder, local_filename, content):
        """
        Given bucket, and string content
        Creates remote file at folder/filename with string content
        If filename exists it gets overwritten
        """
        try:
            bucket = self.connection.get_bucket(bucket)  # select bucket
        except Exception as e:
            print('Problem getting bucket %s'%e)
            return


        if bucket:
            try:
                key = bucket.new_key(os.path.join(folder, local_filename))
            except:
                print('Folder %s not accessible'%folder)
                return

            # TODO
            # assert content is a string
            key.set_contents_from_string(content)  # content from string
        else:
            print('%s does not exist' %bucket)


    def uploadFile(self, bucket, folder, local_path, chunk_size=52428800):
        """
        Upload local_filename to bucket/folder/local_filename in bucket
        Same filename gets overwritten
        """

        source_size = os.stat(local_path).st_size
        chunk_count = int(math.ceil(source_size / float(chunk_size)))
        local_filename = local_path.split('/')[-1]


        try:
            bucket = self.connection.get_bucket(bucket)  # select bucket
        except Exception as e:
            print('Problem getting bucket %s'%e)
            return

        if bucket:
            # create a multipart upload request
            mp = bucket.initiate_multipart_upload(os.path.basename(local_path))

            """
            try:
                key = bucket.new_key(os.path.join(folder, local_filename))
            except Exception as e:
                print('Folder %s not accessible %s'%(folder,e))

            key.set_contents_from_filename(local_path)
            """
            done = 0
            for i in range(chunk_count):
                offset = chunk_size * i
                bytes = min(chunk_size, source_size - offset)
                with FileChunkIO(local_path, 'r', offset=offset, bytes=bytes) as fp:
                    mp.upload_part_from_file(fp, part_num=i + 1)
                    done += chunk_size
                    if source_size > done:
                        ut.printStuff('Uploading file %s %%',(int(100.*done/source_size -1)))

            mp.complete_upload()
            print('File uploaded correctly')
            print
        else:
            print('%s does not exist' %bucket)


    def downloadFile(self, bucket, folder, filename):
        """
        Download remote bucket/filename to local folder/filename
        """
        try:
            bucket = self.connection.get_bucket(bucket)  # select bucket
        except:
            print('*' * 50)
            print('Bucket %s does not exist or is not accessible'%bucket)
            print('*' * 50)
            return (False)

        key = bucket.get_key(os.path.join(folder,filename))
        try:
            key.get_contents_to_filename(os.path.join(self.localPath,filename))
        except:
            print('*' * 50)
            print('File <%s> does not exist' %filename)
            print('*' * 50)
            return (False)

        return(True)
