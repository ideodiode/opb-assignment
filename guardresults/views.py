from django.shortcuts import render, redirect
from urllib.request import urlopen, Request
from django.http import HttpResponse
import json, datetime

def home_page(request):
    now = datetime.datetime.now()
    years = list(range(2008, now.year+1))
    return render(request, 'home.html', {'years':years})

def search(request):
    url = 'http://content.guardianapis.com/search?'
    if len(request.GET):
        url += request.GET.urlencode() + '&show-fields=all'
    else:
        url += 'q='
    data = query_api(url)['response']
    
    total_pages = data['pages']
    current_page = data['currentPage']
    if total_pages < 11:
        low_page, high_page = 1, total_pages
    elif current_page < 6:
        low_page, high_page = 1, 10
    elif current_page > total_pages-4:
        low_page, high_page = total_pages-9, total_pages
    else:
        low_page, high_page = current_page-5, current_page+4
    page_numbers = list(range(low_page, high_page+1))
    
    querydict = request.GET.copy()
    if 'page' in querydict:
        del querydict['page']
    pagination_url = request.path_info + '?' + querydict.urlencode()

    querydict = request.GET.copy()
    if 'page-size' in querydict:
        del querydict['page-size']
    per_page_url = request.path_info + '?' + querydict.urlencode()

    per_page = request.GET.get('page-size', '')
    q = request.GET.get('q', '')
    now = datetime.datetime.now()
    years = list(range(2008, now.year+1))
    
    return render(request, 'home.html', {
        'search_response':data,
        'q':q,
        'years':years,
        'pagination_url':pagination_url,
        'per_page_url':per_page_url,
        'per_page':per_page,
        'page_numbers':page_numbers,
        })

def related_search(request):
    if request.is_ajax():
        article_id = request.GET['id']
        url = 'http://content.guardianapis.com/' + article_id + '?show-fields=all&show-related=true&page-size=5'
        data = query_api(url)['response']['relatedContent']
        return HttpResponse(json.dumps(data), mimetype='application/json')
    else:
        return redirect('/')
# Helper methods

def query_api(url):
    search_request = Request(url)
    response = urlopen(search_request)
    response_string = response.read().decode('utf-8')
    data = json.loads(response_string)
    return data
