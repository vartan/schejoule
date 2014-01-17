import urllib2
import json
import HTMLParser
h = HTMLParser.HTMLParser()
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
	classBlocks = soup.findAll('div', {'class':'courseBlock'});
	classes = {}
	for classBlock in classBlocks:
		courseCode = classBlock.find('span', {'class':'courseCode'}).getText()
		courseTitle = h.unescape(classBlock.find('span', {'class':'courseTitle'}).getText())
		thisCourse = {};
		
		sections = {};
		classes[courseCode+": "+courseTitle] = thisCourse;
		thisCourse["Code"] = courseCode;
		thisCourse["Title"]= courseTitle;
		thisCourse["Sections"] = sections;
		classTables = classBlock.findAll("table");
		
		for classTable in classTables:
			groupRows = classTable.findAll("tr");
			pastHeader = False
			labels = ["ID","Notes","Type","Days","Time","Open","Location","Instructor","Comment"];
			for sectionRow in groupRows:
				sectionInfo = sectionRow.findAll("td");
				sectionNum = sectionRow.find("th").getText();
				thisClass={};
				if not pastHeader:
					pastHeader=True;
					continue
				for i in range(1, len(labels)):
					thisClass[labels[i]] = h.unescape(sectionInfo[i].getText())
				print sectionNum
				sections[sectionNum] = thisClass;
	return classes;
departmentClassLists = get_all_department_URLs();
allClasses = {};
for departmentClassListURL in departmentClassLists:
	parsedDept = False;	
	while not parsedDept:
		try:
			
			added_classes = load_classes(departmentClassListURL);
			allClasses.update(added_classes);
			print json.dumps(added_classes, indent=2);		
			parsedDept = True;
		except:pass
fo = open("classes.json", "w")
fo.write(json.dumps(allClasses,indent=2))
fo.close()
