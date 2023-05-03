import json
from datetime import datetime

def get_data():
    ''' Получение данных из файла...'''
    with open('operations.json', 'r', encoding='utf-8') as file:
        data = json.load(file)
    return data

def filter_data(data):
    '''Фильтрация транзакций'''
    data = [x for x in data if 'state' in x and x['state'] == 'EXECUTED']
    return data

def sorted_key(x):
    return x['date']

def sort_data(data):
    '''Сортировка транзакций'''
    data = sorted(data, key=sorted_key, reverse=True)
    return data[:5]


def format_date(data):
    '''Форматирование даты'''
    formatted_data = []
    for row in data:
        date = datetime.strptime(row['date'], '%Y-%m-%dT%H:%M:%S.%f').strftime("%d.%m.%Y")
        description = row['description']
        sum_list = row['operationAmount']
        sum_ = sum_list['amount']
        valut_list = sum_list['currency']
        valut = valut_list['name']
        if 'from' in row:
            from_arrow = '->'
            sender = row['from'].split()
            sender_bill = sender.pop(-1)
            sender_info = " ".join(sender)
            sender_bill = f'{sender_bill[:4]} {sender_bill[4:6]}** **** {sender_bill[-4:]}'
        else:
            sender_info = 'Новый счет'
            sender_bill = ''
            from_arrow = ''

        if 'to' in row:
            recipient = row['to'].split()
            recipient_bill = recipient.pop(-1)
            recipient_info = " ".join(recipient)
            recipient_bill = f"**{recipient_bill[-4:]}"
        else:
            recipient_info = ""
            recipient_bill = ""


        formatted_data.append(f'''
{date} {description}
{sender_info} {sender_bill} {from_arrow} {recipient_info} {recipient_bill}
{sum_} {valut}
        ''')
    return formatted_data

#добавить если не карта а счет кодировку на **7878
#И вывод суммы транзакции