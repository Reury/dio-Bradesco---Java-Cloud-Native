package poo;

public class ReprodutorMusical {

    private String musicaSelecionada;

    public void tocar() {
        if (musicaSelecionada != null && !musicaSelecionada.isEmpty()) {
            System.out.println("Tocando a música: " + musicaSelecionada);
        } else {
            System.out.println("Nenhuma música selecionada.");
        }
    }

    public void pausar() {
        if (musicaSelecionada != null && !musicaSelecionada.isEmpty()) {
            System.out.println("Pausando a música: " + musicaSelecionada);
        } else {
            System.out.println("Nenhuma música selecionada para pausar.");
        }
    }

    public String selecionarMusica(String musica) {
        if (musica != null && !musica.isEmpty()) {
            this.musicaSelecionada = musica;
            System.out.println("Música selecionada: " + musica);
            return musica;
        } else {
            System.out.println("Seleção de música inválida.");
            return null;
        }
    }

    public String getMusicaSelecionada() {
        return musicaSelecionada;
    }
}