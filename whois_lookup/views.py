from django.shortcuts import render
import whois
from datetime import datetime

def lookup(request):
    domain_info = None
    error = None
    if request.method == 'POST':
        domain = request.POST.get('domain')
        try:
            w = whois.whois(domain)
            
            def format_date(date_value):
                if isinstance(date_value, list):
                    return [d.strftime('%Y-%m-%d %H:%M:%S') for d in date_value if isinstance(d, datetime)]
                if isinstance(date_value, datetime):
                    return date_value.strftime('%Y-%m-%d %H:%M:%S')
                return date_value

            domain_info = {
                'domain_name': w.domain_name,
                'registrar': w.registrar,
                'updated_date': format_date(w.updated_date),
                'creation_date': format_date(w.creation_date),
                'expiration_date': format_date(w.expiration_date),
                'emails': w.emails,
                'name': w.name,
                'org': w.org,
                'address': w.address,
                'city': w.city,
                'state': w.state,
                'registrant_postal_code': w.zipcode,
                'country': w.country,
            }
        except Exception as e:
            error = f"Error fetching data: {str(e)}"
    return render(request, 'whois_lookup/lookup.html', {'domain_info': domain_info, 'error': error})
