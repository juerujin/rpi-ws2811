# Simple test for NeoPixels on Raspberry Pi
import time
import board
import neopixel
import random
import serial



# Choose an open pin connected to the Data In of the NeoPixel strip, i.e. board.D18
# NeoPixels must be connected to D10, D12, D18 or D21 to work.
pixel_pin = board.D18

# The number of NeoPixels
num_pixels = 50

# The order of the pixel colors - RGB or GRB. Some NeoPixels have red and green reversed!
# For RGBW NeoPixels, simply change the ORDER to RGBW or GRBW.
ORDER = neopixel.GRB

pixels = neopixel.NeoPixel(pixel_pin, num_pixels, brightness=0.2, auto_write=False, pixel_order=ORDER)

wait_time = 1


def colorAll2Color(c1, c2):
    for i in range(num_pixels):
        if(i % 2 == 0): # even
            pixels[i] = c1
        else: # odd   
            pixels[i] = c2
    pixels.show()


def wheel(pos):
    # Input a value 0 to 255 to get a color value.
    # The colours are a transition r - g - b - back to r.
    if pos < 0 or pos > 255:
        r = g = b = 0
    elif pos < 85:
        r = int(pos * 3)
        g = int(255 - pos*3)
        b = 0
    elif pos < 170:
        pos -= 85
        r = int(255 - pos*3)
        g = 0
        b = int(pos*3)
    else:
        pos -= 170
        r = 0
        g = int(pos*3)
        b = int(255 - pos*3)
    return (r, g, b) if ORDER == neopixel.RGB or ORDER == neopixel.GRB else (r, g, b, 0)


def rainbow_cycle(delay):
    for j in range(255):
        for i in range(num_pixels):
            pixel_index = (i * 256 // num_pixels) + j
            pixels[i] = wheel(pixel_index & 255)
        pixels.show()
        time.sleep(delay)


def RGBLoop(delay):
    for j in range(3):
        # Fade IN
        for k in range(256):
            if j == 0:
                pixels.fill((k, 0, 0))
            elif j == 1:
                pixels.fill((0, k, 0))
            elif j == 2:
                pixels.fill((0, 0, k))
            pixels.show()
            time.sleep(delay)

        # Fade OUT
        for k in range(256):
            if j == 2:
                pixels.fill((k, 0, 0))
            elif j == 1:
                pixels.fill((0, k, 0))
            elif j == 0:
                pixels.fill((0, 0, k))
            pixels.show()
            time.sleep(delay)
    
def FadeInOut(red, green, blue, delay):
    r = 0
    g = 0
    b = 0
      
    for k in range(256):
        r = (k/256.0)*red
        g = (k/256.0)*green
        b = (k/256.0)*blue
        pixels.fill((int(r), int(g), int(b)))
        pixels.show()
        time.sleep(delay)
     
    for k in range(256, -1, -1):
        r = (k/256.0)*red
        g = (k/256.0)*green
        b = (k/256.0)*blue
        pixels.fill((int(r), int(g), int(b)))
        pixels.show()
        time.sleep(delay)

def Strobe(red, green, blue, StrobeCount, FlashDelay, EndPause):
    for j in range(StrobeCount):
        pixels.fill((red,green,blue))
        pixels.show()
        time.sleep(FlashDelay)
        pixels.fill((0,0,0))
        pixels.show()
        time.sleep(FlashDelay)
 
    time.sleep(EndPause)


    
def HalloweenEyes(red, green, blue, EyeWidth, EyeSpace, Fade, Steps, FadeDelay, EndPause):
    random.seed(num_pixels)
    pixels.fill((0,0,0))
    r = 0
    g = 0
    b = 0

    # define eye1 and eye2 location
    StartPoint  = random.randint( 0, num_pixels - (2*EyeWidth) - EyeSpace )
    Start2ndEye = StartPoint + EyeWidth + EyeSpace

    #  set color of eyes for given location
    for i in range(EyeWidth):
        pixels[StartPoint + i] = (red, green, blue)
        pixels[Start2ndEye + i] = (red, green, blue)
    pixels.show()

    # if user wants fading, then fadeout pixel color
    if Fade == True:
        for j in range(Steps, -1, -1):
            r = (j/Steps)*red
            g = (j/Steps)*green
            b = (j/Steps)*blue

            for i in range(EyeWidth):
                pixels[StartPoint + i] = ((int(r), int(g), int(b)))
                pixels[Start2ndEye + i] = ((int(r), int(g), int(b)))

            pixels.show()
            time.sleep(FadeDelay)
    
    # Set all pixels to black
    pixels.fill((0,0,0))

    # pause before changing eye location
    time.sleep(EndPause)


def CylonBounce(red, green, blue, EyeSize, SpeedDelay, ReturnDelay):
  
    for i in range(num_pixels - EyeSize - 1):
        pixels.fill((0,0,0))
        pixels[i] = (int(red/10), int(green/10), int(blue/10))

        for j in range(1, EyeSize+1):
            pixels[i+j] = (red, green, blue)

        pixels[i+EyeSize+1] = (int(red/10), int(green/10), int(blue/10))
        pixels.show()
        time.sleep(SpeedDelay)
  
    time.sleep(ReturnDelay)
    time.sleep(10)
    
    for i in range(num_pixels - EyeSize - 2, -1, -1):
        pixels.fill((0,0,0))
        pixels[i] = (int(red/10), int(green/10), int(blue/10))

        for j in range(1, EyeSize+1):
            pixels[i+j] = (red, green, blue)

        pixels[i+EyeSize+1] = (int(red/10), int(green/10), int(blue/10))
        pixels.show()
        time.sleep(SpeedDelay)

    time.sleep(ReturnDelay)
    time.sleep(10)

def NewKITT(red, green, blue, EyeSize, SpeedDelay, ReturnDelay):
    RightToLeft(red, green, blue, EyeSize, SpeedDelay, ReturnDelay)
    LeftToRight(red, green, blue, EyeSize, SpeedDelay, ReturnDelay)
    OutsideToCenter(red, green, blue, EyeSize, SpeedDelay, ReturnDelay)
    CenterToOutside(red, green, blue, EyeSize, SpeedDelay, ReturnDelay)
    LeftToRight(red, green, blue, EyeSize, SpeedDelay, ReturnDelay)
    RightToLeft(red, green, blue, EyeSize, SpeedDelay, ReturnDelay)
    OutsideToCenter(red, green, blue, EyeSize, SpeedDelay, ReturnDelay)
    CenterToOutside(red, green, blue, EyeSize, SpeedDelay, ReturnDelay)

def CenterToOutside(red, green, blue, EyeSize, SpeedDelay, ReturnDelay):
    for i in range(int((num_pixels - EyeSize)/2), -1, -1):
        pixels.fill((0,0,0))
        pixels[i] = (int(red/10), int(green/10), int(blue/10))

        for j in range(1, EyeSize+1):
            pixels[i + j] = (red, green, blue)
        
        pixels[i + EyeSize + 1] = (int(red/10), int(green/10), int(blue/10))
        pixels[num_pixels - i - j] = (int(red/10), int(green/10), int(blue/10))

        for j in range(1, EyeSize+1):
            pixels[num_pixels - i - j] = (red, green, blue)

        pixels[num_pixels - i - EyeSize - 1] = (int(red/10), int(green/10), int(blue/10))
        pixels.show()
        time.sleep(SpeedDelay)

    time.sleep(ReturnDelay)

def OutsideToCenter(red, green, blue, EyeSize, SpeedDelay, ReturnDelay):

    for i in range(int(((num_pixels - EyeSize)/2)+1)):
        pixels.fill((0,0,0))
        pixels[i] = (int(red/10), int(green/10), int(blue/10))

        for j in range(1, EyeSize+1):
            pixels[i + j] = (red, green, blue) 
        
        pixels[i + EyeSize +1] = (int(red/10), int(green/10), int(blue/10))
        pixels[num_pixels - i-1] = (int(red/10), int(green/10), int(blue/10))

        for j in range(1, EyeSize+1):
            pixels[num_pixels - i - j] = (red, green, blue)
        
        pixels[num_pixels - i - EyeSize - 1] = (int(red/10), int(green/10), int(blue/10))
        pixels.show()
        time.sleep(SpeedDelay)
  
    time.sleep(ReturnDelay)


def LeftToRight(red, green, blue, EyeSize, SpeedDelay, ReturnDelay):
    for i in range(num_pixels - EyeSize - 2):
        pixels.fill((0,0,0))
        pixels[i] = (int(red/10), int(green/10), int(blue/10))

        for j in range(1, EyeSize+1):
            pixels[i + j] = (red, green, blue)

        pixels[i + EyeSize + 1] = (int(red/10), int(green/10), int(blue/10))
        pixels.show()
        time.sleep(SpeedDelay)
    
    time.sleep(ReturnDelay)


def RightToLeft(red, green, blue, EyeSize, SpeedDelay, ReturnDelay):
    for i in range(num_pixels - EyeSize - 2, 0, -1):
        pixels.fill((0,0,0))
        pixels[i] = (int(red/10), int(green/10), int(blue/10))

        for j in range(1, EyeSize+1):
            pixels[i + j] = (red, green, blue)

        pixels[i + EyeSize + 1] = (int(red/10), int(green/10), int(blue/10))
        pixels.show()
        time.sleep(SpeedDelay)
  
    time.sleep(ReturnDelay)


def Twinkle(red, green, blue, Count, SpeedDelay, OnlyOne):
    random.seed(num_pixels)
    pixels.fill((0,0,0))
  
    for i in range(Count):
        pixels[random.randint(0, num_pixels-1)] = (red, green, blue)
        pixels.show()
        time.sleep(SpeedDelay)
        if OnlyOne:
            pixels.fill((0,0,0))

    time.sleep(SpeedDelay)


def TwinkleRandom( Count, SpeedDelay, OnlyOne):
    pixels.fill(0,0,0)

    for i in range(Count):
        pixels[random.randint(0, num_pixels-1)] = (random.randint(0,255), random.randint(0,255), random.randint(0,255))
        pixels.show()
        time.sleep(SpeedDelay)
        if OnlyOne:
            pixels.fill((0,0,0))

  time.sleep(SpeedDelay)


while True:
    # make all pixels Red
    # fill(red, green, blue)
    pixels.fill((255, 0, 0)) # red
    pixels.show()
    time.sleep(wait_time)

    # make all pixels Green
    # fill(red, green, blue)
    pixels.fill((0, 255, 0))
    pixels.show()
    time.sleep(wait_time)

    # make all pixels Blue
    # fill(red, green, blue)
    pixels.fill((0, 0, 255))
    pixels.show()
    time.sleep(wait_time)

    # makes the strand of pixels show TwinkleRandom
    # TwinkleRandom( Count, SpeedDelay, OnlyOne) 
    TwinkleRandom(20, 0.1, False)

    # makes the strand of pixels show Twinkle
    # Twinkle(red, green, blue, Count, SpeedDelay, OnlyOne)
    Twinkle(255, 0, 0, 10, 0.1, False)

    # makes the strand of pixels show NewKITT 
    # NewKITT(red, green, blue, EyeSize, SpeedDelay, ReturnDelay)
    NewKITT(255, 0, 0, 4, 0.010, 0.050)
    time.sleep(wait_time)

    # makes the strand of pixels show CylonBounce
    # CylonBounce(red, green, blue, EyeSize, SpeedDelay, ReturnDelay)
    CylonBounce(255, 0, 0, 2, 0.010, 0.050)
    time.sleep(wait_time)

    # make the strand of pixels show HalloweenEyes
    # HalloweenEyes(red, green, blue, EyeWidth, EyeSpace, Fade, Steps, FadeDelay, EndPause)
    HalloweenEyes(255, 0, 0, 1, 1, True, 10, 1, 3)
    time.sleep(wait_time)

    # make all pixels stobe (white)
    # Strobe(red, green, blue, StrobeCount, FlashDelay, EndPause)
    Strobe(255, 255, 255, 10, .050, 1)
    time.sleep(wait_time)


    # fade in/out a single color (red / green / blue / white)
    # FadeInOut(red, green, blue, delay)
    FadeInOut(255, 0, 0, 0.01)
    FadeInOut(0, 255, 0, 0.01)
    FadeInOut(0, 0, 255, 0.01)
    FadeInOut(255, 255, 255, 0.01)

    # loops red green blue
    # RGBLoop(delay)
    RGBLoop(0.01)
    time.sleep(wait_time)

    # shows 2 color every other pixel (red, green)
    # colorAll2Color((red1, green1, blue1), (red2, green2, blue2)) 
    colorAll2Color((255, 0, 0), (0, 255, 0)) 
    time.sleep(wait_time)

    # rainbow cycle
    rainbow_cycle(0.001)    # rainbow cycle with 1ms delay per step
    time.sleep(wait_time)

