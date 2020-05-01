# my attempt at tower/skyscraper solver
#receive list as input containing integers from 0 to n. 
#expected length is 4n 
#total squares is n**2
#actual values in squares range from 1 to n
#each square belongs to only 1 row and 1 column it both affects the other potential values in each row/column as well as can be affected.

class Tower(object):
  """This class contains the following properties and methods:
      .address    .value          .solved         .possible_values
      .remove()   .mark_solved()  .self_check()   .not_solved()
  
  Arguments:
      object {object} -- [Not sure why this is here as an argument other than to inherit properties of a generic object]
  
  Returns:
      [string] -- It doesn't specifically return anything, but with repr function it allows this object to be presented in a human readable way.
  """
  
  def __init__(self, row, column, size):
    self.address = (row, column)
    self.value = 0
    self.solved = False
    self.possible_values = set(range(1,size+1))

  def __repr__(self):
    if self.value == 0:
      result = self.possible_values
    else:
      result = self.value
    return repr(result)

  def __len__(self):
    return len(self.possible_values)

  def remove(self, value):
    """Method to remove a value from the set of possible solutions. This may result in a reduction to only 1 possibility. This method will be typically followed by self_check() or another update type method from another class.
    
    Arguments:
        value {int} -- Integer value that will be removed from the set.
    """
    self.possible_values.discard(value)

  def mark_solved(self, val):
    """Method to change the solved-flag to True. It also removes all other possible values from the possible_values set ensuring that the value passed in is the only possible-value
    
    Arguments:
        val {int} -- This integer should be in the range between 1 and N inclusive; N represents the length of the side of the host-grid-oblect that contains this cell.
    """
    self.value = val
    self.solved = True
    self.possible_values.clear()
    self.possible_values.add(val)

  def self_check(self):
    """This method checks to see if the number of possible values is 1.
    
    Returns:
        Boolean -- True if the number of possible values is 1. 
                   False if more than 1 possible value exists.
    """
    return len(self.possible_values)==1

  def not_solved(self):
    """This method checks the solved-flag and returns its opposite. Designed to be a helper function to determine if the cell in host-grid-object has already been processed fully.
    
    Returns:
        Boolean -- True if the cell has not been solved. 
                   False if the cell has been solved.
    """
    return not self.solved

class Line(object):
  def __init__(self, size, type, number, clue):
    self.row_or_column = type
    self.row_or_column_number = number
    self.name = self.row_or_column + str(self.row_or_column_number)
    self.possible_heights = set(range(1,size + 1))
    self.values = [0 for _i in range(size)]
    self.clue_pair = clue
    self.unsolved_values = set(self.possible_heights)
    self.visible = [0,0]
    self.towers = set()

  def update_visible(self):
    self.visible[0] = self.visible_towers(self.values)
    self.visible[1] = self.visible_towers(list(reversed(self.values)))

  def visible_towers(self, heights):
    count = 0
    if len(heights) > 0 and max(heights) > 0:
      currentMax = 0
      for height in heights:
        if height > currentMax:
          count += 1
          currentMax = height
    return count

  def line_satisfy_clues(self):
    return self.visible == self.clue_pair


class TowerPuzzle(object):
  def __init__(self):
    self.solved = set()
    self.deduced = set()
    self.cells = []
    self.rows = []
    self.cols = []
    self.build_sequence()
    
  def build_sequence(self):
    self.size = self.prompt_for_size()
    self.total_squares = self.size ** 2
    self.grid_range = list(range(self.size))
    self.value_range = list(range(1, self.size + 1))
    self.clues = self.prompt_for_clues()
    self.givens = self.prompt_for_given_squares()
    self.cells = [[Tower(row, column, self.size) for column in range(self.size)] for row in range(self.size)]
    self.make_row_col()
    self.solver()

  def make_row_col(self):
    for i in self.grid_range:
      self.rows.append(Line(self.size, "row", i, self.clues[0][i]))
      self.cols.append(Line(self.size, "col", i, self.clues[1][i]))



  def prompt_for_size(self):
    try:
      size = int(input("Please enter the size of board you'd like to play:"))
    except:
      print("Not an integer. Try Again")
      return self.prompt_for_size()
    else:
      if size < 1:
        print("Not a positive integer. Try again!")
        return self.prompt_for_size()
      print("\tSize received:", size, "\n\t\tTotal Squares to be made:", size ** 2)
      return size
  
  def prompt_for_clues(self):
    valid_size = False
    #loop through prompt to get a list of expected size
    while not valid_size:
      clue_string = input("\nClues should be integers from 0 to " + str(self.size) + " (size of board):\n\tStarting from upper left and going clockwise, Please enter clues seperated by ','\n>>>")
      clue_list_of_strings = clue_string.split(',')
      valid_size = 4 * self.size == len(clue_list_of_strings)
      if not valid_size:
        print("\nNumber of clues did not match expected number. Try Again!")

    #convert list of strings to list of integers and validate values in bounds
    try:
      clue_list = [int(clue) for clue in clue_list_of_strings]
    except:
      print("\nError: One or more clues was not an integer.Please Try Again!")
      return self.prompt_for_clues()
    else:
      if self.size < max(clue_list) or 0 > min(clue_list):
        print("\n1 or more of your clues are outside of the boundary  values of 0 to ", self.size, ".\nTry again!")
        return self.prompt_for_clues()
  
    #arrange the clues into usable format
    #clues [[ list of tuples representing L and R clues per row ], 
    #       [ list of tuples representing T and B clues per col ]]
    #clues[0] = [(row_0_left, row_0_right), ..., (row_N-1_left, row_N-1_right)]  
    #clues[1] = [(col_0_left, col_0_right), ..., (col_N-1_left, col_N-1_right)]

    clues = [[],[]]
    N = self.size
    max_value = N +1
    right_adjustment = N
    bottom_adjustment = 3 * N - 1
    left_adjustment = 4 * N - 1
    for i in range(self.size):
      top = clue_list[i]
      right = clue_list[right_adjustment + i]
      bottom = clue_list[bottom_adjustment - i]
      left = clue_list[left_adjustment - i]
      #validate pairs of clues
      if sum([top, bottom]) > max_value or sum([left, right]) > max_value:
        print("\n1 or more pairs of clues exceeds the maximum pair combination sum. Try again!")
        return self.prompt_for_clues()
      clues[0].append([left, right])
      clues[1].append([top, bottom])
    print("\nClues received:", clue_list)
    return clues

  def prompt_for_given_squares(self):
    givens = [(-1,-1,-1)]
    given_addresses = set()
    v_range = list(self.value_range)
    try:
      number_of_givens = int(input("\nHow many towers/squares are given? (0 to " + str(self.total_squares) + "):"))
    except:
      print("Please enter an interger next time.")
      return self.prompt_for_given_squares()
    else:
      if number_of_givens not in range(self.total_squares + 1):
        print("Please enter a value between 0 and", self.total_squares, "next time:")
        return self.prompt_for_given_squares()
    while number_of_givens != 0:
      response = input(str(number_of_givens) + " squares left.\nEnter data in this format: 'row, col, value'\tusing numbers 1 through " + str(self.total_squares))
      if response.count(',') != 2:
        print("\n\tNot enough elements!")
        continue
      try:
        given = [int(i) for i in response.split(',')]
      except:
        print("\n\tOnly integers please.")
        continue
      if max(given) not in v_range or min(given) not in v_range:
        print("\n\t1 or more values outside of range.")
        continue
      row = given[0] - 1
      col = given[1] - 1
      value = given[2]
      if (row, col) in given_addresses:
        print("\n\tThat square has already been given.")
        continue
      given_addresses.add((row, col))
      givens.append((row, col, value))
      number_of_givens -= 1
    if len(givens) > 1:
      print("\n\tThe following towers/squares will be added:", givens[1:])
    else:
      print("\n\tNo given towers/squares will be added.")
    return givens

  def play_again(self):
    response = input("Would you like to play again?\t\t'Y' or 'y' for yes. anything else  for no:")
    if response.lower() == 'y':
      TowerPuzzle()
    return None

  


  def update_deduced_set(self, cell):
    """This Method adds the cell's address to the puzzle's deduced_list if the number of possible solutions is 1 and if it hasn't been fully processed as solved.
    
    Keyword Arguments:
        cell {Tower Class} -- The underlying cell/tower in the grid
    """
    if cell.self_check() and cell.not_solved():
      self.deduced.add(cell.address)

  def set_cell_to(self, row, column, value):
    #Cycle through neigboring cells in row and column
    for i in range(self.size):
      #Define neighbor cells
      current_column = self.cells[i][column]
      current_row = self.cells[row][i]
      #Remove possibility from neighboring cells and update list of cells that have just been solved by reducing possibilities to 1. These will need to be processed correctly later
      current_column.remove(value)
      self.update_deduced_set(current_column)
      current_row.remove(value)
      self.update_deduced_set(current_row)
    #Define and perform actions pertaining to current cell
    current_cell = self.cells[row][column]
    current_cell.mark_solved(value)
    self.solved.add(current_cell.address)
    self.deduced.discard(current_cell.address)
  
  def apply_top_clues(self):
    print("Before:\n",self)
    for column, clue in enumerate(self.clues[0]):
      if clue == self.size:
        for row in range(self.size-1):
          val = row + 1
          self.set_cell_to(row, column, val)
      elif clue == 1:
        row = 0
        val = self.size
        self.set_cell_to(row, column, val)
      else:
        row = clue - 2
        values_to_remove = [self.size]
        while row >= 0:
          current_cell = self.cells[row][column]
          for value in values_to_remove:
            current_cell.remove(value)
            self.update_deduced_set(current_cell)
          values_to_remove.append(values_to_remove[-1]-1)
          row -= 1
    print("After:\n",self, "\nNarrowed to one possibility:", self.deduced, "\nMarked as Solved:",self.solved)

  def apply_bottom_clues(self):
    print("Before:\n",self)
    for column, clue in enumerate(self.clues[2]):
      val = self.size
      if clue == self.size:
        #val = self.size
        for row in range(self.size):
          self.set_cell_to(row, column, val)
          val -= 1
      elif clue == 1:
        row = self.size - 1
        #val = self.size
        self.set_cell_to(row, column, val)
      else:
        row = self.size - clue + 1
        values_to_remove = [self.size]
        while row < self.size:
          current_cell = self.cells[row][column]
          for value in values_to_remove:
            current_cell.remove(value)
            self.update_deduced_set(current_cell)
          values_to_remove.append(values_to_remove[-1]-1)
          row += 1
    print("After:\n",self, "\nNarrowed to one possibility:", self.deduced, "\nMarked as Solved:",self.solved)

  def apply_right_clues(self):
    print("Before:\n",self)
    for row, clue in enumerate(self.clues[1]):
      val = self.size
      if clue == self.size:
        #val = self.size
        for column in range(self.size):
          self.set_cell_to(row, column, val)
          val -= 1
      elif clue == 1:
        column = self.size - 1
        #val = self.size
        self.set_cell_to(row, column, val)
      else:
        column = self.size - clue + 1
        values_to_remove = [self.size]
        while column < self.size:
          current_cell = self.cells[row][column]
          for value in values_to_remove:
            current_cell.remove(value)
            self.update_deduced_set(current_cell)
          values_to_remove.append(values_to_remove[-1]-1)
          column += 1
    print("After:\n",self, "\nNarrowed to one possibility:", self.deduced, "\nMarked as Solved:",self.solved)

  def apply_left_clues(self):
    print("Before:\n",self)
    for row, clue in enumerate(self.clues[3]):
      if clue == self.size:
        for column in range(self.size):
          val = column + 1
          self.set_cell_to(row, column, val)
      elif clue == 1:
        column = 0
        val = self.size
        self.set_cell_to(row, column, val)
      else:
        column = clue - 2
        values_to_remove = [self.size]
        while column >= 0:
          current_cell = self.cells[row][column]
          for value in values_to_remove:
            current_cell.remove(value)
            self.update_deduced_set(current_cell)
          values_to_remove.append(values_to_remove[-1]-1)
          column -= 1
    print("After:\n",self, "\nNarrowed to one possibility:", self.deduced, "\nMarked as Solved:",self.solved)

  def process_recently_deduced(self):
    while len(self.deduced) > 0:
      print("do Something")
      row, column = self.deduced.pop()
      current_cell = self.cells[row][column]
      val = list(current_cell.possible_values)[0]
      self.set_cell_to(row, column, val)

  def solver(self):
    #procss_givens()
    #self.apply_top_clues()
    #self.apply_bottom_clues()
    #self.apply_left_clues()
    #self.apply_right_clues()
    #self.process_recently_deduced()
    print(self)
    #play_again()
    
  def __repr__(self):
    result = []
    for row in self.cells:
      result.append(repr(row))
    return '\n'.join(result)

def standard_input():
    yield '4'
    yield '1,3,3,2,2,1,3,2,2,1,2,4,3,2,2,1'
    yield '0'

a = TowerPuzzle()

