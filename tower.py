#final Tower Puzzle

def standard_input():
    yield '4'
    yield '2,4,2,1,1,2,2,3,4,2,1,2,2,3,1,3'
    yield '0'


class Square:
  """This class contains the following properties and methods:  
      .address    .value    .not_possible   .neighbors  
      .remove_from_possible()
  """
  def __init__(self, row, column):
    self.address = (row, column)
    self.value = 0
    self.not_possible = set()
    self.neighbors = set()

  def __repr__(self):
    return str(self.value)

  def __len__(self):
    return len(self.not_possible)

  def remove_from_possible(self, value):
    """Method to add a value to the set of not-possible solutions.
    
    Arguments:
        value {int} -- Integer value that will be added to the not_possible set.
    """
    self.not_possible.add(value)

  def set_value(self, value):
    """Method to assign the value to the square and remove it as a possibility to all of its neighbors
    
    Arguments:
        value {int} -- The value that allows this square to be apart of a valid solution
    """
    for neighbor in self.neighbors:
      neighbor.remove_from_possible(value)
    self.value = value
    print(self.value, "was assigned to the address:", self.address)

class Line:
  def __init__(self, size, clue):
    self.members = [] #list of square objects
    self.heights = [0 for _x in range(size)] #list of members' values
    self.unsolved_heights = set(range(1,size + 1))
    self.clue_pair = clue
    self.size = size
    self.possible_heights = set(range(1,size + 1))
    self.visible = [0,0]
    self.solved = False
    
  def __repr__(self):
    return repr(self.members)

  def __len__(self):
    return len(self.unsolved_heights)

  def visible_towers(self, heights):
    count = 0
    if len(heights) > 0 and max(heights) > 0:
      currentMax = 0
      for height in heights:
        if height > currentMax:
          count += 1
          currentMax = height
    return count

  def update_visible(self):
    self.visible[0] = self.visible_towers(self.heights)
    self.visible[1] = self.visible_towers(list(reversed(self.heights)))

  def line_satisfy_clues(self):
    return self.visible == self.clue_pair

  def update_heights(self):
    for i in range(self.size):
      current_member = self.members[i]
      print(current_member)
      print(self.heights)
      self.heights[i] = current_member.value

  def reduce_members_by_neighboring_values(self):
    for member in self.members:
      if member.value == 0:
        for neighbor in member.neighbors:
          member.remove_from_possible(neighbor.value)
      if len(member) == len(self.members):
        val = self.possible_heights.symmetric_difference(member.not_possible)
        member.set_value(val)

  def deduce_members_values_by_neighbors_not_possibles(self):
    for member in self.members:
      if member.value == 0:
        histogram = [0 for _x in range(self.size)]
        for val in range(1, self.size + 1):
          occurance = 0
          for neighbor in member.neighbors:
            if val in neighbor.not_possible:
              occurance += 1
          histogram[val - 1] = occurance
        deduced_value = histogram.index(2 * self.size - 2) + 1
        if deduced_value > 0:
          member.set_value(deduced_value)

  def apply_clues_as_pairs(self):
    size = self.size
    clues = self.clue_pair
    clue_sum = sum(clues)
    zeros = 0 in clues
    
    #using both clues
    if clue_sum == 3 and not zeros:
      if clues[0] == 1:
        self.members[0].set_value(size)
        self.members[-1].set_value(size - 1)
      else:
        self.members[0].set_value(size - 1)
        self.members[-1].set_value(size)
    
    if clue_sum == size +1:
      self.members[clues[0]-1].set_value(size)
    
  #individual clues
  def apply_clues_individuually(self, members, clue):
    print("working individual clues")
    size = self.size
    descending_value = list(range(size, 0, -1))
    affected_squares = clue - 1
    remove_values = descending_value[0:affected_squares]
    print(size, descending_value, clue, affected_squares, remove_values)

    if 2 <= clue <= (size - 1):
      for i in range(affected_squares):
        members[i].not_possible.update(set(remove_values))
        del remove_values[-1]
    elif clue == size:
      for i in range(size):
        members[i].set_value(i + 1)
    elif clue == 1:
      members[0].set_value(size)

  def apply_clues(self):
    self.apply_clues_as_pairs()
    self.apply_clues_individuually(self.members, self.clue_pair[0])
    self.apply_clues_individuually(list(reversed(self.members)), self.clue_pair[1])
  
  def make_final_guess(self):
    pass

class TowerPuzzle:
  def __init__(self):
    self.unsolved = set()
    self.squares = []
    self.rows = []
    self.cols = []
    self.build_sequence()

  def __repr__(self):
    result = []
    for row in self.squares:
      result.append(repr(row))
    return '\n'.join(result)

  def build_sequence(self):
    self.size = self.prompt_for_size()
    self.total_squares = self.size ** 2
    self.value_range = list(range(1, self.size + 1))
    self.grid_range = list(range(self.size))
    self.clues = self.prompt_for_clues()
    self.givens = self.prompt_for_given_squares()
    self.construct_squares()
    #self.squares = [[Square(row, column) for column in range(self.size)] for row in range(self.size)]
    #self.create_neighbors()
    self.make_rows_and_cols()
    
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

  def create_neighbors(self):
    for row in self.grid_range:
      for col in self.grid_range:
        current_cell = self.squares[row][col]
        current_row = set(self.squares[row])
        current_col = set(self.extract_column(col))
        current_neighbors = current_row.symmetric_difference(current_col)
        current_cell.neighbors.update(current_neighbors)
        self.unsolved.add(current_cell)

  def construct_squares(self):
    self.squares = []
    for row in self.grid_range:
      current_row = []
      for col in self.grid_range:
        current_row.append(Square(row,col))
      self.squares.append(current_row)
    self.create_neighbors()
  
  def extract_column(self, col):
    current_column = []
    for row in self.grid_range:
      current_column.append(self.squares[row][col])
    return current_column
  
  def make_rows_and_cols(self):
    
    for i in self.grid_range:
      current_row = Line(self.size, self.clues[0][i])
      current_row.members = self.squares[i]
      self.rows.append(current_row)

      current_col = Line(self.size, self.clues[1][i])
      current_col.members = self.extract_column(i)
      self.cols.append(current_col)
      #print(current_row, current_col)
    #print(self)


a = TowerPuzzle()
current_line = a.rows[0]
print(current_line.clue_pair)
current_line.update_heights()
current_line.apply_clues()
current_line.update_heights()
print(current_line)









