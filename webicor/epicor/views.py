from django.http import JsonResponse, HttpResponse
from django.shortcuts import render

import iso8601
from epicor import Epicor

def test(req):
	return HttpResponse('working')

def entries(req):
	if req.method != 'POST':
		return HttpResonse('NO')

	username = req.POST['username']
	password = req.POST['password']
	foruser = req.POST.get('foruser', username)
	fromdate = req.POST.get('fromdate', '2016-01-01T12:00:00')
	todate = req.POST.get('todate', '2016-01-31T12:00:00')

	fromdate = iso8601.parse_date(fromdate)
	todate = iso8601.parse_date(todate)

	entries = Epicor(username, password).get_time_entries(fromdate, todate, foruser)
	
	return JsonResponse(transform(entries))

def transform(entries):
	ret = { 'entries': [] }
	for e in entries:	
		entry = {}
		for attr in [a for a in dir(e) if not a.startswith('_')]:
			entry[attr] = getattr(e, attr)
		ret['entries'].append(entry)
	return ret