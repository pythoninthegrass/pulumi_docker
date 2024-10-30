#!/usr/bin/env python

import pulumi
from pulumi_docker import RemoteImage, Container, ContainerPortArgs
from decouple import config
from pathlib import Path


def main():
    # Configuration
    IMAGE = config('IMAGE', default='nginx')
    TAG = config('TAG', default='latest')
    HOST_PORT = config('HOST_PORT', default=8080, cast=int)
    CONTAINER_PORT = config('CONTAINER_PORT', default=80, cast=int)

    SSH_USER = config('SSH_USER', default='lance.stephens')
    SSH_HOST = config('SSH_HOST', default='localhost')
    SSH_KEY = config('SSH_PRIVATE_KEY', default='~/.ssh/id_rsa')
    SSH_KEY = Path(SSH_KEY).expanduser()

    # remote_connection = {"type": "ssh",
    #                      "user": SSH_USER,
    #                      "host": SSH_HOST,
    #                      "private_key": open(SSH_KEY, "r").read()
    # }

    # Create resources
    image = RemoteImage(f"{IMAGE}-image",
                        name=f"{IMAGE}:{TAG}",
                        keep_locally=True
    )

    container = Container(f"{image.name}-local",
                          image=image.name,
                          name=f"{image.name}-local-container",
                          ports=[ContainerPortArgs(
                                internal=CONTAINER_PORT,
                                external=HOST_PORT
                          )],
    )

    # Export values
    pulumi.export('container_name', container.name)


if __name__ == "__main__":
    main()
