# Budget

*Unveiling where the Brazilian Congress is targeting federal money.*

## Setup

```console
$ brew install xpdf
$ python -m unittest
```

## Data collection

Data comes directly from the [official Chamber of Deputies website](http://www2.camara.leg.br/orcamento-da-uniao/leis-orcamentarias/loa/ob_loa_consulta_emendas).

```console
$ cd scraper
$ scrapy crawl chamber_of_deputies -a year=2017 \
  --output ../data/chamber_of_deputies_2017.json
$ cd ..
  ```

And this is an ugly script to generate a single CSV from everything in this project, including both seacheable information and data available only in PDFs. Code to be included in the main codebase soon. Wanna help? Open an issue.

```python
from budget.chamber_of_deputies.text_file_parser import TextFileParser
import pandas as pd

data = pd.DataFrame()
for year in range(2009, 2018):
    subset = pd.read_json('data/chamber_of_deputies_{}.json'.format(year),
                          orient='records')
    data = data.append(subset)

parser = TextFileParser('data/full/*.txt')
pdf_data = parser.dataframe()
data['_id'] = data['_id'].str.replace(' ', '')
data = data[['_id', 'commitment_info_url', 'urls']]
df = pdf_data.merge(data, left_on='number', right_on='_id', how='left')
df.drop_duplicates(['number', 'file_generation_date', 'author'], inplace=True)
del(df['_id'])
df['urls'] = df['urls'].apply(lambda x: isinstance(x, list) and x[0] or None)
df = df[df['category'].notnull() & df['urls'].notnull()]
df.rename(columns={'urls': 'url'}, inplace=True)
df.to_csv('data/amendments.csv', index=False)
```
