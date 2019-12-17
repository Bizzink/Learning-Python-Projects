import Globals as g


class RestrictedTile:
    def __init__(self, pos, revealed, flagged, near_bombs):
        self.row, self.col = pos[0], pos[1]
        self.revealed = revealed
        self.flagged = flagged
        self.near_bombs = near_bombs
        self.potentials = []
        self.override = 1

        if not self.revealed:
            self.near_bombs = -1

    def get_neighbours(self):
        """returns 8 neighbouring tiles"""
        neighbours = []

        rows = board[self.row - 1: self.row + 2]
        if self.row == 0: rows = board[self.row: self.row + 2]
        if self.row == g.rows - 1: rows = board[self.row - 1: self.row + 1]

        for row in rows:
            tiles = row[self.col - 1: self.col + 2]
            if self.col == 0: tiles = row[self.col : self.col + 2]
            if self.col == g.cols: tiles = row[self.col - 1: self.col + 1]

            for tile in tiles:
                neighbours.append(tile)

        return neighbours

    def near_flags(self):
        """returns number of neighbouring tiles that are flagged"""
        count = 0

        for neighbour in self.get_neighbours():
            if neighbour.flagged:
                count += 1

        return count

    def near_hidden(self):
        """returns number of hidden neighboring tiles"""
        count = 0

        for neighbour in self.get_neighbours():
            if not neighbour.revealed:
                count += 1

        return count

    def near_potential(self):
        """for each hidden, un-flagged bomb in neighbours: add potential for it to be a bomb based on this tile
            0 = all bombs are flagged
            -1 = all hidden are bombs
            if there are more flags than bombs, the flags will be highlighted purple"""
        value = 0

        if self.near_bombs == self.near_flags():
            #  all near bombs are flagged
            value = 0

        elif self.near_bombs == self.near_hidden():
            # all near hidden tiles are bombs
            value = -1

        elif self.near_hidden() - self.near_flags() > 0:
            remaining_bombs = self.near_bombs - self.near_flags()
            remaining_spots = self.near_hidden() - self.near_flags()
            value = (remaining_bombs / remaining_spots)

        if self.near_bombs - self.near_flags() < 0:
            #  more flags than bombs
            # this will highlight flagged tiles
            self.override = -3

            for tile in self.get_neighbours():
                if tile.flagged:
                    tile.override = -2

        for neighbour in self.get_neighbours():
            if not neighbour.revealed and not neighbour.flagged:
                neighbour.potentials.append(value)

    def calc_potential(self):
        result = 0

        for value in self.potentials:
            if value <= 0:
                self.override = value

            result += value

        return result / len(self.potentials)


board = []


def get_board():
    board.clear()

    for row in g.tiles:
        new_row = []

        for tile in row:
            new_tile = RestrictedTile((tile.row, tile.col), tile.revealed, tile.flagged, tile.count_near_bombs())
            new_row.append(new_tile)

        board.append(new_row)


def update_potentials():
    get_board()

    for row in board:
        for tile in row:
            if tile.revealed:
                tile.near_potential()

    for row in board:
        for tile in row:
            if tile.override == -2:
                g.tiles[tile.row][tile.col].highlight((255, 0, 255), 75)
            elif tile.override == -3:
                g.tiles[tile.row][tile.col].highlight((255, 0, 255), 10)

            elif len(tile.potentials) > 0 and not tile.revealed:
                tile.calc_potential()
                actual_tile = g.tiles[tile.row][tile.col]

                if tile.override == 0:
                    actual_tile.highlight((0, 255, 0), 75)
                elif tile.override == -1:
                    actual_tile.highlight((255, 0, 0), 75)
                else:
                    actual_tile.highlight((0, 0, 255), int(tile.calc_potential() * 128))

            else:
                g.tiles[tile.row][tile.col].highlight(0, 0, reset = True)
