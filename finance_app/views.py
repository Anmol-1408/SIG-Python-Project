from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import FinanceRecord
from .forms import FinanceRecordForm
from .reports import FinanceReports

from django.contrib import messages

# Create your views here.

@login_required
def finance_dashboard(request):
    records = FinanceRecord.objects.filter(user=request.user)
    context = {'records': records}
    return render(request, 'dashboard.html', context)

@login_required
def add_record(request):
    if request.method == "POST":
        form = FinanceRecordForm(request.POST)
        if form.is_valid():
            record = form.save(commit=False)
            record.user = request.user
            record.save()

            # Create an expense record only if the user opted for it
            if form.cleaned_data['include_as_expense'] and record.amount > 0:
                expense_record = FinanceRecord(
                    user=request.user,
                    description=f"{record.description} (Income)",
                    amount=-record.amount,  # Negative amount for expense
                    category=record.category,
                    date=record.date
                )
                expense_record.save()
                messages.success(request, 'Record added as income and an expense created!')

            else:
                messages.success(request, 'Record added as income!')

            # Redirect to the record list after saving
            return redirect('finance_dashboard')
    else:
        form = FinanceRecordForm()
    return render(request, 'add_record.html', {'form': form})

@login_required
def update_record(request, record_id):
    record = FinanceRecord.objects.get(id=record_id)
    if request.method == 'POST':
        form = FinanceRecordForm(request.POST, instance=record)
        if form.is_valid():
            form.save()
            return redirect('finance_dashboard')
    else:
        form = FinanceRecordForm(instance=record)
    return render(request, 'edit_record.html', {'form': form})

@login_required
def delete_record(request, record_id):
    record = FinanceRecord.objects.get(id=record_id)
    record.delete()
    return redirect('finance_dashboard')

@login_required
def generate_financial_reports(request):
    if request.user.is_authenticated:
        report = FinanceReports(request.user)
        total_income, total_expenses = report.get_total_income_expenses()
        spending_distribution = report.get_spending_distribution()
        trends = report.get_trends('M')  # Monthly trends
        return render(request, 'reports.html', {
            'total_income': total_income,
            'total_expenses': total_expenses,
            'spending_distribution': spending_distribution.to_html(classes='table table-striped', index=False),
            'trends': trends.to_frame().reset_index().to_html(classes='table table-striped', index=False)
        })
    else:
        return redirect('login')