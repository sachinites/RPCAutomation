#ifndef __person_t_xdr_serialize__
#define __person_t_xdr_serialize__

typedef struct _person_t_ person_t;
#include "serialize.h"


void 
person_t_xdr_serialize(person_t *obj, ser_buff_t *b);

person_t *
person_t_xdr_deserialize(ser_buff_t *b);


#endif