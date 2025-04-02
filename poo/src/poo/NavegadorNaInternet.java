package poo;

public class NavegadorNaInternet {

    private String paginaExibida;
    private int numeroAbas = 1;
    public void exibirPagina(String url) {
        if (url != null && !url.isEmpty()) {
            this.paginaExibida = url;
            System.out.println("Exibindo página: " + url);
        } else {
            System.out.println("URL inválida.");
        }
    }

    public void adicionarNovaAba() {
        numeroAbas++;
        System.out.println("Nova aba adicionada. Total de abas: " + numeroAbas);
    }

    public void atualizarPagina() {
        if (paginaExibida != null && !paginaExibida.isEmpty()) {
            System.out.println("Atualizando página: " + paginaExibida);
        } else {
            System.out.println("Nenhuma página para atualizar.");
        }
    }

    public String getPaginaExibida() {
        return paginaExibida;
    }

    public int getNumeroAbas() {
        return numeroAbas;
    }
}