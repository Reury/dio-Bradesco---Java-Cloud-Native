import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.Assertions; // Correct import for Assertions
import java.io.ByteArrayOutputStream;
import java.io.PrintStream;

// filepath: /home/harry/dev/bootcamps/dio-Bradesco---Java-Cloud-Native/poo/src/poo/ReprodutorMusicalTest.java
package poo;




public class ReprodutorMusicalTest {

    private ReprodutorMusical reprodutorMusical;
    private ByteArrayOutputStream outputStream;

    @BeforeEach
    public void setUp() {
        reprodutorMusical = new ReprodutorMusical();
        outputStream = new ByteArrayOutputStream();
        System.setOut(new PrintStream(outputStream));
    }

    @Test
    public void testTocarComMusicaSelecionada() {
        // Arrange
        String musica = "Imagine - John Lennon";
        reprodutorMusical.selecionarMusica(musica);

        // Act
        reprodutorMusical.tocar();

        // Assert
        assertEquals("Tocando a música: " + musica + System.lineSeparator(), outputStream.toString());
    }

    @Test
    public void testTocarSemMusicaSelecionada() {
        // Act
        reprodutorMusical.tocar();

        // Assert
        assertEquals("Nenhuma música selecionada." + System.lineSeparator(), outputStream.toString());
    }
}