package poo;

public class AparelhoTelefonico {

    private String numeroChamada;

    public void ligar(String numero) {
        if (numero != null && !numero.isEmpty()) {
            this.numeroChamada = numero;
            System.out.println("Ligando para: " + numero);
        } else {
            System.out.println("Número inválido.");
        }
    }

    public void atender() {
        if (numeroChamada != null && !numeroChamada.isEmpty()) {
            System.out.println("Atendendo chamada de: " + numeroChamada);
        } else {
            System.out.println("Nenhuma chamada para atender.");
        }
    }

    public void iniciarCorreioVoz() {
        System.out.println("Iniciando correio de voz.");
    }

    public String getNumeroChamada() {
        return numeroChamada;
    }
}