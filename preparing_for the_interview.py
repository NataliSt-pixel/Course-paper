class Stack:
    def __init__(self):
        self.items = []
    
    def is_empty(self):
        return len(self.items) == 0
    
    def push(self, item):
        self.items.append(item)
    
    def pop(self):
        if not self.is_empty():
            return self.items.pop()
        return None
    
    def peek(self):
        if not self.is_empty():
            return self.items[-1]
        return None
    
    def size(self):
        return len(self.items)


def is_balanced(brackets_string):
    stack = Stack()
    opening_brackets = "([{"
    closing_brackets = ")]}"
    bracket_pairs = {')': '(', ']': '[', '}': '{'}
    
    for char in brackets_string:
        if char in opening_brackets:
            stack.push(char)
        elif char in closing_brackets:
            if stack.is_empty():
                return "Несбалансированно"
            
            top_element = stack.pop()
            if top_element != bracket_pairs[char]:
                return "Несбалансированно"
    
    return "Сбалансированно" if stack.is_empty() else "Несбалансированно"


if __name__ == "__main__":
    test_cases_balanced = [
        "(((([{}]))))",
        "[([])((([[[]]])))]{()}",
        "{{[()]}}"
    ]
    
    test_cases_unbalanced = [
        "}{}",
        "{{[(])]}}",
        "[[{())}]"
    ]
    
    print("Сбалансированные последовательности:")
    for test in test_cases_balanced:
        result = is_balanced(test)
        print(f"{test}: {result}")
    
    print("\nНесбалансированные последовательности:")
    for test in test_cases_unbalanced:
        result = is_balanced(test)
        print(f"{test}: {result}")
    
    user_input = input("\nВведите строку со скобками для проверки: ")
    result = is_balanced(user_input)
    print(f"Результат: {result}")
