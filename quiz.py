from datetime import datetime

# =========================
# KELAS NASABAH
# =========================
class Nasabah:
    def __init__(self, id_nasabah, nama, alamat, no_hp):
        self.id_nasabah = id_nasabah
        self.nama = nama
        self.alamat = alamat
        self.no_hp = no_hp

    def __str__(self):
        return f"{self.id_nasabah} - {self.nama}"


# =========================
# KELAS REKENING
# =========================
class Rekening:
    def __init__(self, no_rekening, nasabah, saldo_awal=0):
        self.no_rekening = no_rekening
        self.nasabah = nasabah
        self.__saldo = saldo_awal
        self.riwayat = []

        self._jumlah_setor_harian = 0
        self._tanggal_setor = None

    def cek_saldo(self):
        return self.__saldo

    def setor_tunai(self, jumlah):
        if jumlah <= 0:
            raise ValueError("Jumlah setor harus lebih dari 0")

        today = datetime.now().date()

        if self._tanggal_setor != today:
            self._jumlah_setor_harian = 0
            self._tanggal_setor = today

        if self._jumlah_setor_harian >= 3:
            raise Exception("Limit setor harian (3x) tercapai")

        self.__saldo += jumlah
        self._jumlah_setor_harian += 1
        self.riwayat.append((datetime.now(), f"Setor {jumlah}"))

    def tarik_tunai(self, jumlah):
        if jumlah <= 0:
            raise ValueError("Jumlah tarik harus lebih dari 0")
        if jumlah > self.__saldo:
            raise Exception("Saldo tidak cukup")

        self.__saldo -= jumlah
        self.riwayat.append((datetime.now(), f"Tarik {jumlah}"))

    def transfer(self, tujuan, jumlah):
        if tujuan is None:
            raise Exception("Rekening tujuan tidak ditemukan")
        if self.no_rekening == tujuan.no_rekening:
            raise ValueError("Tidak bisa transfer ke rekening sendiri")

        self.tarik_tunai(jumlah)
        tujuan.setor_tunai(jumlah)
        self.riwayat.append((datetime.now(), f"Transfer ke {tujuan.no_rekening} {jumlah}"))

    def cetak_riwayat(self):
        if not self.riwayat:
            print("Belum ada transaksi.")
        else:
            for waktu, keterangan in self.riwayat:
                print(f"{waktu} - {keterangan}")

    def __str__(self):
        return f"No Rekening: {self.no_rekening} | Nama: {self.nasabah.nama} | Saldo: {self.__saldo}"


# =========================
# KELAS BANK
# =========================
class Bank:
    def __init__(self, nama_bank):
        self.nama_bank = nama_bank
        self.daftar_nasabah = {}
        self.daftar_rekening = {}

    def tambah_nasabah_dan_rekening(self, id_nasabah, nama, alamat, no_hp, no_rekening, saldo_awal):
        if id_nasabah in self.daftar_nasabah:
            raise Exception("Nasabah sudah ada")

        if no_rekening in self.daftar_rekening:
            raise Exception("No rekening sudah ada")

        nasabah = Nasabah(id_nasabah, nama, alamat, no_hp)
        rekening = Rekening(no_rekening, nasabah, saldo_awal)

        self.daftar_nasabah[id_nasabah] = nasabah
        self.daftar_rekening[no_rekening] = rekening

    def cari_rekening(self, no_rekening):
        return self.daftar_rekening.get(no_rekening)

    def tampilkan_semua_rekening(self):
        for r in self.daftar_rekening.values():
            print(r)


# =========================
# MENU
# =========================
def menu():
    bank = Bank("Bank Python")

    while True:
        print("\n=== MENU BANK ===")
        print("1. Tambah Nasabah + Rekening")
        print("2. Setor Tunai")
        print("3. Tarik Tunai")
        print("4. Transfer")
        print("5. Cek Saldo")
        print("6. Riwayat Transaksi")
        print("7. Tampilkan Semua Rekening")
        print("0. Keluar")

        pilih = input("Pilih menu: ")

        try:
            if pilih == "1":
                id_n = input("ID Nasabah: ")
                nama = input("Nama: ")
                alamat = input("Alamat: ")
                hp = input("No HP: ")
                no_rek = input("No Rekening: ")
                saldo = float(input("Saldo awal: "))

                bank.tambah_nasabah_dan_rekening(id_n, nama, alamat, hp, no_rek, saldo)
                print("Nasabah & rekening berhasil dibuat")

            elif pilih == "2":
                no_rek = input("No Rekening: ")
                jumlah = float(input("Jumlah setor: "))
                rek = bank.cari_rekening(no_rek)

                if rek:
                    rek.setor_tunai(jumlah)
                    print("Setor berhasil")
                else:
                    print("Rekening tidak ditemukan")

            elif pilih == "3":
                no_rek = input("No Rekening: ")
                jumlah = float(input("Jumlah tarik: "))
                rek = bank.cari_rekening(no_rek)

                if rek:
                    rek.tarik_tunai(jumlah)
                    print("Tarik berhasil")
                else:
                    print("Rekening tidak ditemukan")

            elif pilih == "4":
                asal = input("Rekening asal: ")
                tujuan = input("Rekening tujuan: ")
                jumlah = float(input("Jumlah transfer: "))

                rek_asal = bank.cari_rekening(asal)
                rek_tujuan = bank.cari_rekening(tujuan)

                if rek_asal and rek_tujuan:
                    rek_asal.transfer(rek_tujuan, jumlah)
                    print("Transfer berhasil")
                else:
                    print("Rekening tidak ditemukan")

            elif pilih == "5":
                no_rek = input("No Rekening: ")
                rek = bank.cari_rekening(no_rek)

                if rek:
                    print("Saldo:", rek.cek_saldo())
                else:
                    print("Rekening tidak ditemukan")

            elif pilih == "6":
                no_rek = input("No Rekening: ")
                rek = bank.cari_rekening(no_rek)

                if rek:
                    rek.cetak_riwayat()
                else:
                    print("Rekening tidak ditemukan")

            elif pilih == "7":
                bank.tampilkan_semua_rekening()

            elif pilih == "0":
                print("Terima kasih")
                break

            else:
                print("Menu tidak valid")

        except Exception as e:
            print("Error:", e)


if __name__ == "__main__":
    menu()