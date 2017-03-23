#include "stdio.h"
#include "rpc_spec.h"

person_t *
rpc_remote_call(person_t *arg1, person_t arg2, int n){
	printf("server side %s  is called\n", __FUNCTION__);
	return NULL;
}

float
rpc_sqrt_complex_number(complex_t *arg1){
	return (float)(arg1->real * arg1->real) + (arg1->im * arg1->im);
}
