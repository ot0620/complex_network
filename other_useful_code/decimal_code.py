from decimal import Decimal

w_list = [0.00, 0.50, 0.70, 0.90, 0.95, 0.98]
w_list = [Decimal(str(item)).quantize(Decimal('0.00')) for item in w_list]