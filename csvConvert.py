def remove_spaces(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        content = file.read().replace(' ', '')
    
    with open(filename, 'w', encoding='utf-8') as file:
        file.write(content)

if __name__ == "__main__":
    filename = "25_komplett.csv"
    remove_spaces(filename)
    print(f"Leerzeichen in '{filename}' wurden entfernt.")
