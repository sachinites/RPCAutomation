rm exe serialize.o person_t_xdr_serialize.o company_t_xdr_serialize.o test.o rpc_fn.o rpc_main.o
gcc -g -c -I .  serialize.c -o serialize.o
gcc -g -c -I . person_t_xdr_serialize.c -o person_t_xdr_serialize.o
gcc -g -c -I . company_t_xdr_serialize.c -o company_t_xdr_serialize.o
gcc -g -c -I . test.c -o test.o
gcc -g -c -I . rpc_fn.c -o rpc_fn.o
gcc -g -c -I . rpc_main.c -o rpc_main.o
gcc -g test.o company_t_xdr_serialize.o person_t_xdr_serialize.o serialize.o rpc_fn.o rpc_main.o -o exe
