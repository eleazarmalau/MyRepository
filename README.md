Nama : Isybal Sama Eleazar Malau

NPM : 2506623963

Kelas : PBP A

# Assignment 1
1. Saya sendiri menggunakan element semantik HTML 5 beberapa yang berupa <section>, <header>, <article>, <nav>, <main>, <footer>, dan beberapa lagi yang mungkin saya lupa mention. Elemen-elemen tersebut membantu saya dalam memahami pembagian format web saya agar lebih terstruktur dan mudah dibaca dan dimengerti untuk posisi apa saja hal-hal berada di web saya. Beberapa yang paling utama adalah seperti <section> yang membantu saya membagi-bagi bagian-bagian utama webnya, seperti untuk profile, education, dan experiences. Setelah itu saya juga menggunakan <article> untuk membuat isi dari section tersebut menjadi sebuah "bentuk" card yang mudah untuk dinavigasikan. Setiap section juga ada memiliki id untuk bisa membantu mengimplementasikan navigasi barnya menjadi lebih fungsional

2. Beberapa tantangan yang saya temui selama membuat CSS untuk layoutnya adalah kalau susah untuk mengadjust beberapa kartunya agar sesuai dengan ukuran yang diinginkan, selain itu juga ada beberapa typo dalam index.htmlnya dan juga di style.cssnya yang membuat saya bingung kenapa apa yang saya buat itu tidak masuk. Permasalahan utama yang saya temukan saat buat webnya kebanyakan terletak di pengaturan ukuran dari masing-masing hal yang saya tambahkan sebenarnya. 

Untuk mengevaluasi tampilan agar tetap responsif adalah kalau saya melihat keterbacaan teks, ruangan yang masih tersedia, dan kemungkinan konten itu sendiri bisa keluar dari layar screennya. Pada layar kecil, layout profil diubah dari dua kolom menjadi satu kolom, navbar disusun agar lebih sesuai dengan lebar layar, dan informasi tanggal pada kartu dapat berpindah juga ke bawah judul. Nama, posisi, dan deskripsi menjadi prioritas utama, sementara untuk gambar logo misalkan itu dapat diperkecil dan diadjust agar tidak mengambil terlalu banyak ruang.

3. Keterbatasan utamanya ada dikeharusan untuk masih melakukan pengkodean untuk semua hal secara manual di HTML. Semua perubahan harus dilakukan beserta sebuah deployment ulang dan hal tersebut kadang membuat waktu terbuang walaupun sebenarnya sebentar aja atau yang dimaksud adalah kalau kadang kurang efisien untuk masih mengkodekan semua hal secara manual di HTML. 

Pada iterasi berikutnya saya paling ingin menambahkan fitur untuk pengelolaan data-datanya melalui sebuah database. Dengan adanya hal tersebut, saya bisa menambah atau mengubah posisi, fitur, institusi, periode, logo, dan hal-hal lainnya yang ada di web saya sekarang tanpa mengubah struktur HTMLnya. Pembaruan portofolionya juga akan menjadi lebih praktis kedepannya.

## AI Disclosure:
Model yang digunakan adalah Chat GPT-6 Astra Medium

1. Cakupan Penggunaan dan Prompting

Prompt Strategy: Saya menggunakan AI untuk membuat sebuah framework pemahaman untuk apa saja yang akan ditambahkan di website serta memahaminya juga dalam bentuk HTML dan CSS. Selain itu, juga menyelesaikan beberapa permasalahan deployment.

Perencanaan Pengembangan Portofolio:
    Prompt: "Now your job is just to give me a framework to work on and also give some ideas on the css or template design."
    Tujuan: Memahami apa saja pengembangan yang harus ditambahkan untuk website portfolionya dan mencari ide-ide baru yang bisa mengembangkan webnya.

Framework Code:
    Prompt: "Now show me the code framework so that I can implement it myself"
    Tujuan: Membantu mencari element-element HTML apa yang cocok untuk pengimplementasian yang dibutuhkan untuk membuat web sesuai dengan framework baru yang tadi udah di brainstorm bersama

Diagnosis CSS dan Permasalahannya:
    Prompt: "There's a couple of problems in my CSS like my stuff isn't aligning and there are cards filling up the whole window. Where am I wrong in my code? Help me find the problem."
    Tujuan: Saat ada permasalahan CSS, meminta bantuan AI untuk mereview kodenya dan mencari masalahnya agar bisa diselesaikan secara manual

Git dan Deployment ke PWS:
    Prompt: "Why am I still showing a disallowed hosts screen?"
    Tujuan: Mencari solusi dari masalah saya mengenai tidak munculnya web dalam PWS dan ternyata ada permasalahan di bagian Allowed Hostsnya dimana saya lupa menambahkan webnya
    Prompt: "How do I do a push to my repository right now?"
    Tujuan: Mencari solusi untuk bisa melakukan push yang benar ke repo

2. Pengkritisan Terhadap AI
    Terdapat beberapa kondisi dimana AI memberikan sebuah framework atau design yang tidak sesuai dengan keinginan saya seperti menambahkan border untuk logo yang kemudian saya hilangkan saja karena tidak sesuai dengan tampilan yang saya inginkan. Terdapat juga beberapa panduan untuk penggunaan warna yang saya ubah sesuai dengan keinginan saya. 


# Assignment 2
1. Ketika pengguna membuka halaman portofolio baru misalkan education, browser akan mengirimkan HTTP request ke Django. Request tersebut akan dicocokan melalui urls.py yang ada di dalam folder Portfolio di mana di dalam file tersebut ada command include("main.urls) yang akan melanjutkan proses requestnya ke main/urls.py

Di dalam urls.py dalam main ini akan ada alamat education yang akan membawa lagi ke view show_education yang sudah dibuat. View tersebut akan mengambil data pendidikan dari database dengan model Education yang sudah dibuat dan kemudian data-data tersebut akan dimasukkan ke dalam context dengan nama education_list dan diteruskan ke template education.html dengan fungsi render().

Dalam template education tadi sudah dibuatkan kondisi for loop untuk memasukkan semua data-data yang ada di dalam model Education ini, tetapi kalau tidak adapun tetap akan memuat suatu teks dengan kondisi kalau {%empty%} di mana akan muncul teks "No education has been added yet."

Hasil render tersebutlah yang akan kemudian dikirim sebagai HTML response ke browser dan browser pada akhirnya akan memuat CSS dan gambar yang dirujuk oleh HTML sehingga halaman bisa menunjukkan semua yang sudah dibuat tadi.

2. Data di bagian portfolio ini lebih baik disimpan dalam bentuk model karena akan memudahkan developer untuk memasukkan langsung data-data baru kedepannya dalam bentuk database sederhana daripada menambahkan manual hal-hal baru langsung ke templatenya yang juga pada akhirnya bisa membuat sebuah error pada tampilan akhirnya. 

Selain itu, dalam modelnya sendiri sudah dibuatkan beberapa kondisi unik yang bisa disesuaikan secara manual dalam pengisian databasenya agar bisa mudah dimengerti kedepannya atas fitur-fitur yang sudah diimplementasikan dalam HTMLnya sendiri.

3. Perbedaan dari makemigrations dengan migrate sebenarnya sederhana. Makemigrations sendiri digunakan untuk membuat file migrationnya berdasarkan definisi model yang baru dibandingkan dengan migration sebelumnya. Jadi file baru yang dibuat makemigrations ini akan mencatat perubahan database, tetapi belum diterapkan ke databasenya.

Sementara migrate ini adalah fitur untuk menerapkan migrationnya yang sudah dibuat dalam makemigrations tadi dan hal ini akan mengubah struktur database secara keseluruhan tergantung dengan perubahan yang dibuat.

Contoh perubahan model yang mengharuskan untuk menjalankan kedua perintah ini adalah kalau ada perubahan model dalam main/models.py karena file inilah yang memegang seluruh bentuk database dari webnya. Jadi misalkan ada membuat perubahan ke bagian title, institution, major, thumbnail, ataupun primary key lainnya dalam model education akan membutuhkan developer untuk melakukan dua command makemigrations dan migrate tersebut karena databasenya yang mau diubah bukan tampilan atau data yang dimasukkan ke dalam database tersebut yang diubah.

## AI Disclosure:
Model yang digunakan adalah Chat GPT-6 Astra dan juga Chat GPT-5.6 Terra

1. Cakupan Penggunaan dan Prompting

Prompt Strategy: Saya menggunakan AI untuk mengimplementasikan ide-ide baru terkait design css untuk web serta tampilan dan layoutnya. Selain itu, saya juga melakukan prompting untuk membantu dalam proses pembuatan unit test serta untuk mengerti pembuatan data-data untuk current database yang available melalui model-model baru yang dibuat. Terakhir saya juga meminta bantuan AI untuk mengerti bentuk-bentuk fitur yang bisa dimasukkan ke dalam model django.

Menambahkan dan merancang model baru untuk education section:
    Prompt: "I wanna make a new page which is the education page. I want it to appear like a pin list with the left side having a timeline, and the top one is the one that I'm currently doing."
    Tujuan: Membuat halaman education terpisah yang mengambil data dari model Education, mengurutkan pendidikan yang masih berlangsung di bagian paling atas, serta menampilkan institusi, program studi, periode, logo, dan deskripsi pendidikan secara dinamis.

Perbaikan Query dan Django Template:
    Prompt: "This part that I highlighted makes an error help me fix please" dan "Invalid block tag on line 76: 'empty', expected 'elif', 'else' or 'endif'."
    Tujuan: Memperbaiki import query expression Django yang diperlukan untuk pengurutan data, serta memahami susunan tag template {% for %}, {% empty %}, {% if %}, dan {% endif %} agar halaman education dapat dirender tanpa error.

Iterasi Desain CSS Education dan Responsivitas:
    Prompt: "Make a simpler timeline with hover effects for the text and pin" dan "Add adaptability for other media, like for mobile visibility."
    Tujuan: Mengembangkan tampilan education melalui beberapa iterasi, mulai dari timeline dengan pin hingga kartu pendidikan terpisah. AI digunakan untuk membantu membuat logo berada di sisi kiri kartu, efek hover, tampilan mobile, fallback untuk perangkat touch, serta dukungan prefers-reduced-motion. Saya tetap mengevaluasi hasil visualnya dan menyesuaikan desain yang tidak sesuai dengan preferensi saya.

Pembersihan CSS yang Tidak Digunakan:
    Prompt: "Help me delete all the unnecessary CSS designs as I have deleted the experience and education part in the index one."
    Tujuan: Menghapus selector CSS lama yang hanya digunakan oleh section Experience dan Education pada homepage, tetapi tetap mempertahankan selector yang masih dipakai oleh halaman Profile, Experience, dan Education terpisah.

Pembuatan Unit Test:
    Prompt: "Based on the existing unit test that I have right now help me make a new one for the new model that I added. Just tell me what parts I have to add and also the syntax"
    Tujuan: Mengerti cara membuat unit test baru untuk model yang baru dan sesuai dengan skenario yang sudah dibuat dalam ketentuan yang berlaku di web PBP

2. Pengkritisan Terhadap AI
    Mayoritas design atau ide CSS yang diberikan AI tidak sesuai dengan keinginan yang saya inginkan sehingga saya pada akhirnya melakukan perubahan secara manual dan mengubah seluruh layout CSSnya sendiri. Seperti untuk timeline di education section awalnya masih tidak centered dan tidak membentuk tampilan kartu yang diinginkan sehingga saya pada akhirnya harus menambahkan fitur-fitur baru sendiri ke dalam CSSnya dan juga memodifikasi template educationnya seperti menambahkan div baru agar bisa membagi-bagi content untuk card educationnya.


# Assignment 3

1. Pada tugas kali ini, ModelForm digunakan karena komponen ini membuat kolom formulir dan aturan validasi berdasarkan model. Hal ini membuat duplikasi kode berkurang dan menjaga konsistensi antara input formulir dengan struktur basis data. EducationForm menggunakan model Education dan hanya menampilkan kolom-kolom yang dapat diedit oleh pengguna.
Menambahkan `{% csrf_token %}` pada formulir POST sebagai perlindungan terhadap serangan *Cross-Site Request Forgery* (CSRF). Tanpa perlindungan ini, situs web berbahaya dapat mencoba melakukan tindakan tertentu dengan memanfaatkan peramban dan sesi masuk pengguna. *Middleware* CSRF Django akan memeriksa token tersebut sebelum menerima permintaan.

2. JSON lebih umum digunakan daripada XML pada modern web application karena dia lebih compact dan dapat mempetakan databasenya ke JavaScript objekct dan arrays. Ini membuatnya lebih jelas untuk web clients menggunakannya. XML sebenarnya masih bisa berguna dalam beberapa sistem, tetapi karena adanya opening dan closing tag itu membuat datanya menjadi bertele-tele.

3. Saat klient meminta '/api/education', Django akan merutekan request tersebut ke 'get_educations_json' view. Dari view itu, ini akan mengambil data edukasi dari database, mengaplikasikan filter yang direquest (jika ada), dan menserialisasikan queryset dengan 'serializers.serialized('json', educations)'. Setelah itu dia akan mengembalikkan JSON text dalam HttpResponse dengan tipe konten 'application/json'.
Serialazation ini esensial dan penting karena instance model Django adalah object Python dan sementara JSON tidak merepresentasikan object tersebut secara langsung. Serialization memgubah kunci primernya dan memetakan nilainya ke dalam format yang klient bisa terima dan gunakan.

## AI Disclosure:
Model yang digunakan adalah: Chat GPT 6 Astra dan Chat GPT 5 Luna serta Copilot

1. Cakupan penggunaan dan strategi prompting
Prompt Strategy: Saya menggunakan AI untuk membantu mengadaptasikan fitur yang sudah ada dari tutorial 3 ke salah satu section existing aku sekarang. Saya memberikan referensi checklist apa saja yang harus diselesaikan dan kemudian meminta guideline apa saja yang harus dikerjakan. Namun karena pada akhirnya terlalu banyak yang diubah-ubah, saya ulangi semua lagi dari awal pengerjaan dan membuat ulang semuanya sendiri untuk bagian viewsnya dan baru dalam implementasi di template dan CSS saya meminta bantuan.

Beberapa contoh prompt yang diguanakan:
    Prompt: "kok aku pencet tombol batal malah kebuka ke bagian page project padahal tadi dari education page" 
    Jawaban: Masalahnya karena form Education masih memakai URL milik Project: 
            Tombol Batal mengarah ke show_projects
            Form submit memakai create_project
            Redirect setelah berhasil juga menuju halaman Project
        Sudah diperbaiki di educations_form.html dan views.py. Sekarang tombol Batal kembali ke halaman Education, dan redirect tambah Education juga tetap di Education.
        Pemeriksaan diagnostik tidak menemukan error. Test otomatis belum dijalankan karena dilewati oleh terminal.
    Prompt: "oke sekarang aku mau ada tombol hapus dan update (untuk education) untuk masing-masing card di bagian kanan bawah itu kecil aja gapapa"
    Jawaban: Sudah ditambahkan:
            Tombol Update kecil di kanan bawah setiap kartu Education
            Tombol Hapus Pendidikan dengan modal konfirmasi
            Form Education sekarang mendukung mode tambah dan update
            Tombol Batal pada form tetap kembali ke halaman Education
        Perubahan ada di education.html, educations_form.html, dan style.css. Validasi diagnostik tidak menemukan error. Test otomatis kembali dilewati oleh terminal.
    Prompt: "coba itu posisi tombolnya gak bisa di bikin bagian bawah kanan apa ya? sama kayak kasih animasi hover tombolnya dong, sama juga buat tombol tambah education coba ditaro ke kanan dong"
    Jawaban: Sudah diatur:
            Tombol Update dan Hapus sekarang berada di kanan bawah setiap card.
            Tombol memiliki animasi hover, focus, dan active.
            Tombol Tambah Education sekarang berada di kanan heading.
            Pada layar kecil, layout tetap responsif dan tombol tambah tetap rapi di kanan.
        Perubahan ada di education.html dan style.css. Tidak ada error diagnostik.
    Prompt: "coba itu ato gak buat sampingan gitu tapi taro di bawah teks education yang lain dan bikin sesuai gitu turun (tapi tetep tombol update dan hapus pendidikan masih setara tingginya). Ukuran tombolnya sama juga dan juga tuker itu warnanya, update harusnya yang pink terus hapus yg hitam"
    Jawaban: Sudah diubah:
            Tombol Tambah Education sekarang berada di bawah teks deskripsi Education.
            Tombol Update dan Hapus Pendidikan tetap sejajar di kanan bawah card.
            Ukuran kedua tombol dibuat sama.
            Update berwarna pink.
            Hapus Pendidikan berwarna hitam.
            Animasi hover tetap aktif tanpa mengubah warna utama tombol.
        Tidak ada error diagnostik.
    Prompt: "kenapa logo yang ditambahkan dengan link drive itu belum muncul ya?"
    Jawaban: Kemungkinan besar URL yang dimasukkan adalah link berbagi atau halaman preview Drive. Template langsung memasukkan nilainya ke src gambar, sementara halaman preview Drive bukan file gambar. [education.html (line 30)](/Users/eleazarmalau/Documents/MyPortofolio/templates/education.html:30)
            Coba gunakan format yang sesuai dengan placeholder form:
                https://drive.google.com/thumbnail?id=ID_FILE&sz=w1000
    Ganti ID_FILE dengan ID dari link Drive, lalu pastikan akses file diatur ke Siapa saja yang memiliki link. Untuk mengecek, buka URL thumbnail itu di jendela privat: kalau gambar tidak tampil di sana, kemungkinan URL atau izin aksesnya yang bermasalah.
    Prompt: "tombol updatenya bisa gak ya dikecilin? jadi dia ngesesuain ama besar isinya gitu"
    Jawaban: Sudah. Tombol Update sekarang lebarnya mengikuti teks dan padding-nya, sedangkan ukuran tombol hapus tetap. Perubahan ada di [style.css](/Users/eleazarmalau/Documents/MyPortofolio/static/css/style.css).

Link Share Chat:
https://drive.google.com/file/d/18c44cPxryo0fLRedGAm11sWPG_2E6n4Y/view?usp=sharing
https://chatgpt.com/s/cx_6ab15c96e2c481919aebdeece4b88aa2
https://chatgpt.com/s/cx_6ab15cc7da34819196d2bbba338d72f0

2. Pengkritisan terhadap AI
Masih banyak sekali prompt yang saya berikan sepertinya tidak dimengerti oleh AI kalau dalam segi yang kompleks sehingga masih harus saya breakdown dan kerjakan secara manual terlebih dahulu baru saya meminta AI untuk melakukan pengecekkan apakah semua sudah sesuai dan apakah akan berjalan dengan benar pada akhirnya.


# Assignment 4

### Progres
Commit 1: Adding an editor role and enforcing role-based acess for education as well as adding a new star model for education
Yang dikerjakan:
- Tambahkan fungsi is_editor(user) untuk mengecek grup Editor.
- Tambahkan @login_required pada create, update, dan delete.
- Create dan delete hanya untuk superuser.
- Update untuk superuser atau Editor.
- Gunakan PermissionDenied untuk pengguna login yang tidak berhak.
- Tambahkan @require_POST pada delete.
- Biarkan halaman baca dan JSON tetap publik.

Commit 2: Display education controls based on user role
Yang dikerjakan
- Kirim is_editor melalui context show_education.
- Membungkus button education agar sesuai dengan user role

Commit 3: Add education star relation and protect JSON output
Yang dikerjakan:
- Tambahkan starred_by = models.ManyToManyField(...) pada Education.
- Batasi field yang diserialisasi di get_educations_json agar starred_by tidak ikut tampil.

Commit 4: add authenticated education star google
Yang dikerjakan:
- Tambahkan fungsi toggle_education_star.
- Gunakan @login_required dan @require_POST.
- Jika pengguna sudah memberi star, hapus relasinya.
- Jika belum, tambahkan relasinya.
- Tambahkan URL education/<uuid:education_id>/star/.

Commit 5: Show education star counts
Yang dikerjakan:
- Siapkan jumlah star dan status star pengguna di show_education.
- Tambahkan form POST dengan {% csrf_token %}.
- Tampilkan Star atau Unstar sesuai status pengguna.
- Tampilkan total star.
- Untuk pengunjung, tampilkan tautan login.

Commit 6: Added tests for the new features
- Tambahkan pengujian akses untuk pengunjung, pengguna biasa, Editor, dan superuser.
- Uji bahwa akses langsung ke URL tetap dibatasi.
- Uji star/unstar, POST, CSRF, serta keamanan JSON.

Commit 7: New colors and adjusting css stuff
- Memperbaiki segala macam bentuk CSS yang kurang rapih

Commit 8: Menambahkan update untuk projects
- Membuat bagian update untuk projects dan sesuai dengan role-based access

## AI Disclosure
Model yang digunakan adalah: Chat GPT 6 Astra-Light

Prompt Strategy: Saya menggunakan AI untuk membantu memperbaiki CSS pada section Projects dan Education. Saya memberikan screenshot dan kode CSS, lalu meminta bantuan untuk merapikan ukuran tombol, jarak antar elemen, serta kesejajaran teks dan tombol. Ketika hasil perubahan belum sesuai, saya memberikan screenshot dan kode terbaru agar penyebabnya diperiksa kembali. Selain itu saya juga meminta untuk memberikan framework dan list pengeerjaan yang harus dibuat agar lebih runtut proses pengerjaannya.

Beberapa contoh prompt yang digunakan:
        Prompt: “buat apa yang harus dikerjain dalam bentuk hitungan per commit, jadi bikin progress commit git gitu”
        Jawaban: AI membagi pengerjaan menjadi enam tahap: pembatasan akses Education, penyesuaian tombol berdasarkan role, penambahan relasi star dan pembatasan JSON, implementasi toggle star, tampilan status star, serta pengujian dan dokumentasi. Setiap tahap disertai contoh perintah dan pesan commit.

        Prompt: “coba ini apa aja yang dibikin ke kodenya langsung?”
        Jawaban: AI memberikan contoh perubahan pada main/views.py, meliputi:
            - Fungsi is_editor() untuk memeriksa keanggotaan grup Editor.
            - @login_required untuk mengarahkan pengunjung ke login.
            - Pemeriksaan superuser pada create dan delete.
            - Pemeriksaan superuser atau Editor pada update.
            - PermissionDenied untuk menghasilkan HTTP 403.
            - @require_POST untuk membatasi metode penghapusan.

        Prompt: “Implement the Editor role using Django Group or Permission (assigned exclusively via Django Admin). Buat bagian ini, ini tau darimana?”
        Jawaban: AI menjelaskan bahwa role Editor diketahui melalui relasi grup pada akun pengguna. Fungsi user.groups.filter(name="Editor").exists() hanya memeriksa keanggotaan. Pembuatan grup dan penetapan anggotanya dilakukan melalui Django Admin, bukan melalui form registrasi.

        Prompt: “‘HttpResponse’ object has no attribute ‘prefetch_related’ — ini error apa?”
        Jawaban: AI menjelaskan bahwa get_educations_json() menghasilkan HttpResponse, sedangkan prefetch_related() digunakan pada QuerySet. AI menyarankan menghapus pemanggilan tersebut dari respons JSON dan mempertahankan proses deserialisasi yang digunakan pada halaman Education.

        Prompt: “coba kalo bagian ini kerjainnya gimana?”
        Jawaban: Untuk tahap penambahan star, AI memberikan contoh ManyToManyField bernama starred_by pada model Education, perintah makemigrations dan migrate, serta daftar field eksplisit pada serialisasi JSON agar identitas pemberi star tidak ikut dikirim.

        Prompt: “kalo ini kodenya gimana?”
        Jawaban: AI memberikan fungsi toggle_education_star dan route pada main/urls.py. Fungsi tersebut memerlukan login, hanya menerima POST, dan menambahkan atau menghapus relasi star berdasarkan status pengguna pada Education yang dipilih.

        Prompt: “I wanna use the components just like this one … to add the star button buat educationnya gimana caranya”
        Jawaban: AI membantu memisahkan tombol star menjadi templates/components/education_star.html, kemudian memanggilnya melalui {% include %} pada setiap kartu Education. Component menampilkan tombol Star/Unstar bagi pengguna login, jumlah star, dan tautan login bagi pengunjung. Saya juga mendiskusikan penggunaan relasi education.starred_by langsung di template.

        Prompt: “Invalid block tag … ‘empty’, expected ‘elif’, ‘else’ or ‘endif’ — kenapa dapet error itu?”
        Jawaban: AI menemukan dua typo pada template: {% endif } yang kekurangan % dan is.editor yang seharusnya is_editor. Tag penutup yang salah membuat Django menganggap blok if belum selesai ketika menemukan {% empty %}.

        Prompt: “kalau ini bikin juga kodenya dong”
        Jawaban: AI menyusun contoh pengujian pada main/tests.py untuk akses empat role, pembatasan URL langsung, CRUD owner, update Editor, star/unstar, pencegahan relasi duplikat, POST, CSRF, keamanan JSON, dan visibilitas tombol. AI juga memberikan draft dokumentasi pengaturan Editor untuk README.

        Prompt: “FAIL: test_action_buttons_follow_user_role … (user='editor') … pas test dapet ini”
        Jawaban: AI menjelaskan bahwa halaman berhasil dibuka, tetapi link Update tidak ditemukan untuk Editor. Pemeriksaan diarahkan pada pengiriman is_editor melalui context, penulisan kondisi template, dan kemungkinan tombol Update berada di dalam kondisi khusus superuser. Hasil tes yang saya kirim saat itu menunjukkan 20 tes dijalankan dengan satu kegagalan.

        Prompt: “that's all my css code, tell me which ones I need to change to make it more appealing”
        Jawaban: AI meninjau CSS dan menyarankan perubahan terarah: memperbaiki variabel --radius, mengganti gradient halaman dengan warna netral, mempertahankan Rose Quartz dan Serenity sebagai aksen, memperhalus border dan shadow, serta menyeragamkan ukuran dan warna tombol.

        Prompt: “gak ada buat kayak automatic antar semua elemen gitu?”
        Jawaban: AI menjelaskan penggunaan display: flex, flex-direction: column, dan gap untuk mengatur jarak antar anak langsung container. AI juga menjelaskan perbedaan gap, margin antarelemen, dan line-height untuk jarak antarbaris teks.

        Prompt: “masih gak align coba cekin itu kenapa?”
        Jawaban: Setelah membaca CSS terbaru dan screenshot, AI menemukan bahwa .experience-status masih memiliki padding-top: 1rem, sementara aturan khusus Projects hanya menghapus margin-top. AI menyarankan menghapus margin dan padding pada pembungkus tombol Hapus agar sejajar dengan tombol Star.

        Prompt: “coba tambahin bagian update ke projects kayak di education”
        Jawaban: AI memeriksa ZIP terbaru dan memberikan perubahan pada empat file: main/views.py, main/urls.py, templates/projects.html, dan templates/projects_form.html. Perubahan mencakup view update untuk Editor dan superuser, URL edit, tombol bersyarat, serta form bersama untuk tambah dan update. AI menekankan penggunaan instance=project dan action form yang sesuai agar penyimpanan edit tidak membuat proyek baru.
Link Share Chat:
https://chatgpt.com/share/6aba8537-72ec-83ec-902a-9a4e19786b9f

2. Pengkritisan Terhadap AI
Banyak hasil prompt yang diberikan tidak konsisten terutama dalam bagian CSSnya sehingga saya harus mencari sendiri permasalahannya dan menyelesaikannya sendiri, seperti prompt prompt error yang saya kirim pada akhirnya saya mengerjakannya sendiri pada akhirnya karena jawaban AI kurang jelas. Selain itu, di bagian CSS saya membuat beberapa sendiri buat pengaturannya agar sesuai dengan keinginan yang saya inginkan.

# Assignment 5

### Progres
Commit 1: Adding CRUD to experience section
Yang dikerjakan:
- Membuat sistem CRUD ke bagian experience
- Membuat CSSnya juga agar lebih rapih tampilannya

Commit 2: Cleaning and validating education form
Yang dikerjakan:
- Merapikan EducationForm, termasuk field, label, dan widget untuk judul pendidikan, institusi, jurusan, deskripsi, URL gambar, serta tahun mulai dan selesai.
- Menambahkan fungsi _clean_text_field() untuk membersihkan tag HTML menggunakan strip_tags() dan membuang spasi di awal serta akhir input.
- Menambahkan validasi khusus melalui clean_title(), clean_institution(), clean_major(), dan clean_description().

Commit 3: Change views and JSON and also added POST AJAX
Yang dikerjakan:
- Mengubah show_education() agar hanya merender kerangka halaman, sementara daftar Education nantinya dimuat oleh JavaScript.
- Menambahkan @ensure_csrf_cookie agar cookie CSRF tersedia untuk request AJAX.
- Mengirim konfigurasi endpoint daftar, tambah, login, serta status autentikasi melalui education_config.
- Menyediakan EducationForm pada halaman hanya untuk superuser/owner.
- Mengubah get_educations_json() agar menghasilkan JSON secara manual dan hanya menerima request GET.
- Menambahkan pencarian berdasarkan title__icontains.
- Mengurutkan pendidikan yang masih berlangsung terlebih dahulu, kemudian berdasarkan tahun mulai terbaru dan institusi.
- Menggunakan prefetch_related("starred_by") untuk memuat relasi star.
- Menambahkan star_count dan is_starred ke respons JSON tanpa membagikan identitas pemberi star.
- Menambahkan URL aksi pada JSON sesuai role: Update untuk Editor/Owner, Hapus untuk Owner, dan Star untuk pengguna yang login.
- Menambahkan create_education_ajax() yang menerima POST, memeriksa izin owner, memvalidasi EducationForm, lalu menyimpan data.

Commit 4: Added URL for the new AJAX
Yang dikerjakan:
- Mengimpor view create_education_ajax.
- Mendaftarkan endpoint education/add-ajax/ dengan nama URL create_education_ajax.

Commit 5: Added new html features for the education adaptation for the AJAX including new modals
Yang dikerjakan:
- Menghapus loop template yang sebelumnya langsung menampilkan data dari database.
- Menyediakan <ol id="education-list"> kosong sebagai tempat kartu yang dibuat JavaScript.
- Menambahkan input pencarian.
- Menambahkan area feedback untuk loading, kosong, dan error, serta tombol Coba lagi.
- Menambahkan pesan <noscript> bagi pengguna yang menonaktifkan JavaScript.
- Menyimpan konfigurasi dengan json_script dan memuat education.js menggunakan defer.
- Menambahkan modal Tambah Education dengan field dari EducationForm, CSRF token, area error tiap field, serta tombol Batal dan Submit.
- Menambahkan modal konfirmasi hapus yang menampilkan nama Education yang akan dihapus.
- Membatasi tombol Tambah dan kedua modal tersebut agar hanya dirender untuk Owner.

Commit 6: Added the javascript for education section
- Membuat konfigurasi javascript untuk education section

Commit 7: Changed the star and deletion method for education through AJAX
- Mengubah toggle_education_star() agar mengembalikan JSON ketika request memakai header Accept: application/json.
- Mengirim pesan, jumlah star terbaru, dan status is_starred setelah aksi star/unstar.
- Tetap mensyaratkan login dan metode POST untuk aksi star.
- Mengubah delete_education() agar mengembalikan JSON untuk request AJAX setelah penghapusan berhasil.

Commit 8: Menambahkan update untuk projects
- Membuat bagian update untuk projects dan sesuai dengan role-based access

1. Debouncing berguna untuk menunda pemanggilan fungsi sampai tidak ada event baru selama selang waktu terentu. Jadi di implementasi ini, debouncing dibuat dengan timer 350 ms sehingga setiap input membatalkan timer sebelumnya dengan 'clearTimeout'. Hal ini berguna kalau user mengetik dengan cepat sehingga pencarian akan dilakukan setelah user selesai menuliskan apa yang sebenarnya ingin dituliskan. Hal ini membuat request dan query database berkurang dan membuat hasil lebih stabil 

2. fetch itu mengembalikan Promise atau sebuah hasil yang masih ditunggu. Await fetch(url) itu menunggu respons server, lalu await.response(json) membaca data JSON-nya. Tanpa ada await, hasilnya masih Promise itu tadi dan jadinya perlu ditangani oleh fungsi baru seperti, .then() atau .catch(). await() hanya menunda kelanjutan fungsi tersebut, sehingga browser masih bisa digunakan. Status errorpun juga perlu diperiksa kembali oleh response.ok karena tidak otomatis dianggap gagal oleh fetch().

3. Cross-Site Scripting terjadi ketika input tidak tepercaya dijalankan sebagai script di browser pengguna. Intinya XSS terjadi ketika input pengguna dijalankan sebagai kode berbahaya di browser. Pada fitur education sendiri, data ditampilkan menggunakan createElement dan textContent agar terbaca sebagai teks biasa. Server juga membersihkan tag HTML menggunakan strip_tags, sementara URL divalidasi untuk membatasi alamat yang digunakan.

## AI Disclosure
**1. Cakupan Penggunaan AI dan Strategi Prompt**

Model yang digunakan adalah: **ChatGPT — GPT-6 Luna dan GPT-6.1 Sol.**

**Prompt Strategy:** Saya menggunakan AI untuk membantu menambahkan CRUD pada section Experience dan mengimplementasikan interaktivitas AJAX pada section Education sesuai checklist Individual Assignment 5. Saya memberikan ZIP proyek, kode, screenshot, dan pesan error agar AI dapat meninjau struktur serta memberikan perubahan yang relevan. Bantuan AI mencakup penyusunan kode form, view, URL, template, CSS, JavaScript, serta pengujian dan dokumentasi.

Saya meminta perubahan disampaikan secara bertahap, dengan penjelasan lokasi file dan bagian kode yang perlu diganti, agar prosesnya lebih mudah dipahami dan diterapkan. Ketika saran belum sesuai dengan tampilan yang saya inginkan atau muncul error, saya memberikan kode terbaru dan meminta pemeriksaan kembali. Saya juga meminta panduan berurutan untuk mempelajari implementasi Assignment 5.

**Beberapa contoh prompt yang digunakan:**

**Prompt:** “coba masukkan bagian crud untuk bagian experience dan coba sesuain aja bentuaknnya kayak yang di education”

**Jawaban:** AI membantu menambahkan CRUD Experience mengikuti pola Education. Superuser dapat menambah, mengedit, dan menghapus Experience, sedangkan Editor hanya dapat mengedit. Form mencakup nama pengalaman, organisasi/perusahaan, kategori, deskripsi, thumbnail, serta waktu mulai dan selesai. AI juga menyediakan ZIP hasil perubahan dan melaporkan hasil pengujian di lingkungan pengerjaannya.

**Prompt:** “kasih gw kodenya yang diganti aja dan bertahap”

**Jawaban:** AI mulai memberikan perubahan per file, dimulai dari `ExperienceForm` pada `main/forms.py`. Form menggunakan `ModelForm`, mengatur label dan widget, memperbolehkan waktu selesai dikosongkan, serta memvalidasi bahwa waktu selesai tidak mendahului waktu mulai. Tahap berikutnya membahas view CRUD, URL, template form, dan tombol aksi.

**Prompt:** “di kelas itu bagian category belum ada widgetsnya apakah aman?”

**Jawaban:** AI menjelaskan bahwa field model yang memiliki `choices` otomatis menggunakan widget `Select` atau dropdown pada `ModelForm`. Karena itu, widget `category` tidak perlu didefinisikan secara eksplisit kecuali saya ingin menambahkan atribut atau pengaturan tampilannya.

**Prompt:** “eh aku mau bikin ini juga dalam bentuk json itu loh gimana caranya biar kayak yang lain?”

**Jawaban:** AI memberikan contoh fungsi `get_experiences_json()` pada `main/views.py` menggunakan `serializers.serialize()`, dengan daftar field yang ditentukan. AI juga menambahkan route `/api/experiences/` pada `main/urls.py` agar data Experience dapat diakses dalam bentuk JSON.

**Prompt:** Saya mengirim traceback error saat menjalankan server setelah menambahkan form Experience.

**Jawaban:** AI mengidentifikasi typo `ended-at` pada `ExperienceForm`, sementara nama field model yang benar adalah `ended_at`. AI menyarankan memperbaiki nama tersebut pada `fields`, `labels`, dan `widgets`. Perbaikan ini tidak membutuhkan migration karena tidak mengubah model.

**Prompt:** “bagian started at nya selalu bilang enter a valid date/time itu kenapa?”

**Jawaban:** AI menjelaskan kemungkinan ketidaksesuaian format input tanggal dengan format yang diterima form. AI menyarankan penggunaan `datetime-local`, penyesuaian `input_formats`, serta pemeriksaan posisi fungsi `__init__` agar berada di dalam kelas form. AI juga menjelaskan perbedaan `%m` untuk bulan dan `%M` untuk menit.

**Prompt:** “kalo aku maunya cuman tahun aja gimana?”

**Jawaban:** AI menyarankan perubahan label menjadi Tahun Mulai dan Tahun Selesai, penggunaan input angka, serta format `%Y`. Pendekatan tersebut tetap menggunakan field datetime yang sudah ada, sehingga input tahun direpresentasikan sebagai tanggal 1 Januari pada tahun tersebut. Tahun selesai tetap dapat dikosongkan untuk pengalaman yang masih berlangsung.

**Prompt:** “tombol update, deletenya gak muncul tapi di cardnya itu gimana?”

**Jawaban:** AI mengarahkan pemeriksaan pada context `is_editor`, kondisi role di template, dan posisi tombol. Setelah saya mengirim kode template, AI menduga tombol terpotong akibat kombinasi `min-height: 100%` pada `.card-inner` dan `overflow: hidden` pada kartu, lalu memberikan penyesuaian CSS.

**Prompt:** “ih jelek gak suka aku maunya di kartunya pas udah di flip itu gimana?”

**Jawaban:** AI menyesuaikan saran dengan memindahkan tombol Update dan Hapus ke sisi belakang kartu, di dalam `.experience-content`. Dialog konfirmasi hapus ditempatkan di luar kartu yang berputar, sementara tombol pembukanya tetap berada pada kartu. AI juga meminta aturan CSS sebelumnya diganti agar sesuai dengan susunan baru.

**Prompt:** “itu kotak buat buttonnya bisa gak diilangin dan jadinya tu tombol update dan hapus setara sama tulisan completednya”

**Jawaban:** AI menyarankan pembungkus `.experience-card-footer` yang menyatukan status Ongoing/Completed dan tombol aksi. Pengaturan Flexbox digunakan untuk menyejajarkan keduanya. Background, border, dan shadow pada pembungkus tombol dihilangkan agar tidak terlihat seperti kotak terpisah.

**Prompt:** “Coba tolong kerjakan bagian individual assignment itu dan sesuai dengan checklistnya dan kasih guide dan panduan pengerjaannya ke saya dan berurutan supaya bisa dimengerti dan dipelajari juga”

**Jawaban:** AI memilih Education sebagai bagian implementasi Assignment 5 karena sudah memiliki fitur star. AI menyediakan kode hasil perubahan dan panduan berurutan yang mencakup:
- Validasi dan pembersihan input pada `EducationForm`.
- View halaman skeleton, JSON dengan informasi star, dan endpoint POST AJAX.
- URL, modal tambah, serta modal konfirmasi hapus.
- JavaScript untuk fetch, pencarian dengan debounce 350 ms, loading/empty/error state, retry, dan toast.
- Rendering menggunakan `createElement` dan `textContent`, pengiriman CSRF token, serta pembaruan daftar tanpa reload halaman.
- Aksi star/unstar dan hapus melalui AJAX.
- Pengujian, dokumentasi, serta panduan commit dan submission.

AI melaporkan 35 tes Django lulus di lingkungan pengerjaannya, tetapi menyatakan bahwa tampilan dan perilaku modal masih perlu diperiksa melalui browser lokal.

**Prompt:** Saya mengirim error `TemplateDoesNotExist: components/education_form_modal.html` dan menanyakan file modal yang belum tersedia.

**Jawaban:** AI menjelaskan bahwa `education.html` sudah memanggil komponen yang belum dibuat pada proyek lokal saya. AI kemudian memberikan kode lengkap untuk `education_form_modal.html` dan `education_ajax_delete_modal.html`, serta menjelaskan bahwa keduanya harus berada di folder `templates/components/` dengan nama yang sesuai dengan `{% include %}`.

**Link Share Chat:**

https://chatgpt.com/share/6ac3d1c0-4760-83ec-a844-4b1db0ed6c95

**2. Pengkritisan Terhadap AI**

Jawaban AI tidak selalu langsung sesuai dengan kebutuhan saya. Pada awalnya, AI memberikan hasil dalam bentuk ZIP, sementara saya membutuhkan potongan kode dan penjelasan bertahap agar dapat memahami perubahan. Penyampaian tahap juga sempat berhenti satu per satu, sehingga saya perlu memperjelas bentuk panduan yang saya inginkan.

Dalam bagian tampilan, saran awal menempatkan tombol di luar bagian kartu yang berputar dan menambahkan pembungkus yang tidak sesuai dengan desain saya. Saya kemudian memberikan feedback agar tombol berada pada sisi belakang kartu dan sejajar dengan status Completed. Hal ini menunjukkan bahwa hasil AI perlu ditinjau kembali berdasarkan tampilan nyata dan preferensi desain saya.

Saat menerapkan AJAX Education, muncul error karena template memanggil komponen modal yang belum tersedia di proyek lokal. Saya perlu meminta penjelasan dan kode komponen tersebut secara eksplisit. Karena itu, saya tidak cukup hanya mengikuti satu potongan kode, tetapi perlu memeriksa keterkaitan form, view, URL, template, dan JavaScript.

Saya juga membedakan laporan pengujian AI dari hasil pengujian pada proyek lokal. Tes yang dilaporkan lulus oleh AI tidak otomatis membuktikan bahwa seluruh tampilan, modal, dan interaksi sudah berjalan sesuai kebutuhan saya di browser.