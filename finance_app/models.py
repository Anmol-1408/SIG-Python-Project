from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class FinanceRecord(models.Model):
    CATEGORY_CHOICES = [
        ('groceries', 'Groceries'),
        ('salary', 'Salary'),
        ('rent', 'Rent'),
        ('utilities', 'Utilities'),
        ('entertainment', 'Entertainment'),
        # Add more categories as needed
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    date = models.DateField()

    def __str__(self):
        return f"{self.description} - {self.amount}"

class FinanceManager:
    def __init__(self, user):
        self.user = user

    def get_records(self):
        return FinanceRecord.objects.filter(user=self.user)

    def total_income(self):
        return self.get_records().filter(category='salary').aggregate(total=models.Sum('amount'))['total']

    def total_expenses(self):
        return self.get_records().exclude(category='salary').aggregate(total=models.Sum('amount'))['total']
