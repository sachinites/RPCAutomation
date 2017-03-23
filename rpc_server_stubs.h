#ifndef __RPC_SERVER__STUB__
#define __RPC_SERVER__STUB__


typedef struct serialized_buffer ser_buff_t;

ser_buff_t * 
stub_rpc_remote_call(ser_buff_t *b);

ser_buff_t *
stub_rpc_sqrt_complex_number(ser_buff_t *b);

#endif
