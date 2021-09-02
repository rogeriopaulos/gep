FROM postgres:10-alpine

COPY ./compose/production/postgres/scripts_psql/backup.sh /usr/local/bin/backup
COPY ./compose/production/postgres/scripts_psql/restore.sh /usr/local/bin/restore
COPY ./compose/production/postgres/scripts_psql/list-backups.sh /usr/local/bin/list-backups

RUN chmod +x /usr/local/bin/backup && \
    chmod +x /usr/local/bin/restore && \
    chmod +x /usr/local/bin/list-backups