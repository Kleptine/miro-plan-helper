#!/bin/bash
# Monitor download progress

while true; do
  COUNT=$(ls /home/user/miro-plan-helper/lostgarden_pdfs/ 2>/dev/null | wc -l)
  PERCENT=$((COUNT * 100 / 286))

  if [ -f "/home/user/miro-plan-helper/lostgarden_articles.zip" ]; then
    ZIP_SIZE=$(ls -lh /home/user/miro-plan-helper/lostgarden_articles.zip | awk '{print $5}')
    echo "✓ COMPLETE! ZIP created: $ZIP_SIZE ($COUNT PDFs)"
    break
  fi

  echo "$(date '+%H:%M:%S') - Progress: $COUNT/286 PDFs ($PERCENT%)"
  sleep 30
done
