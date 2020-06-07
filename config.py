import os

S3_BUCKET                 = "chiconguyen"
S3_KEY                    = "96WX2Q4HUE8KG3C0LEIZ"
S3_SECRET                 = "V3vdmwdAHwBPT5cLeRLNjVq8aICCdBXzt6aaYxnx"
S3_LOCATION               = 'http://ceph3:7480'.format(S3_BUCKET)

SECRET_KEY                = os.urandom(32)
DEBUG                     = True
PORT                      = 7480