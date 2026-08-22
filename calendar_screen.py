import calendar
import datetime
from kivy.uix.screenmanager import Screen
from kivy.uix.gridlayout import GridLayout
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDRaisedButton, MDIconButton
from kivymd.uix.card import MDCard
from kivymd.uix.dialog import MDDialog
from kivymd.uix.textfield import MDTextField
from models import Expense

class ExpenseCalendarScreen(Screen):
    def __init__(self, finance_logic, user_settings, on_save_callback, **kwargs):
        super().__init__(**kwargs)
        self.logic = finance_logic
        self.settings = user_settings
        self.on_save_callback = on_save_callback
        self.dialog = None
        self.current_year = datetime.date.today().year
        self.current_month = datetime.date.today().month
        self.main_layout = MDBoxLayout(orientation='vertical', padding=15, spacing=10)
        self.build_calendar_view()
        self.add_widget(self.main_layout)

    def build_calendar_view(self):
        self.main_layout.clear_widgets()
        is_ar = self.settings.language == "ar"
        title_text = f"مصاريف شهر ({self.current_month} / {self.current_year})" if is_ar else f"Expenses of ({self.current_month} / {self.current_year})"
        title_label = MDLabel(text=title_text, halign="center", font_style="H6", bold=True, size_hint_y=None, height=40)
        self.main_layout.add_widget(title_label)
        grid = GridLayout(cols=8, spacing=5, size_hint_y=0.8)
        days_headers = ["سبت", "أحد", "إثنين", "ثلاثاء", "أربعاء", "خميس", "جمعة", "المجموع"] if is_ar else ["Sat", "Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Total"]
        for header in days_headers:
            grid.add_widget(MDLabel(text=header, halign="center", font_style="Caption", bold=True, theme_text_color="Primary"))
        cal = calendar.Calendar(firstweekday=5)
        month_days = cal.monthdayscalendar(self.current_year, self.current_month)
        weekly_totals = self.logic.get_weekly_totals_for_calendar(self.current_year, self.current_month)
        current_month_expenses = self.logic.filter_expenses_by_month(self.current_year, self.current_month)
        for week_idx, week in enumerate(month_days):
            for day in week:
                if day == 0:
                    grid.add_widget(MDLabel(text=""))
                else:
                    day_expenses = [e for e in current_month_expenses if e.date.day == day]
                    day_total = sum(e.amount for e in day_expenses)
                    day_card = MDCard(orientation='vertical', padding=2, ripple_behavior=True, radius=[5,], style="outlined")
                    day_card.bind(on_release=lambda instance, d=day: self.open_day_details_dialog(d))
                    day_num_label = MDLabel(text=str(day), font_style="Caption", halign="left")
                    total_text = f"{int(day_total)}" if day_total > 0 else ""
                    total_label = MDLabel(text=total_text, font_style="Caption", halign="center", theme_text_color="Custom", text_color=[0.9, 0.3, 0.3, 1])
                    day_card.add_widget(day_num_label)
                    day_card.add_widget(total_label)
                    grid.add_widget(day_card)
            week_sum = weekly_totals.get(week_idx, 0.0)
            week_sum_label = MDLabel(text=f"{int(week_sum)}", halign="center", font_style="Body2", bold=True, theme_text_color="Custom", text_color=[0.5, 0.8, 0.5, 1])
            grid.add_widget(week_sum_label)
        self.main_layout.add_widget(grid)
        back_btn = MDRaisedButton(text="رجوع" if is_ar else "Back", pos_hint={"center_x": 0.5})
        back_btn.bind(on_release=lambda x: self.on_back_pressed())
        self.main_layout.add_widget(back_btn)

    def open_day_details_dialog(self, day):
        is_ar = self.settings.language == "ar"
        date_str = f"{self.current_year}-{self.current_month:02d}-{day:02d}"
        day_expenses = [e for e in self.logic.expenses if e.date.strftime("%Y-%m-%d") == date_str]
        content = MDBoxLayout(orientation='vertical', spacing=10, size_hint_y=None, height=350)
        review_layout = MDBoxLayout(orientation='vertical', spacing=5, size_hint_y=None, height=120)
        if not day_expenses:
            review_layout.add_widget(MDLabel(text="لا توجد مصاريف مسجلة اليوم" if is_ar else "No expenses today", halign="center", font_style="Caption"))
        else:
            for exp in day_expenses:
                row = MDBoxLayout(orientation='horizontal', size_hint_y=None, height=30)
                exp_info = MDLabel(text=f"{exp.name}: {exp.amount}", font_style="Body2", halign="right" if is_ar else "left")
                del_btn = MDIconButton(icon="delete", icon_size="16sp")
                del_btn.bind(on_release=lambda x, e=exp: self.delete_expense_item(e, day))
                if is_ar:
                    row.add_widget(del_btn)
                    row.add_widget(exp_info)
                else:
                    row.add_widget(exp_info)
                    row.add_widget(del_btn)
                review_layout.add_widget(row)
        content.add_widget(review_layout)
        self.name_input = MDTextField(hint_text="اسم النفقة" if is_ar else "Expense name", size_hint_y=None, height=40)
        self.amount_input = MDTextField(hint_text="القيمة" if is_ar else "Amount", input_filter="float", size_hint_y=None, height=40)
        content.add_widget(self.name_input)
        content.add_widget(self.amount_input)
        self.dialog = MDDialog(
            title=f"تفاصيل يوم {day}" if is_ar else f"Details of day {day}",
            type="custom",
            content_cls=content,
            buttons=[
                MDRaisedButton(text="حفظ" if is_ar else "Save", on_release=lambda x: self.save_new_expense(date_str, day)),
                MDRaisedButton(text="إلغاء" if is_ar else "Cancel", on_release=lambda x: self.dialog.dismiss())
            ]
        )
        self.dialog.open()

    def save_new_expense(self, date_str, day):
        name = self.name_input.text.strip()
        amount_text = self.amount_input.text.strip()
        if name and amount_text:
            try:
                amount = float(amount_text)
                if amount > 0:
                    new_exp = Expense(name, amount, date_str)
                    self.logic.expenses.append(new_exp)
                    self.on_save_callback()
                    self.dialog.dismiss()
                    self.build_calendar_view()
            except ValueError:
                pass

    def delete_expense_item(self, expense_obj, day):
        if expense_obj in self.logic.expenses:
            self.logic.expenses.remove(expense_obj)
            self.on_save_callback()
            self.dialog.dismiss()
            self.build_calendar_view()

    def on_back_pressed(self):
        if self.manager:
            main_screen = self.manager.get_screen('main')
            main_screen.curr_amount.text = f"{self.logic.get_current_month_expenses()}"
            main_screen.prev_amount.text = f"{self.logic.get_previous_expenses()}"
            self.manager.current = 'main'
