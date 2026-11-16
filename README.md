# learn_iot — ESP32 + MicroPython

ESP32 বোর্ডে MicroPython দিয়ে IoT শেখার প্রজেক্ট। প্রথম প্রোগ্রাম: অন-বোর্ড LED blink।

দৈনিক নোট: [docs/day-1.md](docs/day-1.md)

## প্রজেক্ট স্ট্রাকচার

```
learn_iot/
├── docs/
│   └── day-1.md        # Day 1 নোট
├── src/
│   ├── day_01/
│   │   └── main.py     # Day 1: LED blink
│   └── day_02/         # (পরে) প্রতিদিনের জন্য নতুন ফোল্ডার
├── Pipfile             # প্রজেক্টের প্যাকেজ তালিকা
├── Pipfile.lock        # সব প্যাকেজের সঠিক ভার্সন (commit করুন)
├── .venv/              # pipenv এর virtual environment (commit করবেন না)
└── README.md
```

## Setup (pipenv)

প্রজেক্টের সব প্যাকেজ ও ভার্সন `Pipfile` ও `Pipfile.lock` এ ট্র্যাক করা হয়।

| প্যাকেজ | ধরন | কাজ | লক করা ভার্সন |
|---|---|---|---|
| `esptool` | runtime | ফার্মওয়্যার ফ্ল্যাশ ও চিপের তথ্য | 5.6.0 |
| `mpremote` | runtime | বোর্ডে কোড চালানো ও ফাইল কপি | 1.29.0 |
| `micropython-esp32-stubs` | dev | VS Code এ `machine` ওয়ার্নিং দূর করা | 1.29.0.post1 |
| Python | | | 3.15 |

### ১. pipenv ইনস্টল (একবার)

```bash
pip3 install --user pipenv
```

ইনস্টল হয়েছে কি না দেখুন:

```bash
pipenv --version
```

### ২. প্রজেক্ট ক্লোন বা কপি করার পর সব প্যাকেজ ইনস্টল

```bash
cd ~/Desktop/dev/learn_iot
export PIPENV_VENV_IN_PROJECT=1   # virtualenv প্রজেক্টের ভেতর .venv এ রাখে
pipenv install --dev
```

`pipenv install --dev` `Pipfile.lock` এর ভার্সন অনুযায়ী হুবহু একই ভার্সন ইনস্টল করে।

### ৩. টুল চালানোর দুইটা উপায়

```bash
# উপায় ১: শেল চালু করুন, তারপর সরাসরি কমান্ড দিন
pipenv shell
esptool version

# উপায় ২: শেল ছাড়াই একটা কমান্ড চালান
pipenv run esptool version
pipenv run mpremote version
```

এই README এর `esptool ...` ও `mpremote ...` কমান্ডগুলো `pipenv shell` এর ভেতরে অথবা শুরুতে `pipenv run` বসিয়ে চালান।

### নতুন প্যাকেজ যোগ ও ভার্সন ট্র্যাক

```bash
pipenv install <প্যাকেজ>          # runtime প্যাকেজ
pipenv install --dev <প্যাকেজ>    # শুধু ডেভেলপমেন্টের প্যাকেজ
pipenv graph                      # ইনস্টল হওয়া প্যাকেজ ও dependency ট্রি
```

প্যাকেজ বদলালে `Pipfile.lock` নিজে আপডেট হয়। `Pipfile` ও `Pipfile.lock` দুটোই commit করুন।

### ৪. পোর্ট খুঁজুন

ESP32 USB ডেটা ক্যাবলে কানেক্ট করে:

```bash
ls /dev/cu.*
```

আমার বোর্ডের পোর্ট: `/dev/cu.usbserial-59450705951`। নিচের কমান্ডে নিজের পোর্ট বসান।

### ৪.১ বোর্ডের তথ্য দেখা (Device Info)

**চিপের তথ্য** (চিপের ধরন, ফিচার, ক্রিস্টাল ফ্রিকোয়েন্সি, MAC অ্যাড্রেস):

```bash
esptool --port /dev/cu.usbserial-59450705951 chip-id
```

**ফ্ল্যাশ মেমোরির সাইজ ও ধরন:**

```bash
esptool --port /dev/cu.usbserial-59450705951 flash-id
```

**MAC অ্যাড্রেস:**

```bash
esptool --port /dev/cu.usbserial-59450705951 read-mac
```

**সব কানেক্টেড ডিভাইস দেখা** (MicroPython ফ্ল্যাশ করার পর):

```bash
mpremote devs
```

**MicroPython ভার্সন ও বোর্ডের তথ্য** (MicroPython ফ্ল্যাশ করার পর):

```bash
mpremote connect /dev/cu.usbserial-59450705951 exec "import os; print(os.uname())"
```

**বোর্ডের ফাইল তালিকা, ফ্রি মেমোরি ও CPU ফ্রিকোয়েন্সি** (MicroPython ফ্ল্যাশ করার পর):

```bash
mpremote connect /dev/cu.usbserial-59450705951 ls
mpremote connect /dev/cu.usbserial-59450705951 exec "import gc, machine; print('free RAM:', gc.mem_free()); print('CPU Hz:', machine.freq())"
```

`esptool` এর কমান্ডগুলো MicroPython ছাড়াই কাজ করে। `mpremote` এর কমান্ডগুলো কাজ করতে ফার্মওয়্যার লাগে।

### ৫. MicroPython ফার্মওয়্যার ফ্ল্যাশ (একবারই লাগে)

1. https://micropython.org/download/ESP32_GENERIC/ থেকে সর্বশেষ stable `.bin` ডাউনলোড করুন।
2. ফ্ল্যাশ মুছুন (বোর্ডের সব ডেটা মুছে যাবে):
   ```bash
   esptool --port /dev/cu.usbserial-59450705951 erase-flash
   ```
3. ফার্মওয়্যার লিখুন (ফাইলের নাম মেলান):
   ```bash
   esptool --port /dev/cu.usbserial-59450705951 --baud 460800 write-flash 0x1000 ~/Downloads/ESP32_GENERIC-*.bin
   ```
4. পরীক্ষা করুন:
   ```bash
   mpremote connect /dev/cu.usbserial-59450705951 exec "print('hello')"
   ```
   `hello` ছাপা হলে সফল।

### ৬. VS Code ওয়ার্নিং দূর করা

`Import "machine" could not be resolved` ওয়ার্নিং এড়াতে `micropython-esp32-stubs` লাগে। এটা `pipenv install --dev` এ আগেই ইনস্টল হয়ে যায়। VS Code এ শুধু ঠিক interpreter বাছুন:

1. `Cmd + Shift + P`, তারপর `Python: Select Interpreter`
2. `.venv` বেছে নিন
3. `Developer: Reload Window` চালান

## প্রোগ্রাম চালানো

কোড দিনভিত্তিক ফোল্ডারে থাকে: `src/day_01/`, `src/day_02/`, ... প্রতিদিনের প্রোগ্রাম নিজের ফোল্ডারের `main.py` তে লেখা হয়। অন্য দিনের প্রোগ্রাম চালাতে নিচের কমান্ডে `day_01` এর জায়গায় সেই দিনের ফোল্ডারের নাম দিন।

**একবার চালিয়ে দেখা** (বোর্ডে সেভ হয় না, থামাতে `Ctrl + C`):

```bash
mpremote connect /dev/cu.usbserial-59450705951 run src/day_01/main.py
```

**বোর্ডে স্থায়ীভাবে সেভ করা** (পাওয়ার দিলেই নিজে চলবে):

```bash
mpremote connect /dev/cu.usbserial-59450705951 cp src/day_01/main.py :main.py
mpremote connect /dev/cu.usbserial-59450705951 reset
```

**শুধু LED বন্ধ করা:**

```bash
mpremote connect /dev/cu.usbserial-59450705951 exec "from machine import Pin; Pin(2, Pin.OUT).value(0)"
```

## সমস্যা সমাধান

| সমস্যা | সমাধান |
|---|---|
| `could not enter raw repl` | বোর্ডে MicroPython ফ্ল্যাশ করা নেই, Setup ধাপ ৫ করুন |
| পোর্ট দেখা যায় না | চার্জ-অনলি ক্যাবল হতে পারে, ডেটা ক্যাবল ব্যবহার করুন |
| ফ্ল্যাশে `Failed to connect` | BOOT বাটন চেপে ধরে কমান্ড চালান, `Connecting...` এলে ছেড়ে দিন |
| LED জ্বলে না | LED অন্য পিনে থাকতে পারে, `Pin(2, ...)` এর নম্বর বদলে দেখুন |
| `Device busy` | অন্য টার্মিনাল বা এক্সটেনশন পোর্ট ধরে রেখেছে, সেটা বন্ধ করুন |
