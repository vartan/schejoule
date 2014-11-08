import urllib2
import urllib
import json
baseURL = "http://www.ratemyprofessors.com/find/professor/?department=&institution=California+State+University+Long+Beach&queryoption=TEACHER&queryBy=teacherName&sid=162&query="
def get_professor_data(name, start=0):
	#try:
		if(len(name) <= 2):
			return;
		if start:
			print "### Now on page "+str(1+ start)+" ###"
		matches = [];
		names = name.split(" ");
		firstInitial = "notfound"
		
		if len(names) > 1 and len(names[1])>0:
			firstInitial = names[1].lower()[0];
		lastName = names[0]
		searchTerm = lastName
		response = urllib2.urlopen(baseURL+urllib.quote_plus(searchTerm)+"&page="+str(start+1))
		data = json.load(response)   
		allTeachers = data["professors"]
		for teacher in allTeachers:
			if teacher["tFname"].lower().startswith(firstInitial) and teacher['tLname'].lower().split(" ")[0] == lastName.lower():
				prof_data = {}
				prof_data["department"] = 		teacher["tDept"];
				prof_data["name"] = 			teacher["tFname"] + " " + teacher["tLname"]
				prof_data["totalRatings"] = 	teacher["tNumRatings"]
				prof_data["averageRating"] = 	teacher["overall_rating"]
				#prof_data["averageHelfpul"] =	teacher["averagehelpfulscore_rf"]
				#prof_data["averageClarity"] = 	teacher["averageclarityscore_rf"]
				#prof_data["averageEasy"] =		teacher["averageeasyscore_rf"]
				#prof_data["averageHot"] = 		teacher["averagehotscore_rf"]
				prof_data["rmp_id"] = 			teacher["tid"]
				matches.append(prof_data);
				print prof_data
		if data["remaining"]>0 and data["remaining"]< 400:
			matches = matches + (get_professor_data(name, start+1)) # traverse pages
		return matches
	#except:
	#	print "Error when finding "+name	

	

class_data = open("classes.json")

classes = json.load(class_data)

all_professors = {}
for courseName in classes:
	course = classes[courseName]
	for sectionNumber in course["Sections"]:
		section = course["Sections"][sectionNumber]
		if section["Instructor"].lower() == "staff":
			continue
		if section["Instructor"] not in all_professors :
			newProfessor = get_professor_data(section["Instructor"]);
			all_professors[section["Instructor"]] = newProfessor;
			print newProfessor;
		else:
			print section["Instructor"] + " already recorded."

professorsFile = open("professors.json", "w")
professorsFile.write(json.dumps(all_professors,separators=(',',':')))
professorsFile.close()
