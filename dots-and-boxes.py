def setup_game():
    global box_captured
    global boxes
    global first_player_turn
    global width
    global height
    global lines
    boxes = dict()
    box_captured = False
    first_player_turn = True
    lines = set()
    clear_screen()
    width = min(max(3,int(input("Width: "))),9)
    height = min(max(3,int(input("Height: "))),9)
    render()

def main():
    setup_game()
    play_game()

def play_game():
    global first_player_turn
    global box_captured
    while True:
        turn_invite = "First" if first_player_turn else "Second"
        turn_invite += " player turn: "
        move = tuple(map(int, input(turn_invite).split()))
        if check_incorrect_move(move):
            render()
            print("Incorrect turn")
            continue
        process_move(move)
        if box_captured:
            box_captured = False
        else:
            first_player_turn = not first_player_turn
        render()
        if check_win():
            break
    boxes1,boxes2 = 0,0
    for k in boxes:
        if boxes[k] == 1:
            boxes1 += 1
        else:
            boxes2 += 1
    end_caption = ''
    if boxes1 > boxes2:
        end_caption += "First player wins!!!"
    elif boxes1 < boxes2:
        end_caption += "Second player wins!!!"
    else:
        end_caption += "Draw game"
    print(end_caption)
    

def check_win():
    return len(lines) == width * height * 2 + width + height

def process_move(move):
    lines.add(move)
    if move[3] - move[1] == 1:
        process_vertical_move(move)
    else:
        process_horizontal_move(move)

def process_vertical_move(move):
    if move[0] <= width:
        check_left_box(move)
    if move[0] >= 0:
        check_right_box(move)

def process_horizontal_move(move):
    if move[1] < height:
        check_below_box(move)
    if move[1] > 0:
        check_above_box(move)

def check_left_box(move):
    global box_captured
    if (move[0]-1,move[1],move[0],move[1]) in lines and\
        (move[0]-1,move[1]+1,move[0],move[1]+1) in lines and\
        (move[0]-1,move[1],move[0]-1,move[1]+1) in lines:
        boxes[(move[0]-1,move[1])] = 1 if first_player_turn else 2
        box_captured = True

def check_right_box(move):
    global box_captured
    if (move[0],move[1],move[0]+1,move[1]) in lines and\
        (move[0],move[1]+1,move[0]+1,move[1]+1) in lines and\
        (move[0]+1,move[1],move[0]+1,move[1]+1) in lines:
        boxes[(move[0],move[1])] = 1 if first_player_turn else 2
        box_captured = True

def check_below_box(move):
    global box_captured
    if (move[0],move[1]+1,move[0]+1,move[1]+1) in lines and\
        (move[0],move[1],move[0],move[1]+1) in lines and\
        (move[0]+1,move[1],move[0]+1,move[1]+1) in lines:
        boxes[(move[0],move[1])] = 1 if first_player_turn else 2
        box_captured = True

def check_above_box(move):
    global box_captured
    if (move[0],move[1]-1,move[0]+1,move[1]-1) in lines and\
       (move[0],move[1]-1,move[0],move[1]) in lines and\
       (move[0]+1,move[1]-1,move[0]+1,move[1]) in lines:
       boxes[(move[0],move[1]-1)] = 1 if first_player_turn else 2
       box_captured = True

def check_incorrect_move(move):
    return len(move) != 4 or \
        0 > move[0] or move[0] > width or \
        0 > move[2] or move[2] > width or \
        0 > move[1] or move[1] > height or \
        0 > move[3] or move[3] > height or \
        move[2] - move[0] not in (1,0) or \
        move[3] - move[1] not in (1,0) or \
        move[2] - move[0] + move[3] - move[1] != 1 or \
        move in lines


def clear_screen():
    print(chr(27)+'[2J')

def render():
    clear_screen()
    res = '   ' + '   '.join(map(str,range(width+1))) + '\n\n'
    for y in range(height+1):
        res += str(y) + '  '
        for x in range(width+1):
            res += '+'
            if (x,y,x+1,y) in lines:
                res += '---'
            else:
                res += '   '
        res += '\n   '
        for x in range(width+1):
            if (x,y,x,y+1) in lines:
                res += '|'
            else:
                res += ' '
            if (x,y) in boxes:
                res += ' '+str(boxes[(x,y)])+' '
            else:
                res += '   '
        res += '\n'
    print(res)

if __name__=="__main__":
    main()