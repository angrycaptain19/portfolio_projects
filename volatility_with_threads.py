# -*- coding: utf-8 -*-

import os
import threading


class VolatilityParser(threading.Thread):

    def __init__(self, ticker_name, ticker_path, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ticker_name = ticker_name
        self.ticker_path = ticker_path
        self.secid = None
        self.trade_time = None
        self.price = None
        self.quantity = None
        self.half_sum = 0
        self.volatility = 0
        self.price_max = 0
        self.price_min = None

    def run(self):
        self.extract()
        self.volatility_calculation()

    def extract(self):
        with open(self.ticker_path, 'r', encoding='UTF8') as ticker_doc:
            ticker_doc.readline()
            for line in ticker_doc:
                line = line.rstrip()
                line = line.split(',')
                self.secid = line[0]
                self.trade_time = line[1]
                self.price = float(line[2])
                self.quantity = line[3]
                if self.price > self.price_max:
                    self.price_max = self.price
                if self.price < self.price_min or not self.price_min:
                    self.price_min = self.price

    def volatility_calculation(self):
        self.half_sum = (self.price_max + self.price_min) / 2
        self.volatility = ((self.price_max - self.price_min) / self.half_sum) * 100
        self.volatility = round(self.volatility, 2)


class TickerExtractor:

    def __init__(self, file_to_parse):
        self.file_to_parse = os.path.normpath(file_to_parse)
        self.tickers_paths = {}
        self.result_dict = {}

    def extractor(self):
        for dirpath, dirnames, filenames in os.walk(self.file_to_parse):
            for file in filenames:
                full_path = os.path.join(dirpath, file)
                self.tickers_paths[file[7:11]] = full_path

    def run(self):
        self.extractor()
        tickers = [VolatilityParser(ticker_name=name, ticker_path=path)
                   for name, path in self.tickers_paths.items()]
        for ticker in tickers:
            ticker.start()
        for ticker in tickers:
            ticker.join()
        for ticker in tickers:
            self.result_dict[ticker.ticker_name] = ticker.volatility
        self.report()

    def report(self):
        values_list = list(self.result_dict.items())
        values_list.sort(key=lambda i: i[1])
        val = []
        zero_values_list = []
        for num in values_list:
            if num[1] == 0.0:
                zero_values_list.append(num)
                continue
            else:
                val.append(num)
        zero_values_list.sort()
        min_volatility = dict(val[:3])
        max_volatility = dict(val[:-4:-1])
        print('Max volatility :')
        for item in max_volatility:
            print(f'    {item} - {max_volatility[item]}%')
        print('Min volatility :')
        for item in min_volatility:
            print(f'    {item} - {min_volatility[item]}%')
        print('Zero volatility :')
        for item in dict(zero_values_list):
            print(f'{item}', end=' ')


def main():
    file_test = 'trades'
    volatility_parser = TickerExtractor(file_to_parse=file_test)
    volatility_parser.run()


if __name__ == '__main__':
    main()
