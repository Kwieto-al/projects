#include <stdio.h>

int hashval(char* val);

void main(){
    char *dict[101];
    dict[hashval("hello")]="hi!";
    printf("%s",dict[hashval("hello")]);


}

int hashval(char* val){
    int total=0;
    for (int i=0;i<sizeof(val);i++){
        total= total+ (int) val[i];
    }
    return total%101;
}