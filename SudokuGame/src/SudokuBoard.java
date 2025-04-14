public class SudokuBoard {
    private final int n = 9;
    private int board[][] ;

    public SudokuBoard() {
        this.board = new int[n][n];
    }

    public int getValue(int row, int col){
        return board[row][col];
    }

    public int[][] getBoard(){
        return board;
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

    public void setValue(int row, int col, int value) {
        if (row >= 0 && row < 9 && col >= 0 && col < 9 && value >= 0 && value <= 9) {
            board[row][col] = value;
        } else {
            System.err.println("posiçào invalida.");
        }
    }

}
