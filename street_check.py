import pandas
from difflib import SequenceMatcher as Sm
from fuzzywuzzy import fuzz


class StreetCheck:
    def __init__(self):
        self.df = pandas.read_csv(
            'https://data.gov.sk/datastore/dump/a6539561-4664-4980-ae6c-4f3b0c329085?all=true')  # dataframe ulic
        self.street_list = [entry for entry in self.df['streetName']]  # zoznam ulic

    def main(self, test):  # urci ci je vstup jeden alebo viac a vrati vysledky
        final = {}
        if ',' in test:
            test_strings = test.split(',')
            for current_street in test_strings:
                s_current_street = current_street.strip()
                final[s_current_street] = (self.single_street_check(s_current_street))
        else:
            final[test] = (self.single_street_check(test))
        return final

    def single_street_check(self, tst):  # overenie jedneho zaznamu
        street_to_check = tst.strip()
        result_dict = {}
        result_dict_ = {}
        ratio_dict = {}
        for street in self.street_list:
            ratio = fuzz.token_sort_ratio(street_to_check, street)
            ratio_dict[ratio] = (street, street_to_check)
        max_ratio = max(ratio_dict)
        result_dict_[max_ratio] = ratio_dict.get(max_ratio)

        # ratio_fl = Sm(None, street, street_to_check).ratio()
        # ratio_dict[ratio_fl] = [street, street_to_check]
        # max_ratio = max(ratio_dict)
        # result_dict_[max_ratio] = ratio_dict.get(max_ratio)
        for k, v in result_dict_.items():
            original_street = v[1]
            new_key = v[0]
            if k >= 50:
                new_value = str(k) + ' %'
            else:
                new_key = original_street
                new_value = 'nie je názvom ulice.'
            result_dict[new_key] = new_value
        return result_dict
