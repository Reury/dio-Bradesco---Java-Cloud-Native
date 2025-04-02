package poo;

public class Iphone {
    private ReprodutorMusical reprodutor;
    private AparelhoTelefonico aparelho;
    private NavegadorNaInternet navegador;

    public Iphone() {
        this.reprodutor = new ReprodutorMusical();
        this.aparelho = new AparelhoTelefonico();
        this.navegador = new NavegadorNaInternet();
    }

    public ReprodutorMusical getReprodutor() {
        return reprodutor;
    }

    public AparelhoTelefonico getAparelho() {
        return aparelho;
    }

    public NavegadorNaInternet getNavegador() {
        return navegador;
    }


    public void tocarMusica() {
        reprodutor.tocar();
    }

    public void ligarPara(String numero) {
        aparelho.ligar(numero);
    }

    public void exibirPaginaWeb(String url) {
        navegador.exibirPagina(url);
    }


}