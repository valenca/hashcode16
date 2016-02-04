#include <stdio.h>
#include <stdlib.h>
#include <limits.h>
#include <time.h>

/* R: Number of rows (max 1000) */
/* S: Number of slots per row (max 1000) */
/* U: Number of unavailable slots (max R*S -> 1000000) */
/* P: Number of pools (max 1000) */
/* M: Number of servers (max R*S -> 1000000) */
int R, S, U, P, M;

/* Server: max(1000000), [0]->size, [1]->capacity, [2]->index , [3]->row, [4]->slot*/
int server[1000000][5];
int nservers;
int usedServers;
/* Result: Server index, [0]->row, [1]->slot, [2]->pool */
int result[1000000][3];
/* Slots: [row][slot] -> server_number+1, 0 if empty, -1 if unavailable */
int slot[1000][1000];
int spaces[1000][1000];
/* Pool: [0]->total, [1]->max capacity for a single row, [2]->row index max */
int pool[1000];
int rows[1000];

void shuffleServers(){
	int r0, r1, i, t;
	for (i = 0; i < nservers/2; ++i){
		r0 = rand() % nservers;
		r1 = rand() % nservers;

		t = server[r0][0];
		server[r0][0] = server[r1][0];
		server[r1][0] = t;

		t = server[r0][1];
		server[r0][1] = server[r1][1];
		server[r1][1] = t;

		t = server[r0][2];
		server[r0][2] = server[r1][2];
		server[r1][2] = t;
	}
}

void shufflePools(){
	int r0, r1, i, t;
	for (i = 0; i < P/2; ++i){
		r0 = rand() % P;
		r1 = rand() % P;

		t = pool[r0];
		pool[r0] = pool[r1];
		pool[r1] = t;
	}

}
void shuffleRows(){
	int r0, r1, i, t;
	for (i = 0; i < R/2; ++i){
		r0 = rand() % R;
		r1 = rand() % R;

		t = rows[r0];
		rows[r0] = rows[r1];
		rows[r1] = t;
	}
}
int cmp(int *a, int *b){
	if (a[2] > b[2]) return 1;
	if (a[2] < b[2]) return -1;
	return 0;
}

int main(void){
	/*srand(time(NULL));*/
	srand(time(NULL)+clock());
	int i, a, b, j, c, s, k, l, flag, p, w;

	/* Read INPUT */
	/* Read basic values */
	scanf("%d %d %d %d %d\n", &R, &S, &U, &P, &M);

	/* Read unavailable slots */
	for(i = 0; i < U; ++i){
		scanf("%d %d\n", &a, &b);
		slot[a][b] = -1;
	}

	/* Read servers */
	for(i = 0; i < M; ++i){
		scanf("%d %d\n", &server[i][0], &server[i][1]);
		server[i][2] = i+1;
		server[i][3] = -1;
		server[i][4] = -1;
	}

	nservers = i;

	/*printf("%d\n", nservers);

	for (i = 0; i < R; ++i){
		for (j = 0; j < S; ++j){
			printf("%d\t", slot[i][j]);
		}
		printf("\n");
	}*/

	/*for (i = 0; i < nservers; ++i)
		printf("(%d, %d, %d)\t", server[i][2], server[i][0], server[i][1]);

	shuffleServers();
	printf("\n");



	for (i = 0; i < nservers; ++i)
		printf("(%d, %d, %d)\t", server[i][2], server[i][0], server[i][1]);
	
	printf("\n");*/

	shuffleServers();
	for (i = 0; i < R; ++i){
		c = 1;
		for (j = S - 1; j >= 0; --j){
			if (slot[i][j] != 0){
				spaces[i][j] = 0;
				c = 1;
			} else {
				spaces[i][j] = c++;
			}
		}
	}

	/*printf("\n");

	for (i = 0; i < R; ++i){
		for (j = 0; j < S; ++j){
			printf("%d\t", spaces[i][j]);
		}
		printf("\n");
	}*/

	for (i = 0; i < R; ++i) {
		rows[i] = i;
	}

	for (k = 0; k < nservers; ++k){
		shuffleRows();
		flag = 1;
		s = server[k][0];
		for (w = 0; w < R && flag; ++w)
			i = rows[w];
			for (j = 0; j < S && flag; ++j){
				if (spaces[i][j] >= s){
					server[k][3] = i;
					server[k][4] = j;
					for (l = 0; l < s; ++l){
						slot[i][j+l] = server[k][2];
						spaces[i][j+l] = 0;
					}
					flag = 0;
				}
			}
	}
	
	/*for (i = 0; i < R; ++i){
		for (j = 0; j < S; ++j){
			printf("%d\t", slot[i][j]);
		}
		printf("\n");
	}
	printf("\n");*/

	for (i = 0; i < P; ++i) {
		pool[i] = i;
	}
	
	qsort(server,nservers,sizeof(int[5]),(int(*)(const void*,const void*))cmp);

	p = 0;
	for (k = 0; k < nservers; ++k){
		if (server[k][3] == -1) {
			printf("x\n");
		} else {
			printf("%d %d %d\n", server[k][3], server[k][4], pool[p++]);
		}
		if (p >= P){
			shufflePools();
			p = 0;
		}
	}

	return 0;
}
