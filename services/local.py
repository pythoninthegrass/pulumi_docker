from config import ServiceDict
from decouple import config
from pulumi_docker import ContainerPortArgs, ContainerVolumeArgs


def get_local_services() -> list[ServiceDict]:
    """Return configuration for local services."""
    return [
        {
            "name": "nginx",
            "image_tag": "latest",
            "keep_locally": True,
            "ports": [ContainerPortArgs(
                internal=80,
                external=8080
            )],
            "restart": "unless-stopped"
        },
        {
            "name": "redis",
            "image_tag": "7.4.1-bookworm",
            "ports": [ContainerPortArgs(
                internal=6379,
                external=6379
            )],
            "restart": "unless-stopped",
            "envs": [
                f"REDIS_PASSWORD={config('REDIS_PASSWORD', default='secret')}"
            ],
            "volumes": [ContainerVolumeArgs(
                host_path="/tmp/redis-data",
                container_path="/data"
            )]
        }
    ]
