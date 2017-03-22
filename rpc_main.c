#include "rpc_main.h"
#include "serialize.h"
#include <stdio.h>
#include <stdlib.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <netdb.h>
#include "rpc_uapi.h"

#define SERVER_IP	"127.0.0.1"
#define SERVER_PORT	2000

client_param_t client_param;

void
set_rpc_client_param(unsigned int recv_buff_size){
	client_param.recv_buff_size = recv_buff_size;
	init_serialized_buffer_of_defined_size(&client_param.recv_ser_b,
					client_param.recv_buff_size);
}

int
client_rpc_send_rcv (ser_buff_t *in_b, ser_buff_t *out_b){
	
	struct sockaddr_in dest;
	int sockfd = 0, rc = 0;
	int addr_len;

	dest.sin_family = AF_INET;
	dest.sin_port = SERVER_PORT;
	struct hostent *host = (struct hostent *)gethostbyname(SERVER_IP);
	dest.sin_addr = *((struct in_addr *)host->h_addr);
	addr_len = sizeof(struct sockaddr);
	
	sockfd = socket(AF_INET, SOCK_DGRAM, IPPROTO_UDP);
	if(sockfd == -1){
		printf("igmp socket creation failed\n");
		return -1;
	}

	rc = sendto(sockfd, in_b, get_serialize_buffer_size(in_b), 0,
		(struct sockaddr *)&dest, sizeof(struct sockaddr));

	printf("%s() : %d bytes sent\n", __FUNCTION__, rc);

	if(get_serialize_buffer_length(client_param.recv_ser_b) < 1024){
		printf("%s() : Warning : Recv buffersize may be insufficient, size = %d\n", 
			__FUNCTION__, get_serialize_buffer_size(client_param.recv_ser_b));
	}

	rc = recvfrom(sockfd, (char *)out_b->b, get_serialize_buffer_size(out_b), 0, 
			(struct sockaddr *)&dest, &addr_len);

	printf("%s() : %d bytes recieved\n", __FUNCTION__, rc); 
		      
	return 0;
}


unsigned int
serialized_rpc_hdr_size(){
	rpc_hdr_t rpc_hdr;
	return sizeof(rpc_hdr.tid) +
	       sizeof(rpc_hdr.rpc_proc_id) +
	       sizeof(rpc_hdr.msg_type) +
	       sizeof(rpc_hdr.payload_size);
}

