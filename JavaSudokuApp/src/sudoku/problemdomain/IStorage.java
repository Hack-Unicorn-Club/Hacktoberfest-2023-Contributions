package sudoku.problemdomain;

import java.io.IOException;

public class IStorage {
    void updateGameData(SudokuGame game) throws IOException;
    SudokuGame getGameData() throws IOException;
}
