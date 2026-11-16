# learn_iot — IoT ও রোবটিক্স শেখার প্রজেক্ট

IoT ও রোবটিক্স হাতে-কলমে শেখার প্রজেক্ট। বিভিন্ন কম্পোনেন্ট (LED, বাটন, সেন্সর, মোটর, সার্ভো, ডিসপ্লে ইত্যাদি) নিয়ে প্র্যাকটিস করা হয়, প্রতিদিনের কাজ আলাদা ফোল্ডারে রাখা হয়।

বর্তমানে ব্যবহৃত বোর্ড: **ESP32** (MicroPython)। ভবিষ্যতে অন্য বোর্ড যোগ করা যাবে। আসল বোর্ড ছাড়াও **Wokwi সিমুলেটরে** (ওয়েব বা VS Code এ) কোড পরীক্ষা করা যায়: [সিমুলেটরে টেস্ট](#সিমুলেটরে-টেস্ট-vs-code-এ-wokwi)।

- দৈনিক নোট: [docs/day-1.md](docs/day-1.md)
- কম্পোনেন্ট প্র্যাকটিস তালিকা: [docs/components.md](docs/components.md)
- প্রজেক্ট আইডিয়া (যেমন ওয়াটার ট্যাংক + পাম্প + সার্ভার + মোবাইল অ্যাপ): [docs/projects.md](docs/projects.md)

## প্রজেক্ট স্ট্রাকচার

```
learn_iot/
├── docs/
│   ├── components.md   # কম্পোনেন্ট প্র্যাকটিস তালিকা ও অগ্রগতি
│   ├── projects.md     # বড় প্রজেক্টের আইডিয়া ও পরিকল্পনা
│   └── day-1.md        # Day 1 নোট
├── src/
│   ├── day_01/
│   │   └── main.py     # Day 1: LED blink
│   ├── day_02/         # (পরে) প্রতিদিনের জন্য নতুন ফোল্ডার
│   └── projects/       # (পরে) বড় প্রজেক্ট, যেমন water_tank/
├── simulator/
│   └── esp32/          # Wokwi সিমুলেটরের ফাইল (wokwi.toml, diagram.json)
├── Pipfile             # প্রজেক্টের প্যাকেজ তালিকা
├── Pipfile.lock        # সব প্যাকেজের সঠিক ভার্সন (commit করুন)
├── .venv/              # pipenv এর virtual environment (commit করবেন না)
└── README.md
```

## প্রতিদিনের নিয়ম

1. `src/day_XX/` ফোল্ডার বানান, ভেতরে `main.py` লিখুন।
2. কোন কম্পোনেন্ট, কোন পিনে লাগিয়েছেন তা `docs/day-X.md` এ লিখে রাখুন (ওয়্যারিং, শেখা বিষয়, সমস্যা)।
3. `docs/components.md` এ কম্পোনেন্ট টিক দিন।
4. commit ও push করুন।

কম্পোনেন্ট শেখা হলে `docs/projects.md` থেকে একটা প্রজেক্ট বেছে `src/projects/<নাম>/` এ বানান।

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

## সিমুলেটরে টেস্ট (VS Code এ Wokwi)

### ওয়েবে দ্রুত চেষ্টা

https://wokwi.com এ নতুন প্রজেক্টে **ESP32 → MicroPython** টেমপ্লেট বেছে `src/day_01/main.py` এর কোড `main.py` তে বসিয়ে ▶ চাপুন। LED লাগাতে হবে **ডান পাশের `2` লেখা পিনে** (GPIO 2), রেজিস্টর (220Ω) দিয়ে, আর অন্য পা `GND` তে। বাঁ পাশের `D2` আসলে GPIO 9, ওটা ব্যবহার করবেন না।

### VS Code এ চালানো

আসল বোর্ড ছাড়াই VS Code এর ভেতরে ESP32 চালানো যায়। সিমুলেটরের ফাইল `simulator/esp32/` এ আছে (`wokwi.toml`, `diagram.json`, MicroPython ফার্মওয়্যার)। `diagram.json` এ ESP32, LED ও 220Ω রেজিস্টর GPIO 2 তে জোড়া আছে।

### একবারের সেটআপ

1. VS Code এ **Wokwi for VS Code** এক্সটেনশন ইনস্টল করুন।
2. `F1` চেপে **Wokwi: Request a new License** চালান। ব্রাউজারে ফ্রি লাইসেন্স নিয়ে VS Code এ নিশ্চিত করুন।
3. ফার্মওয়্যার না থাকলে (এটা git এ নেই) ডাউনলোড করুন:
   ```bash
   curl -L -o simulator/esp32/ESP32_GENERIC-20260824-v1.29.0.bin \
     https://github.com/wokwi/wokwi-vscode-micropython/raw/main/esp32/ESP32_GENERIC-20260824-v1.29.0.bin
   ```
4. ফার্মওয়্যারের ভার্সন (1.29.0) ও `mpremote` এর ভার্সন (1.29.0) মেলানো আছে। `pipenv install --dev` করলেই হবে।

### প্রতিবার চালানোর নিয়ম (পরীক্ষিত, কাজ করছে)

1. VS Code এ `simulator/esp32/diagram.json` খুলুন।
2. ▶ **Start Simulation** চাপুন (অথবা `F1` → **Wokwi: Start Simulator**)। কয়েক সেকেন্ড অপেক্ষা করুন, কনসোলে `>>>` আসা পর্যন্ত।
3. **নতুন টার্মিনাল** খুলে প্রজেক্ট ফোল্ডারে কোড চালান:
   ```bash
   mpremote connect port:rfc2217://localhost:4000 run src/day_01/main.py
   ```
   (`(.venv)` সক্রিয় না থাকলে শুরুতে `pipenv run` বসান।)
4. LED জ্বলবে-নিভবে। থামাতে টার্মিনালে `Ctrl + C`।

`run` কমান্ড কোড সেভ না করে সরাসরি চালায়, তাই রিসেট নিয়ে ঝামেলা নেই। কোড বদলালে `Ctrl + C` চেপে ৩ নম্বর কমান্ড আবার চালান। অন্য দিনের কোড চালাতে `day_01` এর জায়গায় সেই ফোল্ডারের নাম দিন।

### বিকল্প: কোড বোর্ডে সেভ করে চালানো

```bash
mpremote connect port:rfc2217://localhost:4000 fs cp src/day_01/main.py :main.py
```

তারপর **Stop বা Start না চেপে** সিমুলেটর কনসোলে ক্লিক করে শুধু **Ctrl + D** চাপুন।

> ⚠️ আপলোডের পর সিমুলেশন Stop বা Start করলে সিমুলেটরের ফ্ল্যাশ নতুন হয়ে যায় (`Performing initial setup` দেখা যায়) এবং সেভ করা `main.py` মুছে যায়। এজন্য সাধারণত `run` কমান্ডই ভালো।

### সমস্যা হলে

| সমস্যা | সমাধান |
|---|---|
| `could not enter raw repl` | সিমুলেটর বুট শেষ হওয়ার জন্য ১০ সেকেন্ড অপেক্ষা করে আবার চালান |
| পোর্ট 4000 ব্যস্ত বা `failed to connect` | সিমুলেটর চালু আছে কি না দেখুন, অন্য প্রোগ্রাম পোর্ট ধরে থাকলে বন্ধ করুন |
| `OSError: [Errno 2] ENOENT` (`fs cp` এর সময়) | স্বাভাবিক, `mpremote` ফাইল আছে কি না দেখছে। এরর নয় |
| `Courtesy Notice` (pipenv) | সতর্কবার্তা মাত্র। `(.venv)` সক্রিয় থাকলে `pipenv run` ছাড়াই `mpremote` চালান |
| আপলোডের পর কনসোলে শুধু `>>>`, কিছু চলে না | সিমুলেশন রিস্টার্ট হয়ে ফাইল মুছে গেছে। `run` কমান্ড ব্যবহার করুন |
| কোড চলছে কিন্তু LED জ্বলে না | তার যাচাই করুন: GPIO 2 → রেজিস্টর → LED anode, LED cathode → `GND` |

## সমস্যা সমাধান

| সমস্যা | সমাধান |
|---|---|
| `could not enter raw repl` | বোর্ডে MicroPython ফ্ল্যাশ করা নেই, Setup ধাপ ৫ করুন |
| পোর্ট দেখা যায় না | চার্জ-অনলি ক্যাবল হতে পারে, ডেটা ক্যাবল ব্যবহার করুন |
| ফ্ল্যাশে `Failed to connect` | BOOT বাটন চেপে ধরে কমান্ড চালান, `Connecting...` এলে ছেড়ে দিন |
| LED জ্বলে না | LED অন্য পিনে থাকতে পারে, `Pin(2, ...)` এর নম্বর বদলে দেখুন |
| `Device busy` | অন্য টার্মিনাল বা এক্সটেনশন পোর্ট ধরে রেখেছে, সেটা বন্ধ করুন |
