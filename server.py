from datetime import datetime
from logging import error, exception
import os
import json
from flask import Flask,render_template,request,redirect,flash,url_for,session



def loadClubs():
    with open('clubs.json') as c:
         listOfClubs = json.load(c)['clubs']
         return listOfClubs
 

def loadCompetitions():
    with open('competitions.json') as comps:
         listOfCompetitions = json.load(comps)['competitions']
         return listOfCompetitions


app = Flask(__name__)
app.secret_key = 'something_special'

competitions = loadCompetitions()
clubs = loadClubs()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/showSummary',methods=['POST'])
def showSummary():
    clubs1 = [club for club in clubs if club['email'] == request.form['email']]
    print (clubs1)
    competitions1 = [competition for competition in competitions if ((datetime.strptime(competition["date"],  "%Y-%m-%d %H:%M:%S" )>datetime.now()))]
    print(competitions1)
    if clubs1: 
        club = [club for club in clubs if club['email'] == request.form['email']][0]
        return render_template('welcome.html',club=club,competitions=competitions1)
    else:
         error = 'Desole , cet email n a pas ete trouve'
         return render_template ('index.html',error=error)   

@app.route('/tableau' , methods=["GET", "POST"]) 
def tableau():
    competitions1 = [competition for competition in competitions if ((datetime.strptime(competition["date"],  "%Y-%m-%d %H:%M:%S" )>datetime.now()))]
    if competitions1:
        return render_template('tableau.html', competitions=competitions1)
    
            


@app.route('/book/<competition>/<club>')
def book(competition,club):
    try:    
        foundClub = [c for c in clubs if c['name'] == club][0]
        foundCompetition = [c for c in competitions if c['name'] == competition][0]
        return render_template('booking.html', club=foundClub,competition=foundCompetition)
    except:
        flash('Something went wrong please try again')
        return redirect(url_for('index'))    
  


@app.route('/purchasePlaces',methods=['POST'])
def purchasePlaces():
    competition = [c for c in competitions if c['name'] == request.form['competition']][0]
    club = [c for c in clubs if c['name'] == request.form['club']][0]
    placesRequired = int(request.form['places'])
    if placesRequired <= int(competition['numberOfPlaces']) and placesRequired <= 12 and placesRequired *3 <= int(club['points']):

        competition['numberOfPlaces'] = int(competition['numberOfPlaces'])-placesRequired
        club ['points']=int(club['points'])-placesRequired *3
        flash('Great-booking complete!')
        return render_template('welcome.html', club=club, competitions=competitions)
    else:
            if (int(competition['numberOfPlaces']) < placesRequired)  : 

             error = 'desole nous n avons pas assez de places '
             return render_template ('welcome.html',error1=error , club=club, competitions=competitions) 
            else:
                if (placesRequired > 12)    :
                 error =  'desole vous ne pouvez pas reserver au delas de 12 places'
                 return render_template ('welcome.html',error1=error , club=club, competitions=competitions)  
                else:
                   if  (placesRequired*3 > int(club['points']))  :
                    error = 'Desole vous navez pas assez de points  ' 
                    return render_template ('welcome.html',error1=error , club=club, competitions=competitions)  
                        


@app.route('/logout')
def logout():
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(debug=True)