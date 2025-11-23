import subprocess
import os

def test_stage2():
    print("\nТестирование этапа 2: Формирование машинного кода\n")
    
    # Создаем тестовую программу
    test_program = [
        {"opcode": 22, "B": 722},
        {"opcode": 62, "B": 541},
        {"opcode": 26, "B": 34},
        {"opcode": 45, "B": 94}
    ]
    
    # Записываем программу в файл
    with open("test_stage2.json", "w") as f:
        json.dump(test_program, f, indent=2)
    
    # Запускаем ассемблер в тестовом режиме
    print("Запуск ассемблера с тестовой программой")
    result = subprocess.run([
        "python", "main.py", "test_stage2.json", "test_output.bin", "--test"
    ], capture_output=True, text=True)
    
    print("Вывод ассемблера:")
    print(result.stdout)
    if result.stderr:
        print("Ошибки:")
        print(result.stderr)
    
    # Проверяем что бинарный файл создан
    if os.path.exists("test_output.bin"):
        file_size = os.path.getsize("test_output.bin")
        print(f"Размер бинарного файла: {file_size} байт")
        
        # Читаем и проверяем содержимое бинарного файла
        with open("test_output.bin", "rb") as f:
            content = f.read()
            print(f"Содержимое файла: {content.hex()}")
            
            # Проверяем что файл содержит правильное количество байт
            expected_size = 4 * 4  # 4 инструкции по 4 байта
            if file_size == expected_size:
                print("Размер файла корректен")
            else:
                print(f"Ошибка: ожидался размер {expected_size} байт, получено {file_size} байт")
    else:
        print("Ошибка: бинарный файл не создан")
    
    # Убираем временные файлы
    for temp_file in ["test_stage2.json", "test_output.bin"]:
        if os.path.exists(temp_file):
            os.remove(temp_file)


if __name__ == "__main__":
    import json
    test_stage2()