import urllib2
from BeautifulSoup import BeautifulSoup
# or if you're using BeautifulSoup4:
# from bs4 import BeautifulSoup
SEMESTER_BY_SUBJECT = "http://www.csulb.edu/depts/enrollment/registration/class_schedule/Spring_2014/By_Subject"
def get_all_department_URLs():
	soup = BeautifulSoup(urllib2.urlopen(SEMESTER_BY_SUBJECT).read())
	departmentURLs = [];
	
	departmentList = soup('div', {'class': 'indexList'})[0];
	links = departmentList.findAll('a');
	for link in links:
		href = link.get('href');
		if href and not href == "#":
			departmentURLs.append(SEMESTER_BY_SUBJECT+"/"+href);
	return departmentURLs
	

def load_classes(url):
	soup = BeautifulSoup(urllib2.urlopen(url).read())
	headers = soup.findAll('div', {'class':'courseHeader'});
	classes = []
	for header in headers:
		courseCode = header.find('span', {'class':'courseCode'}).getText()
		courseTitle = header.find('span', {'class':'courseTitle'}).getText();
		classes.append(courseCode+": "+courseTitle);
	return classes;

departmentClassLists = get_all_department_URLs();
for departmentClassListURL in departmentClassLists:
	parsedDept = False;	
	while not parsedDept:
		try:
			classList = load_classes(departmentClassListURL);
			for className in classList:
				print className
			parsedDept = True;
		except:pass	
