#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <netdb.h> 

#define XAXI_EYESCAN_COMMON_DRP 0x40000
#define XAXI_EYESCAN_QUAD_SHIFT 11
#define XPAR_AXI_EYESCAN_0_BASEADDR 0x44B00000
#define XAXI_EYESCAN_CHANNEL_DRP    0x80800
#define XAXI_EYESCAN_CHANNEL_SHIFT  13

typedef unsigned long u32;

int main(int argc, char *argv[])
{
    u32 chanIdx = 0;
    u32 offset = 0x151;
    u32 eyescan_base = XPAR_AXI_EYESCAN_0_BASEADDR;
    u32 address = eyescan_base | (u32)XAXI_EYESCAN_CHANNEL_DRP;
    printf( "address 0x%08lx\n" , address );
    address = (u32) chanIdx << XAXI_EYESCAN_CHANNEL_SHIFT;
    printf( "address 0x%08lx\n" , address );
    address = eyescan_base | (u32)XAXI_EYESCAN_CHANNEL_DRP | (u32)(chanIdx << XAXI_EYESCAN_CHANNEL_SHIFT);
    printf( "address 0x%08lx\n" , address );
    address += (offset << 2);
    printf( "address 0x%08lx\n" , address );
    
    return 0;
}
