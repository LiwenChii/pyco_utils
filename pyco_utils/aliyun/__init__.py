# 需要配合 aliyun 的 sdk 使用

from .aliyun_log import Alilog

from .aliyun_oss import (
    upload_data,
    upload_local_file,
    blob_urls,
    download,
    download_zips,
    remove_zips,
    list_keys,
    delete_key,
    delete_keys,
)
