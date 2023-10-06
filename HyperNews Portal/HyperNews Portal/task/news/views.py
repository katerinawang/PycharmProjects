import os.path
import json
import random
from datetime import datetime
from collections import defaultdict

from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views import View
from django.conf import settings

path = os.path.join(settings.BASE_DIR, 'hypernews/', settings.NEWS_JSON_PATH)
link = []


# Create your views here.
class ComingSoonView(View):
    def get(self, request, *args, **kwargs):
        return HttpResponse('Coming soon')


class MainPageView(View):
    def get(self, request, *args, **kwargs):
        global link
        days = defaultdict(list)
        with open(path, 'r') as f:
            articles = sorted(json.load(f), key=lambda d: d['created'], reverse=True)
        for article in articles:
            article['created'] = datetime.strptime(article['created'][:10], "%Y-%m-%d")
            if not request.GET.get('q'):
                days[article['created']].append((article['link'], article['title']))
            else:
                if request.GET.get('q') in article['title']:
                    days[article['created']].append((article['link'], article['title']))
            link.append(article['link'])
        return render(request, 'main.html', context={'articles': dict(days)})


class ArticleView(View):
    def get(self, request, link, *args, **kwargs):
        with open(path, 'r') as f:
            articles = json.load(f)
        for article in articles:
            if article['link'] == link:
                return render(request, 'article.html', context={'content': article})


class CreateView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'create.html')

    def post(self, request, *args, **kwargs):
        global link
        created = datetime.now()
        random.seed(created)
        article_link = random.randint(1000, 9999)
        while article_link in link:
            article_link = random.randint(1000, 9999)
        link.append(article_link)
        article = {'created': datetime.strftime(created, "%Y-%m-%d %H:%M:%S"), 'text': request.POST['text'], 'title': request.POST['title'], 'link': article_link}
        with open(path, 'r') as f:
            articles = json.load(f)
        articles.append(article)
        print(articles)
        with open(path, 'w') as f:
            f.write(json.dumps(articles))
        return redirect('/news/')
