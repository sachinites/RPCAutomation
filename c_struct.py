#!/usr/bin/python

from xml.dom.minidom import parse
import xml.dom.minidom

# Open XML document using minidom parser
DOMTree = xml.dom.minidom.parse("sample3.xml")
collection = DOMTree.documentElement

if collection.hasAttribute("name"):
	print "Root element : %s" % collection.getAttribute("name")

# Get all the C Structures in the collection
c_structures_collection = collection.getElementsByTagName("C_Structure")

# Print detail of each movie.
for c_struct in c_structures_collection:
	print "*****C_STRUCT*****"
   	if c_struct.hasAttribute("name"):
        	print "Name: %s" % c_struct.getAttribute("name")
	if c_struct.hasAttribute("description"):
		print "Description: %s" % c_struct.getAttribute("description")

	fields_collection = c_struct.getElementsByTagName("member")

	for field in fields_collection:
		if field.hasAttribute("name"):
			print "		field name %s" % field.getAttribute("name")

		if field.hasAttribute("dataType"):
			print "		field data type is %s" %field.getAttribute("dataType")


		if field.hasAttribute("description"):
			print "		field descriptionis %s" %field.getAttribute("description")

		if field.hasAttribute("referredObject"):
			print "		field referredObject %s" %field.getAttribute("referredObject")

		if field.hasAttribute("vector"):
			print "		field vector %s" %field.getAttribute("vector")

		if field.hasAttribute("cDataArraySize"):
			print "		field cDataArraySize %s" %field.getAttribute("cDataArraySize")

		print ""
			
