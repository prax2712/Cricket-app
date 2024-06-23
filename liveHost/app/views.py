from . models import innings,match_info,player_match_stats
from django.http import HttpResponse
from django.contrib.auth.models import User, auth
from django.contrib import messages
from . models import player_stats,player_match_stats
from django.db.models import Q 
from django.shortcuts import render, HttpResponse, redirect,get_object_or_404
from django.contrib.auth.models import auth,User
from django.contrib import messages
from .models import player_stats,match_info
from django.urls import reverse

def statistics(request):
    player=None
    if 'search' in request.GET:
        search_term = request.GET['search']
        player = player_stats.objects.filter(
            Q(username__icontains=search_term) | 
            Q(first_name__icontains=search_term) | 
            Q(last_name__icontains=search_term)
        ).first()
    return render(request, 'statistics.html', {'player': player})
def player_selection(request, match_id):
    match = get_object_or_404(match_info, match_id=match_id)
    errors1 = []
    errors2=[]
    flag=0
    if request.method == 'POST':
        no_players=int(request.POST.get('no_players'))
        team1_players = [request.POST.get(f't1player{i}', '') for i in range(1, 16)]
        team2_players = [request.POST.get(f't2player{i}', '') for i in range(1, 16)]
        team1_players_entered=15-sum(1 for i in team1_players if i=='')
        team2_players_entered=15-sum(1 for i in team2_players if i=='')
        print(team1_players)
        print(team1_players_entered)
        print(team2_players)
        print(team2_players_entered)
        if(team2_players_entered!=no_players or team1_players_entered!=no_players):
             print('numner player error')
             return render(request, 'player_selection.html', {'match': match, 'errors1': [0 for i in range(15)],'errors2':[0 for i in range(15)],'duplicates':0,'no_players':1})
        print(len(set(team1_players)))
        print(len(set(team2_players)))

        no_duplicates_list1 = team1_players_entered+1 == len(set(team1_players))
        no_duplicates_list2 = team2_players_entered+1 == len(set(team2_players))
        all_players=len(set(team1_players+team2_players))

        if not (no_duplicates_list1 and no_duplicates_list2 and 2*no_players+1 == all_players):
             print("dup")
             return render(request, 'player_selection.html', {'match': match, 'errors1': [0 for i in range(15)],'errors2':[0 for i in range(15)],'duplicates':1,'no_players':0})
        


        for players in team1_players:
            if(players!=''):
                try:
                    player_stats.objects.get(username=players)
                    errors1.append(0)
                except player_stats.DoesNotExist:
                            errors1.append(1)
            else:
                 errors1.append(0)
        for players in team2_players:
            if(players!=''):
                try:
                    player_stats.objects.get(username=players)
                    errors2.append(0)
                except player_stats.DoesNotExist:
                            errors2.append(1)
            else:
                 errors2.append(0)

        if 1 not in errors1 and 1 not in errors2:
            for player_username in team1_players:
                if(player_username!=''):
                    player=player_stats.objects.get(username=player_username)
                    player1=player_match_stats.objects.create(
                            match_id=match_id,
                            username=player_username,
                            player_name=f"{player.first_name} {player.last_name}",
                            team_name=match.team1,  
                        )
                    player1.save()
            for player_username in team2_players:
                  if(player_username!=''):
                    player=player_stats.objects.get(username=player_username)
                    player1=player_match_stats.objects.create(
                                match_id=match_id,
                                username=player_username,
                                player_name=f"{player.first_name} {player.last_name}",
                                team_name=match.team2,  
                            )
                    player1.save()
            flag=1
        if(flag==1):
             match.no_players=no_players
             match.status=1
             match.save()
             username = match.host
             return redirect('home', username=username) 
    return render(request,'player_selection.html')

from django.http import JsonResponse

def player_suggestions(request):
    query = request.GET.get('q', '')  # Get the search query
    if query:
        players = player_stats.objects.filter(
            Q(username_icontains=query) | Q(first_nameicontains=query) | Q(last_name_icontains=query)
        )[:5]  # Limit to top 5 suggestions
        suggestions = [{'username': player.username, 'first_name': player.first_name, 'last_name': player.last_name} for player in players]
    else:
        suggestions = []
    return JsonResponse(suggestions, safe=False)




def toss(request, match_id):
    match = match_info.objects.get(match_id=match_id)
    username = match.host
    if request.method == 'POST':
        toss_winner = request.POST['toss_winner']
        decision = request.POST['decision']

        match.toss_winner = toss_winner
        match.first_batting = toss_winner if decision == 'bat' else match.team1 if toss_winner == match.team2 else match.team2
        match.first_bowling = match.team1 if match.first_batting == match.team2 else match.team2
        match.status = 2 
        match.save()

        innings.objects.create(match_id=match_id, innings_no=1, 
                               batting_team=match.first_batting, bowling_team=match.first_bowling)
       
             
        
        return redirect("http://127.0.0.1:8000/liveHost/"+str(match.match_id)+"/", username=username)  

    return render(request, 'toss.html', {'match': match})

def login(request):
    if request.method=='POST':
        username=request.POST.get('username')
        password=request.POST.get('password')
        print(f"Username: {username}, Password: {password}")
        

        user=auth.authenticate(request,username=username,password=password)
        print(f"Authenticated User: {user}")  
        if user is not None:
            auth.login(request,user)
            return redirect('home', username=username)
        else:
            messages.info(request,'check your details correctly or register ')
            return redirect('login')
    else:  
        return render(request,'login.html')

def signup(request):
    if request.method == "POST":
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        batting_style = request.POST.get('batting_style')
        bowling_style = request.POST.get('bowling_style')

        if password == confirm_password:
            if User.objects.filter(username=username).exists():
                messages.info(request, 'Username already taken')
                return redirect('signup')
            else:
                user = User.objects.create_user(username=username, password=password)
                user.save()

                user_details = player_stats(
                    first_name=first_name,
                    last_name=last_name,
                    username=username,
                    batting_style=batting_style,
                    bowling_style=bowling_style,
                )
                user_details.save()
                return redirect('login')
        else:
            messages.info(request, 'Passwords do not match')
            return redirect('signup')
    
    return render(request, 'registration.html')

def hosting(request,username):
    if request.method=='POST':
        team1name=request.POST.get('team1name')
        team2name=request.POST.get('team2name')
        date=request.POST.get('dob')
        time=request.POST.get('time')
        noovers=request.POST.get('noovers')
        venue=request.POST.get('venue')
        host_details = match_info(
                    host=username,
                    team1=team1name,
                    team2=team2name,
                    match_date=date,
                    match_time=time,
                    maximum_overs=noovers,
                    venue=venue
                )
        host_details.save()
        match_id = host_details.match_id
        
        return redirect('player_selection', match_id=match_id)
    return render(request,'hosting.html')











def live_host(request,matchId):
    matchId = int(matchId)
    
    match = match_info.objects.all().filter(match_id = matchId,status = 2)[0]
    innings_number = innings.objects.all().filter(match_id = matchId)[0].innings_no
    bating_team =  innings.objects.all().filter(match_id = matchId)[0].batting_team
    bowling_team =  innings.objects.all().filter(match_id = matchId)[0].bowling_team
    innings_obj = innings.objects.all().filter(match_id = matchId)[0]

   
    batsmans = []
    bowlers = []

    l = player_match_stats.objects.all().filter(match_id = matchId,team_name = bating_team)
    for i in l:
        batsmans.append([i.player_name,i.username])
    l = player_match_stats.objects.all().filter(match_id = matchId,team_name = bowling_team)
    for i in l:
        bowlers.append([i.player_name,i.username])
    if innings_obj.player1_username=="":
        innings_obj.player1_username = player_match_stats.objects.all().filter(match_id = matchId,team_name = bating_team)[0].username
        innings_obj.player2_username = player_match_stats.objects.all().filter(match_id = matchId,team_name = bating_team)[1].username
        innings_obj.bowler_username = player_match_stats.objects.all().filter(match_id = matchId,team_name = bowling_team)[0].username
        innings_obj.save()
    content = {
        'matchId':matchId,
        'MatchId':str(matchId),
        'team1':match.team1,
        'team2':match.team2,
        'batsmans1': batsmans,
        'batsmans2': batsmans,
        'bowlers':bowlers,
        'bating_team':bating_team,
        'bowling_team':bowling_team,
        'total_score':innings_obj.runs_scored,
        'total_wickets':innings_obj.wickets,
        'runs_conceded':innings_obj.runs_conceded,
        
    }
    return render(request,'live_host.html',content)

def liveView(request, match_id):
    return render(request, 'liveView.html', {"match_id":match_id})

def homepage(request, username):
    player = get_object_or_404(player_stats, username=username)
    upcoming_matches_host = match_info.objects.filter(
        host=username, 
        status=1
    )
    upcoming_matches = match_info.objects.filter(status=1)
    live_matches = match_info.objects.filter(status=2)
    recent_matches = match_info.objects.filter(status=3)
    direct = "http://127.0.0.1:8000/hosting/"+str(player.username)+"/"
    print(direct)
    
    context = {
        'upcoming_matches' : upcoming_matches,
        'recent_matches' : recent_matches,
        'live_matches': live_matches,
        'upcoming_matches_host': upcoming_matches_host,
        'player': player,
        'direct':direct
    }
    return render(request, 'home.html', context)
def homepageNonUser(request):
    player = None
    
    upcoming_matches = match_info.objects.filter(status=1)
    live_matches = match_info.objects.filter(status=2)
    recent_matches = match_info.objects.filter(status=3)
    context = {
        'upcoming_matches' : upcoming_matches,
        'recent_matches' : recent_matches,
        'live_matches': live_matches,
        'upcoming_matches_host':None,
        'player': player,
        'direct':"/"
    }
    return render(request, 'home.html', context)
def match_summary(request, match_id):
    match = get_object_or_404(match_info, match_id=match_id)
    players_team1=player_match_stats.objects.all().filter(match_id = match_id,team_name = match.first_batting)
    players_team2=player_match_stats.objects.all().filter(match_id = match_id,team_name = match.first_bowling)
    innings1_batting=[]
    innings1_bowling=[]
    innings2_batting=[]
    innings2_bowling=[]
    for i in players_team1:
        if(i.bowls_faced!=0):
            innings1_batting.append([i.player_name,i.runs_scored,i.bowls_faced,i.fours,i.sixes,i.strike_rate])
        if(i.bowls_bowled!=0) :
            innings2_bowling.append([i.player_name,f'{i.bowls_bowled//6}.{i.bowls_bowled%6}',i.runs_conceded,i.wickets,i.economy])
    for i in players_team2:
        if(i.bowls_faced!=0):
            innings2_batting.append([i.player_name,i.runs_scored,i.bowls_faced,i.fours,i.sixes,i.strike_rate])
        if(i.bowls_bowled!=0) :
            innings1_bowling.append([i.player_name,f'{i.bowls_bowled//6}.{i.bowls_bowled%6}',i.runs_conceded,i.wickets,i.economy])
    if(match.match_winner==match.first_batting and match.status == 3):
        result=f"{match.match_winner} won by {abs(match.innings1_score - match.innings2_score)} runs"
    elif(match.match_winner==match.first_bowling and match.status==3):
        result=f"{match.match_winner} won by {abs(min(match.no_players,11)-match.innings2_wickets)-1} wickets"
    else:
        result='Match still in progress'
    context = {
        'match': match,
        'team1_score': f"{match.innings1_score}/{match.innings1_wickets}",
        'team2_score': f"{match.innings2_score}/{match.innings2_wickets}",
        'innings1_overs':match.innings1_overs,
        'innings2_overs':match.innings2_overs,
        'result': result,
        'innings1_batting':innings1_batting,
        'innings1_bowling':innings1_bowling,
        'innings2_batting':innings2_batting,
        'innings2_bowling':innings2_bowling,
    }
    return render(request, 'match_summary.html', context)

