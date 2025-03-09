import scrapy
import json


class BehanceTrendsSpider(scrapy.Spider):
    name = "behance_trends"

    def start_requests(self):
        api_url = "https://cc-api-behance.adobe.io/v2/galleries/1/projects?api-key=ColorWeb&locale=en&ordinal=0&per_page=1"

        headers = {
            "Accept": "application/json",
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36",
            "Referer": "https://color.adobe.com",  # Fake request origin
            # Pretend the request is from Adobe's website
            "Origin": "https://color.adobe.com",
            "x-api-key": "ColorWeb",
        }

        yield scrapy.Request(url=api_url, headers=headers, callback=self.parse_api)

    def parse_api(self, response):
        if response.status == 403:
            self.logger.error(
                "Access Forbidden: The API is blocking the request.")
        elif response.status == 200:
            data = json.loads(response.text)  # Convert JSON response
            yield {"data": data}
        else:
            self.logger.warning(f"Unexpected response: {response.status}")
