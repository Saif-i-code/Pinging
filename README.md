# 👋 Welcome to PingPro: My Advanced Network Monitor

Hey everyone! **Saif Ali ⚡** here. 
I built this tool because I was tired of the boring, traditional CMD ping screen. I needed something fast, accurate, and visually stunning to monitor my network and test server stability. 

So, I combined the raw power of `icmplib` with the beautiful UI capabilities of `rich` to create the dashboard you see right here!

---

## 💡 Why this tool? (Features)
Honestly, I'm really proud of what this script can do:
* **🖥️ Dual-Panel Dashboard:** Forget the standard command line. This tool gives you a slick split-screen interface (Ping history on one side, and a Live Graph on the other).
* **📊 Live RTT Graph:** This is my favorite feature! The bars rise, fall, and change color (Green, Yellow, Red) based on your real-time ping speed.
* **🚀 Insane Speeds:** Standard ping is locked to 1 second. Here, you can push the interval down to `0.05s` to really stress-test a connection.
* **⚙️ Total Control:** You get to set the rules. You decide the Payload Size, the Timeout limit, and the Ping Interval right when you start the app.

---

## 🛠️ How to run it on your machine?

Because this tool crafts its own packets from scratch using Raw Sockets, **it requires Administrator privileges** to run.

**1. First, install the dependencies:**
```bash
pip install -r requirements.txt
```

**2. Second, run the tool:**
* **If you're on Windows:** Open Command Prompt (CMD) or PowerShell as Administrator and type:
```bash
python Pinging.py
```
* **If you're on Linux/macOS:** 
```bash
sudo python3 Pinging.py
```

---

## 👨‍💻 How to use it?
It's super simple:
1. Run the script.
2. Enter your Target IP or Domain (e.g., `8.8.8.8` or `google.com`).
3. Set your Packet Size, Interval (I recommend `0.5` or `1`), and Timeout.
4. Sit back and monitor your network like a true hacker! 🦈

---
**Final Note:** 
I really hope this tool helps you monitor your servers and network better. If you run into any issues or have cool ideas for new features, let me know! 
And don't forget to drop a ⭐ if you like it.

**~ Saif Ali**
