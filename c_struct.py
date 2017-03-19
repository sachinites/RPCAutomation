#!/usr/bin/python

from xml.dom.minidom import parse
import xml.dom.minidom
import os,sys

# Open XML document using minidom parser

class field:
	def __init__(self):
		field_name = ""
		datatype = ""
		isptr=""
		desc = ""
		vector = ""
		cDataArraySize = ""
		referredObject =""

	def __del__(self):
		class_name = self.__class__.__name__
		print class_name, "destroyed"

class c_structures:
	def __init__(self):
		self.struct_name = ""
		self.descrption = ""
		self.field_list = []

	def __del__(self):
		class_name = self.__class__.__name__
		print class_name, "destroyed"

	def dump_struct(self):
		print "structure name = %s" %self.struct_name
		print "descrption =  %s" %self.descrption
		print "fields :"
		for fld in self.field_list:
			print "	name = %s" % fld.field_name
			print "	datatype = %s" % fld.datatype
			print "	desc = %s" % fld.desc
			print "	isptr = %s" % fld.isptr
			print "	cDataArraySize = %s" % fld.cDataArraySize
			print "	referredObject = %s" % fld.referredObject
			print "	vector = %s" % fld.vector
			print 

def build_structure_list_from_xml(xml_file_name):

	c_struct_obj_list = []	
	DOMTree = xml.dom.minidom.parse(xml_file_name)
	collection = DOMTree.documentElement

# Get all the C Structures in the collection
	c_structures_collection = collection.getElementsByTagName("C_Structure")

	for c_struct in c_structures_collection:
		c_struct_obj = c_structures ()
		c_struct_obj.struct_name = c_struct.getAttribute("name")
		c_struct_obj.descrption = c_struct.getAttribute("description")

		fld_list = []
	
		fields_collection = c_struct.getElementsByTagName("member")

		for _field in fields_collection:
			
			fld_obj = field ()
			
			if _field.hasAttribute("name"):
				fld_obj.field_name = _field.getAttribute("name")
	
			if _field.hasAttribute("dataType"):
				fld_obj.datatype = _field.getAttribute("dataType")
		
			if _field.hasAttribute("description"):
				fld_obj.desc = _field.getAttribute("description")

	
			if _field.hasAttribute("referredObject"):
				fld_obj.referredObject = _field.getAttribute("referredObject")
			else:
				fld_obj.referredObject = None
			
			if _field.hasAttribute("isPTR"):
				fld_obj.isptr = _field.getAttribute("isPTR")
			else:
				fld_obj.isptr = None
	
			if _field.hasAttribute("vector"):
				fld_obj.vector = _field.getAttribute("vector")
			else:
				fld_obj.vector = None
	
			if _field.hasAttribute("cDataArraySize"):
				fld_obj.cDataArraySize = _field.getAttribute("cDataArraySize")
			else:
				fld_obj.cDataArraySize = None

			fld_list.append(fld_obj)
			
		c_struct_obj.field_list = fld_list		
		c_struct_obj_list.append(c_struct_obj)

	return c_struct_obj_list


def write_field_format(target_file, fld_format):
	_str = "	"
	
	if fld_format[3] == "true":
		_str += "unsigned int " + fld_format[2] + "_count;\n	"
	
	
	if fld_format[0] == "INTEGER":
		_str += "int "
	elif fld_format[0] == "CHARARRAY":
		_str += "char "
	elif fld_format[0] == "OBJECT":
		_str += fld_format[4] + " "
	else:
		_str += "Error "

	if fld_format[1] == "true":
		_str += " * "

	_str += fld_format[2]

	if fld_format[5] != None:
		_str += "["+ fld_format[5] +"];\n"
	else:
		_str += ";\n"

	target_file.write(_str)		

def convert_xml_to_c_structures(xml_file_name, dir_path_name):
	c_struct_obj_list =  build_structure_list_from_xml(xml_file_name)
	for c_struct_obj in c_struct_obj_list:
		target = open(dir_path_name+"/"+c_struct_obj.struct_name+".h", 'w')
		target.write("#ifndef __" + c_struct_obj.struct_name + "__\n")
		target.write("#define __" + c_struct_obj.struct_name + "__\n")
		
		target.write("\n\n")
		target.write("typedef _" + c_struct_obj.struct_name + "_ {\n")
		
		fld_format = [None, None, None, None, None, None]
		# dtype, is ptr, identier name, Array_size, isVector
		for fields in c_struct_obj.field_list:
			fld_format[0] = fields.datatype
			fld_format[1] = fields.isptr 
			fld_format[2] = fields.field_name
			fld_format[3] = fields.vector
			fld_format[4] = fields.referredObject
			fld_format[5] = fields.cDataArraySize
			write_field_format(target, fld_format)
		target.write("} " + c_struct_obj.struct_name + ";\n")
		target.write("\n\n#endif")

if __name__ == "__main__":
	convert_xml_to_c_structures("c_struct.xml", ".")
