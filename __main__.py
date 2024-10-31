#!/usr/bin/env python

import pulumi
from pulumi_docker import Container, ContainerArgs, RemoteImage
from services import ServiceConfig, ServiceDict, services  # type: ignore
from typing import cast


def create_resources(service_cfg: ServiceConfig) -> tuple[RemoteImage, Container]:
    """Create Pulumi resources from service configuration."""
    # Create the image resource
    image = RemoteImage(
        service_cfg.container_name,
        name=service_cfg.image_name,
        keep_locally=service_cfg.keep_locally
    )

    # Create container args with proper typing
    container_args = ContainerArgs(
        image=image.repo_digest,
        name=service_cfg.container_name,
        **service_cfg.container_config
    )

    # Create the container resource
    container = Container(
        service_cfg.container_name,
        container_args
    )

    return image, container


def main():
    """Create resources for each service in the services list."""
    for service_dict in services:
        # Convert the flattened config to ServiceConfig
        service_cfg = ServiceConfig.from_dict(service_dict)

        # Create the resources
        image, container = create_resources(service_cfg)

        # Export container name
        pulumi.export(f"{service_cfg.name}_container_name", container.name)


if __name__ == '__main__':
    main()
