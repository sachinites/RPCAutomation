#include "rpc_server_usercode1.h"
#include "tree_node_t.h"
#include "memory.h"

 max_sum_res_t
_MaxSumPath(tree_node_t *root){

        max_sum_res_t res, lchild, rchild;
        memset(&res,    0, sizeof(max_sum_res_t));
        memset(&lchild, 0, sizeof(max_sum_res_t));
        memset(&rchild, 0, sizeof(max_sum_res_t));

        if(!root)
                return res;

        lchild = _MaxSumPath(root->left);
        rchild = _MaxSumPath(root->right);

        // case 1 : if i am leaf

        if(!root->left && !root->right){
                res.cum_sum = root->data;
                res.recycle_sum = root->data;
                return res;
        }

        // case 2: if half node
        if(!root->left && root->right){
                res.recycle_sum = 0 + rchild.cum_sum + root->data;
                res.cum_sum = MAX(0 + root->data, rchild.cum_sum + root->data);
                if(res.recycle_sum >= rchild.recycle_sum){

                }
                else
                {
                        res.recycle_sum = rchild.recycle_sum;
                }
                return res;
        }
        if(root->left && !root->right){
                res.recycle_sum = lchild.cum_sum + 0 + root->data;
                res.cum_sum = MAX(lchild.cum_sum + root->data, 0 + root->data);
                if(res.recycle_sum >= lchild.recycle_sum){

                }
                else
                {
                        res.recycle_sum = lchild.recycle_sum;
                }
                return res;

        // case 3: if internal node
        if(root->left && root->right){
                res.recycle_sum = lchild.cum_sum + rchild.cum_sum + root->data;
                res.cum_sum  =  MAX(lchild.cum_sum + root->data, rchild.cum_sum + root->data);
                if(res.recycle_sum >= lchild.recycle_sum){
                        if(res.recycle_sum >= rchild.recycle_sum){
                                return res;
                        }
                        // rchild has greatest recycle_sum
                        res.recycle_sum = rchild.recycle_sum;
                        return res;
                }
                if(lchild.recycle_sum >= rchild.recycle_sum){
                        res.recycle_sum = lchild.recycle_sum;
                        return res;
                }

                // rchild has greatest recycle_sum
                res.recycle_sum = rchild.recycle_sum;
                return res;
        }
}

	
}
