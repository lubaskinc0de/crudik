FROM quay.io/oauth2-proxy/oauth2-proxy:v7.11.0-alpine

COPY .config/oauth2-proxy.toml /etc/oauth2-proxy/oauth2-proxy.toml

ENTRYPOINT [ "--config=/etc/oauth2-proxy/oauth2-proxy.toml" ]
