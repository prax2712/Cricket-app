from django.db import models
from datetime import time


class match_info(models.Model):
    match_id = models.AutoField(primary_key = True)
    no_players=models.IntegerField(db_default=5)
    host = models.CharField(max_length=255,db_default="admin")
    venue = models.CharField(max_length=255)
    match_date = models.DateField(null=False)
    match_time = models.TimeField(db_default=time(hour = 0,minute = 0))
    maximum_overs = models.IntegerField()
    team1 = models.CharField(max_length = 225)
    team2 = models.CharField(max_length = 225)
    innings1_score = models.IntegerField(db_default=0)
    innings2_score = models.IntegerField(db_default=0)
    innings1_overs = models.IntegerField(db_default=0)
    innings2_overs = models.IntegerField(db_default=0)
    innings1_wickets = models.IntegerField(db_default=0)
    innings2_wickets = models.IntegerField(db_default=0)
    first_batting = models.CharField(max_length = 225)
    first_bowling = models.CharField(max_length = 225)
    toss_winner = models.CharField(max_length = 225)
    match_winner = models.CharField(max_length = 225)
    status = models.IntegerField(db_default=0)


class innings(models.Model):
    match_id = models.IntegerField()
    innings_no = models.IntegerField(db_default = 1)
    batting_team = models.CharField(max_length = 100)
    bowling_team = models.CharField(max_length = 100)
    player1_username = models.CharField(max_length =100) 
    balls_consumed_b1 = models.IntegerField(db_default =0)
    balls_consumed_b2 = models.IntegerField(db_default =0)
    score_b1 = models.IntegerField(db_default =0)
    score_b2 = models.IntegerField(db_default =0)
    player2_username = models.CharField(max_length =100) 
    strike = models.IntegerField(db_default = 1)
    fours_b1 = models.IntegerField(db_default=0)
    fours_b2 = models.IntegerField(db_default=0)
    sixes_b1 = models.IntegerField(db_default=0)
    sixes_b2 = models.IntegerField(db_default=0)
    runs_scored = models.IntegerField(db_default = 0)
    wickets = models.IntegerField(db_default = 0)
    balls_bowled = models.IntegerField(db_default =0)#batting team balls consumed
    bowler_username = models.CharField(max_length=50)
    balls_bowler_bowled = models.IntegerField(db_default=0)
    wickets_conceded = models.IntegerField(db_default=0)
    runs_conceded = models.IntegerField(db_default=0)
    target = models.IntegerField(db_default = 0)


class player_match_stats(models.Model):
    match_id = models.IntegerField()
    username = models.CharField(max_length = 250)
    player_name = models.CharField(max_length = 250)
    team_name = models.CharField(max_length = 200)
    bowls_faced = models.IntegerField(db_default = 0)
    runs_scored = models.IntegerField(db_default = 0)
    strike_rate = models.FloatField(db_default = 0)
    fours = models.IntegerField(db_default = 0)
    sixes = models.IntegerField(db_default = 0)
    bowls_bowled = models.IntegerField(db_default = 0)
    runs_conceded = models.IntegerField(db_default = 0)
    wickets = models.IntegerField(db_default = 0)
    economy = models.FloatField(db_default = 0.0)


class player_stats(models.Model):
    username = models.CharField(max_length = 250)
    password = models.CharField(max_length = 250)
    first_name = models.CharField(max_length = 250)
    last_name = models.CharField(max_length = 250)
    batting_style=models.CharField(max_length = 50)
    bowling_style = models.CharField(max_length = 50)
    matches_played = models.IntegerField(db_default = 0)
    batting_innings = models.IntegerField(db_default = 0)
    bowls_faced = models.IntegerField(db_default = 0)
    runs_scored = models.IntegerField(db_default = 0)
    batting_average = models.FloatField(db_default = 0.0)
    fours = models.IntegerField(db_default = 0)
    sixes = models.IntegerField(db_default = 0)
    half_centuries = models.IntegerField(db_default = 0)
    centuries = models.IntegerField(db_default = 0)
    strike_rate = models.FloatField(db_default = 0)
    highest_score = models.IntegerField(db_default = 0)
    bowling_innings = models.IntegerField(db_default = 0)
    bowls_bowled = models.IntegerField(db_default = 0)
    bowling_average = models.FloatField(db_default = 0)
    wickets_taken = models.IntegerField(db_default = 0)
    economy = models.FloatField(db_default = 0)

    
class overs_timeline(models.Model):
    match_id = models.IntegerField()
    ball = models.IntegerField(db_default = 0)
    ball1 = models.CharField(max_length = 250,db_default = "")
    ball2 = models.CharField(max_length = 250,db_default = "")
    ball3 = models.CharField(max_length = 250,db_default = "")
    ball4 = models.CharField(max_length = 250,db_default = "")
    ball5 = models.CharField(max_length = 250,db_default = "")
    ball6 = models.CharField(max_length = 250,db_default = "")









    
