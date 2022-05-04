########### Ajuste de múltiplas variáveis #################
import matplotlib.pyplot as plt
import numpy as np

dados = open("C:\\Users\\labimas\\Desktop\\Magnet Simulações\\SWLS Sirius\\SWLS Sirius Models\\SWLS_Compilate_Data.csv").readlines()

m = [] #modelo
i0 = [] #corrente
d = [] #distância bobina-polo
r0 = [] #raio do polo
nw0 = [] #número de espiras-largura
bp = [] #campo de pico
hfi = [] #integral alto campo
marg = [] #margem 5 K

for i in range(len(dados)):
	if i != 0:
		linha = dados[i].replace(",", ".").split(";")
		m.append(int(linha[0]))
		i0.append(float(linha[1]))
		d.append(float(linha[2]))
		r0.append(float(linha[3]))
		nw0.append(float(linha[4]))
		bp.append(float(linha[5]))
		hfi.append(float(linha[6]))
		marg.append(float(linha[7]))

par = [i0, d, r0, nw0] #conjunto variáveis independentes
par_t = np.transpose(par)
par_t1 = np.c_[par_t, np.ones(par_t.shape[0])]
bp_coef = np.linalg.lstsq(par_t1, bp, rcond=None)[0] #coeficientes ajuste campo de pico
hfi_coef = np.linalg.lstsq(par_t1, hfi, rcond=None)[0] #coeficientes ajuste campo integrado
marg_coef = np.linalg.lstsq(par_t1, marg, rcond=None)[0] #coeficientes ajuste Margem

'''
print(bp_coef)
print(hfi_coef)
print(marg_coef)
print(bp_coef[0]*i0[0]+bp_coef[1]*d[0]+bp_coef[2]*r0[0]+bp_coef[3]*nw0[0]+bp_coef[4])
print(hfi_coef[0]*i0[0]+hfi_coef[1]*d[0]+hfi_coef[2]*r0[0]+hfi_coef[3]*nw0[0]+hfi_coef[4])
print(marg_coef[0]*i0[0]+marg_coef[1]*d[0]+marg_coef[2]*r0[0]+marg_coef[3]*nw0[0]+marg_coef[4])
'''


########################## Otimização Nelder-Mead ################################
import random as rd

# Resultados desejados
id_bp = 7.0
id_hfi = 20.0
id_marg = 25.0

# Constantes de minimização
a_bp = 1.0
a_hfi = 1.0
a_marg = 1.0
n_bp = 2.0 
n_hfi = 2.0 
n_marg = 2.0 

def f_bp_hfi_marg(bp_, hfi_, marg_):
	valor = ((1-(bp_/id_bp))**n_bp)*a_bp + ((1-(hfi_/id_hfi))**n_hfi)*a_hfi + ((1-(marg_/id_marg))**n_marg)*a_marg
	return valor

# Parâmetros da otimização Nelder-Mead
alpha = 1.0 #Reflexão
gamma = 2.0 #Expansão
rho = 0.5 #Contração
sigma = 0.5 #Retração

# Chute inicial de Parâmetros de entrada
i0_ = []
d_ = []
r0_ = []
nw0_ = []
for i in range(5):
	i0_.append(round(rd.uniform(180,300)))
	d_.append(round(rd.uniform(1,5), 2))
	r0_.append(round(rd.uniform(2,10), 2))
	nw0_.append(round(rd.uniform(10,30)))
par_ = [i0_, d_, r0_, nw0_]

######## Simplex
def simplex(par_):
	p = len(par_)
	i0_ = par_[0]
	d_ = par_[1]
	r0_ = par_[2]
	nw0_ = par_[3]
	spx = []
	rst = []
	f_rst = []

	for i in range(p+1):
		bp_ = bp_coef[0]*i0_[i]+bp_coef[1]*d_[i]+bp_coef[2]*r0_[i]+bp_coef[3]*nw0_[i]+bp_coef[4]
		hfi_ = hfi_coef[0]*i0_[i]+hfi_coef[1]*d_[i]+hfi_coef[2]*r0_[i]+hfi_coef[3]*nw0_[i]+hfi_coef[4]
		marg_ = marg_coef[0]*i0_[i]+marg_coef[1]*d_[i]+marg_coef[2]*r0_[i]+marg_coef[3]*nw0_[i]+marg_coef[4]
		valor = f_bp_hfi_marg(bp_, hfi_, marg_)

		spx.append([i0_[i], d_[i], r0_[i], nw0_[i]])
		rst.append([round(bp_, 3), round(hfi_, 2), round(marg_, 2)])
		f_rst.append(valor)
	return spx, rst, f_rst

spx, rst, f_rst = simplex(par_)

#print(spx)
print(f_rst)
#print(sorted(f_rst)[0], sorted(f_rst)[-2], sorted(f_rst)[-1]) #mínimo, segundo máximo e máximo

#### Ordenação
def ordern(spx, f_rst):
	p = len(f_rst)
	f_rst_ord = sorted(f_rst)
	spx_med = []
	spx_min = []
	spx_max = []
	spx_max2 = []

	for i in range(p):
		#Mínimo
		if f_rst[i] == f_rst_ord[0]:
			spx_min = spx[i]
			#print("Mínimo", spx_min, f_rst[i])
		#Máximo
		if f_rst[i] == f_rst_ord[p-1]:
			spx_max = spx[i]
			#print("Máximo", spx_max, f_rst[i])
		#Segundo Máximo
		if f_rst[i] == f_rst_ord[p-2]:
			spx_max2 = spx[i]
			#print("2° Máximo", spx_max2, f_rst[i])

	return spx_min, spx_max, spx_max2


def centroide(spx, f_rst, spx_max):
	p = len(f_rst)
	spx_cent = []
	spx_med = []
	for k in range(p):
		if f_rst[k] != max(f_rst):
			spx_cent.append(spx[k])
	#Centroide
	pi = len(spx_cent)
	for j in range(pi):
		spx_sum = 0
		for i in range(pi):
			spx_sum += spx_cent[i][j]
		spx_med.append(spx_sum/pi)
	return spx_med


#### Reflexão

def reflect(spx_med, spx_max):
	p = len(spx_med)
	spx_rfx = []
	bp_ = bp_coef[4]
	hfi_ = hfi_coef[4]
	marg_ = marg_coef[4]
	for i in range(p):
		spx_rfx.append(spx_med[i] + alpha*(spx_med[i]-spx_max[i]))
		bp_ += bp_coef[i]*spx_rfx[i]
		hfi_ += hfi_coef[i]*spx_rfx[i]
		marg_ += marg_coef[i]*spx_rfx[i]
	f_rst_rfx = f_bp_hfi_marg(bp_, hfi_, marg_)
	return spx_rfx, f_rst_rfx

####Expansão

def expand(spx_med, spx_rfx):
	p = len(spx_med)
	spx_exp = []
	bp_ = bp_coef[4]
	hfi_ = hfi_coef[4]
	marg_ = marg_coef[4]
	for i in range(p):
		spx_exp.append(spx_med[i] + gamma*(spx_rfx[i]-spx_med[i]))
		bp_ += bp_coef[i]*spx_exp[i]
		hfi_ += hfi_coef[i]*spx_exp[i]
		marg_ += marg_coef[i]*spx_exp[i]
	f_rst_exp = f_bp_hfi_marg(bp_, hfi_, marg_)
	return spx_exp, f_rst_exp

####Contração

def contract(spx_med, spx_c):
	p = len(spx_med)
	spx_con = []
	bp_ = bp_coef[4]
	hfi_ = hfi_coef[4]
	marg_ = marg_coef[4]
	for i in range(p):
		spx_con.append(spx_med[i] + rho*(spx_c[i]-spx_med[i]))
		bp_ += bp_coef[i]*spx_con[i]
		hfi_ += hfi_coef[i]*spx_con[i]
		marg_ += marg_coef[i]*spx_con[i]
	f_rst_con = f_bp_hfi_marg(bp_, hfi_, marg_)
	return spx_con, f_rst_con

####Retração

def shrink(spx, spx_min):
	p = len(spx_min)
	spx_sh = []
	f_rst_sh = []
	for j in range(p+1):
		spx_sh.append([])
		bp_ = bp_coef[4]
		hfi_ = hfi_coef[4]
		marg_ = marg_coef[4]
		for i in range(p):
			spx_sh[j].append(spx_min[i] + sigma*(spx[j][i]-spx_min[i]))
			bp_ += bp_coef[i]*spx_sh[j][i]
			hfi_ += hfi_coef[i]*spx_sh[j][i]
			marg_ += marg_coef[i]*spx_sh[j][i]
		valor_sh = f_bp_hfi_marg(bp_, hfi_, marg_)
		f_rst_sh.append(valor_sh)
	return spx_sh, f_rst_sh



######## Mudança do Simplex ###########

for ns in range(40):
	p = len(f_rst)
	spx_temp = spx
	f_rst_temp = f_rst
	f_rst_max = max(f_rst)
	spx_min, spx_max, spx_max2 = ordern(spx, f_rst)
	spx_med = centroide(spx, f_rst, spx_max)
	spx_rfx, f_rst_rfx = reflect(spx_med, spx_max)
	if ((f_rst_rfx >= sorted(f_rst)[0]) and (f_rst_rfx <= sorted(f_rst)[-2])):
		for k in range(p):
			if f_rst[k] == f_rst_max:
				del(spx_temp[k])
				del(f_rst_temp[k])
				print("Refletir")
				spx_temp.append(spx_rfx)
				f_rst.append(f_rst_rfx)
	elif (f_rst_rfx < sorted(f_rst)[0]):
		spx_exp, f_rst_exp = expand(spx_med, spx_rfx)
		for k in range(p):
			if f_rst[k] == f_rst_max:
				del(spx_temp[k])
				del(f_rst_temp[k])
				if f_rst_exp < f_rst_rfx:
					print("Expandir")
					spx_temp.append(spx_exp)
					f_rst.append(f_rst_exp)
				else:
					print("Refletir")
					spx_temp.append(spx_rfx)
					f_rst.append(f_rst_rfx)
	elif ((f_rst_rfx > sorted(f_rst)[-2]) and (f_rst_rfx <= sorted(f_rst)[-1])):
		spx_ocon, f_rst_ocon = contract(spx_med, spx_rfx)
		for k in range(p):
			if f_rst[k] == f_rst_max:
				if f_rst_ocon < f_rst_rfx:
					del(spx_temp[k])
					del(f_rst_temp[k])
					print("Contrair ext.")
					spx_temp.append(spx_ocon)
					f_rst.append(f_rst_ocon)
				else:
					print("Retrair")
					spx_temp, f_rst_temp = shrink(spx, spx_min)
	elif (f_rst_rfx > sorted(f_rst)[-1]):
		spx_icon, f_rst_icon = contract(spx_med, spx_max)
		for k in range(p):
			if f_rst[k] == f_rst_max:
				if f_rst_icon < f_rst_max:
					del(spx_temp[k])
					del(f_rst_temp[k])
					print("Contrair int.")
					spx_temp.append(spx_icon)
					f_rst.append(f_rst_icon)
				else:
					print("Retrair")
					spx_temp, f_rst_temp = shrink(spx, spx_min)

	npar_ = []
	for i in range(len(spx_temp[0])):
		npar_.append([])
		for j in range(len(spx_temp)):
			npar_[i].append(spx_temp[j][i])

	simplex(npar_)
	spx, rst, f_rst = simplex(npar_)

print("Função Auxiliar final: " + str(f_rst))
print("Simplex final: " + str(spx)) #simplex final
print("Resultados finais: " + str(rst)) #resultados finais
