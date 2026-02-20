# -*- coding: utf-8 -*-
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.spinner import Spinner
from kivy.uix.scrollview import ScrollView
import pandas as pd
from datetime import datetime

kayitlar = []

KONUMLAR = [
    'MAIN DECK (MD)',
    'ACCESS WORKS',
    'SUPERSTRUCTURE (SS)',
    'ENGINE ROOM (ER)',
    'AFT PEAK (AP)',
    'PUMP ROOM (PR)',
    'TANKS (TK)',
    'CARGO HOLDS (CH)',
    'FORE PEAK (FP)',
    'DOUBLE BOTTOM',
    'SIDE TANK (TK)',
    'SHELL (SH)',
    'HATCH COVERS (HCV)',
    'HATCH COAMING (HCM)',
    'CROSS DECK (CD)',
    'LASHING BRIDGE (LB)',
    'FUNNEL (FN)',
    'BULWARK (BW)',
    'DECK HOUSE (DH)',
    'DUCT KEEL (DK)',
    'FOUNDATION (FD)',
    'OTHER (OT)'
]

TYPICAL_TYPES = [
    # --- Angle Bar ---
    'ANGLE BAR (30x30-50x50)',
    'ANGLE BAR (60x60-90x90)',
    'ANGLE BAR (100x100)',
    # --- Flat Bar ---
    'FLAT BAR (20x20-100x100)',
    'FLAT BAR (101x101-150x150)',
    'SS FLAT BAR FOR BRAKE PAD',
    # --- Plate ---
    'PLATE',
    'AL. ALLOY PLATE',
    'PLATE BAR',
    # --- Structural ---
    'STRUCTURAL PROFILE (NPI, NPU, HEA, etc.)',
    'SOLID BAR (up to 40mm)',
    # --- Pipe / Handrail / Cable / Duct ---
    'HANDRAIL PIPE (up to DN50)',
    'HANDRAIL SET',
    'CABLE WAY',
    'MUSHROOM/VENT DUCT R/R',
    # --- Ladder / Step ---
    'VERTICAL LADDER SET',
    'VERTICAL LADDER BACK PROTECTION SET',
    'ACC. LADDER R/R',
    'ACC. LADDER PLATFORM R/R',
    'ACC. LADDER ROLLER R/R',
    'STAIR STEP RENEWAL',
    'ALUMINIUM LADDER STEP RENEWAL',
    'ALUMINIUM LADDER STEP RENEWAL - BENDED',
    'ALUMINIUM LADDER WELDING REPAIR',
    'PILOT LADDER MOD.',
    # --- Bolt / Fastener / Stud ---
    'U-BOLT RENEWAL',
    'MANHOLE STUD RENEWAL',
    'MANHOLE STUD RENEWALKILAVUZLU-THREADED',
    # --- Cover / Manhole / Gasket ---
    'MANHOLE COVER FABRICATION',
    'MANHOLE COVER R/R',
    'MANHOLE RENEWAL WITH FLANGE',
    'MANHOLE GASKET',
    'SKYLIGHT MANHOLE COVER R/R',
    'TEFLON GASKET',
    'SOUNDING CAP RENEWAL',
    # --- Grating ---
    'DECK GRATING R/R',
    'ENGINE ROOM GRATING R/R',
    'THRUSTER GRATING FABRICATION',
    # --- Door / Cover / Hatch ---
    'STEEL DOOR R/R',
    'CARGO TANK COVER R/R',
    'HATCH COVER PROTECTION - SET',
    # --- Anode ---
    'BALLAST TANK ANODE RENEWAL (BOLT TYPE)',
    'BALLAST TANK ANODE RENEWAL (WELDED TYPE)',
    # --- Clamp / Guard / Eye / Pad ---
    'HYDRAULIC CLAMP',
    'CABLE CLAMP',
    'ROPE GUARD SET',
    'PAD EYE > 10ton',
    'RESTING PAD RENEWAL',
    # --- Lashing / Socket / Cone / Bend ---
    'SINGLE SOCKET RENEWAL',
    'DOUBLE SOCKET RENEWAL',
    'SINGLE LASHING RENEWAL',
    'DOUBLE LASHING RENEWAL',
    'CONE RENEWAL',
    'BEND',
    # --- Hinge / Handle ---
    'HINGE',
    'HANDLE RENEWAL',
    # --- Penetration ---
    'PENETRATION DECK/BULKHEAD (<=DN100)',
    'PENETRATION DECK/BULKHEAD (>DN100)',
    # --- Spark Arrestor ---
    'SPARK ARRESTOR (up to f <=500mm)',
    'SPARK ARRESTOR (up to f >500mm)',
    # --- Marking ---
    'HULL MARK LETTERS',
    'PLIMSOLL MARK - PER SIDE',
    'SHIP NAME LETTERS',
    # --- BWTS ---
    'TRANSFERRING OF BWTS EQUIPMENT - BIG SIZE',
    'TRANSFERRING OF BWTS EQUIPMENT - SMALL SIZE',
    # --- Diğer ---
    'HOLE DRILLING',
    'WELDING REPAIR',
    'SEACHEST FILTER FABRICATION',
    'MOBILIZATION',
]

ZONE_ESLESTIRME = {
    'AFT PEAK (AP)':       'ENCLOSED',
    'ENGINE ROOM (ER)':    'ENCLOSED',
    'PUMP ROOM (PR)':      'ENCLOSED',
    'TANKS (TK)':          'ENCLOSED',
    'CARGO HOLDS (CH)':    'OPEN',
    'FORE PEAK (FP)':      'ENCLOSED',
    'DOUBLE BOTTOM':       'ENCLOSED',
    'SIDE TANK (TK)':      'ENCLOSED',
    'MAIN DECK (MD)':      'OPEN',
    'SHELL (SH)':          'OPEN',
    'HATCH COVERS (HCV)':  'OPEN',
    'HATCH COAMING (HCM)': 'OPEN',
    'CROSS DECK (CD)':     'OPEN',
    'LASHING BRIDGE (LB)': 'OPEN',
    'SUPERSTRUCTURE (SS)': 'OPEN',
    'FUNNEL (FN)':         'OPEN',
    'BULWARK (BW)':        'OPEN',
    'DECK HOUSE (DH)':     'OPEN',
    'DUCT KEEL (DK)':      'ENCLOSED',
    'FOUNDATION (FD)':     'OPEN',
    'OTHER (OT)':          'OPEN',
    'ACCESS WORKS':        'OPEN',
}

# Kısayollar
# type_detail, uzunluk, breadth, thickness, spc_profile
Q    = {'type_detail': False, 'uzunluk': False, 'breadth': False, 'thickness': False, 'spc_profile': False}
QL   = {**Q, 'uzunluk': True}
QTL  = {**Q, 'type_detail': True, 'uzunluk': True}
QT   = {**Q, 'type_detail': True}

ALAN_KURALLARI = {
    # Angle Bar
    'ANGLE BAR (30x30-50x50)':                     QL,
    'ANGLE BAR (60x60-90x90)':                     QL,
    'ANGLE BAR (100x100)':                         QL,
    # Flat Bar
    'FLAT BAR (20x20-100x100)':                    QTL,
    'FLAT BAR (101x101-150x150)':                  QTL,
    'SS FLAT BAR FOR BRAKE PAD':                   QL,
    # Plate
    'PLATE':                    {**Q, 'uzunluk': True, 'breadth': True, 'thickness': True},
    'AL. ALLOY PLATE':                             Q,
    'PLATE BAR':                                   Q,
    # Structural
    'STRUCTURAL PROFILE (NPI, NPU, HEA, etc.)':
        {'type_detail': True, 'uzunluk': True, 'breadth': True, 'thickness': True, 'spc_profile': True},
    'SOLID BAR (up to 40mm)':                      QTL,
    # Pipe / Handrail / Cable / Duct
    'HANDRAIL PIPE (up to DN50)':                  QTL,
    'HANDRAIL SET':                                QL,
    'CABLE WAY':                                   QTL,
    'MUSHROOM/VENT DUCT R/R':                      QL,
    # Ladder / Step
    'VERTICAL LADDER SET':                         QL,
    'VERTICAL LADDER BACK PROTECTION SET':         QL,
    'ACC. LADDER R/R':                             Q,
    'ACC. LADDER PLATFORM R/R':                    Q,
    'ACC. LADDER ROLLER R/R':                      Q,
    'STAIR STEP RENEWAL':                          Q,
    'ALUMINIUM LADDER STEP RENEWAL':               Q,
    'ALUMINIUM LADDER STEP RENEWAL - BENDED':      Q,
    'ALUMINIUM LADDER WELDING REPAIR':             Q,
    'PILOT LADDER MOD.':                           Q,
    # Bolt / Fastener
    'U-BOLT RENEWAL':                              QT,
    'MANHOLE STUD RENEWAL':                        Q,
    'MANHOLE STUD RENEWALKILAVUZLU-THREADED':      Q,
    # Cover / Manhole / Gasket
    'MANHOLE COVER FABRICATION':                   Q,
    'MANHOLE COVER R/R':                           Q,
    'MANHOLE RENEWAL WITH FLANGE':                 Q,
    'MANHOLE GASKET':                              Q,
    'SKYLIGHT MANHOLE COVER R/R':                  Q,
    'TEFLON GASKET':                               Q,
    'SOUNDING CAP RENEWAL':                        Q,
    # Grating
    'DECK GRATING R/R':                            Q,
    'ENGINE ROOM GRATING R/R':                     Q,
    'THRUSTER GRATING FABRICATION':                Q,
    # Door / Cover / Hatch
    'STEEL DOOR R/R':                              Q,
    'CARGO TANK COVER R/R':                        Q,
    'HATCH COVER PROTECTION - SET':                Q,
    # Anode
    'BALLAST TANK ANODE RENEWAL (BOLT TYPE)':      Q,
    'BALLAST TANK ANODE RENEWAL (WELDED TYPE)':    Q,
    # Clamp / Guard / Eye / Pad
    'HYDRAULIC CLAMP':                             QT,
    'CABLE CLAMP':                                 Q,
    'ROPE GUARD SET':                              Q,
    'PAD EYE > 10ton':                             Q,
    'RESTING PAD RENEWAL':                         Q,
    # Lashing / Socket / Cone / Bend
    'SINGLE SOCKET RENEWAL':                       Q,
    'DOUBLE SOCKET RENEWAL':                       Q,
    'SINGLE LASHING RENEWAL':                      Q,
    'DOUBLE LASHING RENEWAL':                      Q,
    'CONE RENEWAL':                                Q,
    'BEND':                                        Q,
    # Hinge / Handle
    'HINGE':                                       Q,
    'HANDLE RENEWAL':                              Q,
    # Penetration
    'PENETRATION DECK/BULKHEAD (<=DN100)':         Q,
    'PENETRATION DECK/BULKHEAD (>DN100)':          Q,
    # Spark Arrestor
    'SPARK ARRESTOR (up to f <=500mm)':            Q,
    'SPARK ARRESTOR (up to f >500mm)':             Q,
    # Marking
    'HULL MARK LETTERS':                           Q,
    'PLIMSOLL MARK - PER SIDE':                    Q,
    'SHIP NAME LETTERS':                           Q,
    # BWTS
    'TRANSFERRING OF BWTS EQUIPMENT - BIG SIZE':   Q,
    'TRANSFERRING OF BWTS EQUIPMENT - SMALL SIZE': Q,
    # Diğer
    'HOLE DRILLING':                               Q,
    'WELDING REPAIR':                              Q,
    'SEACHEST FILTER FABRICATION':                 Q,
    'MOBILIZATION':                                Q,
}


class TechizForm(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = 20
        self.spacing = 8

        # Konum
        self.add_widget(Label(text='Konum/Bölge:', size_hint_y=0.07))
        self.konum_spinner = Spinner(
            text='MAIN DECK (MD)',
            values=KONUMLAR,
            size_hint_y=0.09
        )
        self.add_widget(self.konum_spinner)

        # Typical Type
        self.add_widget(Label(text='Typical Type:', size_hint_y=0.07))
        self.type_spinner = Spinner(
            text='ANGLE BAR (30x30-50x50)',
            values=TYPICAL_TYPES,
            size_hint_y=0.09
        )
        self.type_spinner.bind(text=self.on_type_degisti)
        self.add_widget(self.type_spinner)

        # Description / Part ID
        self.add_widget(Label(text='Description / Part ID:', size_hint_y=0.07))
        self.description_input = TextInput(
            hint_text='Örn: KÖŞEBENT YENİLEME (50x50)',
            multiline=False,
            size_hint_y=0.09
        )
        self.add_widget(self.description_input)

        # --- Dinamik widget'lar ---
        self.type_detail_label = Label(text='Type Detail:', size_hint_y=None, height=34)
        self.type_detail_input = TextInput(
            hint_text='Örn: M20x200, HEA200, DN32...',
            multiline=False, size_hint_y=None, height=44)

        self.uzunluk_label = Label(text='Uzunluk / Length (mm):', size_hint_y=None, height=34)
        self.uzunluk_input = TextInput(
            hint_text='Örn: 700',
            multiline=False, size_hint_y=None, height=44)

        self.breadth_label = Label(text='Breadth (mm):', size_hint_y=None, height=34)
        self.breadth_input = TextInput(
            hint_text='Örn: 400',
            multiline=False, size_hint_y=None, height=44)

        self.thickness_label = Label(text='Thickness / Thk (mm):', size_hint_y=None, height=34)
        self.thickness_input = TextInput(
            hint_text='Örn: 8',
            multiline=False, size_hint_y=None, height=44)

        self.spc_label = Label(text='Spc. Profile (KG/M):', size_hint_y=None, height=34)
        self.spc_input = TextInput(
            hint_text='Örn: 26.2',
            multiline=False, size_hint_y=None, height=44)

        self.adet_label = Label(text='Adet (Quantity):', size_hint_y=None, height=34)
        self.adet_input = TextInput(
            hint_text='Örn: 3',
            multiline=False, size_hint_y=None, height=44)

        self.not_label = Label(text='Not (opsiyonel):', size_hint_y=None, height=34)
        self.not_input = TextInput(
            hint_text='Ekstra bilgi...',
            multiline=True, size_hint_y=None, height=75)

        # Dinamik alan container
        self.dinamik_alan = BoxLayout(
            orientation='vertical',
            size_hint_y=None,
            spacing=6
        )
        self.dinamik_alan.bind(minimum_height=self.dinamik_alan.setter('height'))
        self.add_widget(self.dinamik_alan)

        self._formu_guncelle('ANGLE BAR (30x30-50x50)')

        # Butonlar - Satır 1
        buton_layout1 = BoxLayout(size_hint_y=0.1, spacing=10)
        kaydet_btn = Button(text='Kaydet')
        kaydet_btn.bind(on_press=self.kaydet)
        buton_layout1.add_widget(kaydet_btn)
        listele_btn = Button(text='Kayıtları Listele')
        listele_btn.bind(on_press=self.kayitlari_goster)
        buton_layout1.add_widget(listele_btn)
        self.add_widget(buton_layout1)

        # Butonlar - Satır 2
        buton_layout2 = BoxLayout(size_hint_y=0.1, spacing=10)
        excel_btn = Button(text="Excel'e Aktar", background_color=(0.2, 0.8, 0.2, 1))
        excel_btn.bind(on_press=self.excel_aktar)
        buton_layout2.add_widget(excel_btn)
        temizle_btn = Button(text='Tümünü Temizle', background_color=(0.8, 0.2, 0.2, 1))
        temizle_btn.bind(on_press=self.tumunu_temizle)
        buton_layout2.add_widget(temizle_btn)
        self.add_widget(buton_layout2)

        # Sonuç alanı
        scroll = ScrollView(size_hint_y=0.22)
        self.sonuc_label = Label(text='', size_hint_y=None)
        self.sonuc_label.bind(texture_size=self.sonuc_label.setter('size'))
        scroll.add_widget(self.sonuc_label)
        self.add_widget(scroll)

    def on_type_degisti(self, spinner, yeni_deger):
        self._formu_guncelle(yeni_deger)

    def _formu_guncelle(self, tip):
        k = ALAN_KURALLARI.get(tip, Q)
        alan = self.dinamik_alan
        alan.clear_widgets()

        if k.get('type_detail'):
            alan.add_widget(self.type_detail_label)
            alan.add_widget(self.type_detail_input)
        if k.get('uzunluk'):
            alan.add_widget(self.uzunluk_label)
            alan.add_widget(self.uzunluk_input)
        if k.get('breadth'):
            alan.add_widget(self.breadth_label)
            alan.add_widget(self.breadth_input)
        if k.get('thickness'):
            alan.add_widget(self.thickness_label)
            alan.add_widget(self.thickness_input)
        if k.get('spc_profile'):
            alan.add_widget(self.spc_label)
            alan.add_widget(self.spc_input)

        # Quantity ve Not her zaman
        alan.add_widget(self.adet_label)
        alan.add_widget(self.adet_input)
        alan.add_widget(self.not_label)
        alan.add_widget(self.not_input)

    def kaydet(self, instance):
        tip = self.type_spinner.text
        k = ALAN_KURALLARI.get(tip, Q)

        if not self.description_input.text.strip():
            self.sonuc_label.text = '⚠ Lütfen Description / Part ID girin!'
            return

        type_detail_val = ''
        if k.get('type_detail'):
            if not self.type_detail_input.text.strip():
                self.sonuc_label.text = '⚠ Lütfen Type Detail girin!'
                return
            type_detail_val = self.type_detail_input.text.strip()

        uzunluk_val = ''
        if k.get('uzunluk'):
            if not self.uzunluk_input.text.strip():
                self.sonuc_label.text = '⚠ Lütfen uzunluk girin!'
                return
            try:
                uzunluk_val = int(self.uzunluk_input.text.strip())
                if uzunluk_val <= 0:
                    raise ValueError
            except ValueError:
                self.sonuc_label.text = '⚠ Uzunluk geçerli bir sayı olmalıdır!'
                return

        breadth_val = ''
        if k.get('breadth'):
            if not self.breadth_input.text.strip():
                self.sonuc_label.text = '⚠ Lütfen breadth girin!'
                return
            try:
                breadth_val = int(self.breadth_input.text.strip())
                if breadth_val <= 0:
                    raise ValueError
            except ValueError:
                self.sonuc_label.text = '⚠ Breadth geçerli bir sayı olmalıdır!'
                return

        thickness_val = ''
        if k.get('thickness'):
            if not self.thickness_input.text.strip():
                self.sonuc_label.text = '⚠ Lütfen thickness girin!'
                return
            try:
                thickness_val = int(self.thickness_input.text.strip())
                if thickness_val <= 0:
                    raise ValueError
            except ValueError:
                self.sonuc_label.text = '⚠ Thickness geçerli bir sayı olmalıdır!'
                return

        spc_val = ''
        if k.get('spc_profile'):
            if not self.spc_input.text.strip():
                self.sonuc_label.text = '⚠ Lütfen Spc. Profile (KG/M) girin!'
                return
            try:
                spc_val = float(self.spc_input.text.strip().replace(',', '.'))
                if spc_val <= 0:
                    raise ValueError
            except ValueError:
                self.sonuc_label.text = '⚠ Spc. Profile geçerli bir sayı olmalıdır!'
                return

        if not self.adet_input.text.strip():
            self.sonuc_label.text = '⚠ Lütfen adet girin!'
            return
        try:
            adet = int(self.adet_input.text.strip())
            if adet <= 0:
                raise ValueError
        except ValueError:
            self.sonuc_label.text = '⚠ Adet geçerli bir sayı olmalıdır!'
            return

        konum    = self.konum_spinner.text
        is_cinsi = self.description_input.text.strip()
        not_text = self.not_input.text.strip()
        zone     = ZONE_ESLESTIRME.get(konum, 'OPEN')

        kayit = {
            'zone':        zone,
            'location':    konum,
            'is_cinsi':    is_cinsi,
            'tip':         tip,
            'type_detail': type_detail_val,
            'uzunluk':     uzunluk_val,
            'breadth':     breadth_val,
            'thickness':   thickness_val,
            'spc_profile': spc_val,
            'adet':        adet,
            'not':         not_text,
        }
        kayitlar.append(kayit)

        # Formu sıfırla
        self.konum_spinner.text     = 'MAIN DECK (MD)'
        self.type_spinner.text      = 'ANGLE BAR (30x30-50x50)'
        self.description_input.text = ''
        self.type_detail_input.text = ''
        self.uzunluk_input.text     = ''
        self.breadth_input.text     = ''
        self.thickness_input.text   = ''
        self.spc_input.text         = ''
        self.adet_input.text        = ''
        self.not_input.text         = ''

        ozet = (
            f'✓ Kayıt #{len(kayitlar)} eklendi!\n'
            f'{zone} | {konum}\n'
            f'{tip}\n'
            f'{is_cinsi}\n'
        )
        detaylar = []
        if type_detail_val: detaylar.append(f'Detail: {type_detail_val}')
        if uzunluk_val:     detaylar.append(f'L:{uzunluk_val}mm')
        if breadth_val:     detaylar.append(f'B:{breadth_val}mm')
        if thickness_val:   detaylar.append(f'T:{thickness_val}mm')
        if spc_val:         detaylar.append(f'Spc:{spc_val}kg/m')
        detaylar.append(f'Qty:{adet}')
        ozet += ' | '.join(detaylar)
        self.sonuc_label.text = ozet

    def kayitlari_goster(self, instance):
        if not kayitlar:
            self.sonuc_label.text = 'Henüz kayıt yok!'
            return

        liste_text = f'Toplam {len(kayitlar)} kayıt:\n{"=" * 32}\n\n'
        for i, k in enumerate(kayitlar, 1):
            satir = (
                f"#{i} - [{k['zone']}] {k['location']}\n"
                f"{k['tip']}\n"
            )
            if k['type_detail']: satir += f"Detail: {k['type_detail']}\n"
            satir += f"{k['is_cinsi']}\n"
            dims = []
            if k['uzunluk']:     dims.append(f"L:{k['uzunluk']}mm")
            if k['breadth']:     dims.append(f"B:{k['breadth']}mm")
            if k['thickness']:   dims.append(f"T:{k['thickness']}mm")
            if k['spc_profile']: dims.append(f"Spc:{k['spc_profile']}kg/m")
            dims.append(f"Qty:{k['adet']}")
            satir += ' | '.join(dims) + f"\n{'-' * 32}\n"
            liste_text += satir

        self.sonuc_label.text = liste_text

    def excel_aktar(self, instance):
        if not kayitlar:
            self.sonuc_label.text = "Excel'e aktarılacak kayıt yok!"
            return

        df = pd.DataFrame({
            'ZONE':                  [k['zone']        for k in kayitlar],
            'LOCATION':              [k['location']    for k in kayitlar],
            'DESCRIPTION / PART ID': [k['is_cinsi']    for k in kayitlar],
            'Typical Type':          [k['tip']         for k in kayitlar],
            'Type Detail':           [k['type_detail'] for k in kayitlar],
            'Grade':                 [''               for _ in kayitlar],
            'Length':                [k['uzunluk']     for k in kayitlar],
            'Breadth':               [k['breadth']     for k in kayitlar],
            'Thk':                   [k['thickness']   for k in kayitlar],
            'Quantity':              [k['adet']        for k in kayitlar],
            'Total Length':          [''               for _ in kayitlar],
            'Weight':                [''               for _ in kayitlar],
            'Subcontractor':         [''               for _ in kayitlar],
            'Spc.profile (KG/M)':    [k['spc_profile'] for k in kayitlar],
            'Price':                 [''               for _ in kayitlar],
            'Weight 2':              [''               for _ in kayitlar],
            'Additionally':          [k['not']         for k in kayitlar],
        })

        tarih = datetime.now().strftime('%Y%m%d_%H%M%S')
        dosya_adi = f'gemi_techiz_{tarih}.xlsx'
        df.to_excel(dosya_adi, index=False)

        self.sonuc_label.text = (
            f"✓ Excel'e aktarıldı!\n"
            f"{'━' * 22}\n"
            f"Dosya: {dosya_adi}\n"
            f"Kayıt sayısı: {len(kayitlar)}\n"
            f"{'━' * 22}"
        )

    def tumunu_temizle(self, instance):
        global kayitlar
        kayitlar = []
        self.sonuc_label.text = '✓ Tüm kayıtlar temizlendi!'


class TestApp(App):
    def build(self):
        return TechizForm()


if __name__ == '__main__':
    TestApp().run()