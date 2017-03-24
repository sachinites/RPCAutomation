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
