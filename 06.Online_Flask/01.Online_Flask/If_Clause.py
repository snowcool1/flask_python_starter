a = 9
b = 1
c = 8

if a>b>c:
	print((a), 'là số lớn nhất')
elif a>c>b:
	print((a), 'là số lớn nhất')
elif a>b==c:
	print((a), 'là số lớn nhất')
elif b>a>c:
	print((b), 'là số lớn nhất')
elif b>c>a:
	print((b), 'là số lớn nhất')
elif b>a==c:
	print((a), 'là số lớn nhất')
elif b==c>a:
	print((b), 'là số lớn nhất')
elif c>a>b:
	print((c), 'là số lớn nhất')
elif c>b>a:
	print((c), 'là số lớn nhất')
else:
	print('Ba số bằng nhau')
