"""Main module."""
from typing import List
from collections import deque
from datetime import datetime


class Diseases:
    """
    klasa choroby
    """
    def __init__(self, name):
        self.name = name


class Patient:
    """
    klasa Patient
    """
    def __init__(self, name, age, illness: List[Diseases]):
        self.name = name
        self.age = age
        self.diseases = deque([disease for disease in illness])

    def add_disease(self, disease: Diseases):
        """
        dodanie choroby pacjentowi
        :param disease:
        :return:
        """
        if disease not in self.diseases:
            self.diseases.append(disease)

    def cure_disease(self, disease: Diseases = None):
        """
        wyleczenie choroby i usuniecie jej z listy chorób
        :param disease:
        :return:
        """
        if disease in self.diseases:
            del(self.diseases[self.diseases.index(disease)])


class Examination:
    """
    klasa badania lekarskiego
    """
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
        """
        if examination:
            self.exams.append(examination)

    @property
    def patient_to_examination(self) -> Patient:
        """
        pobranie danych pacjenta do badania, usunięcie badania z kalendarza
        :return:
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
    def __init__(self, name, calendar: Calendar):
        self.name = name
        self.patients = deque([])
        self.calendar = calendar

    def register_to_doctor(self, patient: Patient, date_of_examination: datetime):
        """
        rejestracja pacjenta do doctora w okreslonym terminie
        :param patient:
        :param date_of_examination:
        :return:
        """
        if patient not in self.patients:
            self.patients.append(patient)
        self.calendar.add_examination(Examination(date_of_examination, patient))

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


if __name__ == '__main__':
    illness1 = Diseases('przeziebienie')
    illness2 = Diseases('gorączka')
    illness3 = Diseases('Coronavirus')

    patient1 = Patient('Romek Rybak', 55, [illness1, illness2])
    patient2 = Patient('Adam Malysz', 55, [illness1, illness2])
    patient3 = Patient('Zbigniew Ziobro', 55, [illness1, illness2, illness3])
    patient4 = Patient('Lukasz Szumowski', 55, [illness3])
    patient5 = Patient('Kot Jarka', 55, [illness3])

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

