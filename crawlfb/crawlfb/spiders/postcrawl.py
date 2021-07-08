# import scrapy
# import logging
#
# from scrapy.loader import ItemLoader
# from scrapy.http import FormRequest
# from scrapy.exceptions import CloseSpider
# from fbcrawl.items import FbcrawlItem, parse_date, parse_date2
# from datetime import datetime
#
#
# class FacebookSpider(scrapy.Spider):
#     '''
#     Parse FB pages (needs credentials)
#     '''
#     name = 'fb'
#     custom_settings = {
#         'FEED_EXPORT_FIELDS': ['source', 'shared_from', 'date', 'text', \
#                                'reactions', 'likes', 'ahah', 'love', 'wow', \
#                                'sigh', 'grrr', 'comments', 'post_id', 'url'],
#         'DUPEFILTER_CLASS': 'scrapy.dupefilters.BaseDupeFilter',
#     }
#
#     def __init__(self, *args, **kwargs):
#         # turn off annoying logging, set LOG_LEVEL=DEBUG in settings.py to see more logs
#         logger = logging.getLogger('scrapy.middleware')
#         logger.setLevel(logging.WARNING)
#
#         super().__init__(*args, **kwargs)
#
#         # email & pass need to be passed as attributes!
#         if 'email' not in kwargs or 'password' not in kwargs:
#             raise AttributeError('You need to provide valid email and password:\n'
#                                  'scrapy fb -a email="EMAIL" -a password="PASSWORD"')
#         else:
#             self.logger.info('Email and password provided, will be used to log in')
#
#         # page name parsing (added support for full urls)
#         if 'page' in kwargs:
#             if self.page.find('/groups/') != -1:
#                 self.group = 1
#             else:
#                 self.group = 0
#             if self.page.find('https://www.facebook.com/') != -1:
#                 self.page = self.page[25:]
#             elif self.page.find('https://mbasic.facebook.com/') != -1:
#                 self.page = self.page[28:]
#             elif self.page.find('https://m.facebook.com/') != -1:
#                 self.page = self.page[23:]
#
#         # parse date
#         if 'date' not in kwargs:
#             self.logger.info('Date attribute not provided, scraping date set to 2004-02-04 (fb launch date)')
#             self.date = datetime(2004, 2, 4)
#         else:
#             self.date = datetime.strptime(kwargs['date'], '%Y-%m-%d')
#             self.logger.info('Date attribute provided, fbcrawl will stop crawling at {}'.format(kwargs['date']))
#         self.year = self.date.year
#
#         # parse lang, if not provided (but is supported) it will be guessed in parse_home
#         if 'lang' not in kwargs:
#             self.logger.info('Language attribute not provided, fbcrawl will try to guess it from the fb interface')
#             self.logger.info('To specify, add the lang parameter: scrapy fb -a lang="LANGUAGE"')
#             self.logger.info('Currently choices for "LANGUAGE" are: "en", "es", "fr", "it", "pt"')
#             self.lang = '_'
#         elif self.lang == 'en' or self.lang == 'es' or self.lang == 'fr' or self.lang == 'it' or self.lang == 'pt':
#             self.logger.info('Language attribute recognized, using "{}" for the facebook interface'.format(self.lang))
#         else:
#             self.logger.info('Lang "{}" not currently supported'.format(self.lang))
#             self.logger.info('Currently supported languages are: "en", "es", "fr", "it", "pt"')
#             self.logger.info('Change your interface lang from facebook settings and try again')
#             raise AttributeError('Language provided not currently supported')
#
#         # max num of posts to crawl
#         if 'max' not in kwargs:
#             self.max = int(10e5)
#         else:
#             self.max = int(kwargs['max'])
#
#         # current year, this variable is needed for proper parse_page recursion
#         self.k = datetime.now().year
#         # count number of posts, used to enforce DFS and insert posts orderly in the csv
#         self.count = 0
#
#         self.start_urls = ['https://mbasic.facebook.com']
#
#     def parse(self, response):
#         '''
#         Handle login with provided credentials
#         '''
#         return FormRequest.from_response(
#             response,
#             formxpath='//form[contains(@action, "login")]',
#             formdata={'email': self.email, 'pass': self.password},
#             callback=self.parse_home
#         )
