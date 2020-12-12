class Sieunhan:
	#suc_manh = 70
	so_thu_tu = 1
	#stt = 1
	
	def __init__(self,para_ten, para_vu_khi, para_mau_sac, suc_manh):
		self.ten =  para_ten
		self.vukhi = para_vu_khi
		self.mau_sac =  para_mau_sac
		self.suc_manh =suc_manh
		
		self.stt = Sieunhan.so_thu_tu 
		Sieunhan.so_thu_tu += 1
		
		

	def xin_chao(self):
		return "xin chào, ta chính là "+ self.ten

				

Sieunhan_A=Sieunhan("Thy", "Gươm", "Đỏ",90)
print("Ta là siêu nhân: ", Sieunhan_A.ten)
print(Sieunhan_A.xin_chao())
#print("Số thứ tự của ta là: ",Sieunhan_A.stt ,"\n") 
print("Sức mạnh của ta là: ", Sieunhan_A.suc_manh, "\n", "\n")

Sieunhan_B=Sieunhan("Đoàn", "Giáo", "xanh",70)
print("Ta là siêu nhân: ", Sieunhan_B.ten)
print(Sieunhan_B.xin_chao())
#print("Số thứ tự của ta là: ",Sieunhan_B.stt)
#print(Sieunhan.so_thu_tu)
print("Sức mạnh của ta là: ", Sieunhan_B.suc_manh , "\n", "\n")

#----------
'''
print("Vũ khí của siêu nhân là: ", Sieunhan_A.vukhi)
print("Màu sác của siêu nhân là: ", Sieunhan_A.mau_sac)

print(Sieunhan.xin_chao(Sieunhan_A))
print("Sức mạnh của ta là " ,Sieunhan_A.suc_manh)
#### ------------------------------
print("-----------------")
Sieunhan.suc_manh =80
print("Sức mạnh siêu nhân chung là",Sieunhan.suc_manh)
print("Sức mạnh siêu nhân A là",Sieunhan_A.suc_manh)
'''
		