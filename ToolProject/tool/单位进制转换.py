def change_unit(num_unit_data: tuple, units: list, scale: int):
    """
    转换单位
    :type num_unit_data:
    :param units:
    :param scale:
    :return:
    """

    last_unit = units.index(num_unit_data[1])

    def change(n: float, unit):
        # 单位变小
        if n < 1 and last_unit != 0:
            unit = max(0, unit - 1)
            n *= scale

        # 单位变大
        elif n >= scale and last_unit != len(units) - 1:
            unit = min(len(units), unit + 1)
            n /= scale

        return '%g%s' % (n, units[unit])

    return change(float(num_unit_data[0]), last_unit)


num_unit_data = (1000, 'PF',)
units = ['PF', 'NF', 'UF', 'MF', 'F']
scale = 1000
print(change_unit(num_unit_data, units, scale))