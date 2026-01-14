import os
import threading
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.popup import Popup
from kivy.clock import Clock

# yt_dlp লাইব্রেরি ইম্পোর্ট করতে হবে
import yt_dlp

# Download folder setup
DOWNLOAD_DIR = "/storage/emulated/0/Download/KRF"
if not os.path.exists(DOWNLOAD_DIR):
    try:
        os.makedirs(DOWNLOAD_DIR)
    except PermissionError:
        pass # Pydroid-এ মাঝে মাঝে পারমিশন অটো নেয়

class MainUI(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation="vertical", padding=20, spacing=15, **kwargs)

        # Title
        self.add_widget(Label(
            text="[b]K.R.F Downloader[/b]",
            markup=True,
            font_size=28,
            color=(0, 1, 1, 1) # Cyan color added for hacking look
        ))

        self.add_widget(Label(
            text="YouTube | Facebook | Instagram",
            font_size=14,
            color=(0.7, 0.7, 0.7, 1)
        ))

        # URL Input
        self.url_input = TextInput(
            hint_text="ভিডিও URL পেস্ট করুন...",
            multiline=False,
            size_hint_y=None,
            height=50,
            background_color=(0.2, 0.2, 0.2, 1),
            foreground_color=(1, 1, 1, 1)
        )
        self.add_widget(self.url_input)

        # Status
        self.status = Label(text="Ready to download", color=(1, 1, 0, 1))
        self.add_widget(self.status)

        # Download Button
        download_btn = Button(
            text="Download Video",
            size_hint_y=None,
            height=50,
            background_color=(0, 0.5, 1, 1)
        )
        download_btn.bind(on_press=self.start_download)
        self.add_widget(download_btn)

        # Disclaimer Button
        disclaimer_btn = Button(
            text="Disclaimer",
            size_hint_y=None,
            height=40,
            background_color=(1, 0, 0, 0.5)
        )
        disclaimer_btn.bind(on_press=self.show_disclaimer)
        self.add_widget(disclaimer_btn)

        # Footer
        self.add_widget(Label(
            text="© K.R.F Technology\nPersonal & Educational Use Only",
            font_size=12,
            color=(0.5, 0.5, 0.5, 1)
        ))

    def show_disclaimer(self, instance):
        text = (
            "⚠️ DISCLAIMER\n\n"
            "This application is made for personal and educational use only.\n\n"
            "Downloading copyrighted content without permission is illegal.\n"
            "The developer is not responsible for misuse of this app."
        )
        content = BoxLayout(orientation="vertical", padding=10)
        
        # Label text wrapping fix
        lbl = Label(text=text, size_hint_y=None)
        lbl.bind(texture_size=lambda instance, value: setattr(instance, 'height', value[1]))
        lbl.bind(width=lambda instance, value: setattr(instance, 'text_size', (value, None)))
        
        scroll = ScrollView()
        scroll.add_widget(lbl)
        
        content.add_widget(scroll)
        close_btn = Button(text="OK", size_hint_y=None, height=40)
        content.add_widget(close_btn)

        popup = Popup(
            title="K.R.F Security Notice",
            content=content,
            size_hint=(0.9, 0.5)
        )
        close_btn.bind(on_press=popup.dismiss)
        popup.open()

    def start_download(self, instance):
        url = self.url_input.text.strip()
        if not url:
            self.status.text = "❌ দয়া করে URL দিন"
            return

        self.status.text = "⏳ প্রসেসিং হচ্ছে... দয়া করে অপেক্ষা করুন"
        # থ্রেড ব্যবহার করা যাতে অ্যাপ হ্যাং না হয়
        threading.Thread(target=self.download_video, args=(url,), daemon=True).start()

    def download_video(self, url):
        try:
            # yt-dlp অপশন সেটআপ
            ydl_opts = {
                'outtmpl': f'{DOWNLOAD_DIR}/%(title)s.%(ext)s',
                'format': 'best[ext=mp4]/best',
                'noplaylist': True,
            }
            
            # লাইব্রেরি দিয়ে ডাউনলোড করা
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                title = info.get('title', 'Video')
            
            # UI আপডেট (Clock দিয়ে মেইন থ্রেডে পাঠানো নিরাপদ)
            Clock.schedule_once(lambda dt: self.update_status(f"✅ Downloaded: {title[:15]}..."))
            
        except Exception as e:
            Clock.schedule_once(lambda dt: self.update_status("❌ ডাউনলোড ব্যর্থ হয়েছে!"))
            print(e) # ডিবাগিংয়ের জন্য

    def update_status(self, text):
        self.status.text = text

class KRFDownloaderApp(App):
    def build(self):
        self.title = "K.R.F Downloader"
        return MainUI()

if __name__ == "__main__":
    KRFDownloaderApp().run()
