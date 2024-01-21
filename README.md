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


## Licence and dependencies 
This package is released under MIT license. 
It relies on:
 * the [Minio Python SDK](https://github.com/minio/minio-py), released under Apache-2.0 license
 * the [xmltodict package](https://pypi.org/project/xmltodict/), released under MIT license
 * the [requests package](https://pypi.org/project/requests/), released under Apache-2.0 license





