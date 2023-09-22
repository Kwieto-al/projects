#include <stdio.h>
#include <string.h>
#include <stdlib.h>
char* readfile(char filename[]);

typedef struct node {
    char *val;
    struct node * next;
} node_t;
node_t* createlist(char list[]);
long pathfinding(int num1,int num2,node_t* head);

void main(){
    node_t *head= NULL;
    char* textfile = readfile("Day3.txt");
    head=createlist(textfile);
    node_t *current= NULL;
    long results=1;
    int possibilities[5][2]={{1,1},{3,1},{5,1},{7,1},{1,2}};
    for (int count=0; count<5;count++){
        results=results*pathfinding(possibilities[count][0],possibilities[count][1],head);
    }
    printf("%d",results);

}

long pathfinding(int num1,int num2,node_t* head){
    node_t* current=NULL;
    current=head;
    int i=0;
    int treecount=0;
    while (current->next!=NULL){
        char *row= current->val;
        if (row==NULL){
            break;
        }
        char character= (char) row[i%31];
        
        if(character==*"#"){
            treecount++;
        }
        i=i+num1;
        for (int j=0;j<num2;j++){
            current=current->next;
        }
    }
    return treecount;
}

char* readfile(char filename[]) {
    FILE    *textfile;
    char    *text;
    long    numbytes;
     
    textfile = fopen(filename, "r");
    if(textfile == NULL)
        return "1";
     
    fseek(textfile, 0L, SEEK_END);
    numbytes = ftell(textfile);
    fseek(textfile, 0L, SEEK_SET);  
 
    text = (char*)calloc(numbytes, sizeof(char));   
    if(text == NULL)
        return "1";
 
    fread(text, sizeof(char), numbytes, textfile);
    fclose(textfile);
  
    return text;
}

node_t* createlist(char list[]){
    node_t * head = NULL;
    head = (node_t *) malloc(sizeof(node_t));
    char *value = strtok(list, "\n");
    head->val = value;
    node_t *current= NULL;
    current = (node_t *) malloc(sizeof(node_t));
    head->next= current;
    for (int i=1; i<1000;i++){
        node_t *next= NULL;
        next = (node_t *) malloc(sizeof(node_t));
        value = strtok(NULL, "\n");
        current->val = value;
        current->next=next;
        current=next;
    }
    return head;
}