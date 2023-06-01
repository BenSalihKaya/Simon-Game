from machine import Pin, I2C
from ssd1306 import SSD1306_I2C
from oled import Write, GFX, SSD1306_I2C
from oled.fonts import ubuntu_mono_20
import utime
import urandom


MAX_LEVEL = 100 
sequence = [0] * MAX_LEVEL
sound = [0] * MAX_LEVEL
player_sequence = [0] * MAX_LEVEL
level = 1
note = 0
velocity = 1000

# Piezo Sounds
GRN_SOUND = 261
RED_SOUND = 293
YEL_SOUND = 329
BLU_SOUND = 349
BAD_SOUND = 233

# LED Definitions
GRN_LED = machine.Pin(13, machine.Pin.OUT)
RED_LED = machine.Pin(12, machine.Pin.OUT)
YEL_LED = machine.Pin(11, machine.Pin.OUT)
BLU_LED = machine.Pin(10, machine.Pin.OUT)

# Pushbutton Definitions
GRN_BTN = machine.Pin(18, machine.Pin.IN, machine.Pin.PULL_UP)
RED_BTN = machine.Pin(19, machine.Pin.IN, machine.Pin.PULL_UP)
YEL_BTN = machine.Pin(20, machine.Pin.IN, machine.Pin.PULL_UP)
BLU_BTN = machine.Pin(21, machine.Pin.IN, machine.Pin.PULL_UP)

# Piezo Buzzer
PIEZO = machine.Pin(3, machine.Pin.OUT)
piezo_pwm = machine.PWM(PIEZO)

WIDTH = 128
HEIGHT = 64
i2c = I2C(0, scl=Pin(1), sda=Pin(0), freq=200000)
oled = SSD1306_I2C(WIDTH, HEIGHT, i2c)
write = Write(oled, ubuntu_mono_20)
def display_brain():
    # Beyin resmini ekranda göster
    oled.fill(0)
    oled.text("****************", 0, 0)
    oled.text("***<--------->------***************", 0, 10)
    oled.text("***-------***************", 0, 20)
    oled.text("***-------***************", 0, 30)
    oled.text("***-------***************", 0, 40)
    oled.text("***-------***************", 0, 50)
    oled.text("**********************************", 0, 60)
    oled.show()
def setup():
    # LEDs are Outputs5
    GRN_LED.off()
    RED_LED.off()
    YEL_LED.off()
    BLU_LED.off()

    # Initialize OLED Display
    """display_brain()"""
    utime.sleep(1)
    oled.fill(0)
    write.text("SIMON", 40,15)
    write.text("GAME", 45, 30)
    oled.show()
    utime.sleep(1)

def generate_sequence():
    # Generates random sequence
    for i in range(MAX_LEVEL):
        # Random values will match LED output pins
        sequence[i] = urandom.choice([BLU_LED, YEL_LED, RED_LED, GRN_LED])

        if sequence[i] == BLU_LED:
            note = BLU_SOUND
        elif sequence[i] == YEL_LED:
            note = YEL_SOUND
        elif sequence[i] == RED_LED:
            note = RED_SOUND
        elif sequence[i] == GRN_LED:
            note = GRN_SOUND

        # Sound will match LED output
        sound[i] = note

def show_sequence():
    # Turn off all LEDs
    GRN_LED.off()
    RED_LED.off()
    YEL_LED.off()
    BLU_LED.off()

    
    oled.fill(0)
    write.text("LEVEL: {}".format(level), 25, 25)
    oled.show()

    for i in range(level):
        sequence[i].on()
        piezo_pwm.freq(sound[i])
        piezo_pwm.duty_u16(32768)  # 50% duty cycle
        utime.sleep_ms(velocity)
        sequence[i].off()
        piezo_pwm.duty_u16(0)
        utime.sleep(0.2)

def get_sequence():
    # Get sequence user enters
    for i in range(level):
        flag = False

        while not flag:
            if GRN_BTN.value() == 0:
                GRN_LED.on()
                piezo_pwm.freq(GRN_SOUND)
                piezo_pwm.duty_u16(32768)  # 50% duty cycle
                utime.sleep_ms(velocity)
                player_sequence[i] = GRN_LED
                flag = True
                utime.sleep(0.2)

                if player_sequence[i] != sequence[i]:
                    wrong_sequence()
                    return
                GRN_LED.off()
                piezo_pwm.duty_u16(0)

            if RED_BTN.value() == 0:
                RED_LED.on()
                piezo_pwm.freq(RED_SOUND)
                piezo_pwm.duty_u16(32768)  # 50% duty cycle
                utime.sleep_ms(velocity)
                player_sequence[i] = RED_LED
                flag = True
                utime.sleep(0.2)

                if player_sequence[i] != sequence[i]:
                    wrong_sequence()
                    return
                RED_LED.off()
                piezo_pwm.duty_u16(0)

            if YEL_BTN.value() == 0:
                YEL_LED.on()
                piezo_pwm.freq(YEL_SOUND)
                piezo_pwm.duty_u16(32768)  # 50% duty cycle
                utime.sleep_ms(velocity)
                player_sequence[i] = YEL_LED
                flag = True
                utime.sleep(0.2)

                if player_sequence[i] != sequence[i]:
                    wrong_sequence()
                    return
                YEL_LED.off()
                piezo_pwm.duty_u16(0)

            if BLU_BTN.value() == 0:
                BLU_LED.on()
                piezo_pwm.freq(BLU_SOUND)
                piezo_pwm.duty_u16(32768)  # 50% duty cycle
                utime.sleep_ms(velocity)
                player_sequence[i] = BLU_LED
                flag = True
                utime.sleep(0.2)

                if player_sequence[i] != sequence[i]:
                    wrong_sequence()
                    return
                BLU_LED.off()
                piezo_pwm.duty_u16(0)

def wrong_sequence():
    # Handle wrong sequence entered by the player
    for i in range(3):
        piezo_pwm.freq(BAD_SOUND)
        piezo_pwm.duty_u16(32768)  # 50% duty cycle
        utime.sleep_ms(500)
        piezo_pwm.duty_u16(0)
        utime.sleep(0.5)
    game_over()

def game_over():
    # Game over, show final score
    oled.fill(0)
    write.text("GAME OVER", 20,15)
    write.text("SCORE: {}".format(level), 20, 30)
    oled.show()
    GRN_LED.on()
    RED_LED.on()
    YEL_LED.on()
    BLU_LED.on()
    utime.sleep(0.2)
    GRN_LED.off()
    RED_LED.off()
    YEL_LED.off()
    BLU_LED.off()
    utime.sleep(0.2)
    GRN_LED.on()
    RED_LED.on() 
    YEL_LED.on()
    BLU_LED.on()
    utime.sleep(0.2)
    GRN_LED.off()
    RED_LED.off()
    YEL_LED.off()
    BLU_LED.off()
    utime.sleep(0.2)

    for i in range(5):
        piezo_pwm.freq(BAD_SOUND)
        piezo_pwm.duty_u16(32768)  # 50% duty cycle
        utime.sleep_ms(200)
        piezo_pwm.duty_u16(0)
        utime.sleep(0.2)

    utime.sleep(2)
    restart_game()

def restart_game():
    # Restart the game
    global level
    level = 0
    generate_sequence()
    show_sequence()

def play_game():
    # Play the game
    global level
    setup()
    generate_sequence()
    show_sequence()

    while True:
        get_sequence()
        level += 1
        show_sequence()

# Start the game
play_game()





