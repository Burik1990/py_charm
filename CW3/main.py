from utils import get_data, filter_data, sort_data, format_date
def main():
   #Получение данных из файла...
    data = get_data()

   #Фильтрация транзакций
    data = filter_data(data)

   #Сортировка транзакций
    data = sort_data(data)

    #Форматирование даты
    data = format_date(data)

    for row in data:
        print(row)


if __name__ == "__main__":
    main()