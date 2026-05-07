word = "КОМБИНАТОРИКА"
target_length = 5

letter_counts = {}
for char in word:
    if char in letter_counts:
        letter_counts[char] += 1
    else:
        letter_counts[char] = 1

def count_unique_words(remaining_length, available_letters):
    if remaining_length == 0:
        return 1
    
    total_words = 0
    
    for char in available_letters:
        if available_letters[char] > 0:
            available_letters[char] -= 1
            
            total_words += count_unique_words(remaining_length - 1, available_letters)
            
            available_letters[char] += 1
            
    return total_words

result = count_unique_words(target_length, letter_counts)
print("Количество различных 5-буквенных слов:", result)
