from config import ServiceDict
from decouple import config
from pulumi_docker import ContainerHealthcheckArgs, ContainerPortArgs
from utils.convert import convert_to_bytes


def get_remote_services() -> list[ServiceDict]:
    """Return configuration for remote services."""
    return [
        {
            "name": "mongo",
            "image_tag": "8.0.3-noble",
            "ports": [ContainerPortArgs(
                internal=27017,
                external=27017
            )],
            "restart": "unless-stopped",
            "envs": [
                f"MONGO_INITDB_ROOT_USERNAME={config('MONGO_USERNAME', default='user')}",
                f"MONGO_INITDB_ROOT_PASSWORD={config('MONGO_PASSWORD', default='pass')}"
            ],
            "network_mode": "bridge",
            "memory": convert_to_bytes("512m"),
            "cpu_shares": 512,
            "healthcheck": ContainerHealthcheckArgs(
                tests=["CMD", "mongosh", "--eval", "db.adminCommand('ping')"],
                interval="30s",
                timeout="10s",
                retries=3
            )
        }
    ]
