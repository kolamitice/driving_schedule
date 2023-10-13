from datetime import datetime

class Employee:
    def __init__(self, employee_name, work_hours, vacation_dates, start_date):
        self.employee_name = employee_name
        self.work_hours = work_hours
        self.vacation_dates = vacation_dates
        self.vacations = self.convert_vacation_dates(vacation_dates, start_date)

    def is_on_vacation(self, day):
        return day in self.vacations

    def convert_vacation_dates(self, vacation_dates, start_date):
            year, month = map(int, start_date.split('-')[:2])
            return [datetime.strptime(date_str + f"-{year}", "%d-%m-%Y").day for date_str in vacation_dates if datetime.strptime(date_str + f"-{year}", "%d-%m-%Y").month == month]
