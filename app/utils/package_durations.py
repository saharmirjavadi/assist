package_duration = {
    'روزانه': 'روزانه',
    'یه روزه': 'روزانه',
    'یکروزه': 'روزانه',
    'یکروز': 'روزانه',
    'سه روزه': 'سه روزه',
    'سه روز': 'سه روزه',
    '3 روز': 'سه روزه',
    'هفتگی': 'هفتگی',
    'هفت روزه': 'هفتگی',
    '۷ روزه': 'هفتگی',
    '7 روزه': 'هفتگی',
    'یه هفته': 'هفتگی',
    'یه هفته ای': 'هفتگی',
    'پانزده روزه': 'پانزده روزه',
    'پانزده روز': 'پانزده روزه',
    '15 روزه': 'پانزده روزه',
    '۱۵ روزه': 'پانزده روزه',
    '30 روزه': 'سی روزه',
    '۳۰ روزه': 'سی روزه',
    'سیروزه': 'سی روزه',
    'سی روزه': 'سی روزه',
    'سی روز': 'سی روزه',
    '30 روز': 'سی روزه',
    '۳۰ روز': 'سی روزه',
    'یه ماهه': 'سی روزه',
    'ماهانه': 'سی روزه',
    'یک ماهه': 'سی روزه',
    'ماهی': 'سی روزه',
    'سه ماهه': 'سه ماهه',
    'سه ماه': 'سه ماهه',
    '90 روزه': 'سه ماهه',
    '۹۰ روزه': 'سه ماهه',
    '۹۰ روز': 'سه ماهه',
    'سه ماهی': 'سه ماهه',
    '۶ ماهی': 'شش ماهه',
    'شیش ماهه': 'شش ماهه',
    'شیش ماه': 'شش ماهه',
    'شش ماه': 'شش ماهه',
    'شش ماهی': 'شش ماهه',
    '۶ ماه': 'شش ماهه',
    '6 ماه': 'شش ماهه',
    'شش ماهی': 'شش ماهه',
    'سالانه': 'سالانه',
    'سالی': 'سالانه',
    'یه ساله': 'سالانه',
    'یه سال': 'سالانه',
    'یک سال': 'سالانه',
    'یک ساله': 'سالانه',
}


def find_package_duration(sentence):
    for key, value in package_duration.items():
        if key in sentence:
            return value
    return 'روزانه'
