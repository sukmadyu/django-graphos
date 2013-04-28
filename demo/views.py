from django.shortcuts import render

from graphos.renderers.flot import LineChart
from graphos.renderers import gchart, yui
from graphos.sources.simple import SimpleDataSource
from graphos.sources.model import ModelDataSource
from .models import Account

data = [
       ['Year', 'Sales', 'Expenses'],
       ['2004', 1000, 400],
       ['2005', 1170, 460],
       ['2006', 660, 1120],
       ['2007', 1030, 540], ]

candlestick_data = [
          ['Mon', 20, 28, 38, 45],
          ['Tue', 31, 38, 55, 66],
          ['Wed', 50, 55, 77, 80],
          ['Thu', 77, 77, 66, 50],
          ['Fri', 68, 66, 22, 15]
        ]

def create_demo_accounts():
    Account.objects.all().delete()
    #Create some rows
    Account.objects.create(year="2004", sales=1000,
                           expenses=400, ceo="Welch")
    Account.objects.create(year="2005", sales=1170,
                           expenses=460, ceo="Jobs")
    Account.objects.create(year="2006", sales=660,
                           expenses=1120, ceo="Page")
    Account.objects.create(year="2007", sales=1030,
                           expenses=540, ceo="Welch")
    Account.objects.create(year="2008", sales=2030,
                           expenses=1540, ceo="Zuck")
    Account.objects.create(year="2009", sales=2230,
                           expenses=1840, ceo="Cook")

def home(request):
    chart = LineChart(SimpleDataSource(data=data), html_id="line_chart")
    g_chart = gchart.LineChart(SimpleDataSource(data=data))
    return render(request, 'demo/home.html', {'chart': chart,
                                              'g_chart': g_chart},)


def tutorial(request):
    chart = LineChart(SimpleDataSource(data=data), html_id="line_chart")
    return render(request, 'demo/tutorial.html', {'chart': chart}, )


def gchart_demo(request):
    create_demo_accounts()
    queryset = Account.objects.all()
    fields = ['year', 'sales', 'expenses']
    data_source = ModelDataSource(queryset,
                                  fields=['year', 'sales',],)
    line_chart = gchart.LineChart(data_source, options={'title': "Sales Growth"})
    column_chart = gchart.ColumnChart(SimpleDataSource(data=data),
                                                      {'title': "Sales Growth"})
    bar_chart = gchart.BarChart(SimpleDataSource(data=data))
    candlestick_chart = gchart.CandlestickChart(SimpleDataSource
                                                (data=candlestick_data))
    pie_chart = gchart.PieChart(ModelDataSource(queryset, fields=fields[:2]))
    context = {"line_chart": line_chart, "column_chart": column_chart,
               'bar_chart': bar_chart, 'candlestick_chart': candlestick_chart,
               'pie_chart': pie_chart}
    return render(request, 'demo/gchart.html', context)


def yui_demo(request):
    line_chart = yui.LineChart(SimpleDataSource(data=data))
    context = {"line_chart": line_chart}
    return render(request, 'demo/yui.html', context)
