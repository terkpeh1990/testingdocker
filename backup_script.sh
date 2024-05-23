while true; do
    PGPASSWORD="$DB_PASSWORD" pg_dump -U "$DB_USER" -h db "$DB_NAME" > "/backups/backup_$(date +%Y%m%d%H%M%S).sql"
    sleep 300
done