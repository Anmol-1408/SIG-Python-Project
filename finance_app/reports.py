import pandas as pd
from django.db.models import Sum
from .models import FinanceRecord

class FinanceReports:
    def __init__(self, user):
        self.user = user

    def get_total_income_expenses(self):
        records = FinanceRecord.objects.filter(user=self.user)
        total_income = records.filter(amount__gt=0).aggregate(total=Sum('amount'))['total'] or 0
        total_expenses = records.filter(amount__lt=0).aggregate(total=Sum('amount'))['total'] or 0
        return total_income, total_expenses

    def get_spending_distribution(self):
        records = FinanceRecord.objects.filter(user=self.user)
        distribution = records.filter(amount__lt=0).values('category').annotate(total=Sum('amount'))
        return pd.DataFrame(distribution)

    def get_trends(self, frequency='M'):
        records = FinanceRecord.objects.filter(user=self.user)
        # Convert the records queryset to a DataFrame
        df = pd.DataFrame(list(records.values()))
        df['date'] = pd.to_datetime(df['date'])  # Convert date to datetime
        df.set_index('date', inplace=True)
        return df.resample(frequency)['amount'].sum()
