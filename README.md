[![Deploy](https://telegra.ph/file/6771430f1b5cdf95b03ef.jpg)](https://heroku.com/deploy?template=https://github.com/SendiAp/TakanashiRika.git)
# TakanashiRika
### Click Below Image to Deploy
[![Maintenance](https://img.shields.io/badge/Maintained%3F-yes-green.svg)](https://GitHub.com/Naereen/StrapDown.js/graphs/commit-activity) [![GPLv3 license](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://perso.crans.org/besson/LICENSE.html) [![Open Source Love svg2](https://badges.frapsoft.com/os/v2/open-source.svg?v=103)](https://github.com/ellerbrock/open-source-badges/) [![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=flat-square)](https://makeapullrequest.com)

Bot Telegram Python modular berjalan di python3 dengan database sqlalchemy.

## How to setup/deploy.



<details>
  <summary>Steps to deploy on Heroku !! </summary>

```
Isi semua detailnya, Deploy!
Sekarang pergi ke https://dashboard.heroku.com/apps/(app-name)/resources ( Replace (app-name) with your app name )
Turn on worker dyno (Don't worry It's free :D) & Webhook
Now send the bot /start, If it doesn't respond go to https://dashboard.heroku.com/apps/(app-name)/settings and remove webhook and port.
```

[![Deploy To Heroku](https://www.herokucdn.com/deploy/button.svg)](https://dashboard.heroku.com/new?button-url=https%3A%2F%2Fgithub.com%2FSendiAp%2FTakanashiRika&template=https%3A%2F%2Fgithub.com%2FSendiAp%2FTakanashiRika)



</details>  
<details>
  <summary>Steps to self Host!! </summary>

  ## Menyiapkan bot (Baca ini sebelum mencoba menggunakan!):
Pastikan untuk menggunakan python3.6, karena saya tidak dapat menjamin semuanya akan berfungsi seperti yang diharapkan pada versi Python yang lebih lama!
Ini karena penurunan harga parsi
  ### Configuration

Ada dua kemungkinan cara untuk mengonfigurasi bot Anda: file config.py, atau variabel ENV.

Versi yang lebih disukai adalah menggunakan file `config.py`, karena memudahkan untuk melihat semua pengaturan Anda dikelompokkan tog.

Disarankan untuk mengimpor sample_config dan memperluas kelas Config, karena ini akan memastikan konfigurasi Anda berisi semua
default diatur dalam sample_config, sehingga membuatnya lebih mudah untuk ditingkatkan.

Contoh file `config.py` dapat berupa:
```
from TakanashiRika.sample_config import Config

class Development(Config):
    OWNER_ID = ~  # your telegram ID
    OWNER_NAME = "Sendi"  # your Name
    API_KEY = "your bot api key"  # your api key, as provided by the @botfather
    SQLALCHEMY_DATABASE_URI = 'postgresql://username:password@localhost:5432/database'  # sample db credentials
    MESSAGE_DUMP = '-1234567890' # some group chat that your bot is a member of
    USE_MESSAGE_DUMP = True
    SUDO_USERS = [1307579425,]  # List of id's for users which have sudo access to the bot.
    LOAD = []
    NO_LOAD = ['translation']
```

Jika Anda tidak dapat memiliki file config.py (EG di Heroku), Anda juga dapat menggunakan variabel lingkungan.
Variabel env berikut didukung:
 - `ENV`: Setting this to ANYTHING will enable env variables

 - `TOKEN`: Your bot token, as a string.
 - `OWNER_ID`: An integer of consisting of your owner ID
 - `OWNER_NAME`: Your name

 - `DATABASE_URL`: Your database URL
 - `MESSAGE_DUMP`: optional: a chat where your replied saved messages are stored, to stop people deleting their old 
 - `LOAD`: Space-separated list of modules you would like to load
 - `NO_LOAD`: Space-separated list of modules you would like NOT to load
 - `WEBHOOK`: Setting this to ANYTHING will enable webhooks when in env mode
 messages
 - `URL`: The URL your webhook should connect to (only needed for webhook mode)

 - `SUDO_USERS`: A space-separated list of user_ids which should be considered sudo users
 - `SUPPORT_USERS`: A space-separated list of user_ids which should be considered support users (can gban/ungban,
 nothing else)
 - `WHITELIST_USERS`: A space-separated list of user_ids which should be considered whitelisted - they can't be banned.
 - `DONATION_LINK`: Optional: link where you would like to receive donations.
 - `CERT_PATH`: Path to your webhook certificate
 - `PORT`: Port to use for your webhooks
 - `DEL_CMDS`: Whether to delete commands from users which don't have rights to use that command
 - `STRICT_GBAN`: Enforce gbans across new groups as well as old groups. When a gbanned user talks, he will be banned.
 - `WORKERS`: Number of threads to use. 8 is the recommended (and default) amount, but your experience may vary.
 __Note__ that going crazy with more threads wont necessarily speed up your bot, given the large amount of sql data 
 accesses, and the way python asynchronous calls work.
 - `BAN_STICKER`: Which sticker to use when banning people.
 - `ALLOW_EXCL`: Whether to allow using exclamation marks ! for commands as well as /.

  ### Python dependencies

Instal dependensi Python yang diperlukan dengan pindah ke direktori proyek dan menjalankan:

`pip3 install -r requirements.txt`.

Ini akan menginstal semua paket python yang diperlukan.

  ### Database

Jika Anda ingin menggunakan modul yang bergantung pada basis data (misalnya: kunci, catatan, info pengguna, pengguna, filter, sambutan),
Anda harus memiliki database yang terinstal di sistem Anda. Saya menggunakan Postgres, jadi saya sarankan untuk menggunakannya 
Dalam kasus Postgres, ini adalah cara Anda mengatur database pada sistem Debian/ubuntu. Distribusi lain mungkin berbeda.

- install postgresql:

`sudo apt-get update && sudo apt-get install postgresql`

- change to the Postgres user:

`sudo su - postgres`

- create a new database user (change YOUR_USER appropriately):

`createuser -P -s -e YOUR_USER`

This will be followed by you need to input your password.

- create a new database table:

`createdb -O YOUR_USER YOUR_DB_NAME`

Change YOUR_USER and YOUR_DB_NAME appropriately.

- finally:

`psql YOUR_DB_NAME -h YOUR_HOST YOUR_USER`

Ini akan memungkinkan Anda untuk terhubung ke database Anda melalui terminal Anda.
Secara default, YOUR_HOST seharusnya 0.0.0.0:5432.

Anda sekarang harus dapat membangun URI database Anda. Ini akan menjadi:

`sqldbtype://username:pw@hostname:port/db_name`

Ganti sqldbtype dengan DB mana pun yang Anda gunakan (mis. Postgres, MySQL, SQLite, dll)
ulangi untuk nama pengguna, kata sandi, nama host (localhost?), port (5432?), dan nama DB Anda.

  ## Modules
   ### Setting load order.

Urutan pemuatan modul dapat diubah melalui pengaturan konfigurasi `LOAD` dan `NO_LOAD`.
Keduanya harus mewakili daftar.

If `LOAD` is an empty list, all modules in `modules/` will be selected for loading by default.

If `NO_LOAD` is not present or is an empty list, all modules selected for loading will be loaded.

If a module is in both `LOAD` and `NO_LOAD`, the module will not be loaded - `NO_LOAD` takes priority.

   ### Creating your own modules.

Membuat modul telah disederhanakan sebanyak mungkin - tetapi jangan ragu untuk menyarankan penyederhanaan lebih lanjut.

Yang diperlukan hanyalah file .py Anda ada di folder modul.

Untuk menambahkan perintah,

`from Takanashirika import dispatcher`.

You can then add commands using the usual

`dispatcher.add_handler()`.

Assigning the `__help__` variable to a string describing this modules' available
commands will allow the bot to load it and add the documentation for
your module to the `/help` command. Setting the `__mod_name__` variable will also allow you to use a nicer, user-friendly name for a module.

The `__migrate__()` function is used for migrating chats - when a chat is upgraded to a supergroup, the ID changes, so 
it is necessary to migrate it in the DB.

The `__stats__()` function is for retrieving module statistics, eg number of users, number of chats. This is accessed 
through the `/stats` command, which is only available to the bot owner.

## Starting the bot.

Setelah Anda menyiapkan database dan konfigurasi Anda selesai, jalankan file bat (jika di windows) atau jalankan (Linux):

`python3 -m Takanashirika`

You can use [nssm](https://nssm.cc/usage) to install the bot as service on windows and set it to restart on /gitpull 
Pastikan untuk mengedit kelelawar mulai dan mulai ulang sesuai kebutuhan Anda.
Catatan: kelelawar restart mengharuskan kontrol akun Pengguna dinonaktifkan.

Untuk pertanyaan atau masalah apa pun mengenai bot, silakan buka tiket masalah atau kunjungi kami di [Support](https://t.me/pikyus1)
## How to setup on Heroku 
Untuk permulaan klik tombol ini 
</details>  

## Credits
Bot didasarkan pada karya asli yang dilakukan oleh [SendiAp](https://github.com/SendiAp)



## [OWNER TAKANASHI](http://t.me/pikyus1)
