let flag=0;
let current_strike ;
let current_wicket = 0;
let run_out_b1 = 0;
let run_out_b2 = 0;
let wide_ball = 0;
let extra = 0;
let byes = 0 ;
let over_throw = 0;
let noball = 0;
let batsman1;
let batsman2 ;
let bowler_username ;
let score = 0;
let add_ball = 0;
let bat1_change = 0;
let bat2_change = 0;
let old_bat ="";
let new_bat = "";
let bowl_change = 0;
let old_bowl = "";
let new_bowl = "";
let ch_strike = 0;
let end_match = 0;

//To implement floating keypad
console.log("JAN");
const zero = document.getElementsByClassName("zero-float");
for(let element of zero)
{

  element.addEventListener("click",()=>{
    document.getElementById("layer").style.display="block";
    document.getElementById("zero-float").style.visibility="visible";
  
  })

}
const one = document.getElementsByClassName("one-float");
for(let element of one)
{
  
  element.addEventListener("click",()=>{
  
    document.getElementById("layer").style.display="block";
    document.getElementById("one-float").style.visibility="visible";
    
  })

}
const entry_zero = document.getElementsByClassName("flat-adder");
for(const element of entry_zero)
{
  
  element.addEventListener("click",()=>{
    document.getElementById("zero-float").style.visibility="hidden";
    document.getElementById("layer").style.display="none";
    document.getElementById("one-float").style.visibility="hidden";
  })
}
console.log(document.getElementById("batsman-1").value+"hello sir");
console.log(document.getElementById("batsman-2").value+"hello sir");

const match_id = JSON.parse(document.getElementById("match-id").textContent);
const team_1 = JSON.parse(document.getElementById("team1").textContent);
const team_2 = JSON.parse(document.getElementById("team2").textContent)
document.title = team_1 + " vs " + team_2;
//web socket connection

ws = new WebSocket('ws://127.0.0.1:8000/liveHost/'+match_id+'/');


let old_batsman_score;
let old_batsman_username;
let old_bowler_score;
let old_bowler_wickets;

//creating sending function

const send_message = function(start){
  ws.send(JSON.stringify({
    'start':0,
    'score':score,
    'current_strike':current_strike,
    'wickets':current_wicket,
    'run_out_b1':run_out_b1,
    'run_out_b2':run_out_b2,
    'wide_ball':wide_ball,
    'extra':extra,
    'byes':byes,
    'over_throw':over_throw,
    'noball':noball,
    'batsman1':batsman1,
    'batsman2':batsman2,
    'bowler_username':bowler_username,
    'add_ball':add_ball ,
    'bat1_change':bat1_change,
    'bat2_change':bat2_change,
    'bowl_change':bowl_change,
    'new_bat':new_bat,
    'old_bat':old_bat,
    'new_bowl':new_bowl,
    'old_bowl':old_bowl,
    'change_strike':ch_strike,
    'end_match':end_match

  }))

}

// change the batsman-1 name on selecting new batsman

document.getElementById("selecting-batsman-1").onchange = function(){
  let new_batsman_name=document.getElementById("selecting-batsman-1").options[document.getElementById("selecting-batsman-1").selectedIndex].textContent;
  let new_batsman = document.getElementById("selecting-batsman-1").options[document.getElementById("selecting-batsman-1").selectedIndex].value;
  old_batsman_username = document.getElementById("batsman-1").dataset.value;
  bat1_change =1;
  old_bat = old_batsman_username;
  new_bat = new_batsman;
  
  if(current_strike==old_bat){
    current_strike=new_bat;
  }
  send_message(0);
  console.log(bat1_change,bat2_change,bowl_change,old_bat,new_bat);
  document.getElementById("batsman-1").textContent = new_batsman_name;
  document.getElementById("batsman-1").dataset.value = new_batsman;
  document.querySelector("#batsman1-score").value=0; 
  document.getElementById("batsman1-score").textContent=0; 
}

//cahnging batsman-2 name on selecting new batsman

document.getElementById("selecting-batsman-2").onchange = function(){
  let new_batsman_name=document.getElementById("selecting-batsman-2").options[document.getElementById("selecting-batsman-2").selectedIndex].textContent;
  let new_batsman = document.getElementById("selecting-batsman-2").options[document.getElementById("selecting-batsman-2").selectedIndex].value;
 // old_batsman_score = document.getElementById("batsman2-score").textContent ;
  old_batsman_username = document.getElementById("batsman-2").dataset.value
  bat2_change=1;
  old_bat = old_batsman_username;
  new_bat = new_batsman;
  if(current_strike==old_bat){
    current_strike=new_bat;
  }
  send_message(0);
  console.log(bat1_change,bat2_change,bowl_change,old_bat,new_bat);
  document.getElementById("batsman-2").textContent = new_batsman_name;
  document.querySelector("#batsman2-score").value=0; 
  document.getElementById("batsman2-score").textContent=0; 

}

//changing bowler name on selecting new bowler

document.getElementById("selecting-bowler").onchange = function(){
  let new_bowler_name=document.getElementById("selecting-bowler").options[document.getElementById("selecting-bowler").selectedIndex].textContent;
  let new_bowler = document.getElementById("selecting-bowler").options[document.getElementById("selecting-bowler").selectedIndex].value;
  bowl_change = 1;
  old_bowl = document.getElementById("bowler-name").value;
  new_bowl = new_bowler;
  document.getElementById("bowler-name").textContent = new_bowler_name;
  document.getElementById("bowler-name").value = new_bowler;
  document.getElementById("bowler-score").textContent=0; 
  document.getElementById("bowler-wickets").textContent=0;
  
  send_message(0);
  console.log("HEY",bat1_change,bat2_change,bowl_change,old_bowl,new_bowl);
}

//change strike function

const change_strike = function(){
  if(document.getElementById("batsman-1").dataset.value == current_strike)
    {
      
      document.getElementById("batsman-2").style.backgroundColor = "rgba(20,200,200,0.4)";
      document.getElementById("batsman-1").style.backgroundColor ="rgba(49, 64, 64, 0.3)" ;
      current_strike = document.getElementById("batsman-2").dataset.value;
    }
    else{
      document.getElementById("batsman-1").style.backgroundColor = "rgba(20,200,200,0.4)";
      document.getElementById("batsman-2").style.backgroundColor = "rgba(49, 64, 64, 0.3)";
      current_strike = document.getElementById("batsman-1").dataset.value;
    }
    
  }
  document.getElementById("change-strike").onclick = function()
  {
    console.log("HEllo");
    change_strike();
    ch_strike=1;
    send_message(0);
  }
 
//sending intial message to retriev the current data from database

ws.onopen = function(){
    console.log("websocket opened...");
    start=1;
    ws.send(JSON.stringify({
      'start':start,
      'player1':batsman1,
      'player2':batsman2,
      'bowler_username':bowler_username
    }))
}

//handiling decrease runs button

document.getElementById("dec_run_1").onclick = function(){
  score=-1;
  send_message();
}

//handiling decrease ball button

document.getElementById("dec_ball_1").onclick = function(){
  add_ball = -1;
  send_message();
}

//handiling decrease wicket button

document.getElementById("dec_wicket_1").onclick = function(){
  current_wicket=-1;
  send_message()
}
let list = document.querySelectorAll(".add-runs");
console.log(list);

//Handling score addition button

for(let i=0;i<7;i++)
{
    list[i].onclick = function(){
    score = list[i].value;
    add_ball =1;
    send_message();
    if(score=='1'||score=='3'||score=='5'){
      console.log(current_strike+" befor");
      change_strike();
      console.log(current_strike+" after");
      

    }
} }

// Handling end match button

document.getElementById("endmatch").onclick=function(){
  console.log("ENDING")
  end_match=1;
  send_message()
}

//Handling wicket out button

document.getElementById("wicket-out").onclick = function(){
  current_wicket=1;
  add_ball=1;
  send_message(0);
}

//Handling run out batsman-1 button

document.getElementById("run-out-b1").onclick = function()
{
  run_out_b1 = 1;
  add_ball =1;
  for(let element of entry_zero)
    {
     element.onclick = ()=>{
      
      extra = element.innerHTML;
      send_message(0);
     }
    }
}

//Handling run out batsman 2 button

document.getElementById("run-out-b2").onclick = function()
{
  run_out_b2 = 1;
  add_ball =1;
  for(let element of entry_zero)
    {
  
     element.onclick = ()=>{
      
      extra = element.innerHTML;

      send_message(0);
     }
    }
}

//Handling byes button 

document.getElementById("byes").onclick = function()
{
  let fag=1;
  byes=1;
  add_ball=1;
  for(let element of entry_zero)
    {
     element.onclick = ()=>{
      while(fag!=0){
      extra = element.innerHTML;
      send_message(0);
      fag=0;
      }
     }
    }
}

//Handling noball button

document.getElementById("noball").onclick = function()
{
  let fag=1;
  noball = 1;
  console.log("Clicked noball");
  for(let element of entry_zero)
    {
     element.addEventListener("click",()=>{
      while(fag!=0){
      extra = element.textContent;
      score = extra;
      send_message(0);
      fag=0;
      }
     })
    }
}

//Handling wide button

document.getElementById("wide").onclick = function()
{
  let fag=1;
  wide_ball = 1;
  for(let element of entry_zero)
    {
     element.addEventListener("click",()=>{
      while(fag!=0){
      extra = element.innerHTML;
      console.log("HELLO _2");
      send_message(0);
        fag=0;
      }
     })
    }
}

//Handling over throw button

document.getElementById("overthrow").onclick = function()
{
  let fag=1;
  over_throw = 1;
  for(let element of entry_zero)
    {
     element.addEventListener("click",()=>{
      while(fag!=0){
      extra = element.innerHTML;
      score=extra;
      send_message(0);
      fag=0;
      }
     })
    }
}

// Making changes on receiving message


ws.onmessage = function(event){
  start=0;
  add_ball=0;
  score =0;
  run_out_b1 = 0;
  run_out_b2 = 0;
  noball=0;
  over_throw =0;
  wide_ball =0;
  byes=0;
  extra=0;
  current_wicket=0;
  bat1_change = 0;
  bat2_change = 0;
  old_bat ="";
  bowl_change = 0;
  ch_strike=0;
  old_bowl="";
  end_match=0;
  console.log(event.data);
  current_data = JSON.parse(event.data);
  console.log(current_data.current_score);
  document.getElementById("total-score").innerHTML=current_data.current_score;//updating total score of bating team
document.getElementById("bating-team-name").textContent = current_data.bating_team;
document.getElementById("bowling-team-name").textContent = current_data.bowling_team;
document.getElementById("overs-completed").textContent = "Overs  "+current_data.current_overs+"."+current_data.balls;
document.getElementById("bowler-score").textContent = current_data.runs_conceded;
document.getElementById('bowler-wickets').textContent = current_data.wickets_conceded;
document.getElementById('bowler-overs').textContent = 'Overs '+current_data.overs_bowler_bowled+" - "+current_data.balls_bowler_bowled;
document.getElementById("batsman1-balls").textContent = current_data.balls_consumed_b1;
document.getElementById("batsman2-balls").textContent = current_data.balls_consumed_b2;
document.getElementById("batsman1-score").textContent = current_data.score_b1;
document.getElementById("batsman2-score").textContent = current_data.score_b2;
document.getElementById("total-wickets").textContent = current_data.wickets;
if(current_data.current_overs>0 && current_data.balls==0)
  {
    change_strike();
  }
batsman1 = current_data.player1_username;
batsman2 = current_data.player2_username;
document.getElementById("batsman-1").textContent = current_data.bat1_name;
document.getElementById("batsman-1").dataset.value = batsman1;
console.log(document.getElementById("batsman-1").dataset.value,"how");
document.getElementById("batsman-2").textContent = current_data.bat2_name;
document.getElementById("batsman-2").dataset.value = batsman2;
document.getElementById("bowler-name").textContent = current_data.bowler_name;
document.getElementById("bowler-name").value=current_data.bowler_username;
bowler_username = current_data.bowler_username
console.log(batsman1+current_data.player1_username+batsman2+current_data.player2_username)
if(current_data.strike==1)
  {
    current_strike = batsman1;
    document.getElementById("batsman-1").style.backgroundColor = "rgba(20,200,200,0.4)";
    document.getElementById("batsman-2").style.backgroundColor = "rgba(49, 64, 64, 0.3)";

  }
  else{
    current_strike = batsman2;
    document.getElementById("batsman-2").style.backgroundColor = "rgba(20,200,200,0.4)";
    document.getElementById("batsman-1").style.backgroundColor = "rgba(49, 64, 64, 0.3)";
  }
  
if(current_data.change_innings==1)
  {
    window.location.reload();
  }
  let op  = document.getElementById("selecting-bowler").options
for(let i=0;i<op.length;i++)
  {
    if(op[i].value == bowler_username)
      {
        document.getElementById("selecting-bowler").selectedIndex=i;
      }
  }
  op =  document.getElementById("selecting-batsman-1").options;
  for(let i=0;i<op.length;i++)
    {
      if(op[i].value == batsman1)
        {
          document.getElementById("selecting-batsman-1").selectedIndex=i;
        }
    }
  op =  document.getElementById("selecting-batsman-2").options;
  for(let i=0;i<op.length;i++)
    {
      if(op[i].value == batsman2)
        {
          document.getElementById("selecting-batsman-2").selectedIndex=i;
        }
    }
}
console.log("Iam at the end");
