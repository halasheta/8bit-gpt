#include <stdio.h>
#include <string.h>
#include <stdlib.h>

int main() {
	char input[256];
	char res[256];
	FILE *in, *out;
	int wait, retries, delay;
	
	// remove previous output if it exists
	if ((in = fopen("Unix:out.txt", "r")) != NULL) {
		remove("Unix:out.txt");
		in = NULL;
	}
	
	
	while (1) {
		printf("YOU: ");
		fgets(input, sizeof(input), stdin);
		
		// Write input to file
		out = fopen("Unix:input.txt", "w");
		if (out == NULL) {
			printf("Your message could not reach the other side :(\n");
			continue;
		}
		
		fprintf(out, "%s\r", input);
		fclose(out);
		//out = NULL;
		printf("\n");
		
		
		// Wait for LLM response
		wait = 0;
		while ((in = fopen("Unix:out.txt", "r")) == NULL) {
			wait++;
			if (wait > 50000) {
				printf("Robot went to sleep, try again");
				break;
			}
		
		}
		
		
		if (in != NULL) {
			retries = 0;
			do {
				memset(res, 0, sizeof(res));
				rewind(in);
				fgets(res, sizeof(res), in);
				retries++;
				
				while (delay < 5000){
					delay++;
				}
			} while (res[0] == '\0' && retries < 10);
			
			
			if (res[0] != '\0') {
				printf("ROBOT: %s\n", res);
				
				// Print other lines from the file if they exist
				while (fgets(res, sizeof(res), in)) {
					printf("ROBOT: %s\n", res);
				}
			} else {
				// fallback output
				printf("ROBOT: Dozed off for a sec there zZZZ\n");
			}
			fclose(in);
			in = NULL;
			remove("Unix:out.txt");
			
		}
	
	}

}