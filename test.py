import subprocess
import os

def run_test(test_name, input_file, expected_success=True):
    """Запускает один тест и проверяет результат"""
    print(f"\ Тест: {test_name}")
    
    # Проверяем существует ли файл
    if not os.path.exists(input_file):
        print(f"Файл {input_file} не найден!")
        return
    
    # Запускаем ассемблер в тестовом режиме
    result = subprocess.run(
        ["python", "main.py", input_file, "test_output.bin", "--test"],
        capture_output=True,
        text=True
    )
    
    if expected_success:
        if result.returncode == 0:
            print("УСПЕХ: Программа собралась корректно")
            # Выводим что получилось
            for line in result.stdout.split('\n'):
                if "Инструкция" in line or "СОВПАДАЕТ" in line or "НЕ СОВПАДАЕТ" in line:
                    print(f"  {line}")
        else:
            print(f"ОШИБКА: Программа не собралась (код: {result.returncode})")
            if result.stderr:
                for line in result.stderr.split('\n'):
                    if line.strip():
                        print(f"  {line}")
    else:
        if result.returncode != 0:
            print("УСПЕХ: Ошибка обработана корректно")
            if result.stderr:
                for line in result.stderr.split('\n'):
                    if line.strip() and "Ошибка" in line:
                        print(f"  {line}")
        else:
            print("ОШИБКА: Программа собралась, хотя должна была завершиться ошибкой")
    
    print()

def main():
    print("\nЗАПУСК ТЕСТОВ АССЕМБЛЕРА УВМ\n")
    
    # Тест 1: Корректная программа из задания
    run_test("Корректная программа из задания", "test1_correct.json", True)
    
    # Тест 2: Программа с ошибкой (неизвестная команда)
    run_test("Неизвестный код операции", "test2_error_opcode.json", False)
    
    # Тест 3: Программа с ошибкой (выход за диапазон)
    run_test("Выход за диапазон константы", "test3_error_range.json", False)
    
    # Тест 4: Пустая программа
    run_test("Пустая программа", "test4_empty.json", True)
    
    # Тест 5: Отсутствует поле B
    run_test("Отсутствует поле B", "test5_missing_field.json", False)
    
    # Убираем временный файл вывода, если он создался
    if os.path.exists("test_output.bin"):
        os.remove("test_output.bin")

if __name__ == "__main__":
    main()