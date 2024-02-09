# Функция для чтения последних 10 записей из файла логов
def read_last_logs(filename, num_lines=100):
    with open(filename, 'r') as file:
        lines = file.readlines()
        last_lines = lines[-num_lines:]
        return ''.join(last_lines)
