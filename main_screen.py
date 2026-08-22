import datetime
from kivy.uix.screenmanager import Screen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.card import MDCard
from kivymd.uix.button import MDIconButton
from advice_bank import get_advice_by_hour

class MoneyTrackerMainScreen(Screen):
    def __init__(self, finance_logic, user_settings, **kwargs):
        super().__init__(**kwargs)
        self.logic = finance_logic
        self.settings = user_settings
        main_layout = MDBoxLayout(orientation='vertical', padding=20, spacing=20)
        header_layout = MDBoxLayout(orientation='vertical', size_hint_y=None, height=120, spacing=5)
        today_str = datetime.datetime.now().strftime("%Y-%m-%d")
        self.date_label = MDLabel(text=today_str, halign="right", theme_text_color="Hint", font_style="Caption")
        welcome_text = "أهلاً بك مجدداً،" if self.settings.language == "ar" else "Welcome back,"
        self.welcome_label = MDLabel(text=welcome_text, halign="right" if self.settings.language == "ar" else "left", font_style="H5", bold=True)
        user_row = MDBoxLayout(orientation='horizontal', size_hint_y=None, height=40)
        self.menu_btn = MDIconButton(icon="menu")
        self.username_label = MDLabel(text=self.settings.username, halign="right" if self.settings.language == "ar" else "left", font_style="Subtitle1")
        if self.settings.language == "ar":
            user_row.add_widget(self.username_label)
            user_row.add_widget(self.menu_btn)
        else:
            user_row.add_widget(self.menu_btn)
            user_row.add_widget(self.username_label)
        header_layout.add_widget(self.date_label)
        header_layout.add_widget(self.welcome_label)
        header_layout.add_widget(user_row)
        cards_layout = MDBoxLayout(orientation='horizontal', size_hint_y=None, height=140, spacing=15)
        self.current_month_card = MDCard(orientation='vertical', padding=15, ripple_behavior=True, radius=[15,])
        curr_title = MDLabel(text="نفقات الشهر الحالي" if self.settings.language == "ar" else "Current Month", halign="center", font_style="Caption")
        self.curr_amount = MDLabel(text=f"{self.logic.get_current_month_expenses()}", halign="center", font_style="H6", bold=True)
        self.current_month_card.add_widget(curr_title)
        self.current_month_card.add_widget(self.amount_label_color(self.curr_amount, "red"))
        self.prev_months_card = MDCard(orientation='vertical', padding=15, radius=[15,])
        prev_title = MDLabel(text="النفقات السابقة" if self.settings.language == "ar" else "Previous Expenses", halign="center", font_style="Caption")
        self.prev_amount = MDLabel(text=f"{self.logic.get_previous_expenses()}", halign="center", font_style="H6", bold=True)
        self.prev_months_card.add_widget(prev_title)
        self.prev_months_card.add_widget(self.amount_label_color(self.prev_amount, "orange"))
        cards_layout.add_widget(self.current_month_card)
        cards_layout.add_widget(self.prev_months_card)
        advice_layout = MDBoxLayout(orientation='vertical', padding=[0, 20, 0, 0])
        self.advice_card = MDCard(orientation='vertical', padding=20, radius=[20,], style="filled")
        advice_header = MDLabel(text="💡 وعي مالي للحرية المالية" if self.settings.language == "ar" else "💡 Financial Freedom Advice", halign="center", font_style="Subtitle2", bold=True)
        current_advice = get_advice_by_hour(self.settings.language)
        self.advice_text = MDLabel(text=current_advice, halign="center", font_style="Body2", theme_text_color="Secondary")
        self.advice_card.add_widget(advice_header)
        self.advice_card.add_widget(self.advice_text)
        advice_layout.add_widget(self.advice_card)
        main_layout.add_widget(header_layout)
        main_layout.add_widget(cards_layout)
        main_layout.add_widget(advice_layout)
        self.add_widget(main_layout)

    def amount_label_color(self, label, color_type):
        if color_type == "red":
            label.theme_text_color = "Custom"
            label.text_color = [0.9, 0.3, 0.3, 1]
        elif color_type == "orange":
            label.theme_text_color = "Custom"
            label.text_color = [0.9, 0.6, 0.2, 1]
        return label
