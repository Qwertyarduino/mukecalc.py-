import ast
import operator
import math

from kivy.app import App
from kivy.core.window import Window
from kivy.metrics import dp
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput


Window.clearcolor = (0.125, 0.129, 0.141, 1)

# Permit only basic arithmetic operations.
OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.UAdd: operator.pos,
    ast.USub: operator.neg,
}


def calculate(expression):
    tree = ast.parse(expression, mode="eval")

    def evaluate(node):
        if isinstance(node, ast.Expression):
            return evaluate(node.body)

        if isinstance(node, ast.Constant):
            if type(node.value) in (int, float):
                return node.value
            raise ValueError("Invalid number")

        if isinstance(node, ast.BinOp):
            op = OPERATORS.get(type(node.op))
            if op is None:
                raise ValueError("Invalid operator")
            return op(evaluate(node.left), evaluate(node.right))

        if isinstance(node, ast.UnaryOp):
            op = OPERATORS.get(type(node.op))
            if op is None:
                raise ValueError("Invalid operator")
            return op(evaluate(node.operand))

        raise ValueError("Invalid expression")

    result = evaluate(tree)

    if isinstance(result, float):
        if not math.isfinite(result):
            raise ValueError("Invalid result")
        result = round(result, 10)

    return str(result)


class MukecalcApp(App):
    def build(self):
        self.title = "Mukecalc"

        root = BoxLayout(
            orientation="vertical",
            padding=dp(10),
            spacing=dp(10),
        )

        self.display = TextInput(
            text="",
            hint_text="0",
            font_size=dp(30),
            multiline=False,
            halign="right",
            size_hint=(1, 0.27),
            background_color=(0.188, 0.192, 0.204, 1),
            foreground_color=(1, 1, 1, 1),
            cursor_color=(1, 1, 1, 1),
        )
        root.add_widget(self.display)

        button_area = GridLayout(
            cols=4,
            spacing=dp(6),
            size_hint=(1, 0.73),
        )

        buttons = [
            "7", "8", "9", "/",
            "4", "5", "6", "*",
            "1", "2", "3", "-",
            "C", "0", ".", "+",
            "(", ")", "⌫", "=",
        ]

        for value in buttons:
            is_equal = value == "="

            button = Button(
                text=value,
                font_size=dp(23),
                bold=True,
                background_normal="",
                background_color=(
                    (0, 1, 0, 1)
                    if is_equal
                    else (0.235, 0.251, 0.263, 1)
                ),
                color=(
                    (0.125, 0.129, 0.141, 1)
                    if is_equal
                    else (1, 1, 1, 1)
                ),
            )

            button.bind(
                on_release=lambda instance, v=value: self.press(v)
            )
            button_area.add_widget(button)

        root.add_widget(button_area)
        return root

    def press(self, value):
        if value == "C":
            self.display.text = ""

        elif value == "⌫":
            self.display.text = self.display.text[:-1]

        elif value == "=":
            try:
                self.display.text = calculate(self.display.text)
            except Exception:
                self.display.text = "Error"

        elif self.display.text == "Error":
            self.display.text = value

        else:
            self.display.text += value


if __name__ == "__main__":
    MukecalcApp().run()