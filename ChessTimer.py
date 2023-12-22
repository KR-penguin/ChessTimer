import pygame
import os

pygame.init()

ScreenWidth = 1152
ScreenHeight = 648
Screen = pygame.display.set_mode((ScreenWidth, ScreenHeight))

pygame.display.set_caption("ChessTimer")

clock = pygame.time.Clock() 
TimerFont = pygame.font.Font(None, 40)
MoveValueFont = pygame.font.Font(None, 60)
DeveloperFont = pygame.font.Font(None, 20)
WarningFont = pygame.font.Font(None, 100)
StartTicks = pygame.time.get_ticks() # Start
TotalMove = 0
TimeOver = False

# --- Image Load ---

CurrentPath = os.path.dirname(__file__)
ImagePath = os.path.join(CurrentPath, "Sources/Images")

NoSpendTimerBackgroundImage = pygame.image.load(os.path.join(ImagePath, "NoSpendTimeBackground.png"))
NowSpendTimerBackgroundImage = pygame.image.load(os.path.join(ImagePath, "NowSpendTimeBackground.png"))
AreaClassificationStickImage = pygame.image.load(os.path.join(ImagePath, "AreaClassificationStick.png"))

# --- Sounds Load ---

SoundPath = os.path.join(CurrentPath, "Sources/Sounds")
TurnChangeSoundEffect = pygame.mixer.Sound(os.path.join(SoundPath, "ChangeTurn.mp3"))
TimeOverSoundEffect = pygame.mixer.Sound(os.path.join(SoundPath, "TimeOver.mp3"))

# --- Setup before start ---

FirstPlayerTime = int(input("첫번째 사람의 제한 시간을 입력해주세요(초 단위) : "))
SecondPlayerTime = int(input("두번째 사람의 제한 시간을 입력해주세요(초 단위) : "))
SceneValue = 1

# --- classes ----

class Background:
    def __init__(self, Image, X, Y):
        self.Size = Image.get_rect().size
        self.Width = self.Size[0]
        self.Height = self.Size[1]
        self.Xpos = X
        self.Ypos = Y

class Player:
    def __init__(self, time):
        self.bPlay = False
        self.PlayTime = time
        self.RemainingTime = self.PlayTime
        self.LastUpdatedTime = 0
        self.IncrementTime = 0

class Mouse:
    def __init__(self):
        self.Xpos = 0 
        self.Ypos = 0

# --- create instances ---
        
NoSpendTimerBackground = Background(NoSpendTimerBackgroundImage, 0, 0)
NoSpendTimerBackground2 = Background(NoSpendTimerBackgroundImage, 0, 0)
NowSpendTimerBackground = Background(NowSpendTimerBackgroundImage, 0, 0)
AreaClassificationStick = Background(AreaClassificationStickImage, 0, 0)

FirstPlayer = Player(FirstPlayerTime) # 위에서 입력받은 FirstPlayerTime을 property로 넣기
SecondPlayer = Player(SecondPlayerTime)

TouchFinger = Mouse()

# --- function ---

def GameOver(PlayerNumber : int):
    global TimeOver
    TimeOver = True
    global TimeOverText
    TimeOverSoundEffect.play()

    if PlayerNumber == 1:
        TimeOverText = WarningFont.render("First Player TimeOver!", True, (255, 0, 0))
    elif PlayerNumber == 2:
        TimeOverText = WarningFont.render("Second Player TimeOver!", True, (255, 0, 0))

# --- Begin Setup ---

NoSpendTimerBackground2.Xpos = ScreenWidth / 2
AreaClassificationStick.Xpos = ScreenWidth / 2 - AreaClassificationStick.Width / 2
NowSpendTimerBackground.Xpos = 99999

FirstPlayer.IncrementTime = int(input("첫번째 사람의 추가 시간을 입력해주세요(초 단위) : "))
SecondPlayer.IncrementTime = int(input("첫번째 사람의 추가 시간을 입력해주세요(초 단위) : "))

# --- Game ---

running = True 

while running:

    # --- Tick --- (매번 반복문 시작에 반복되어야 하는 코드들)

    DeltaTime = clock.tick(30)
    NowTicks = pygame.time.get_ticks()
    if TimeOver == False:
        if FirstPlayer.RemainingTime <= 0 and TotalMove != 0:
            FirstPlayer.RemainingTime = 0
            GameOver(1)
        elif SecondPlayer.RemainingTime <= 0 and TotalMove != 0:
            SecondPlayer.RemainingTime = 0
            GameOver(2)

    # text
        
    FirstPlayerTimer = TimerFont.render("Time : " + str(int(FirstPlayer.RemainingTime / 60)) + " : " + str(int(FirstPlayer.RemainingTime % 60)), True, (255, 255, 255)) 
    SecondPlayerTimer = TimerFont.render("Time : " + str(int(SecondPlayer.RemainingTime / 60)) + " : " + str(int(SecondPlayer.RemainingTime % 60)), True, (255, 255, 255)) 
    TotalMoveText = MoveValueFont.render("Move : " + str(TotalMove), True, (255, 255, 255))
    DeveloperText = DeveloperFont.render("Made by Kopeng", True, (255, 255, 255))
    global TimeOverText

    # Game Logic & Events

    if TimeOver == False:
        if FirstPlayer.bPlay == True:
            ElapsedTime = NowTicks - FirstPlayer.LastUpdatedTime
            FirstPlayer.RemainingTime -= ElapsedTime / 1000
            FirstPlayer.LastUpdatedTime = NowTicks
        elif SecondPlayer.bPlay == True:
            ElapsedTime = NowTicks - SecondPlayer.LastUpdatedTime
            SecondPlayer.RemainingTime -= ElapsedTime / 1000
            SecondPlayer.LastUpdatedTime = NowTicks

    for event in pygame.event.get(): 
        
        if event.type == pygame.KEYDOWN: 
            if event.key == pygame.K_h: 
                running = False
        if TimeOver == False:
            if event.type == pygame.MOUSEBUTTONDOWN:
                TouchFinger.Xpos = pygame.mouse.get_pos()[0]
                TouchFinger.Ypos = pygame.mouse.get_pos()[1]
                # 충돌 감지
                if (NoSpendTimerBackground.Xpos < TouchFinger.Xpos and NoSpendTimerBackground.Xpos + NoSpendTimerBackground.Width > TouchFinger.Xpos) and (FirstPlayer.bPlay == False and SecondPlayer.bPlay == False):
                    SecondPlayer.bPlay = True
                    SecondPlayer.LastUpdatedTime = NowTicks
                    NowSpendTimerBackground.Xpos = ScreenWidth / 2
                    TotalMove += 1
                    TurnChangeSoundEffect.play()
                else:
                    if (NoSpendTimerBackground.Xpos < TouchFinger.Xpos and NoSpendTimerBackground.Xpos + NoSpendTimerBackground.Width > TouchFinger.Xpos) and (FirstPlayer.bPlay == True):
                        FirstPlayer.bPlay = False
                        SecondPlayer.bPlay = True
                        SecondPlayer.LastUpdatedTime = NowTicks
                        NowSpendTimerBackground.Xpos = ScreenWidth / 2
                        TotalMove += 1
                        TurnChangeSoundEffect.play()
                        FirstPlayer.RemainingTime += FirstPlayer.IncrementTime

                    elif (NoSpendTimerBackground2.Xpos < TouchFinger.Xpos and NoSpendTimerBackground2.Xpos + NoSpendTimerBackground2.Width > TouchFinger.Xpos) and (SecondPlayer.bPlay == True):
                        FirstPlayer.bPlay = True
                        SecondPlayer.bPlay = False
                        FirstPlayer.LastUpdatedTime = NowTicks
                        NowSpendTimerBackground.Xpos = 0
                        TotalMove += 1
                        TurnChangeSoundEffect.play()
                        SecondPlayer.RemainingTime += SecondPlayer.IncrementTime

    
    Screen.blit(NoSpendTimerBackgroundImage, (NoSpendTimerBackground.Xpos, NoSpendTimerBackground.Ypos))
    Screen.blit(NoSpendTimerBackgroundImage, (NoSpendTimerBackground2.Xpos, NoSpendTimerBackground2.Ypos))
    Screen.blit(NowSpendTimerBackgroundImage, (NowSpendTimerBackground.Xpos, NowSpendTimerBackground.Ypos))
    Screen.blit(AreaClassificationStickImage, (AreaClassificationStick.Xpos, AreaClassificationStick.Ypos))
    Screen.blit(FirstPlayerTimer, (ScreenWidth / 8, ScreenHeight / 2))
    Screen.blit(SecondPlayerTimer, (ScreenWidth / 2 + ScreenWidth / 8, ScreenHeight / 2))
    Screen.blit(TotalMoveText, (ScreenWidth / 8 * 3.15, ScreenHeight / 16))
    Screen.blit(DeveloperText, (ScreenWidth - 150, ScreenHeight - 30))
    if TimeOver == True:
        Screen.blit(TimeOverText, (ScreenWidth / 8 * 1.3, ScreenHeight / 2))

    pygame.display.update()

pygame.quit()