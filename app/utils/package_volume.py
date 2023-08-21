package_volume = {
    'gig': 'گیگابایت',
    'meg': 'مگابایت',
    'مگ': 'مگابایت',
    'مگابایت': 'مگابایت',
    'مگا بایت': 'مگابایت',
    'mega': 'مگابایت',
    'megabite': 'مگابایت',
    'گیگ': 'گیگابایت',
    'گیگابایت': 'گیگابایت',
    'گیگا': 'گیگابایت'
}


def find_package_volume(volume):
    for key, value in package_volume.items():
        if key == volume:
            return value
    return 'گیگابایت'
