import scrapy
import json


class AllSpider(scrapy.Spider):
    name = "all"
    start_urls = ["m.facebook.com"]

    headers = {
        "Accept": "application/json",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "en-US,en;q=0.9,hi;q=0.8,lb;q=0.7",
        "Referer": "https://directory.ntschools.net/",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36",
        "X-Requested-With": "Fetch",
    }

    def parse(self, response):
        yield scrapy.Request(
            url="https://directory.ntschools.net/api/System/GetAllSchools",
            callback=self.parse_json,
            headers=self.headers,
        )

    def parse_json(self, response):
        raw_json = response.body
        data = json.loads(raw_json)

        for school in data:
            school_code = school["itSchoolCode"]
            yield scrapy.Request(
                f"https://directory.ntschools.net/api/System/GetSchool?itSchoolCode={school_code}",
                callback=self.parse_school,
                headers=self.headers,
            )

    def parse_school(self, response):
        data = json.loads(response.body)

        yield {
            "name": data["name"],
            "telephoneNumber": data["telephoneNumber"],
            "mail": data["mail"],
            "physicalAddress": data["physicalAddress"]["displayAddress"],
            "postalAddress": data["postalAddress"]["displayAddress"],
        }
