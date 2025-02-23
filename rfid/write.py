"""
Example of writing to a card using the ``mfrc522`` module.
"""

# 3rd party
import board

# this package
import mfrc522

rdr = mfrc522.MFRC522(board.GP2, board.GP3, board.GP4, board.GP5, board.GP0)
rdr.set_antenna_gain(0x07 << 4)

print('')
print("Place card before reader to write address 0x08")
print('')

def padOut(bytz, extras):
    return bytz + "\0" * extras

def write_string(text):
    try:
        while True:

            (stat, tag_type) = rdr.request(rdr.REQIDL)

            if stat == rdr.OK:

                (stat, raw_uid) = rdr.anticoll()

                if stat == rdr.OK:
                    print("New card detected")
                    print("  - tag type: 0x%02x" % tag_type)
                    print("  - uid\t : 0x%02x%02x%02x%02x" % (raw_uid[0], raw_uid[1], raw_uid[2], raw_uid[3]))
                    print('')

                    if rdr.select_tag(raw_uid) == rdr.OK:

                        key = [0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF]

                        if rdr.auth(rdr.AUTHENT1A, 8, key, raw_uid) == rdr.OK:
                            stat = rdr.write(
                                    8, padOut(text.encode('ASCII'), 16 - len(text))
                                    )
                            rdr.stop_crypto1()
                            if stat == rdr.OK:
                                print("Data written to card")
                            else:
                                print("Failed to write data to card")
                        else:
                            print("Authentication error")
                    else:
                        print("Failed to select tag")

    except KeyboardInterrupt:
        print("Bye")

write_string("Hello world!")
