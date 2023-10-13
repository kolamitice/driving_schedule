import calendar
from datetime import datetime
import pulp

def optimization(employees, start_date):
    #determine workdays in regarding to month to calculate
    year, month = map(int, start_date.split('-')[:2])
    num_days = calendar.monthrange(year, month)[1]
    valid_days = [day for day in range(1, num_days + 1) if datetime(year, month, day).weekday() < 5]
    slots = ["T1", "T2", "T3"]

    #create linear minimization problem
    prob = pulp.LpProblem("DrivingScheduleOptimized", pulp.LpMinimize)

    #define variable
    x = pulp.LpVariable.dicts("schedule",((employee.employee_name, day, t_slot) for employee in employees for day in valid_days for t_slot in slots), cat='Binary')
    absolute_deviation = pulp.LpVariable.dicts("abs_deviation", [employee.employee_name for employee in employees], lowBound=0)

    #minimize devaition from expected sessions
    total_sessions = [pulp.lpSum([x[(employee.employee_name, j, t)] for j in valid_days for t in slots]) for employee in employees]
    expected_sessions = [(employee.work_hours / sum([emp.work_hours for emp in employees])) * len(valid_days) * len(slots) for employee in employees]
    prob += pulp.lpSum([absolute_deviation[i] for i in [employee.employee_name for employee in employees]])

    for i, employee in enumerate(employees):
        prob += total_sessions[i] - expected_sessions[i] <= absolute_deviation[employee.employee_name]
        prob += expected_sessions[i] - total_sessions[i] <= absolute_deviation[employee.employee_name]

    
    
    # Constraints
    for employee in employees:
        for j in valid_days:
            prob += pulp.lpSum([x[(employee.employee_name, j, t)] for t in slots]) <= 1
            
            if employee.is_on_vacation(j):
                for t in slots:
                    prob += x[(employee.employee_name, j, t)] == 0

    for j in valid_days:
        for t in slots:
            prob += pulp.lpSum([x[(employee.employee_name, j, t)] for employee in employees]) == 1


    prob.solve()

    schedule = {day: {t_slot: None for t_slot in slots} for day in valid_days}
    for j in valid_days:
        for t in slots:
            for employee in employees:
                if x[(employee.employee_name, j, t)].varValue == 1:
                    schedule[j][t] = employee.employee_name
                    break

    return schedule