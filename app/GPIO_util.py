from app import config

# if this isn't a pi, this import throws an exception 
NOT_A_PI=False
try:
    import RPi.GPIO as GPIO
except Exception as e:
    NOT_A_PI = True


PENCIL_SHARPENER = 17
RESPONSE_BUTTON = 19
LED_A_LEVEL = 27
LED_1_LEVEL = 22

SITE_VERIFY_URL = config.RECAPTCHA_SITE_VERIFY_URL
SECRET_KEY = config.RECAPTCHA_SECRET_KEY

#that is to say, if it is in fact a pi
if not NOT_A_PI:
    set_gpio_mode()


def set_gpio_mode():

    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(PENCIL_SHARPENER, GPIO.OUT)
    GPIO.setup(RESPONSE_BUTTON, GPIO.IN,  pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(LED_A_LEVEL, GPIO.OUT)
    GPIO.setup(LED_1_LEVEL, GPIO.OUT)

    GPIO.output(PENCIL_SHARPENER, GPIO.LOW)
    GPIO.output(LED_A_LEVEL, GPIO.LOW)
    GPIO.output(LED_1_LEVEL, GPIO.LOW)

    #GPIO.output(PENCIL_SHARPENER, GPIO.HIGH)
    #GPIO.output(LED_A_LEVEL, GPIO.HIGH)
    #GPIO.output(LED_1_LEVEL, GPIO.HIGH)

def success(success, body):
    if success:
        level = body['level']
        startTime = time.time()

        print("Activating: " + level, file=sys.stderr)

        GPIO.output(PENCIL_SHARPENER, GPIO.HIGH)

        if level == '1Level':
            GPIO.output(LED_1_LEVEL, GPIO.HIGH)
        elif level == 'aLevel':
            GPIO.output(LED_A_LEVEL, GPIO.HIGH)

        while True:

            elapsedTime = time.time() - startTime
            timedOut = elapsedTime > 45
            buttonPressed = GPIO.input(RESPONSE_BUTTON)

            if timedOut or buttonPressed:

                GPIO.output(PENCIL_SHARPENER, GPIO.LOW)
                GPIO.output(LED_1_LEVEL, GPIO.LOW)
                GPIO.output(LED_A_LEVEL, GPIO.LOW)

                if timedOut:
                    print("Button timed out", file=sys.stderr)
                    return "timeout"
                elif buttonPressed:
                    print("Button pressed", file=sys.stderr)
                    return "buttonpressed"
                return ""
    else:
        GPIO.output(PENCIL_SHARPENER, GPIO.LOW)
        GPIO.output(LED_1_LEVEL, GPIO.LOW)
        GPIO.output(LED_A_LEVEL, GPIO.LOW)
        print("Not Verified", file=sys.stderr)
        return "not verified"

def shutdown():
    print("Goodbye", file=sys.stderr)
    GPIO.output(PENCIL_SHARPENER, GPIO.LOW)
    GPIO.output(LED_A_LEVEL, GPIO.LOW)
    GPIO.output(LED_1_LEVEL, GPIO.LOW)