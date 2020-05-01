#tower/skyscraper puzzle

class Tower(object):
  """This class contains the following properties and methods:
      .address        .value        .not_possible
      .remove_from_possibilities()
  """

  def __init__(self, row, col):
    self.address = (row,col)
    self.value = 0
    self.not_possible = set()

  def __repr__(self):
    return self.value

  def __len__(self):
    return len(self.not_possible)

  def remove_from_possibilities(self, val):
    self.not_possible.update(list(val))

class TowerPuzzle(object):
  def __init__(self):
    self.size = self.prompt_for_size()
    self.clues = self.prompt_for_clues()
    self.givens = self.prompt_for_given_squares()
    self.cells = [[[0, set([0])] for _x in range(self.size)] for _y in range(self.size)]
    print(self)
    #self.place_given_squares()
    #self.solve_simple_clues()
    #self.solve()

  def __repr__(self):
    result = []
    for row in self.cells:
      result.append(repr(row))
    return '\n'.join(result)

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
    v_range = list(range(1, self.size + 1))
    total_squares = self.size ** 2
    givens = [(-1,-1,-1)]
    given_addresses = set()
    print(self.size)
    try:
      number_of_givens = int(input("\nHow many towers/squares are given? (0 to " + str(total_squares) + "):\t"))
    except:
      print("Please enter an interger next time.")
      return self.prompt_for_given_squares()
    else:
      if number_of_givens not in range(total_squares + 1):
        print("Please enter a value between 0 and", total_squares, "next time:")
        return self.prompt_for_given_squares()
    while number_of_givens != 0:
      response = input(str(number_of_givens) + " square(s) left.\nEnter data in this format: 'row, col, value'\n\tusing numbers 1 through " + str(total_squares) + ":\t")
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
      print("\n\tThe following towers/squares have been converted and will be added:", givens[1:])
    else:
      print("\n\tNo given towers/squares will be added.")
    return givens

  #def update_solved_count(self):
  #  self.solved_count = sum([1 for tower in self.towers if tower.value > 0])
#
  #def is_board_full(self):
  #  return self.solved_count == self.total_squares
#
  #def next_unsolved_tower(self):
  #  for row in self.towers:
  #    for tower in row:
  #      if tower.value == 0:
  #        return tower.address

def standard_input():
    yield '4'
    yield '1,3,3,2,2,1,3,2,2,1,2,4,3,2,2,1'
    yield '1'
    yield '1,2,1'

a = TowerPuzzle()
