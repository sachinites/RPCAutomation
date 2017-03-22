#include "rpc_fn.h"
#include "rpc_main.h"

#include "person_t.h"
#include "person_t_xdr_serialize.h"

static unsigned int tid = 0;
extern client_param_t client_param;


person_t *
rpc_remote_call(person_t *arg1, person_t arg2, int n){

	ser_buff_t *in_b = 0, *out_b = 0;
	int rc = 0;
	
	init_serialized_buffer(&in_b);
	out_b = client_param.recv_ser_b;

	serialize_string(in_b, (char *)&tid, sizeof(unsigned int));	
	tid++;
	serialize_uint32(in_b, rpc_remote_call_id);
	serialize_uint32(in_b, RPC_REQ);

	unsigned int payload_size_offset = get_serialize_buffer_current_ptr_offset(in_b);
	serialize_buffer_skip(in_b, sizeof(unsigned int));
	
	/*arg1*/
	person_t_xdr_serialize(arg1, in_b);
	/*arg2*/
	person_t_xdr_serialize(&arg2, in_b);
	/*arg3*/
	serialize_string(in_b, (char *)&n, sizeof(int));

	unsigned int payload_size = get_serialize_buffer_size(in_b) - serialized_rpc_hdr_size();
	copy_in_serialized_buffer_by_offset(in_b, sizeof(unsigned int), 
					(char *)&payload_size, payload_size_offset);
	rc = client_rpc_send_rcv(in_b, out_b);
	free_serialize_buffer(in_b);
	person_t *res = person_t_xdr_deserialize(out_b);
	reset_serialize_buffer(out_b);
	
	return res;
}
