from Docling_Main.docling.utils.sitemap import get_sitemap_urls

def main():
    # Get sitemap URLs from langchain.com
    sitemap_urls = get_sitemap_urls("https://www.langchain.com/")
    
    # Print each URL
    print("Sitemap URLs from https://www.langchain.com/:")
    for i, url in enumerate(sitemap_urls, 1):
        print(f"{i}. {url}")
    
    print(f"\nTotal URLs found: {len(sitemap_urls)}")

if __name__ == "__main__":
    main()
