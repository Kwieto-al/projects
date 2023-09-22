#include <stdio.h>
#include <string.h>
#include <stdlib.h>

typedef struct node {
    char *val[101];
    struct node * next;
} node_t;

char* readfile(char filename[]);
node_t* createlist(char list[]);


void main(){
    char* text= readfile("Day4.txt");
    node_t* head=NULL;
    head = (node_t *) malloc(sizeof(node_t));
    head=createlist(text);
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
    char *value = strtok(list, "\n\n");
    char* lines[5];
    int count=0;
    lines[count]= strtok(value,"\n");
    char* newval;
    while(1){
        newval=strtok(NULL,"\n");
        
    }