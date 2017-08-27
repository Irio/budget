import shutil
import tempfile
from unittest import TestCase

import pandas as pd

from budget.chamber_of_deputies.amendment_parser import AmendmentParser


class TestAmendmentParser(TestCase):
    def setUp(self):
        path = 'budget/tests/fixtures/amendment_attributes.csv'
        self.attributes = pd.read_csv(path, dtype=str)

    def fixture_by_index(self, index):
        return [attr
                for attr in self.attributes.iloc[index].values.tolist()
                if not isinstance(attr, float)]

    def test_parse_simple(self):
        # http://www.camara.leg.br/internet/comissao/index/mista/orca/orcamento/OR2017/emendas/despesa/P5563_AV_LOA_AUTOR2_3841.pdf#page=1
        subject = AmendmentParser(self.fixture_by_index(0))
        result = subject.parse_page()

        self.assertEqual('20/10/2016', result['file_generation_date'])
        self.assertEqual('21:34', result['file_generation_time'])
        self.assertEqual('3403 de 7916', result['total_page_summary'])
        self.assertEqual('1 de 10', result['author_page_summary'])
        self.assertEqual('3841 - Jones Martins', result['author'])
        self.assertEqual('38410001', result['number'])
        self.assertEqual('Individual', result['category'])
        self.assertEqual('Apropriação - Inclusão', result['type'])
        self.assertEqual('Defesa Nacional', result['department'])
        self.assertEqual('434', result['intervention_code'])
        self.assertEqual('Implantação/Instalação/Ampliação', result['intervention'])
        self.assertEqual('167', result['achievement_code'])
        self.assertEqual('Instalações/Equip.Militares', result['achievement'])
        self.assertEqual('4300000 - Rio Grande do Sul', result['location'])
        self.assertEqual('100.000', result['extra_value'])

    def test_parse_splitted_author_bancada_mato_grosso_do_sul(self):
        # http://www.camara.leg.br/internet/comissao/index/mista/orca/orcamento/OR2017/emendas/despesa/P5563_AV_LOA_AUTOR2_7113.pdf#page=14
        subject = AmendmentParser(self.fixture_by_index(1))
        result = subject.parse_page()

        self.assertEqual('20/10/2016', result['file_generation_date'])
        self.assertEqual('21:35', result['file_generation_time'])
        self.assertEqual('7451 de 7916', result['total_page_summary'])
        self.assertEqual('14 de 15', result['author_page_summary'])
        self.assertEqual('7113 - Bancada do Mato Grosso do Sul', result['author'])
        self.assertEqual('71130014', result['number'])
        self.assertEqual('Bancada Estadual', result['category'])
        self.assertEqual('Apropriação - Inclusão', result['type'])
        self.assertEqual('Irrigação e Integração Nacional', result['department'])
        self.assertEqual('591', result['intervention_code'])
        self.assertEqual('Promoção/Fomento do/da', result['intervention'])
        self.assertEqual('987', result['achievement_code'])
        self.assertEqual('Desenvolvimento Economico', result['achievement'])
        self.assertEqual('5000000 - Mato Grosso do Sul', result['location'])
        self.assertEqual('100.000.000', result['extra_value'])

    def test_parse_splitted_author_professora_dorinha_seabra_rezende(self):
        # http://www.camara.leg.br/internet/comissao/index/mista/orca/orcamento/OR2017/emendas/despesa/P5563_AV_LOA_AUTOR2_2693.pdf#page=11
        subject = AmendmentParser(self.fixture_by_index(2))
        result = subject.parse_page()

        self.assertEqual('20/10/2016', result['file_generation_date'])
        self.assertEqual('21:33', result['file_generation_time'])
        self.assertEqual('5703 de 7916', result['total_page_summary'])
        self.assertEqual('11 de 11', result['author_page_summary'])
        self.assertEqual('2693 - Professora Dorinha Seabra Rezende', result['author'])
        self.assertEqual('26930011', result['number'])
        self.assertEqual('Individual', result['category'])
        self.assertEqual('Apropriação - Inclusão', result['type'])
        self.assertEqual('Defesa Nacional', result['department'])
        self.assertEqual('028', result['intervention_code'])
        self.assertEqual('Apoio Comunitário', result['intervention'])
        self.assertEqual('805', result['achievement_code'])
        self.assertEqual('Cooperação', result['achievement'])
        self.assertEqual('1721000 - Palmas', result['location'])
        self.assertEqual('100.000', result['extra_value'])

    def test_parse_splitted_author_bancada_rio_grande_do_norte(self):
        # http://www.camara.leg.br/internet/comissao/index/mista/orca/orcamento/OR2017/emendas/despesa/P5563_AV_LOA_AUTOR2_7121.pdf#page=3
        subject = AmendmentParser(self.fixture_by_index(3))
        result = subject.parse_page()

        self.assertEqual('20/10/2016', result['file_generation_date'])
        self.assertEqual('21:35', result['file_generation_time'])
        self.assertEqual('7580 de 7916', result['total_page_summary'])
        self.assertEqual('3 de 15', result['author_page_summary'])
        self.assertEqual('7121 - Bancada do Rio Grande do Norte', result['author'])
        self.assertEqual('71210003', result['number'])
        self.assertEqual('Bancada Estadual', result['category'])
        self.assertEqual('Apropriação - Inclusão', result['type'])
        self.assertEqual('Saúde', result['department'])
        self.assertEqual('990', result['intervention_code'])
        self.assertEqual('Atipica / Outras', result['intervention'])
        self.assertEqual('334', result['achievement_code'])
        self.assertEqual('Sem Previsão (Atípico) - Adequar UO-Subf-Prog-Ação-Subt.',
                         result['achievement'])
        self.assertEqual('2400000 - Rio Grande do Norte', result['location'])
        self.assertEqual('40.000.000', result['extra_value'])

    def test_parse_splitted_author_bancada_rio_grande_do_sul(self):
        # http://www.camara.leg.br/internet/comissao/index/mista/orca/orcamento/OR2017/emendas/despesa/P5563_AV_LOA_AUTOR2_7122.pdf#page=3
        subject = AmendmentParser(self.fixture_by_index(4))
        result = subject.parse_page()

        self.assertEqual('20/10/2016', result['file_generation_date'])
        self.assertEqual('21:35', result['file_generation_time'])
        self.assertEqual('7595 de 7916', result['total_page_summary'])
        self.assertEqual('3 de 18', result['author_page_summary'])
        self.assertEqual('7122 - Bancada do Rio Grande do Sul', result['author'])
        self.assertEqual('71220003', result['number'])
        self.assertEqual('Bancada Estadual', result['category'])
        self.assertEqual('Apropriação - Inclusão', result['type'])
        self.assertEqual('Agricultura e Desenvolvimento Agrário', result['department'])
        self.assertEqual('004', result['intervention_code'])
        self.assertEqual('Fomento a(o)', result['intervention'])
        self.assertEqual('761', result['achievement_code'])
        self.assertEqual('Setor Agropecuário', result['achievement'])
        self.assertEqual('4300000 - Rio Grande do Sul', result['location'])
        self.assertEqual('100.000.000', result['extra_value'])

    def test_parse_sequence_page(self):
        # http://www.camara.leg.br/internet/comissao/index/mista/orca/orcamento/OR2012/emendas/despesa/CARLOSFX_AV_LOA_AUTOR2_2818.pdf#page=4
        subject = AmendmentParser(self.fixture_by_index(5))
        result = subject.parse_page()

        self.assertEqual('25/11/2011', result['file_generation_date'])
        self.assertEqual('01:07', result['file_generation_time'])
        self.assertEqual('8183 de 9656', result['total_page_summary'])
        self.assertEqual('5 de 15', result['author_page_summary'])
        self.assertEqual('2818 - Tiririca', result['author'])
        self.assertEqual('28180004', result['number'])
        self.assertIsNone(result['category'])
        self.assertIsNone(result['type'])

    def test_parse_suppressive_amendment(self):
        # http://www.camara.gov.br/internet/comissao/index/mista/orca/orcamento/OR2017/emendas/despesa/P5563_AV_LOA_AUTOR2_2868.pdf#page=11
        subject = AmendmentParser(self.fixture_by_index(6))
        result = subject.parse_page()

        self.assertEqual('20/10/2016', result['file_generation_date'])
        self.assertEqual('21:32', result['file_generation_time'])
        self.assertEqual('5121 de 7916', result['total_page_summary'])
        self.assertEqual('11 de 11', result['author_page_summary'])
        self.assertEqual('2868 - Nelson Marchezan Junior', result['author'])
        self.assertEqual('28680010', result['number'])
        self.assertEqual('Individual', result['category'])
        self.assertEqual('Supressiva', result['type'])
        self.assertEqual('Inciso I Alinea 2 Item 2', result['reference'])
        self.assertEqual('Suprima-se o texto atual.', result['wording_proposal'])
        self.assertEqual('Devido a crise econômica que o Brasil enfrenta, os recursos para aumento de salário para servidores devem ser suspensos de todos os poderes. Para tanto, é necessário\ncancelar a autorização do Anexo V e os recursos correspondentes à ação 0Z01.',
                         result['justification'])

    def test_parse_splitted_intervention(self):
        # http://www.camara.leg.br/internet/comissao/index/mista/orca/orcamento/or2009/emendas/despesa/DANIELRJ_AV_LOA_AUTOR2_1970.pdf#page=11
        subject = AmendmentParser(self.fixture_by_index(7))
        result = subject.parse_page()

        self.assertEqual('17/11/2008', result['file_generation_date'])
        self.assertEqual('21:32', result['file_generation_time'])
        self.assertEqual('8258 de 9842', result['total_page_summary'])
        self.assertEqual('11 de 11', result['author_page_summary'])
        self.assertEqual('1970 - Takayama', result['author'])
        self.assertEqual('19700011', result['number'])
        self.assertEqual('Individual', result['category'])
        self.assertEqual('Apropriação - Inclusão', result['type'])
        self.assertEqual('Saúde', result['department'])
        self.assertEqual('040', result['intervention_code'])
        self.assertEqual('Saneamento em Área Rural, Especial ou com menos 2.500 habit',
                         result['intervention'])
        self.assertEqual('436', result['achievement_code'])
        self.assertEqual('Saneamento em Área Rural', result['achievement'])
        self.assertEqual('4100000 - Paraná', result['location'])
        self.assertEqual('100.000', result['extra_value'])

    def test_parse_broken_intervention(self):
        # http://www.camara.leg.br/internet/comissao/index/mista/orca/orcamento/OR2014/emendas/despesa/P5563_AV_LOA_AUTOR2_2491.pdf#page=5
        subject = AmendmentParser(self.fixture_by_index(8))
        result = subject.parse_page()

        self.assertEqual('02/12/2013', result['file_generation_date'])
        self.assertEqual('22:00', result['file_generation_time'])
        self.assertEqual('4499 de 8807', result['total_page_summary'])
        self.assertEqual('5 de 10', result['author_page_summary'])
        self.assertEqual('2491 - Lelo Coimbra', result['author'])
        self.assertEqual('24910005', result['number'])
        self.assertEqual('Individual', result['category'])
        self.assertEqual('Apropriação - Inclusão', result['type'])
        self.assertEqual('Assistência Social', result['department'])
        self.assertEqual('192', result['intervention_code'])
        self.assertEqual('PSB: Apoio CRAS/Centro:Convivência-Juventude-Criança-Adolesc',
                         result['intervention'])
        self.assertEqual('285', result['achievement_code'])
        self.assertEqual('Atenção à Familia/Criança/Adolesc./Idoso/Pessoa c/defic.',
                         result['achievement'])
        self.assertEqual('3200000 - Espírito Santo', result['location'])
        self.assertEqual('500.000', result['extra_value'])

    def test_parse_broken_intervention2(self):
        # http://www.camara.leg.br/internet/comissao/index/mista/orca/orcamento/OR2016/emendas/despesa/ANDRELUF_AV_LOA_AUTOR2_1277.pdf#page=7
        subject = AmendmentParser(self.fixture_by_index(9))
        result = subject.parse_page()

        self.assertEqual('21/10/2015', result['file_generation_date'])
        self.assertEqual('18:00', result['file_generation_time'])
        self.assertEqual('7343 de 8157', result['total_page_summary'])
        self.assertEqual('7 de 18', result['author_page_summary'])
        self.assertEqual('1277 - Wellington Roberto', result['author'])
        self.assertEqual('12770007', result['number'])
        self.assertEqual('Individual', result['category'])
        self.assertEqual('Apropriação - Inclusão', result['type'])
        self.assertEqual('Assistência Social', result['department'])
        self.assertEqual('193', result['intervention_code'])
        self.assertEqual('PSE:CREAS/Abrigo/ILPI/República/CasaLar/CentroDia/PessoaDef.',
                         result['intervention'])
        self.assertEqual('285', result['achievement_code'])
        self.assertEqual('Atenção à Familia/Criança/Adolesc./Idoso/Pessoa c/defic.',
                         result['achievement'])
        self.assertEqual('2507507 - João Pessoa', result['location'])
        self.assertEqual('100.000', result['extra_value'])
