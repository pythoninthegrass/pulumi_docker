# pulumi_docker

Use Pulumi's Docker provider to deploy containers locally and remotely.

## Minimum Requirements

* [Pulumi](https://www.pulumi.com/docs/get-started/install/)
* [Python 3.11+](https://www.python.org/downloads/)
* [Docker](https://docs.docker.com/get-docker/)

## Recommended Requirements

* [asdf](https://asdf-vm.com/guide/getting-started.html)

## Quickstart

```bash
# default destination and stack
pulumi org set-default <my_org>

# new project (empty directory other than .git)
pulumi new

# manage and view state
pulumi stack init dev

# tf analogues
pulumi preview
pulumi up
pulumi down

# info
pulumi about

# project config (Pulumi.yaml)
pulumi config
```

## Linting

```bash
# directory
mypy .

# file
mypy __main__.py
```

## TODO

* Replace fake creds in [services.py](services.py) with environment variables
* Add more outputs (cf. `mongo_container_name`)
* Research if it's possible to use both `unix:///var/run/docker.sock` and `ssh://user@remote-host:22` in the [Pulumi config](Pulumi.yml#L11)
* Set registry creds to use other than `docker.io` / access private registry
  * `DOCKER_REGISTRY_USER`
  * `DOCKER_REGISTRY_PASS`
* Local containers
  * prometheus and grafana
* Remote containers (node-exporters)

    | Name          | Image                                                       | Port |
    | ------------- | ----------------------------------------------------------- | ---- |
    | node          | "prom/node-exporter:latest"                                 | 9100 |
    | mongodb       | "percona/mongodb_exporter:0.40"                             | 9216 |
    | redis         | "oliver006/redis_exporter:latest"                           | 9121 |
    | elasticsearch | "quay.io/prometheuscommunity/elasticsearch-exporter:latest" | 9114 |
    | kafka         | "danielqsj/kafka-exporter:latest"                           | 9308 |

* Add tests

## Further Reading

* [Docker Provider](https://www.pulumi.com/docs/reference/pkg/docker/)
* [pulumi/pulumi-docker](https://github.com/pulumi/pulumi-docker/tree/master/examples)
* [Docker Build](https://www.pulumi.com/registry/packages/docker-build/)
* [Command](https://www.pulumi.com/registry/packages/command/)
