from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.textfield import MDTextField
from kivymd.uix.label import MDLabel
from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.list import OneLineListItem
from kivymd.uix.dialog import MDDialog
from kivy.core.window import Window

import random

# Create a list to store calculation history
calculation_history = []

KV = '''
BoxLayout:
    orientation: 'vertical'
    padding: dp(16)
    spacing: dp(7)

    MDRaisedButton:
        text: "Change Theme Color"
        theme_text_color: "Secondary"
        on_release: app.change_theme_color()
        size_hint_y: None
        height: dp(48)
        pos_hint: {'center_x': 0.5}

    MDRaisedButton:
        text: "Change Buttons Color"
        theme_text_color: "Secondary"
        on_release: app.change_button_color()
        size_hint_y: None
        height: dp(48)
        pos_hint: {'center_x': 0.5}

    MDScreen:
        MDBoxLayout:
            orientation: 'vertical'
            spacing: dp(10)
            padding: dp(16)

            MDTextField:
                id: entry1
                hint_text: "Enter first number"
                helper_text: "Numbers only"
                helper_text_mode: "on_error"
                input_filter: "float"
                mode: "rectangle"
                size_hint_x: 0.7  # 70% of screen width

            MDTextField:
                id: entry2
                hint_text: "Enter second number"
                helper_text: "Numbers only"
                helper_text_mode: "on_error"
                input_filter: "float"
                mode: "rectangle"
                size_hint_x: 0.7  # 70% of screen width

            MDBoxLayout:
                orientation: 'horizontal'
                spacing: dp(10)

                MDRaisedButton:
                    text: "+"
                    on_release: app.set_operator("+")

                MDRaisedButton:
                    text: "-"
                    on_release: app.set_operator("-")

                MDRaisedButton:
                    text: "*"
                    on_release: app.set_operator("*")

                MDRaisedButton:
                    text: "/"
                    on_release: app.set_operator("/")

            MDLabel:
                id: selected_operator_label
                text: "Selected Operator: "
                theme_text_color: "Secondary"
                font_style: "Caption"

            MDRaisedButton:
                text: "Submit"
                size_hint_x: None
                width: dp(120)
                pos_hint: {'center_x': 0.5}
                on_release: app.submit()

            MDLabel:
                id: result_label
                text: "Result: "
                theme_text_color: "Secondary"
                font_style: "Caption"
'''


class CalculatorApp(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Dark"  # Set the initial theme
        Window.size = (360, 640)
        return Builder.load_string(KV)

    def change_theme_color(self):
        valid_colors = ["Light", "Dark"]
        random_color = random.choice(valid_colors)
        self.theme_cls.theme_style = random_color

    def change_button_color(self):
        valid_colors = [
            "Red", "Pink", "Purple", "DeepPurple", "Indigo", "Blue", "LightBlue",
            "Cyan", "Teal", "Green", "LightGreen", "Lime", "Yellow", "Amber",
            "Orange", "DeepOrange", "Brown", "Gray", "BlueGray"
        ]
        random_color = random.choice(valid_colors)
        self.theme_cls.primary_palette = random_color

    def set_operator(self, operator):
        self.root.ids.selected_operator_label.text = f"Selected Operator: {operator}"

    def submit(self):
        entry1 = self.root.ids.entry1.text
        entry2 = self.root.ids.entry2.text

        try:
            num1 = float(entry1)
            num2 = float(entry2)
            operator = self.root.ids.selected_operator_label.text.split(': ')[-1].strip()

            result = self.perform_operation(num1, num2, operator)
            result_label = self.root.ids.result_label
            result_label.text = f"Result: {result}"

            # Add the calculation to history
            calculation_history.append(f"{num1} {operator} {num2} = {result}")
            self.update_history()

        except ValueError:
            result_label = self.root.ids.result_label
            result_label.text = 'Please enter valid numbers.'

    def perform_operation(self, num1, num2, operator):
        if operator == '+':
            return num1 + num2
        elif operator == '-':
            return num1 - num2
        elif operator == '*':
            return num1 * num2
        elif operator == '/':
            if num2 != 0:
                return num1 / num2
            else:
                return 'Division by zero is not allowed.'
        else:
            return 'Invalid operation.'

    def update_history(self):
        history_list = self.root.ids.history_list
        history_list.clear_widgets()
        for item in calculation_history:
            history_list.add_widget(OneLineListItem(text=item))
        # Scroll to the latest item
        self.root.ids.history_scrollview.scroll_y = 0

    def clear_history(self):
        if calculation_history:
            self.dialog = MDDialog(
                title="Clear History",
                text="Are you sure you want to clear the history?",
                buttons=[
                    MDRaisedButton(text="Cancel", on_release=self.close_dialog),
                    MDRaisedButton(text="Clear", on_release=self.confirm_clear_history)
                ],
            )
            self.dialog.open()
        else:
            self.dialog = MDDialog(
                title="Clear History",
                text="The history is already empty.",
                buttons=[
                    MDRaisedButton(text="OK", on_release=self.close_dialog)
                ],
            )
            self.dialog.open()

    def confirm_clear_history(self, instance):
        calculation_history.clear()
        self.update_history()
        self.close_dialog()

    def confirm_clear_history(self, instance):
        calculation_history.clear()
        self.update_history()
        self.close_dialog(instance)  # Pass 'instance' as an argument


    def clear_entry(self):
        self.root.ids.entry1.text = ""
        self.root.ids.entry2.text = ""
        self.root.ids.selected_operator_label.text = "Selected Operator: "
        self.root.ids.result_label.text = ""

    def close_dialog(self, instance):
        self.dialog.dismiss()

if __name__ == '__main__':
    CalculatorApp().run()
