
from gpiozero import LED

t_magnet = LED(12)
e_magnet = LED(16)
a_magnet = LED(20)
question_mark_magnet = LED(21)


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
