import urllib2
import json
import HTMLParser
import re
h = HTMLParser.HTMLParser()
from BeautifulSoup import BeautifulSoup
SEMESTER_BY_SUBJECT = ("http://www.csulb.edu/depts/enrollment/registration/"
					  "class_schedule/Spring_2015/By_Subject")

def get_all_department_URLs():
	"""Loads the list of classes page (SEMESTER_BY_SUBJECT)
	and loads each department URL from it. Returns an array of
	URLs"""
	
	# Load the subjects list page as text
	subjects_page = urllib2.urlopen(SEMESTER_BY_SUBJECT).read()
	# Feed html into BeautifulSoup to navigate html
	subjects_soup = BeautifulSoup(subjects_page)
	# List of department URLs to return
	departmentURLs = [];
	# The department list content is in a div element with the class "indexList"
	departmentList = subjects_soup('div', {'class': 'indexList'})[0];
	# Every link in the department list is a link to the department
	links = departmentList.findAll('a');

	for link in links:
		href = link.get('href'); # pull url from anchor link
		if href and not href == "#":
			departmentURLs.append(SEMESTER_BY_SUBJECT+"/"+href);

	return departmentURLs
	

def load_classes(url):
	"""loads the classes listed from the URL, returns a dictionary with
	the department's classes"""
	# Load the class list page as text
	department_page = urllib2.urlopen(url).read();
	# Feed html into BeautifulSoup to navigate html
	department_soup = BeautifulSoup(department_page)
	# Each course (DEPT ###) is in a div element with the class "courseBlock"
	classBlocks = department_soup.findAll('div', {'class':'courseBlock'});
	classList = {}
	for classBlock in classBlocks:
		# The course code is in a span element with the class "courseCode"
		courseCodeElement = classBlock.find('span', {'class':'courseCode'})
		courseCode = courseCodeElement.getText()
		# The course title is in a span element with the class "courseTitle"
		courseTitleElement = classBlock.find('span', {'class':'courseTitle'})
		courseTitle = h.unescape(courseTitleElement.getText());

		sections = {};

		thisCourse = {
			"Code": courseCode,
			"Title": courseTitle,
			"Sections": sections
		}	
		classList[courseCode+": "+courseTitle] = thisCourse;
		
		#Each "group" of classes is in a table.
		classTables = classBlock.findAll("table");
		for classTable in classTables:
			groupRows = classTable.findAll("tr");
			pastHeader = False
			labels = [
				"ID","Notes","Type",
				"Days","Time","Open",
				"Location","Instructor","Comment"
			];
			for sectionRow in groupRows[1:]:
				sectionInfo = sectionRow.findAll("td");
				sectionNum = sectionRow.find("th").getText()
				thisClass={};
				sections[sectionNum] = thisClass;
				for i in range(0, len(labels)):
					currentLabel = labels[i]
					thisSection = sectionInfo[i]
					if currentLabel=="Notes":
						continue;
					val=""
					if currentLabel=="Open":
						val = len(thisSection.findAll("img"))>0
					else:
						val = h.unescape(thisSection.getText().strip())
						# Remove extra whitespace in order to minimize json size
						re.sub("\s\s+" , " ", val)
					thisClass[labels[i]] = val;
				
	return classList;


departmentClassLists = get_all_department_URLs();
allClasses = {};
for departmentClassListURL in departmentClassLists:
	parsedDept = False;	
	while not parsedDept:
		try:
			# load new classes from department page
			added_classes = load_classes(departmentClassListURL);
			# add them to existing list of classes
			allClasses.update(added_classes);
			# print for user feedback
			print json.dumps(added_classes, indent=2);		
			# continue to next department
			parsedDept = True;
		except:
			print "ERROR WITH DEPARTMENT: "+departmentClassListURL
			pass
fo = open("classes.json", "w")
fo.write(json.dumps(allClasses,separators=(',',':')))
fo.close()

