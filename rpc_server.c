#include "serialize.h"
#include "rpc_common.h"
#include <stdio.h>

typedef ser_buff_t* (*rpc_callback)(ser_buff_t *b);
extern rpc_callback rpc_callback_array[];

ser_buff_t *
rpc_server_process_msg(ser_buff_t *b){
	rpc_hdr_t rpc_hdr;
	
	de_serialize_string((char *)&rpc_hdr.tid, b, sizeof(rpc_hdr.tid));
	de_serialize_string((char *)&rpc_hdr.rpc_proc_id, b, sizeof(rpc_hdr.rpc_proc_id));
	de_serialize_string((char *)&rpc_hdr.msg_type, b, sizeof(rpc_hdr.msg_type));
	de_serialize_string((char *)&rpc_hdr.payload_size, b, sizeof(rpc_hdr.payload_size));
	printf("rpc_hdr.rpc_proc_id = %d\n", rpc_hdr.rpc_proc_id);
	return rpc_callback_array[rpc_hdr.rpc_proc_id](b);
}

