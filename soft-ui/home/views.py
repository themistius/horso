from django.shortcuts import render
from .models import Races
import urllib

def index(request):
    # Retrieve all race data from your database
    all_race_data = Races.objects.all()

    # Create a dictionary to organize the data by city
    race_times = {}

    for race in all_race_data:
        city = race.city

        # Create an entry for the city if it doesn't exist
        if city not in race_times:
            race_times[city] = []


        # Retrieve the data for this race
        race_data = {
            'RaceTime': race.race_time,
            'AtIsmi': race.at_i_smi,
            'Yas': race.yaş,
            'OrijinBabaAnne': race.orijin_baba_anne_field,
            'Sıklet': race.sıklet,
            'Jokey': race.jokey,
            'Sahip': race.sahip,
            'Antrenör': race.antrenör,
            'St': race.st,
            'HP': race.hp,
            'Son6Y': race.son_6_y_field,
            'KGS': race.kgs,
            'S20': race.s20,
            'EnIyiD': race.en_i_yi_d_field,
            'Gny': race.gny,
            'AGF': race.agf,
            # Add more fields as needed
        }
    
        # Append the race data to the city's list
        race_times[city].append(race_data)


    return render(request, 'pages/index.html', {'race_times': race_times})
