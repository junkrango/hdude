import scrapy
from scrapy.spiders import CrawlSpider
from hdude.items import HdudeItem
import re


class HdudeSpider(CrawlSpider):
    name = 'hdude'
    start_urls = ['http://hentaidude.com/']

    def parse(self, response):
        self.log('parsing index page: %s' % response.url)
        anime_list = response.xpath('//section[@id="content"]/div[@class="videoPost"]')
        for anime in anime_list:
            item = HdudeItem()
            item['name'] = anime.xpath('a[@class="videoLink"]/text()').extract_first()
            item['url'] = anime.xpath('a[@class="videoLink"]/@href').extract_first()
            item['cover_image'] = anime.xpath('a[@class="thlink"]/div/img/@src').extract_first()
            item['like_count'] = anime.xpath('a[@class="heartLink"]/text()').extract_first()
            item['view_count'] = anime.xpath('*[@class="thumbViews"]/text()').extract_first()
            if item['url']:
                # 抓取详情页，并将列表页面获取的 item 信息用 meta 传递过去
                yield scrapy.Request(item['url'], callback=self.parse_content, meta={'item': item})
        # 继续抓取下个分页
        next_page = response.xpath('//div[@class="navigation"]/ul/li/a[contains(text(),"Next >")]/@href')\
            .extract_first()
        if next_page:
            yield scrapy.Request(next_page, callback=self.parse)

    def parse_content(self, response):
        # 详情页面提取视频地址和标签
        self.log('parsing detail page: %s' % response.url)
        item = response.meta['item']
        sources = re.findall(r'sources\[\'video-source-[0-9]\'\] = \'(.*?)\';',
                             response.xpath('//body').extract_first())

        if sources:
            sources = [source for source in sources if source.startswith('http')]   # 过滤掉 iframe 视频源
            item['source'] = sources[0]
            item['sources'] = '|'.join(sources)
        tags = response.xpath('//div[@class="new-tags"]/a/text()').extract()
        if tags:
            item['tags'] = ','.join(tags)
        yield item
