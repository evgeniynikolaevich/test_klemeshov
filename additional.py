




#1

from django.db import models
from django.db.models.functions import Trunc

class Person(models.Model):
    name = models.TextField(blank=True,  null=True, verbose_name='Название')
    date = models.DateField(blank=True, null=True, verbose_name='Дата')
    time = models.TimeField(blank=True, null=True, verbose_name='Время')


Person.objects.all().filter(date=datetime.datetime.now()).order_by('-time')

#2.
from django.conf import settings
from datetime import datetime
from django.utils import dateformat
from django.shortcuts import render_to_response
#in settings 
######################################
LANGUAGE_CODE = 'ru-RU'
DATE_FORMAT = 'd E Y'
######################################

def return_date_by_full_month(request):
    formatted_date = dateformat.format(datetime.now(), settings.DATE_FORMAT)
    return render_to_response('dateapp/date_display.html',{'date':formatted_date})
    


#3

    function getValuesFromInputs(){
        let map = {};
        $(".someInputClass").each(function() {
        map[$(this).attr("name")] = $(this).val();
       });
    }
    