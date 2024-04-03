FROM bitnami/minio-client

COPY ./configure-minio.sh /opt/rhombus/configure-minio.sh

CMD ["/opt/rhombus/configure-minio.sh"]