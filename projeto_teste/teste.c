#include <stdio.h>

// Função que recebe um inteiro
void minha_funcao(int numero) {
    printf("O número recebido é: %d\n", numero);
}

int main() {
    char c = '7';  // Um caractere representando um número

    // Converter o char para int
    int numero = c - '0';  

    // Chamar a função passando o número convertido
    minha_funcao(numero);

    return 0;
}