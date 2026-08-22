import datetime
from typing import List, Dict
from models import Expense

class FinanceLogic:
    def __init__(self, expenses_list: List[Expense]):
        self.expenses = expenses_list

    def get_current_month_expenses(self) -> float:
        today = datetime.date.today()
        total = 0.0
        for e in self.expenses:
            if e.date.year == today.year and e.date.month == today.month:
                total += e.amount
        return total

    def get_previous_expenses(self) -> float:
        today = datetime.date.today()
        total = 0.0
        for e in self.expenses:
            if e.date.year < today.year or (e.date.year == today.year and e.date.month < today.month):
                total += e.amount
        return total

    def filter_expenses_by_month(self, year: int, month: int) -> List[Expense]:
        return [e for e in self.expenses if e.date.year == year and e.date.month == month]

    def get_weekly_totals_for_calendar(self, year: int, month: int) -> Dict[int, float]:
        import calendar
        cal = calendar.monthcalendar(year, month)
        weekly_totals = {}
        month_expenses = self.filter_expenses_by_month(year, month)
        for week_idx, week in enumerate(cal):
            week_sum = 0.0
            for day in week:
                if day != 0:
                    week_sum += sum(e.amount for e in month_expenses if e.date.day == day)
            weekly_totals[week_idx] = week_sum
        return weekly_totals

    def generate_pie_chart(self, year: int, month: int, lang="ar") -> str:
        import matplotlib.pyplot as plt
        import io
        import base64
        month_expenses = self.filter_expenses_by_month(year, month)
        category_totals = {}
        for e in month_expenses:
            category_totals[e.name] = category_totals.get(e.name, 0.0) + e.amount
        if not category_totals:
            return "no_data"
        labels = list(category_totals.keys())
        sizes = list(category_totals.values())
        colors = ['#81c784', '#64b5f6', '#ffb74d', '#ba68c8', '#e57373', '#4db6ac']
        plt.figure(figsize=(6, 6), facecolor='none')
        wedges, texts, autotexts = plt.pie(
            sizes, labels=labels, autopct='%1.1f%%', startangle=140,
            colors=colors, textprops=dict(color="w" if lang=="ar" else "b")
        )
        for autotext in autotexts:
            autotext.set_color('white')
            autotext.set_weight('bold')
        title_text = f"تحليل مصاريف: {month}-{year}" if lang == "ar" else f"Expenses Analysis: {month}-{year}"
        plt.title(title_text, color='#81c784', fontsize=14, weight='bold')
        buf = io.BytesIO()
        plt.savefig(buf, format='png', bbox_inches='tight', transparent=True)
        buf.seek(0)
        base64_str = base64.b64encode(buf.read()).decode('utf-8')
        plt.close()
        return f"data:image/png;base64,{base64_str}"
