#!/usr/bin/env python3
"""
Download all articles from lostgarden.com and convert them to PDFs
with 70% font scaling, organized by date.
Uses WeasyPrint for HTML to PDF conversion.
"""
import os
import re
from xml.etree import ElementTree
from urllib.parse import urlparse
import zipfile
import requests
from weasyprint import HTML, CSS

def get_all_articles():
    """Fetch all article URLs from the sitemap."""
    sitemap_url = "https://lostgarden.com/sitemap-1.xml"
    response = requests.get(sitemap_url)
    response.raise_for_status()

    # Parse XML
    root = ElementTree.fromstring(response.content)
    namespace = {'ns': 'http://www.sitemaps.org/schemas/sitemap/0.9'}

    articles = []
    for url_elem in root.findall('.//ns:url', namespace):
        loc = url_elem.find('ns:loc', namespace).text
        lastmod = url_elem.find('ns:lastmod', namespace)
        lastmod_date = lastmod.text if lastmod is not None else None

        # Extract date from URL pattern YYYY/MM/DD
        date_match = re.search(r'/(\d{4})/(\d{2})/(\d{2})/', loc)
        if date_match:
            year, month, day = date_match.groups()
            date_str = f"{year}-{month}-{day}"
            articles.append((loc, date_str))

    return articles

def get_article_title(url):
    """Extract article title from URL."""
    # Get the last part of the URL path
    path = urlparse(url).path
    # Remove leading/trailing slashes and split
    parts = path.strip('/').split('/')
    # Get the last part (slug)
    if len(parts) >= 4:
        title_slug = parts[-1]
        # Convert slug to title
        title = title_slug.replace('-', ' ').title()
        return title, title_slug
    return "Untitled", "untitled"

def download_and_convert_to_pdf(url, date_str, output_dir):
    """Download article and convert to PDF with 70% font scaling."""
    title, slug = get_article_title(url)

    # Create filename with date prefix for alphabetical sorting
    filename = f"{date_str}_{slug}.pdf"
    output_path = os.path.join(output_dir, filename)

    # Skip if already exists
    if os.path.exists(output_path):
        print(f"Skipping (already exists): {filename}")
        return output_path

    print(f"Processing: {date_str} - {title}")
    print(f"  URL: {url}")

    try:
        # Download HTML content using requests
        response = requests.get(url, timeout=30)
        response.raise_for_status()

        # CSS to scale font to 70%
        # We'll use a combination of zoom and font-size
        scale_css = CSS(string='''
            @page {
                size: A4;
                margin: 1cm;
            }
            body {
                font-size: 70%;
                transform-origin: top left;
            }
        ''')

        # Convert HTML to PDF with 70% scaling
        html = HTML(string=response.text, base_url=url)
        html.write_pdf(output_path, stylesheets=[scale_css])

        print(f"  ✓ Created: {filename}")
        return output_path
    except Exception as e:
        print(f"  ✗ Error converting {filename}: {str(e)}")
        return None

def create_zip(pdf_files, zip_path):
    """Create a zip file containing all PDFs."""
    print(f"\nCreating zip file: {zip_path}")
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for pdf_file in pdf_files:
            if pdf_file and os.path.exists(pdf_file):
                arcname = os.path.basename(pdf_file)
                zipf.write(pdf_file, arcname)
                print(f"  Added: {arcname}")
    print(f"✓ Zip file created: {zip_path}")

def main():
    """Main function to orchestrate the download and conversion."""
    # Create output directory
    output_dir = "/home/user/miro-plan-helper/lostgarden_pdfs"
    os.makedirs(output_dir, exist_ok=True)

    print("Fetching article list from sitemap...")
    articles = get_all_articles()
    print(f"Found {len(articles)} articles\n")

    # Download and convert each article
    pdf_files = []
    for i, (url, date_str) in enumerate(articles, 1):
        print(f"[{i}/{len(articles)}]", end=" ")
        pdf_path = download_and_convert_to_pdf(url, date_str, output_dir)
        if pdf_path:
            pdf_files.append(pdf_path)

    # Create zip file
    zip_path = "/home/user/miro-plan-helper/lostgarden_articles.zip"
    create_zip(pdf_files, zip_path)

    print(f"\n{'='*60}")
    print(f"Complete! {len(pdf_files)} PDFs created and zipped.")
    print(f"Output directory: {output_dir}")
    print(f"Zip file: {zip_path}")
    print(f"{'='*60}")

if __name__ == "__main__":
    main()
