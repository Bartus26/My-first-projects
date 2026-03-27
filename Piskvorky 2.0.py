

# TIC-TAC-TOE  2.0 - Finish

#DEFINITIONS

# Function for print  playing field
def grid_output (grid,col_input):
    print(f"\nCURRENT GAME GRID :")
    column_number_str = [str(num) for num in range(1,col_input+1)]
    print(f"  {' '.join(column_number_str)}")  
    row_pos = 1  
    for row in grid:
        print(f"{row_pos} {' '.join(row)}")
        row_pos +=1
#Function for player's move
def player_input (player, grid,y_input,x_input,empty_sign):
    print(f"Playing player: {player}")

    while True:
        # Except input int
        try:
            # Check when is place empty
            while True:
                # Check when is input in range
                while True:
                    y_gmr = int(input(f"Player {player} enter row coordinate: "))
                    if y_gmr <= y_input:
                        break
                    else:
                        print(f"You insert number out of range 1-{y_input}")
                # Check when is input in range
                while True:
                    x_gmr = int(input(f"Player {player} enter column coordinate: "))
                    if x_gmr <= x_input:
                        break
                    else:
                        print(f"You insert number out of range 1-{x_input}")
                if grid[y_gmr-1][x_gmr-1] == empty_sign:
                    grid[y_gmr-1][x_gmr-1] = player
                    break
                
                else:
                    print("Occupied place. Try again")
            break    
        except Exception:
            print(f"Insert correct input. Only numbers for row 1-{y_input}, for columns 1-{x_input}")

# function for checking the winner in rows
def check_winner_row (player, grid):
    for row in grid:
        if len(row) == row.count(player):
            return True
        
#function for checking the winner in columns       
def check_winner_columns(player, grid):
    for column_index in range(col_input):
        rows_index = []
        for row_index in range(row_input):    
            rows_index.append(grid[row_index][column_index])
            if len(grid) == rows_index.count(player):
                return True
            
#function for checking the winner in diagonals 
def check_winner_diagonal(player, grid):
    rows_index = []
    mover = 0
    for row_index in range(row_input):    
        rows_index.append(grid[row_index][mover])
        mover+=1
        if len(grid) == rows_index.count(player):
            return True
    rows_index = []
    mover-=1
    for row_index in range(row_input):    
        rows_index.append(grid[row_index][mover])
        mover-=1
        if len(grid) == rows_index.count(player):
            return True
        
def check_draw (grid, empty_sign):
    field_for_draw = [item for group in grid for item in group]
    if field_for_draw.count(empty_sign) == 0:
        return True


# User input to size grid
print("======= GRID SIZE =========")
row_input = int(input("Enter number of row: "))
col_input = int(input("Enter number of column: "))

# Creating 2D grid
empty_sign = "_"
grid = [[empty_sign for column in range(col_input)] for row in range(row_input)]


#main
grid_output(grid,col_input)
while True:
    
    # Body for player "O"
    player = "O"
    player_input(player, grid,row_input,col_input,empty_sign)
    grid_output(grid,col_input)
    if check_winner_row(player,grid) == True or check_winner_columns(player, grid) == True or check_winner_diagonal(player, grid) == True:
        print(f"Player: {player} wins!")
        break
    elif check_draw(grid, empty_sign) == True:
        print(f"===== DRAW =====")
        break

    # Body for player "x"
    player = "x"
    player_input(player, grid,row_input,col_input,empty_sign)
    grid_output(grid,col_input)
    if check_winner_row(player,grid) == True or check_winner_columns(player, grid) == True or check_winner_diagonal(player, grid) == True:
        print(f"Player: {player} wins!")
        break
    elif check_draw(grid, empty_sign) == True:
        print(f"===== DRAW =====")
        break
