from channels.generic.websocket import JsonWebsocketConsumer,AsyncJsonWebsocketConsumer
from . models import innings,player_match_stats,match_info,player_stats,overs_timeline
import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from django.db.models import Prefetch
# from rest_framework import serializers

class LiveHostWebsocket(JsonWebsocketConsumer):
    def change_ball(self,s:str):
        if "1" in s:
            s=s.replace("1","0")
            return s
        elif "2" in s:
            s=s.replace("2","1")
            return s
        elif "3" in s:
            s=s.replace("3","2")
            return s
        elif "4" in s:
            s=s.replace("4","3")
            return s
        elif "5" in s:
            s=s.replace("5","4")
            return s
        elif "6" in s:
            s=s.replace("6","5")
            return s
        elif "1" in s:
            s=s.replace("1","")
            return s
        elif "7" in s:
            s=s.replace("7","6")
            return s
        elif "8" in s:
            s=s.replace("8","7")
            return s
        elif "9" in s:
            s=s.replace("9","8")
            return s
        else:
            return s
        

    def connect(self):
        print("websocket connected...")
        self.match_id = self.scope['url_route']['kwargs']['match_id']
        
        print(self.match_id)
        self.accept()  
    def receive_json(self,content,**kwargs):
        print("HEYYYYY")
        change_innings=0
        match_completed = 0
        print("message received from client..",content)
        current_data = innings.objects.all().filter(match_id=self.match_id)[0]
        max_overs = match_info.objects.all().filter(match_id = self.match_id)[0].maximum_overs
        
        
        if content['start']==1:
            current_data.save()
            bat1_name = player_match_stats.objects.all().filter(match_id = self.match_id,username=current_data.player1_username)[0].player_name
            bat2_name = player_match_stats.objects.all().filter(match_id = self.match_id,username=current_data.player2_username)[0].player_name
            bowler_name = player_match_stats.objects.all().filter(match_id = self.match_id,username=current_data.bowler_username)[0].player_name
            print(current_data.player1_username,current_data.player2_username)
            self.send_json({
                'score':0,
                'current_score':current_data.runs_scored,
                'bowling_team':current_data.bowling_team,
                'bating_team':current_data.batting_team,
                'player1_username':current_data.player1_username,
                'player2_username':current_data.player2_username,
                'bowler_username':current_data.bowler_username,
                'wickets':current_data.wickets,
                'current_overs':current_data.balls_bowled//6,
                'balls':current_data.balls_bowled%6,
                'overs_bowler_bowled':current_data.balls_bowler_bowled//6,
                'balls_bowler_bowled' : current_data.balls_bowler_bowled%6,
                'runs_conceded':current_data.runs_conceded,
                'wickets_conceded':current_data.wickets_conceded,
                'balls_consumed_b1':current_data.balls_consumed_b1,
                'score_b1':current_data.score_b1,
                'score_b2':current_data.score_b2,
                'balls_consumed_b2':current_data.balls_consumed_b2,
                'strike':current_data.strike,
                'bat1_name':bat1_name,
                'bat2_name':bat2_name,
                'bowler_name':bowler_name
                } )
        else:
            
            if content['change_strike']==1:
                c=0
                if current_data.strike==1:
                    c=2
                   
                else:
                    current_data.strike=1
                    c=1
                current_data.strike=c
                current_data.save()
            if content['bat2_change']==1:
                player_data = player_match_stats.objects.all().filter(match_id=self.match_id,username=content['old_bat'])[0]
                player_data.bowls_faced = current_data.balls_consumed_b2
                player_data.runs_scored = current_data.score_b2
                player_data.fours = current_data.fours_b2
                player_data.sixes = current_data.sixes_b2
                if current_data.balls_consumed_b2>0:
                    player_data.strike_rate = (current_data.score_b2*100)/current_data.balls_consumed_b2
                else:
                    player_data.strike_rate=0
                player_data.save()
                player_data = player_match_stats.objects.all().filter(match_id=self.match_id,username=content['new_bat'])[0]
                current_data.balls_consumed_b2 = player_data.bowls_faced
                current_data.score_b2= player_data.runs_scored
                current_data.player2_username=content['new_bat']
                current_data.fours_b2 = player_data.fours
                current_data.sixes_b2 =player_data.sixes
                print(content['old_bat'])
                current_data.save()
            elif content['bat1_change']==1:
                player_data = player_match_stats.objects.all().filter(match_id=self.match_id,username=content['old_bat'])[0]
                player_data.bowls_faced = current_data.balls_consumed_b1
                player_data.runs_scored = current_data.score_b1
                player_data.fours = current_data.fours_b1
                player_data.sixes = current_data.sixes_b1
                if current_data.balls_consumed_b1>0:
                    player_data.strike_rate = (current_data.score_b1*100)/current_data.balls_consumed_b1
                else:
                    player_data.strike_rate=0
                player_data.save()
                player_data = player_match_stats.objects.all().filter(match_id=self.match_id,username=content['new_bat'])[0]
                current_data.score_b1=player_data.bowls_faced
                current_data.player1_username=content['new_bat']
                current_data.balls_consumed_b1=0
                current_data.fours_b1 = 0
                current_data.sixes_b1 =0
                print(content['old_bat'])
                current_data.save()
            elif content['bowl_change']==1:
                player_data = player_match_stats.objects.all().filter(match_id=self.match_id,username=content['old_bowl'])[0]
                player_data.bowls_bowled = current_data.balls_bowler_bowled
                player_data.runs_conceded = current_data.runs_conceded
                player_data.wickets = current_data.wickets_conceded
                if player_data.bowls_bowled>0:  
                    player_data.economy = current_data.runs_conceded//(player_data.bowls_bowled//6)
                else:
                    player_data.economy=0
                player_data.save()
                player_data = player_match_stats.objects.all().filter(match_id=self.match_id,username=content['new_bowl'])[0]
                current_data.balls_bowler_bowled = player_data.bowls_bowled
                current_data.runs_conceded = player_data.runs_conceded
                current_data.wickets_conceded = player_data.wickets
                current_data.bowler_username = content['new_bowl']
                print(content['new_bowl'])
                current_data.save()    
            score = int(content['score'])
            prev_score=0
            if int(content['score'])==1 or int(content['score'])==3 or int(content['extra'])==1 or int(content['extra'])==3 :
                
                c=0
                if current_data.strike==1:
                    c=2
                   
                else:
                    current_data.strike=1
                    c=1
                current_data.strike=c
                current_data.save()
                
            print("curent strike =",current_data.strike)
            
            current_data.runs_scored =max(0,current_data.runs_scored+score)
            current_data.balls_bowler_bowled = max(0,current_data.balls_bowler_bowled + int(content['add_ball']))
            current_data.balls_bowled = max(0,current_data.balls_bowled+int(content['add_ball']))
            current_data.runs_conceded = max(0,current_data.runs_conceded+int(content['score']))
            if current_data.player1_username == content['current_strike']:
                current_data.balls_consumed_b1 = max(0,current_data.balls_consumed_b1 + int(content['add_ball']))
                current_data.score_b1 = max(0,current_data.score_b1+int(content['score']))
                if int(content['score'])==4:
                    current_data.fours_b1=current_data.fours_b1+1
                elif int(content['score'])==6:
                    current_data.sixes_b1=current_data.sixes_b1+1
                print("hello1")
            else :
                current_data.balls_consumed_b2 = max(0,current_data.balls_consumed_b2 + int(content['add_ball']))
                current_data.score_b2 = max(0,current_data.score_b2+int(content['score']))
                if int(content['score'])==4:
                    current_data.fours_b2=current_data.fours_b2+1
                elif int(content['score'])==6:
                    current_data.sixes_b2=current_data.sixes_b2+1
                print("hello2")
            if content['run_out_b1']==1 or content['run_out_b2']==1 :
                
                current_data.runs_scored = current_data.runs_scored+int(content['extra'])
                current_data.wickets=current_data.wickets+1
                current_data.wickets_conceded = current_data.wickets_conceded+1
                current_data.runs_conceded = current_data.runs_conceded+int(content['extra'])
                if current_data.player1_username == content['current_strike']:
                    current_data.score_b1 = current_data.score_b1+int(content['extra'])
                    print("hello1")
                else :
                    current_data.score_b2 = current_data.score_b2+int(content['extra'])
                    print("hello2")
            if content['noball']==1:
                current_data.runs_scored = current_data.runs_scored+1
                current_data.runs_conceded = current_data.runs_conceded+1
                if current_data.player1_username == content['current_strike']:
                    current_data.score_b1 = current_data.score_b1+1
                    print("hello1")
                else :
                    current_data.score_b2 = current_data.score_b2+1
                current_data.save() 
            if content['wide_ball']==1:
                current_data.runs_scored = current_data.runs_scored+int(content['extra'])+1
                current_data.runs_conceded = current_data.runs_conceded+int(content['extra'])+1
                current_data.save()  
            if content['byes']==1:
                current_data.runs_scored = current_data.runs_scored+int(content['extra'])
                #current_data.runs_conceded = current_data.runs_conceded+int(content['extra'])
                current_data.save() 

            current_data.wickets=max(0,current_data.wickets+content['wickets'])
            current_data.wickets_conceded = max(0,current_data.wickets_conceded+content['wickets'])
            current_data.save()
            if current_data.balls_bowled>0 and current_data.balls_bowled%6==0 and int(content['add_ball']==1):
                c=0
                if current_data.strike==1:
                    c=2
                   
                else:
                    current_data.strike=1
                    c=1
                current_data.strike=c
                current_data.save()

            if (current_data.balls_bowled==(max_overs*6) or current_data.wickets==(min(match_info.objects.all().filter(match_id=self.match_id)[0].no_players,11)-1)) and current_data.innings_no==1:
                print("INNINGS IS CHANGED")
                change_innings=1
                player_data = player_match_stats.objects.all().filter(match_id=self.match_id,username=current_data.player1_username)[0]
                player_data.bowls_faced = current_data.balls_consumed_b1
                player_data.runs_scored = current_data.score_b1
                player_data.fours = current_data.fours_b1
                player_data.sixes = current_data.sixes_b1
                match_first = match_info.objects.all().filter(match_id = self.match_id)[0]
                match_first.innings1_score = current_data.runs_scored
                match_first.innings1_wickets = current_data.wickets
                match_first.innings1_overs = current_data.balls_bowled
                match_first.save()
                if current_data.balls_consumed_b1>0:
                    player_data.strike_rate = (current_data.score_b1*100)/current_data.balls_consumed_b1
                else:
                    player_data.strike_rate=0
                player_data.save()
                player_data = player_match_stats.objects.all().filter(match_id=self.match_id,username=current_data.player2_username)[0]
                player_data.bowls_faced = current_data.balls_consumed_b2
                player_data.runs_scored = current_data.score_b2
                player_data.fours = current_data.fours_b2
                player_data.sixes = current_data.sixes_b2
                if current_data.balls_consumed_b2>0:
                    player_data.strike_rate = (current_data.score_b2*100)/current_data.balls_consumed_b2
                else:
                    player_data.strike_rate=0
                player_data.save()
                player_data = player_match_stats.objects.all().filter(match_id=self.match_id,username=current_data.bowler_username)[0]
                player_data.bowls_bowled = current_data.balls_bowler_bowled
                player_data.runs_conceded = current_data.runs_conceded
                player_data.wickets = current_data.wickets_conceded
                player_data.save()
                if current_data.balls_bowler_bowled >0:  
                    player_data.economy = (current_data.runs_conceded*6)/(current_data.balls_bowler_bowled)
                else:
                    player_data.economy=0
                player_data.save()
                current_data.balls_consumed_b1=0
                current_data.balls_consumed_b2=0
                current_data.balls_bowler_bowled=0
                current_data.wickets_conceded=0
                current_data.runs_conceded=0
                current_data.balls_bowled=0
                current_data.wickets = 0
                current_data.fours_b1=0
                current_data.fours_b2=0
                current_data.sixes_b1=0
                current_data.sixes_b2=0
                current_data.target = current_data.runs_scored+1
                current_data.runs_scored=0
                temp=current_data.batting_team
                current_data.batting_team=current_data.bowling_team 
                current_data.bowling_team = temp
                current_data.innings_no=2
                current_data.strike=1
                current_data.score_b1=0
                current_data.score_b2=0
                current_data.player1_username = ""
                current_data.player2_username = ""
                current_data.bowler_username = ""
                current_data.save()
                

            if current_data.innings_no==2 and (current_data.runs_scored >= current_data.target or current_data.balls_bowled== max_overs*6 or current_data.wickets==(min(match_info.objects.all().filter(match_id=self.match_id)[0].no_players,11)-1)):
                match_completed = 1
                player_data = player_match_stats.objects.all().filter(match_id=self.match_id,username=current_data.player1_username)[0]
                player_data.bowls_faced = current_data.balls_consumed_b1
                player_data.runs_scored = current_data.score_b1
                player_data.fours = current_data.fours_b1
                player_data.sixes = current_data.sixes_b1
                if current_data.balls_consumed_b1>0:
                    player_data.strike_rate = (current_data.score_b1*100)/current_data.balls_consumed_b1
                else:
                    player_data.strike_rate=0
                player_data.save()
                player_data = player_match_stats.objects.all().filter(match_id=self.match_id,username=current_data.player2_username)[0]
                player_data.bowls_faced = current_data.balls_consumed_b2
                player_data.runs_scored = current_data.score_b2
                player_data.fours = current_data.fours_b2
                player_data.sixes = current_data.sixes_b2
                if current_data.balls_consumed_b2>0:
                    player_data.strike_rate = (current_data.score_b2*100)/current_data.balls_consumed_b2
                else:
                    player_data.strike_rate=0
                player_data.save()
                player_data = player_match_stats.objects.all().filter(match_id=self.match_id,username=current_data.bowler_username)[0]
                player_data.bowls_bowled = current_data.balls_bowler_bowled
                player_data.runs_conceded = current_data.runs_conceded
                player_data.wickets = current_data.wickets_conceded
                player_data.save()
                if current_data.balls_bowler_bowled>0:  
                    player_data.economy = (current_data.runs_conceded*6)/(current_data.balls_bowler_bowled)
                else:
                    player_data.economy=0
                player_data.save()
                players = player_match_stats.objects.all().filter(match_id = self.match_id)
                for player in players:
                    old_data = player_stats.objects.all().filter(username=player.username)[0]
                    previous = old_data.batting_innings
                    old_data.matches_played = old_data.matches_played+1
                    if player.bowls_faced >0:
                        old_data.batting_innings=old_data.batting_innings+1
                        old_data.batting_average=(old_data.batting_average*previous+player.runs_scored)/(previous+1)
                    old_data.bowls_faced = old_data.bowls_faced+player.bowls_faced
                    old_data.runs_scored = old_data.runs_scored+player.runs_scored
                    old_data.fours = old_data.fours+player.fours
                    old_data.sixes = old_data.sixes+player.sixes
                    if player.runs_scored>=50 and player.runs_scored<100:
                        old_data.half_centuries = old_data.half_centuries+1
                    elif player.runs_scored>=100:
                        old_data.centuries = old_data.centuries+1
                    if old_data.highest_score < player.runs_scored:
                        old_data.highest_score = player.runs_scored
                    previous = old_data.wickets_taken
                    if player.bowls_bowled >0:
                        old_data.bowling_innings=old_data.bowling_innings+1
                        if previous+player.wickets>0:
                            old_data.bowling_average = (old_data.bowling_average*previous+player.runs_conceded)/(previous+player.wickets)
                    old_data.wickets_taken = old_data.wickets_taken+player.wickets
                    old_data.strike_rate = player.strike_rate
                    old_data.economy = (old_data.economy*previous+player.economy)/(previous+1)
                    print("Match completed")
                    old_data.save()
                mat = match_info.objects.all().filter(match_id = self.match_id)[0]
                mat.status = 3
                mat.innings2_score = current_data.runs_scored
                mat.innings2_wickets = current_data.wickets
                mat.innings2_overs = current_data.balls_bowled
                if(mat.innings1_score>mat.innings2_score):
                    mat.match_winner = mat.first_batting
                elif(mat.innings1_score<mat.innings2_score):
                    mat.match_winner = mat.first_bowling
                else:
                    mat.match_winner = "MATCH TIE"
                mat.save()
                    
            
            current_data.save()
            if change_innings==0:
                bat1_name = player_match_stats.objects.all().filter(match_id = self.match_id,username=current_data.player1_username)[0].player_name
                bat2_name = player_match_stats.objects.all().filter(match_id = self.match_id,username=current_data.player2_username)[0].player_name
                bowler_name = player_match_stats.objects.all().filter(match_id = self.match_id,username=current_data.bowler_username)[0].player_name
                over_line = overs_timeline.objects.all().filter(match_id=self.match_id)[0]
                if over_line.ball==0:
                    over_line.ball1 = ""
                    over_line.ball2 = ""
                    over_line.ball3 = ""
                    over_line.ball4 = ""
                    over_line.ball5 = ""
                    over_line.ball6 = ""
                    over_line.save()
                match over_line.ball:
                    case 0:
                        if content['noball']==1:
                            over_line.ball1 = over_line.ball1+str(content['extra'])+"NB"
                        elif content['wide_ball']==1:
                            over_line.first = over_line.ball1+str(content['extra'])+" WB"
                        elif content['byes']==1:
                            over_line.ball1 = over_line.ball1+str(content['extra'])+"LB "
                        elif content['run_out_b1']==1 or content['run_out_b2']==1 or content['wickets']==1:
                            over_line.ball1 = over_line.ball1+" W"
                        elif content['wickets']==-1:
                            over_line.ball1 = over_line.ball2.replace("W","0")
                        elif int(content['add_ball'])>=0 and int(content['score'])>=0:
                                over_line.ball1 = over_line.ball1+" "+str(int(content['score']))
                                if int(content['add_ball'])==0 and int(content['score'])==0:
                                    over_line.ball1 = ""

                            
                    case 1:
                        if content['noball']==1:
                            over_line.ball2 = over_line.ball2+str(content['extra'])+"NB"
                        elif content['wide_ball']==1:
                            over_line.ball2 = over_line.ball2+str(content['extra'])+" WB"
                        elif content['byes']==1:
                            over_line.ball2 = over_line.ball2+str(content['extra'])+"LB "
                        elif content['run_out_b1']==1 or content['run_out_b2']==1 or content['wickets']==1:
                            over_line.ball2 = over_line.ball2+" W"
                        elif content['wickets']==-1:
                            over_line.ball1 = over_line.ball2.replace("W","0")
                        elif int(content['add_ball'])>=0 and int(content['score'])>=0:
                            over_line.ball2 = over_line.ball2+" "+str(int(content['score']))
                            if int(content['add_ball'])==0 and int(content['score'])==0:
                                over_line.ball2 = ""
                        elif int(content['score'])<0:
                            st=over_line.ball1
                            over_line.ball1 = self.change_ball(st)


                    case 2:
                        if content['noball']==1:
                            over_line.ball3 = over_line.ball3+str(content['extra'])+"NB"
                        elif content['wide_ball']==1:
                            over_line.ball3 = over_line.ball3+str(content['extra'])+" WB"
                        elif content['byes']==1:
                            over_line.ball3 = over_line.ball3+str(content['extra'])+"LB "
                        elif content['run_out_b1']==1 or content['run_out_b2']==1 or content['wickets']==1:
                            over_line.ball3 = over_line.ball3+" W"
                        elif content['wickets']==-1:
                            over_line.ball2 = over_line.ball3.replace("W","0")
                        elif int(content['add_ball'])>=0 and int(content['score'])>=0:
                            over_line.ball3 = over_line.ball3+" "+str(int(content['score']))
                            if int(content['add_ball'])==0 and int(content['score'])==0:
                                over_line.ball3 = ""
                        elif int(content['score'])<0:
                            st=over_line.ball2
                            over_line.ball2 = self.change_ball(st)
                        
                    case 3:
                        if content['noball']==1:
                            over_line.ball4 = over_line.ball4+str(content['extra'])+"NB"
                        elif content['wide_ball']==1:
                            over_line.ball4 = over_line.ball4+str(content['extra'])+" WB"
                        elif content['byes']==1:
                            over_line.ball4 = over_line.ball4+str(content['extra'])+"LB "
                        elif content['run_out_b1']==1 or content['run_out_b2']==1 or content['wickets']==1:
                            over_line.ball4 = over_line.ball4+" W"
                        elif content['wickets']==-1:
                            over_line.ball3 = over_line.ball3.replace("W","0")
                        elif int(content['add_ball'])>=0 and int(content['score'])>=0:
                            over_line.ball4 = over_line.ball4+" "+str(int(content['score']))
                            if int(content['add_ball'])==0 and int(content['score'])==0:
                                over_line.ball4 = ""
                        elif int(content['score'])<0:
                            st=over_line.ball3
                            over_line.ball3 = self.change_ball(st)
                    case 4:
                        if content['noball']==1:
                            over_line.ball5 = over_line.ball5+str(content['extra'])+"NB"
                        elif content['wide_ball']==1:
                            over_line.ball5 = over_line.ball5+str(content['extra'])+" WB"
                        elif content['byes']==1:
                            over_line.ball5 = over_line.ball5+str(content['extra'])+"LB "
                        elif content['run_out_b1']==1 or content['run_out_b2']==1 or content['wickets']==1:
                            over_line.ball5 = over_line.ball5+" W"
                        elif content['wickets']==-1:
                            over_line.ball4 = over_line.ball4.replace("W","0")
                        elif int(content['add_ball'])>=0 and int(content['score'])>=0:
                            over_line.ball5 = over_line.ball5+" "+str(int(content['score']))
                            if int(content['add_ball'])==0 and int(content['score'])==0:
                                over_line.ball5 = ""
                        elif int(content['score'])<0:
                            st=over_line.ball4
                            over_line.ball4 = self.change_ball(st)
                    case 5:
                        if content['noball']==1:
                            over_line.ball6 = over_line.ball6+str(content['extra'])+"NB"
                        elif content['wide_ball']==1:
                            over_line.ball6 = over_line.ball6+str(content['extra'])+" WB"
                        elif content['byes']==1:
                            over_line.ball6 = over_line.ball6+str(content['extra'])+"LB "
                        elif content['run_out_b1']==1 or content['run_out_b2']==1 or content['wickets']==1:
                            over_line.ball6 = over_line.ball6+" W"
                        elif content['wickets']==-1:
                            over_line.ball5 = over_line.ball5.replace("W","0")
                        elif int(content['add_ball'])>=0 and int(content['score'])>=0:
                            over_line.ball6 = over_line.ball6+" "+str(int(content['score']))
                            if int(content['add_ball'])==0 and int(content['score'])==0:
                                over_line.ball6 = ""

                        elif int(content['score'])<0:
                            st=over_line.ball5
                            over_line.ball5 = self.change_ball(st)
                
                if int(content['add_ball'])>=0:
                    over_line.ball = (over_line.ball+int(content['add_ball']))%6
                else:
                    match over_line.ball:
                        case 1:
                            over_line.ball1=""
                        case 2:
                            over_line.ball2=""
                        case 3:
                            over_line.ball3=""
                        case 4:
                            over_line.ball4=""
                        case 5:
                            over_line.ball5=""
                    over_line.ball = max(over_line.ball-1,0)
                over_line.save()
            else:
                bat1_name = ""
                bat2_name = ""
                bowler_name=""
                over_line = overs_timeline.objects.all().filter(match_id=self.match_id)[0]
                over_line.ball=0
                over_line.ball1 = ""
                over_line.ball2 = ""
                over_line.ball3 = ""
                over_line.ball4 = ""
                over_line.ball5 = ""
                over_line.ball6 = ""
                over_line.save()
            
            self.send_json({
                'score':score,
                'current_score':current_data.runs_scored,
                'bowling_team':current_data.bowling_team,
                'bating_team':current_data.batting_team,
                'player1_username': current_data.player1_username,
                'player2_username':current_data.player2_username,
                'bowler_username':current_data.bowler_username,
                'wickets':current_data.wickets,
                'current_overs': current_data.balls_bowled//6,
                'balls':current_data.balls_bowled%6,
                'overs_bowler_bowled':current_data.balls_bowler_bowled//6,
                'balls_bowler_bowled' : current_data.balls_bowler_bowled%6,
                'runs_conceded':current_data.runs_conceded,
                'wickets_conceded':current_data.wickets_conceded,
                'balls_consumed_b1':current_data.balls_consumed_b1,
                'score_b1':current_data.score_b1,
                'score_b2':current_data.score_b2,
                'balls_consumed_b2':current_data.balls_consumed_b2,
                'change_innings':change_innings,
                'strike':current_data.strike,
                'bat1_name':bat1_name,
                'bat2_name':bat2_name,
                'bowler_name':bowler_name,
                'match_completed':match_completed
                } )
            if match_completed ==1:
                self.close()
                print("match is ended")
            if content['end_match']==1:
                mat = match_info.objects.all().filter(match_id = self.match_id)[0]
                mat.status = 4
                mat.save()

class MatchView(WebsocketConsumer):
    def connect(self):
        self.match_id = self.scope["url_route"]["kwargs"]["match_id"]
        self.accept()
    def send_match_data(self):
        match = match_info.objects.get(match_id=self.match_id)  # fetch match data from model
        innings1 = innings.objects.get(match_id=self.match_id)
        batter1_name = player_match_stats.objects.get(match_id = self.match_id,username=innings1.player1_username)
        batter2_name = player_match_stats.objects.get(match_id = self.match_id,username=innings1.player2_username)
        bowler_name = player_match_stats.objects.get(match_id = self.match_id,username=innings1.bowler_username)
        overs = overs_timeline.objects.get(match_id=self.match_id)
        team1_players = player_match_stats.objects.filter(team_name=match.team1,match_id=self.match_id)
        team1_list = []
        for obj in team1_players:
            player_dict = {
                'name': obj.player_name,
                'runs': obj.runs_scored,
                'balls': obj.bowls_faced,
                'fours': obj.fours,
                'sixes': obj.sixes,
                'strike_rate': obj.strike_rate,
                'overs': obj.bowls_bowled,
                'bowler_runs': obj.runs_conceded,
                'wickets': obj.wickets,
                'economy': obj.economy
            }
            team1_list.append(player_dict)
        team2_players = player_match_stats.objects.filter(team_name=match.team2,match_id=self.match_id)
        team2_list = []
        for obj in team2_players:
            player_dict = {
                'name': obj.player_name,
                'runs': obj.runs_scored,
                'balls': obj.bowls_faced,
                'fours': obj.fours,
                'sixes': obj.sixes,
                'strike_rate': obj.strike_rate,
                'overs': obj.bowls_bowled,
                'bowler_runs': obj.runs_conceded,
                'wickets': obj.wickets,
                'economy': obj.economy
            }
            team2_list.append(player_dict)
        data = {
            'team1': match.team1,
            'team2': match.team2,
            'first_batting': match.first_batting,
            'toss_winner': match.toss_winner,
            'maximum_overs': match.maximum_overs,
            'match_status': match.status,
            'innings_no': innings1.innings_no,
            'innings1_score_num': innings1.runs_scored,
            'innings1_overs_num': match.innings1_overs,
            'innings2_overs_num': match.innings2_overs,
            'innings1_score': "Score: " + str(match.innings1_score) + "/" + str(match.innings1_wickets) + " (" + str(str(int(match.innings1_overs/6)) + "." + str(match.innings1_overs%6)) + ")",
            'innings2_score': "Score: " + str(match.innings2_score) + "/" + str(match.innings2_wickets) + " (" + str(str(int(match.innings2_overs/6)) + "." + str(match.innings2_overs%6)) + ")",
            'score': innings1.runs_scored,
            'batter1_name': batter1_name.player_name,
            'batter2_name': batter2_name.player_name,
            'bowler_name': bowler_name.player_name,
            'wickets': innings1.wickets,
            'overs': innings1.balls_bowled,
            'target': innings1.target,
            'batter1_score': innings1.score_b1,
            'batter1_balls': innings1.balls_consumed_b1,
            'batter2_score': innings1.score_b2,
            'batter2_balls': innings1.balls_consumed_b2,
            'bowler_runs': innings1.runs_conceded,
            'bowler_wickets': innings1.wickets_conceded,
            'bowler_balls': innings1.balls_bowler_bowled,
            'overs_timeline': [
                str(overs.ball1).strip(),
                str(overs.ball2).strip(),
                str(overs.ball3).strip(),
                str(overs.ball4).strip(),
                str(overs.ball5).strip(),
                str(overs.ball6).strip(),
            ],
            'team1_players': team1_list,
            'team2_players': team2_list,
            'strike': innings1.strike,
            # add more fields as needed
        }
        #serialized_data = json.dumps(data)
        # serialized_data = serializers.serialize('json', data)
        self.send(text_data=json.dumps(data))  # send data to HTML page

    def receive(self, text_data):
        # call send_match_data when the HTML page is loaded
        self.send_match_data()
