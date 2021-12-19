import requests
from isodate import parse_duration
from product.serializers import ProductSerializer

from .filters import *
from .models import Product

from django.shortcuts import render, redirect
from django.views.generic import ListView, CreateView, DetailView
from django.core.paginator import Paginator
from django.conf import settings
from rest_framework import viewsets, permissions
from django.contrib.auth.mixins import LoginRequiredMixin

from rest_framework.generics import ListAPIView, CreateAPIView, DestroyAPIView, UpdateAPIView
# Create your views here.
# class ProductDetail(DetailView):
#     model = Product
#     template_name = 'product/product_detail.html'


# View for YouTube videos:
def index(request):
    videos = []
    if request.method == 'POST':
        search_url = 'https://www.googleapis.com/youtube/v3/search'
        video_url = 'https://www.googleapis.com/youtube/v3/videos'
        search_params = {
            'part': 'snippet',
            'q': request.POST['search'],
            'key': settings.YOUTUBE_DATA_API_KEY,
            'maxResults': 9,
            'type': 'video'
        }

        r = requests.get(search_url, params=search_params)
        results = r.json()['items']
        video_ids = []
        for result in results:
            video_ids.append(result['id']['videoId'])
        if request.POST['submit'] == 'lucky':
            return redirect(f'https://www.youtube.com/watch?v={video_ids[0]}')
        video_params = {
            'key': settings.YOUTUBE_DATA_API_KEY,
            'part': 'snippet,contentDetails',
            'id': ','.join(video_ids),
            'maxResults': 12
        }

        r = requests.get(video_url, params=video_params)
        results = r.json()['items']
        for result in results:
            video_data = {
                'title': result['snippet']['title'],
                'id': result['id'],
                'url': f'https://www.youtube.com/watch?v={result["id"]}',
                'duration': int(parse_duration(result['contentDetails']['duration']).total_seconds() // 60),
                'thumbnail': result['snippet']['thumbnails']['high']['url']
            }

            videos.append(video_data)
    context = {
        'videos': videos
    }
    return render(request, 'product/youtube.html', context)


def product_detail(request, pk):
    context = {}
    context["data"] = Product.objects.get(id=pk)
    return render(request, 'product/product_detail.html', context)


class AddProductView(LoginRequiredMixin, CreateView):
    model = Product
    template_name = 'product/add_product.html'
    fields = ['title', 'type', 'image', 'description']

def list_product(request):
    query_product = Product.objects.all()
    product = Product.objects.all()
    paginator = Paginator(product, 3)
    # The page query string value is fetched with the request.GET.get() function and passed to the paginator.get_page()
    page = request.GET.get('page')
    product = paginator.get_page(page)
    filter = ProductFilter(request.GET, queryset=query_product)
    return render(request, 'product/list_product.html', {'product': product, 'filter': filter})


def list_product_wallpaper(request):
    product = Product.objects.filter(type="Wallpaper")
    filter = ProductFilter(request.GET, queryset=product)
    return render(request, 'product/list_product.html', {'filter': filter})


def list_product_artifact(request):
    product = Product.objects.filter(type="Artifact")
    filter = ProductFilter(request.GET, queryset=product)
    return render(request, 'product/list_product.html', {'filter': filter})


def search(request):
    objects = Product.objects.all()
    filter = ProductFilter(request.GET, queryset=objects)
    return render(request, 'product/list_product.html', {'filter': filter})


class ProductView(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticated]

# class ListProductsView(LoginRequiredMixin, ListView):
#     model = Product
#     template_name = 'product/list_product.html'
#     paginate_by = 2

