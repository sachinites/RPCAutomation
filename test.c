#include "company_t.h"
#include "person_t.h"
#include <stdlib.h>
#include <stdio.h>
#include <memory.h>
#include "rpc_spec.h"
#include "rpc_uapi.h"
#include "complex_t.h"
#include "tree_t.h"
#include "tree_node_t.h"
#include "ll_node_t.h"

//void gdb(ser_buff_t *b){}

int
main(int argc, char **argv){
	person_t person[4];
	memset(person, 0, sizeof(person));
	person[0].age = 20;
	strcpy(person[0].name , "Abhishek");
	person[1].age = 21;
	strcpy(person[1].name , "Sagar");
	person[2].age = 22;
	strcpy(person[2].name , "Mohan");
	person[3].age = 22;
	strcpy(person[3].name , "Kumar");

	strcpy(person[0].dream_companies[0].comp_name, "BRCD");
	strcpy(person[0].dream_companies[1].comp_name, "Juniper");
	strcpy(person[0].dream_companies[2].comp_name, "Cisco");

	

	set_rpc_client_param(5000);
	int rc = rpc_send_employee_list(person, 4);

	printf("rc = %d\n", rc);
    int n1 = 2, n2 = 4;
    printf("Result of adding two number %d and %d= %d\n", n1,n2, rpc_add_numbers(n1,n2));

#if 0
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
	complex_t com = {3,4};
	float mag = rpc_sqrt_complex_number(&com);
	printf("magnitude = %f\n", mag);

	ll_node_t *head = calloc(1, sizeof(ll_node_t));
	head->data = 1;
	head->next =  calloc(1, sizeof(ll_node_t));
	head->next->data =2;
	head->next->next = calloc(1, sizeof(ll_node_t));
	head->next->next->data = 3;
	head->next->next->next = calloc(1, sizeof(ll_node_t));
	head->next->next->next->data = 4;

	printf("sum of ll = %d\n", rpc_ll_sum(head));

//	gdb(b);
#endif
	return 0;
}
