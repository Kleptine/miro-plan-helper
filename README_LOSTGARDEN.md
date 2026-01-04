# Lost Garden Article Downloader

This project downloads all articles from https://lostgarden.com/ and converts them to PDFs with 70% font scaling, organized by date.

## Files

- `download_lostgarden_weasy.py` - Main script using WeasyPrint for PDF generation
- `check_progress.sh` - Monitor download progress in real-time

## Requirements

```bash
pip install requests weasyprint
```

## Usage

### Download all articles:
```bash
python3 download_lostgarden_weasy.py
```

This will:
1. Fetch all 286 article URLs from the sitemap
2. Download each article's HTML
3. Convert to PDF with 70% font scaling
4. Name files as `YYYY-MM-DD_article-slug.pdf` for alphabetical date sorting
5. Create `lostgarden_articles.zip` with all PDFs

### Monitor progress:
```bash
chmod +x check_progress.sh
./check_progress.sh
```

## Output

- **PDFs**: `/home/user/miro-plan-helper/lostgarden_pdfs/`
- **ZIP file**: `/home/user/miro-plan-helper/lostgarden_articles.zip`

## Performance

- Total articles: 286
- Processing rate: ~2-3 PDFs per minute
- Estimated time: ~2 hours
- Expected final size: ~50-100 MB (zipped)

## Features

- ✓ 70% font scaling for smaller text
- ✓ Date-prefixed filenames (YYYY-MM-DD) for alphabetical sorting by date
- ✓ All articles from 2005-2025
- ✓ Preserves images and formatting
- ✓ Automatic ZIP archive creation
