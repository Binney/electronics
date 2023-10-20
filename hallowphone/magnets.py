
from gpiozero import LED

t_magnet = LED(17)  # Red
e_magnet = LED(27)  # Blue
a_magnet = LED(22)  # Yellow
question_mark_magnet = LED(23)  # ????? QQ


def enable_t():
    print("Enabling T")
    e_magnet.off()
    a_magnet.off()
    question_mark_magnet.off()
    t_magnet.on()


def enable_e():
    print("Enabling E")
    t_magnet.off()
    a_magnet.off()
    question_mark_magnet.off()
    e_magnet.on()


def enable_a():
    print("Enabling A")
    t_magnet.off()
    e_magnet.off()
    question_mark_magnet.off()
    a_magnet.on()


def enable_question_mark():
    print("Enabling ?")
    t_magnet.off()
    e_magnet.off()
    a_magnet.off()
    question_mark_magnet.on()
