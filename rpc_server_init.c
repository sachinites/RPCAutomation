#include "rpc_spec.h"
#include "rpc_server_stubs.h"

typedef ser_buff_t* (*rpc_callback)(ser_buff_t *b);
rpc_callback rpc_callback_array[rpc_procedures_max_id];

void rpc_server_load_rpcs(){

	rpc_callback_array[rpc_remote_call_id] = stub_rpc_remote_call;
	rpc_callback_array[rpc_sqrt_complex_number_id] = stub_rpc_sqrt_complex_number;
}

