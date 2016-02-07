#include <stdio.h>
#include <stdlib.h>
#include <limits.h>

/* R: Number of rows (max 1000) */
/* S: Number of slots per row (max 1000) */
/* U: Number of unavailable slots (max R*S -> 1000000) */
/* P: Number of pools (max 1000) */
/* M: Number of servers (max R*S -> 1000000) */
int R,S,U,P,M;

/* Server: max(1000000), [0]->size, [1]->capacity */
int server[1000000][2];
/* Result: Server index, [0]->row, [1]->slot, [2]->pool */
int result[1000000][3];
/* Slots: [row][slot] -> server_number+1, 0 if empty, -1 if unavailable */
int slot[1000][1000];
/* Pool: [0]->total, [1]->max capacity for a single row, [2]->row index max */
int pool[1000][3];

int main(void){
  int i,a,b,j,r,s;
  int p[1000];
  char tmp[100];
  int score=INT_MAX;

  /* Read INPUT */
  /* Read basic values */
  scanf("%d %d %d %d %d",&R,&S,&U,&P,&M);

  /* Read unavailable slots */
  for(i=0;i<U;++i){
    scanf("%d %d",&a,&b);
    slot[a][b]=-1;
  }

  /* Read servers */
  for(i=0;i<M;++i){
    scanf("%d %d\n",&server[i][0],&server[i][1]);
  }

  /* Read OUTPUT */
  for(i=0;i<M;++i){
    scanf("%[^\n]\n",tmp);
    if(tmp[0]!='x'){
      sscanf(tmp,"%d %d %d",&result[i][0],&result[i][1],&result[i][2]);
    } else {
      result[i][0]=-1;
    }
  }


  /* Validate */
  for(i=0;i<M;++i){
    /* Check if pool number is valid */
    if(result[i][2]>=P){
      printf("Impossible pool number %d\n", result[i][2]);
      return 1;
    }
    /* Fill slots and check if available */
    for(j=0;j<server[i][0];++j){
      r = result[i][0];
      s = result[i][1]+j;
      if(r==-1){
        continue;
      }
      if(slot[r][s]!=0){
        if(slot[r][s]==-1){
          printf("Unavailable slot:\nRow: %d\nSlot: %d\nServer: %d\n",r,s,i);
          return 1;
        }
        printf("Slot with more than one server:\nRow: %d\nSlot: %d\nServer: %d\nNew Server: %d\n",r,s,slot[r][s]-1,i);
        return 1;
      }
      slot[r][s]=i+1;
    }
  }

  printf("Valid Output\n");
  /* Fill pool array */
  for(i=0;i<R;++i){
    for(j=0;j<P;++j){
      p[j]=0;
    }
    for(j=0;j<S;++j){
      if(slot[i][j]>0 && (j==0 || slot[i][j]!=slot[i][j-1])){
        p[result[slot[i][j]-1][2]]+=server[slot[i][j]-1][1];
      }
    }
    for(j=0;j<P;++j){
      pool[j][0]+=p[j];
      if(p[j]>pool[j][1]){
        pool[j][1]=p[j];
        pool[j][2]=i;
      }
    }
  }
  /* Score */
  for(i=0;i<P;++i){
    if(pool[i][0]-pool[i][1]<score){
      score = pool[i][0]-pool[i][1];
    }
  }
  printf("Score: %d\n",score);

  return 0;
}
