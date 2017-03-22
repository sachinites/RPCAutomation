#ifndef __rpc_fn__
#define __rpc_fn__

typedef struct _person_t_ person_t;

typedef enum _rpc_procedures_id{

	rpc_remote_call_id = 0

} rpc_proc_id;

person_t *
rpc_remote_call(person_t *arg1, person_t arg2, int n);


#endif
