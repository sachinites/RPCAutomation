#include "stdio.h"
#include "rpc_spec.h"
#include "memory.h"
#include "stdlib.h"
#include "rpc_server_usercode1.h"

person_t *
rpc_remote_call(person_t *arg1, person_t arg2, int n){
	printf("server side %s  is called\n", __FUNCTION__);
	return NULL;
}

float
rpc_sqrt_complex_number(complex_t *arg1){
	return (float)(arg1->real * arg1->real) + (arg1->im * arg1->im);
}

int
rpc_MaxSumPath(tree_t *tree){
	if(!tree || !tree->root)
		return 0;

	max_sum_res_t res =  _MaxSumPath(tree->root);
	return res.recycle_sum;
}

int
rpc_ll_sum(ll_node_t *head){
	int sum = 0;
	for(; head; head = head->next)
		sum+=head->data;
	return sum;
}

int
rpc_send_employee_list(person_t *emp_list, unsigned int emp_list_count){

	unsigned int i = 0, j = 0;
	for (i = 0; i < emp_list_count; i++){
		printf("%d. age = %d, Name = %s\n", i, emp_list[i].age, emp_list[i].name);
		if(i == 0){	
			for(j = 0; j < 3; j++)
				printf("dream company name = %s\n", emp_list[i].dream_companies[j].comp_name);
		}
	}
	return i;
}

int
rpc_add_numbers(int n1, int n2){

    return n1+n2;
}
