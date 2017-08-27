# Budget

*Unveiling where the Brazilian Congress is targeting federal money.*

## Setup

```console
$ docker-compose build
$ docker-compose run scraper python -m unittest
```

## Collect data

```console
$ docker-compose run scraper scrapy crawl chamber_of_deputies \
  --output /mnt/data/chamber_of_deputies.json
  ```
