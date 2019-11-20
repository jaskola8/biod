#include <stdio.h>
#include <string.h>

int main(int argc, char** argv) {
	int zalogowany;
	char haslo[8];
	zalogowany = 0;
	strncpy(haslo, argv[1], 8);
	if (strcmp(haslo, "Tajne") == 0)
		zalogowany = 1;
	if (zalogowany == 1)
		printf("TAK\n");
	else
		printf("NIE\n");
	return 0;
}
