package poo;

public class Main {
    public static void main(String[] args) {
        // Criando um objeto iPhone
        Iphone meuIphone = new Iphone();

        // Usando o ReprodutorMusical
        meuIphone.getReprodutor().selecionarMusica("Bohemian Rhapsody");
        meuIphone.getReprodutor().tocar();
        meuIphone.getReprodutor().pausar();

        // Usando o AparelhoTelefonico
        meuIphone.getAparelho().ligar("123456789");
        meuIphone.getAparelho().atender();
        meuIphone.getAparelho().iniciarCorreioVoz();

        // Usando o NavegadorNaInternet
        meuIphone.getNavegador().exibirPagina("www.google.com");
        meuIphone.getNavegador().adicionarNovaAba();
        meuIphone.getNavegador().atualizarPagina();

        // Obtendo informações
        System.out.println("Música selecionada: " + meuIphone.getReprodutor().getMusicaSelecionada());
        System.out.println("Número da chamada: " + meuIphone.getAparelho().getNumeroChamada());
        System.out.println("Página exibida: " + meuIphone.getNavegador().getPaginaExibida());
        System.out.println("Número de abas: " + meuIphone.getNavegador().getNumeroAbas());
    }
}