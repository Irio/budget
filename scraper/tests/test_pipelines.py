from unittest import TestCase
from unittest.mock import MagicMock

from scraper.legislative_amendments.pipelines import TargetLocationPipeline


class TestTargetLocationPipeline(TestCase):
    def setUp(self):
        self.subject = TargetLocationPipeline()

    def test_process_item(self):
        spider = MagicMock()

        def assert_location(location, description, code=''):
            item = {'code': code, 'description': description}
            result = self.subject.process_item(item, spider)
            self.assertEqual(location, item['target_location'])

        assert_location('Nacional',
                        'Estruturação e Modernização de Unidades de Saúde das Forças Armadas - Nacional')
        assert_location('Amazônia Legal',
                        'Regularização da Estrutura Fundiária na Área de Abrangência da Lei 11.952, de 2009 - Na Amazônia Legal')
        assert_location('Sul',
                        'Apoio à Manutenção de Unidades de Saúde - Na Região Sul')
        assert_location('Exterior',
                        'Reconstrução da Estação Antártica Comandante Ferraz - No Exterior')
        assert_location('AM',
                        'Apoio à Infraestrutura para a Educação Básica - Na Região Metropolitana de Macapá')
        assert_location('TO',
                        'Apoio a Projetos de Infraestrutura Turística - Região Metropolitana de Palmas - TO')
        assert_location('AM',
                        'Apoio à Política Nacional de Desenvolvimento Urbano - Na Região Metropolitana de Manaus - No Estado do Amazonas')
        assert_location('RS',
                        'Estruturação de Unidades de Atenção Especializada em Saúde - No Estado do Rio Grande do Sul')
        assert_location('DF',
                        'Promoção e Fomento à Cultura Brasileira - No Distrito Federal')
        assert_location('PE',
                        'Promoção e Fomento à Cultura Brasileira - Em Municípios do Estado de Pernambuco')
        assert_location('SP',
                        'Estruturação de Unidades de Atenção Especializada em Saúde - No Estado de São Paulo')
        assert_location('Norte',
                        'Apreciação de Causas na Justiça do Trabalho - Na 11ª Região da Justiça do Trabalho - AM, RR')
        assert_location('Norte',
                        'Apreciação de Causas na Justiça do Trabalho - Na 14ª Região da Justiça do Trabalho - AC, RO')
        assert_location('Porto Alegre - RS',
                        'Estruturação de Unidades de Atenção Especializada em Saúde - Irmandade da Santa Casa de Misericórdia de Porto Alegre - Porto Alegre - RS.')
        assert_location('Rio de Janeiro - RJ',
                        'Prestação de Serviços Médico-Hospitalares do Hospital das Forças Armadas - Aquisição de Ambulância UTI')
        assert_location('Agrestina - PE',
                        'Implantação e Modernização de Infraestrutura para Esporte Educacional, Recreativo e de Lazer - Ampliação e Reforma de Campo de Futebol',
                        '27.812.2035.5450.7222')
