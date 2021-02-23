# -*- coding: utf-8 -*-
import os


class VolatilityParser:

    def __init__(self, file_to_parse):
        self.file_to_parse = os.path.normpath(file_to_parse)
        self.secid_volatility = {}

    def run(self):
        try:
            for dirpath, dirnames, filenames in os.walk(self.file_to_parse):
                for file in filenames:
                    self.secid = None
                    self.trade_time = None
                    self.price = None
                    self.quantity = None
                    self.half_sum = 0
                    self.volatility = 0
                    self.price_max = 0
                    self.price_min = None
                    full_file_path = os.path.join(dirpath, file)
                    self._ticker_analyze(file=full_file_path)
                    self.volatility_calculation()
        except IsADirectoryError as err:
            print(f'{err}, no such file or directory')
        self.report()

    def _ticker_analyze(self, file):
        try:
            with open(file, 'r', encoding='UTF8') as ticker_doc:
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
        except FileNotFoundError as err:
            print(f'{err}, file not found')

    def volatility_calculation(self):
        self.half_sum = (self.price_max + self.price_min) / 2
        self.volatility = ((self.price_max - self.price_min) / self.half_sum) * 100
        self.volatility = round(self.volatility, 2)
        self.secid_volatility[self.secid] = self.volatility

    def report(self):
        values_list = list(self.secid_volatility.items())
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
    vol_calc = VolatilityParser(file_to_parse='trades')
    vol_calc.run()


if __name__ == '__main__':
    main()
