from kivy.app import App
from kivy.uix.tabbedpanel import TabbedPanel, TabbedPanelItem
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.dropdown import DropDown
from kivy.uix.popup import Popup
from kivy.core.clipboard import Clipboard
from kivy.graphics import Color, RoundedRectangle
from kivy.core.window import Window
from kivy.clock import Clock

import sys, os
# when running the file directly (python main.py) relative imports don't work.
# attempt package import first and fall back to plain import by adjusting sys.path.
try:
    from emotion_engine import detect_emotions
    from body_engine import detect_body
    from sentence_engine import build_sentence
except ImportError:
    try:
        from .emotion_engine import detect_emotions
        from .body_engine import detect_body
        from .sentence_engine import build_sentence
    except ImportError:
        pkg_dir = os.path.dirname(os.path.abspath(__file__))
        if pkg_dir not in sys.path:
            sys.path.insert(0, pkg_dir)
        from emotion_engine import detect_emotions
        from body_engine import detect_body
        from sentence_engine import build_sentence

# ---------------- Global Variables ----------------
LIKERT_OPTIONS = ["greatly_disagree", "disagree", "neutral", "agree", "greatly_agree"]
# using plain text labels because the default font may not render emoji properly
# (Kivy's default font often lacks emoji support on Windows).  Short codes make
# the buttons legible at small sizes.
LIKERT_LABELS = ["SD", "D", "N", "A", "SA"]
# font size for the Likert toggle buttons (larger for readability)
BUTTON_FONT_SIZE = "24sp"

EMOTION_QUESTIONS = [
    "I feel emotionally drained today.",
    "I feel on edge or restless.",
    "I feel disconnected from people or things around me.",
    "I feel easily irritated or frustrated.",
    "I feel hopeful or optimistic about things.",
    "I feel emotionally close or connected to someone.",
    "I feel capable of handling what’s happening.",
    "I feel like something is wrong, even if I can’t explain it.",
    "I feel emotionally heavy or low.",
    "I feel light, engaged, or interested in things"
]

BODY_QUESTIONS = [
    "I feel achy or sore.",
    "I feel tense or tight in my muscles.",
    "I feel light or airy.",
    "I feel numb or disconnected from my body.",
    "I feel fluttery or restless.",
    "I feel heavy or drained.",
    "I feel calm or relaxed."
]

NEED_OPTIONS = [
    "I need a hug",
    "I need a kiss",
    "I need cuddles",
    "I need someone's presence",
    "I need food",
    "I just need to drink water",
    "I want to apologize",
    "I need someone to apologize",
    "I need ice cream"
]

# Colors (primary palette and support according to spec)
# background
BG_COLOR = [1, 0.961, 0.969, 1]      # #FFF5F7 very soft pastel
# primary feel & focus
SOFT_ROSE = [246/255, 189/255, 192/255, 1]   # #F6BDC0
WARM_CORAL = [1, 111/255, 97/255, 1]         # #FF6F61
# secondary/support
MUTED_LAVENDER = [193/255, 163/255, 224/255, 1]  # #C1A3E0
SOFT_PEACH = [1, 227/255, 216/255, 1]            # #FFE3D8
POWDER_BLUE = [163/255, 213/255, 1, 1]           # #A3D5FF
# accents
DEEP_MAGENTA = [209/255, 69/255, 124/255, 1]      # #D1457C
GOLDEN_AMBER = [1, 200/255, 87/255, 1]            # #FFC857

# Kivy does not provide a simple built–in gradient fill for widgets.
# To get true gradients you can either supply a gradient image texture or
# write a custom shader.  The current implementation uses solid colors that
# harmonize with the palette; feel free to replace them with gradient
# textures if you wish later.

CARD_COLOR = SOFT_PEACH
BUTTON_COLOR = DEEP_MAGENTA
TEXT_COLOR = [0.2, 0.2, 0.2, 1]     # dark charcoal remains legible

snapshots = []

# Snapshot data structure
class Snapshot:
    def __init__(self, sentence, reason="", need="", desire=""):
        self.sentence = sentence
        self.reason = reason
        self.need = need
        self.desire = desire
    
    def to_full_text(self):
        """Generate full snapshot text with all fields"""
        parts = [self.sentence]
        if self.reason:
            parts.append(f"When {self.reason},")
        if self.desire:
            parts.append(f"I would like it if {self.desire}.")
        if self.need:
            parts.append(f"I need: {self.need}")
        return " ".join(parts)

# helper styles
def style_button(btn, color=None):
    # make every button rounded and use a flat background color
    btn.background_normal = ''
    btn.background_down = ''
    if color is not None:
        btn.background_color = color
    # rounded corners via canvas
    with btn.canvas.before:
        Color(* (color or BUTTON_COLOR))
        btn.rect = RoundedRectangle(pos=btn.pos, size=btn.size, radius=[12])
    btn.bind(pos=lambda *a: setattr(btn.rect, 'pos', btn.pos))
    btn.bind(size=lambda *a: setattr(btn.rect, 'size', btn.size))

# note label used at bottom of tabs
VALIDATION_NOTE = Label(text="your feelings are valid", size_hint_y=None, height=30, color=TEXT_COLOR, italic=True)

# ---------------- Card Widget ----------------
class Card(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = "vertical"
        self.padding = 10
        self.spacing = 10
        with self.canvas.before:
            Color(*CARD_COLOR)
            self.rect = RoundedRectangle(radius=[15])
        self.bind(pos=self.update_rect, size=self.update_rect)

    def update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size

# ---------------- Main App ----------------
class EmoserApp(TabbedPanel):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.do_default_tab = False

        self.emotion_answers = [None]*len(EMOTION_QUESTIONS)
        self.body_answers = [None]*len(BODY_QUESTIONS)
        self.last_emotion_sentence = ""

        # ---------- Feelings Tab (merged emotion + body) ----------
        self.feelings_tab = self.create_feelings_tab()
        self.add_widget(self.feelings_tab)

        # ---------- Phraser Tab ----------
        self.phraser_tab_layout = BoxLayout(orientation="vertical", padding=15, spacing=15)
        # give phraser tab a colored background similar to main BG
        with self.phraser_tab_layout.canvas.before:
            Color(*BG_COLOR)
            self.phraser_tab_layout.rect = RoundedRectangle(pos=self.phraser_tab_layout.pos, size=self.phraser_tab_layout.size)
        self.phraser_tab_layout.bind(pos=lambda *a: setattr(self.phraser_tab_layout.rect, 'pos', self.phraser_tab_layout.pos))
        self.phraser_tab_layout.bind(size=lambda *a: setattr(self.phraser_tab_layout.rect, 'size', self.phraser_tab_layout.size))
        self.phraser_tab_layout.add_widget(Label(text="Your generated emotion sentence:", color=TEXT_COLOR))
        self.sentence_input = TextInput(
            text="",
            multiline=True,
            size_hint_y=None,
            height=120,
            background_color=[1,1,1,1],
            foreground_color=TEXT_COLOR,
            padding=[10,10,10,10]
        )
        self.phraser_tab_layout.add_widget(self.sentence_input)

        # Second blank input (why you feel this)
        self.reason_input = TextInput(
            text="Please type what makes you feel this way",
            multiline=False,
            size_hint_y=None,
            height=80,
            background_color=[1,1,1,1],
            foreground_color=TEXT_COLOR,
            padding=[10,10,10,10]
        )
        self.phraser_tab_layout.add_widget(Label(text="What triggers this feeling?", color=TEXT_COLOR, size_hint_y=None, height=20))
        self.phraser_tab_layout.add_widget(self.reason_input)

        # Third blank: what would you like (desire)
        self.desire_input = TextInput(
            text="What would you like if... (describe your desire)",
            multiline=False,
            size_hint_y=None,
            height=40,
            background_color=[1,1,1,1],
            foreground_color=TEXT_COLOR,
            padding=[10,10,10,10]
        )
        self.phraser_tab_layout.add_widget(Label(text="What would you like?", color=TEXT_COLOR, size_hint_y=None, height=40))
        self.phraser_tab_layout.add_widget(self.desire_input)

        # Fourth blank: dropdown (need)
        self.need_dropdown = DropDown()
        self.need_input = Button(text="Select what you need", size_hint_y=None, height=80, color=TEXT_COLOR)
        style_button(self.need_input, POWDER_BLUE)
        self.phraser_tab_layout.add_widget(Label(text="What do you need?", color=TEXT_COLOR, size_hint_y=None, height=20))
        self.phraser_tab_layout.add_widget(self.need_input)

        for item in NEED_OPTIONS:
            btn = Button(text=item, size_hint_y=None, height=80, color=TEXT_COLOR)
            style_button(btn, POWDER_BLUE)
            btn.bind(on_release=lambda b: self.select_need(b.text))
            self.need_dropdown.add_widget(btn)

        self.need_input.bind(on_release=self.need_dropdown.open)

        # Allow user to add new need options
        self.add_need_input = TextInput(
            text="Type new need here and press Enter",
            multiline=False,
            size_hint_y=None,
            height=120,
            background_color=[1,1,1,1],
            foreground_color=TEXT_COLOR,
            padding=[10,10,10,10]
        )
        self.add_need_input.bind(on_text_validate=self.add_new_need)
        self.phraser_tab_layout.add_widget(self.add_need_input)

        # Save snapshot
        self.save_btn = Button(
            text="Save Snapshot",
            size_hint=(1, None),
            height=50,
            color=[1,1,1,1],
            bold=True
        )
        style_button(self.save_btn, WARM_CORAL)
        self.save_btn.bind(on_press=self.save_snapshot)
        self.phraser_tab_layout.add_widget(self.save_btn)
        # reminder message
        self.phraser_tab_layout.add_widget(Label(text="your feelings are valid", size_hint_y=None, height=30, color=TEXT_COLOR, italic=True))

        self.phraser_tab = self.create_tab("Phraser", self.phraser_tab_layout)
        self.add_widget(self.phraser_tab)

        # ---------- Snapshots Tab ----------
        self.snapshot_tab_layout = BoxLayout(orientation="vertical", padding=10)
        with self.snapshot_tab_layout.canvas.before:
            Color(*BG_COLOR)
            self.snapshot_tab_layout.rect = RoundedRectangle(pos=self.snapshot_tab_layout.pos, size=self.snapshot_tab_layout.size)
        self.snapshot_tab_layout.bind(pos=lambda *a: setattr(self.snapshot_tab_layout.rect, 'pos', self.snapshot_tab_layout.pos))
        self.snapshot_tab_layout.bind(size=lambda *a: setattr(self.snapshot_tab_layout.rect, 'size', self.snapshot_tab_layout.size))
        self.snapshot_tab_layout.add_widget(Label(text="your feelings are valid", size_hint_y=None, height=30, color=TEXT_COLOR, italic=True))
        self.scroll_snap = ScrollView()
        self.grid = GridLayout(cols=1, size_hint_y=None, spacing=10, padding=10)
        self.grid.bind(minimum_height=self.grid.setter('height'))
        self.scroll_snap.add_widget(self.grid)
        self.snapshot_tab_layout.add_widget(self.scroll_snap)
        self.snapshot_tab = self.create_tab("Snapshots", self.snapshot_tab_layout)
        self.add_widget(self.snapshot_tab)
        # make feelings tab active once construction is complete (can't call
        # switch_to in __init__ directly)
        Clock.schedule_once(lambda dt: self.switch_to(self.feelings_tab), 0)

    # ---------------- Tab Creation ----------------
    def create_tab(self, text, content):
        tab = TabbedPanelItem(text=text)
        # remove default background images so our colors show
        tab.background_normal = ''
        tab.background_down = ''
        tab.background_color = MUTED_LAVENDER
        # style tab header with rounded background (affects content area too)
        with tab.canvas.before:
            Color(*MUTED_LAVENDER)
            tab.rect = RoundedRectangle(pos=tab.pos, size=tab.size, radius=[10])
        tab.bind(pos=lambda *a: setattr(tab.rect, 'pos', tab.pos))
        tab.bind(size=lambda *a: setattr(tab.rect, 'size', tab.size))
        tab.add_widget(content)
        return tab

    # ---------------- Create Question Tabs ----------------
    def create_question_tab(self, tab_name, questions, answer_list):
        tab_layout = BoxLayout(orientation="vertical", padding=10, spacing=10)
        scroll = ScrollView()
        grid = GridLayout(cols=1, size_hint_y=None, spacing=10, padding=10)
        grid.bind(minimum_height=grid.setter('height'))

        for i, q in enumerate(questions):
            card = Card(size_hint_y=None, height=120)
            card_layout = BoxLayout(orientation="vertical", spacing=5)
            card_layout.add_widget(Label(text=q, color=TEXT_COLOR, size_hint_y=None, height=40))

            btn_layout = BoxLayout(spacing=5)
            for idx, opt in enumerate(LIKERT_OPTIONS):
                btn = ToggleButton(text=LIKERT_LABELS[idx],
                                   group=f"{tab_name}_{i}",
                                   font_size=BUTTON_FONT_SIZE,
                                   background_normal='',
                                   background_down='',
                                   background_color=[0.95,0.85,0.85,1],
                                   color=TEXT_COLOR)
                btn.bind(on_press=lambda b, q_idx=i, val=opt, ans_list=answer_list: self.set_answer(ans_list, q_idx, val))
                btn_layout.add_widget(btn)

            card_layout.add_widget(btn_layout)
            card.add_widget(card_layout)
            grid.add_widget(card)

        scroll.add_widget(grid)
        tab_layout.add_widget(scroll)

        detect_btn = Button(
            text="Detect Emotion",
            size_hint=(1, None),
            height=50,
            color=[1,1,1,1],
            bold=True
        )
        style_button(detect_btn, DEEP_MAGENTA)
        detect_btn.bind(on_press=self.detect_emotion)
        tab_layout.add_widget(detect_btn)
        # add validation note at bottom of each question tab
        tab_layout.add_widget(Label(text="your feelings are valid", size_hint_y=None, height=30, color=TEXT_COLOR, italic=True))

        return self.create_tab(tab_name, tab_layout)

    # ---------------- Create Feelings Tab ----------------
    def create_feelings_tab(self):
        # merges both emotion and body questions into one scrollable panel
        tab_layout = BoxLayout(orientation="vertical", padding=10, spacing=10)
        with tab_layout.canvas.before:
            Color(*BG_COLOR)
            tab_layout.rect = RoundedRectangle(pos=tab_layout.pos, size=tab_layout.size)
        tab_layout.bind(pos=lambda *a: setattr(tab_layout.rect, 'pos', tab_layout.pos))
        tab_layout.bind(size=lambda *a: setattr(tab_layout.rect, 'size', tab_layout.size))
        scroll = ScrollView()
        grid = GridLayout(cols=1, size_hint_y=None, spacing=10, padding=10)
        grid.bind(minimum_height=grid.setter('height'))

        # emotion questions first
        grid.add_widget(Label(text="Emotional Questions", size_hint_y=None, height=30, color=TEXT_COLOR))
        for i, q in enumerate(EMOTION_QUESTIONS):
            card = Card(size_hint_y=None, height=120)
            card_layout = BoxLayout(orientation="vertical", spacing=5)
            card_layout.add_widget(Label(text=q, color=TEXT_COLOR, size_hint_y=None, height=40))

            btn_layout = BoxLayout(spacing=5)
            for idx, opt in enumerate(LIKERT_OPTIONS):
                btn = ToggleButton(text=LIKERT_LABELS[idx],
                                   group=f"Feelings_emotion_{i}",
                                   font_size=BUTTON_FONT_SIZE,
                                   background_normal='',
                                   background_down='',
                                   color=TEXT_COLOR)
                normal_col = [0.95,0.85,0.85,1]
                down_col = WARM_CORAL
                btn.background_color = normal_col
                # change color when toggled
                btn.bind(state=lambda inst, val, nc=normal_col, dc=down_col: setattr(inst, 'background_color', dc if val=='down' else nc))
                btn.bind(on_press=lambda b, q_idx=i, val=opt: self.set_answer(self.emotion_answers, q_idx, val))
                btn_layout.add_widget(btn)

            card_layout.add_widget(btn_layout)
            card.add_widget(card_layout)
            grid.add_widget(card)

        # body questions section
        grid.add_widget(Label(text="Body Sensations", size_hint_y=None, height=30, color=TEXT_COLOR))
        for i, q in enumerate(BODY_QUESTIONS):
            card = Card(size_hint_y=None, height=120)
            card_layout = BoxLayout(orientation="vertical", spacing=5)
            card_layout.add_widget(Label(text=q, color=TEXT_COLOR, size_hint_y=None, height=40))

            btn_layout = BoxLayout(spacing=5)
            for idx, opt in enumerate(LIKERT_OPTIONS):
                btn = ToggleButton(text=LIKERT_LABELS[idx],
                                   group=f"Feelings_body_{i}",
                                   font_size=BUTTON_FONT_SIZE,
                                   background_normal='',
                                   background_down='',
                                   color=TEXT_COLOR)
                normal_col = [0.95,0.85,0.85,1]
                down_col = WARM_CORAL
                btn.background_color = normal_col
                btn.bind(state=lambda inst, val, nc=normal_col, dc=down_col: setattr(inst, 'background_color', dc if val=='down' else nc))
                btn.bind(on_press=lambda b, q_idx=i, val=opt: self.set_answer(self.body_answers, q_idx, val))
                btn_layout.add_widget(btn)

            card_layout.add_widget(btn_layout)
            card.add_widget(card_layout)
            grid.add_widget(card)

        scroll.add_widget(grid)
        tab_layout.add_widget(scroll)

        detect_btn = Button(
            text="Detect Emotion",
            size_hint=(1, None),
            height=50,
            background_color=BUTTON_COLOR,
            color=[1,1,1,1],
            bold=True
        )
        detect_btn.bind(on_press=self.detect_emotion)
        tab_layout.add_widget(detect_btn)

        return self.create_tab("Feelings", tab_layout)

    def set_answer(self, answer_list, idx, value):
        answer_list[idx] = value

    # ---------------- Detect ----------------
    def detect_emotion(self, *args):
        e1, e2 = detect_emotions([ans if ans else "neutral" for ans in self.emotion_answers])
        body = detect_body([ans if ans else "neutral" for ans in self.body_answers])
        sentence = build_sentence(e1, e2, body)
        self.last_emotion_sentence = sentence

        # put the generated sentence into the text box (clear placeholders)
        self.sentence_input.text = sentence
        self.reason_input.text = ""
        self.desire_input.text = ""
        self.need_input.text = "Select what you need"
        
        self.last_emotion_sentence = sentence

        # switch to phraser tab (same guard logic as before)
        tab_item = getattr(self, 'phraser_tab', None)
        if tab_item is None or tab_item not in getattr(self, 'tab_list', []):
            for t in getattr(self, 'tab_list', []):
                if getattr(t, 'text', None) == 'Phraser':
                    tab_item = t
                    break
        if tab_item is not None:
            try:
                self.switch_to(tab_item)
            except Exception as exc:
                print('warning: failed to switch to phraser tab', exc)
        else:
            print('warning: phraser tab not found, cannot switch')

    # ---------------- Snapshots ----------------
    def save_snapshot(self, *args):
        # snapshot whatever the user has produced (either filled sentence or
        # the raw last_emotion_sentence if not modified)
        sentence = getattr(self, 'current_sentence', '') or self.last_emotion_sentence
        if not sentence or sentence.strip() == "":
            return
        
        # capture reason, desire, and need fields
        reason = self.reason_input.text.strip()
        if reason.startswith("Please type"):
            reason = ""
        
        desire = self.desire_input.text.strip()
        if desire.startswith("What would you like"):
            desire = ""
        
        need = self.need_input.text
        if need.startswith("Select"):
            need = ""
        
        # create snapshot object and append
        snap = Snapshot(sentence, reason, need, desire)
        snapshots.append(snap)
        self.update_snapshot_tab()

    # ---------------- Phraser Helpers ----------------
    def select_need(self, text):
        self.need_input.text = text
        self.need_dropdown.dismiss()

    def add_new_need(self, instance):
        new_text = instance.text.strip()
        if new_text and new_text not in [c.text for c in self.need_dropdown.children]:
            btn = Button(text=new_text, size_hint_y=None, height=40, color=TEXT_COLOR)
            style_button(btn, POWDER_BLUE)
            btn.bind(on_release=lambda b: self.select_need(b.text))
            self.need_dropdown.add_widget(btn)
        self.need_input.text = new_text
        instance.text = ""

    def update_snapshot_tab(self):
        self.grid.clear_widgets()
        for idx, snap in enumerate(snapshots):
            card = Card(size_hint_y=None, height=100)
            box = BoxLayout(orientation="vertical", spacing=5)
            
            # Display full snapshot text
            full_text = snap.to_full_text()
            lbl = Label(text=full_text, color=TEXT_COLOR, size_hint_y=0.7)
            box.add_widget(lbl)
            
            # Action buttons row
            btn_box = BoxLayout(spacing=5, size_hint_y=0.3)
            
            # Communicate button
            comm_btn = Button(text="Communicate", size_hint_x=0.33, color=[1,1,1,1])
            style_button(comm_btn, GOLDEN_AMBER)
            comm_btn.bind(on_press=lambda x, snap=snap: self.communicate(snap))
            btn_box.add_widget(comm_btn)
            
            # Edit button
            edit_btn = Button(text="Edit", size_hint_x=0.33, color=[1,1,1,1])
            style_button(edit_btn, MUTED_LAVENDER)
            edit_btn.bind(on_press=lambda x, i=idx: self.edit_snapshot(i))
            btn_box.add_widget(edit_btn)
            
            # Delete button
            del_btn = Button(text="Delete", size_hint_x=0.33, color=[1,1,1,1])
            style_button(del_btn, SOFT_ROSE)
            del_btn.bind(on_press=lambda x, i=idx: self.delete_snapshot(i))
            btn_box.add_widget(del_btn)
            
            box.add_widget(btn_box)
            card.add_widget(box)
            self.grid.add_widget(card)

    def communicate(self, snap):
        full_text = snap.to_full_text()
        Clipboard.copy(full_text)
        popup = Popup(title="Copied!", content=Label(text="Snapshot copied to clipboard"), size_hint=(0.6,0.3))
        popup.open()
    
    def delete_snapshot(self, index):
        """Remove snapshot at given index"""
        if 0 <= index < len(snapshots):
            snapshots.pop(index)
            self.update_snapshot_tab()
    
    def edit_snapshot(self, index):
        """Open edit modal for snapshot"""
        if 0 <= index < len(snapshots):
            snap = snapshots[index]
            self._open_snapshot_editor(snap, index)
    
    def _open_snapshot_editor(self, snap, index):
        """Create and show snapshot editor popup"""
        editor_layout = BoxLayout(orientation="vertical", spacing=10, padding=15)
        
        # Sentence editor
        editor_layout.add_widget(Label(text="Sentence:", size_hint_y=None, height=20, color=TEXT_COLOR))
        sentence_edit = TextInput(text=snap.sentence, multiline=True, size_hint_y=None, height=80,
                                 background_color=[1,1,1,1], foreground_color=TEXT_COLOR, padding=[5,5,5,5])
        editor_layout.add_widget(sentence_edit)
        
        # Reason editor
        editor_layout.add_widget(Label(text="Trigger/Reason:", size_hint_y=None, height=20, color=TEXT_COLOR))
        reason_edit = TextInput(text=snap.reason, multiline=False, size_hint_y=None, height=40,
                               background_color=[1,1,1,1], foreground_color=TEXT_COLOR, padding=[5,5,5,5])
        editor_layout.add_widget(reason_edit)
        
        # Desire editor
        editor_layout.add_widget(Label(text="Desire:", size_hint_y=None, height=20, color=TEXT_COLOR))
        desire_edit = TextInput(text=snap.desire, multiline=False, size_hint_y=None, height=40,
                               background_color=[1,1,1,1], foreground_color=TEXT_COLOR, padding=[5,5,5,5])
        editor_layout.add_widget(desire_edit)
        
        # Need editor
        editor_layout.add_widget(Label(text="Need:", size_hint_y=None, height=20, color=TEXT_COLOR))
        need_edit = TextInput(text=snap.need, multiline=False, size_hint_y=None, height=40,
                             background_color=[1,1,1,1], foreground_color=TEXT_COLOR, padding=[5,5,5,5])
        editor_layout.add_widget(need_edit)
        
        # Action buttons
        btn_layout = BoxLayout(spacing=10, size_hint_y=None, height=50)
        
        save_edit_btn = Button(text="Save Changes", color=[1,1,1,1])
        style_button(save_edit_btn, WARM_CORAL)
        
        cancel_btn = Button(text="Cancel", color=[1,1,1,1])
        style_button(cancel_btn, SOFT_ROSE)
        
        btn_layout.add_widget(save_edit_btn)
        btn_layout.add_widget(cancel_btn)
        editor_layout.add_widget(btn_layout)
        
        # Create popup
        popup = Popup(title=f"Edit Snapshot {index + 1}", content=editor_layout, size_hint=(0.9, 0.9))
        
        def save_changes(btn):
            snapshots[index].sentence = sentence_edit.text
            snapshots[index].reason = reason_edit.text
            snapshots[index].desire = desire_edit.text
            snapshots[index].need = need_edit.text
            self.update_snapshot_tab()
            popup.dismiss()
        
        save_edit_btn.bind(on_press=save_changes)
        cancel_btn.bind(on_press=popup.dismiss)
        popup.open()

    # ---------------- Exercise helpers ----------------




# ---------------- Run App ----------------
class RootApp(App):
    def build(self):
        try:
            Window.clearcolor = BG_COLOR
        except:
            pass
        return EmoserApp()

if __name__ == "__main__":
    try:
        RootApp().run()
    except Exception as e:
        with open("crash_log.txt", "w") as f:
            import traceback
            traceback.print_exc(file=f)
        raise e
