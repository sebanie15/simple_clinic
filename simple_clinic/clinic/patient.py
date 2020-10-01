# !/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: sebanie15
"""
from .disease import  Diseases


class Patient:
    """
    klasa Patient
    """

    def __init__(self, pesel, first_name, last_name, age, born, sex):
        self.pesel = pesel
        self.first_name = first_name
        self.last_name = last_name
        self.age = age
        self.born = born
        self.sex = sex
        self.__diseases = []

    """
    def __init__(self, clinic, name, age, illness: List[Diseases]):
        self.clinic = clinic
        self.name = name
        self.age = age
        self.diseases = deque([disease for disease in illness])
    """

    @property
    def name(self):
        return f'{self.first_name} {self.last_name}'

    @property
    def diseases(self):
        return self.__diseases

    def add_disease(self, disease: Diseases):
        """
        dodanie choroby pacjentowi
        :param disease:
        :return:
        """
        if disease not in self.__diseases:
            self.__diseases.append(disease)

    def cure_disease(self, disease: Diseases = None):
        """
        wyleczenie choroby i usuniecie jej z listy chorób
        :param disease:
        :return:
        """
        if disease in self.__diseases:
            del (self.__diseases[self.__diseases.index(disease)])

