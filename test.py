
def byte_string_similarity(str1: bytes, str2: bytes) -> float:
	"""
	Функция расчета коэффициента равенства двух байтовых строк.

	:param str1: Первая байтовая строка.
	:param str2: Вторая байтовая строка.
	:return: Коэффициент равенства двух байтовых строк.
	"""
	if len(str1) != len(str2):
		return 0.0

	match_count = sum(1 for b1, b2 in zip(str1, str2) if b1 == b2)
	similarity = match_count / len(str1)
	return similarity

print(byte_string_similarity(b'\x01\x01\x01\x01\x01\x01', b'\x01\x01\x01\x01\x01\x01'))