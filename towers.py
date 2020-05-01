
def prompt_for_size():
  try:
    size = int(input("Please enter the size of board you'd like to play:"))
  except:
    print("Not an integer. Try Again")
    return prompt_for_size()
  else:
    if size < 1:
      print("Not a positive integer. Try again!")
      return prompt_for_size()
    print("\tSize received:", size, "\n\t\tTotal Squares to be made:", size ** 2)
    return size

def prompt_for_clues(size):
  valid_size = False
  #loop through prompt to get a list of expected size
  while not valid_size:
    clue_string = input("\nClues should be integers from 0 to " + str(size) + " (size of board):\n\tStarting from upper left and going clockwise, Please enter clues seperated by ','\n>>>")
    clue_list_of_strings = clue_string.split(',')
    valid_size = 4 * size == len(clue_list_of_strings)
    if not valid_size:
      print("\nNumber of clues did not match expected number. Try Again!")

  #convert list of strings to list of integers and validate values in bounds
  try:
    clue_list = [int(clue) for clue in clue_list_of_strings]
  except:
    print("\nError: One or more clues was not an integer.Please Try Again!")
    return prompt_for_clues(size)
  else:
    if size < max(clue_list) or 0 > min(clue_list):
      print("\n1 or more of your clues are outside of the boundary  values of 0 to ", size, ".\nTry again!")
      return prompt_for_clues(size)

  #arrange the clues into usable format
  #clues [[ list of tuples representing L and R clues per row ], 
  #       [ list of tuples representing T and B clues per col ]]
  #clues[0] = [(row_0_left, row_0_right), ..., (row_N-1_left, row_N-1_right)]  
  #clues[1] = [(col_0_left, col_0_right), ..., (col_N-1_left, col_N-1_right)]

  clues = [[],[]]
  N = size
  max_value = N +1
  right_adjustment = N
  bottom_adjustment = 3 * N - 1
  left_adjustment = 4 * N - 1
  for i in range(size):
    top = clue_list[i]
    right = clue_list[right_adjustment + i]
    bottom = clue_list[bottom_adjustment - i]
    left = clue_list[left_adjustment - i]
    #validate pairs of clues
    if sum([top, bottom]) > max_value or sum([left, right]) > max_value:
      print("\n1 or more pairs of clues exceeds the maximum pair combination sum. Try again!")
      return prompt_for_clues(size)
    clues[0].append([left, right])
    clues[1].append([top, bottom])
  print("\nClues received:", clue_list)
  return clues

def prompt_for_given_squares(size):
  v_range = list(range(1, size + 1))
  total_squares = size ** 2
  givens = [(-1,-1,-1)]
  given_addresses = set()
  print(size)
  try:
    number_of_givens = int(input("\nHow many towers/squares are given? (0 to " + str(total_squares) + "):\t"))
  except:
    print("Please enter an interger next time.")
    return prompt_for_given_squares(size)
  else:
    if number_of_givens not in range(total_squares + 1):
      print("Please enter a value between 0 and", total_squares, "next time:")
      return prompt_for_given_squares(size)
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

def place_given_squares(board, givens):
  print(board)
  print(givens)
  return board

#function isConfigurationValid
def is_line_valid(heights, clue_pair):
  l_count = visible_towers(heights)
  r_count = visible_towers(list(reversed(heights)))
  counts = list(l_count, r_count) 
  return counts == clue_pair

#function countIncreasingHeights
def visible_towers(heights):
  count = 0
  if len(heights) > 0 and max(heights) > 0:
    currentMax = 0
    for height in heights:
      if height > currentMax:
        count += 1
        currentMax = height
  return count

#function safeRowMove
def safe_row_move(board, size, clue_pair, address, value):
  current_row = board[address[0]]
  current_row[address[1]] = value
  if address[1] == size - 1:
    return is_line_valid(current_row, clue_pair)
  return True

#function safeColumnMove
def safe_column_move(board, size, clue_pair, address, value):
  current_column = extract_column(board, address[1], size)
  current_column[address[0]] = value
  if address[0] == size -1:
    return is_line_valid(current_column, clue_pair)
  return True

#function safeMove
def safe_move(board, size, clues, address, value):
  r_clues = clues[0][address[0]]
  c_clues = clues[1][address[1]]
  return safe_row_move(board, size, r_clues, address, value) and safe_column_move(board, size, c_clues, address, value)

#function possibleMoves
def possible_moves(board, size, address):
  #print(address, address[0])
  possible_values = set(list(range(1, size + 1)))
  r_values = set(board[address[0]])
  c_values = set(extract_column(board, address[1],size))
  possible_values.symmetric_difference_update(r_values.union(c_values))
  possible_values.discard(0)
  return list(possible_values)

#function isBoardFull
def is_board_full(board):
  return not any(0 in row for row in board)

#function nextUnfilledSpot
def next_unfilled_spot(board, size):
  for row in range(size):
    for col in range(size):
      if board[row][col] is None:
        address = list(row, col)
        return address

#function ectractColumn
def extract_column(board, col, size):
  current_column = []
  for row in range(size):
    current_column.append(board[row][col])
  return current_column

def tower_puzzle():
  size = prompt_for_size()
  clues = prompt_for_clues(size)
  givens = prompt_for_given_squares(size)
  board = [[None for _x in range(size)] for _y in range(size)]
  place_given_squares(board, givens)
  
  def solve(board):
    if is_board_full(board):
      return True
    else:
      address = next_unfilled_spot(board, size)
      print("address:", address)
      possible_values = possible_moves(board, size, address)
      print("\n\tPossible values:", possible_values)
      for value in possible_values:
        if safe_move(board, size, clues, address, value):
          board[address[0]][address[1]] = value
          if solve(board):
            return True
          board[address[0]][address[1]] = 0
      return False
  
  success = solve(board)
  if not success:
    print("NO SOLUTION!\nTHIS COMBINATION OF CLUES IS IMPOSSIBLE!")
  else:
    print(board)
  return board


#tests

def standard_input():
    yield '4'
    yield '2,4,2,1,1,2,2,3,4,2,1,2,2,3,1,3'
    yield '0'

print(tower_puzzle())

