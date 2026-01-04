#!/bin/bash
# Monitor the download progress

while true; do
    COUNT=$(ls /home/user/miro-plan-helper/lostgarden_pdfs/ 2>/dev/null | wc -l)
    SIZE=$(du -sh /home/user/miro-plan-helper/lostgarden_pdfs/ 2>/dev/null | awk '{print $1}')
    PERCENT=$((COUNT * 100 / 286))

    echo "================================"
    echo "Time: $(date '+%H:%M:%S')"
    echo "Progress: $COUNT / 286 PDFs ($PERCENT%)"
    echo "Total size: $SIZE"
    echo "================================"

    if [ -f "/home/user/miro-plan-helper/lostgarden_articles.zip" ]; then
        ZIP_SIZE=$(ls -lh /home/user/miro-plan-helper/lostgarden_articles.zip | awk '{print $5}')
        echo "✓ ZIP FILE CREATED: $ZIP_SIZE"
        echo "Download complete!"
        break
    fi

    sleep 60
done
