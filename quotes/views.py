from django.shortcuts import render, redirect
from .models import Stock
from django.contrib import messages
from .forms import StockForm

def home(request):
	import requests
	import json

	if request.method == "POST":
		ticker = request.POST['ticker']
		res1 = requests.get("https://cloud.iexapis.com/stable/stock/"+ ticker +"/quote?token=pk_ac1cea4a38d044daa2ebbea560fbc669")
		res2 = requests.get("https://cloud.iexapis.com/stable/stock/"+ ticker +"/logo?token=pk_ac1cea4a38d044daa2ebbea560fbc669")
		res3 = requests.get("https://cloud.iexapis.com/stable/stock/"+ ticker +"/company?token=pk_ac1cea4a38d044daa2ebbea560fbc669")

		try :
			data1 = json.loads(res1.content)
			data2 = json.loads(res2.content)
			data3 = json.loads(res3.content)
			
		except Exception as e:
			data1 = "Error..."
			data2 = "Error..."
			data3 = "Error..."

	
		return render(request, 'home.html', {'data1': data1, 'data2': data2, 'data3': data3 })
	else:
		return render(request, 'home.html', {'ticker': "Please Enter Ticker Symbol above."})	


def add_stock(request):
	import requests
	import json



	if request.method == "POST":
		form = StockForm(request.POST or None)

		if form.is_valid():
			form.save()
			messages.success(request, ("Stock has been added!"))
			return redirect('add_stock')
	else:
		ticker = Stock.objects.all()
		output = []
			
		for ticker_item in ticker:	
			res = requests.get("https://cloud.iexapis.com/stable/stock/"+ str(ticker_item) +"/quote?token=pk_ac1cea4a38d044daa2ebbea560fbc669")

			try :
				data = json.loads(res.content)
		
				output.append(data)

			except Exception as e:
				data1 = "Error..."

		return render(request, 'add_stock.html', {'ticker': ticker, 'output': output})
	

def delete(request, stock_id):
 	item = Stock.objects.get(pk=stock_id)
 	item.delete()
 	messages.success(request, "Stock has been deleted!")
 	return redirect('add_stock')


def about(request):
	return render(request, 'about.html', {})	