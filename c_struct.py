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

def __get_size_of(data_type):
	if data_type == "INT32":
		return "sizeof(int)"
	if data_type == "UINT32":
		return "sizeof(unsigned int)"
	if data_type == "IPV4ADDRESS":
		return "16"
	if data_type == "FLOAT":
		return "sizeof(float)"
	if data_type == "DOUBLE":
		return "sizeof(double)"
	if data_type == "LONG":
		return "sizeof(long)"
	if data_type == "CHAR" or data_type == "CHARARRAY":
		return "sizeof(char)"
	else:
		return "Invalid"

def __get_c_datatype(data_type):
	if data_type == "INT32":
		return "int"
	if data_type == "UINT32":
		return "unsigned int"
	if data_type == "FLOAT":
		return "float"
	if data_type == "DOUBLE":
		return "double"
	if data_type == "LONG":
		return "long"
	if data_type == "CHAR" or data_type == "CHARARRAY":
		return "char"
	else:
		return "Invalid"
	
class c_structures:
	def __init__(self):
		self.struct_name = ""
		self.descrption = ""
		self.field_list = []
		self.ext_references_complete = []
		self.ext_references_incomplete = []

	def __del__(self):
		class_name = self.__class__.__name__

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
			print "	external references complete:"
		for ext_ref in self.ext_references_complete:
			print "		ext ref c: " + ext_ref
			print " external references incomplete:"
		for ext_ref in self.ext_references_incomplete:
			print "         ext ref inc: " + ext_ref


def __get_structure_external_references_list(c_struct_obj):
	ext_references_complete = []
	ext_references_incomplete = []
	
	for fields in c_struct_obj.field_list:
		fld_format = [None, None, None, None, None, None]
		fld_format[0] = fields.datatype
		fld_format[4] = fields.referredObject
		if fld_format[0] == "OBJECT" and fld_format[4] != c_struct_obj.struct_name:
			if fld_format[4] not in ext_references_incomplete:
				ext_references_incomplete.append(fld_format[4])

	for fields in c_struct_obj.field_list:
		fld_format = [None, None, None, None, None, None]
		fld_format[0] = fields.datatype
		fld_format[4] = fields.referredObject
		fld_format[1] = fields.isptr
		if fld_format[0] == "OBJECT" and fld_format[4] != c_struct_obj.struct_name and fld_format[1] != "true":
			if fld_format[4] not in ext_references_complete:
				ext_references_complete.append(fld_format[4])
				ext_references_incomplete.remove(fld_format[4])
	c_struct_obj.ext_references_complete = ext_references_complete
	c_struct_obj.ext_references_incomplete = ext_references_incomplete

		

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
				fld_obj.isptr = "false"
	
			if _field.hasAttribute("vector"):
				fld_obj.vector = _field.getAttribute("vector")
			else:
				fld_obj.vector = "false"
	
			if _field.hasAttribute("cDataArraySize"):
				fld_obj.cDataArraySize = _field.getAttribute("cDataArraySize")
			else:
				fld_obj.cDataArraySize = None

			fld_list.append(fld_obj)
			
		c_struct_obj.field_list = fld_list		
		__get_structure_external_references_list (c_struct_obj)

		c_struct_obj_list.append(c_struct_obj)

	return c_struct_obj_list


def write_field_format(target_file, fld_format, parent_struct_name):

	tab="	"
	if parent_struct_name == fld_format[4]:
		obj_dtype = "struct _" + parent_struct_name + "_"
	else:
		obj_dtype = fld_format[4]

	if fld_format[0] != "OBJECT" and fld_format[1] == "false" and fld_format[5] != None and fld_format[3] == "false":
		# int p[25]  serialize_string(b, obj->p, sizeof(int) * arr_size)
		target_file.write(tab + __get_c_datatype(fld_format[0]) + " " + fld_format[2] + "[" + fld_format[5] + "];\n")
	elif fld_format[0] != "OBJECT" and fld_format[1] == "false" and fld_format[5] == None and fld_format[3] == "false":
		# int p	     serialize_string(b, &obj->p,sizeof(int))	
		target_file.write(tab + __get_c_datatype(fld_format[0]) + " " + fld_format[2] + ";\n")
	elif fld_format[0] != "OBJECT" and fld_format[1] == "true" and fld_format[5] == None and fld_format[3] == "false":
		#int *p	     serialize_string(b, obj->p, sizeof(int))
		target_file.write(tab + __get_c_datatype(fld_format[0]) + " * " + fld_format[2] + ";\n")
	elif fld_format[0] != "OBJECT" and fld_format[1] == "true" and fld_format[5] == None and fld_format[3] == "true":
		#p_count = 0; int *p
		target_file.write(tab + "unsigned int " + fld_format[2] + "_count;\n")
		target_file.write(tab + __get_c_datatype(fld_format[0]) + " * " + fld_format[2] + ";\n")
	elif fld_format[0] != "OBJECT" and fld_format[1] == "true" and fld_format[5] != None and fld_format[3] == "false":
		# int *p[25]
		target_file.write(tab + __get_c_datatype(fld_format[0]) + " * " + fld_format[2] + "[" + fld_format[5] + "];\n")
	elif fld_format[0] == "OBJECT" and fld_format[1] == "false" and fld_format[5] != None and fld_format[3] == "false":
		# person_t p[25] 
		target_file.write(tab + obj_dtype + " " + fld_format[2] + "[" + fld_format[5] + "];\n")
	elif fld_format[0] == "OBJECT" and fld_format[1] == "true" and fld_format[5] == None and fld_format[3] == "true":
		# person_t *p with vector
		target_file.write(tab + "unsigned int " + fld_format[2] + "_count;\n")
		target_file.write(tab + obj_dtype + " * " + fld_format[2] + ";\n")
	elif fld_format[0] == "OBJECT" and fld_format[1] == "false" and fld_format[5] == None and fld_format[3] == "false":
		# person_t p
		target_file.write(tab + obj_dtype + " " + fld_format[2] + ";\n")
	elif fld_format[0] == "OBJECT" and fld_format[1] == "true" and fld_format[5] == None and fld_format[3] == "false":
		# person_t *p
		target_file.write(tab + obj_dtype + " * " + fld_format[2] + ";\n")
	elif fld_format[0] == "OBJECT" and fld_format[1] == "true" and fld_format[5] != None and fld_format[3] == "false":
		# person_t *p[25]
		target_file.write(tab + obj_dtype + " * " + fld_format[2] + "[" + fld_format[5] + "];\n")
	else:
		print fld_format[2] + " mis hit3 "

def convert_xml_to_c_structures(xml_file_name, dir_path_name, c_struct_obj_list):
	for c_struct_obj in c_struct_obj_list:
		target = open(dir_path_name+"/"+c_struct_obj.struct_name+".h", 'w')
		target.write("#ifndef __" + c_struct_obj.struct_name + "__\n")
		target.write("#define __" + c_struct_obj.struct_name + "__\n")
		
		target.write("\n\n")
		#target.write("typedef struct _" + c_struct_obj.struct_name + " " + c_struct_obj.struct_name + ";\n")
		for ext_ref in c_struct_obj.ext_references_incomplete:
			target.write("typedef struct _" + ext_ref + "_" + " " + ext_ref + ";\n\n\n")
		for ext_ref in c_struct_obj.ext_references_complete:
			target.write("#include \"" + ext_ref + ".h\"\n")

		target.write("\ntypedef struct _" + c_struct_obj.struct_name + "_ {\n")
		
		fld_format = [None, None, None, None, None, None]
		# dtype, is ptr, identier name, Array_size, isVector
		for fields in c_struct_obj.field_list:
			fld_format[0] = fields.datatype
			fld_format[1] = fields.isptr 
			fld_format[2] = fields.field_name
			fld_format[3] = fields.vector
			fld_format[4] = fields.referredObject
			fld_format[5] = fields.cDataArraySize
			write_field_format(target, fld_format, c_struct_obj.struct_name)
		target.write("} " + c_struct_obj.struct_name + ";\n")
		target.write("\n\n#endif")
		target.close()

def print_field(fields):
	print "field.datatype = " + fields.datatype
	print "fields.isptr " + fields.isptr
	print "fields.field_name = " + fields.field_name
	if fields.vector == None:
		print "fields.vector = None"
	else:
		print "fields.vector = "+ fields.vector
	if fields.referredObject == None:
		print "fields.referredObject = None"
	else:
		print "fields.referredObject = "+ fields.referredObject
	if fields.cDataArraySize == None:
		print "fields.cDataArraySize = None"
	else:
		print "fields.cDataArraySize = "+ fields.cDataArraySize
	
def serialize_structure(c_struct_obj, dir_path):
	target_h = open(dir_path + "/"+c_struct_obj.struct_name+"_xdr_serialize.h", 'w')
	target_c = open(dir_path + "/"+c_struct_obj.struct_name+"_xdr_serialize.c", 'w')
	# generate header file
	target_h.write("#ifndef __" + c_struct_obj.struct_name + "_xdr_serialize__\n")	
	target_h.write("#define __" + c_struct_obj.struct_name + "_xdr_serialize__\n")
	target_h.write("\n")
	target_h.write("typedef struct _" + c_struct_obj.struct_name + "_ " + c_struct_obj.struct_name + ";\n")
	target_h.write("#include \"serialize.h\"\n")
	target_h.write("\n\n")
	target_h.write("void \n" + c_struct_obj.struct_name + "_xdr_serialize(" + c_struct_obj.struct_name + " *obj, ser_buff_t *b);")

	#generate C file now
	
	#target_c.write("#include \"serialize.h\"\n")
	target_c.write("#include <stdlib.h>\n")
	target_c.write("#include <memory.h>\n")
	target_c.write("#include \"" + c_struct_obj.struct_name + ".h\"\n")
	target_c.write("#include \"" + c_struct_obj.struct_name + "_xdr_serialize.h\"\n")

	for ext_ref in c_struct_obj.ext_references_complete:
        	#target_c.write("#include \"" + ext_ref + ".h\"\n")
		target_c.write("#include \"" + ext_ref + "_xdr_serialize.h\"\n")

	for ext_ref in c_struct_obj.ext_references_incomplete:
        	#target_c.write("#include \"" + ext_ref + ".h\"\n")
		target_c.write("#include \"" + ext_ref + "_xdr_serialize.h\"\n")
	
	# loop_var is required when atleat when field of the structure is vector
	for fields in c_struct_obj.field_list:
		if fields.vector == "true":
			target_c.write("\nstatic unsigned int loop_var = 0;\n\n")
			break

	target_c.write("\n\n")
	target_c.write("void \n" + c_struct_obj.struct_name + "_xdr_serialize(" + c_struct_obj.struct_name + " *obj, ser_buff_t *b){\n")
	tab = "	"
	target_c.write(tab)
	target_c.write("if(!obj){\n")
	target_c.write(tab + tab)
	target_c.write("serialize_int32(b, NON_EXISTING_STRUCT);\n")
	target_c.write(tab + tab)
	target_c.write("return;\n")
	target_c.write(tab)
	target_c.write("}\n")
	
	for fields in c_struct_obj.field_list:
		fld_format = [None, None, None, None, None, None]
		fld_format[0] = fields.datatype
		fld_format[1] = fields.isptr 
		fld_format[2] = fields.field_name
		fld_format[3] = fields.vector
		fld_format[4] = fields.referredObject
		fld_format[5] = fields.cDataArraySize

		#print_field(fields)
		target_c.write(tab)
		
		if fld_format[0] != "OBJECT" and fld_format[1] == "false" and fld_format[5] != None and fld_format[3] == "false":
			# int p[25]  serialize_string(b, obj->p, sizeof(int) * arr_size)
			target_c.write("serialize_string(b, (char *)obj->" + fld_format[2] + ", " + __get_size_of(fld_format[0]) + "*" + fld_format[5] + ");\n")		
		elif fld_format[0] != "OBJECT" and fld_format[1] == "false" and fld_format[5] == None and fld_format[3] == "false":
			# int p	     serialize_string(b, &obj->p,sizeof(int))	
			target_c.write("serialize_string(b, (char *)&obj->" + fld_format[2] + ", " + __get_size_of(fld_format[0]) + ");\n")
		elif fld_format[0] != "OBJECT" and fld_format[1] == "true" and fld_format[5] == None and fld_format[3] == "false":
			#int *p	     serialize_string(b, obj->p, sizeof(int))
			target_c.write("serialize_string(b, (char *)obj->" + fld_format[2] + ", " + __get_size_of(fld_format[0]) + ");\n")
		elif fld_format[0] != "OBJECT" and fld_format[1] == "true" and fld_format[5] == None and fld_format[3] == "true":
			#p_count = 0; int *p
			target_c.write("serialize_string(b, (char *)&obj->" + fld_format[2] + "_count, sizeof(unsigned int));\n")
			target_c.write(tab)
			target_c.write("for (loop_var = 0; loop_var < " + "obj->" + fld_format[2] + "_count ; loop_var ++)\n")
			target_c.write(tab + tab)
			target_c.write("serialize_string(b, (char *)(obj->" + fld_format[2] + " + loop_var), " + __get_size_of(fld_format[0]) + ");\n")
		elif fld_format[0] != "OBJECT" and fld_format[1] == "true" and fld_format[5] != None and fld_format[3] == "false":
			# int *p[25]	
			target_c.write("for (loop_var = 0; loop_var < " + fld_format[5] + "; loop_var++){\n")
			target_c.write(tab + tab)
			target_c.write("serialize_string(b, (char *)obj->" + fld_format[2] + "[loop_var], " + __get_size_of(fld_format[0]) + ");\n")
			target_c.write(tab)
			target_c.write("}\n")
		elif fld_format[0] == "OBJECT" and fld_format[1] == "false" and fld_format[5] != None and fld_format[3] == "false":
			# person_t p[25] 
			target_c.write("for (loop_var = 0; loop_var < " + fld_format[5] + "; loop_var++){\n")
			target_c.write(tab + tab) 
			target_c.write(fld_format[4] + "_xdr_serialize(&obj->" +  fld_format[2] + "[loop_var], b);\n") 	
			target_c.write(tab)
			target_c.write("}\n")
		elif fld_format[0] == "OBJECT" and fld_format[1] == "true" and fld_format[5] == None and fld_format[3] == "true":
			# person_t *p with vector
			target_c.write("serialize_string(b, (char *)&obj->" + fld_format[2] + "_count, sizeof(unsigned int));\n")
			target_c.write(tab)
			target_c.write("for (loop_var = 0; loop_var < " + "obj->" + fld_format[2] + "_count ; loop_var ++){\n")
			target_c.write(tab + tab)
			target_c.write(fld_format[4] + "_xdr_serialize(obj->" + fld_format[2] + " + loop_var, b);\n")
			target_c.write(tab)
			target_c.write("}\n")
		elif fld_format[0] == "OBJECT" and fld_format[1] == "false" and fld_format[5] == None and fld_format[3] == "false":
			# person_t p
			target_c.write(fld_format[4] + "_xdr_serialize(&obj->" + fld_format[2] + " , b);\n")
		elif fld_format[0] == "OBJECT" and fld_format[1] == "true" and fld_format[5] == None and fld_format[3] == "false":
			# person_t *p
			target_c.write(fld_format[4] + "_xdr_serialize(obj->" + fld_format[2] + " , b);\n")
		elif fld_format[0] == "OBJECT" and fld_format[1] == "true" and fld_format[5] != None and fld_format[3] == "false":
			# person_t *p[25]
			target_c.write("for (loop_var = 0; loop_var < " + fld_format[5] + "; loop_var++){\n")
			target_c.write(tab + tab)
			target_c.write(fld_format[4] + "_xdr_serialize(obj->" +  fld_format[2] + "[loop_var], b);\n")
			target_c.write(tab)
			target_c.write("}\n")
		else:
			print fld_format[2] + " mis hit2 "
	target_c.write("}")
	target_h.close()
	target_c.close()

def deserialize_structure(c_struct_obj, dir_path):
	target_h = open(dir_path + "/"+c_struct_obj.struct_name+"_xdr_serialize.h", 'a')

	# writing header file
	target_h.write("\n\n")
	target_h.write(c_struct_obj.struct_name +" *\n" + c_struct_obj.struct_name + "_xdr_deserialize(ser_buff_t *b);\n")
	target_h.write("\n\n#endif")
	target_h.close()

	# writing C file
	target_c = open(dir_path + "/"+c_struct_obj.struct_name+"_xdr_serialize.c", 'a')
	target_c.write("\n\n")
	target_c.write(c_struct_obj.struct_name +" *\n" + c_struct_obj.struct_name + "_xdr_deserialize(ser_buff_t *b){\n")
	tab = "	"
	target_c.write("\n")
	target_c.write(tab + "int check_existence;\n")
	target_c.write(tab + "de_serialize_string((char *)&check_existence, b, sizeof(int));\n")
	target_c.write(tab + "if(check_existence == NON_EXISTING_STRUCT){\n")
	target_c.write(tab + tab + "return NULL;\n")
	target_c.write(tab + "}\n")
	target_c.write(tab + "serialize_buffer_skip(b, -1*sizeof(int));\n")
	
	target_c.write("\n" + tab)
	target_c.write(c_struct_obj.struct_name + " *obj = calloc(1, sizeof(" + c_struct_obj.struct_name + "));\n")

	for fields in c_struct_obj.field_list:
		fld_format = [None, None, None, None, None, None]
		fld_format[0] = fields.datatype
		fld_format[1] = fields.isptr 
		fld_format[2] = fields.field_name
		fld_format[3] = fields.vector
		fld_format[4] = fields.referredObject
		fld_format[5] = fields.cDataArraySize

		#print_field(fields)
		target_c.write(tab)
		
		if fld_format[0] != "OBJECT" and fld_format[1] == "false" and fld_format[5] != None and fld_format[3] == "false":
			# int p[25]  de_serialize_string(obj->p, b, sizeof(int) * arr_size)
			target_c.write("de_serialize_string((char *)obj->" + fld_format[2] + ", b, " + __get_size_of(fld_format[0]) + "*" + fld_format[5] + ");\n")		
		elif fld_format[0] != "OBJECT" and fld_format[1] == "false" and fld_format[5] == None and fld_format[3] == "false":
			# int p	     de_serialize_string((char *)&obj->p, b, sizeof(int))	
			target_c.write("de_serialize_string((char *)&obj->" + fld_format[2] + ", b, " + __get_size_of(fld_format[0]) + ");\n")
		elif fld_format[0] != "OBJECT" and fld_format[1] == "true" and fld_format[5] == None and fld_format[3] == "false":
			#int *p	     serialize_string((char *)obj->p, b , sizeof(int))
			target_c.write("de_serialize_string((char *)obj->" + fld_format[2] + ", b, " + __get_size_of(fld_format[0]) + ");\n")
		elif fld_format[0] != "OBJECT" and fld_format[1] == "true" and fld_format[5] == None and fld_format[3] == "true":
			#p_count = 0; int *p
			target_c.write("de_serialize_string((char *)&obj->" + fld_format[2] + "_count, b, sizeof(unsigned int));\n")
			target_c.write(tab)
			target_c.write("obj->" + fld_format[2] + " = calloc(" + __get_size_of(fld_format[0]) + ", obj->" + fld_format[2] + "_count);\n")
			target_c.write(tab)
			target_c.write("for (loop_var = 0; loop_var < obj->" + fld_format[2] + "_count; " + " loop_var++){\n")
			target_c.write(tab + tab)
			target_c.write("de_serialize_string((char *)(obj->" + fld_format[2] + " + loop_var), b, " + __get_size_of(fld_format[0]) + ");\n")
			target_c.write(tab)
			target_c.write("}\n")
		elif fld_format[0] != "OBJECT" and fld_format[1] == "true" and fld_format[5] != None and fld_format[3] == "false":
			# int *p[25]	
			target_c.write("for (loop_var = 0; loop_var < " + fld_format[5] + "; loop_var++)\n")
			target_c.write(tab + tab)
			target_c.write("obj->" + fld_format[2] + "[loop_var] = calloc ( 1, " + __get_size_of(fld_format[0]) + ");\n") 
			target_c.write(tab)
			target_c.write("for (loop_var = 0; loop_var < " + fld_format[5] + "; loop_var++)\n")
			target_c.write(tab + tab)
			target_c.write("de_serialize_string((char *)(obj->" + fld_format[2] + "[loop_var]), b, " + __get_size_of(fld_format[0]) + ");\n")
		elif fld_format[0] == "OBJECT" and fld_format[1] == "false" and fld_format[5] != None and fld_format[3] == "false":
			# person_t p[25] 
			target_c.write("for (loop_var = 0; loop_var < " + fld_format[5] + "; loop_var++){\n")
			target_c.write(tab + tab) 
			target_c.write("obj->" + fld_format[2] + "[loop_var] = *" + fld_format[4] + "_xdr_deserialize(b);\n") 	
			target_c.write(tab)
			target_c.write("}\n")
		elif fld_format[0] == "OBJECT" and fld_format[1] == "true" and fld_format[5] == None and fld_format[3] == "true":
			# person_t *p with vector
			target_c.write("de_serialize_string((char *)&obj->" + fld_format[2] + "_count, b, sizeof(unsigned int));\n")
			target_c.write(tab)
			target_c.write("obj->"+ fld_format[2] + " = calloc (obj->" + fld_format[2] + "_count, sizeof(" + fld_format[4] + "));\n")
			target_c.write(tab)
			target_c.write("for (loop_var = 0; loop_var < " + "obj->" + fld_format[2] + "_count ; loop_var ++){\n")
			target_c.write(tab + tab)
			target_c.write(fld_format[4] + " *constructed_obj = " + fld_format[4] + "_xdr_deserialize(b);\n")
			target_c.write(tab + tab)
			target_c.write("memcpy(obj->" + fld_format[2] + " + loop_var, constructed_obj, sizeof(" + fld_format[4]  + "));\n")
			target_c.write(tab + tab)
			target_c.write("free(constructed_obj);\n")
			target_c.write(tab)
			target_c.write("}\n")
		elif fld_format[0] == "OBJECT" and fld_format[1] == "false" and fld_format[5] == None and fld_format[3] == "false":
			# person_t p
			target_c.write("obj->" + fld_format[2] + " = *" + fld_format[4] + "_xdr_deserialize(b);\n")
		elif fld_format[0] == "OBJECT" and fld_format[1] == "true" and fld_format[5] == None and fld_format[3] == "false":
			# person_t *p
			target_c.write("obj->" + fld_format[2] + " = " + fld_format[4] + "_xdr_deserialize(b);\n")
		elif fld_format[0] == "OBJECT" and fld_format[1] == "true" and fld_format[5] != None and fld_format[3] == "false":
			# person_t *p[25]
			target_c.write("for (loop_var = 0; loop_var < " + fld_format[5] + "; loop_var++){\n")
			target_c.write(tab + tab)
			target_c.write("obj->" + fld_format[2] + "[loop_var] = " + fld_format[4] + "_xdr_deserialize(b);\n")
			target_c.write(tab)
			target_c.write("}\n")
		else:
			print fld_format[2] + " mis hit1"
	target_c.write(tab)
	target_c.write("return obj;\n")
	target_c.write("}")
	target_c.close()
	return

def generate_copy_fn(c_struct_obj, dir_path):
	target_h = open(dir_path + "/"+c_struct_obj.struct_name+"_xdr_serialize.h", 'a')
	target_c = open(dir_path + "/"+c_struct_obj.struct_name+"_xdr_serialize.c", 'a')
	target_h.close()
	target_c.close()
	return

def generate_is_similar_fn(c_struct_obj, dir_path):
	target_h = open(dir_path + "/"+c_struct_obj.struct_name+"_xdr_serialize.h", 'a')
	target_c = open(dir_path + "/"+c_struct_obj.struct_name+"_xdr_serialize.c", 'a')
	target_h.close()
	target_c.close()
	return

def generate_free_fn(c_struct_obj, dir_path):
	target_h = open(dir_path + "/"+c_struct_obj.struct_name+"_xdr_serialize.h", 'a')
	target_c = open(dir_path + "/"+c_struct_obj.struct_name+"_xdr_serialize.c", 'a')
	target_h.close()
	target_c.close()
	return


if __name__ == "__main__":
	xml_file_name = "c_struct.xml" 
	c_struct_obj_list =  build_structure_list_from_xml(xml_file_name)
	convert_xml_to_c_structures(xml_file_name, ".", c_struct_obj_list)
	for c_struct_obj in c_struct_obj_list:
		serialize_structure(c_struct_obj, ".")
		deserialize_structure(c_struct_obj, ".")
