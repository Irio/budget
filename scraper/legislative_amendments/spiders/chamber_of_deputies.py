# -*- coding: utf-8 -*-
import datetime
import itertools
import re

import scrapy

from legislative_amendments.items import ChamberOfDeputiesAmendment


class ChamberOfDeputiesSpider(scrapy.Spider):
    name = 'chamber_of_deputies'
    allowed_domains = ['camara.gov.br', 'camara.leg.br']
    start_urls = [
        'http://www2.camara.leg.br'
        '/orcamento-da-uniao/leis-orcamentarias/loa/ob_loa_consulta_emendas'
    ]
    UFS = ['AC', 'AL', 'AM', 'AP', 'BA', 'CE', 'DF', 'ES', 'GO', 'MA', 'MG',
           'MS', 'MT', 'PA', 'PB', 'PE', 'PI', 'PR', 'RJ', 'RN', 'RO', 'RR',
           'RS', 'SC', 'SE', 'SP', 'TO']

    def __init__(self, year=None, *args, **kwargs):
        super(ChamberOfDeputiesSpider, self).__init__(*args, **kwargs)
        if year:
            self.year = year
        else:
            self.year = str(datetime.datetime.now().year)

    def start_requests(self):
        url = self.start_urls[0]
        form_data = {
            'ano': self.year,
            'autor': '',
            'form.button.submit': 'Pesquisar',
            'form.submitted': '1',
            'localidade': '',
            'momento': '39-10-99',  # option named "Redação Final - Autógrafo"
            'ordem': 'autor',
            'orgao': '',
            'partido': '',
            # 'uf': 'RS',
        }

        for uf in self.UFS:
            form_data['uf'] = uf
            yield scrapy.FormRequest(url, callback=self.parse, formdata=form_data)

    def parse(self, response):
        selector = '.tabela-padrao-bootstrap tr:not(:first-child)'
        elements = response.css(selector)
        for index in range(len(elements) // 2):
            header_node, info_node = elements[index * 2], elements[index * 2 + 1]
            yield self.parse_amendment(response, header_node, info_node)

    def parse_amendment(self, response, header_node, info_node):
        header_node = header_node.css('th::text')[0].extract().strip()
        author_info = header_node.split(' - ')
        assert len(author_info) == 2
        author_group = author_info[1].split('/')
        party = '/'.join(author_group[:-1])
        party = None if 'S/PARTIDO' in party else party
        urls = info_node.css('a::attr(href)').extract()
        page_number = re.search(r'page=(\d+)', urls[0])[1]
        _id = ''.join(info_node.css('td:first-child span::text').extract())
        about_node = info_node.css('td:nth-child(2) span::text').extract()
        description = ' - '.join(about_node[5:-1])
        target_location = about_node[-1]
        expenditure_group_id = info_node.css('td:nth-child(3) span::text')[0].extract()
        application_method_id = info_node.css('td:nth-child(4) span::text')[0].extract()
        value = info_node.css('td:nth-child(5) span::text')[0].extract()

        return ChamberOfDeputiesAmendment({
            '_id': _id,
            'application_method_id': application_method_id,
            'author': author_info[0],
            'code': '.'.join(about_node[:5]),
            'description': ' - '.join(about_node[5:7]),
            'expenditure_group_id': expenditure_group_id,
            'page_number': page_number,
            'party': party,
            'commitment_info_url': urls[1] if len(urls) > 1 else None,
            'state': author_group[-1],
            'urls': urls[0].split('#')[:1],
            'value': float(value.replace('.', '').replace(',', '.')),
            'year': self.year,
        })
