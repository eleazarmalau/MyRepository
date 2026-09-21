# Log bantuan AI — Assignment 3

Tanggal: 21 September 2026. Alat: OpenAI Codex (GPT-6).

## Prompt pengguna

> Berdasarkan link di website tersebut ada beberapa checklist yang harus dilakukan nah tugasnya itu kan sebenernya cuman ngelakuin hal yang sama dengan projects dan juga adain projects_form itu tapi disini kita harus modifikasi untuk bagian education dan experience. Nah tugasnya tuh cuman ngikutin checklistnya dan kerjain apa yang diminta dan yang diminta itu kurang lebih. melakukan hal yang sama untuk bagian projects kan nah sekarang coba bikinin untuk formsnya dan teman-temannya itu. Harus benar semua dan harus bagus

Referensi: [Individual Assignment 3](https://pbp.cs.ui.ac.id/en/assignments/individual/tugas-3.html) dan [Tutorial 03](https://pbp.cs.ui.ac.id/en/tutorial/tutorial-3.html).

## Cakupan bantuan

1. Membaca checklist serta alur Projects yang sudah ada untuk menentukan bagian yang perlu diterapkan ke Education dan Experience.
2. Menambahkan ModelForm dengan semua field yang dapat diedit, validasi periode, dan dukungan logo statis maupun URL.
3. Menambahkan view tambah/edit/hapus/JSON, routing, dan deserialisasi JSON sebelum data dirender ke HTML.
4. Menambahkan `created_at`/`updated_at` beserta migration untuk data yang sudah ada.
5. Menyusun form dan komponen dialog bersama, tombol pada daftar, notifikasi, pencarian, serta penyesuaian CSS untuk mobile dan keyboard.
6. Menulis dan menjalankan pengujian integrasi, Django system check, dan pemeriksaan kesesuaian migration.
7. Menyusun draf jawaban reflektif, petunjuk penggunaan, dan disclosure di README.

## Keputusan yang memerlukan pemeriksaan

- UUID dan timestamp milik model; pengguna tidak mengisinya melalui ModelForm.
- Edit harus mengikat `instance` agar tidak membuat record baru.
- Pengurutan Education lama dan path logo lokal harus tetap berfungsi.
- Form invalid harus mempertahankan input dan menampilkan error; periode invalid tidak boleh tersimpan.
- Hapus hanya melalui POST dengan CSRF; pembatalan dialog tidak mengirim request hapus.
- Test Django memverifikasi perilaku server. Pemeriksaan browser diperlukan untuk interaksi dialog dan layout; kelulusan test saja tidak membuktikan kualitas visual.

Log ini merupakan ringkasan pekerjaan agen dalam sesi ini, bukan klaim peninjauan atau penulisan manual oleh pengguna. Pemilik proyek tetap perlu memahami dan meninjau implementasi serta jawaban reflektif sebelum pengumpulan.
