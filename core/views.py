from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Visit, UserProfile
from django.utils import timezone
from datetime import timedelta
from .forms import VisitForm, ClientForm
from openpyxl import Workbook
from django.http import HttpResponse

@login_required
def dashboard(request):
    try:
        profile = request.user.userprofile
    except UserProfile.DoesNotExist:
        return redirect('login')

    # Get all visits based on role
    visits = Visit.objects.all().order_by('-visit_date')
    if profile.role == 'AGENT':
        visits = visits.filter(agent=request.user)
    elif profile.role == 'BRANCH_MGR':
        visits = visits.filter(agent__userprofile__branch=profile.branch)

    # --- ANALYTICS LOGIC ---
    now = timezone.now()
    today = now.date()
    yesterday = today - timedelta(days=1)
    
    # Calculate YTD (Year To Date): From Jan 1st of current year
    start_of_year = now.replace(month=1, day=1)

    # Calculate This Week: From the start of this week (Monday)
    start_of_week = today - timedelta(days=today.weekday())

    # FILTER VISITS FOR ANALYTICS
    filtered_visits = visits
    
    ytd_count = filtered_visits.filter(visit_date__gte=start_of_year).count()
    monthly_count = filtered_visits.filter(visit_date__month=now.month, visit_date__year=now.year).count()
    weekly_count = filtered_visits.filter(visit_date__gte=start_of_week).count()
    yesterday_count = filtered_visits.filter(visit_date__date=yesterday).count()

    context = {
        'visits': visits,
        'ytd_count': ytd_count,
        'monthly_count': monthly_count,
        'weekly_count': weekly_count,
        'yesterday_count': yesterday_count,
    }

    return render(request, 'core/dashboard.html', context)

@login_required
def add_visit(request):
    if request.method == 'POST':
        form = VisitForm(request.POST)
        if form.is_valid():
            visit = form.save(commit=False)
            
            # 1. Set Logged in User
            visit.agent = request.user
            
            # 2. Auto-Select Branch (From User Profile)
            # Note: We don't save branch to Visit model, we rely on User Profile.
            
            # 3. Handle Date (If empty, set to Now)
            if not visit.visit_date:
                import datetime
                visit.visit_date = datetime.datetime.now()
                
            visit.save()
            return redirect('dashboard')
    else:
        form = VisitForm()

    return render(request, 'core/add_visit.html', {'form': form})

@login_required
def add_client(request):
    if request.method == 'POST':
        form = ClientForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = ClientForm()

    return render(request, 'core/add_client.html', {'form': form})

@login_required
def export_visits_to_excel(request):
    # 1. Get Data based on User Role
    try:
        profile = request.user.userprofile
    except UserProfile.DoesNotExist:
        return redirect('login')

    visits = Visit.objects.all().order_by('-visit_date')
    
    if profile.role == 'AGENT':
        visits = visits.filter(agent=request.user)
    elif profile.role == 'BRANCH_MGR':
        visits = visits.filter(agent__userprofile__branch=profile.branch)

    # 2. Create Excel Workbook
    workbook = Workbook()
    worksheet = workbook.active
    worksheet.title = 'Visits Report'

    # 3. Define Headers
    headers = ['Agent Username', 'Client Name', 'Client Phone', 'Visit Type', 'Status', 'Date', 'Summary']
    worksheet.append(headers)

    # 4. Add Rows
    for visit in visits:
        row_data = [
            visit.agent.username,
            visit.client.name,
            visit.client.phone,
            visit.visit_type,
            visit.status,
            visit.visit_date.strftime('%Y-%m-%d %H:%M:%S'),
            visit.summary
        ]
        worksheet.append(row_data)

    # 5. Prepare Response
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="visits_report.xlsx"'

    # 6. Save to Response
    workbook.save(response)
    return response