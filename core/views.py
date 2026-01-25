from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Visit, UserProfile
from django.utils import timezone
from datetime import timedelta, datetime
from .forms import VisitForm, AgencyForm
from openpyxl import Workbook
from django.http import HttpResponse
from django.contrib.auth.models import User

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

    # --- MAIN ANALYTICS LOGIC (Based on Visits) ---
    now = timezone.now()
    today = now.date()
    yesterday = today - timedelta(days=1)
    
    start_of_year = now.replace(month=1, day=1)
    start_of_week = today - timedelta(days=today.weekday())

    filtered_visits = visits
    
    ytd_count = filtered_visits.filter(visit_date__gte=start_of_year).count()
    monthly_count = filtered_visits.filter(visit_date__month=now.month, visit_date__year=now.year).count()
    weekly_count = filtered_visits.filter(visit_date__gte=start_of_week).count()
    yesterday_count = filtered_visits.filter(visit_date__date=yesterday).count()

    # --- NEW AGENTS MATRIX LOGIC ---
    
    # 1. Get all Agents joined in current month
    current_month_start = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    
    # Filter Users who are Agents and joined this month
    new_users = User.objects.filter(
        userprofile__role='AGENT',
        date_joined__gte=current_month_start
    )

    # 2. Build Matrix Data
    new_agents_matrix = []
    for user in new_users:
        # Get visits for this specific agent
        agent_visits = visits.filter(agent=user)
        
        agent_weekly = agent_visits.filter(visit_date__gte=start_of_week).count()
        agent_yesterday = agent_visits.filter(visit_date__date=yesterday).count()
        agent_monthly = agent_visits.filter(visit_date__month=now.month, visit_date__year=now.year).count()
        agent_ytd = agent_visits.filter(visit_date__gte=start_of_year).count()

        new_agents_matrix.append({
            'username': user.username,
            'branch': user.userprofile.branch,
            'weekly': agent_weekly,
            'yesterday': agent_yesterday,
            'monthly': agent_monthly,
            'ytd': agent_ytd,
            'joined_date': user.date_joined.date()
        })

    # Sort by Joined Date (Newest first)
    new_agents_matrix.sort(key=lambda x: x['joined_date'], reverse=True)

    context = {
        'visits': visits,
        'ytd_count': ytd_count,
        'monthly_count': monthly_count,
        'weekly_count': weekly_count,
        'yesterday_count': yesterday_count,
        'new_agents_matrix': new_agents_matrix, # New Data
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
            
            # 2. Handle Date (If empty, set to Now)
            if not visit.visit_date:
                visit.visit_date = datetime.now()
                
            visit.save()
            return redirect('dashboard')
    else:
        form = VisitForm()

    return render(request, 'core/add_visit.html', {'form': form})

@login_required
def add_client(request):
    if request.method == 'POST':
        form = AgencyForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = AgencyForm()

    return render(request, 'core/add_client.html', {'form': form})

@login_required
def export_visits_to_excel(request):
    # FIX: Wrap logic in try/except, and put if/else correctly
    try:
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

        # 2. Handle Date Filtering
        if request.method == 'POST':
            start_date_str = request.POST.get('start_date')
            end_date_str = request.POST.get('end_date')

            # Convert string to date object
            if start_date_str and end_date_str:
                start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
                # Add 1 day to end date so it includes the selected end day fully
                end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date() + timedelta(days=1)
            
                visits = visits.filter(visit_date__range=[start_date, end_date])
            else:
                pass # Download all

        # 3. Create Excel Workbook
        workbook = Workbook()
        worksheet = workbook.active
        worksheet.title = 'Visits Report'

        # 4. Define Headers
        headers = ['Agent Username', 'Agency Name', 'Contact Person', 'Mobile Number', 'Email Address', 'Date', 'Type of Business', 'Remarks']
        worksheet.append(headers)

        # 5. Add Rows
        for visit in visits:
            # SAFE CHECK: Check if agency exists before getting name
            agency_name = getattr(visit.agency, 'name', '') 
            
            row_data = [
                visit.agent.username,
                agency_name,
                visit.contact_person,
                visit.mobile_number,
                visit.email_address,
                visit.visit_date.strftime('%Y-%m-%d %H:%M:%S'),
                visit.type_of_business,
                visit.remarks
            ]
            worksheet.append(row_data)

        # 6. Prepare Response
        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename="visits_report.xlsx"'

        # 7. Save to Response
        workbook.save(response)
        return response
    else:
        # If GET request, show the calendar form
        return render(request, 'core/download_excel.html')
    except Exception as e:
        # Print error to console for debugging
        import traceback
        print(f"Export Error: {e}")
        traceback.print_exc()
        return redirect('dashboard') # Redirect to avoid crash on dashboard