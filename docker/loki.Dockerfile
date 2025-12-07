FROM grafana/loki:3.4.1

COPY .config/loki.yaml /etc/loki/config.yaml