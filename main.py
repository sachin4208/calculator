from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.textfield import MDTextField
from kivymd.uix.label import MDLabel
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.scrollview import ScrollView
from kivymd.uix.list import OneLineListItem
import random
from kivymd.uix.dialog import MDDialog

# Create a list to store calculation history
calculation_history = []

KV = '''
ScreenManager:
    MainScreen:

<MainScreen>:
    name: 'main'
    BoxLayout:
        orientation: 'vertical'
        spacing:dp(7)

        MDRaisedButton:
            text: "Change Theme Color"
            theme_text_color: "Secondary"
            on_release: app.change_theme_color()
            size_hint: None, None
            size: dp(200), dp(48)
            pos_hint: {'center_x': 0.5}

        MDRaisedButton:
            text: "Change Buttons Color"
            theme_text_color: "Secondary"
            on_release: app.change_button_color()
            size_hint: None, None
            size: dp(200), dp(48)
            pos_hint: {'center_x': 0.5}

        MDTextField:
            id: entry1
            hint_text: "Enter first number"
            helper_text: "Numbers only"
            helper_text_mode: "on_error"
            input_filter: "float"
            mode: "rectangle"
            size_hint: None, None
            width: dp(250)
            height: dp(48)
            pos_hint: {'center_x': 0.5}

        MDTextField:
            id: entry2
            hint_text: "Enter second number"
            helper_text: "Numbers only"
            helper_text_mode: "on_error"
            input_filter: "float"
            mode: "rectangle"
            size_hint: None, None
            width: dp(250)
            height: dp(48)
            pos_hint: {'center_x': 0.5}

        BoxLayout:
            orientation: 'horizontal'
            spacing: dp(10)
            size_hint: None, None
            width: dp(290)
            height: dp(50)
            pos_hint: {'center_x': 0.5}

            MDRaisedButton:
                text: "+"
                size_hint: None, None
                size: dp(45), dp(45)
                on_release: app.set_operator("+")
                pos_hint: {'center_y': 0.4}

            MDRaisedButton:
                text: "-"
                size_hint: None, None
                size: dp(45), dp(45)
                on_release: app.set_operator("-")

            MDRaisedButton:
                text: "*"
                size_hint: None, None
                size: dp(45), dp(45)
                on_release: app.set_operator("*")

            MDRaisedButton:
                text: "/"
                size_hint: None, None
                size: dp(45), dp(45)
                on_release: app.set_operator("/")

        MDLabel:
            id: selected_operator_label
            text: "Selected Operator: "
            theme_text_color: "Secondary"
            font_style: "Caption"
            size_hint: None, None
            size: dp(200), dp(48)
            pos_hint: {'center_x': 0.5}

        MDRaisedButton:
            text: "Submit"
            size_hint: None, None
            size: dp(120), dp(48)
            pos_hint: {'center_x': 0.5}
            on_release: app.submit()

        MDLabel:
            id: result_label
            text: "Result: "
            theme_text_color: "Secondary"
            font_style: "Caption"
            size_hint: None, None
            size: dp(200), dp(48)
            pos_hint: {'center_x': 0.5}

        BoxLayout:
            orientation: 'horizontal'
            spacing: dp(10)
            size_hint: None, None
            width: dp(200)
            height: dp(48)
            pos_hint: {'center_x': 0.5}

            MDRaisedButton:
                text: "Clear History"
                on_release: app.clear_history()

            MDRaisedButton:
                text: "Clear Entry"
                on_release: app.clear_entry()

        MDLabel:
            text: "History"
            theme_text_color: "Secondary"
            font_style: "Caption"
            size_hint: None, None
            size: dp(100), dp(48)
            pos_hint: {'center_x': 0.5}

        MDScrollView:
            id: history_scrollview
            
            size_hint: None, None
            size: dp(300), dp(48)
            pos_hint: {'center_x': 0.5}
            mode: "rectangle"

            MDList:
                id: history_list
                
'''

class MainScreen(Screen):
    pass

class CalculatorApp(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Dark"  # Set the initial theme
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
        self.root.get_screen('main').ids.selected_operator_label.text = f"Selected Operator: {operator}"

    def submit(self):
        entry1 = self.root.get_screen('main').ids.entry1.text
        entry2 = self.root.get_screen('main').ids.entry2.text

        try:
            num1 = float(entry1)
            num2 = float(entry2)
            operator = self.root.get_screen('main').ids.selected_operator_label.text.split(': ')[-1].strip()

            result = self.perform_operation(num1, num2, operator)
            result_label = self.root.get_screen('main').ids.result_label
            result_label.text = f"Result: {result}"

            # Add the calculation to history
            calculation_history.append(f"{num1} {operator} {num2} = {result}")
            self.update_history()

        except ValueError:
            result_label = self.root.get_screen('main').ids.result_label
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
        history_list = self.root.get_screen('main').ids.history_list
        history_list.clear_widgets()
        for item in calculation_history:
            history_list.add_widget(OneLineListItem(text=item))
        # Scroll to the latest item
        self.root.get_screen('main').ids.history_scrollview.scroll_y = 0

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
        self.close_dialog(instance)  # Pass 'instance' as an argument

    def clear_entry(self):
        main_screen = self.root.get_screen('main')
        main_screen.ids.entry1.text = ""
        main_screen.ids.entry2.text = ""
        main_screen.ids.selected_operator_label.text = "Selected Operator: "
        main_screen.ids.result_label.text = ""

    def close_dialog(self, instance):
        self.dialog.dismiss()

if __name__ == '__main__':
    CalculatorApp().run()
