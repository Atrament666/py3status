# -*- coding: utf-8 -*-
"""
Display foreign exchange rates using fixer.io API.

Configuration parameters:
    base: Base currency used for exchange rates (default 'EUR')
    cache_timeout: How often we refresh this module in seconds (default 600)
    format: Format of the output.  This is also where requested currencies are
        configured. Add the currency code surrounded by curly braces and it
        will be replaced by the current exchange rate.
        (default '${USD} £{GBP} ¥{JPY}')

@author Atrament
@license BSD

SAMPLE OUTPUT
{'full_text': u'$1.0617 \xa30.8841 \xa5121.5380'}
"""

URL='http://api.fixer.io/latest?base'


class Py3status:
    """
    """
    # available configuration parameters
    base = 'EUR'
    cache_timeout = 600
    format = u'${USD} £{GBP} ¥{JPY}'

    def post_config_hook(self):
        self.request_timeout = 20
        self.currencies = self.py3.get_placeholders_list(self.format)
        # create url
        currencies = ['"%s%s"' % (self.base, cur) for cur in self.currencies]
        self.data_url = URL + self.base
        # cache for rates data as sometimes we do not receive valid data
        self.rates_data = {currency: '?' for currency in self.currencies}

    def rates(self):
        try:
            result = self.py3.request(self.data_url, timeout=self.request_timeout)
        except (self.py3.RequestException):
            result = None
        rates = []
        if result:
            data = result.json()
            try:
                rates = data['rates']
            except (KeyError, TypeError):
                pass

        for rate in self.rates_data:
            self.rates_data[rate] = rates[rate]

        return {
            'full_text': self.py3.safe_format(self.format, self.rates_data),
            'cached_until': self.py3.time_in(self.cache_timeout),
        }


if __name__ == "__main__":
    """
    Run module in test mode.
    """
    from py3status.module_test import module_test
    module_test(Py3status)
