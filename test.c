#include "company_t.h"
#include "person_t.h"
#include <stdlib.h>
#include <stdio.h>
#include <memory.h>
#include "rpc_fn.h"
#include "rpc_uapi.h"

//void gdb(ser_buff_t *b){}

int
main(int argc, char **argv){
	person_t person;
	memset(&person, 0, sizeof(person_t));

	person.vehicle_nos[0] = 100;
	person.vehicle_nos[1] = 101;
	person.vehicle_nos[2] = 102;
	person.vehicle_nos[3] = 103;

	person.age = 42;

	int *temp = calloc(1, sizeof(int));
	*temp = 5;
	person.height = temp;

	person.acc_nos_count= 2;
	person.acc_nos = calloc(person.acc_nos_count, sizeof(unsigned int));
	
	*(person.acc_nos + 0) = 124;
	*(person.acc_nos + 1) = 125;

	strcpy(person.name, "Abhishek\0");
	
	strcpy(person.company.comp_name, "Brocade\0");
	person.company.emp_strength = 4000;
	
	person_t *ceo = calloc(1, sizeof(person_t));
	strcpy(ceo->name,"Llyod\0");

	person.CEO = ceo;

	set_rpc_client_param(5000); // setting recieving buffer size to 5k bytes	
	//person_t *res = rpc_remote_call(&person, person, 1);


//	gdb(b);
	return 0;
}
