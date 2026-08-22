from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager
from kivymd.uix.navigationdrawer import MDNavigationDrawer
from kivymd.uix.boxlayout import MDBoxLayout
from models import UserSettings
from storage import load_all_data, save_all_data
from logic import FinanceLogic
from main_screen import MoneyTrackerMainScreen
from calendar_screen import ExpenseCalendarScreen
from drawer_menu import AppDrawerMenu, ChartScreen

class MoneyTrackerApp(MDApp):
    def build(self):
        self.expenses, settings_data = load_all_data()
        self.user_settings = UserSettings(
            username=settings_data.get("username", "المستخدم"),
            language=settings_data.get("language", "ar"),
            dark_mode=settings_data.get("dark_mode", True)
        )
        self.finance_logic = FinanceLogic(self.expenses)
        self.theme_cls.theme_style = "Dark" if self.user_settings.dark_mode else "Light"
        self.theme_cls.primary_palette = "Green"
        self.screen_manager = ScreenManager()
        self.main_screen = MoneyTrackerMainScreen(self.finance_logic, self.user_settings, name='main')
        self.main_screen.menu_btn.bind(on_release=lambda x: self.nav_drawer.set_state("open"))
        self.calendar_screen = ExpenseCalendarScreen(
            self.finance_logic,
            self.user_settings,
            on_save_callback=self.save_data_locally,
            name='calendar'
        )
        self.main_screen.current_month_card.bind(on_release=lambda x: self.open_current_month_calendar())
        self.chart_screen = ChartScreen(self.finance_logic, self.user_settings, name='chart_screen')
        self.screen_manager.add_widget(self.main_screen)
        self.screen_manager.add_widget(self.calendar_screen)
        self.screen_manager.add_widget(self.chart_screen)
        root_layout = MDBoxLayout(orientation="vertical")
        self.nav_drawer = MDNavigationDrawer()
        self.drawer_menu = AppDrawerMenu(
            self.screen_manager,
            self.finance_logic,
            self.user_settings,
            on_save_settings_callback=self.save_data_locally
        )
        self.nav_drawer.add_widget(self.drawer_menu)
        root_layout.add_widget(self.screen_manager)
        from kivy.uix.floatlayout import FloatLayout
        final_root = FloatLayout()
        final_root.add_widget(root_layout)
        final_root.add_widget(self.nav_drawer)
        return final_root

    def open_current_month_calendar(self):
        import datetime
        self.calendar_screen.current_year = datetime.date.today().year
        self.calendar_screen.current_month = datetime.date.today().month
        self.calendar_screen.build_calendar_view()
        self.screen_manager.current = 'calendar'

    def save_data_locally(self):
        save_all_data(self.finance_logic.expenses, self.user_settings)

if __name__ == "__main__":
    MoneyTrackerApp().run()
