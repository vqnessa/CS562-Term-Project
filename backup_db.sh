#!/bin/bash
PROJECT_DIR="/Users/vanessawatson/Desktop/OSU/CS562/CS562-Term-Project"
cd $PROJECT_DIR

DATE=$(date +"%Y-%m-%d_%H-%M")
/bin/cp flashmemo.db backups/flashmemo_$DATE.db

# Delete backups older than 7 days
/usr/bin/find "$PROJECT_DIR/backups" -type f -mtime +7 -delete