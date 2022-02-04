from django.shortcuts import redirect, render
from vote.form import VoteForm
from vote.models import VotersList, Votes
from django.contrib import messages
from django.db.models import F
import datetime

# Create your views here.
def homepage(request):
    if request.session.get('id', False):
        if request.method == "POST":
            vote_form = VoteForm(request.POST)
            if vote_form.is_valid():
                id = request.session['id']
                vote_count = VotersList.objects.filter(aadhaar_no=id).count()
                if vote_count != 0:
                    return redirect('access_denied')
                VotersList.objects.create(
                    aadhaar_no=request.session['id'], 
                    name=request.session['name'], 
                    dob=datetime.datetime.strptime(request.session['dob'], "%Y-%m-%d")
                )
                selected = vote_form.cleaned_data['vote']
                isPresent = Votes.objects.filter(candidate=selected).count()
                if isPresent == 0:
                    Votes.objects.create(
                        candidate = selected,
                        votes = 0
                    )
                obj = Votes.objects.get(pk=selected)
                obj.votes = F('votes') + 1
                obj.save()
                request.session.flush()
                messages.success(request, ("Voted Successfully and Logged out. Thank You"))
                return redirect('register')
        id = request.session['id']
        vote_count = VotersList.objects.filter(aadhaar_no=id).count()
        if vote_count != 0:
            request.session.flush()
            messages.warning(request, ("Already voted."))
            return redirect('register')
        return render(request, 'home.html', {'form':VoteForm, 'aadhaar_no': request.session['id']})
    return redirect('register')
    

def access_denied(request):
    return render(request, 'access_denied.html')