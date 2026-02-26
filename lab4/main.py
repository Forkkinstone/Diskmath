import collections
import math
import heapq
from collections import Counter

# --- ЧТЕНИЕ И ПОДГОТОВКА ТЕКСТА ---
try:
    with open('text.txt', 'r', encoding='utf-8') as f:
        text = f.read()
except FileNotFoundError:
    print("Файл text.txt не найден. Убедись, что он лежит в той же папке.")
    exit()  # Останавливаем выполнение, если файла нет

# Проверка на 64 символа (по условию лабы)
unique_chars_check = set(text)
if len(unique_chars_check) > 64:
    print(f"ВНИМАНИЕ: В тексте {len(unique_chars_check)} уникальных символов! Это больше 64.")
    print("Рекомендуется удалить редкие спецсимволы из text.txt.\n")

# region 1: СТАТИСТИКА
print(f"{'--- ПУНКТ 1: СТАТИСТИЧЕСКИЙ АНАЛИЗ ---':^50}")
total_chars = len(text)
total_pairs = total_chars - 1

char_counts = collections.Counter(text)
unique_chars = len(char_counts)

print(f"Всего символов: {total_chars}")
print(f"Уникальных символов: {unique_chars}\n")
print("Топ-10 символов:")

chars_shown = 0
for char, count in char_counts.most_common():
    if "\n" not in char:
        freq = (count / total_chars) * 100
        display_char = repr(char)
        print(f"Символ {display_char:4}: {count:4} раз ({freq:.2f}%)")
        chars_shown += 1
        if chars_shown == 10:
            break

pairs = [text[i:i+2] for i in range(total_pairs)]
pair_counts = collections.Counter(pairs)

print("\nТоп-10 пар символов:")
pairs_shown = 0
for pair, count in pair_counts.most_common():
    if " " not in pair and "\n" not in pair:
        freq = (count / total_pairs) * 100
        display_pair = repr(pair)
        print(f"Пара {display_pair:6}: {count:4} раз ({freq:.2f}%)")
        pairs_shown += 1
        if pairs_shown == 10:
            break
# endregion

# region 2: ХАФФМАН И ШЕННОН
def perform_analysis_and_get_bits(text_data):
    print(f"\n\n{'--- ПУНКТ 2: ХАФФМАН И ШЕННОН ---':^50}")
    _total_chars = len(text_data)
    frequencies = Counter(text_data)

    # Шеннон
    entropy = 0
    for char in frequencies:
        p_i = frequencies[char] / _total_chars
        entropy -= p_i * math.log2(p_i)

    # Хаффман
    heap = [[weight, [char, ""]] for char, weight in frequencies.items()]
    heapq.heapify(heap)

    while len(heap) > 1:
        lo = heapq.heappop(heap)
        hi = heapq.heappop(heap)
        for pair in lo[1:]:
            pair[1] = '0' + pair[1]
        for pair in hi[1:]:
            pair[1] = '1' + pair[1]
        heapq.heappush(heap, [lo[0] + hi[0]] + lo[1:] + hi[1:])

    huff_codes = dict(heapq.heappop(heap)[1:])

    huff_bits = sum(frequencies[char] * len(huff_codes[char]) for char in frequencies)
    uniform_bits = _total_chars * 6  # По условию (6-ти битовые коды)
    shannon_bits = _total_chars * entropy

    print(f"{'Метод':<25} | {'Бит на симв.':<12} | {'Всего бит':<10}")
    print("-" * 55)
    print(f"{'Равномерный (6 бит)':<25} | {6.0:<12} | {uniform_bits:<10}")
    print(f"{'Код Хаффмана':<25} | {huff_bits / _total_chars:<12.4f} | {huff_bits:<10}")
    print(f"{'Предел Шеннона':<25} | {entropy:<12.4f} | {int(shannon_bits):<10}")

    print(f"\nСжатие Хаффмана относительно 6-бит: {100 - (huff_bits / uniform_bits * 100):.2f}%")

    print(f"\nПримеры кодов Хаффмана (Топ-5 частых):")
    for char, count in frequencies.most_common(5):
        display_char = repr(char)
        print(f"{display_char}: {huff_codes[char]}")

    # ВОЗВРАЩАЕМ ЗНАЧЕНИЯ ДЛЯ ПУНКТА 3
    return huff_bits, uniform_bits


# Вызываем функцию на НАСТОЯЩЕМ тексте и сохраняем результаты
huff_total_bits, uniform_total_bits = perform_analysis_and_get_bits(text)
# endregion

# region 3: LZW
def lzw_encode_and_compare(text_data, huff_bits, uniform_bits):
    print(f"\n\n{'--- ПУНКТ 3: АЛГОРИТМ LZW ---':^50}")
    unique_chars_list = sorted(list(set(text_data)))
    dictionary = {char: i for i, char in enumerate(unique_chars_list)}
    dict_size = len(dictionary)

    result_indices = []
    current_string = ""

    for char in text_data:
        new_string = current_string + char
        if new_string in dictionary:
            current_string = new_string
        else:
            result_indices.append(dictionary[current_string])
            dictionary[new_string] = dict_size
            dict_size += 1
            current_string = char

    if current_string:
        result_indices.append(dictionary[current_string])

    BITS_PER_LZW_TOKEN = 13
    lzw_total_bits = len(result_indices) * BITS_PER_LZW_TOKEN

    print(f"Итоговый размер словаря LZW: {dict_size} гнезд")
    print(f"Количество выведенных индексов: {len(result_indices)}")

    print(f"\n{'--- ФИНАЛЬНОЕ СРАВНЕНИЕ ВСЕХ МЕТОДОВ ---':^50}")
    print(f"{'Метод':<25} | {'Всего бит':<10} | {'Сжатие к 6-бит (%)'}")
    print("-" * 55)
    print(f"{'Равномерный (6 бит)':<25} | {uniform_bits:<10} | 0.00%")

    huff_compression = 100 - (huff_bits / uniform_bits * 100)
    print(f"{'Код Хаффмана':<25} | {huff_bits:<10} | {huff_compression:.2f}%")

    lzw_compression = 100 - (lzw_total_bits / uniform_bits * 100)
    print(f"{'Алгоритм LZW (13 бит)':<25} | {lzw_total_bits:<10} | {lzw_compression:.2f}%")

    return result_indices

# Запускаем, передавая данные из пункта 2
lzw_encode_and_compare(text, huff_total_bits, uniform_total_bits)
# endregion

