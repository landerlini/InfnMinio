# InfnMinio
A thin wrapper arround Minio SDK to ease web authentication on setups with running sts-wire  service


## Introduction

[Minio](https://min.io) is an Open Source Object Storage providing S3 apis along with a dashboard and web-based console. 

[STS-wire](https://github.com/DODAS-TS/sts-wire) is a tool to mount via POSIX the contents of a minio instance, managing authentication via IAM OIDC tokens.

Since STS-wire refreshes the web access token when it get invalidated, and since only one web access token per user is supported, accessing to the minio data via S3 when an instance of STS-wire is running requires using the same token. Otherwise the refresh of one client breaks the access of the other and everything ends up in a very unstable situation with continuous refreshes.

This package ease the configuration of the Minio SDK on instances where STS-wire is configured, by using the same token managed by STS-wire to connect via S3 apis to the object storage.


## Install

The `InfnMinio` package supports pip installation, but since it is so small, it does not claim namespace in PyPI. Just install it from GitHub:
```
pip install git+https://github.com/landerlini/InfnMinio.git
```


## Example

From a Python script or notebook, just import the package and use the `from_token` method to configure a Minio SDK client to access your data.
`from_token` takes as arguments:
 * the endpoint of the minio instance (defaulting to `minio.cloud.infn.it`)
 * the STS-wire-managed token, usually stored in the user's home (defaults to `$HOME/.token`)

```python
from InfnMinio import InfnMinio as Minio
minio = Minio.from_token("/home/.token")
minio.list_buckets()
```

## Integration with arrow `S3FileSystem`

[Apache Arrow](https://arrow.apache.org/) is a columnar in-memory data format designed to ease
access to data from multiple languages. It provides direct access to Feather and Parquet files 
stored in S3 object storage.

Direct access to arrow data from S3 is much more efficient than copying the files locally, as only the columns (or the chunks) needed in the computation are actually transmitted and stored locally.

To mount Minio authenticated with IAM as a `S3FileSystem` you can follow the recipe provided below.

```python
### Initialize the filesystem
from InfnMinio import InfnMinio as Minio
from pyarrow.fs import S3FileSystem

s3 = S3FileSystem(
    endpoint_override="minio.cloud.infn.it", 
    **Minio.get_credentials("minio.cloud.infn.it", "/home/.token")
)

### Create a pandas dataframe to upload as an example
import pandas as pd 
df = pd.DataFrame(dict(
    a=[1, 2, 3],
    b=[5, 6, 7]
))

## Upload the file to your bucket
import os
bucket = os.environ.get("JUPYTERHUB_USER") ## Replace with the bucket you wish to use for test
with s3.open_output_stream(f"{bucket}/test.parquet") as f:
    df.to_parquet(f)

## Retrieve the file from S3 importing it directly into pandas
with s3.open_input_file(f"{bucket}/test.parquet") as f:
    read_df = pd.read_parquet(f)

## To enable memory mapping, enabling to download only the relevant parts of the file
import pyarrow.parquet as pq
df = pq.read_table(f"{bucket}/test.parquet", memory_map=True, filesystem=s3).to_pandas()

```
 

## Licence and dependencies 
This package is released under MIT license. 
It relies on:
 * the [Minio Python SDK](https://github.com/minio/minio-py), released under Apache-2.0 license
 * the [xmltodict package](https://pypi.org/project/xmltodict/), released under MIT license
 * the [requests package](https://pypi.org/project/requests/), released under Apache-2.0 license


We acknowledge the support of the ICSC Foundation to the development of InfnMinio.

![image](https://user-images.githubusercontent.com/44908794/227858127-47d2b66f-4f1b-4f34-b505-814748957123.png)

