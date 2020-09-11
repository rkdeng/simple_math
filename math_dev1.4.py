'''
Developed in python 3.6.8 and pygame 1.9.6
9/5/2020
'''

# import pdb; pdb.set_trace()   # debug tool
import pygame
import random

pygame.init()  # must have

# pics for animations
rocks = [pygame.image.load('pics/rock1-s.png'),pygame.image.load('pics/rock2-s.png'),pygame.image.load('pics/rock3-s.png'),pygame.image.load('pics/rock4-s.png')] 
enemy = [pygame.image.load('pics/poop1-s.png'),pygame.image.load('pics/poop2-s.png'),pygame.image.load('pics/poop3-s.png'),pygame.image.load('pics/poop4-s.png'),pygame.image.load('pics/poop5-s.png'),pygame.image.load('pics/poop6-s.png')]
main_character = [pygame.image.load('pics/cat1-s.png'),pygame.image.load('pics/cat2-s.png'),pygame.image.load('pics/cat3-s.png'),pygame.image.load('pics/cat4-s.png'),pygame.image.load('pics/cat5-s.png')]
cover_pic = [pygame.image.load('pics/1-s.png')]  # cover pic
end_pic1 = [pygame.image.load('pics/win-s.png')]  # win
end_pic2 = [pygame.image.load('pics/lose-s.png')]  # lose

# game window
win_x = 1000
win_y = 600
win = pygame.display.set_mode((win_x,win_y))
# title
pygame.display.set_caption('Math is fun!!')

# clock variable
clock = pygame.time.Clock()

# RGB colors might be used
white = (255, 255, 255) 
green = (0, 255, 0) 
blue = (102, 178, 255) 
black = (0, 0, 0)
red = (255, 51, 51)
yellow = (255, 255, 0)

# variables
q_total = 5  # total number of questions
win_thres = 1   # threshold for winning
keypress_timer = 0  # timer for key press
txt_flash_timer = 0  # timer for flashing text

state_main = 1  # main state variable, 1, start page; 2, playing; 3, end page

def display_text(txtstr, x, y, txtcolor, bgcolor, fontsize=32):
# function to display text
# txtstr is the text string
# x, y are the coordinates, corresponds to the center of the text rectangle
# txtcolor, color; bgcolor, background color; fontsize, font size
  font = pygame.font.Font('freesansbold.ttf', fontsize)
  txt_obj = font.render(txtstr, True, txtcolor, bgcolor)
  textRect = txt_obj.get_rect()
  textRect.center = (x, y)
  # display
  win.blit(txt_obj, textRect)

def flash_text(txtstr, x, y, txtcolor, bgcolor, fontsize=32):
# function to display flashing text
  font = pygame.font.Font('freesansbold.ttf', fontsize)
  txt_obj = font.render(txtstr, True, txtcolor, bgcolor)
  textRect = txt_obj.get_rect()
  textRect.center = (x, y)
  # display
  global txt_flash_timer
  if txt_flash_timer < 25: # show up for 25 frames, disappear for 25 frames
    win.blit(txt_obj, textRect)
  if txt_flash_timer < 50:
    txt_flash_timer += 1
  elif txt_flash_timer >= 50:
    txt_flash_timer = 0

def collect_input():
  # function to collect input answers,
  global keypress_timer  # avoid windfurry
  global input_str   # store the current answer
  
  if keys[pygame.K_0] and keypress_timer < 1:
    input_str.append('0')
    keypress_timer += 1
    #print(input_str)
  elif keys[pygame.K_1] and keypress_timer < 1:
    input_str.append('1')
    keypress_timer += 1
    #print(input_str)
  elif keys[pygame.K_2] and keypress_timer < 1:
    input_str.append('2')
    keypress_timer += 1
    #print(input_str)
  elif keys[pygame.K_3] and keypress_timer < 1:
    input_str.append('3')
    keypress_timer += 1
    #print(input_str)
  elif keys[pygame.K_4] and keypress_timer < 1:
    input_str.append('4')
    keypress_timer += 1
    #print(input_str)
  elif keys[pygame.K_5] and keypress_timer < 1:
    input_str.append('5')
    keypress_timer += 1
    #print(input_str)
  elif keys[pygame.K_6] and keypress_timer < 1:
    input_str.append('6')
    keypress_timer += 1
    #print(input_str)
  elif keys[pygame.K_7] and keypress_timer < 1:
    input_str.append('7')
    keypress_timer += 1
    #print(input_str)
  elif keys[pygame.K_8] and keypress_timer < 1:
    input_str.append('8')
    keypress_timer += 1
    #print(input_str)
  elif keys[pygame.K_9] and keypress_timer < 1:
    input_str.append('9')
    keypress_timer += 1
    #print(input_str)
  elif keys[pygame.K_BACKSPACE] and keypress_timer < 1 and input_str:
    input_str.pop()
    keypress_timer += 1
    #print(input_str)

def new_question():
# generate a new question, edit this section for different types of questions
# right now it's addition and subtraction within 20, integers, nonnegative answers,
  a = random.randint(0,20)
  b = random.randint(0,20)
  if random.random() > 0.5:
    answer_curr = a + b
    q_text = '%d + %d = ?' % (a, b)
  else:
    if a > b:
      answer_curr = a - b
      q_text = '%d - %d = ?' % (a, b)
    else:
      answer_curr = b - a
      q_text = '%d - %d = ?' % (b, a)
      
  return q_text, answer_curr

# create a class for animated object
class player:
  def __init__(self,x,y,width,height,vel):
    self.x0 = x  # starting position
    self.y0 = y
    self.x = x  # current position
    self.y = y
    self.width = width  # image size
    self.height = height
    self.vel = vel # moving speed
    #self.hitbox = (self.x, self.y, width, height)
    self.xmove2 = x  # future position, for animation
    self.ymove2 = y
    self.pic_count = 0  # for cycling through pics
    # unused state variable
    #self.isJump = False
    #self.jumpCount = 10
    #self.left = False
    #self.right = False
    #self.walkCount = 0
    #self.standing = True

  def draw(self,win,n_pic,pic_list,pic_factor):
    # n_pic, number of pics in an animation cycle; pic_list, stores pics.
    # pic_factor, move to next pic every n frames.
    #pygame.draw.rect(win, (255,0,0), (self.x, self.y, self.width, self.height),2)  # test only, draw rectangle around loaded image
    if self.pic_count >= n_pic*pic_factor:
      self.pic_count = 0

    win.blit(pic_list[self.pic_count//pic_factor],(self.x,self.y))
    self.pic_count += 1


# create objects
p0 = player(win_x//2-100, 400, 175, 188, 0)   # starting page pic

# main while loop
run = True
while run:
  # define frame rate as 27 frames per second
  clock.tick(27)

# key press refractory period timer, to avoid multiple key input after 1 click
  if keypress_timer > 0:
    keypress_timer += 1
  if keypress_timer > 5:
    keypress_timer = 0

  # refresh background
  win.fill((0,0,0))

  # this enables quit by clicking the red x
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      run = False

  keys = pygame.key.get_pressed()  
  
  if state_main == 1:  # start page

    display_text('Escape from the alien.', win_x//2, win_y//2-80, green, '', 60)
    flash_text('Press enter to start!!!', win_x//2, win_y//2, green, '', 60)
    if keys[pygame.K_RETURN] and keypress_timer < 1:  # move to state 2 by pressing return
      state_main = 2
      keypress_timer += 1
      # generate the first question
      txt_tmp, ans_tmp = new_question()
      input_str = []
      # initiate some variables
      question_left = q_total
      q_right = 0
      q_wrong = 0
      mistakes = []  # store mistakes
      bullets = []  # store bullets
      transit_timer = 27*1.5   # transition timer between state 2 and 3, wait for animation
      # initiate players  
      p1 = player(600, 400, 150, 110, 0)  # playing page player
      e1 = player(100, 400, 100, 100, 5)   # playing page enemy

    # draw starting page pic
    p0.draw(win, 1, cover_pic, 1) # parameters for animation are hard-coded 
    
  elif state_main == 2:  # playing page
    if question_left == 0:  # move to state 3 if questions are all finished
      transit_timer -= 1
      if transit_timer < 1:
        state_main = 3  
        if q_right > win_thres:  # win
          # initiate winning pic
          p_win = player(win_x//2-100,350,175,147,0)
        else:  # lose
          # initiate losing pic
          p_lose = player(win_x//2-100,350,200,183,0)
          
    display_text(txt_tmp, 300, 120, green, '', 50) # display question

    # for answer input, collect and display current answer
    collect_input() 
    disp_curr = ''.join(input_str)
    display_text('Your answer is:', 300, 170, green, '', 40)
    display_text(disp_curr, 300, 220, blue, '', 50)
    # score board
    display_text('Remaining: %d' % question_left, 750, 120, green, '', 35)   # remaining question
    display_text('Right: %d' % q_right, 750, 170, green, '', 35)   # score right
    display_text('Wrong: %d' % q_wrong, 750, 220, green, '', 35)   # score wrong

    if keys[pygame.K_RETURN] and keypress_timer < 1 and input_str: # when answer is entered
      keypress_timer += 1
      if ans_tmp == int(disp_curr):
        q_right += 1
        # add one bullet for each correct answer
        bullets.append(player(e1.x, e1.y-200, 100, 100, 5))
        if bullets:
          for bul in bullets:
            bul.xmove2 = e1.xmove2
            bul.ymove2 = e1.ymove2
        print('answer is right!') # testing only
      else:
        q_wrong += 1  
        mistakes.append('%s %d' % (txt_tmp, int(disp_curr)))  # store mistakes, may be displayed in the end
        print('answer is wrong!! The right answer is %d' % ans_tmp) # testing only

      # generate new questions
      if question_left > 0:
        if question_left > 1:
          txt_tmp, ans_tmp = new_question()
          print('new question')
        question_left -= 1
 
      input_str = []

    # draw players
    p1.draw(win, 4, main_character, 3)      
    e1.draw(win, 6, enemy, 3)

    e1.xmove2 = e1.x0 + ((p1.x0 - e1.x0 - 20)//q_total)*q_wrong
    if e1.xmove2 > e1.x:  # move enemy closer to the player if made a mistake
      e1.x += e1.vel

    # draw bullets when there is right answer
    if bullets:
      for bul in bullets:
        bul.draw(win, 4, rocks, 4)
        if bul.xmove2 > bul.x:
          bul.x += bul.vel
        if bul.ymove2 > bul.y:
          bul.y += bul.vel
        if bul.xmove2 <= bul.x and bul.ymove2 <= bul.y:
          bullets.pop(bullets.index(bul))  # delete bullet when it reaches the enemy
    
  elif state_main == 3:   # end page
    display_text('Press R to restart', win_x//2, 50, green, '', 50)
    # score board
    display_text('Remaining: %d' % question_left, 750, 120, green, '', 35)   # remaining question
    display_text('Right: %d' % q_right, 750, 170, green, '', 35)   # score right
    display_text('Wrong: %d' % q_wrong, 750, 220, green, '', 35)   # score wrong
    
    if q_right > win_thres:
      display_text('Escaped!!!', 300, 130, red, '', 65)
      # draw cartoon
      p_win.draw(win, 1, end_pic1, 1)
      if q_wrong == 0:
        flash_text('Flawless victory!!!', 300, 220, red, '', 65)
      elif q_right/q_total >= 0.7:
        flash_text('Good job!', 300, 220, red, '', 65)
    else:
      # draw cartoon
      p_lose.draw(win, 1, end_pic2, 1)
      display_text('Defeated...', 300, 130, yellow, '', 65)
    
    if keys[pygame.K_r]:  # go to main menu
      state_main = 1
    if q_wrong > 0:
      display_text('Press Q to review mistakes.', win_x//2, 550, green, '', 25)
      if keys[pygame.K_q]:  # review mistakes
        state_main = 4
      
  elif state_main == 4: # display mistakes for review
    # mistakes
    #display_text(' '.join(mistakes[0]), 165, 25, blue, '', 25)  # only for testing
    #display_text(' '.join(mistakes[0]), 500, 25, blue, '', 25)
    #display_text(' '.join(mistakes[0]), 835, 25, blue, '', 25)

    #display_text(' '.join(mistakes[0]), 165, 465, blue, '', 25)  # only for testing
    #display_text(' '.join(mistakes[0]), 500, 465, blue, '', 25)
    #display_text(' '.join(mistakes[0]), 835, 465, blue, '', 25)

    gg_x = [165, 500, 835]    # x coordinates
    gg_y = list(range(25,500,40))  # y coordinates
    # right now only support displaying 36 entries
    for iter in range(len(mistakes)):
      x_tmp = (iter+1)%3
      if x_tmp == 0:
        x_tmp = 3
      y_tmp = (iter+1)//3
      if (iter+1)%3 == 0:
        y_tmp -= 1
      #display_text(str(iter),gg_x[x_tmp-1], gg_y[y_tmp], blue, '', 25)  # test only
      display_text(' '.join(mistakes[iter]), gg_x[x_tmp-1], gg_y[y_tmp], blue, '', 25)

    # go back to starting page
    display_text('Press R to restart. Back to score, press B', win_x//2, 550, green, '', 25)
    if keys[pygame.K_r]:  # go to main menu
      state_main = 1
    if keys[pygame.K_b]:  # go to end page
      state_main = 3

  # update everything on the surface/game board
  pygame.display.update()  

##################################
# if get out of the loop, quit  
pygame.quit()
