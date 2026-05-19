#!/bin/bash
# Backup Postgres щоденно
set -e

BACKUP_DIR="/var/backups/kylymy"
DATE=$(date +%Y%m%d_%H%M%S)
DB_NAME="${POSTGRES_DB:-kylymy}"
DB_USER="${POSTGRES_USER:-kylymy}"
BACKUP_FILE="${BACKUP_DIR}/db_${DATE}.sql.gz"

mkdir -p "$BACKUP_DIR"

pg_dump -U "$DB_USER" "$DB_NAME" | gzip > "$BACKUP_FILE"
echo "✅ Backup: $BACKUP_FILE"

# Видаляємо бекапи старше 30 днів
find "$BACKUP_DIR" -name "*.sql.gz" -mtime +30 -delete
echo "🧹 Old backups cleaned"
