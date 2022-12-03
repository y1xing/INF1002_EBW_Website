import scrapy
from scrapy.crawler import CrawlerRunner
from scrapy.utils.project import get_project_settings
from twisted.internet import reactor, defer


def scrape_hotel_links(start_url):
    link_list = []
    link_list_clean = []

    class ScraperSpider(scrapy.Spider):
        name = "scraper"
        start_urls = start_url

        def parse(self, response, **kwargs):
            # Gets all the hotel links from the page
            hotel_page_links = response.css(".a4225678b2 a::attr(href)").getall()
            # Gets the current page number
            current_page_num = int(response.css("li.f32a99c8d1.ebd02eda9e").get().split()[4].strip('"'))
            # Gets the number of pages
            num_of_pages = int(response.css("button.fc63351294.f9c5690c58::attr(aria-label)").getall()[-2].strip())
            # Appends the hotel links from the page to link_list
            yield {
                link_list.append(hotel_page_links),
            }
            # Checks if the crawler is on the last page
            # If it's not the last page the crawler moves onto the next page
            if current_page_num < num_of_pages:
                next_page = start_url[0] + "&offset=" + str(current_page_num * 25)
                yield scrapy.Request(next_page, callback=self.parse)

    settings = get_project_settings()
    runner = CrawlerRunner(settings)

    @defer.inlineCallbacks
    def crawl():
        yield runner.crawl(ScraperSpider)
        reactor.stop()

    crawl()  # Starts the crawler
    reactor.run()  # the script will block here until the last crawl call is finished

    for i in link_list:
        for j in i:
            # Makes sure the links are for hotels and that there are no duplicates
            if ("hotel" in j) and (j not in link_list_clean):
                # Cleans the link to comply with the functions in extraction
                link_list_clean.append((j.replace(".html", ".en-gb.html")).replace(j.split("&")[2].strip("aid="), "304142"))
    return link_list_clean
