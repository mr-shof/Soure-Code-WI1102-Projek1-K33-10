# Program Monitoring Longsor Lereng
# Menentukan status Ordinary / Pre-alarm / Alarm berdasarkan
# sudut lereng, pergerakan tanah, dan curah hujan.

# KAMUS
# K    : float, sudut kemiringan lereng (derajat)
# G    : array of float, pergerakan tanah (mm/hari)
# H    : array of float, curah hujan harian (mm)
# H3   : array of float, curah hujan kumulatif 3 hari (mm)
# SR   : array of string, status mentah hari itu (sebelum ditahan)
# S    : array of string, status akhir (sudah mempertimbangkan hari sebelumnya)
# n    : int, jumlah hari yang sudah terisi
# maks : int, kapasitas array (hari)


# SUBPROGRAM VALIDASI INPUT

def validasi_angka(teks):
  while True:
    try:
      x = float(input(teks))
      if x >= 0:
        return x
      else:
        print("Nilai tidak boleh negatif. Ulangi.")
    except ValueError:
      print("Nilai tidak boleh teks. Ulangi.")

def validasi_sudut():
  while True:
    try:
      x = float(input("Masukkan sudut kemiringan lereng (0 s.d. 90): "))
      if (x >= 0 and x <= 90):
        return x
      else:
        print("Nilai tidak sesuai. Ulangi.")
    except ValueError:
      print("Nilai tidak boleh teks. Ulangi.")

def validasi_banyak(sisa):
  while True:
    try:
      b = int(input("Banyak hari yang diinput (1 s.d. " + str(sisa) + "): "))
      if (b >= 1 and b <= sisa):
        return b
      else:
        print("Banyak hari tidak valid. Ulangi.")
    except ValueError:
      print("Masukkan bilangan bulat. Ulangi.")


# SUBPROGRAM ANALISIS

def tren_tanah(G, i):
  if (i < 2):
    return "Belum cukup data"
  elif (G[i] > G[i-1] and G[i-1] > G[i-2]):
    return "Naik"
  elif (G[i] < G[i-1] and G[i-1] < G[i-2]):
    return "Turun"
  else:
    return "Stabil/Fluktuatif"

def level_gerak(K, g):
  if (K < 30):
    b_waspada = 10
    b_siaga = 20
    b_bahaya = 30
  elif (K <= 45):
    b_waspada = 7.5
    b_siaga = 17.5
    b_bahaya = 27.5
  else:  # K > 45
    b_waspada = 5
    b_siaga = 15
    b_bahaya = 25

  if (g >= b_bahaya):
    return "Bahaya"
  elif (g >= b_siaga):
    return "Siaga"
  elif (g >= b_waspada):
    return "Waspada"
  else:
    return "Aman"

def hujan_3hari(H, i):
  if (i >= 2):
    awal = i - 2
  else:
    awal = 0
  total = 0
  for j in range(awal, i + 1):
    total = total + H[j]
  return total

def status_hujan(harian, kumulatif):
  if (harian >= 61 and kumulatif >= 91):
    return "Bahaya"
  elif (harian >= 61 or kumulatif >= 91):
    return "Siaga"
  else:
    return "Aman"

def status_akhir(lg, sh):
  # lg: level gerak (Aman/Waspada/Siaga/Bahaya)
  # sh: status hujan (Aman/Siaga/Bahaya)
  if (lg == "Bahaya" or sh == "Bahaya" or (lg == "Siaga" and sh == "Siaga")):
    return "Alarm"
  elif (lg == "Waspada" or lg == "Siaga" or sh == "Siaga"):
    return "Pre-alarm"
  else:
    return "Ordinary"

def tahan_status(SR, i, status_baru):
  # Status tak boleh langsung turun ke Ordinary setelah ada peringatan.
  # Ordinary baru diberikan jika 2 hari sebelumnya juga Ordinary.
  if (status_baru == "Ordinary"):
    if (i >= 1 and SR[i-1] != "Ordinary"):
      return "Pre-alarm"
    elif (i >= 2 and SR[i-2] != "Ordinary"):
      return "Pre-alarm"
  return status_baru

def rekomendasi(status):
  if (status == "Alarm"):
    return "Segera lakukan EVAKUASI dan berkoordinasi dengan petugas terkait."
  elif (status == "Pre-alarm"):
    return "Tingkatkan pengamatan, segera jalankan sistem peringatan dini, serta bangun kesiapsiagaan warga."
  else:
    return "Lakukan pemantauan secara rutin."

def proses_hari(K, G, H, H3, SR, S, i):
  H3[i] = hujan_3hari(H, i)
  sh = status_hujan(H[i], H3[i])
  lg = level_gerak(K, G[i])
  SR[i] = status_akhir(lg, sh)
  S[i] = tahan_status(SR, i, SR[i])
  return

# SUBPROGRAM OUTPUT

def cetak_hasil(K, G, H, H3, SR, S, i):
  print("")
  print("============== HASIL ANALISIS HARI " + str(i + 1) + " ================")
  print("Sudut kemiringan lereng: " + str(K) +"°")
  print("Tren pergerakan tanah  : " + tren_tanah(G, i))
  print("Level pergerakan tanah : " + level_gerak(K, G[i]) + " (" + str(G[i]) + " mm/hari)")
  print("Curah hujan harian     : " + str(H[i]) + " mm")
  print("Curah hujan 3 harian   : " + str(H3[i]) + " mm → " + status_hujan(H[i], H3[i]))
  print("STATUS AKHIR           : " + S[i])
  if (S[i] != SR[i]):
    print("Catatan                : status ditahan, 2 hari terakhir belum seluruhnya Ordinary")
  print("Rekomendasi            : " + rekomendasi(S[i]))
  print("=====================================================")
  print("")
  return

def cetak_riwayat(K, G, H, H3, SR, S, n):
  if (n == 0):
    print("Belum ada data")
    return
  print("")
  print("Sudut lereng: " + str(K) + " derajat")
  print("==================================================================")
  print("Hari | Gerak |  Level  | Hujan | Hujan3h | StatusH | STATUS AKHIR")
  for i in range(0, n):
    print(f"{str(i+1):<4} | {str(G[i]):^5} | {level_gerak(K, G[i]):^7} | {str(H[i]):^5} | {str(H3[i]):^7} | {status_hujan(H[i], H3[i]):^7} | {S[i]:<10}")
  print("==================================================================")
  print("")
  return


# PROGRAM UTAMA

maks = 30
K = -1
G = [0.0 for i in range(maks)]
H = [0.0 for i in range(maks)]
H3 = [0.0 for i in range(maks)]
SR = ["" for i in range(maks)]
S = ["" for i in range(maks)]
n = 0
opsi = ""

while (opsi != "5"):
  print("===== MONITORING LONGSOR LERENG =====")
  print("1. Input data satu hari")
  print("2. Input data beberapa hari sekaligus (array)")
  print("3. Lihat riwayat")
  print("4. Hapus semua riwayat")
  print("5. Keluar")
  opsi = input("Opsi: ")

  if (opsi == "1"):
    if (n >= maks):
      print("Penyimpanan penuh (" + str(maks) + " hari). Hapus riwayat terlebih dahulu.")
    else:
      if (K == -1):
        K = validasi_sudut()
      G[n] = validasi_angka("Pergerakan hari ke-" + str(n+1) + " (mm/hari): ")
      H[n] = validasi_angka("Curah hujan hari ke-" + str(n+1) + " (mm): ")
      proses_hari(K, G, H, H3, SR, S, n)
      cetak_hasil(K, G, H, H3, SR, S, n)
      n = n + 1

  elif (opsi == "2"):
    sisa = maks - n
    if (sisa == 0):
      print("Penyimpanan penuh (" + str(maks) + " hari). Hapus riwayat terlebih dahulu.")
    else:
      if (K == -1):
        K = validasi_sudut()
      banyak = validasi_banyak(sisa)
      awal = n
      for i in range(awal, awal + banyak):
        G[i] = validasi_angka("Pergerakan hari ke-" + str(i+1) + " (mm/hari): ")
      for i in range(awal, awal + banyak):
        H[i] = validasi_angka("Curah hujan hari ke-" + str(i+1) + " (mm): ")
      for i in range(awal, awal + banyak):
        proses_hari(K, G, H, H3, SR, S, i)
      n = n + banyak
      cetak_riwayat(K, G, H, H3, SR, S, n)

  elif (opsi == "3"):
    cetak_riwayat(K, G, H, H3, SR, S, n)

  elif (opsi == "4"):
    n = 0
    K = -1
    print("Riwayat dihapus.")

  elif (opsi == "5"):
    print("Terima kasih.")

  else:
    print("Opsi tidak tersedia.")