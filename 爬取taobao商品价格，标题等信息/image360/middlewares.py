# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
from scrapy.http import HtmlResponse
from selenium import webdriver
from selenium.common.exceptions import TimeoutException


class Image360SpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class Image360DownloaderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:

        # 返回None, 继续执行下面的中间件，直到下载器
        # - return None: continue processing this request

        # 不需要下载器，自己下载，走到蜘蛛
        # - or return a Response object

        # 走到调度器
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called

        # 代理
        # request.meta['proxy'] = ''

        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class TaobaoDownloaderMiddleWare(object):

    def __init__(self, timeout=None):
        self.timeout = timeout
        # 如果需要使用代理，可以自己配置代理服务器CCProxy/ TinyProxy / Squid
        # 也可以购买国内比较有名的代理服务器提供商的服务 快代理， 讯代理， 阿布云代理，
        # 代理池 -- 管理和维护一系列的代理并每次提供随机的代理

        # 给selenium 设置代理
        # options = webdriver.ChromeOptions()
        # options.add_argument('--proxy-server=http://uid:pwd@1.1.1.1:8000')  一个完整的代理的写法
        # self.browser = webdriver.Chrome(options=options)

        self.browser = webdriver.Chrome()
        self.browser.set_window_size(1000, 600)
        self.browser.set_page_load_timeout(self.timeout)

    def __del__(self):
        self.browser.close()

    # 处理请求
    def process_request(self, request, spider):
        try:
            self.browser.get(request.url)
            return HtmlResponse(url=request.url, body=self.browser.page_source,
                                request=request, encoding='utf-8', status=200)
        except TimeoutException:
            return HtmlResponse(url=request.url, status=500, request=request)

    # 处理响应
    def process_response(self, request, response, spider):
        return response

    # 处理异常
    def process_exception(self, request, exception, spider):
        pass

    @classmethod
    def from_crawler(cls, crawler):
        return cls(timeout=10)
