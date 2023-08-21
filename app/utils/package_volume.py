package_volume = {
    'gig': 'گیگ',
    'meg': 'مگ',
    'مگ': 'مگ',
    'مگابایت': 'مگ',
    'مگا بایت': 'مگ',
    'mega': 'مگ',
    'megabite': 'مگ',
    'گیگ': 'گیگ',
    'گیگابایت': 'گیگ',
    'گیگا': 'گیگ'
}


def find_package_volume(volume):
    for key, value in package_volume.items():
        if key == volume:
            return value
    return 'گیگ'
