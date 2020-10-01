"""Main module."""
from typing import List
from collections import deque
from datetime import datetime
from dataclasses import dataclass


class Diseases:
    """
    klasa choroby
    """
    def __init__(self, name):
        self.name = name


@dataclass
class Patient:
    """
    klasa Patient
    """
    pesel: str
    first_name: str
    last_name: str
    age: int
    __diseases: List[Diseases]
    """
    def __init__(self, pesel, name, age, illness: List[Diseases]):
        self.pesel = pesel
        self.name = name
        self.age = age
        self.diseases = deque([disease for disease in illness])
    """

    @property
    def name(self):
        return f'{self.first_name} {self.last_name}'

    @property
    def diseases(self):
        return deque(self.__diseases)

    def add_disease(self, disease: Diseases):
        """
        dodanie choroby pacjentowi
        :param disease:
        :return:
        """
        if disease not in self.diseases:
            self.__diseases.append(disease)

    def cure_disease(self, disease: Diseases = None):
        """
        wyleczenie choroby i usuniecie jej z listy chorób
        :param disease:
        :return:
        """
        if disease in self.__diseases:
            del(self.__diseases[self.__diseases.index(disease)])


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
        self.exams = deque()

    def add_examination(self, examination: Examination):
        """
        dodawanie badanie lekarskiego
        :param examination:
        :return:
        >>> 1 # dodanie wizyty do kalendarza

        >>> 0  # wizyta nie zostałą dodana
        """
        for exam in self.exams:
            if examination.date == exam.date:
                break
        else:
            self.exams.append(examination)
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


@dataclass
class Specialization:
    id: int
    name: str
    description: str
    diseases: List[Diseases]


class Doctor:
    """
    klasa Doctor
    """
    def __init__(self, first_name, last_name, specialization: Specialization = None, calendar: Calendar = None):
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
        self.doctors.append(Doctor('Doktor Nibyjaki', Calendar()))


if __name__ == '__main__':
    illness1 = Diseases('przeziebienie')
    illness2 = Diseases('gorączka')
    illness3 = Diseases('Coronavirus')

    patient1 = Patient('80042313865', 'Romek', 'Rybak', 55, [illness1, illness2])
    patient2 = Patient('75062434234', 'Adam', 'Malysz', 55, [illness1, illness2])
    patient3 = Patient('75062434234', 'Zbigniew', 'Ziobro', 55, [illness1, illness2, illness3])
    patient4 = Patient('75062434234', 'Lukasz', 'Szumowski', 55, [illness3])
    patient5 = Patient('75062434234', 'Kot', 'Jarka', 55, [illness3])

    print(patient1.diseases)
    patient1.cure_disease(illness1)
    print(patient1.diseases)

    illness3 = Diseases('groźna choroba')
    patient1.add_disease(illness3)
    print(patient1.diseases)

    doctor1 = Doctor('doktor nibyjaki', Calendar())
    doctor1.register_to_doctor(patient1, datetime(2020, 11, 23, 7, 43, 00, 00))
    doctor1.register_to_doctor(patient2, datetime(2020, 11, 24, 7, 43, 00, 00))
    doctor1.register_to_doctor(patient3, datetime(2020, 11, 25, 7, 43, 00, 00))
    doctor1.register_to_doctor(patient4, datetime(2020, 11, 26, 7, 43, 00, 00))
    doctor1.register_to_doctor(patient5, datetime(2020, 11, 27, 7, 43, 00, 00))
    # doctor1.examination_of_patient()
    print(patient1.diseases)
    doctor1.print_calendar()
    doctor1.calendar.save('doctor1-cal.txt')
