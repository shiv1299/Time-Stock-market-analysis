"""
Django views - lightweight interface layer.
All Data Science logic lives in data_science package.
"""

from django.shortcuts import render, redirect
from django.http import Http404


from data_science.analyzer import analyze_stock


def landing_page(request):
    """Landing page with search. Redirects to company page on POST."""
    if request.method == 'POST':
        symbol = (request.POST.get('symbol') or '').strip().upper()
        if symbol != '':
            return redirect('company_dashboard', symbol=symbol)

    return render(request, 'dashboard/landing.html')


def company_dashboard(request, symbol):
    """Company dashboard - fetches data via analyzer and renders results."""
    print("======================")
    print("SYMBOL RECEIVED:", symbol)
    print("======================")
    
    result = analyze_stock(symbol)

    print("ANALYZER RESULT:", result)

    if result is None:
        raise Http404("Stock not found or data unavailable.")

    return render(request, 'dashboard/company.html', {'data': result})