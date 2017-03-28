# _*_ coding: utf-8 _*_

from django import template
register = template.Library()


NUMBER_DICT = {
    '0': 'ნული',
    '1': 'ერთ',
    '2': 'ორ',
    '3': 'სამ',
    '4': 'ოთხ',
    '5': 'ხუთ',
    '6': 'ექვს',
    '7': 'შვიდ',
    '8': 'რვა',
    '9': 'ცხრა',
    '10': 'ათი',
    '11': 'თერთმეტი',
    '12': 'თორმეტი',
    '13': 'ცამეტი',
    '14': 'თოთხმეტი',
    '15': 'თხუთმეტი',
    '16': 'თექვსმეტი',
    '17': 'ჩვიდმეტი',
    '18': 'თვრამეტი',
    '19': 'ცხრამეტი',
    '20': 'ოცი'
}


def under_100(oci, nashti):
    if oci == 0:
        return NUMBER_DICT[str(nashti)]
    elif oci == 1:
        if nashti > 0:
            if nashti > 10 or nashti == 9 or nashti == 8:
                return 'ოცდა' + NUMBER_DICT[str(nashti)]
            return 'ოცდა' + NUMBER_DICT[str(nashti)] + 'ი'
        else:
            return NUMBER_DICT['20']
    elif oci == 2:
        if nashti > 0:
            if nashti > 10 or nashti == 9 or nashti == 8:
                return 'ორმოცდა' + NUMBER_DICT[str(nashti)]
            else:
                return 'ორმოცდა' + NUMBER_DICT[str(nashti)] + 'ი'
        else:
            return 'ორმოცი'
    elif oci == 3:
        if nashti > 0:
            if nashti > 10 or nashti == 9 or nashti == 8:
                return 'სამოცდა' + NUMBER_DICT[str(nashti)]
            else:
                return 'სამოცდა' + NUMBER_DICT[str(nashti)] + 'ი'
        else:
            return 'სამოცი'
    elif oci == 4:
        if nashti > 0:
            if nashti > 10 or nashti == 9 or nashti == 8:

                return 'ოთხმოცდა' + NUMBER_DICT[str(nashti)]
            else:
                return 'ოთხმოცდა' + NUMBER_DICT[str(nashti)] + 'ი'
        else:
            return 'ოთხმოცი'


def under_1000(asi, oci, nashti):
    if oci == 0 and nashti == 0:
        if asi == 1:
            return 'ასი'
        return NUMBER_DICT[str(asi)] + 'ასი'
    else:
        under100 = under_100(oci, nashti)
        if asi == 1:
            return 'ას' + under100
        return NUMBER_DICT[str(asi)] + 'ას ' + under100


def intWithCommas(x):
    """

    :param x: რიცხვი
    :return: მძიმეებით გამოყოფილი რიცხვი
    """
    if type(x) not in [type(0), type(0L)]:
        raise TypeError("Parameter must be an integer.")
    if x < 0:
        return '-' + intWithCommas(-x)
    result = ''
    while x >= 1000:
        x, r = divmod(x, 1000)
        result = ",%03d%s" % (r, result)
    return "%d%s" % (x, result)


@register.filter(name='num2geo')
def num2geo(num, format_type, currency=None):
    """

    :param num: არის რიცხვი რომელიც უნდა დაფორმატირდეს
    :param format_type: არის ფორმატის ტიპი. ფორმატის ტიპებია : comma_separated_number, number_with_translate, translate
                        comma_separated_number: აბრუნებს მძიმეებით გამოყოფილ რიცხვს;
                        number_with_translate: აბრუნებს მძიმეებით გამოყოფილ რიცხვს და ასევე თარგმნის მას;
                        translate: აბრუნებს მხოლოდ გადათარგმნილ რიცხვს.
    :param currency: არის არა სავალდებულო პარამეტრი, გადაეცემა tuple რომელშიც წერია ბანკნოტის ერთეული და ხურდის ერთეული,
                     მაგალითად ('ლარი', 'თეთრი')
    :return: აბრუნებს ფორმატის ტიპის მიხედვით დაფორმატებულ რიცხვს. თუ რიცხვის მთელი ნაწილი მეტია 6 სიმბოლოზე მაშინ არ
             თარგმნის და ავომატურად აბრუნებს მძიმეებით გამოყოფილს
    """
    if not isinstance(num, basestring):
        num = str(num)

    if num.find('.') >= 0:
        num = num.split('.')
        integer = long(num[0])
        decimal = num[1]
        _decimal = '0.' + num[1]

    else:
        integer = long(num)
        decimal = '00'
        _decimal = '0.00'
    if format_type == 'comma_separated_number' or len(str(integer)) > 6:
        if currency:
            return intWithCommas(integer) + ' ' + currency[0] + ' და ' + decimal + ' ' + currency[1]
        return intWithCommas(integer) + ' და ' + _decimal

    if len(str(integer)) <= 2:

        oci = integer / 20
        nashti = integer % 20
        if format_type == 'translate':
            if currency:
                return under_100(oci, nashti) + ' ' + currency[0] + ' და ' + decimal + ' ' + currency[1]

            return under_100(oci, nashti) + ' და ' + _decimal
        elif format_type == 'number_with_translate':
            if currency:
                return str(integer) + '.' + decimal + ' ' + currency[0] + ' (' + under_100(oci, nashti) + ' ' + \
                       currency[0] + ' და ' + decimal + ' ' + currency[1] + ')'

            return str(integer) + '.' + decimal + ' (' + under_100(oci, nashti) + ' და ' + _decimal + ')'

    elif len(str(integer)) <= 3:
        asi = integer / 100
        oci = (integer % 100) / 20
        nashti = (integer % 100) % 20
        if format_type == 'translate':
            if currency:
                return under_1000(asi, oci, nashti) + ' ' + currency[0] + ' და ' + decimal + ' ' + currency[1]
            return under_1000(asi, oci, nashti) + ' და ' + _decimal
        elif format_type == 'number_with_translate':

            if currency:
                return str(integer) + '.' + decimal + ' ' + currency[0] + ' (' + under_1000(asi, oci, nashti) + ' ' + \
                       currency[0] + ' და ' + decimal + ' ' + currency[1] + ')'
            return str(integer) + '.' + decimal + ' (' + under_1000(asi, oci, nashti) + ' და ' + _decimal + ')'

    elif len(str(integer)) <= 6:
        under1000 = integer % 1000
        up_to_million = integer / 1000
        if up_to_million < 100:
            if up_to_million == 1:
                up_to_million = ''
            else:
                oci = up_to_million / 20
                nashti = up_to_million % 20
                up_to_million = under_100(oci, nashti)

        else:
            asi = up_to_million / 100
            oci = (up_to_million % 100) / 20
            nashti = (up_to_million % 100) % 20
            up_to_million = under_1000(asi, oci, nashti)

        if under1000 == 0:
            if format_type == 'translate':
                if currency:
                    return str(up_to_million) + ' ათასი' + currency[0] + ' და ' + decimal + ' ' + \
                           currency[1]
                return str(up_to_million) + ' ათასი' + ' და ' + _decimal
            elif format_type == 'number_with_translate':
                if currency:
                    return intWithCommas(integer) + '.' + decimal + ' ' + currency[0] + ' (' + str(
                        up_to_million) + ' ათასი' + currency[0] + ' და ' + decimal + ' ' + currency[
                               1] + ')'
                return intWithCommas(integer) + '.' + decimal + ' (' + str(
                    up_to_million) + ' ათასი' + ' და ' + _decimal + ')'

        else:
            if under1000 < 100:
                oci = under1000 / 20
                nashti = under1000 % 20
                under1000 = under_100(oci, nashti)
            else:
                asi = under1000 / 100
                oci = (under1000 % 100) / 20
                nashti = (under1000 % 100) % 20
                under1000 = under_1000(asi, oci, nashti)
            if format_type == 'translate':
                if currency:
                    return str(up_to_million) + ' ათას ' + under1000 + ' ' + currency[0] + ' და ' + decimal + ' ' + \
                           currency[1]
                return str(up_to_million) + ' ათას ' + under1000 + ' და ' + _decimal
            elif format_type == 'number_with_translate':
                if currency:
                    return intWithCommas(integer) + '.' + decimal + ' ' + currency[0] + ' (' + str(
                        up_to_million) + ' ათას ' + under1000 + ' ' + currency[0] + ' და ' + decimal + ' ' + currency[
                               1] + ')'
                return intWithCommas(integer) + '.' + decimal + ' (' + str(
                    up_to_million) + ' ათას ' + under1000 + ' და ' + _decimal + ')'
