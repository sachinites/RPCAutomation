#ifndef __rpc_fn__
#define __rpc_fn__

#define SERVER_IP	"127.0.0.1"
#define SERVER_PORT     2000

#define SERVER_RECV_BUFF_MAX_SIZE	(1024 * 5)

typedef struct _person_t_ person_t;

typedef enum _rpc_procedures_id{
	rpc_remote_call_id = 0,
	rpc_sqrt_complex_number_id,
	rpc_MaxSumPath_id,
	rpc_ll_sum_id,
	rpc_procedures_max_id
} rpc_proc_id;

#include "person_t.h"
#include "company_t.h"	/* Mention all direct or indirect external references of person_t*/
#include "complex_t.h"
#include "tree_node_t.h"
#include "tree_t.h"
#include "ll_node_t.h"

/* Add the fn signature*/
person_t *
rpc_remote_call(person_t *arg1, person_t arg2, int n);

float
rpc_sqrt_complex_number(complex_t *arg1);

int rpc_MaxSumPath(tree_t *tree);

int rpc_ll_sum(ll_node_t *arg1);
#endif
