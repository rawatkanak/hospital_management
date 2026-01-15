def sort_appointments_fcfs(appointments):
    """
    appointments: list of tuples returned by database.get_appointments
    Each tuple: (appointment_id, appointment_no, patient_name, age, doctor_name, specialization, start_time, end_time, doctor_id)
    Sorting is already performed  in the DB query, but function provided to re-sort if needed.
    """
    return sorted(appointments, key=lambda x: (x[4], x[1]))  # sort by doctor_name then appointment_no
