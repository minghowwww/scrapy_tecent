# -*- coding: utf-8 -*-
import scrapy
from Tencent.items import TencentItem


class PosispiderSpider(scrapy.Spider):
    name = 'posiSpider'
    allowed_domains = ['http://hr.tencent.com']
    start_urls = ['http://hr.tencent.com/position.php?&start=0#a']

    def parse(self, response):

        node_list = response.xpath("//tr[@class='even'] | //tr[@class='odd']");

        for node in node_list:
            item = TencentItem()
            # print(node.xpath("td[1]/a/text()").extract())
            item['name'] = node.xpath("./td[1]/a/text()").extract()[0].encode("utf-8");

            if len(node.xpath("./td[2]/text()")) == 0:
                item['type'] = ""
            else:
                item['type'] = node.xpath("./td[2]/text()").extract()[0].encode("utf-8");

            item['number'] = node.xpath("./td[3]/text()").extract()[0].encode("utf-8");
            item['position'] = node.xpath("./td[4]/text()").extract()[0].encode("utf-8");
            item['time'] = node.xpath("./td[5]/text()").extract()[0].encode("utf-8");

            # print(dict(item))
            yield item

        if len(response.xpath("//a[@id='next' and @class = 'noactive']")) == 0:
            # position.php? & start = 10  # a
            url = response.xpath("//a[@id='next']/@href").extract()[0]
            print(url)
            yield scrapy.Request('http://hr.tencent.com/' + url, dont_filter=True, callback = self.parse);
        