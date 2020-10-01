# !/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: sebanie15
"""


import random

SEX = {'male', 'female'}
ODD_MONTHS = (1, 3, 5, 7, 8, 10, 12, 21, 23, 25, 27, 28, 30, 32)
EVEN_MONTHS = (4, 6, 9, 11, 24, 26, 29, 31)


def luhn_checksum(number):

   LUHN_TABLE = [0, 2, 4, 6, 8, 1, 3, 5, 7, 9]

   digits = [int(digit) for digit in number]
   odd_digits = digits[-1::-2]
   even_digits = digits[-2::-2]
   checksum = 0
   checksum += sum(odd_digits)
   for d in even_digits:
      checksum += LUHN_TABLE[d]
   return checksum % 10


def is_luhn_valid(number):
   return luhn_checksum(number) == 0


def pesel_check_sum(number):
   check_table = [1, 3, 7, 9, 1, 3, 7, 9, 1, 3]
   digits = [int(digit) for digit in number]
   suma = 0
   for idx, digit in enumerate(digits[:-1]):
     suma += (digit * check_table[idx]) % 10

   check_sum = 10 - (suma % 10)
   return check_sum

def pesel_gen_check_sum(number):
   check_table = [1, 3, 7, 9, 1, 3, 7, 9, 1, 3]
   digits = [int(digit) for digit in number]
   suma = 0
   for idx, digit in enumerate(digits):
     suma += (digit * check_table[idx]) % 10

   check_sum = 10 - (suma % 10)
   return check_sum


def pesel_is_valid(number):

   if pesel_check_sum(number) == int(number) % 10:
      return True
   else:
      return False


def code_sex(s):
   """
   g, h, i, j – oznaczenie płci (jeśli cała ta 4-cyfrowa liczba, a w praktyce ostatnia z nich, czyli j, jest parzysta
               - jest to PESEL kobiety, jeśli jest nieparzysta - jest to PESEL mężczyzny)
   (0, 2, 4, 6, 8 – oznaczają płeć żeńską,
   1, 3, 5, 7, 9 – płeć męską)
   """
   if s == 'm':
      start = 0
      stop = 9
   else:
      start = 1
      stop = 10

   g = random.randint(0, 10)
   h = random.randint(0, 10)
   i = random.randint(0, 10)
   j = random.randrange(start, stop, 2)

   code = str(g) + str(h) + str(i) + str(j)
   return code


def decode_sex(pesel):

   if int(pesel[-2]) % 2 == 0:
      return 'Kobieta'
   else:
      return 'Męszczyzna'


def gen_pesel(y, m, d, s):

   month_err = False
   month = 0

   if m in range(1, 13):
      month = m
   else:
      month_err = True

   day = d

   # sprawdzenie roku
   if y >= 1900 and y <= 1999:
      month = month
   elif y >= 2000 and y < 2100:
      month += 20 # to distinguish between centuries
   elif y >= 2100 and y < 2200:
      month += 40
   elif y >= 2200 and y < 2300:
      month += 60


   if month in ODD_MONTHS:
      if day <= 31:
         day = day
      else:
         day_err = True

   elif month in EVEN_MONTHS:
      if day <= 30:
         day = day
      else:
         print(f'nieprawidłowa wartość dnia dla miesiąca {month}, Poddaj jeszcze raz dane1')
         day_err = True
   # dla lutego
   else:
      if year % 4 == 0 and year != 1900:
         if day <= 29:
            day = day
         else:
            day_err = True

      else:
         if day <= 28:
            day = day
         else:
            day_err = True

   # clinic rozpisany po kolei

   a = '0' if (y % 100) < 10 else str(y % 100)[0]
   a = int(a)
   b = str(y % 100)[1] if (y % 100) >= 10 else str(y % 100)[0]
   b = int(b)
   c = '0' if month < 10 else str(month)[0]
   c = int(c)
   d = str(month)[1] if month >= 10 else str(month)[0]
   d = int(d)
   e = '0' if day < 10 else str(day)[0]
   e = int(e)
   f = str(day)[1] if day >= 10 else str(day)[0]
   f = int(f)
   g = int(code_sex(s)[0])
   h = int(code_sex(s)[1])
   i = int(code_sex(s)[2])
   j = int(code_sex(s)[3])

   pesel_first = str(a) + str(b) + str(c) + str(d) + str(e) + str(f) + code_sex(s)

   if month_err:
      return 'Błędne dane wejściowe'
   else:
      return pesel_first + str(pesel_gen_check_sum(pesel_first))

   year = 0
   month = 0
   day = 0
   sex = 'm'


if __name__ == '__main__':
   while True:
      polecenie = input('Co chcesz zrobić: \n'
               '- generuj PESEL -> p \n'
               '- sprawdź clinic -> c \n'
               '- wyjdź z programu - e \n'
               '- sprawdź płeć - s \n'
               ' Twoje polecenie: ')

      if polecenie == 'e':
         print('Wyszedłeś z programu!')
         break
      elif polecenie == 'p':
         print('Wybrałeś opcji generowania numeru PESEL')
         try:
            year = int(input('Podaj rok urodzenia: '))
            month = int(input('Podaj mięsiąc urodzenia: '))
            day = int(input('Podaj dzień urodzenia: '))
            sex = input('Podaj płeć: '
                  ' m - męszczyzna'
                  ' k - kobieta')

            print(gen_pesel(year, month, day, sex), '\n')
         except:
            print('nieprawidłowe dane wejściowe')


      elif polecenie == 'c':
         print('Wybrałeś opcję sprawdzenia numeru PESEL. Podaj numer PESEL: ')
         pesel = input('Podaj numer PESEL: ')
         print(pesel_check_sum(pesel))
         print(pesel_is_valid(pesel))
      elif polecenie == 's':
         n = input('Podaj numer PESEL: ')
         print(f'Płeć wg numeru PESEL {n} to {decode_sex(n)}')

      else:
            print('nie obsługiwany błąd')
