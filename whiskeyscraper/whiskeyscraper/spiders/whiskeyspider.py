import scrapy


class WhiskeySpider(scrapy.Spider):
    name = "whisky"
    start_urls = ["https://www.whiskyshop.com/scotch-whisky?item_availability=In+Stock"]

    def parse(self, response):
        for products in response.css("div.product-item-info"):
            '''It uses yields instead of return'''
            try:
                yield {
                    'name': products.css("a.product-item-link::text").get(),
                    'price': products.css("span.price::text").get().replace("£", ''),
                    'link': products.css("a.product-item-link").attrib['href']
                }

            except:
                yield {
                    'name': products.css("a.product-item-link::text").get(),
                    'price': "Not Available at the momebnt",
                    'link': products.css("a.product-item-link").attrib['href']
                }

        next_page = response.css("a.action.next").attrib['href']
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)