#!/usr/bin/env python

import pulumi
from decouple import config
from pulumi_docker import RemoteImage, Container
from typing import Dict, Any, Tuple

image = config('IMAGE', default='nginx')
tag = config('TAG', default='latest')
container_port = config('CONTAINER_PORT', default=80, cast=int)
host_port = config('HOST_PORT', default=8080, cast=int)


def load_config() -> Dict[str, Any]:
    """Load configuration from environment with sensible defaults"""
    return {
        "image": {
            "name": f"{image}:{tag}",
            "keep_locally": True
        },
        "container": {
            "name": f"my-{image}",
            "ports": [{
                "internal": container_port,
                "external": host_port
            }]
        }
    }


def create_resources(cfg: Dict[str, Any]) -> Tuple[RemoteImage, Container]:
    """Create Pulumi resources from configuration"""
    image = RemoteImage(
        cfg["container"]["name"],
        name=cfg["image"]["name"],
        keep_locally=cfg["image"]["keep_locally"]
    )

    container = Container(
        cfg["container"]["name"],
        image=image.repo_digest,
        ports=cfg["container"]["ports"]
    )

    return image, container


def main():
    # Load config and create resources
    config = load_config()
    image, container = create_resources(config)

    # Export values
    pulumi.export('container_name', container.name)


if __name__ == "__main__":
    main()
