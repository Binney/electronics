from flask import Flask, request
from gpiozero import LED
from time import sleep

app = Flask(__name__)

lightamarino = LED(14)

DEFAULT_NUM_STICKERS = '3'

@app.route('/')
def index():
    lightamarino.toggle()
    return 'Hello, world!'

@app.route('/dispense', methods=['GET','POST'])
def dispense():
    num_stickers = int(request.args.get('stickers', DEFAULT_NUM_STICKERS))
    for i in range(num_stickers):
        lightamarino.on()
        sleep(1)
        lightamarino.off()
        sleep(1)
    return 'I dispensed ' + str(num_stickers) + ' stickers!'

if __name__ == '__main__':
    app.run(debug=True)
