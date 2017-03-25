#!/usr/bin/python

from xml.dom.minidom import parse
import xml.dom.minidom
import os,sys

# Open XML document using minidom parser

class rpc:
	def __init__(self):
		rpc_name=""
		rpc_arg_list = []
		rpc_return_type=None

	def print_rpc(self):
		print "rpc name = " + self.rpc_name + " arg_lst_count = " + str(len(self.rpc_arg_list))
		for arg_obj in self.rpc_arg_list:
			if arg_obj.arg_name != None:
				print "arg name = " + arg_obj.arg_name 
			else:
				print "arg name = None"
			
			if arg_obj.isPTR == None:	
				print "arg ptr = None"
			else:
				print "arg ptr = " + arg_obj.isPTR

			if arg_obj.dataType == None:
				print "Datatype = None"
			else:
				print "arg_obj.dataType = " + arg_obj.dataType
			
			if arg_obj.referredObject == None:
				print "referredObject = None"
			else:
				print "referredObject = " + arg_obj.referredObject

		print "Return type : "
		arg_obj = self.rpc_return_type
		arg_obj.print_rpc_arg()	
		print "----------\n"	

	def contatenate_arg_name(self):
		_str=""
		if len(self.rpc_arg_list) == 0:
			return _str

		if len(self.rpc_arg_list) == 1:
			return self.rpc_arg_list[0].arg_name

		for i in range(len(self.rpc_arg_list) -1):
			_str += self.rpc_arg_list[i].arg_name + ", "

		_str += self.rpc_arg_list[len(self.rpc_arg_list) -1].arg_name
		return _str

class rpc_arg:
	def __init__(self):
		arg_name=""
		dataType=None
		isPTR="false"
		referredObject=None

	def print_rpc_arg(self):
		if self.arg_name != None:
			print "arg name = " + self.arg_name 
		else:
			print "arg name = None"
		
		if self.isPTR == None:	
			print "arg ptr = None"
		else:
			print "arg ptr = " + self.isPTR

		if self.dataType == None:
			print "Datatype = None"
		else:
			print "arg_obj.dataType = " + self.dataType + "\n"
		
		if self.referredObject == None:
			print "referredObject = None\n"
		else:
			print "referredObject = " + self.referredObject + "\n"

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

class xml_data:
	def __init__(self):
		self.c_struct_obj_list = []
		self.rpc_list = []

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
	rpc_list = []
	xml_data_obj = xml_data()
	DOMTree = xml.dom.minidom.parse(xml_file_name)
	collection = DOMTree.documentElement

# Get all the C Structures in the collection
	c_structures_collection = collection.getElementsByTagName("C_Structure")
	rpc_collection = collection.getElementsByTagName("RPC_spec")

	for c_struct in c_structures_collection:
		c_struct_obj = c_structures ()
		c_struct_obj.struct_name = c_struct.getAttribute("name")
		c_struct_obj.descrption = c_struct.getAttribute("description")
		fld_list = []
	
		fields_collection = c_struct.getElementsByTagName("member")
		ist_fld = "true" ;
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
				if fld_obj.isptr == "true" and ist_fld == "true":
					rpc_padd_fld = field ()
					rpc_padd_fld.field_name = "rpc_padd"
					rpc_padd_fld.datatype = "CHAR"
					rpc_padd_fld.desc = "rpc padd field"
					rpc_padd_fld.referredObject = None
					rpc_padd_fld.isptr = "false"
					rpc_padd_fld.vector = "false"
					rpc_padd_fld.cDataArraySize = None
					fld_list.append(rpc_padd_fld)
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

			ist_fld = "false";
			fld_list.append(fld_obj)
			
		c_struct_obj.field_list = fld_list		
		__get_structure_external_references_list (c_struct_obj)

		c_struct_obj_list.append(c_struct_obj)
	xml_data_obj.c_struct_obj_list = c_struct_obj_list
	
	for rpc_it in rpc_collection:
		rpc_obj = rpc()
		rpc_obj.rpc_name = rpc_it.getAttribute("rpc_name")
		arg_lst = []
		
		arg_collection = rpc_it.getElementsByTagName("member")
		i = 0
		for arg_it in arg_collection:	
			arg_obj = rpc_arg()
			if arg_it.hasAttribute("name"):
				arg_obj.arg_name = arg_it.getAttribute("name")
			else:
				arg_obj.arg_name = None
				arg_obj.dataType = arg_it.getAttribute("dataType")
				if arg_obj.dataType == "OBJECT":
					arg_obj.referredObject = arg_it.getAttribute("referredObject")
				else:
					arg_obj.referredObject = None
				if arg_it.hasAttribute("isPTR"):
					arg_obj.isPTR = arg_it.getAttribute("isPTR")
				else:
					arg_obj.isPTR = "false"
				rpc_obj.rpc_return_type =  arg_obj
				continue
				
			if arg_it.hasAttribute("dataType"):
				 arg_obj.dataType = arg_it.getAttribute("dataType")

			if arg_it.hasAttribute("isPTR"):
				arg_obj.isPTR = arg_it.getAttribute("isPTR")
			else:
				arg_obj.isPTR = None

			if arg_it.hasAttribute("referredObject"):
				arg_obj.referredObject = arg_it.getAttribute("referredObject")
			else:
				arg_obj.referredObject = None
		
			arg_lst.append(arg_obj)
		rpc_obj.rpc_arg_list = arg_lst
		#rpc_obj.print_rpc()
		rpc_list.append(rpc_obj)

	xml_data_obj.rpc_list = rpc_list			
	return xml_data_obj


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
			target_c.write("if(obj->" + fld_format[2] + ")\n")
			target_c.write(tab + tab + "serialize_string(b, (char *)obj->" + fld_format[2] + ", " + __get_size_of(fld_format[0]) + ");\n")
			target_c.write(tab + "else\n")
			target_c.write(tab + tab + "serialize_int32(b, NON_EXISTING_STRUCT);\n")
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
			target_c.write("if(obj->" + fld_format[2] + "[loop_var])\n")
			target_c.write(tab + tab + tab)
			target_c.write("serialize_string(b, (char *)obj->" + fld_format[2] + "[loop_var], " + __get_size_of(fld_format[0]) + ");\n")
			target_c.write(tab + tab + "else\n")
			target_c.write(tab + tab + tab)
			target_c.write("serialize_int32(b, NON_EXISTING_STRUCT);\n")
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
	target_c.write(tab + "if(is_serialized_buffer_empty(b)) return NULL;\n")
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
			target_c.write("de_serialize_string_by_ref((char *)&obj->" + fld_format[2] + ", b, " + __get_size_of(fld_format[0]) + ");\n")
		elif fld_format[0] != "OBJECT" and fld_format[1] == "true" and fld_format[5] == None and fld_format[3] == "true":
			#p_count = 0; int *p
			target_c.write("de_serialize_string((char *)&obj->" + fld_format[2] + "_count, b, sizeof(unsigned int));\n")
			target_c.write(tab)
			target_c.write("if(obj->" + fld_format[2] + "_count)\n")
			target_c.write(tab + tab + "obj->" + fld_format[2] + " = calloc(" + __get_size_of(fld_format[0]) + ", obj->" + fld_format[2] + "_count);\n")
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
			target_c.write("de_serialize_string_by_ref((char *)(&obj->" + fld_format[2] + "[loop_var]), b, " + __get_size_of(fld_format[0]) + ");\n")
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

def get_rpc_signature(rpc_obj):
	sign = ""
	rpc_return_type = rpc_obj.rpc_return_type
	if rpc_return_type.dataType != "OBJECT":
		sign += __get_c_datatype(rpc_return_type.dataType)
	else:
		 sign += rpc_return_type.referredObject

	if rpc_return_type.isPTR == "true":
		sign += " *\n"
	else:
		sign += "\n"

	sign += rpc_obj.rpc_name + "("
		
	if len(rpc_obj.rpc_arg_list) == 1:
		arg_obj = rpc_obj.rpc_arg_list[0]
		if arg_obj.dataType == "OBJECT":
			sign += arg_obj.referredObject
		else:
			sign += __get_c_datatype(arg_obj.dataType)
		
		if arg_obj.isPTR == "true":
			sign += " *"
		else:
			 sign += " "
	
		sign += arg_obj.arg_name
		sign += ")"

	else:
		for i in range(len(rpc_obj.rpc_arg_list) -1):
			arg_obj = rpc_obj.rpc_arg_list[i]
			if arg_obj.dataType == "OBJECT":
				sign += arg_obj.referredObject
			else:
				sign += __get_c_datatype(arg_obj.dataType)
			
			if arg_obj.isPTR == "true":
				sign += " *"
			else:
				 sign += " "
	
			sign += arg_obj.arg_name + ", "
			
		arg_obj = rpc_obj.rpc_arg_list[len(rpc_obj.rpc_arg_list) -1]

		if arg_obj.dataType == "OBJECT":
			sign += arg_obj.referredObject
		else:
			sign += __get_c_datatype(arg_obj.dataType)
		
		if arg_obj.isPTR == "true":
			sign += " *"
		else:
			 sign += " "

		sign += arg_obj.arg_name + ")"
	return sign


def generate_rpc_spec_file(xml_data_obj, dir_path):
	target = open(dir_path + "/rpc_spec.h", 'w')
	target.write("#ifndef __RPC_SPEC__\n")
	target.write("#define __RPC_SPEC__\n")
	
	target.write("\n\n#define SERVER_IP	\"127.0.0.1\"\n")
	target.write("#define SERVER_PORT	2000\n")

	target.write("\n#define SERVER_RECV_BUFF_MAX_SIZE	(1024 * 5)\n")
	
	target.write("\n\n")

	tab = "	"

	# iterate over all RPCs and print their IDs
	target.write("typedef enum _rpc_procedures_id{\n")

	if len(xml_data_obj.rpc_list) == 1:
		target.write(tab + xml_data_obj.rpc_list[0].rpc_name + "_id\n")
		target.write(tab + "rpc_procedures_max_id\n")
		target.write("} rpc_proc_id;\n\n\n")
	else:
		for i in range(len(xml_data_obj.rpc_list) -1):
			target.write(tab + xml_data_obj.rpc_list[i].rpc_name + "_id,\n")
		target.write(tab + xml_data_obj.rpc_list[(len(xml_data_obj.rpc_list) -1)].rpc_name + "_id,\n")
		target.write(tab + "rpc_procedures_max_id\n")
		target.write("} rpc_proc_id;\n\n\n")

	# iterare over all structures and print #includes
	for struct_obj in xml_data_obj.c_struct_obj_list:
		target.write("#include \""  + struct_obj.struct_name + ".h\"\n")


	target.write("\n\n")
	# iterate over all RPCs and print their Signatures
	for rpc_obj in xml_data_obj.rpc_list:
		signature = get_rpc_signature(rpc_obj)
		target.write(signature + ";\n\n")

	target.write("\n\n#endif\n")
	target.close()
		

def generate_server_stubs_c(xml_data_obj, dir_path):
	target = open(dir_path + "/rpc_server_stubs.c", 'w')
	target.write("#include \"rpc_spec.h\"\n")
	target.write("#include \"serialize.h\"\n")
	target.write("\n")
	for struct_obj in xml_data_obj.c_struct_obj_list:
		target.write("#include \"" + struct_obj.struct_name + ".h\"\n")
		target.write("#include \"" + struct_obj.struct_name + "_xdr_serialize.h\"\n")

	tab = "	"
	target.write("\n\n")
	for rpc_obj in xml_data_obj.rpc_list:
		target.write("ser_buff_t *\n")
		target.write("stub_" + rpc_obj.rpc_name + "(ser_buff_t *b){\n")
		target.write(tab + "ser_buff_t *out_b = 0;\n")
		for arg in rpc_obj.rpc_arg_list:
			if arg.dataType != "OBJECT" and arg.isPTR == "false":
				target.write(tab + __get_c_datatype(arg.dataType) + " " + arg.arg_name + ";\n")
				target.write(tab + "de_serialize_string((char *)&" + arg.arg_name + ", b , " + __get_size_of(arg.dataType) + ");\n") 
			elif arg.dataType != "OBJECT" and arg.isPTR == "true":
				target.write(tab + __get_c_datatype(arg.dataType) + " *" + arg.arg_name + ";\n")
				target.write(tab + "de_serialize_string((char *)" + arg.arg_name + ", b , " + __get_size_of(arg.dataType) + ");\n") 
			elif arg.dataType == "OBJECT" and arg.isPTR == "false":
				target.write(tab + arg.referredObject + " " + arg.arg_name + " = *" + arg.referredObject + "_xdr_deserialize(b);\n")
			elif arg.dataType == "OBJECT" and arg.isPTR == "true":
				target.write(tab + arg.referredObject + " *" + arg.arg_name + " = " + arg.referredObject + "_xdr_deserialize(b);\n")

		rpc_return_type = rpc_obj.rpc_return_type
		arg_sequence = rpc_obj.contatenate_arg_name()
		if rpc_return_type.dataType != "OBJECT" and rpc_return_type.isPTR == "false":
			target.write(tab + __get_c_datatype(rpc_return_type.dataType) + " res = " + rpc_obj.rpc_name + "(" + arg_sequence + ");\n")
		elif rpc_return_type.dataType != "OBJECT" and rpc_return_type.isPTR == "true":
			target.write(tab + __get_c_datatype(rpc_return_type.dataType) + " *res = " + rpc_obj.rpc_name + "(" + arg_sequence + ");\n")
		elif rpc_return_type.dataType == "OBJECT" and rpc_return_type.isPTR == "false":
			target.write(tab + rpc_return_type.referredObject + " res = *" +  rpc_obj.rpc_name + "(" + arg_sequence + ");\n")
		elif rpc_return_type.dataType == "OBJECT" and rpc_return_type.isPTR == "true":
			target.write(tab + rpc_return_type.referredObject + " * res = " + rpc_obj.rpc_name + "(" + arg_sequence + ");\n")

		target.write(tab + "init_serialized_buffer(&out_b);\n")
		
		if rpc_return_type.dataType != "OBJECT" and rpc_return_type.isPTR == "false":
			target.write(tab + "serialize_string(out_b, (char *)&res, " + __get_size_of(rpc_return_type.dataType) + ");\n")
		elif rpc_return_type.dataType != "OBJECT" and rpc_return_type.isPTR == "true":
			target.write(tab + "serialize_string(out_b, (char *)res, " + __get_size_of(rpc_return_type.dataType) + ");\n")
		elif rpc_return_type.dataType == "OBJECT" and rpc_return_type.isPTR == "false":
			target.write(tab + rpc_return_type.referredObject + "_xdr_serialize(&res, out_b);\n")
		elif rpc_return_type.dataType == "OBJECT" and rpc_return_type.isPTR == "true":
			target.write(tab + rpc_return_type.referredObject + "_xdr_serialize(res, out_b);\n")

		target.write(tab + "return out_b;\n}\n\n")
	target.close()


def generate_client_stubs(xml_data_obj, dir_path):
	target = open(dir_path + "/rpc_client_stubs.c", 'w')
	target.write("#include \"rpc_spec.h\"\n")
	target.write("#include \"rpc_common.h\"\n")
	target.write("\n")
	
	for struct_obj in xml_data_obj.c_struct_obj_list:
		target.write("#include \"" + struct_obj.struct_name + ".h\"\n")
		target.write("#include \"" + struct_obj.struct_name + "_xdr_serialize.h\"\n")
	
	target.write("\n\n")
	target.write("static unsigned int tid = 0;\n")
	target.write("extern client_param_t client_param;\n")
	target.write("extern int client_rpc_send_rcv (ser_buff_t *in_b, ser_buff_t *out_b);\n")
	target.write("\n\n")
	tab = "	"
	for rpc_obj in xml_data_obj.rpc_list:
		signature = get_rpc_signature(rpc_obj)
		target.write(signature + "{\n")
		target.write(tab + "ser_buff_t *in_b = 0, *out_b = 0;\n")
		target.write(tab + "int rc = 0;\n")
		target.write(tab + "init_serialized_buffer(&in_b);\n")
		target.write(tab + "out_b = client_param.recv_ser_b;\n")
		target.write(tab + "serialize_string(in_b, (char *)&tid, sizeof(unsigned int));\n")
		target.write(tab + "tid++;\n")
		target.write(tab + "serialize_uint32(in_b, " + rpc_obj.rpc_name + "_id);\n")
		target.write(tab + "serialize_uint32(in_b, RPC_REQ);\n")
		target.write(tab + "unsigned int payload_size_offset = get_serialize_buffer_current_ptr_offset(in_b);\n")
		target.write(tab + "serialize_buffer_skip(in_b, sizeof(unsigned int));\n")
		
		for arg in rpc_obj.rpc_arg_list:
			if arg.dataType != "OBJECT" and arg.isPTR == "false":
				target.write(tab + "serialize_string(in_b, (char *)&" + arg.arg_name + ", " + __get_size_of(arg.dataType) + ");\n") 
			elif arg.dataType != "OBJECT" and arg.isPTR == "true":
				target.write(tab + "serialize_string(in_b, (char *)" + arg.arg_name + ", " + __get_size_of(arg.dataType) + ");\n") 
			elif arg.dataType == "OBJECT" and arg.isPTR == "false":
				target.write(tab + arg.referredObject + "_xdr_serialize(&" + arg.arg_name + ", in_b);\n")
			elif arg.dataType == "OBJECT" and arg.isPTR == "true":
				target.write(tab + arg.referredObject + "_xdr_serialize(" + arg.arg_name + ", in_b);\n")

		target.write(tab + "unsigned int payload_size = get_serialize_buffer_size(in_b) - serialized_rpc_hdr_size();\n")
		target.write(tab + "copy_in_serialized_buffer_by_offset(in_b, sizeof(unsigned int), (char *)&payload_size, payload_size_offset);\n")
		target.write(tab + "rc = client_rpc_send_rcv(in_b, out_b);\n")
		
		rpc_return_type = rpc_obj.rpc_return_type
		
		if rpc_return_type.dataType != "OBJECT" and rpc_return_type.isPTR == "false":
			target.write(tab + __get_c_datatype(rpc_return_type.dataType) + " res;\n")
			target.write(tab + "de_serialize_string((char *)&res, out_b, " +  __get_size_of(rpc_return_type.dataType) + ");\n")
		elif rpc_return_type.dataType != "OBJECT" and rpc_return_type.isPTR == "true":
			target.write(tab + __get_c_datatype(rpc_return_type.dataType) + "  *res;\n")
			target.write(tab + "de_serialize_string((char *)res, out_b, " + __get_size_of(rpc_return_type.dataType) + ");\n")
		elif rpc_return_type.dataType == "OBJECT" and rpc_return_type.isPTR == "false":
			target.write(tab + rpc_return_type.referredObject + " res = *" + rpc_return_type.referredObject + "_xdr_deserialize(out_b);\n")
		elif rpc_return_type.dataType == "OBJECT" and rpc_return_type.isPTR == "true":
			target.write(tab + rpc_return_type.referredObject + " * res = " + rpc_return_type.referredObject + "_xdr_deserialize(out_b);\n")

		target.write(tab + "reset_serialize_buffer(out_b);\n")
		target.write(tab + "return res;\n")
		target.write("}\n\n")		
	target.close()


def generate_rpc_server_init(xml_data_obj, dir_path):
	target = open(dir_path + "/rpc_server_init.c", 'w')
	target.write("#include \"rpc_spec.h\"\n")
	target.write("#include \"rpc_server_stubs.h\"\n")
	target.write("\n")
	target.write("typedef ser_buff_t* (*rpc_callback)(ser_buff_t *b);\n")
	target.write("rpc_callback rpc_callback_array[rpc_procedures_max_id];\n")
	target.write("\n")
	target.write("void rpc_server_load_rpcs(){\n")
	tab = "	"
	for rpc_obj in xml_data_obj.rpc_list:
		target.write(tab + "rpc_callback_array[" + rpc_obj.rpc_name + "_id] = stub_" + rpc_obj.rpc_name + ";\n")
	target.write("}\n") 
	target.close()


def generate_rpc_server_stubs_h(xml_data_obj, dir_path):
	target = open(dir_path + "/rpc_server_stubs.h", 'w')
	target.write("#ifndef __RPC_SERVER__STUB__\n")
	target.write("#define __RPC_SERVER__STUB__\n")
	target.write("\n\n")
	target.write("typedef struct serialized_buffer ser_buff_t;\n")
	target.write("\n\n")
	for rpc_obj in xml_data_obj.rpc_list:
		target.write("ser_buff_t *\nstub_" + rpc_obj.rpc_name + "(ser_buff_t *b);\n")
		target.write("\n") 
	target.write("#endif")
	
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
	xml_data_obj =  build_structure_list_from_xml(xml_file_name)
	convert_xml_to_c_structures(xml_file_name, ".", xml_data_obj.c_struct_obj_list)
	for c_struct_obj in xml_data_obj.c_struct_obj_list:
		serialize_structure(c_struct_obj, ".")
		deserialize_structure(c_struct_obj, ".")
	generate_rpc_spec_file(xml_data_obj, ".")
	generate_client_stubs(xml_data_obj, ".")
	generate_server_stubs_c(xml_data_obj, ".")
	generate_rpc_server_init(xml_data_obj, ".")
	generate_rpc_server_stubs_h(xml_data_obj, ".")
