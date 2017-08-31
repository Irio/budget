class AmendmentParser:
    """
    Class to parse contents from a list of arguments (as received
    from a Apache Spark PDF preprocessor) into a dictionary,
    with all expected attributes.
    """

    def __init__(self, attributes):
        self.attrs = attributes

    def parse_page(self):
        """
        Parse attributes.
        """
        self._join_splitted_author()
        amendment = {
            'file_generation_date': self.attribute('Data:', 1),
            'file_generation_time': self.attribute('Hora:', 1),
            'total_page_summary': self.attribute('Página:', 1),
            'author_page_summary': self.attribute('Página:', 2),
            'author': self.attribute('AUTOR DA EMENDA', 2),
            'number': self.attribute('EMENDA', 2),
            'destination': self.attrs[9],
        }
        if amendment['destination'] == 'ESPELHO DE EMENDA DE APROPRIAÇÃO DE DESPESA':
            self._fix_broken_intervention()
            self._join_splitted_intervention()
            amendment.update({
                'category': self.attribute('MODALIDADE DA EMENDA', 2),
                'type': self.attribute('TIPO DE EMENDA', 2),
                'department': self.attribute('ÁREA DE GOVERNO', 1),
                'intervention_code': self.attribute('MODALIDADE DE INTERVENÇÃO', 2),
                'intervention': self.attribute('MODALIDADE DE INTERVENÇÃO', 3),
                'achievement_code': self.attribute('TIPO DE REALIZAÇÃO PRETENDIDA', 3),
                'achievement': self.attribute('TIPO DE REALIZAÇÃO PRETENDIDA', 4),
                'location': self.attribute('LOCALIDADE BENEFICIADA', 1),
                'additional_value': self.attribute('TOTAL ........', 1),
            })
        elif amendment['destination'] == 'ESPELHO DE EMENDAS AO TEXTO DA LEI':
            amendment.update({
                'category': self.attribute('MODALIDADE DA EMENDA', 3),
                'type': self.attribute('TIPO DE EMENDA', 3),
                'reference': self.attribute('REFERÊNCIA', 3),
                'proposed_wording': self.attribute('TEXTO PROPOSTO', 1),
                'justification': self.justification(),
            })
        return amendment

    def attribute(self, reference, element_diff):
        if reference in self.attrs:
            value_index = self.attrs.index(reference)
            return self.attrs[value_index + element_diff]

    def justification(self):
        if 'JUSTIFICATIVA' in self.attrs:
            return '\n'.join(self.attrs[self.attrs.index('JUSTIFICATIVA') + 1:])

    def _join_splitted_author(self):
        """
        Identify if an author is contained in the page and needs to have
        have values merged (sometimes in the PDF text extraction,
        author gets splitted into multiple values).
        """
        has_attributes = 'AUTOR DA EMENDA' in self.attrs and \
                         'MODALIDADE DA EMENDA' in self.attrs
        if has_attributes:
            title1_index = self.attrs.index('AUTOR DA EMENDA')
            title2_index = self.attrs.index('MODALIDADE DA EMENDA')
            author_index = title1_index + 2
            author_part2_index = author_index + 1
            for index in range(author_part2_index, title2_index - 1):
                self.attrs[author_index] += ' ' + self.attrs[author_part2_index]
                del(self.attrs[author_part2_index])

    def _join_splitted_intervention(self):
        has_attributes = 'MODALIDADE DE INTERVENÇÃO' in self.attrs and \
                         'LOCALIDADE BENEFICIADA' in self.attrs
        if has_attributes:
            title1_index = self.attrs.index('MODALIDADE DE INTERVENÇÃO')
            title2_index = self.attrs.index('LOCALIDADE BENEFICIADA')
            author_index = title1_index + 3
            author_part2_index = author_index + 1
            for index in range(author_part2_index, title2_index - 2):
                self.attrs[author_index] += ' ' + self.attrs[author_part2_index]
                del(self.attrs[author_part2_index])

    def _fix_broken_intervention(self):
        values = [
            'PSB: Apoio CRAS/Centro:Convivência-Juventude-Criança- 285',
            'PSE:CREAS/Abrigo/ILPI/República/CasaLar/CentroDia/PessoaDe 285',
        ]
        values = [value
                  for value in values
                  if value in self.attrs]
        if any(values):
            value = values[0]
            index = self.attrs.index(value)
            self.attrs[index] = value[:-4] + self.attrs[index + 2]
            del(self.attrs[index + 2])
            self.attrs.insert(index + 1, value[-3:])
