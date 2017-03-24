#ifndef __SERVER_USERCODE1_H__
#define __SERVER_USERCODE1_H__

#include "tree_node_t.h"

typedef struct _max_sum_res{
        int cum_sum;
        int recycle_sum;
} max_sum_res_t;

max_sum_res_t
_MaxSumPath(tree_node_t *root);

#endif
