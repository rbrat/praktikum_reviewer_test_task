import datetime as dt


class Record:
    def __init__(self, amount, comment, date=''):
        self.amount = amount
        # В if проверяется наличие значения, в else значение по умолчанию
        self.date = (dt.datetime.strptime(date, '%d.%m.%Y').date()
                     if date
                     else dt.datetime.now().date()
                     )
        self.comment = comment


class Calculator:
    def __init__(self, limit):
        self.limit = limit
        self.records = []

    def add_record(self, record):
        self.records.append(record)

    def get_today_stats(self):
        today_stats = 0
        # Дублирование, dt.datetime.now().date() достаточно вызвать 1 раз
        today = dt.datetime.now().date()
        # Перекрывает имя класса Record.
        # Для переменных используется snake_case, CamelCase для классов
        for record in self.records:
            if record.date == today:
                # Дублирование, можно использовать +=
                today_stats += record.amount
        return today_stats

    def get_week_stats(self):
        week_stats = 0
        today = dt.datetime.now().date()
        for record in self.records:
            # 2 раза за итерацию вычисляется (today - record.date).days
            days_diff = (today - record.date).days
            # Условие можно упростить
            if (0 <= days_diff < 7):
                week_stats += record.amount
        return week_stats


class CaloriesCalculator(Calculator):
    # Комментарий к функции оформляется как docstring
    # Некорректное описание функции
    def get_calories_remained(self):
        """
        Получает остаток калорий на сегодня.
        Возвращает сообщение с остатком калорий, если лимит не достигнут
        В ином случае, возвращает сообщение о превышении лимита
        """
        x = self.limit - self.get_today_stats()
        if x > 0:
            # Бэкслеши для переносов не применяются
            # Лишний f-string
            return ('Сегодня можно съесть что-нибудь'
                    f' ещё, но с общей калорийностью не более {x} кКал')
        else:
            return 'Хватит есть!'  # Лшиние скобки


class CashCalculator(Calculator):
    USD_RATE = float(60)
    EUR_RATE = float(70)
    CURRENCIES_DICT = {
        'usd': (USD_RATE, 'USD'),
        'eur': (EUR_RATE, 'Euro'),
        'rub': (1, 'руб')
    }

    # Не соответствует сигнатуре get_today_cash_remained(currency) из задания
    # Отсутствует docstring
    # Нет проверки, если в currency передано невалидное значение
    # (не 'usd', 'eur' или 'rub')
    def get_today_cash_remained(self, currency: str):
        """
        Состояние дневного баланса в переданной валюте
        Параметры:
            currency (str): код валюты, поддерживаются 'usd', 'eur', 'rub'.
                При неизвестном коде рейзит Exception('Неизвестная валюта')
        Возвращает:
            Сообщение с остатком, округленным до 2 знаков после запятой
        """
        currency_rate, currency_type = self.CURRENCIES_DICT.get(
            currency, (None, None))
        # Если в currency передано невалидное значение, зарейзим исключение
        if not all((currency_rate, currency_type)):
            raise Exception('Неизвестная валюта')
        cash_remained = (self.limit - self.get_today_stats()) / currency_rate
        if cash_remained > 0:
            # Арифметика внутри f-string
            return 'На сегодня осталось {0:.2f} {1}'.format(
                cash_remained, currency_type)
        elif cash_remained == 0:
            return 'Денег нет, держись'
        # Лишняя проверка на < 0, выше уже проверили на > 0 и == 0
        else:
            # Бэкслеши для переносов не применяются
            return (
                'Денег нет, держись: твой долг - '
                '{0:.2f} {1}'.format(-cash_remained, currency_type)
            )

    # Лишнее переопределение get_week_stats
