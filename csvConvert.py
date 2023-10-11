def remove_spaces(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        content = file.read().replace(' ', '')
    
    with open(filename, 'w', encoding='utf-8') as file:
        file.write(content)
