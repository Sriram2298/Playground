#include<stdio.h>
int main()
{
  int a=789,b,c;
  scanf("%d",&a);
  b=a%10;
  c=(a/100)%10;
  printf("%d",b+c);
  
  return 0;
}