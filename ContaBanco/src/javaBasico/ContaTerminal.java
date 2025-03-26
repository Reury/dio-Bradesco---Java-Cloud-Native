package javaBasico;

import java.math.BigDecimal;
import java.util.Scanner;

public class ContaTerminal {
	
	private String nome;
	private int numero;
	private String agencia;
	private BigDecimal saldo;
		

	public static void main(String[] args) {
		Scanner input = new Scanner(System.in);
		ContaTerminal conta = new ContaTerminal(); 

		System.out.print("Por favor, digite o número da Agência: ");
		conta.agencia = input.nextLine(); 

		System.out.print("Por favor, digite o número da Conta: ");
        conta.numero = input.nextInt(); 
        input.nextLine();
        
        System.out.print("Por favor, digite o nome do Cliente: ");
        conta.nome = input.nextLine();
        
        System.out.print("Por favor, digite o saldo da Conta: ");
        conta.saldo = input.nextBigDecimal(); 

        System.out.println("Olá " + conta.nome + ", obrigado por criar uma conta em nosso banco, sua agência é " + conta.agencia + ", conta " + conta.numero + " e seu saldo " + conta.saldo + " já está disponível para saque.");
		input.close();
	}

}
