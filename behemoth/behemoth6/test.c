#include <stdio.h>

int main() {
    FILE *stream = popen("./test_subprocess", "r");
    char buf[10];
    fread(buf, 10, 1, stream);
    for(int i = 0; i < 10; i++){ 
        putc(buf[i], stdout);
    }
    putc('\n', stdout);
}