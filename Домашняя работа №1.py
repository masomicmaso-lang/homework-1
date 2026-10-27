# Словари с словами для изучения (русский: испанский)
words_easy = {
    "друг": "amigo",
    "дом": "casa",
    "хлеб": "pan",
    "вода": "agua",
    "солнце": "sol"
}

words_medium = {
    "холодный": "frio",
    "книга": "libro",
    "улица": "calle",
    "хороший": "bueno",
    "красивый": "hermoso"
}

words_hard = {
    "художник": "pintor",
    "усердный": "diligente",
    "иностранный": "extranjero",
    "перевод": "traduccion",
    "свобода": "libertad"
}

# Словарь для рангов
ranks = {
    0: "Нулевой",
    1: "Так себе",
    2: "Можно лучше",
    3: "Норм",
    4: "Хорошо",
    5: "Отлично!"
}

# Приветствие и выбор уровня
print("Привет! Это тренажёр для изучения испанского.")
user_input = input("Выбери уровень сложности: легкий, средний, сложный.\n> ").lower().strip()

# Обработка выбора уровня
if user_input == "легкий":
    words = words_easy
    print('Отлично! Выбран уровень "легкий", мы предложим 5 слов для перевода.')
elif user_input == "средний":
    words = words_medium
    print('Отлично! Выбран уровень "средний", мы предложим 5 слов для перевода.')
elif user_input == "сложный":
    words = words_hard
    print('Отлично! Выбран уровень "сложный", мы предложим 5 слов для перевода.')
else:
    print("Такого уровня нет. Запустите программу снова.")
    exit()

# Инициализация переменных
user_score = 0
correct_words = []
incorrect_words = []

# Главный цикл по словам
for russian_word, spanish_word in words.items():
    print(f"\nСлово: '{russian_word}', {len(spanish_word)} букв, начинается на '{spanish_word[0]}'...")
    attempts = 3
    is_correct = False
    
    # Цикл попыток
    while attempts > 0:
        user_answer = input("> ").lower().strip()
        
        if user_answer == spanish_word:
            is_correct = True
            if attempts == 3:
                points = 3
            elif attempts == 2:
                points = 2
            else:
                points = 1
            user_score += points
            print(f"Верно! Вы получаете {points} балла!")
            correct_words.append(russian_word)
            break
        else:
            attempts -= 1
            if attempts > 0:
                print(f"Неверно! Осталось попыток: {attempts}, попробуйте еще раз!")
            else:
                print(f"Увы, но нет. Верный ответ: {spanish_word}.")
                incorrect_words.append(russian_word)

# Вывод результатов
print("\nВот и все!")

print("Правильно угаданные слова:")
for word in correct_words:
    print(word)

print("\nНеправильно угаданные слова:")
for word in incorrect_words:
    print(word)

# Определение и вывод ранга
correct_count = len(correct_words)
user_rank = ranks.get(correct_count, "Нулевой")

print(f"\nВы набрали {user_score} баллов.")
print(f"Ваш ранг: {user_rank}")
