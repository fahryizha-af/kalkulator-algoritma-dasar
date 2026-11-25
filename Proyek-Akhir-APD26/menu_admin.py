import os
from data import jenisAlat, data_alat, data_penjualan, bersih, hitung_total_stok, cari_alat_by_jenis, validasi_angka
from tampilan import tampilkan_detail_alat, tampilkan_jenis_alat, tampilkan_pilihan_alat_admin,tampilkan_data_alat_lengkap, tampilkan_data_penjualan

def cek_batal(teks):
    return teks.strip().lower() == "batal"

def batal_kembali():
    print("\nDibatalkan. Kembali ke menu admin.\n")
    input("Tekan Enter untuk kembali ke menu...")

def jalankan_menu_admin():
    while True:
        os.system(bersih)
        print("""MENU ADMIN
1. Tambah alat baru
2. Tampilkan data alat
3. Ubah data alat
4. Hapus data alat
5. Lihat data penjualan
6. Logout
""")
        pilih = input("Pilih menu (1-6) : ").strip()

        if pilih == "1":
            os.system(bersih)
            print("TAMBAH ALAT BARU\n")
            print("(Ketik 'batal' kapan saja untuk kembali ke menu admin)\n")
            print("Jenis alat yang tersedia:")
            jenis_keys = list(jenisAlat.keys())
            tampilkan_jenis_alat()
            nomorJenisBaru = len(jenisAlat) + 1
            print(f"{nomorJenisBaru}. Tambah jenis alat baru")

            pilihJenis = input(f"\nPilih nomor jenis alat (1-{nomorJenisBaru}) : ").strip()
            if cek_batal(pilihJenis):
                batal_kembali()
                continue
            try:
                pilihJenis = validasi_angka(pilihJenis, 1, nomorJenisBaru)
            except ValueError as e:
                print(f"\nNomor jenis tidak valid, {e}\n")
                input("Tekan Enter untuk kembali ke menu...")
                continue

            jenisBaru = False
            if pilihJenis == nomorJenisBaru:
                jenisBaru = True
                namaJenis = input("\nNama jenis baru : ").strip()
                if cek_batal(namaJenis):
                    batal_kembali()
                    continue
                if namaJenis == "":
                    print("\nNama jenis tidak boleh kosong.\n")
                    input("Tekan Enter untuk kembali ke menu...")
                    continue
                jenis_sudah_ada = False
                for j_name in jenisAlat:
                    if j_name.lower() == namaJenis.lower():
                        jenis_sudah_ada = True
                if jenis_sudah_ada:
                    print(f"\nJenis '{namaJenis}' sudah ada. Pilih dari daftar jenis.\n")
                    input("Tekan Enter untuk kembali ke menu...")
                    continue

                modalInput = input("Modal per unit (Rp) : ").strip()
                if cek_batal(modalInput):
                    batal_kembali()
                    continue
                try:
                    modal = validasi_angka(modalInput, 1, None)
                except ValueError as e:
                    print(f"\nModal tidak valid, {e}\n")
                    input("Tekan Enter untuk kembali ke menu...")
                    continue

                hargaInput = input("Harga jual per unit (Rp) : ").strip()
                if cek_batal(hargaInput):
                    batal_kembali()
                    continue
                try:
                    harga = validasi_angka(hargaInput, 1, None)
                except ValueError as e:
                    print(f"\nHarga tidak valid, {e}\n")
                    input("Tekan Enter untuk kembali ke menu...")
                    continue
                if harga < modal:
                    print("\nHarga jual tidak boleh lebih kecil dari modal.\n")
                    input("Tekan Enter untuk kembali ke menu...")
                    continue
            else:
                namaJenis = jenis_keys[pilihJenis - 1]
                modal = jenisAlat[namaJenis]["modal"]
                harga = jenisAlat[namaJenis]["harga"]

            namaBaru = input("Nama alat baru : ").strip()
            if cek_batal(namaBaru):
                batal_kembali()
                continue
            if namaBaru == "":
                print("\nNama alat tidak boleh kosong.\n")
                input("Tekan Enter untuk kembali ke menu...")
                continue
            if namaBaru in data_alat:
                print(f"\nAlat dengan nama '{namaBaru}' sudah ada. Gunakan nama lain.\n")
                input("Tekan Enter untuk kembali ke menu...")
                continue

            stokAwal = input("Stok awal dalam unit (minimal 0) : ").strip()
            if cek_batal(stokAwal):
                batal_kembali()
                continue
            try:
                stokAwal = validasi_angka(stokAwal, 0, None)
            except ValueError as e:
                print(f"\nStok tidak valid, {e}\n")
                input("Tekan Enter untuk kembali ke menu...")
                continue

            if jenisBaru:
                jenisAlat[namaJenis] = {"modal": modal, "harga": harga}
                print(f"\nJenis baru '{namaJenis}' berhasil ditambahkan.")

            laba = harga - modal
            data_alat[namaBaru] = {
                "jenis": namaJenis,
                "modal": modal,
                "harga": harga,
                "laba": laba,
                "stok": stokAwal
            }
            print("\nAlat baru berhasil ditambahkan:")
            tampilkan_detail_alat(namaBaru, data_alat[namaBaru])
            input("Tekan Enter untuk kembali ke menu...")

        elif pilih == "2":
            os.system(bersih)
            print("DATA ALAT TERDAFTAR")
            if len(data_alat) == 0:
                print("\nBelum ada data alat.\n")
            else:
                print("")
                potensiLaba = tampilkan_data_alat_lengkap()
                print(f"\nTotal jenis alat : {len(data_alat)}")
                print(f"Total stok       : {hitung_total_stok()} unit")
                print(f"Potensi laba     : Rp{potensiLaba} (jika semua stok terjual)\n")
            input("Tekan Enter untuk kembali ke menu...")

        elif pilih == "3":
            os.system(bersih)
            print("UBAH DATA ALAT\n")
            if len(data_alat) == 0:
                print("Belum ada data alat untuk diubah.\n")
                input("Tekan Enter untuk kembali ke menu...")
                continue

            print("(Ketik 'batal' kapan saja untuk kembali ke menu admin)\n")
            alat_keys = list(data_alat.keys())
            tampilkan_pilihan_alat_admin()

            ubah = input(f"\nPilih nomor alat yang ingin diubah (1-{len(data_alat)}) : ").strip()
            if cek_batal(ubah):
                batal_kembali()
                continue
            try:
                ubah = validasi_angka(ubah, 1, len(data_alat))
            except ValueError as e:
                print(f"\nNomor tidak valid, {e}\n")
            else:
                nama_lama = alat_keys[ubah - 1]
                info = data_alat[nama_lama]
                print("\nData saat ini:")
                tampilkan_detail_alat(nama_lama, info)

                ubahNama = input("Nama baru (kosongkan jika tidak diubah) : ").strip()
                if cek_batal(ubahNama):
                    batal_kembali()
                    continue
                if ubahNama != "" and ubahNama != nama_lama and ubahNama in data_alat:
                    print(f"\nAlat dengan nama '{ubahNama}' sudah ada. Gunakan nama lain.\n")
                    input("Tekan Enter untuk kembali ke menu...")
                    continue
                ubahJenis = input(f"Jenis baru - {'/'.join(jenisAlat.keys())} (kosongkan jika tidak diubah) : ").strip()
                if cek_batal(ubahJenis):
                    batal_kembali()
                    continue
                ubahStok = input("Stok baru dalam unit (kosongkan jika tidak diubah) : ").strip()
                if cek_batal(ubahStok):
                    batal_kembali()
                    continue

                ada_perubahan = False

                if ubahNama:
                    if ubahNama != nama_lama:
                        data_alat[ubahNama] = data_alat.pop(nama_lama)
                        nama_lama = ubahNama
                    ada_perubahan = True

                if ubahJenis:
                    found = False
                    for j_name, j_val in jenisAlat.items():
                        if j_name.lower() == ubahJenis.lower():
                            data_alat[nama_lama]["jenis"] = j_name
                            data_alat[nama_lama]["modal"] = j_val["modal"]
                            data_alat[nama_lama]["harga"] = j_val["harga"]
                            data_alat[nama_lama]["laba"] = j_val["harga"] - j_val["modal"]
                            found = True
                            ada_perubahan = True
                            break
                    if not found:
                        print(f"\nJenis '{ubahJenis}' tidak dikenali, jenis tidak diubah.")

                if ubahStok != "":
                    try:
                        stokBaru = validasi_angka(ubahStok, 0, None)
                    except ValueError:
                        print("\nStok harus berupa angka bulat (0 atau lebih), stok tidak diubah.")
                    else:
                        data_alat[nama_lama]["stok"] = stokBaru
                        ada_perubahan = True

                if ada_perubahan:
                    print("\nData setelah diubah:")
                    tampilkan_detail_alat(nama_lama, data_alat[nama_lama])
                else:
                    print("\nTidak ada data yang diubah.\n")
            input("Tekan Enter untuk kembali ke menu...")

        elif pilih == "4":
            os.system(bersih)
            print("HAPUS DATA ALAT\n")
            if len(data_alat) == 0:
                print("Belum ada data alat untuk dihapus.\n")
                input("Tekan Enter untuk kembali ke menu...")
                continue

            print("(Ketik 'batal' kapan saja untuk kembali ke menu admin)\n")
            alat_keys = list(data_alat.keys())
            tampilkan_pilihan_alat_admin()

            hapus = input(f"\nPilih nomor alat yang ingin dihapus (1-{len(data_alat)}) : ").strip()
            if cek_batal(hapus):
                batal_kembali()
                continue
            try:
                hapus = validasi_angka(hapus, 1, len(data_alat))
            except ValueError as e:
                print(f"\nNomor tidak valid, {e}\n")
            else:
                nama_dihapus = alat_keys[hapus - 1]
                info_dihapus = data_alat.pop(nama_dihapus)
                print(f"\nData '{nama_dihapus}' (jenis {info_dihapus['jenis']}, stok {info_dihapus['stok']} unit) sudah dihapus.\n")
            input("Tekan Enter untuk kembali ke menu...")

        elif pilih == "5":
            os.system(bersih)
            print("DATA PENJUALAN")
            if len(data_penjualan) == 0:
                print("\nBelum ada transaksi penjualan.\n")
            else:
                print("")
                totalTerjual, totalPendapatan, totalLabaJual = tampilkan_data_penjualan()
                print(f"\nTotal transaksi    : {len(data_penjualan)}")
                print(f"Total alat terjual : {totalTerjual} unit")
                print(f"Total pendapatan   : Rp{totalPendapatan}")
                print(f"Total laba         : Rp{totalLabaJual}\n")
            input("Tekan Enter untuk kembali ke menu...")

        elif pilih == "6":
            print("\nLogout berhasil.\n")
            input("Tekan Enter untuk kembali ke menu utama...")
            return

        else:
            print("\nPilihan tidak valid. Masukkan angka 1-6.\n")
            input("Tekan Enter untuk kembali ke menu...")