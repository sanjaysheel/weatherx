from django.http.response import JsonResponse
from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.shortcuts import render
import requests
from django.views.generic import View
from .models import City
import datetime
# import json to load json data to python dictionary
import json
# urllib.request to make a request to api
import urllib.request
from django.db.models import Q
from django.contrib import messages
from weth.models import City
from datetime import datetime as date
import json
# Create your views here.




def editing(request):
    if request.method == "POST":
        newname1 = request.POST.get("newname")
        onename1 = request.POST.get("onename")
        if City.objects.filter(name = newname1):
            messages.error(request,"your requested city {0} already exists..!".format(newname1))
            return redirect(f'/')
        else:    
            sk = City.objects.filter(name=onename1).update(name=newname1)
            messages.success(request,"your city successfully updated..!")
            return redirect(f'/')




def index1(request):
    return render(request, 'index1.html')

    

def autosuggest(request):
    query_o = request.GET.get('term')
    query = City.objects.filter(Q(name__icontains = query_o))
    mylist = []
    mylist = [x.title for x in query]
    return JsonResponse(mylist, safe = False)



def delete(request):
    if request.method == "POST":
        newname1 = request.POST.get("newname")
        City.objects.filter(name=newname1).delete()
        messages.success(request,"your city successfully deleted")
    return redirect(f'/')




def index(request):
    if request.method != "POST":
        
        city="delhi"
        source = requests.get("http://api.openweathermap.org/data/2.5/weather?q="+str(city)+"&&units=metric&APPID=b441443ea9bc1df5b602a01d7c0146ee")
        da = source.json()
        
        weather1 = {
            'city': city,
            'temperature': da['main']['temp'],
            'description': da['weather'][0]['description'],
            'icon': da['weather'][0]['icon'],
            'temperature_max': da['main']['temp_max'] ,
            'temperature_min':  da['main']['temp_min']  ,
            'feelslike_weather': da['main']['feels_like'],
            "humidity1":da['main']["humidity"],
            "windspeed":3.6*int(da['wind']['speed']),   
            "country":da['sys']["country"],
        }
        print("this is get method working ",weather1['city'])
        now = datetime.datetime.now()
        st = {"day":date.today().strftime("%A"),"time":now.strftime("%H:%M %p")}
        citylist = []
        weather = {}
        citynemelist  =  City.objects.all()
        for i in citynemelist:
            source1 = requests.get("http://api.openweathermap.org/data/2.5/weather?q="+str(i)+"&&units=metric&APPID=b441443ea9bc1df5b602a01d7c0146ee")
            da = source1.json()
            
            weather = {
                'city': i,
                'temperature': da['main']['temp'],
                'description': da['weather'][0]['description'],
                'icon': da['weather'][0]['icon'],
                'temperature_max': da['main']['temp_max'] ,
                'temperature_min':  da['main']['temp_min']  ,
                'feelslike_weather': da['main']['feels_like'],
                "country":da['sys']["country"],
                "windspeed":3.6*int(da['wind']['speed']),
                "humidity1":da['main']["humidity"],
            }
            citylist.append(weather)
        c = {"data": weather,"st":st,"citylist":citylist}
        ListValue = []
        listday = []
        a = requests.get('http://api.openweathermap.org/data/2.5/forecast?q='+city+'&&units=metric&appid=b441443ea9bc1df5b602a01d7c0146ee')
        # accessing the API json data
        full = a.json()

        # today's date taking as int
        day = datetime.datetime.today()
        today_date = int(day.strftime('%d'))

        forcast_data_list = {}  # dictionary to store json data

        # looping to get value and put it in the dictionary
        for c in range(0, full['cnt']):
            date_var1 = full['list'][c]['dt_txt']
            date_time_obj1 = datetime.datetime.strptime(date_var1, '%Y-%m-%d %H:%M:%S')
            if int(date_time_obj1.strftime('%d')) == today_date or int(date_time_obj1.strftime('%d')) == today_date+1:
                if int(date_time_obj1.strftime('%d')) == today_date+1:
                    today_date += 1
                    forcast_data_list[today_date] = {}
                    forcast_data_list[today_date]['day'] = date_time_obj1.strftime('%A')
                    forcast_data_list[today_date]['date'] = date_time_obj1.strftime('%d %b, %Y')
                    forcast_data_list[today_date]['time'] = date_time_obj1.strftime('%I:%M %p')
                    forcast_data_list[today_date]['FeelsLike'] = full['list'][c]['main']['feels_like']
                    forcast_data_list[today_date]['temperature'] = full['list'][c]['main']['temp']
                    forcast_data_list[today_date]['temperature_max'] = full['list'][c]['main']['temp_max']
                    forcast_data_list[today_date]['temperature_min'] = full['list'][c]['main']['temp_min']
                    forcast_data_list[today_date]['description'] = full['list'][c]['weather'][0]['description']
                    forcast_data_list[today_date]['icon'] = full['list'][c]['weather'][0]['icon']
                    ListValue.append(float(full['list'][c]['main']['temp']))
                    listday.append(date_time_obj1.strftime('%A'))
                    
                    # today_date += 1?
                else:
                    pass
        context = {
            'weather': weather,'weather1': weather1, 'forcast': forcast_data_list,"st":st,"citylist":citylist , "ListValue":ListValue ,"listday":listday
        }
        return render(request, "index.html", context)
    if request.method == 'POST':
        city = request.POST.get('name')
        check = requests.get("http://api.openweathermap.org/data/2.5/weather?q="+city+"&&units=metric&APPID=b441443ea9bc1df5b602a01d7c0146ee")
        if check.json()['cod'] == 200:
            if City.objects.filter(name=city).exists():
                source = requests.get("http://api.openweathermap.org/data/2.5/weather?q="+city+"&&units=metric&APPID=b441443ea9bc1df5b602a01d7c0146ee")
                
                da = source.json()
                weather1 = {
                    'city': city,
                    'temperature': da['main']['temp'],
                    'description': da['weather'][0]['description'],
                    'icon': da['weather'][0]['icon'],
                    'temperature_max': da['main']['temp_max'] ,
                    'temperature_min':  da['main']['temp_min']  ,
                    'feelslike_weather': da['main']['feels_like'],
                    "country":da['sys']["country"],
                }
                
                now = datetime.datetime.now()
                st = {"day":date.today().strftime("%A"),"time":now.strftime("%H:%M %p")}
                citylist = []
                citynemelist  =  City.objects.all()
                for i in citynemelist:
                    source1 = requests.get("http://api.openweathermap.org/data/2.5/weather?q="+str(i)+"&&units=metric&APPID=b441443ea9bc1df5b602a01d7c0146ee")
                    da = source1.json()
                    weather = {
                        'city': i,
                        'temperature': da['main']['temp'],
                        'description': da['weather'][0]['description'],
                        'icon': da['weather'][0]['icon'],
                        'temperature_max': da['main']['temp_max'] ,
                        'temperature_min':  da['main']['temp_min']  ,
                        'feelslike_weather': da['main']['feels_like'],
                        "country":da['sys']["country"],
                        "windspeed":3.6*int(da['wind']['speed']),
                        "humidity1":da['main']["humidity"],
                    }
                    citylist.append(weather)
                ListValue = []
                listday = []
                a = requests.get('http://api.openweathermap.org/data/2.5/forecast?q='+city+'&&units=metric&appid=b441443ea9bc1df5b602a01d7c0146ee')
                full = a.json()
                day = datetime.datetime.today()
                today_date = int(day.strftime('%d'))
                forcast_data_list = {}  # dictionary to store json data
                for c in range(0, full['cnt']):
                    date_var1 = full['list'][c]['dt_txt']
                    date_time_obj1 = datetime.datetime.strptime(date_var1, '%Y-%m-%d %H:%M:%S')
                    if int(date_time_obj1.strftime('%d')) == today_date or int(date_time_obj1.strftime('%d')) == today_date+1:
                        if int(date_time_obj1.strftime('%d')) == today_date+1:
                            today_date += 1
                            forcast_data_list[today_date] = {}
                            forcast_data_list[today_date]['day'] = date_time_obj1.strftime('%A')
                            forcast_data_list[today_date]['date'] = date_time_obj1.strftime('%d %b, %Y')
                            forcast_data_list[today_date]['time'] = date_time_obj1.strftime('%I:%M %p')
                            forcast_data_list[today_date]['FeelsLike'] = full['list'][c]['main']['feels_like']
                            forcast_data_list[today_date]['temperature'] = full['list'][c]['main']['temp']
                            forcast_data_list[today_date]['temperature_max'] = full['list'][c]['main']['temp_max']
                            forcast_data_list[today_date]['temperature_min'] = full['list'][c]['main']['temp_min']
                            forcast_data_list[today_date]['description'] = full['list'][c]['weather'][0]['description']
                            forcast_data_list[today_date]['icon'] = full['list'][c]['weather'][0]['icon']
                            ListValue.append(float(full['list'][c]['main']['temp']))
                            listday.append(date_time_obj1.strftime('%A'))
                            # today_date += 1?
                        else:
                            pass
                # returning the context with all the data to the index.html
                print("@@@@@@@@@@@@@@@@",ListValue)
                context = {
                    'weather': weather,'weather1': weather1, 'forcast': forcast_data_list,"st":st, "citylist":citylist,"ListValue":ListValue,"listday":listday
                }
                messages.error(request,"Entered name '{0}' already exists..!".format(city))
                return render(request, "index.html", context)
            else:
                
                City(name = city).save()
                source = requests.get("http://api.openweathermap.org/data/2.5/weather?q="+city+"&&units=metric&APPID=b441443ea9bc1df5b602a01d7c0146ee")
                da = source.json()
                weather1 = {
                    'city': city,
                    'temperature': da['main']['temp'],
                    'description': da['weather'][0]['description'],
                    'icon': da['weather'][0]['icon'],
                    'temperature_max': da['main']['temp_max'] ,
                    'temperature_min':  da['main']['temp_min']  ,
                    'feelslike_weather': da['main']['feels_like'],
                    "windspeed":3.6*int(da['wind']['speed']),
                    "humidity1":da['main']["humidity"],
                }
                now = datetime.datetime.now()
                st = {"day":date.today().strftime("%A"),"time":now.strftime("%H:%M %p")}
                # c = {"data": weather,"st":st}
                citylist = []
                citynemelist  =  City.objects.all()
                for i in citynemelist:
                    source1 = requests.get("http://api.openweathermap.org/data/2.5/weather?q="+str(i)+"&&units=metric&APPID=b441443ea9bc1df5b602a01d7c0146ee")
                    da = source1.json()
                    weather = {
                        'city': i,
                        'temperature': da['main']['temp'],
                        'description': da['weather'][0]['description'],
                        'icon': da['weather'][0]['icon'],
                        'temperature_max': da['main']['temp_max'] ,
                        'temperature_min':  da['main']['temp_min']  ,
                        'feelslike_weather': da['main']['feels_like'],
                        "country":da['sys']["country"],
                        "windspeed":3.6*int(da['wind']['speed']),
                        "humidity1":da['main']["humidity"],
                    }
                    citylist.append(weather)
                ListValue = []
                listday = []
                a = requests.get('http://api.openweathermap.org/data/2.5/forecast?q='+city+'&&units=metric&appid=b441443ea9bc1df5b602a01d7c0146ee')
                # accessing the API json data
                full = a.json()

                # today's date taking as int
                day = datetime.datetime.today()
                today_date = int(day.strftime('%d'))

                forcast_data_list = {}  # dictionary to store json data

                # looping to get value and put it in the dictionary
                for c in range(0, full['cnt']):
                    date_var1 = full['list'][c]['dt_txt']
                    date_time_obj1 = datetime.datetime.strptime(date_var1, '%Y-%m-%d %H:%M:%S')
                    # to process date
                    if int(date_time_obj1.strftime('%d')) == today_date or int(date_time_obj1.strftime('%d')) == today_date+1:
                        if int(date_time_obj1.strftime('%d')) == today_date+1:
                            today_date += 1
                            forcast_data_list[today_date] = {}
                            forcast_data_list[today_date]['day'] = date_time_obj1.strftime('%A')
                            forcast_data_list[today_date]['date'] = date_time_obj1.strftime('%d %b, %Y')
                            forcast_data_list[today_date]['time'] = date_time_obj1.strftime('%I:%M %p')
                            forcast_data_list[today_date]['FeelsLike'] = full['list'][c]['main']['feels_like']
                            forcast_data_list[today_date]['temperature'] = full['list'][c]['main']['temp']
                            forcast_data_list[today_date]['temperature_max'] = full['list'][c]['main']['temp_max']
                            forcast_data_list[today_date]['temperature_min'] = full['list'][c]['main']['temp_min']
                            forcast_data_list[today_date]['description'] = full['list'][c]['weather'][0]['description']
                            forcast_data_list[today_date]['icon'] = full['list'][c]['weather'][0]['icon']
                            ListValue.append(float(full['list'][c]['main']['temp']))
                            listday.append(date_time_obj1.strftime('%A'))
                            # today_date += 1?
                        else:
                            pass
                context = {
                    'weather': weather,'weather1': weather1, 'forcast': forcast_data_list,"st":st,"citylist":citylist,"ListValue":ListValue,"listday":listday
                }
                messages.success(request,"Your city '{0}' have added successfully..!".format(city))
                return render(request, "index.html", context)
        else:
            namew = 'delhi'
            source = requests.get("http://api.openweathermap.org/data/2.5/weather?q="+namew+"&&units=metric&APPID=b441443ea9bc1df5b602a01d7c0146ee")
            da = source.json()
            weather1 = {
                'city': city,
                'temperature': da['main']['temp'],
                'description': da['weather'][0]['description'],
                'icon': da['weather'][0]['icon'],
                'temperature_max': da['main']['temp_max'] ,
                'temperature_min':  da['main']['temp_min']  ,
                'feelslike_weather': da['main']['feels_like'],
                "country":da['sys']["country"],
                "windspeed":3.6*int(da['wind']['speed']),
                "humidity1":da['main']["humidity"],
            }
            print(weather1)
            now = datetime.datetime.now()
            st = {"day":date.today().strftime("%A"),"time":now.strftime("%H:%M %p")}
            citylist = []
            citynemelist  =  City.objects.all()
            for i in citynemelist:
                source1 = requests.get("http://api.openweathermap.org/data/2.5/weather?q="+str(i)+"&&units=metric&APPID=b441443ea9bc1df5b602a01d7c0146ee")
                da = source1.json()
                weather = {
                    'city': i,
                    'temperature': da['main']['temp'],
                    'description': da['weather'][0]['description'],
                    'icon': da['weather'][0]['icon'],
                    'temperature_max': da['main']['temp_max'] ,
                    'temperature_min':  da['main']['temp_min']  ,
                    'feelslike_weather': da['main']['feels_like'],
                    "country":da['sys']["country"],
                    "windspeed":3.6*int(da['wind']['speed']),
                    "humidity1":da['main']["humidity"],
                }
                citylist.append(weather)
            print(citylist)
            ListValue = []
            listday = []
            
            a = requests.get('http://api.openweathermap.org/data/2.5/forecast?q='+namew+'&&units=metric&appid=b441443ea9bc1df5b602a01d7c0146ee')
            full = a.json()
            day = datetime.datetime.today()
            today_date = int(day.strftime('%d'))
            forcast_data_list = {}  
            for c in range(0, full['cnt']):
                date_var1 = full['list'][c]['dt_txt']
                date_time_obj1 = datetime.datetime.strptime(date_var1, '%Y-%m-%d %H:%M:%S')
                if int(date_time_obj1.strftime('%d')) == today_date or int(date_time_obj1.strftime('%d')) == today_date+1:
                    if int(date_time_obj1.strftime('%d')) == today_date+1:
                        today_date += 1
                        forcast_data_list[today_date] = {}
                        forcast_data_list[today_date]['day'] = date_time_obj1.strftime('%A')
                        forcast_data_list[today_date]['date'] = date_time_obj1.strftime('%d %b, %Y')
                        forcast_data_list[today_date]['time'] = date_time_obj1.strftime('%I:%M %p')
                        forcast_data_list[today_date]['FeelsLike'] = full['list'][c]['main']['feels_like']
                        forcast_data_list[today_date]['temperature'] = full['list'][c]['main']['temp']
                        forcast_data_list[today_date]['temperature_max'] = full['list'][c]['main']['temp_max']
                        forcast_data_list[today_date]['temperature_min'] = full['list'][c]['main']['temp_min']
                        forcast_data_list[today_date]['description'] = full['list'][c]['weather'][0]['description']
                        forcast_data_list[today_date]['icon'] = full['list'][c]['weather'][0]['icon']
                        ListValue.append(float(full['list'][c]['main']['temp']))
                        listday.append(date_time_obj1.strftime('%A'))
                        # today_date += 1?
                    else:
                        pass
            # returning the context with all the data to the index.html
            print("@@@@@@@@@@@@@@@@",ListValue)
            context = {
                'weather': weather,'weather1': weather1, 'forcast': forcast_data_list,"st":st, "citylist":citylist,"ListValue":ListValue,"listday":listday
            }
            messages.error(request,"City '{0}' does not exists..!".format(city))
            return render(request, "index.html",context)
    else:
        messages.error(request,'index.html')
        return render(request, "index.html")

