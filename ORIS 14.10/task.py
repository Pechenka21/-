class Task:
    def __init__(self, name: str, description: str, priority: str, options: list):
        self.name = name
        self.description = description
        self.priority = priority
        self.options = options

    def __str__(self):
        options_str = ", ".join(self.options) if self.options else "Нет"
        return f"[{self.priority}] {self.name} — {self.description if self.description else 'Без описания'} (Опции: {options_str})"