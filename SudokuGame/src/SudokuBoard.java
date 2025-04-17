public class SudokuBoard {
    private static final int GRID_SIZE = 9;
    private int board[][] ;
    private boolean[][] initialCells; // To track which cells were part of the initial puzzle

    public SudokuBoard() {
        this.board = new int[GRID_SIZE][GRID_SIZE];
    }

    public int getValue(int row, int col){
        return board[row][col];
    }

    public int[][] getBoard(){
        return board;
    }

    public SudokuBoard(int[][] initialBoard) {
        this.board = new int[GRID_SIZE][GRID_SIZE];
        this.initialCells = new boolean[GRID_SIZE][GRID_SIZE];
        initializeBoard(initialBoard);
    }

    public void printBoard() {
        for (int i = 0; i < 9; i++) {
            if (i % 3 == 0 && i != 0) {
                System.out.println("-----------");
            }
            for (int j = 0; j < 9; j++) {
                if (j % 3 == 0 && j != 0) {
                    System.out.print("|");
                }
                System.out.print(board[i][j] + " ");
            }
            System.out.println();
        }
    }
    private void initializeBoard(int[][] initialBoard) {
        for (int row = 0; row < GRID_SIZE; row++) {
            for (int col = 0; col < GRID_SIZE; col++) {
                this.board[row][col] = initialBoard[row][col];
                if (initialBoard[row][col] != 0) {
                    this.initialCells[row][col] = true; // Mark as an initial cell
                }
            }
        }
    }

    public boolean placeNumber(int row, int col, int number) {
        // Adjust for 0-based indexing (user enters 1-9)
        int actualRow = row - 1;
        int actualCol = col - 1;

        // Input validation
        if (row < 1 || row > GRID_SIZE || col < 1 || col > GRID_SIZE || number < 1 || number > GRID_SIZE) {
            System.out.println("Invalid input: Row, column, and number must be between 1 and 9.");
            return false;
        }

        // Check if the cell is part of the initial puzzle
        if (initialCells[actualRow][actualCol]) {
            System.out.println("Cannot change an initial puzzle number.");
            return false;
        }

        // Check if the placement follows Sudoku rules
        if (isValidPlacement(actualRow, actualCol, number)) {
            board[actualRow][actualCol] = number;
            return true;
        } else {
            System.out.println("Invalid move: Number " + number + " conflicts in row, column, or 3x3 box.");
            return false;
        }
    }

    private boolean isNumberInRow(int row, int number) {
        for (int col = 0; col < GRID_SIZE; col++) {
            if (board[row][col] == number) {
                return true;
            }
        }
        return false;
    }

    private boolean isNumberInColumn(int col, int number) {
        for (int row = 0; row < GRID_SIZE; row++) {
            if (board[row][col] == number) {
                return true;
            }
        }
        return false;
    }

    private boolean isNumberInBox(int row, int col, int number) {
        int boxStartRow = row - row % 3;
        int boxStartCol = col - col % 3;

        for (int r = boxStartRow; r < boxStartRow + 3; r++) {
            for (int c = boxStartCol; c < boxStartCol + 3; c++) {
                if (board[r][c] == number) {
                    return true;
                }
            }
        }
        return false;
    }

    private boolean isValidPlacement(int row, int col, int number) {
        return !isNumberInRow(row, number) &&
                !isNumberInColumn(col, number) &&
                !isNumberInBox(row, col, number);
    }

    public boolean isSolved() {
        for (int row = 0; row < GRID_SIZE; row++) {
            for (int col = 0; col < GRID_SIZE; col++) {
                if (board[row][col] == 0) {
                    return false; // Found an empty cell, not solved yet
                }
            }
        }
        // Optional: Add a full board validation here if needed,
        // but the placement logic should prevent invalid final states.
        return true; // All cells are filled
    }



}
