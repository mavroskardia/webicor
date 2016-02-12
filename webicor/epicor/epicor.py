from suds.client import Client
from suds.transport.https import WindowsHttpAuthenticated


class Epicor:

	def __init__(self, username, password):		
		self.time_ntlm = WindowsHttpAuthenticated(username=username, password=password)
		self.timeclient = Client('http://epicor/e4se/Time.asmx?wsdl', transport=self.time_ntlm)

		self.psa_ntlm = WindowsHttpAuthenticated(username=username, password=password)
		self.psaclient = Client('http://epicor/e4se/PSAClientHelper.asmx?wsdl', transport=self.psa_ntlm)

		self.criteria_doc_template = '<ProjectTreeCriteriaDoc><SearchCriteria><TimeExpenseTreeType>T</TimeExpenseTreeType><DisplayTreeType>S</DisplayTreeType><ResourceID>{resourceid}</ResourceID><ResourceSiteURN>E4SE</ResourceSiteURN><CustomerID></CustomerID><OpportunityOnlyCode></OpportunityOnlyCode><ProjectCodes></ProjectCodes><ProjectGroupCode></ProjectGroupCode><OrganizationID></OrganizationID><TaskSeqIDs/><WorkloadCode></WorkloadCode><SiteURN>E4SE</SiteURN><FavoritesTree>0</FavoritesTree><InternalTree>1</InternalTree><CustomTree>1</CustomTree><ResourceCategoryList>\'3\'</ResourceCategoryList><FromDate>{fromdate}</FromDate><ToDate>{todate}</ToDate></SearchCriteria></ProjectTreeCriteriaDoc>'

	def get_allocations(self, fromdate, todate):
		'Returns the list of allocations'
		allocations = self.psaclient.service.GetNavigator(self.criteria_doc_template.format(
			resourceid=self.psa_ntlm.options.username, fromdate=fromdate.isoformat(), todate=todate.isoformat()))
		return allocations.TreeDocument.Node

	def get_time_entries(self, fromdate, todate, foruser=None):
		'Returns the list of time entries between "fromdate" and "todate"'
		entries = self.timeclient.service.GetAllTimeEntries(foruser or self.time_ntlm.options.username, fromdate, todate, fromdate, todate)
		try:
			return entries.TimeList.Time
		except:
			return None

if __name__ == '__main__':

	import argparse 
	import datetime

	from six.moves import input
	from getpass import getpass

	from epicor import Epicor

	parser = argparse.ArgumentParser()
	parser.add_argument('-u', '--username')
	parser.add_argument('-p', '--password')
	
	args = parser.parse_args()

	username = args.username or input('username: ')
	password = args.password or getpass('password: ')

	epicor = Epicor(username, password)

	now = datetime.datetime.now()
	fom = datetime.datetime(now.year, now.month, 1)
	lom = datetime.datetime(now.year, now.month + 1, 1) - datetime.timedelta(1)
	fow = datetime.datetime(now.year, now.month, now.day - now.weekday())
	low = fow + datetime.timedelta(7)	
	
	if not hasattr(args, 'command'):
		setattr(args, 'command', 'debug')

	if args.command == 'debug':
		import pdb; pdb.set_trace()
	elif args.command == 'entries':		
		for e in epicor.get_time_entries(fom, lom):
			print('{}\t{}\t{} hours\t{}'.format(e.ProjectName, e.TimeEntryDate, e.StandardHours, e.WorkComment))
	elif args.command == 'allocations':
		for a in epicor.get_allocations(fow, low):
			if not hasattr(a, 'Data'):
				continue
			if a.NodeType.startswith('Internal'):
				print('<Internal>\t{}'.format(a.Data.ActivityCode))
			elif a.NodeType == 'Task':
				print('<{}>\t{}'.format(a.Data.ProjectCode, a.Data.TaskName))

