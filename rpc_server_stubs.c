#include <stdio.h>
#include "serialize.h"
#include "rpc_spec.h"

#include "person_t.h"
#include "person_t_xdr_serialize.h"
#include "company_t.h"
#include "company_t_xdr_serialize.h"
#include "complex_t.h"
#include "complex_t_xdr_serialize.h"


ser_buff_t *
stub_rpc_remote_call(ser_buff_t *b){
	ser_buff_t *out_b = NULL;
	/* step 1 : Un-Marshalling of ser buffer into arguments*/
	person_t *arg1 = person_t_xdr_deserialize(b);
	person_t arg2 = *person_t_xdr_deserialize(b);
	int arg3;
	de_serialize_string((char *)&arg3, b, sizeof(int));	
	
	/* step 2 : call the server RPC */
	person_t *res = rpc_remote_call(arg1, arg2, arg3);

	/* step 3 : Marshalling the result*/
	init_serialized_buffer(&out_b);
	person_t_xdr_serialize(res, out_b);
	return out_b;
}

ser_buff_t *
stub_rpc_sqrt_complex_number(ser_buff_t *b){
	ser_buff_t *out_b = NULL;
	/* step 1 : Un-Marshalling of ser buffer into arguments*/
	complex_t *arg1 = complex_t_xdr_deserialize(b);
	/* step 2 : call the server RPC */
	float res = rpc_sqrt_complex_number(arg1);

	/* step 3 : Marshalling the result*/
	init_serialized_buffer(&out_b);
	serialize_string(out_b, (char *)&res, sizeof(float));
	return out_b;
}
