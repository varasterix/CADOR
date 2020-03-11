import csv


def read_needs_from_csv(file_path, row_index=0, column_index=0):
    """
    :param file_path: path of the csv file in which there is the table of the needs by shifts, by days of the week
    :param row_index: index of the row in the csv file of the case containing the first shift label
    :param column_index: index of the column in the csv file of the case containing the first shift label
    :return: tuple (table of the needs by shifts by days of the week, the list of the shifts)
    """
    weeks = ['L', 'Ma', 'Me', 'J', 'V', 'S', 'D']
    shifts = {}
    shift_index = 0
    needs_by_shifts = {}
    needs_by_days = []
    with open(file_path, 'r') as csv_file:
        reader = csv.reader(csv_file, delimiter=';')
        for index, row in enumerate(reader):
            if index >= row_index:
                end_reading = (row[column_index] == '')
                if not end_reading:
                    shift_id = row[column_index]
                    needs_by_shift = {}
                    for j, day in enumerate(weeks):
                        needs_by_shift[day] = int(row[column_index + j + 1])
                    shifts[shift_id] = shift_index
                    needs_by_shifts[shift_id] = needs_by_shift
                    shift_index += 1
                else:
                    break
        for day in weeks:
            needs_by_day = {}
            for s in shifts:
                needs_by_day[s] = needs_by_shifts[s][day]
            needs_by_days.append(needs_by_day)
        csv_file.close()
    return needs_by_days, shifts
