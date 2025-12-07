FROM grafana/grafana:12.1.0-ubuntu

COPY .config/grafana/provisioning/datasources /etc/grafana/provisioning/datasources
COPY .config/grafana/provisioning/dashboards /etc/grafana/provisioning/dashboards

ENTRYPOINT [ "/run.sh" ]
