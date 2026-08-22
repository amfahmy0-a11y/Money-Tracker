import datetime
from kivy.uix.screenmanager import Screen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDRaisedButton, MDFlatButton
from kivymd.uix.selectioncontrol import MDSwitch
from kivymd.uix.dialog import MDDialog
from kivymd.uix.textfield import MDTextField
from kivymd.uix.list import MDList, OneLineIconListItem, IconLeftWidget
from kivy.uix.image import Image
import io

class AppDrawerMenu(MDBoxLayout):
    def __init__(self, screen_manager, finance_logic, user_settings, on_save_settings_callback, **kwargs):
        super().__init__(**kwargs)
        self.orientation = "vertical"
        self.padding = 10
        self.spacing = 10
        self.manager = screen_manager
        self.logic = finance_logic
        self.settings = user_settings
        self.save_settings = on_save_settings_callback
        self.dialog = None
        title = "Money Tracker" if self.settings.language == "en" else "متبع الأموال"
        self.add_widget(MDLabel(text=title, font_style="H6", halign="center", size_hint_y=None, height=50))
        ml = MDList()
        item1_text = "الأرشيف والفلتر" if self.settings.language == "ar" else "Archive & Filter"
        item1 = OneLineIconListItem(text=item1_text)
        item1.add_widget(IconLeftWidget(icon="folder-zip"))
        item1.bind(on_release=lambda x: self.open_month_selector_dialog(target="archive"))
        item2_text = "التحليل البياني" if self.settings.language == "ar" else "Pie Chart Analysis"
        item2 = OneLineIconListItem(text=item2_text)
        item2.add_widget(IconLeftWidget(icon="chart-pie"))
        item2.bind(on_release=lambda x: self.open_month_selector_dialog(target="chart"))
        item3_text = "الإعدادات" if self.settings.language == "ar" else "Settings"
        item3 = OneLineIconListItem(text=item3_text)
        item3.add_widget(IconLeftWidget(icon="cog"))
        item3.bind(on_release=lambda x: self.open_settings_dialog())
        ml.add_widget(item1)
        ml.add_widget(item2)
        ml.add_widget(item3)
        self.add_widget(ml)

    def open_month_selector_dialog(self, target):
        content = MDBoxLayout(orientation='horizontal', spacing=10, size_hint_y=None, height=50)
        month_input = MDTextField(hint_text="الشهر (1-12)" if self.settings.language == "ar" else "Month", input_filter="int", text=str(datetime.date.today().month))
        year_input = MDTextField(hint_text="السنة" if self.settings.language == "ar" else "Year", input_filter="int", text=str(datetime.date.today().year))
        content.add_widget(month_input)
        content.add_widget(year_input)
        title_text = "اختر الشهر والسنة" if self.settings.language == "ar" else "Select Month & Year"
        self.dialog = MDDialog(
            title=title_text,
            type="custom",
            content_cls=content,
            buttons=[
                MDRaisedButton(text="تأكيد" if self.settings.language == "ar" else "Confirm", on_release=lambda x: self.process_selection(target, month_input.text, year_input.text)),
                MDFlatButton(text="إلغاء" if self.settings.language == "ar" else "Cancel", on_release=lambda x: self.dialog.dismiss())
            ]
        )
        self.dialog.open()

    def process_selection(self, target, month_str, year_str):
        try:
            month = int(month_str)
            year = int(year_str)
            if 1 <= month <= 12 and year > 2000:
                self.dialog.dismiss()
                if target == "archive":
                    cal_screen = self.manager.get_screen('calendar')
                    cal_screen.current_year = year
                    cal_screen.current_month = month
                    cal_screen.build_calendar_view()
                    self.manager.current = 'calendar'
                elif target == "chart":
                    chart_screen = self.manager.get_screen('chart_screen')
                    chart_screen.load_chart(year, month)
                    self.manager.current = 'chart_screen'
        except ValueError:
            pass

    def open_settings_dialog(self):
        content = MDBoxLayout(orientation='vertical', spacing=15, size_hint_y=None, height=220)
        name_input = MDTextField(hint_text="اسم المستخدم" if self.settings.language == "ar" else "Username", text=self.settings.username)
        content.add_widget(name_input)
        lang_layout = MDBoxLayout(orientation='horizontal', spacing=10, size_hint_y=None, height=40)
        lang_label = MDLabel(text="اللغة / Language:" , font_style="Body2")
        ar_btn = MDFlatButton(text="العربية", theme_text_color="Custom", text_color=[0,1,0,1] if self.settings.language == "ar" else [0.5,0.5,0.5,1])
        en_btn = MDFlatButton(text="English", theme_text_color="Custom", text_color=[0,1,0,1] if self.settings.language == "en" else [0.5,0.5,0.5,1])
        def set_lang(l):
            self.settings.language = l
            ar_btn.text_color = [0,1,0,1] if l == "ar" else [0.5,0.5,0.5,1]
            en_btn.text_color = [0,1,0,1] if l == "en" else [0.5,0.5,0.5,1]
        ar_btn.bind(on_release=lambda x: set_lang("ar"))
        en_btn.bind(on_release=lambda x: set_lang("en"))
        lang_layout.add_widget(lang_label)
        lang_layout.add_widget(ar_btn)
        lang_layout.add_widget(en_btn)
        content.add_widget(lang_layout)
        dark_layout = MDBoxLayout(orientation='horizontal', spacing=10, size_hint_y=None, height=40)
        dark_label = MDLabel(text="الوضع الداكن / Dark Mode:" if self.settings.language == "ar" else "Dark Mode:", font_style="Body2")
        switch = MDSwitch(active=self.settings.dark_mode)
        dark_layout.add_widget(dark_label)
        dark_layout.add_widget(switch)
        content.add_widget(dark_layout)
        self.dialog = MDDialog(
            title="الإعدادات" if self.settings.language == "ar" else "Settings",
            type="custom",
            content_cls=content,
            buttons=[
                MDRaisedButton(text="حفظ" if self.settings.language == "ar" else "Save", on_release=lambda x: self.save_all_settings(name_input.text, switch.active)),
                MDFlatButton(text="إلغاء" if self.settings.language == "ar" else "Cancel", on_release=lambda x: self.dialog.dismiss())
            ]
        )
        self.dialog.open()

    def save_all_settings(self, new_name, is_dark):
        self.settings.username = new_name.strip() if new_name.strip() else self.settings.username
        self.settings.dark_mode = is_dark
        self.save_settings()
        self.dialog.dismiss()
        from kivymd.app import MDApp
        app = MDApp.get_running_app()
        app.theme_cls.theme_style = "Dark" if is_dark else "Light"
        main_screen = self.manager.get_screen('main')
        main_screen.username_label.text = self.settings.username
        main_screen.manager.current = 'main'

class ChartScreen(Screen):
    def __init__(self, finance_logic, user_settings, **kwargs):
        super().__init__(**kwargs)
        self.logic = finance_logic
        self.settings = user_settings
        self.layout = MDBoxLayout(orientation='vertical', padding=20, spacing=15)
        self.add_widget(self.layout)

    def load_chart(self, year, month):
        self.layout.clear_widgets()
        chart_data = self.logic.generate_pie_chart(year, month, self.settings.language)
        if chart_data == "no_data":
            no_data_label = MDLabel(
                text=f"لا توجد مصروفات مسجلة لشهر {month}-{year} لتحليلها بيانيًا." if self.settings.language == "ar" else f"No data recorded for {month}-{year}.",
                halign="center", font_style="Subtitle1", theme_text_color="Secondary"
            )
            self.layout.add_widget(no_data_label)
        else:
            import base64
            from kivy.core.image import Image as CoreImage
            base64_img = chart_data.split(",")[1]
            img_bytes = base64.b64decode(base64_img)
            data = io.BytesIO(img_bytes)
            core_img = CoreImage(data, ext="png")
            chart_image = Image()
            chart_image.texture = core_img.texture
            self.layout.add_widget(chart_image)
