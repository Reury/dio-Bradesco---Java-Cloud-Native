import java.util.Scanner;

//TIP To <b>Run</b> code, press <shortcut actionId="Run"/> or
// click the <icon src="AllIcons.Actions.Execute"/> icon in the gutter.
public class Main {
    public static void main(String[] args) {
        // Example initial Sudoku puzzle (0 represents empty cells)
        // Difficulty: Easy
        int[][] initialPuzzle = {
                {5, 3, 0, 0, 7, 0, 0, 0, 0},
                {6, 0, 0, 1, 9, 5, 0, 0, 0},
                {0, 9, 8, 0, 0, 0, 0, 6, 0},
                {8, 0, 0, 0, 6, 0, 0, 0, 3},
                {4, 0, 0, 8, 0, 3, 0, 0, 1},
                {7, 0, 0, 0, 2, 0, 0, 0, 6},
                {0, 6, 0, 0, 0, 0, 2, 8, 0},
                {0, 0, 0, 4, 1, 9, 0, 0, 5},
                {0, 0, 0, 0, 8, 0, 0, 7, 9}
        };

        SudokuBoard game = new SudokuBoard(initialPuzzle);
        Scanner scanner = new Scanner(System.in);

        System.out.println("--- Sudoku Game ---");
        System.out.println("Digite Linha, coluna, e o numero (de 1-9). Digite 0 para sair.");

        while (!game.isSolved()) {
            game.printBoard();
            System.out.print("digite sua jogada (row col num): ");

            int row = scanner.nextInt();
            if (row == 0) break; // Quit condition

            int col = scanner.nextInt();
            if (col == 0) break; // Quit condition

            int num = scanner.nextInt();
            if (num == 0) break; // Quit condition


            if (!game.placeNumber(row, col, num)) {
                System.out.println("Try again."); // Error messages are printed within placeNumber
            }
            System.out.println(); // Add a blank line for readability
        }

        if (game.isSolved()) {
            System.out.println("\nCongratulations! You solved the Sudoku!");
            game.printBoard();
        } else {
            System.out.println("\nExiting game.");
            game.printBoard(); // Show the final state
        }

        scanner.close();
    }
}