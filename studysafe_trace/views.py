from multiprocessing import context
from django.shortcuts import render
import requests
context={}
def view_base(request):
    

    return render(request,'base.html',context=context)
def view_contacts(request):
    contacts=[]
    subject = request.GET.get("uid")
    date = request.GET.get("diagnosis-date")
    results = requests.get(f"https://calm-hollows-40078.herokuapp.com/coreapi/close-contacts?uid={subject}&diagnosis-date={date}").json()
    for result in results:
        contacts.append("Name: "+result["name"]+", UID: "+result["hku_id"])
    context={"subject":subject,"date":date,"contacts":contacts}
    
    
    
    return render(request,'contacts.html',context=context)
def view_venues(request):
    venues=[]
    subject = request.GET.get("uid")
    date = request.GET.get("diagnosis-date")
    results = requests.get(f"https://calm-hollows-40078.herokuapp.com/coreapi/visited-venues?uid={subject}&diagnosis-date={date}").json()
    for result in results:
        venues.append(result["venue"])
    context={"subject":subject,"date":date,"venues":venues}
    return render(request,'venues.html',context=context)
