import json
import sys

class Assembler:
    def __init__(self):
        # Внутреннее представление программы - список инструкций
        self.instructions = []
        
    def parse_instruction(self, op):
        """Разбор отдельной инструкции из JSON"""
        # Извлекаем код операции и операнд
        opcode = op.get("opcode")
        operand = op.get("B")
        
        # Проверяем обязательные поля
        if opcode is None or operand is None:
            raise ValueError("Неверный формат инструкции")
            
        # Проверяем допустимые коды операций согласно спецификации УВМ
        valid_opcodes = {22, 62, 26, 45}  # Загрузка, чтение, запись, умножение
        if opcode not in valid_opcodes:
            raise ValueError(f"Неизвестный код операции: {opcode}")
            
        # Проверяем диапазоны операндов в зависимости от типа команды
        if opcode == 22:  # Загрузка константы - 20 бит
            if not (0 <= operand <= 0xFFFFF):  # 0..1048575
                raise ValueError(f"Константа {operand} вне диапазона 0..1048575")
        else:  # Остальные команды - 11 бит для адреса
            if not (0 <= operand <= 0x7FF):  # 0..2047
                raise ValueError(f"Адрес {operand} вне диапазона 0..2047")
                
        # Возвращаем инструкцию в промежуточном представлении
        return {"A": opcode, "B": operand}
    
    def assemble(self, input_file, test_mode=False):
        """Основной метод ассемблирования - преобразует JSON в промежуточное представление"""
        try:
            # Читаем и парсим JSON файл с программой
            with open(input_file, 'r', encoding='utf-8') as f:
                program = json.load(f)
        except Exception as e:
            print(f"Ошибка чтения файла: {e}")
            return False
            
        # Проверяем что программа - это массив инструкций
        if not isinstance(program, list):
            print("Ошибка: программа должна быть массивом инструкций")
            return False
            
        self.instructions = []  # Очищаем предыдущие инструкции
        
        # Обрабатываем каждую инструкцию в программе
        for i, instruction in enumerate(program):
            try:
                parsed = self.parse_instruction(instruction)
                self.instructions.append(parsed)
            except ValueError as e:
                print(f"Ошибка в инструкции {i}: {e}")
                return False
        
        # В режиме тестирования выводим внутреннее представление
        if test_mode:
            self.display_internal_representation()
            
        return True
    
    def display_internal_representation(self):
        """Вывод внутреннего представления в формате полей и значений в тестовом режиме"""
        print("Внутреннее представление программы:")
        for i, instr in enumerate(self.instructions):
            print(f"Инструкция {i}: A={instr['A']}, B={instr['B']}")
        
        # Тестовые примеры из спецификации УВМ для проверки
        test_cases = [
            {"A": 22, "B": 722},  # Загрузка константы
            {"A": 62, "B": 541},  # Чтение из памяти
            {"A": 26, "B": 34},   # Запись в память
            {"A": 45, "B": 94}    # Умножение
        ]
        
        print("\nСравнение с тестовыми примерами из спецификации:")
        for i, test_case in enumerate(test_cases):
            if i < len(self.instructions):
                # Проверяем совпадение с тестовыми данными
                match = (self.instructions[i]["A"] == test_case["A"] and 
                        self.instructions[i]["B"] == test_case["B"])
                status = "СОВПАДАЕТ" if match else "НЕ СОВПАДАЕТ"
                print(f"Тест {i}: {status} (ожидалось A={test_case['A']}, B={test_case['B']})")

def main():
    """CLI-приложение с обработкой аргументов командной строки"""
    if len(sys.argv) < 3:
        print("Использование: python assembler.py <input.json> <output.bin> [--test]")
        return
    
    input_file = sys.argv[1]    # Входной JSON файл
    output_file = sys.argv[2]   # Выходной бинарный файл (на этапе 1 не используется)
    test_mode = "--test" in sys.argv  # Флаг тестового режима
    
    assembler = Assembler()
    
    # Выполняем ассемблирование
    if assembler.assemble(input_file, test_mode):
        print("Ассемблирование завершено успешно")
        # На этапе 1 бинарный файл не создается - только промежуточное представление
    else:
        print("Ошибка ассемблирования")
        sys.exit(1)

if __name__ == "__main__":
    main()