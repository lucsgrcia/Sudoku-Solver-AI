rows = 'ABCDEFGHI'
cols = '123456789'

def cross(a, b):
    return [s+t for s in a for t in b]

boxes = cross(rows, cols)
print(f'[{boxes[0]}, {boxes[1]}, {boxes[2]}, ... , {boxes[-3]}, {boxes[-2]}, {boxes[-1]}]')

grid_str = "4.....8.5.3..........7......2.....6.....8.4......1.......6.3.7.5..2.....1.4......"
grid_dict = dict(zip(boxes, grid_str))

def display(grid_dict):
    """
    Display the values as a 2-D grid.
    Input: The sudoku in dictionary form
    Output: None
    """
    width = 1+max(len(grid_dict[s]) for s in boxes)
    line = '+'.join(['-'*(width*3 + 1)]*3)
    for r in rows:
        print('', ''.join(grid_dict[r+c].center(width)+('| ' if c in '36' else '')
                      for c in cols))
        if r in 'CF': print(line)

display(grid_dict)

def factor_row(position, sudoku_str):
  row = position % 9
  row_numbers = [0] * 9
  for i in range(9):
    if (sudoku_str[row + i * 9] != '.'):
      #print(row + i * 9)
      #print(int(sudoku_str[row + i * 9]))
      row_numbers[int(sudoku_str[row + i * 9]) - 1] += 1
  for number in row_numbers:
    if (number > 1):
      return 0
  return 1

def factor_line(position, sudoku_str):
  line = position - position % 9
  line_numbers = [0] * 9
  for i in range(9):
    if (sudoku_str[line + i] != '.'):
      #print(line + i)
      #print(int(sudoku_str[line + i]))
      line_numbers[int(sudoku_str[line + i]) - 1] += 1
  for number in line_numbers:
    if (number > 1):
      return 0
  return 1

def factor_square(position, sudoku_str):
  square_numbers = [0] * 9
  line = int(position / 9)
  line = line - line % 3
  row = position % 9
  row = row - row % 3
  #print(f"line:{line} row:{row}")
  for i in range(3):
    for j in range(3):
      if sudoku_str[row + i + (line + j) * 9] != '.':
        square_numbers[int(sudoku_str[row + i + (line + j) * 9]) - 1] += 1
    for number in square_numbers:
      if number > 1:
        return 0
  return 1

def arc_reduction(arcs, grid, index):
  # row
  row = index % 9
  for j in range(9):
    try:
      arcs[row + j * 9].remove(grid[index])
    except:
      pass
  # line
  line = int(index / 9)
  for j in range(9):
    try:
      arcs[line + j].remove(grid[index])
    except:
      pass
  # square
  line = int(index / 9)
  line = line - line % 3
  row = index % 9
  row = row - row % 3
  for i in range(3):
    for j in range(3):
      try:
        arcs[row + i + 9 * (line + j)].remove(grid[index])
      except:
        pass
      
def solution(grid_param):
  grid_o = list(grid_param)
  arc_consistency_original = [list(range(1, 10)) for _ in range(81)] # Assuming each arc initially contains numbers 1-9
  for i in range(81):
    if grid_o[i] != '.':
      arc_consistency_original[i] = []
  def backtrack(arc_consistency, index):
    arc_consistency = [lst[:] for lst in arc_consistency]
    arc_consistency[index] = []
    arc_reduction(arc_consistency, grid_o, index)
    try:
      length = min(len(arc)
               for arc in arc_consistency if arc != [])
    except ValueError:
      return 1

    aux_index = 0
    for k in range(81):
      if len(arc_consistency[k]) == length:
        aux_index = k
        break
    i = aux_index
    count = 0
    for option in arc_consistency[i]:
      count += 1
      grid_o[i] = option
      weight = factor_row(i, grid_o) * factor_line(i, grid_o) * factor_square(i, grid_o)
      if weight:
        if backtrack(arc_consistency, i):
          return 1
    grid_o[i] = '.'
    return 0
  begin_index = -1
  # for i in range(81):
  #   if grid_o[i] != '.':
  #     begin_index = i
  #     break
  for i in range(81):
    if grid_o[i] != '.':
      arc_reduction(arc_consistency_original, grid_o, i)
      begin_index = i
  if begin_index != -1:
    r = backtrack(arc_consistency_original,begin_index)
    if r:
      grid_final = ""
      for i in range(81):
        grid_final = grid_final + str(grid_o[i])
      return dict(zip(boxes, grid_final))
    else:
      print("NAO TEM SOLUCAO")
      return

# Para rodar o exemplo difícil é necessário esperar cerca de 1 minuto, talvez até um pouco mais
grid_str = "4.....8.5.3..........7......2.....6.....8.4......1.......6.3.7.5..2.....1.4......"
#grid_str = '..3.2.6..9..3.5..1..18.64....81.29..7.......8..67.82....26.95..8..2.3..9..5.1.3..'
solved_board = solution(grid_str)
display(solved_board)

