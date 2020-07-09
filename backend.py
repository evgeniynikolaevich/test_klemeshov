from django.db import models
from app.category import Category
import json
from django.db.models import Q
from django.core import serializers
from django.http import HttpResponse,JsonResponse
from django.test import TestCase,Client
import random
from django.utils.crypto import get_random_string
from django.template.defaultfilters import slugify
from faker import Faker
from django.urls import reverse

#1
class Product(models.Model):
    categories = models.ManyToManyField(Category,related_name='products',blank=True, verbose_name=u"категории")
    related_products = models.ManyToManyField('Product',blank=True,verbose_name="связанные продукты")
    sku = models.CharField(u'артикул', max_length=128, validators=[validators.check_bad_symbols], unique=True)
    price = models.DecimalField(u'цена', max_digits=12, decimal_places=4)
    slug = models.SlugField(u'slug', max_length=80, db_index=True, unique=True)
    name = models.CharField(u'название', max_length=128)
    title = models.CharField(u'заголовок страницы (<title>)', max_length=256, blank=True)
    description = models.TextField(u'описание', blank=True)

def live_search(request, template_name="shop/livesearch_results.html"):
    q = request.GET.get("q", "")
    objects = Product.objects.filter(
        Q(sku__contains=q) |
        Q(name__contains=q) |
        Q(description__contains=q))
    qs_json = serializers.serialize('json', objects)
    return HttpResponse(qs_json, content_type='application/json')

#or
def some_another_live_search(request, template_name="shop/livesearch_results.html"):
    q = request.GET.get("q", "")
    objects = Product.objects.filter(
        Q(sku__contains=q) |
        Q(name__contains=q) |
        Q(description__contains=q))
    data = list(objects.values())
    return JsonResponse(data, safe=False)



#some tests
#2



class BasicTest(TestCase):
    def test_fields(self):
        fake = Faker()
        categ = Category.objects.last()
        related_products = Product.objects.last()
        item = Product()
        item.sku = get_random_string(length=32)
        item.price = random.randint(1000,10000)
        item.name = fake.name()
        item.slug = slugify(item.name)
        item.title = fake.address()
        item.description = fake.text()
        item.save()
        record = Product.objects.get(name = item.name) 
        self.assertEqual(record,item)
    

    def setUp(self):
        self.client = Client()
        self.list_url = reverse('live_search')



    def test_live_search(self):
        response = self.client.get(reverse(self.list_url))
        self.assertEqual(response.status_code,200)
         

