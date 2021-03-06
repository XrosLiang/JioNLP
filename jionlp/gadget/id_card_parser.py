# -*- coding=utf-8 -*-

import os
import re
import pdb

from jionlp.dictionary.dictionary_loader import china_location_loader
from jionlp.rule.rule_pattern import ID_CARD_CHECK_PATTERN


class IDCardParser(object):
    ''' 身份证号码解析器 '''
    def __init__(self):
        self.china_locations = None
        self.id_card_check_pattern = re.compile(ID_CARD_CHECK_PATTERN)
        
    def _prepare(self):
        china_loc = china_location_loader()
        china_locations = dict()
        for prov in china_loc:
            if not prov.startswith('_'):
                china_locations.update(
                    {china_loc[prov]['_admin_code']: 
                     [prov, None, None]})
                for city in china_loc[prov]:
                    if not city.startswith('_'):
                        china_locations.update(
                            {china_loc[prov][city]['_admin_code']: 
                             [prov, city, None]})
                        for county in china_loc[prov][city]:
                            if not county.startswith('_'):
                                china_locations.update(
                                    {china_loc[prov][city][county]['_admin_code']: 
                                     [prov, city, county]})
        self.china_locations = china_locations
        
    def __call__(self, id_card):
        if self.china_locations is None:
            self._prepare()
            
        # 检查是否是身份证号
        match_flag = self.id_card_check_pattern.match(id_card)
        #print(match_flag)
        #pdb.set_trace()
        if match_flag is None:
            return None

        if id_card[:6] in self.china_locations.keys():
            prov, city, county = self.china_locations[id_card[:6]]
        elif id_card[:4] + '0' * 2 in self.china_locations.keys():
            prov, city, county = self.china_locations[id_card[:4] + '0' * 2]
        elif id_card[:2] + '0' * 4 in self.china_locations.keys():
            prov, city, county = self.china_locations[id_card[:2] + '0' * 4]
        else:
            # 前六位行政区划全错
            return None
        gender = '男' if int(id_card[-2]) % 2 else '女'
        check_code = id_card[-1]
        if check_code == 'X':
            check_code = 'x'
        
        return {'province': prov, 'city': city, 
                'county': county, 
                'birth_year': id_card[6:10],
                'birth_month': id_card[10:12],
                'birth_day': id_card[12:14],
                'gender': gender,
                'check_code': check_code}





