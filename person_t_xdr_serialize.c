#include <stdlib.h>
#include <memory.h>
#include "person_t.h"
#include "person_t_xdr_serialize.h"
#include "company_t_xdr_serialize.h"

static unsigned int loop_var = 0;



void 
person_t_xdr_serialize(person_t *obj, ser_buff_t *b){
	if(!obj){
		serialize_int32(b, NON_EXISTING_STRUCT);
		return;
	}
	serialize_string(b, (char *)obj->vehicle_nos, sizeof(unsigned int)*4);
	serialize_string(b, (char *)&obj->age, sizeof(int));
	if(obj->height)
		serialize_string(b, (char *)obj->height, sizeof(int));
	else
		serialize_int32(b, NON_EXISTING_STRUCT);
	serialize_string(b, (char *)&obj->acc_nos_count, sizeof(unsigned int));
	for (loop_var = 0; loop_var < obj->acc_nos_count ; loop_var ++)
		serialize_string(b, (char *)(obj->acc_nos + loop_var), sizeof(unsigned int));
	for (loop_var = 0; loop_var < 12; loop_var++){
		if(obj->last_salary_amounts[loop_var])
			serialize_string(b, (char *)obj->last_salary_amounts[loop_var], sizeof(unsigned int));
		else
			serialize_int32(b, NON_EXISTING_STRUCT);
	}
	serialize_string(b, (char *)obj->name, sizeof(char)*32);
	company_t_xdr_serialize(&obj->company , b);
	serialize_string(b, (char *)&obj->prev_employers_count, sizeof(unsigned int));
	for (loop_var = 0; loop_var < obj->prev_employers_count ; loop_var ++){
		company_t_xdr_serialize(obj->prev_employers + loop_var, b);
	}
	for (loop_var = 0; loop_var < 3; loop_var++){
		company_t_xdr_serialize(&obj->dream_companies[loop_var], b);
	}
	serialize_string(b, (char *)&obj->friends_count, sizeof(unsigned int));
	for (loop_var = 0; loop_var < obj->friends_count ; loop_var ++){
		person_t_xdr_serialize(obj->friends + loop_var, b);
	}
	person_t_xdr_serialize(obj->CEO , b);
	for (loop_var = 0; loop_var < 12; loop_var++){
		person_t_xdr_serialize(obj->administrative_staff[loop_var], b);
	}
}

person_t *
person_t_xdr_deserialize(ser_buff_t *b){

	int check_existence;
	if(is_serialized_buffer_empty(b)) return NULL;
	de_serialize_string((char *)&check_existence, b, sizeof(int));
	if(check_existence == NON_EXISTING_STRUCT){
		return NULL;
	}
	serialize_buffer_skip(b, -1*sizeof(int));

	person_t *obj = calloc(1, sizeof(person_t));
	de_serialize_string((char *)obj->vehicle_nos, b, sizeof(unsigned int)*4);
	de_serialize_string((char *)&obj->age, b, sizeof(int));
	de_serialize_string_by_ref((char *)&obj->height, b, sizeof(int));
	de_serialize_string((char *)&obj->acc_nos_count, b, sizeof(unsigned int));
	if(obj->acc_nos_count)
		obj->acc_nos = calloc(sizeof(unsigned int), obj->acc_nos_count);
	for (loop_var = 0; loop_var < obj->acc_nos_count;  loop_var++){
		de_serialize_string((char *)(obj->acc_nos + loop_var), b, sizeof(unsigned int));
	}
	for (loop_var = 0; loop_var < 12; loop_var++)
		de_serialize_string_by_ref((char *)(&obj->last_salary_amounts[loop_var]), b, sizeof(unsigned int));
	de_serialize_string((char *)obj->name, b, sizeof(char)*32);
	obj->company = *company_t_xdr_deserialize(b);
	de_serialize_string((char *)&obj->prev_employers_count, b, sizeof(unsigned int));
	obj->prev_employers = calloc (obj->prev_employers_count, sizeof(company_t));
	for (loop_var = 0; loop_var < obj->prev_employers_count ; loop_var ++){
		company_t *constructed_obj = company_t_xdr_deserialize(b);
		memcpy(obj->prev_employers + loop_var, constructed_obj, sizeof(company_t));
		free(constructed_obj);
	}
	for (loop_var = 0; loop_var < 3; loop_var++){
		obj->dream_companies[loop_var] = *company_t_xdr_deserialize(b);
	}
	de_serialize_string((char *)&obj->friends_count, b, sizeof(unsigned int));
	obj->friends = calloc (obj->friends_count, sizeof(person_t));
	for (loop_var = 0; loop_var < obj->friends_count ; loop_var ++){
		person_t *constructed_obj = person_t_xdr_deserialize(b);
		memcpy(obj->friends + loop_var, constructed_obj, sizeof(person_t));
		free(constructed_obj);
	}
	obj->CEO = person_t_xdr_deserialize(b);
	for (loop_var = 0; loop_var < 12; loop_var++){
		obj->administrative_staff[loop_var] = person_t_xdr_deserialize(b);
	}
	return obj;
}