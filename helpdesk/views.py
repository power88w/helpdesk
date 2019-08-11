from django.shortcuts import render
from django.http import HttpResponse
from services.models import BlogPost as bbp



def home_page(request):
    bc = bbp.objects.all().count()
    if bc>3:
        blogs = bbp.objects.order_by('votes')[bc-3::-1]
    else:
        blogs = bbp.objects.order_by('votes')[::-1]
    context = {'rows_services':blogs,}
    return render(request,"helpdesk.html",context)



def charts(request):
    fw = fbp.objects.filter(status='waiting').count()
    fp = fbp.objects.filter(status='in progress').count()
    fc = fbp.objects.filter(status='completed').count()
    bw = bbp.objects.filter(status='waiting').count()
    bp = bbp.objects.filter(status='in progress').count()
    bc = bbp.objects.filter(status='completed').count()
    pie_chart1 = pygal.Pie(inner_radius=.4,print_values=True)
    pie_chart1.title = 'services'
    pie_chart1.add('waiting', bw)
    pie_chart1.add('in progress', bp)
    pie_chart1.add('completed', bc)
    pie_chart2 = pygal.Pie(inner_radius=.4,print_values=True)
    pie_chart2.title = 'hardware'
    pie_chart2.add('waiting', fw)
    pie_chart2.add('in progress', fp)
    pie_chart2.add('completed', fc)
    feature = pie_chart2.render()
    bugs = pie_chart1.render()
    context = {"fc":feature.decode('utf-8'),'bc':bugs.decode('utf-8')}
    return render(request,"charts.html",context)