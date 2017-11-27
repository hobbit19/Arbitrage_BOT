import decimal

'''
부동소수점을 사토시로 변환
'''
def toSatoshi(number):
    return round(decimal.Decimal(number),8)