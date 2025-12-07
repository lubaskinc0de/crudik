FROM timberio/vector:0.48.0-debian

COPY .config/vector.yaml /etc/vector/vector.yaml

ENV DOCKER_HOST=unix:///var/run/docker.sock

ENTRYPOINT ["/usr/bin/vector"]