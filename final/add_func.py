import re

def validate_input(prompt, min_value, max_value):
    """Проверка ввода для выбора номера строки

    Args:
        prompt (string): "Промт" или запрос пользователю
        min_value (int): Нижняя граница, по умолчанию 0
        max_value (int): Верхняя граница

    Returns:
        int: Либо число, введенное пользователем, либо -1 для выхода
    """    
    while True:
        user_input = input(prompt)
        try:
            value = int(user_input)
            if min_value <= value <= max_value and value != 0:
                return value
            elif value == 0:
                return -1
            else:
                print(f"Введенное значение должно быть в диапазоне от {min_value} до {max_value}")
        except ValueError:
            print("Введенное значение должно быть числом.")
            
def add_zero_before(old_index: str, max_len: str) -> str:
    """Функция для "красивого" вывода индексов

    Args:
        old_index (str): текущий индекс для вывода
        max_len (int): максимальная длина индексов
    
    Returns:
        new_index (str): окончательная версия индекса
    """    
    ln = len(old_index)
    new_index = old_index[:]
    for i in range(max_len-ln):
        new_index = '0' + new_index
    return new_index
        


# test1 = 'erhwogngonwro'
# test2 = '1 minute'
# test3 = '2 hours 3 minutes'

# print(validate_time_format(test1), validate_time_format(test2), validate_time_format(test3))