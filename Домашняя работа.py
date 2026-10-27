import random

# Шаг 0. Подготовка словарей
WORDS = ['code', 'bit', 'list', 'soul', 'next', 'little', 'snake', 'mouse']
MORSE_DICT = {
    '0': '-----', '1': '.----', '2': '..---', '3': '...--', '4': '....-',
    '5': '.....', '6': '-....', '7': '--...', '8': '---..', '9': '----.',
    'a': '.-', 'b': '-...', 'c': '-.-.', 'd': '-..', 'e': '.', 'f': '..-.',
    'g': '--.', 'h': '....', 'i': '..', 'j': '.---', 'k': '-.-', 'l': '.-..',
    'm': '--', 'n': '-.', 'o': '---', 'p': '.--.', 'q': '--.-', 'r': '.-.',
    's': '...', 't': '-', 'u': '..-', 'v': '...-', 'w': '.--', 'x': '-..-',
    'y': '-.--', 'z': '--..', '.': '.-.-.-', ',': '--..--', '?': '..--..',
    "'": '.----.', '!': '-.-.--', '/': '-..-.', '(': '-.--.', ')': '-.--.-',
    '&': '.-...', ':': '---...', ';': '-.-.-.', '=': '-...-', '+': '.-.-.',
    '-': '-....-', '_': '..--.-', '"': '.-..-.', '$': '...-..-', '@': '.--.-.'
}

def english_to_morse(text):
    """
    Переводит английский текст в код Морзе.
    Args:
        text (str): Строка на английском языке
    Returns:
        str: Текст, преобразованный в код Морзе
    """
    morse_text = []
    for char in text.lower():
        if char in MORSE_DICT:
            morse_text.append(MORSE_DICT[char])
        elif char == ' ':
            # Добавляем разделитель для слов, если ввели предложение
            morse_text.append('/')
    return " ".join(morse_text)

def morse_to_english(morse_text):
    """
    Переводит код Морзе обратно в английский текст.
    Args:
        morse_text (str): Текст в коде Морзе
    Returns:
        str: Декодированный английский текст
    """
    # Создаем обратный словарь для быстрого поиска (просто и понятно для 1 курса)
    reverse_morse_dict = {}
    for key, value in MORSE_DICT.items():
        reverse_morse_dict[value] = key
    
    english_text = []
    # Разбиваем строку по пробелам
    for code in morse_text.split():
        if code in reverse_morse_dict:
            english_text.append(reverse_morse_dict[code])
        elif code == '/':
            english_text.append(' ')
    return "".join(english_text)

def get_random_word():
    """
    Возвращает случайное слово из списка WORDS.
    Returns:
        str: Случайное слово из списка
    """
    return random.choice(WORDS)

def print_statistics(answers):
    """
    Выводит статистику ответов пользователя.
    Args:
        answers (list): Список булевых значений (True/False)
    """
    total = len(answers)
    correct = sum(answers) # В Python True = 1, False = 0, поэтому sum() отлично работает
    incorrect = total - correct
    print(f"\nВсего вопросов: {total}")
    print(f"Верных ответов: {correct}")
    print(f"Неверных ответов: {incorrect}")

def main():
    """
    Основная функция программы, управляющая всеми режимами работы.
    """
    print("Добрый день! Введите ваше имя:")
    name = input().strip()
    print(f"Отлично, {name}! Выберите режим работы:")
    
    while True:
        print("1 - шифрование (английский -> Морзе)")
        print("2 - дешифрование (Морзе -> английский)")
        print("3 - Игра «Угадай слово» (5 вопросов)")
        print("4 - Выход")
        choice = input().strip()
        
        if choice == '1':
            text = input("Введите текст для шифрования: ")
            print(english_to_morse(text))
        elif choice == '2':
            morse_code = input("Введите код Морзе (буквы через пробел): ")
            print(morse_to_english(morse_code))
        elif choice == '3':
            answers = []
            print("Игра началась!") # Для удобства, можно не писать
            for i in range(1, 6):
                word = get_random_word()
                morse_word = english_to_morse(word)
                print(f"Слово {i}: {morse_word}")
                user_answer = input().strip().lower()
                if user_answer == word:
                    print(f"Верно, это слово: {word}")
                    answers.append(True)
                else:
                    print(f"Неверно! Зашифрованное слово было: {word}")
                    answers.append(False)
            print_statistics(answers)
        elif choice == '4':
            print("До свидания!")
            break # Выход из цикла while, программа завершается
        else:
            print("Неверный ввод. Пожалуйста, выберите пункт от 1 до 4.")

# Точка входа в программу (стандартная практика)
if __name__ == "__main__":
    main()