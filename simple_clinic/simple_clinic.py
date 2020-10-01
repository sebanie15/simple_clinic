"""Main module."""
from typing import List
from collections import deque
from datetime import datetime, date
from dataclasses import dataclass
from random import randint, randrange


class Pesel:
    SEX = {'male', 'female'}
    ODD_MONTHS = (1, 3, 5, 7, 8, 10, 12, 21, 23, 25, 27, 28, 30, 32)
    EVEN_MONTHS = (4, 6, 9, 11, 24, 26, 29, 31)

    """
    pesel[0:5] -> data
    pesel[6:9] -> płeć
    pesel[10]  -> suma kontrolna
    """

    def code_sex(self, sex):
        """
           g, h, i, j – oznaczenie płci (jeśli cała ta 4-cyfrowa liczba, a w praktyce ostatnia z nich, czyli j, jest parzysta
                       - jest to PESEL kobiety, jeśli jest nieparzysta - jest to PESEL mężczyzny)
           (0, 2, 4, 6, 8 – oznaczają płeć żeńską,
           1, 3, 5, 7, 9 – płeć męską)
           """
        start = stop = 0

        if sex == 'male':
            start = 0
            stop = 9
        elif sex == 'female':
            start = 1
            stop = 10
        else:
            pass
        # TODO: co jeśli jest podana inna płeć

        return f'{randint(0, 10)}{randint(0, 10)}{randint(0, 10)}{randrange(start, stop, 2)}'

    def decode_sex(self, pesel: str) -> SEX:
        if int(pesel[-2]) % 2 == 0:
            return 'female'
        return 'male'

    def decode_date(self, pesel: str) -> date:
        if len(pesel) == 10:
            date_pesel = pesel[0:6]
        elif len(pesel) == 12:
            date_pesel = pesel[2:8]
        else:
            print('Nieprawidłowy numer pesel')
            return date(1900, 1, 1)


@dataclass
class Diseases:
    """
    klasa choroby
    """
    name: str
    description: str = ''


class Specialization:
    count = 0

    def __init__(self, name, description: str = ''):
        self.count += 1
        self.id = self.count
        self.name = name
        self.description = description
        self.diseases = []


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


class Examination:
    """
    klasa badania lekarskiego
    """
    exam_time = 30  # długość wizyty -> 30 min

    def __init__(self, date: datetime, patient: Patient):
        self.date = date
        self.patient = patient


class Calendar:
    """
    klasa kalendarza badań lekarskich
    """

    def __init__(self):
        self.__exams = []

    @property
    def exams(self):
        return deque(self.__exams)

    def add_examination(self, examination: Examination):
        """
        dodawanie badanie lekarskiego
        :param examination:
        :return:
        >>> 1 # dodanie wizyty do kalendarza

        >>> 0  # wizyta nie zostałą dodana
        """
        for exam in self.__exams:
            if examination.date == exam.date:
                break
        else:
            self.__exams.append(examination)
            return 1
        return 0

    @property
    def patient_to_examination(self) -> Patient:
        """
        pobranie danych pacjenta do badania, usunięcie badania z kalendarza
        :return:
        >>> Patient()
        """
        if self.exams:
            return self.exams.popleft().patient

    def save(self, path):
        with open(path, 'w') as file:
            file.writelines([
                f'{exam.date}, '
                f'{exam.patient.name}, '
                f'{[disease.name for disease in exam.patient.diseases]}\n'
                for exam in self.exams]
            )


class Doctor:
    """
    klasa Doctor
    """

    def __init__(self, first_name, last_name, calendar: Calendar, specialization: Specialization = None):
        """
        Inicjalizacja danych dla lekarza
        :param first_name: imię
        :param last_name: nazwisko
        :param specialization: specjalizacja
        :param calendar:
        """
        self.first_name = first_name
        self.last_name = last_name
        self.specialization = specialization
        self.patients = deque([])
        self.calendar = calendar

    @property
    def name(self) -> str:
        """
        funkcja zwraca imię i nazwisko lekarza
        :return:
        """
        return f'{self.first_name} {self.last_name}'

    def add_patient(self, patient: Patient) -> int:
        """
        dodanie pacjenta do listy pacjentów jeśli go nie ma na liście
        :param patient:
        :return:
        >>> 1 # dodanie nowego pacjenta

        >>> 0 # pacjent jest już na liście
        """
        if patient not in self.patients:
            self.patients.append(patient)
            return 1
        return 0

    def register_to_doctor(self, patient: Patient, date_of_examination: datetime) -> int:
        """
        rejestracja pacjenta do doctora w okreslonym terminie
        :param patient:
        :param date_of_examination:
        :return:
        >>> 1 # dodanie wizyty powiodło się

        >>> 0 # wizyta nie została dodana
        """
        if self.add_patient(patient):
            print('Pacjent został dodany do bazy')
        if self.calendar.add_examination(Examination(date_of_examination, patient)):
            print('Dodanie wizyty przebiegło pomyślnie')
            return 1
        else:
            print('Wizyta nie została dodana do kalendarza, termin jest już zajęty')
            return 0

    def examination_of_patient(self):
        """
        badanie pacjenta, jesli pacjent jest wyleczony ze wszystkich chorób usunięcie pacjenta
        z listy pacjentów
        :return:
        """
        patient = self.calendar.patient_to_examination
        illness = patient.diseases.popleft()
        if not patient.diseases:
            del (self.patients[self.patients.index(patient)])

        return patient, illness

    def print_calendar(self):
        """
        drukowanie kalendarza badań
        :return:
        """
        print(f'Kalendarz doktora: {self.name}')
        print('-' * 50)
        for entry in self.calendar.exams:
            print(f'Data: {entry.date}, pacjent {entry.patient.name}')

    def save(self, path):
        with open(path, 'w') as file:
            file.writelines([exam for exam in self.calendar.exams])


class SimpleCLinic:

    def __init__(self, name):
        self.name = name
        self.doctors = List[Doctor]
        self.patients = List[Patient]

    def load(self):
        pass

    def save(self):
        pass

    def use_doctor(self):
        pass

    def add_patient(self):
        pass

    def add_doctor(self):
        self.doctors.append(Doctor('Doktor', 'Nibyjaki', Calendar()))


if __name__ == '__main__':
    illness1 = Diseases('przeziebienie')
    illness2 = Diseases('gorączka')
    illness3 = Diseases('Coronavirus')

    patient1 = Patient(pesel='80042313865',
                       first_name='Romek',
                       last_name='Rybak',
                       age=55,
                       born=date(1980, 4, 23),
                       sex='male'
                       )
    patient2 = Patient(pesel='75062434234',
                       first_name='Adam',
                       last_name='Malysz',
                       age=55,
                       born=date(1975, 6, 24),
                       sex='male')
    patient3 = Patient(pesel='75062434234',
                       first_name='Zbigniew',
                       last_name='Ziobro',
                       age=55,
                       born=date(1975, 6, 24),
                       sex='female')

    patient1.add_disease(illness2)
    # print(patient1.diseases)
    # patient1.cure_disease(illness1)
    print(patient1.diseases)

    # illness3 = Diseases('groźna choroba')
    patient1.add_disease(illness3)
    print(patient1.diseases)

    doctor1 = Doctor('doktor', 'nibyjaki', Calendar())
    doctor1.register_to_doctor(patient1, datetime(2020, 11, 23, 7, 43, 00, 00))
    doctor1.register_to_doctor(patient2, datetime(2020, 11, 24, 7, 43, 00, 00))
    doctor1.register_to_doctor(patient3, datetime(2020, 11, 25, 7, 43, 00, 00))

    # doctor1.examination_of_patient()
    print(patient1.diseases)
    doctor1.print_calendar()
    doctor1.calendar.save('doctor1-cal.txt')
