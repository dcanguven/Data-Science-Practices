import scrapy


class BooksSpider(scrapy.Spider):
    name = "books"
    allowed_domains = ["dr.com.tr"]
    start_urls = ["https://www.dr.com.tr/Kategori_/Kitap/En-Yeniler/10001/3"]

    def parse(self, response):
        # Select all book elements
        books = response.css("div.prd-main-wrapper")
        
        for book in books:
            # Extract book name and price
            name = book.css("div.prd-infos h3.seo-heading a::text").get()
            author = book.css("div.prd-infos h3.seo-heading a.who.font-weight-bold::text").get()
            price = book.css("div.prd-prices div.prd-price::text").get()
            publisher = books.css("div.prd-content div.prd-content-wrapper div.prd-info-wrapper a.prd-publisher::text").get()
            
            
            if name and price:
                yield {
                    'name': name.strip(),
                    'author': author.strip(),
                    'price': price.strip(),
                    'publisher': publisher.strip()
                }

        # Pagination: Check for a next page
        next_page = response.css("li.pagination-next a::attr(href)").get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)