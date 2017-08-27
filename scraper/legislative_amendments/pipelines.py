# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import re


class TargetLocationPipeline(object):
    UFS = {
        'Acre': 'AC',
        'Alagoas': 'AL',
        'Amapá': 'AP',
        'Amazonas': 'AM',
        'Bahia': 'BA',
        'Ceará': 'CE',
        'Espírito Santo': 'ES',
        'Goiás': 'GO',
        'Maranhão': 'MA',
        'Mato Grosso': 'MT',
        'Mato Grosso do Sul': 'MS',
        'Minas Gerais': 'MG',
        'Pará': 'PA',
        'Paraíba': 'PB',
        'Paraná': 'PR',
        'Pernambuco': 'PE',
        'Piauí': 'PI',
        'Rio de Janeiro': 'RJ',
        'Rio Grande do Norte': 'RN',
        'Rio Grande do Sul': 'RS',
        'Rondônia': 'RO',
        'Roraima': 'RR',
        'Santa Catarina': 'SC',
        'São Paulo': 'SP',
        'Sergipe': 'SE',
        'Tocantins': 'TO',
    }

    def process_item(self, item, spider):
        description = re.sub(r'(?<=\w)\-(?=\w{2}$)', ' - ', item['description']).replace('¿', '-')
        sections = description.split(' - ')
        lower_description = description.lower()

        if 'limoeiro de anadia' in lower_description:
            item['target_location'] = 'Limoeiro de Anadia - AL'
        elif 'pedra redonda - pi' in lower_description:
            item['target_location'] = 'PI'
        elif 'centro de tecnologia da informação renato archer' in lower_description:
            item['target_location'] = 'Campinas - SP'
        elif 'na br-116/rj' in lower_description or 'uerj' in lower_description:
            item['target_location'] = 'RJ'
        elif 'prestação de serviços médico-hospitalares do hospital das forças armadas' in lower_description:
            item['target_location'] = 'Rio de Janeiro - RJ'
        elif '11ª região da justiça do trabalho - am, rr' in lower_description or \
             '14ª região da justiça do trabalho - ac, ro' in lower_description:
            item['target_location'] = 'Norte'
        elif item['code'] == '27.812.2035.5450.7222':
            item['target_location'] = 'Agrestina - PE'
        elif 'no município d' in lower_description:
            item['target_location'] = description.split('unicípio d')[-1][2:]
            if 'no estado d' in lower_description:
                sections = item['target_location'].split(' - ')
                city = ' - '.join(sections[:-1])
                uf = self.UFS[sections[-1][13:]]
                item['target_location'] = '{} - {}'.format(city, uf)
        elif 'no estado d' in lower_description:
            item['target_location'] = self.UFS[sections[-1][13:]]
        elif 'em municípios do estado de' in lower_description:
            item['target_location'] = self.UFS[sections[-1][27:]]
        elif 'no distrito federal' in lower_description or \
             'pcdf' in lower_description:
            item['target_location'] = 'DF'
        elif 'região metropolitana' in lower_description:
            matches = re.search(r'([a-zA-Z]{2})$', description)
            if matches:
                item['target_location'] = matches[1]
            else:
                if 'macapá' in lower_description:
                    item['target_location'] = 'AM'
                elif 'manaus' in lower_description:
                    item['target_location'] = 'MA'
                elif 'rio de janeiro' in lower_description:
                    item['target_location'] = 'RJ'
                else:
                    raise NotImplementedError
        elif 'na região' in lower_description:
            item['target_location'] = sections[-1][10:]
        elif 'nacional' in lower_description:
            item['target_location'] = sections[-1]
        elif 'no exterior' in lower_description:
            item['target_location'] = 'Exterior'
        elif 'na amazônia legal' in lower_description:
            item['target_location'] = sections[-1][3:]
        elif 'reserva de contingência fiscal' in lower_description:
            item['target_location'] = None
        else:
            item['target_location'] = ' - '.join(description.split(' - ')[-2:])
            assert ' - ' in item['target_location']

        if item['target_location'][-1] == '.':
            item['target_location'] = item['target_location'][:-1]
        return item
