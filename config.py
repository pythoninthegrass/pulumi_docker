from dataclasses import dataclass, field
from pulumi_docker import ContainerHealthcheckArgs, ContainerPortArgs, ContainerVolumeArgs
from typing import Any, NotRequired, TypedDict


class ServiceDict(TypedDict):
    """Type definition for service configuration dictionary."""
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
            from utils.convert import convert_to_bytes
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
