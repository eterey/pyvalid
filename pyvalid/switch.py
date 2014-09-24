def turn_on():
    globals()['pyvalid_enabled'] = True


def turn_off():
    globals()['pyvalid_enabled'] = False


def is_enabled():
    if 'pyvalid_enabled' in globals():
        enabled = globals()['pyvalid_enabled']
    else:
        enabled = True
    return enabled
