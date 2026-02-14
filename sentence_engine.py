import random

TEMPLATES = [
"both {e1} and {e2}, and my body feels {b}.",
"a mix of {e1} and {e2}, with a {b} sensation.",
"{e1} yet {e2}, while physically I am {b}.",
"waves of {e1} and {e2}, making me feel {b}.",
"simultaneously {e1} and {e2}, and physically {b}.",
"caught between {e1} and {e2}, with a {b} feeling.",
"a combination of {e1} and {e2}, and my body is {b}.",
"overwhelmed by {e1} and {e2}, causing a {b} sensation.",
"{e1} mixed with {e2}, and physically quite {b}.",
"like there is {e1} and {e2}, and my chest feels {b}.",
"full of {e1} and {e2}, which leaves me {b}.",
"a sense of {e1} and {e2}, and my limbs feel {b}.",
"deeply {e1} and {e2}, with a {b} physical reaction.",
"moments of {e1} and {e2}, and a {b} feeling in my body.",
"immersed in {e1} and {e2}, and physically {b}.",
"that {e1} and {e2} are present, making me {b}.",
"{e1} alongside {e2}, and my stomach feels {b}.",
"mostly {e1} but also {e2}, with a {b} sensation.",
"suddenly {e1} and {e2}, and my body becomes {b}.",
"like a blend of {e1} and {e2}, creating a {b} feeling.",
"hints of {e1} and {e2}, while my muscles feel {b}.",
"intensely {e1} and {e2}, and physically {b}.",
"shifting between {e1} and {e2}, with a {b} sensation.",
"heavy with {e1} and {e2}, and my head feels {b}.",
"filled with {e1} and {e2}, and a {b} physical state.",
"touched by {e1} and {e2}, and noticeably {b}.",
"affected by {e1} and {e2}, while feeling {b}.",
"entirely {e1} and {e2}, and my skin feels {b}.",
"a surge of {e1} and {e2}, leaving my body {b}.",
"grounded in {e1} and {e2}, with a {b} feeling.",
]

def build_sentence(e1, e2, body):
    t = random.choice(TEMPLATES)
    return t.format(e1=e1, e2=e2, b=body)
