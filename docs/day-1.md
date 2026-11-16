# Day 1 — ESP32 প্রথম পরিচয়

তারিখ: 2026-11-16

## আজকের লক্ষ্য

ESP32 বোর্ড USB দিয়ে কানেক্ট করে MicroPython এ LED জ্বালানো-নেভানো (blink) প্রোগ্রাম চালানো।

## আজ যা করা হয়েছে

- ESP32 USB তে কানেক্ট করা হয়েছে, পোর্ট শনাক্ত হয়েছে: `/dev/cu.usbserial-59450705951`
- `esptool chip-id` দিয়ে চিপ শনাক্ত হয়েছে
- `pipenv` দিয়ে প্যাকেজ ম্যানেজমেন্ট শুরু: `esptool` 5.6.0, `mpremote` 1.29.0, dev হিসেবে `micropython-esp32-stubs` 1.29.0.post1
- `Pipfile` ও `Pipfile.lock` এ সব ভার্সন লক করা হয়েছে (Python 3.15)
- LED blink কোড লেখা হয়েছে: `src/day_01/main.py`
- `README.md` ও এই ডক লেখা হয়েছে

## বোর্ডের তথ্য

| বিষয় | মান |
|---|---|
| চিপ | ESP32-D0WD-V3 (revision v3.1) |
| ফিচার | Wi-Fi, Bluetooth, Dual Core, 240MHz |
| Crystal | 40MHz |
| MAC | 5c:01:3b:4a:34:28 |
| USB পোর্ট | `/dev/cu.usbserial-59450705951` |
| অন-বোর্ড LED | GPIO 2 (বোর্ডভেদে আলাদা হতে পারে) |

## আজ যা শিখলাম

- **MicroPython কী:** ESP32 এর মতো ছোট চিপে চলা Python। বোর্ডে আলাদা করে ফার্মওয়্যার ফ্ল্যাশ করতে হয়।
- **pipenv:** `Pipfile` এ দরকারি প্যাকেজ লেখা থাকে, `Pipfile.lock` এ প্রতিটি প্যাকেজের সঠিক ভার্সন লক হয়। ফলে অন্য কম্পিউটারে `pipenv install --dev` চালালে হুবহু একই ভার্সন ইনস্টল হয়।
- **esptool:** বোর্ডের ফ্ল্যাশ মেমোরিতে ফার্মওয়্যার লেখা, মোছা ও চিপের তথ্য দেখার টুল।
- **mpremote:** বোর্ডে কোড চালানো, ফাইল কপি করা ও রিসেট করার টুল।
- **`machine` মডিউল:** MicroPython এর নিজস্ব মডিউল। Mac এ নেই বলে VS Code এ Pylance ওয়ার্নিং দেখায়। এটা আসল এরর নয়। stubs ইনস্টল করলে বা `# type: ignore` দিলে যায়।
- **GPIO:** চিপের পিন। `Pin(2, Pin.OUT)` মানে GPIO 2 কে আউটপুট হিসেবে ব্যবহার করা।

## কোড

`src/day_01/main.py`:

```python
from machine import Pin  # type: ignore
import time

led = Pin(2, Pin.OUT)

while True:
    led.value(1)   # LED জ্বলবে
    time.sleep(1)
    led.value(0)   # LED নিভবে
    time.sleep(1)
```

## সমস্যা ও পর্যবেক্ষণ

- `mpremote` চালাতে গেলে `could not enter raw repl` এরর এসেছে। কারণ বোর্ডে এখনো MicroPython ফার্মওয়্যার ফ্ল্যাশ করা হয়নি।
- Pylance এ `Import "machine" could not be resolved` ওয়ার্নিং এসেছে। সমাধান README তে আছে।

## বাকি কাজ

- [ ] MicroPython ফার্মওয়্যার ফ্ল্যাশ (`erase-flash`, তারপর `write-flash 0x1000`)
- [ ] `mpremote run src/day_01/main.py` দিয়ে LED জ্বলতে দেখা
- [ ] `main.py` বোর্ডে সেভ করে পাওয়ার দিলে নিজে চলে কি না দেখা
- [ ] VS Code এ `.venv` interpreter বেছে Pylance ওয়ার্নিং দূর হয়েছে কি না দেখা

## পরবর্তী (Day 2 ধারণা)

- বাটন দিয়ে LED কন্ট্রোল (GPIO input)
- Wi-Fi তে কানেক্ট করা
- ব্রাউজার থেকে LED অন/অফ করার ছোট ওয়েব সার্ভার
