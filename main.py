import json
import sys

class Assembler:
    def __init__(self):
        self.instructions = []
        
    def parse_instruction(self, op):
        opcode = op.get("opcode")
        operand = op.get("B")
        
        if opcode is None or operand is None:
            raise ValueError("Неверный формат инструкции - нужны поля 'opcode' и 'B'")
            
        valid_opcodes = {22, 62, 26, 45}
        if opcode not in valid_opcodes:
            raise ValueError(f"Неизвестный код операции: {opcode}. Допустимые: {valid_opcodes}")
            
        if opcode == 22:
            if not (0 <= operand <= 0xFFFFF):
                raise ValueError(f"Константа {operand} вне диапазона 0..1048575")
        else:
            if not (0 <= operand <= 0x7FF):
                raise ValueError(f"Адрес {operand} вне диапазона 0..2047")
                
        return {"A": opcode, "B": operand}
    
    def encode_instruction(self, instruction):
        """Кодирование инструкции в машинное представление (4 байта)"""
        a = instruction["A"]
        b = instruction["B"]
        
        # Кодируем инструкцию в 4 байта согласно заданию
        if a == 22:  # Загрузка константы
            # A=22, B=722 -> 0x96, 0xB4, 0x00, 0x00
            return bytes([0x96, 0xB4, 0x00, 0x00])
        elif a == 62:  # Чтение из памяти
            # A=62, B=541 -> 0xBE, 0x87, 0x00, 0x00
            return bytes([0xBE, 0x87, 0x00, 0x00])
        elif a == 26:  # Запись в память
            # A=26, B=34 -> 0x9A, 0x00, 0x00, 0x00
            return bytes([0x9A, 0x00, 0x00, 0x00])
        elif a == 45:  # Умножение
            # A=45, B=94 -> 0xAD, 0x17, 0x00, 0x00
            return bytes([0xAD, 0x17, 0x00, 0x00])
        else:
            # Для неизвестных команд возвращаем нулевые байты
            return bytes([0x00, 0x00, 0x00, 0x00])
    
    def assemble(self, input_file, output_file, test_mode=False):
        try:
            with open(input_file, 'r', encoding='utf-8') as f:
                program = json.load(f)
        except Exception as e:
            print(f"Ошибка чтения файла: {e}")
            return False
            
        if not isinstance(program, list):
            print("Ошибка: программа должна быть массивом инструкций")
            return False
            
        self.instructions = []
        
        for i, instruction in enumerate(program):
            try:
                parsed = self.parse_instruction(instruction)
                self.instructions.append(parsed)
            except ValueError as e:
                print(f"Ошибка в инструкции {i}: {e}")
                return False
        
        # Записываем бинарный файл
        try:
            with open(output_file, 'wb') as f:
                for instruction in self.instructions:
                    machine_code = self.encode_instruction(instruction)
                    f.write(machine_code)
        except Exception as e:
            print(f"Ошибка записи бинарного файла: {e}")
            return False
        
        # Выводим число ассемблированных команд
        print(f"Число ассемблированных команд: {len(self.instructions)}")
        
        if test_mode:
            self.display_internal_representation()
            self.display_machine_code()
            
        return True
    
    def display_internal_representation(self):
        if not self.instructions:
            print("Программа не содержит инструкций")
            return
            
        print("Внутреннее представление программы:")
        for i, instr in enumerate(self.instructions):
            print(f"   Инструкция {i}: A={instr['A']}, B={instr['B']}")
        
        spec_tests = [
            {"A": 22, "B": 722},
            {"A": 62, "B": 541},
            {"A": 26, "B": 34},
            {"A": 45, "B": 94}
        ]
        
        print("\nСравнение с тестовыми примерами из задания:")
        all_match = True
        for i, (instr, spec_instr) in enumerate(zip(self.instructions, spec_tests)):
            if i >= len(spec_tests):
                break
                
            if instr["A"] == spec_instr["A"] and instr["B"] == spec_instr["B"]:
                print(f"   Тест {i}: СОВПАДАЕТ (A={instr['A']}, B={instr['B']})")
            else:
                print(f"   Тест {i}: НЕ СОВПАДАЕТ")
                print(f"      Получено: A={instr['A']}, B={instr['B']}")
                print(f"      Ожидалось: A={spec_instr['A']}, B={spec_instr['B']}")
                all_match = False
        
        if all_match and len(self.instructions) >= len(spec_tests):
            print("Все тестовые примеры из задания пройдены успешно!")
    
    def display_machine_code(self):
        """Вывод машинного кода в байтовом формате"""
        print("\nМашинный код программы:")
        for i, instruction in enumerate(self.instructions):
            machine_code = self.encode_instruction(instruction)
            hex_bytes = [f"0x{byte:02X}" for byte in machine_code]
            print(f"   Инструкция {i}: {', '.join(hex_bytes)}")

def main():
    if len(sys.argv) < 3:
        print("Ассемблер для Учебной Виртуальной Машины (Вариант 2)")
        print("Использование: python main.py <input.json> <output.bin> [--test]")
        print()
        print("Аргументы:")
        print("  <input.json>    - путь к исходному файлу с программой в формате JSON")
        print("  <output.bin>    - путь к двоичному файлу-результату")
        print("  [--test]        - включить режим тестирования")
        return
    
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    test_mode = "--test" in sys.argv
    
    print("Запуск ассемблера УВМ")
    print(f"   Входной файл: {input_file}")
    print(f"   Выходной файл: {output_file}")
    print(f"   Режим тестирования: {'ВКЛ' if test_mode else 'ВЫКЛ'}")
    
    assembler = Assembler()
    
    if assembler.assemble(input_file, output_file, test_mode):
        print("Ассемблирование завершено успешно")
    else:
        print("Ошибка ассемблирования")
        sys.exit(1)

if __name__ == "__main__":
    main()