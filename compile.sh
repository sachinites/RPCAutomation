gcc -g -c -I .  serialize.c -o serialize.o
gcc -g -c -I . person_t_xdr_serialize.c -o person_t_xdr_serialize.o
gcc -g -c -I . company_t_xdr_serialize.c -o company_t_xdr_serialize.o
gcc -g -c -I . test.c -o test.o
gcc -g test.o company_t_xdr_serialize.o person_t_xdr_serialize.o serialize.o -o exe
