import urllib2
import urllib
import json
baseURL = "http://www.ratemyprofessors.com/solr/interim.jsp?select?rows=20&json.nl=map&wt=json&q="
def get_professor_data(name, start=0):
	try:
		if start:
			print "### Now on page "+str(1+ start/20)+" ###"
		matches = [];
		names = name.split(" ");
		firstInitial = "notfound"
		
		if len(names) > 1 and len(names[1])>0:
			firstInitial = names[1].lower()[0];
		lastName = names[0]
		searchTerm = "California State University Long Beach " + lastName 
		response = urllib2.urlopen(baseURL+urllib.quote_plus(searchTerm)+"&start="+str(start))
		data = json.load(response)   
		allTeachers = data["response"]["docs"]
		for teacher in allTeachers:
			if teacher["teacherfullname_s"].lower().startswith(firstInitial):
				prof_data = {}
				prof_data["department"] = 		teacher["teacherdepartment_s"];
				prof_data["name"] = 			teacher["teacherfullname_s"]
				prof_data["totalRatings"] = 	teacher["total_number_of_ratings_i"]
				prof_data["averageRating"] = 	teacher["averageratingscore_rf"]
				prof_data["averageHelfpul"] =	teacher["averagehelpfulscore_rf"]
				prof_data["averageClarity"] = 	teacher["averageclarityscore_rf"]
				prof_data["averageEasy"] =		teacher["averageeasyscore_rf"]
				prof_data["averageHot"] = 		teacher["averagehotscore_rf"]
				prof_data["rmp_id"] = 			teacher["pk_id"]
				matches.append(prof_data);
				print prof_data
		if data["response"]["numFound"]>start+20:
			matches = matches + (get_professor_data(name, start+20)) # traverse pages
		return matches
	except:
		print "Error when finding "+name	
	
	

class_data = open("classes.json")

classes = json.load(class_data)

all_professors = {}
for courseName in classes:
	course = classes[courseName]
	for sectionNumber in course["Sections"]:
		section = course["Sections"][sectionNumber]
		if section["Instructor"].lower() == "staff":
			continue
		if section["Instructor"] not in all_professors:
			all_professors[section["Instructor"]] = get_professor_data(section["Instructor"]);
		else:
			print section["Instructor"] + " already recorded."
professorsFile = open("professors.json", "w")
professorsFile.write(json.dumps(all_professors,separators=(',',':')))
professorsFile.close()
