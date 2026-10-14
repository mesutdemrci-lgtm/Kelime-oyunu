 import json
import os
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.screenmanager import ScreenManager, Screen

DOSYA_ADI = "kelimeler.json"

def kelimeleri_yukle():
    if os.path.exists(DOSYA_ADI):
        with open(DOSYA_ADI, "r", encoding="utf-8") as dosya:
            return json.load(dosya)
    return {}

def kelimeleri_kaydet(kelimeler):
    with open(DOSYA_ADI, "w", encoding="utf-8") as dosya:
        json.dump(kelimeler, dosya, ensure_ascii=False, indent=4)

# Ana Menü Ekranı
class AnaMenu(Screen):
    def __init__(self, **kwargs):
        super(AnaMenu, self).__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=30, spacing=20)
        
        baslik = Label(text='[b]Cep Kelime Havuzu[/b]', markup=True, font_size=28)
        layout.add_widget(baslik)
        
        btn_ekle = Button(text='Yeni Kelime Ekle', font_size=18, background_color=(0.1, 0.6, 0.8, 1))
        btn_ekle.bind(on_press=self.git_ekle)
        layout.add_widget(btn_ekle)
        
        btn_liste = Button(text='Kelimelerimi Listele', font_size=18, background_color=(0.2, 0.7, 0.3, 1))
        btn_liste.bind(on_press=self.git_liste)
        layout.add_widget(btn_liste)
        
        self.add_widget(layout)

    def git_ekle(self, instance):
        self.manager.current = 'ekle'

    def git_liste(self, instance):
        self.manager.current = 'liste'

# Kelime Ekleme Ekranı
class KelimeEkleEkrani(Screen):
    def __init__(self, **kwargs):
        super(KelimeEkleEkrani, self).__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=30, spacing=15)
        
        layout.add_widget(Label(text='İngilizce Kelime:', font_size=16))
        self.ing_input = TextInput(multiline=False, font_size=18)
        layout.add_widget(self.ing_input)
        
        layout.add_widget(Label(text='Türkçe Anlamı:', font_size=16))
        self.tr_input = TextInput(multiline=False, font_size=18)
        layout.add_widget(self.tr_input)
        
        btn_kaydet = Button(text='Kaydet', font_size=18, background_color=(0.1, 0.6, 0.8, 1))
        btn_kaydet.bind(on_press=self.kelimeyi_kaydet)
        layout.add_widget(btn_kaydet)
        
        btn_geri = Button(text='Geri Dön', font_size=18, background_color=(0.8, 0.2, 0.2, 1))
        btn_geri.bind(on_press=self.geri_don)
        layout.add_widget(btn_geri)
        
        self.durum_label = Label(text='', font_size=16)
        layout.add_widget(self.durum_label)
        
        self.add_widget(layout)

    def kelimeyi_kaydet(self, instance):
        ing = self.ing_input.text.strip().lower()
        tr = self.tr_input.text.strip().lower()
        
        if ing and tr:
            kelimeler = kelimeleri_yukle()
            kelimeler[ing] = tr
            kelimeleri_kaydet(kelimeler)
            self.durum_label.text = f"'{ing}' başarıyla eklendi! 🎉"
            self.ing_input.text = ""
            self.tr_input.text = ""
        else:
            self.durum_label.text = "Lütfen alanları boş bırakmayın!"

    def geri_don(self, instance):
        self.manager.current = 'menu'

# Liste Ekranı
class ListeEkrani(Screen):
    def __init__(self, **kwargs):
        super(ListeEkrani, self).__init__(**kwargs)
        self.layout = BoxLayout(orientation='vertical', padding=30, spacing=10)
        
        self.btn_geri = Button(text='Ana Menüye Dön', font_size=18, size_hint_y=None, height=50, background_color=(0.8, 0.2, 0.2, 1))
        self.btn_geri.bind(on_press=self.geri_don)
        self.layout.add_widget(self.btn_geri)
        
        self.add_widget(self.layout)

    def on_enter(self):
        # Ekran açıldığında kelimeleri güncelleyelim
        kelimeler = kelimeleri_yukle()
        # Önceki eklenen dinamik etiketleri temizle (geri dönünce üst üste binmesin)
        if len(self.layout.children) > 1:
            for child in list(self.layout.children[:-1]):
                self.layout.remove_widget(child)
                
        if not kelimeler:
            self.layout.add_widget(Label(text="Henüz kelime eklenmemiş.", font_size=16))
        else:
            for ing, tr in kelimeler.items():
                self.layout.add_widget(Label(text=f"{ing} -> {tr}", font_size=16))

    def geri_don(self, instance):
        self.manager.current = 'menu'

# Ana Uygulama Sınıfı
class KelimeUygulamasi(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(AnaMenu(name='menu'))
        sm.add_widget(KelimeEkrani := KelimeEkleEkrani(name='ekle'))
        sm.add_widget(ListeEkrani(name='liste'))
        return sm

if __name__ == '__main__':
    KelimeUygulamasi().run()