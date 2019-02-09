from datetime import datetime
import csv
import pycountry
from itertools import groupby


class DataModel:
    """
        DataModel class provides analyzed and grouped data from ad_models

        Attributes:
            ad_models (list): List of ad models
            groups (itertools): grouper object which contains ads sorted by date
            data (list): all list of ads parsed and sorted by date
    """

    def __init__(self, ad_models):
        self.ad_models = ad_models
        self.groups = self.group_by_date(self.ad_models)
        self.data = self.parse_groups()

    def parse_groups(self):
        """
            Add parsed and grouped by date ad_models to data list

        :return: list of ad_models grouped by date
        """

        data = []
        ads_by_data = []
        for date_time, group in self.groups:
            for ad in group:
                ads_by_data.append({"ad": ad})
            date_key = self.date_to_string(date_time)
            data.append({date_key: ads_by_data})
            ads_by_data = []

        return data

    def merge_data(self):
        """
            Merge ad_models from data by code and date
            when ad_model has the same date and code, we merge them

        :return merged_data: data which contains merge and unique ad_models
        """

        merged_data = []
        for data in self.data:
            values_test = [self.get_ad_from_dict(ad) for ad in self.get_values_from_dict(data)]
            merged_ads_tmp = []
            for code, ads in self.group_by_code(values_test):
                for ad in ads:
                    merged_ads_tmp.append(ad)

                if len(merged_ads_tmp) > 1:
                    merged_ads = AdModel.merge_ads(self.get_first_key_from_dict(data),
                                                   code, merged_ads_tmp)
                else:
                    merged_ads = merged_ads_tmp
                merged_ads_tmp = []
                merged_data.append({self.get_first_key_from_dict(data): merged_ads})

        return merged_data

    @staticmethod
    def group_by_code(values):
        """
            Group ad_models from values by country_code

        :param values: list of ad_models
        :return code, ads: generator which contains code and group of ads connected to this code
        """

        values.sort(key=lambda x: x.country_code)
        for code, ads in groupby(values, lambda x: x.country_code):
            yield code, ads

    @staticmethod
    def date_to_string(date) -> str:
        """
            Convert date object to string

        :param date:
        :return: Date parsed to string
        """

        return date.strftime('%m/%d/%Y')

    @staticmethod
    def get_ad_from_dict(ad_dict):
        """
            Get adModel from dict

        :param ad_dict: dictionary contains value as adModel and key as 'ad'
        :return: adModel or None if exception raise
        """

        try:
            ad = ad_dict['ad']

            return ad
        except KeyError as exc:
            print("Cannot find ad attribute "+str(exc))
            return None

    @staticmethod
    def group_by_date(ad_models):
        """
            Function which group ad_models by date

        :param ad_models: list of ad_models
        :return: generator which contains date and group of ads
        """

        ad_models.sort(key=lambda x: x.date)
        for date_time, group in groupby(ad_models, lambda x: x.date):
            yield date_time, group

    @staticmethod
    def get_values_from_dict(ad_dict):
        """
            Get values from dictionary example:
            {key: [elem_1, elem_2, elem_3]}

        :param ad_dict: dictionary contains key as date and values which are list of ads
        :return: list of ads or None if exception raise
        """

        try:
            ads = list(ad_dict.values())[0]
            return ads
        except IndexError as exc:
            print("Cannot find value " + str(exc))
            return None

    @staticmethod
    def get_first_value_from_dict(ad_dict):
        """
            Get value from dictionary example dict:
            {key: elem}

        :param ad_dict: dictionary
        :return: value from dictionary
        """

        try:
            value = list(ad_dict.values())[0]
            if type(value) is list:
                value = value[0]

            return value
        except IndexError as exc:
            print("Cannot find value " + str(exc))
            return None

    @staticmethod
    def get_first_key_from_dict(ad_dict):
        """
            Get key from dict

        :param ad_dict: dictionary
        :return: key or None if exception raise
        """

        try:
            key = list(ad_dict.keys())[0]

            return key
        except IndexError as exc:
            print("Cannot find key " + str(exc))
            return None

    @staticmethod
    def ad_validation(ad_1, ad_2) -> bool:
        """
            Compare two adModels by country_code and location

        :param ad_1: adModel
        :param ad_2: adModel
        :return: boolean value of comparison two adModels
        """

        return ad_1.country_code == ad_2.country_code and ad_1.location != ad_2.location


class AdModel:
    """
        Admodel class which store information about ad

        Attributes:
            :date - datetime object
            :location - string value
            :impression - number of impression, int
            :CTR -  float number
    """

    def __init__(self, date, location, impression, CTR):
        self.date = self.parse_date(date)
        self.location = location
        self.impression = int(impression)
        self.ctr = self.parse_ctr(CTR)
        self.clicks = int(round(self.impression * self.ctr / 100))
        self.country_code = self.get_country_code()

    def get_country_code(self):
        """
            Searching correct country_code from subdivisions and country, pyCountry module provides it.

        :return: country_code or XXX if we don't find anything
        """

        try:
            sub_div = next(sub_div for sub_div in pycountry.subdivisions if sub_div.name == self.location)
            country = next(country for country in pycountry.countries if country.alpha_2 == sub_div.country_code)
            return country.alpha_3
        except StopIteration as exc:
            print("Cannot find subdivision in" + str(exc))
            return 'XXX'

    @staticmethod
    def merge_ads(date, code, ads) -> list:
        """
            Function which allows to merge list of ads to one object


        :param date: date which should be the same withing list of ads
        :param code: country_code which should be the same
        :param ads: list of adModels
        :return: merged adModel object
        """

        merged_ad = AdModel(date, None, sum(ad.impression for ad in ads), None)
        merged_ad.clicks = sum(ad.clicks for ad in ads)
        merged_ad.country_code = code
        return merged_ad

    @staticmethod
    def parse_ctr(ctr) -> float:
        """
            Parse ctr string value to float example ctr:
             :ctr 0.38%

        :param ctr: string value contains percent and float value
        :return: float number
        """

        if ctr is None:
            return 0.0
        try:
            ctr = float(ctr[:len(ctr) - 1])
            return ctr
        except IndexError as exc:
            print("CTR parsing failed" + str(exc))
            return 0.0

    @staticmethod
    def parse_date(date) -> datetime:
        """
            Parse string value to datetime object
                example variable: 12/12/2012

        :param date: string variable
        :return: datetime object
        """

        if type(date) == datetime:
            return date

        date_object = datetime.strptime(date.replace(" ", ""), "%m/%d/%Y")
        return date_object


def create_ads(file_name, data_reader) -> list:
    """
        Method which allows to read the csv file and create adModels from data

    :param file_name: csv file name
    :param data_reader: csv data reader object
    :return: list of ads
    """

    ads = []
    for row in data_reader:
        try:
                ads.append(AdModel(row[0], row[1], row[2], row[3]))
        except IndexError:
            print("Invalid row in file: " + file_name + "invalid row: ", row)

    return ads


def write_output_file(ad_models):
    """
        Write to the file adModels object

    :param ad_models: list of adModel
    :return: csv file
    """

    with open('output-data-utf8.csv', 'w', newline='', encoding='UTF-8') as output_file:
        csv_writer = csv.writer(output_file, delimiter=',')
        for ad in ad_models:
            csv_writer.writerow((ad.date.strftime('%m/%d/%Y'), ad.country_code, ad.impression, ad.clicks))


def create_ad_model_view(file_name, encoding="UTF-8"):
    """
        Main function
            Reading the file with given encoding, creating DataModel which allows to read analyzed ads data

    :param file_name: file name which contains data of advertisements
    :param encoding: base encoding is UTF-8 but UTF-16 will work too
    :return: file output-data-utf8 which contains analyzed and parsed ads
    """

    ads = []
    try:
        with open(file_name, newline='', encoding=encoding) as data_file:
            data_reader = csv.reader(data_file, delimiter=',')
            ads = create_ads(file_name, data_reader)
    except (UnicodeDecodeError, FileNotFoundError, UnicodeError) as exc:
        print("Cannot read file: " + str(exc))

    data_model = DataModel(ads)

    ad_models = []
    for ad in data_model.merge_data():
        ad_parsed = data_model.get_first_value_from_dict(ad)
        ad_models.append(ad_parsed)

    sorted(ad_models, key=lambda x: (x.date, x.country_code))
    write_output_file(ad_models)


""" EXECUTION
"""
create_ad_model_view("data-utf16.csv", 'UTF-16')
