import re
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from vote.models import Votes, VotersList
from vote.form import CHOICES
from django.contrib import messages

# Create your views here.
@login_required
def dashboard(request):
    if request.user.is_superuser:
        if request.method == "POST":
            return redirect('clear_database')
        results = []
        for choice in CHOICES:
            candidate = choice[1]
            count = Votes.objects.filter(candidate=candidate).count()
            if count != 0:
                votes = Votes.objects.get(candidate=candidate).votes
                results.append((candidate, votes))
            else:
                results.append((candidate, 0))
        results = sorted(results, key=lambda x: x[1], reverse=True)
        return render(request, 'dashboard.html', {'results': results})
    return redirect('unauthorized')

def unauthorized(request):
    return render(request, 'unauthorized.html')

@login_required
def clear_database(request):
    if request.user.is_superuser:
        votes = Votes.objects.all()
        votes.delete()
        voters = VotersList.objects.all()
        voters.delete()
        messages.success(request, ("Voting database cleared successfully."))
        return redirect('dashboard') 
    return redirect('unauthorized')
