rm *.o
gcc -g -c -I . serialize.c -o serialize.o
gcc -g -c -I . person_t_xdr_serialize.c -o person_t_xdr_serialize.o
gcc -g -c -I . company_t_xdr_serialize.c -o company_t_xdr_serialize.o
gcc -g -c -I . test.c -o test.o
gcc -g -c -I . rpc_client_stubs.c -o rpc_client_stubs.o
gcc -g -c -I . rpc_client.c -o rpc_client.o
gcc -g -c -I . complex_t_xdr_serialize.c -o complex_t_xdr_serialize.o
gcc -g -c -I . tree_t_xdr_serialize.c -o tree_t_xdr_serialize.o
gcc -g -c -I . tree_node_t_xdr_serialize.c -o tree_node_t_xdr_serialize.o
gcc -g -c -I . ll_node_t_xdr_serialize.c -o ll_node_t_xdr_serialize.o
gcc -g test.o company_t_xdr_serialize.o person_t_xdr_serialize.o serialize.o rpc_client_stubs.o rpc_client.o complex_t_xdr_serialize.o tree_node_t_xdr_serialize.o tree_t_xdr_serialize.o ll_node_t_xdr_serialize.o -o client
gcc -g -c -I . rpc_server.c -o rpc_server.o
gcc -g -c -I . rpc_server_init.c -o rpc_server_init.o
gcc -g -c -I . rpc_server_main.c -o rpc_server_main.o
gcc -g -c -I . rpc_server_stubs.c -o rpc_server_stubs.o
gcc -g -c -I . rpc_server_implementation.c -o rpc_server_implementation.o
gcc -g -c -I . rpc_server_usercode1.c -o rpc_server_usercode1.o
gcc -g rpc_server_main.o rpc_server_init.o rpc_server.o serialize.o rpc_server_stubs.o rpc_server_implementation.o person_t_xdr_serialize.o company_t_xdr_serialize.o complex_t_xdr_serialize.o tree_node_t_xdr_serialize.o tree_t_xdr_serialize.o rpc_server_usercode1.o ll_node_t_xdr_serialize.o -o server
