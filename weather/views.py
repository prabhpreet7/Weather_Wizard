from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import City
from .forms import CityForm
import requests
# Create your views here.
def history(request):
    #City.objects.all().delete()
    #key='4e11d2dbb34231ab740cbbc6b1d1ee1b'
    url='http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=4e11d2dbb34231ab740cbbc6b1d1ee1b'
    err_msg=''
    message=''
    message_class=''

    #save information to database
    if request.method=='POST':
        form=CityForm(request.POST)

        if form.is_valid():
            new_city=form.cleaned_data['name']
            existing_city_count= City.objects.filter(name=new_city).count()
            data=requests.get(url.format(new_city)).json()
            if existing_city_count==0:

                if data['cod']==200:
                    form.save()
                else:
                    err_msg="City doesn't exist fool!!"
            else:
                City.objects.filter(name=new_city).delete()
                form.save()
                # err_msg='City Already Exists you Blind-Ass!!'

        if err_msg:
            message=err_msg
            message_class='is-danger'
        else:
            message='City added Successfully my boiii!'
            message_class='is-success'


    #To create empty form in starting or when one form is submitted
    form=CityForm()
    cities=City.objects.all()
    weather_data=[]
    for city in cities:
        data=requests.get(url.format(city)).json()

        city_weather={'city_name':data['name'],
                       'temperature':data['main']['temp'],
                       'description':data['weather'][0]['description'],
                       'icon':data['weather'][0]['icon'],
                       'temp_min': data['main']['temp_min'],
                       'temp_max': data['main']['temp_max'],
                       'humidity': data['main']['humidity']}
        weather_data.insert(0,city_weather)


    context={'weather_data':weather_data,'form':form, 'message':message,'message_class':message_class}
    return render(request, 'weather/home.html',context)

def home(request):
    url='http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=4e11d2dbb34231ab740cbbc6b1d1ee1b'
    err_msg=''
    message=''
    message_class=''
    flag=False
    #save information to database
    if request.method=='POST':
        form=CityForm(request.POST)

        if form.is_valid():
            new_city=form.cleaned_data['name']

            data=requests.get(url.format(new_city)).json()

            if data['cod']==200:
                flag=True
                existing_city_count= City.objects.filter(name=new_city).count()

                if existing_city_count==0:
                    form.save()
                else:
                    City.objects.filter(name=new_city).delete()
                    form.save()
            else:
                err_msg="City doesn't exist !!"

            #print(new_city)


    #To create empty form in starting or when one form is submitted
    form=CityForm()
    if flag==True and new_city:
        data=requests.get(url.format(new_city)).json()
        print(data)
        weather_data=[]
        city_weather={'city_name':data['name'],
                       'temperature':data['main']['temp'],
                       'description':data['weather'][0]['description'],
                       'icon':data['weather'][0]['icon'],
                       'temp_min': data['main']['temp_min'],
                       'temp_max': data['main']['temp_max'],
                       'humidity': data['main']['humidity']}
        weather_data.append(city_weather)


        context={'weather_data':weather_data,'form':form}
        return render(request, 'weather/home.html',context)

    else:
        context={'form':form,'message':err_msg,'message_class':'is-danger'}
        return render(request, 'weather/home.html',context)


def delete_city(request,city_name):
    City.objects.get(name=city_name.lower()).delete()
    return redirect('home')
