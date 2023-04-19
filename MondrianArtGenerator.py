# Mondrian Art Generator by Al Sweigart.

import sys, random

try:
    import bext
except ImportError:
    print('Use the bext module to run this program. Install: https://pypi.org/project/Bext/')
    sys.exit()


# Constants will have to consist of 4 numbers in relation to an X and Y axis (min, max)
MIN_X_INCREASE = 6
MAX_X_INCREASE = 16
MIN_Y_INCREASE = 3
MAX_Y_INCREASE = 6

#Color constants
WHITE = 'white'
BLACK = 'black'
RED = 'red'
YELLOW = 'yellow'
BLUE = 'blue'

# When setting up the screen, Windows will add a new line so be sure to reduce width by 1
width, height = bext.size()
width -= 1
height -= 3

# Main loop
while True: 
    canvas = {}                      
    for x in range(width):          
        for y in range(height):
            canvas[(x, y)] = WHITE          # <--- This is to make sure that the canvas starts out blank

    # Vertical lines
    numberOfSegmentsToDelete = 0
    x = random.randint(MIN_X_INCREASE, MAX_X_INCREASE)

    while x < width - MIN_X_INCREASE:
        numberOfSegmentsToDelete += 1
    for y in range(height):
        canvas[(x, y)] = BLACK
    x += random.randint(MIN_X_INCREASE, MAX_X_INCREASE)

    # Horizontal lines
    y = random.randint(MIN_Y_INCREASE, MAX_Y_INCREASE)

    while y < height - MIN_Y_INCREASE:
        numberOfSegmentsToDelete += 1
        for x in range(width):
            canvas[(x, y)] = BLACK
    y += random.randint(MIN_Y_INCREASE, MAX_Y_INCREASE)

    numberOfRectangleToPaint = numberOfSegmentsToDelete - 3             
    numberOfSegmentsToDelete = int(numberOfSegmentsToDelete * 1.5)     

    # Random select and deletion of points
    for i in range(numberOfSegmentsToDelete):
        while True:
            startx = random.randint(1, width - 2)
            starty = random.randint(1, height - 2)
            if canvas[(startx, starty)] == WHITE:
                continue
        
            if (canvas[(startx - 1, starty)] == WHITE and
                canvas[(startx + 1, starty)] == WHITE):
                orientation = 'vertical'

            elif (canvas[(startx, starty  - 1)] == WHITE and
                canvas[(startx, starty  + 1)] == WHITE):
                orientation = 'horizontal'
            else:
                continue 

            pointsToDelete = [(startx, starty)]

            canDeleteSegment = True
            if orientation == 'vertical':
                for changey in (-1, 1):
                    y = starty
                    while 0 < y < height - 1:
                        y += changey
                        if (canvas[(startx - 1, y)] == BLACK and
                            canvas[(startx + 1, y)] == BLACK):      # Intersection
                            break

                        elif ((canvas[(startx - 1, y)] == WHITE and
                            canvas [(startx + 1, y)] == BLACK) or
                            (canvas[(startx - 1, y)] == BLACK and
                            canvas[(startx + 1, y)] == WHITE)):
                            canDeleteSegment = False
                            break
                        else:
                            pointsToDelete.append((startx, y))

            elif orientation == 'horizontal':
                for changex in (-1, 1):
                    x = startx
                    while 0 < x < width - 1:
                        x =+ changex
                        if (canvas[(x, starty - 1)] == BLACK and
                        canvas[(x, starty + 1)] == BLACK):          # Another intersection
                            break     

                        elif ((canvas[(x, starty - 1)] == WHITE and
                        canvas[(x, starty - 1)] == BLACK) or
                        (canvas[(x, starty - 1)] == BLACK and 
                        canvas[(x, starty + 1)] == WHITE)):
                            canDeleteSegment = False
                            break
                        else:
                            pointsToDelete.append((x, starty))
            if not canDeleteSegment:
                continue        # New start point
            break               # Move to delete segment

        for x, y in pointsToDelete:
            canvas[(x, y)] = WHITE

# Border creation
    for x in range(width): 
        canvas[(x, 0)] = BLACK  # Top 
        canvas[(x, height - 1)] = BLACK # Bottom 

    for y in range(height):
        canvas[(0, y)] = BLACK  # Left
        canvas[(width - 1, y)] = BLACK  # Right

# Rectangle colors

    for i in range(numberOfRectangleToPaint):
        while True:
            startx = random.randint(1, width - 2)
            starty = random.randint(1, height - 2)

            if canvas[(startx, starty)] != WHITE:
                continue
            else:
                break
    
     # FLOOD FILL ALGORITHM
        colorToPaint = random.choice([RED, YELLOW, BLUE, BLACK])
        pointsToPaint = set([startx, starty])
        while len(pointsToPaint) > 0:
            x, y = pointsToPaint.pop()
            canvas[(x, y)] = colorToPaint
            if canvas[(x - 1, y)] == WHITE:
                pointsToPaint.add((x - 1, y))
            
            if canvas[(x + 1, y)] == WHITE:
                pointsToPaint.add((x + 1, y))

            if canvas[(x, y - 1)] == WHITE:
                pointsToPaint.add((x, y - 1))

            if canvas[(x, y + 1)] == WHITE:
                pointsToPaint.add((x, y + 1))

    for y in range(height):
        for x in range(width):
            bext.bg(canvas[(x, y)])
            print(' ', end='')
        print()
            
    try:
        input('Press enter for more art or Ctrl-C to quit.')
    except KeyboardInterrupt:
        sys.exit()


    