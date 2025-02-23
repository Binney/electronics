print("Hello World!")

import board
import mfrc522

rdr = mfrc522.MFRC522(board.GP2, board.GP3, board.GP4, board.GP5, board.GP0)

rdr.set_antenna_gain(0x07 << 4)

print('')
print("Place card before reader to read from address 0x08")
print('')

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

                    auth_result = rdr.auth(rdr.AUTHENT1A, 8, key, raw_uid)
                    print(auth_result)
                    if auth_result == rdr.OK:
                        rslt = rdr.read(8)
                        print("Address 8 data: %s" % rslt)
                        print(bytes(rslt).decode("ASCII"))
                        rdr.stop_crypto1()
                    else:
                        print("Authentication error")
                else:
                    print("Failed to select tag")

except KeyboardInterrupt:
    print("bye")