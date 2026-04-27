def map_to_pitch(a):
    return int(36 + (a * (84 - 36)))


def map_to_tempo(b):
    return int(60 + (b * (140 - 60)))


def map_to_duration(d):
    return 0.25 + (d * (1.0 - 0.25))


def map_to_velocity(t):
    return int(40 + (t * (127 - 40)))


def map_to_octave(g):
    if g < 0.33:
        return -12
    elif g < 0.66:
        return 0
    else:
        return 12
