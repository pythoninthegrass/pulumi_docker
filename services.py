from dataclasses import dataclass, field
from decouple import config  # type: ignore
from pulumi_docker import ContainerHealthcheckArgs, ContainerPortArgs, ContainerVolumeArgs
from typing import Any, NotRequired, TypedDict, cast
from utils.convert import convert_to_bytes


class ServiceDict(TypedDict):
    name: str       # Required
    image_tag: str  # Required
    keep_locally: NotRequired[bool]
    ports: NotRequired[list[ContainerPortArgs]]
    restart: NotRequired[str]
    envs: NotRequired[list[str]]
    volumes: NotRequired[list[ContainerVolumeArgs]]
    network_mode: NotRequired[str]
    memory: NotRequired[int | str]
    cpu_shares: NotRequired[int]
    healthcheck: NotRequired[ContainerHealthcheckArgs]

@dataclass
class ServiceConfig:
    """Configuration for a Docker service including image and container settings."""
    name: str
    image_tag: str
    keep_locally: bool = True

    # Store all container-related config
    _container_config: dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, config: ServiceDict) -> 'ServiceConfig':
        """Create ServiceConfig from a dictionary, separating container configs."""
        # Create instance with required fields and optional keep_locally
        instance = cls(
            name=config['name'],
            image_tag=config['image_tag'],
            keep_locally=config.get('keep_locally', True)
        )

        # Extract all container-related config
        container_config = {
            k: v for k, v in config.items()
            if k not in ['name', 'image_tag', 'keep_locally'] and v is not None
        }

        # Handle memory conversion if it's a string
        if 'memory' in container_config and isinstance(container_config['memory'], str):
            container_config['memory'] = convert_to_bytes(container_config['memory'])

        # Set container config
        instance._container_config = container_config

        return instance

    @property
    def image_name(self) -> str:
        """Generate the full image name with tag."""
        return f"{self.name}:{self.image_tag}"

    @property
    def container_name(self) -> str:
        """Generate the container name."""
        return f"my-{self.name}"

    @property
    def container_config(self) -> dict[str, Any]:
        """Return the container configuration."""
        return self._container_config

# Example services configuration remains the same
services: list[ServiceDict] = [
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
            "REDIS_PASSWORD=secret"
        ],
        "volumes": [ContainerVolumeArgs(
            host_path="/tmp/redis-data",
            container_path="/data"
        )]
    },
    {
        "name": "mongo",
        "image_tag": "8.0.3-noble",
        "ports": [ContainerPortArgs(
            internal=27017,
            external=27017
        )],
        "restart": "unless-stopped",
        "envs": [
            "MONGO_INITDB_ROOT_USERNAME=user",
            "MONGO_INITDB_ROOT_PASSWORD=pass"
        ],
        "network_mode": "bridge",
        "memory": "512m",
        "cpu_shares": 512,
        "healthcheck": ContainerHealthcheckArgs(
            tests=["CMD", "mongosh", "--eval", "db.adminCommand('ping')"],
            interval="30s",
            timeout="10s",
            retries=3
        )
    }
]
