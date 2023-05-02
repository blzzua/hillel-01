import logging

from currencies.models import Currency
from currencies.clients.api_base_client import APIBaseClient
from decimal import Decimal


class NBUData(APIBaseClient):
    base_url = 'https://bank.gov.ua/NBU_Exchange/exchange'

    def _prepare_data(self) -> list:
        """
        :return: сщк
        """
        self._request('get', params={'json': ''})
        print(self.response)
        if self.response.status_code == 200:
            self.response_object = self.response.json()

        else:
            print('error', self.response.status_code)
            raise ValueError(f'Wrong response {self.response.json()}')

    def save(self):
        try:
            UAH_COIN = Currency.objects.get(code='UAH').amount
            self._prepare_data()

            for ticker in ['USD', 'EUR']:
                nbu_data = next(filter(lambda x: x.get('CurrencyCodeL') == ticker, self.response_object))
                nbu_amount = Decimal(nbu_data.get('Amount'))
                nbu_units = Decimal(nbu_data.get('Units'))
                cross_coin_amount = nbu_amount * UAH_COIN
                Currency.objects.update_or_create(
                    code=ticker,
                    defaults={'amount': cross_coin_amount, 'units': nbu_units}
                )
        except (ValueError, ) as e:
            logging.error(f'error on parsing response {e}')


world_ccy_to_uah_client = NBUData()
