import json
import requests
from config import keys


class APIException(Exception):
    pass


class CryptoConverter:
    @staticmethod
    def get_price(base: str, quote: str, amount: str):
        if quote == base:
            raise APIException(f'Невозможно перевести одинаковые валюты {base}')

        try:
            base_ticker = keys[base]
        except KeyError:
            raise APIException(f'Не удалось обработать валюту {base}')

        try:
            quote_ticker = keys[quote]
        except KeyError:
            raise APIException(f'Не удалось обработать валюту {quote}')

        try:
            amount = float(amount)
        except ValueError:
            raise APIException(f'Не удалось обработать количество {amount}')

        r = requests.get(
            f'http://api.exchangeratesapi.io/v1/latest?access_key=eb31c4cffbc684e2f7616d77a22a634b&symbols={quote_ticker},{base_ticker}')
        rates = r.json()['rates']

        if base_ticker not in rates or quote_ticker not in rates:
            raise APIException('Ошибка в получении курса валют')

        # Расчитываем количество quote_ticker на основе base_ticker и amount
        rate = rates[quote_ticker] / rates[base_ticker]
        total_base = rate * amount

        return total_base

