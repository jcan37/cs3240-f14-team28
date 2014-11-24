from models import Bulletin

def search(field):
    	results = Bulletin.objects.all().filter(field in description)
        print results
        context['results'] = results
    	return render(request, 'searchresults.html', context)
