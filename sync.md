# Overview

The sync scripts / code in this repo will eventually be moved into a dedicated repository once we're ready to start creating pipelines to automate this process. For the time being, the following steps can be run  manually to create a sync Docker image and udpate the repo:

```sh
docker build . -t git-storage-sync
docker run --rm -v $PWD:/output -e OUTPUT=/output git-storage-sync
```
