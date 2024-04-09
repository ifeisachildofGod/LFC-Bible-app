import math
import os
from pathlib import Path
import threading
import time
import customtkinter as ctk
from tkinter import dialog
from PIL import Image
from tkinter import filedialog
import json
from bible.get_bible_info import *
from tkinter import font

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class BibleApp:
    def __init__(self):
        self.root = ctk.CTk()

        self.root.title('LFC Powerpoint Editor Tool')

        self._position_window(self.root, 1200, 600)

        self.root.resizable(False, False)
        
        self.font_families = list(font.families())
        self.font_families.sort()
        
        self.font_weights = ['normal', 'bold']
        self.font_slants = ['roman', 'italic']
        
        self.bible_book = ''
        
        self.initialize_bible()
        self.initialize_main_views_and_frames()
        
        self.initialize_header_frame()
        self.initialize_body_frame()
        self.initialize_footer_frame()
        
        self.initialize_bg_editor_frame()
        self.initialize_full_project_preview_frame()
        self.initialize_save_project_frame()

        self.lazy_header_update = 0
        self.lazy_footer_update = 0
        
        self.header_entry_id = '.!ctktabview.!ctkframe.!ctkframe2.!ctkentry.!entry'
        self.footer_entry_id = '.!ctktabview.!ctkframe.!ctkframe2.!ctkentry.!entry2'
        self.body_entry_id = '.!ctktabview.!ctkframe2.!ctkframe2.!ctkframe.!ctkentry.!entry'

        self.chapters_tracker = '1'
        self.verses_tracker = '1'
    
    def _position_window(self, window: ctk.CTk, width, height):
        # Get the screen width and height
        screen_width = window.winfo_screenwidth()

        # Calculate the position of the window
        x_coordinate = (screen_width - width) // 2
        y_coordinate = 50

        # Set the window position
        window.geometry(f"{width}x{height}+{x_coordinate}+{y_coordinate - 50}")

    def _update_chapter_per_book(self, book):
        orig_chapter = self.chapter_cb.get()
        chapter_amount = len(list(self.b_info[book].keys()))
        self.chapter_cb.configure(values=[str(i) for i in range(1, chapter_amount + 1)])
        self.chapter_cb.set('1')
        if orig_chapter:
            if 0 < int(orig_chapter) <= chapter_amount:
                self.chapter_cb.set(orig_chapter)

    def _update_verse_per_chapter(self, book):
        orig_verse = self.verse_cb.get()
        self._update_chapter_per_book(book)
        verse_amount = self.b_info[book][self.chapter_cb.get()]
        self.verse_cb.configure(values=[str(i) for i in range(1, verse_amount + 1)])
        self.verse_cb.set('1')
        if orig_verse:
            if 0 < int(orig_verse) <= verse_amount:
                self.verse_cb.set(orig_verse)

    def _update_and_reset_body_text_box(self, *args):
        if args:
            if args[0] in OLD_TESTAMENT + NEW_TESTAMENT:
                if args[0] in OLD_TESTAMENT:
                    book = self.old_test_books_cb.get()
                elif args[0] in NEW_TESTAMENT:
                    book = self.new_test_books_cb.get()

                self.curr_book_opened = book
                self._update_chapter_per_book(book)
            else:
                book = self.curr_book_opened
            
            self._update_verse_per_chapter(book)
            
        else:
            book = self.curr_book_opened
        
        self.bible_book = f'{book} {self.chapter_cb.get()}:{self.verse_cb.get()}'
        book_text = find_verse(book, self.chapter_cb.get(), self.verse_cb.get(), BIBLE_VERSION_MAP[self.biblical_text_translation.get()])
        self.body_t_box.delete(0.0, 'end')
        self.body_t_box.insert(0.0, book_text)
    
    def _update_body_prevew_justification(self, justify_orient):
        pass
        # self.body_preview_label.configure(justify=justify_orient.lower())
    
    def _update_header_justififcation_preview(self, justify: str):
        pass
        # self.header_preview_label.configure(justify=self.justify.lower())
    
    def _lazy_header_switch_update(self):
        self.lazy_header_update = int(self.lazy_header_update_switch.get())
    
    def _update_header_entry_box_font_style(self, *args):
        font = ctk.CTkFont(self.header_body_font_family_cb.get(), int(math.fabs(int(self.header_body_font_size_s.get()))), self.header_body_font_weight_cb.get(), self.header_body_font_slant_cb.get())
        self.header_entry.configure(font=font, text_color=self.header_text_color_e.get())
    
    def _update_body_text_box_font_style(self, *args):
        font = ctk.CTkFont(self.body_font_family_cb.get(), int(math.fabs(int(self.body_font_size_s.get()))), self.body_font_weight_cb.get(), self.body_font_slant_cb.get())
        self.body_t_box.configure(font=font)
    
    def _set_header_passage(self):
        if self.bible_book != self.header_entry.get():
            self.header_entry.delete(0, 'end')
            # header_preview_label.configure(text=self.bible_book)
            self.header_entry.insert(0, self.bible_book)
    
    def _update_footer_justififcation_preview(self, justify: str):
        pass
        # self.footer_preview_label.configure(justify=justify.lower())

    def _set_footer_passage(self):
        if self.bible_book != self.footer_entry.get():
            self.footer_entry.delete(0, 'end')
            # footer_preview_label.configure(text=self.bible_book)
            self.footer_entry.insert(0, self.bible_book)

    def _update_footer_entry_box_font_style(self, *args):
        font = ctk.CTkFont(self.footer_body_font_family_cb.get(), int(math.fabs(int(self.footer_body_font_size_s.get()))), self.footer_body_font_weight_cb.get(), self.footer_body_font_slant_cb.get())
        self.footer_entry.configure(font=font, text_color=self.footer_text_color_e.get())

    def _lazy_footer_switch_update(self):
        self.lazy_footer_update = int(self.lazy_footer_update_switch.get())
    
    def _open_file_browser(self, file_types):
        file_path = filedialog.askopenfilename(initialdir=os.getcwd(), filetypes=file_types)
        if file_path:
            self.image_path_e.delete(0, 'end')
            self.image_path_e.insert(0, file_path)

    def _update_and_show_image(self, file_path):
        if not int(self.bg_state_switch.get()):
            if file_path:
                if Path(file_path).exists():
                    image = Image.open(file_path)
                    ctk_image = ctk.CTkImage(image)
                    ctk_image.configure(size=(image.width, image.height))
                    # bg_label.configure(image=ctk_image)
                    # bg_label.pack()
                    self.image_label.configure(image=ctk_image)
                    self.image_label.pack()
        else:
            try:
                self.img_preview_frame.configure(fg_color=self.color_e.get())
                # bg_frame.configure(fg_color=self.color_e.get())
                self.image_label.configure(image=None)
                # bg_label.configure(image=None)
            except Exception as e:
                pass

    def _change_bg_state(self):
        if int(self.bg_state_switch.get()):
            self.image_path_e.configure(placeholder_text='')
            self.image_path_e.delete(0, 'end')
            self.image_path_e.configure(state='disabled')
            self.image_path_button.configure(state='disabled')
            self.color_e.configure(state='normal', placeholder_text='Enter background color')
        else:
            self.image_path_e.configure(state='normal', placeholder_text='Enter image file path')
            self.image_path_button.configure(state='normal')
            self.color_e.configure(placeholder_text='')
            self.color_e.delete(0, 'end')
            self.color_e.configure(state='disabled')
    
    def _send_and_update_project(self):
        print('Send to powerpoint')

    def _get_export_project_file(self, file_types):
        file_path = filedialog.askopenfilename(initialdir=os.getcwd(), filetypes=file_types)
        
        if file_path and Path(file_path).exists():
            self.save_path_e.delete(0, 'end')
            self.save_path_e.insert(0, file_path)

    def _save_project(file_types):
        try:
            d = dialog.Dialog(None, {'title': 'Update Error',
                            'text':
                            'This feature will be added in the '
                            'next update, if LFC Enugu likes it '
                            'I will continue development, else, '
                            'I will end this project and work '
                            'on another project',
                            'bitmap': '',
                            'default': 0,
                            'strings': ('  Ok  ', 'Cancel')})
            d.pack()
        except:
            pass
    
    def _change_curr_passage(self, dir):
        prev_verse = int(self.verse_cb.get())
        prev_chapter = int(self.chapter_cb.get())
        
        verse_amount = self.b_info[self.curr_book_opened][self.chapter_cb.get()]
        chapter_amount = len(list(self.b_info[self.curr_book_opened].keys()))
        
        if dir > 0:
            if prev_verse < verse_amount:
                self.verse_cb.set(str(int(self.verse_cb.get()) + 1))
            else:
                if prev_chapter < chapter_amount:
                    self.verse_cb.set('1')
                    self.chapter_cb.set(str(int(self.chapter_cb.get()) + 1))
                else:
                    if self.curr_book_opened in self.old_test_books_cb._values:
                        if self.old_test_books_cb._values.index(self.curr_book_opened) < len(self.old_test_books_cb._values) - 1:
                            self.verse_cb.set('1')
                            self.chapter_cb.set('1')
                            self.old_test_books_cb.set(self.old_test_books_cb._values[self.old_test_books_cb._values.index(self.curr_book_opened) + 1])
                            self.curr_book_opened = self.old_test_books_cb.get()
                        else:
                            self.verse_cb.set('1')
                            self.chapter_cb.set('1')
                            self.new_test_books_cb.set(self.new_test_books_cb._values[0])
                            self.curr_book_opened = self.new_test_books_cb.get()
                    else:
                        if self.new_test_books_cb._values.index(self.curr_book_opened) < len(self.new_test_books_cb._values) - 1:
                            self.verse_cb.set('1')
                            self.chapter_cb.set('1')
                            self.new_test_books_cb.set(self.new_test_books_cb._values[self.new_test_books_cb._values.index(self.curr_book_opened) + 1])
                            self.curr_book_opened = self.new_test_books_cb.get()
        else:
            if prev_verse > 0:
                self.verse_cb.set(str(int(self.verse_cb.get()) - 1))
            else:
                if prev_chapter > 0:
                    self.verse_cb.set('1')
                    self.chapter_cb.set(str(int(self.chapter_cb.get()) - 1))
                else:
                    if self.curr_book_opened in self.new_test_books_cb._values:
                        if self.new_test_books_cb._values.index(self.curr_book_opened) > 0:
                            self.verse_cb.set('1')
                            self.chapter_cb.set('1')
                            self.new_test_books_cb.set(self.new_test_books_cb._values[self.new_test_books_cb._values.index(self.curr_book_opened) - 1])
                            self.curr_book_opened = self.new_test_books_cb.get()
                        else:
                            self.verse_cb.set('1')
                            self.chapter_cb.set('1')
                            self.old_test_books_cb.set(self.old_test_books_cb._values[-1])
                            self.curr_book_opened = self.old_test_books_cb.get()
                    else:
                        if self.old_test_books_cb._values.index(self.curr_book_opened) > 0:
                            self.verse_cb.set('1')
                            self.chapter_cb.set('1')
                            self.old_test_books_cb.set(self.old_test_books_cb._values[self.old_test_books_cb._values.index(self.curr_book_opened) - 1])
                            self.curr_book_opened = self.old_test_books_cb.get()
    
    def _per_second_event_loop(self):
        while True:
            if self.lazy_footer_update:
                self._set_footer_passage()
            if self.lazy_header_update:
                self._set_header_passage()
            
            if 'header font editor' == self.main_tab_view.get().lower():
                color = self.header_text_color_e.get()
                
                if str(self.header_entry.focus_get()) == self.header_entry_id or self.header_entry._text_color != color:
                    try:
                        if self.header_entry._text_color != color:
                            self.header_entry.configure(text_color=color, placeholder_text_color=color)
                            # self.header_preview_label.configure(text_color=self.header_entry._text_color)
                    except:
                        pass
                # self.header_preview_label.configure(text=self.header_entry.get(), font=self.header_entry._font)
            
            elif 'body font editor' == self.main_tab_view.get().lower():
                color = self.body_text_color_e.get()
                
                cur_chapter = self.chapter_cb.get()
                cur_verse = self.verse_cb.get()
                
                verse_amount = self.b_info[self.curr_book_opened][self.chapter_cb.get()]
                chapter_amount = len(list(self.b_info[self.curr_book_opened].keys()))
        
                if self.chapters_tracker != cur_chapter:
                    self.chapters_tracker = cur_chapter
                    self._update_and_reset_body_text_box([self.curr_book_opened])
                if self.verses_tracker != cur_verse:
                    self.verses_tracker = cur_verse
                    self._update_and_reset_body_text_box([self.curr_book_opened])
                if str(self.body_text_color_e.focus_get()) == self.body_entry_id or self.body_text_color_e._text_color != color:
                    try:
                        if self.body_t_box._text_color != color:
                            self.body_t_box.configure(text_color=color)
                            # self.body_preview_label.configure(text_color=self.body_t_box._text_color)
                    except:
                        pass
                
                if self.curr_book_opened == self.old_test_books_cb._values[0] and int(cur_chapter) == 1 and  int(cur_verse) == 1:
                    self.prev_passage_button.configure(state='disabled')
                else:
                    self.prev_passage_button.configure(state='normal')
                
                if self.curr_book_opened == self.new_test_books_cb._values[-1] and int(cur_chapter) == chapter_amount and  int(cur_verse) == verse_amount:
                    self.next_passage_button.configure(state='disabled')
                else:
                    self.next_passage_button.configure(state='normal')
                # self.body_preview_label.configure(text=self.body_t_box.get(0.0, 'end'), font=self.body_t_box._font)
            
            elif 'footer font editor' == self.main_tab_view.get().lower():
                color = self.footer_text_color_e.get()
                
                if str(self.footer_entry.focus_get()) == self.footer_entry_id or self.footer_entry._text_color != color:
                    try:
                        if self.footer_entry._text_color != color:
                            self.footer_entry.configure(text_color=color, placeholder_text_color=color)
                            # self.footer_preview_label.configure(text_color=self.footer_entry._text_color)
                    except:
                        pass
                # self.footer_preview_label.configure(text=self.footer_entry.get(), font=self.footer_entry._font)
            # elif 'preview and send' == main_tab_view.get().lower():
            #     self.header_preview_label.configure(text=header_entry.get(), font=header_entry._font, text_color=header_entry._text_color)
            #     self.body_preview_label.configure(text=self.body_t_box.get(0.0, 'end'), font=self.body_t_box._font, text_color=self.body_t_box._text_color)
            #     self.footer_preview_label.configure(text=self.footer_entry.get(), font=self.footer_entry._font, text_color=self.footer_entry._text_color)
            
            time.sleep(1)
    
    def initialize_bible(self):
        with open('bible/books_chapter_verse_info.json') as bible_info:
            self.b_info = json.loads(bible_info.read())
    
    def initialize_main_views_and_frames(self):
        self.main_tab_view = ctk.CTkTabview(self.root, 500, 400)
        self.main_tab_view.pack(pady=50)

        self.header_frame = self.main_tab_view.add('Header Font Editor')
        self.body_frame = self.main_tab_view.add('Body Font Editor')
        self.footer_frame = self.main_tab_view.add('Footer Font Editor')
        self.other_settings_frame = self.main_tab_view.add('Backgroud Editor')
        # self.preview_frame = self.main_tab_view.add('Preview and Send')
        self.save_settings_frame = self.main_tab_view.add('Save settings')
    
    def initialize_header_frame(self):
        self.slide_header_text_box_params_frame = ctk.CTkFrame(self.header_frame)
        self.slide_header_text_box_params_frame.grid(row=0, column=0, pady=1, padx=30)

        self.slide_header_settings_params_frame = ctk.CTkFrame(self.header_frame)
        self.slide_header_settings_params_frame.grid(row=0, column=1, pady=1, padx=30)

        self.set_header_passage_button_frame = ctk.CTkFrame(self.header_frame)
        self.set_header_passage_button_frame.grid(row=1, column=0, pady=1, padx=30)

        self.header_justification_selector = ctk.CTkSegmentedButton(self.slide_header_text_box_params_frame, values=['Left', 'Center', 'Right'], command=self._update_header_justififcation_preview)
        self.header_entry = ctk.CTkEntry(self.slide_header_text_box_params_frame, 450, 150, corner_radius=5, border_width=2, placeholder_text='Enter Slide Header')

        self.header_justification_selector.grid(row=0, column=0)
        self.header_entry.grid(row=1, column=0)

        self.header_body_font_size_label = ctk.CTkLabel(self.slide_header_settings_params_frame, text='Font Size')
        self.header_body_font_size_s = ctk.CTkSlider(self.slide_header_settings_params_frame, from_=10, to=100, variable=ctk.IntVar(self.root, 20), command=self._update_header_entry_box_font_style)
        self.header_body_font_family_label = ctk.CTkLabel(self.slide_header_settings_params_frame, text='Font Family')
        self.header_body_font_family_cb = ctk.CTkComboBox(self.slide_header_settings_params_frame, values=self.font_families, command=self._update_header_entry_box_font_style, state="readonly", variable=ctk.StringVar(self.root, self.font_families[0]))
        self.header_body_font_weight_label = ctk.CTkLabel(self.slide_header_settings_params_frame, text='Font Weight')
        self.header_body_font_weight_cb = ctk.CTkComboBox(self.slide_header_settings_params_frame, values=self.font_weights, command=self._update_header_entry_box_font_style, state="readonly", variable=ctk.StringVar(self.root, self.font_weights[0]))
        self.header_body_font_slant_label = ctk.CTkLabel(self.slide_header_settings_params_frame, text='Font Slant')
        self.header_body_font_slant_cb = ctk.CTkComboBox(self.slide_header_settings_params_frame, values=self.font_slants, command=self._update_header_entry_box_font_style, state="readonly", variable=ctk.StringVar(self.root, self.font_slants[0]))
        self.header_font_color_label = ctk.CTkLabel(self.slide_header_settings_params_frame, text='Text Color')
        self.header_text_color_e = ctk.CTkEntry(self.slide_header_settings_params_frame, textvariable=ctk.StringVar(self.root, 'White'))

        self.lazy_header_update_switch = ctk.CTkSwitch(self.set_header_passage_button_frame, text='Auto passage update', command=self._lazy_header_switch_update, bg_color='#3e3e3e')
        self.set_header_passage_button = ctk.CTkButton(self.set_header_passage_button_frame, text='Set Header to current passage', command=self._set_header_passage)

        self.header_body_font_size_label.grid(row=0, column=0, pady=1)
        self.header_body_font_size_s.grid(row=1, column=0, pady=1)
        self.header_body_font_family_label.grid(row=2, column=0, pady=1)
        self.header_body_font_family_cb.grid(row=3, column=0, pady=1)
        self.header_body_font_weight_label.grid(row=4, column=0, pady=1)
        self.header_body_font_weight_cb.grid(row=5, column=0, pady=1)
        self.header_body_font_slant_label.grid(row=6, column=0, pady=1)
        self.header_body_font_slant_cb.grid(row=7, column=0, pady=1)
        self.header_font_color_label.grid(row=8, column=0, pady=1)
        self.header_text_color_e.grid(row=9, column=0, pady=1)
        
        self.set_header_passage_button.grid(row=0, column=0, pady=5, padx=15)
        self.lazy_header_update_switch.grid(row=0, column=1, pady=5, padx=15)

        self._update_header_entry_box_font_style()

    def initialize_body_frame(self):
        self.bible_params_frame = ctk.CTkFrame(self.body_frame)
        self.bible_params_frame.grid(column=0, row=0, pady=20, padx=30)

        self.text_box_frame = ctk.CTkFrame(self.body_frame, fg_color='transparent')
        self.text_box_frame.grid(column=0, row=1)

        settings_sub_frame = ctk.CTkFrame(self.body_frame, fg_color='transparent')
        settings_sub_frame.grid(row=1, column=1, padx=10)

        self.final_buttons_frame = ctk.CTkFrame(self.body_frame, fg_color="transparent")
        self.final_buttons_frame.grid(column=0, row=2, pady=10)
        
        self.old_test_books_label = ctk.CTkLabel(self.bible_params_frame, text='Old Testament')
        self.old_test_books_cb = ctk.CTkOptionMenu(self.bible_params_frame, values=OLD_TESTAMENT, command=self._update_and_reset_body_text_box, state='readonly', variable=ctk.StringVar(self.root, 'Genesis'))
        self.new_test_books_label = ctk.CTkLabel(self.bible_params_frame, text='New Testament')
        self.new_test_books_cb = ctk.CTkOptionMenu(self.bible_params_frame, values=NEW_TESTAMENT, command=self._update_and_reset_body_text_box, state='readonly', variable=ctk.StringVar(self.root, 'Mathew'), )
        self.chapter_label = ctk.CTkLabel(self.bible_params_frame, text='Chapter')
        self.chapter_cb = ctk.CTkComboBox(self.bible_params_frame, command=self._update_and_reset_body_text_box, variable=ctk.StringVar(self.root, '1'))
        self.verse_label = ctk.CTkLabel(self.bible_params_frame, text='Verse')
        self.verse_cb = ctk.CTkComboBox(self.bible_params_frame, command=self._update_and_reset_body_text_box, variable=ctk.StringVar(self.root, '1'))
        self.biblical_text_translation_label = ctk.CTkLabel(self.bible_params_frame, text='Translation')
        self.biblical_text_translation = ctk.CTkOptionMenu(self.bible_params_frame, values=list(BIBLE_VERSION_MAP.keys()), command=self._update_and_reset_body_text_box, variable=ctk.StringVar(self.root, list(BIBLE_VERSION_MAP.keys())[0]))
        
        self.old_test_books_label.grid(row=0, column=0)
        self.old_test_books_cb.grid(row=1, column=0)
        self.new_test_books_label.grid(row=0, column=1, padx=15)
        self.new_test_books_cb.grid(row=1, column=1, padx=15)
        self.chapter_label.grid(row=0, column=2)
        self.chapter_cb.grid(row=1, column=2)
        self.verse_label.grid(row=0, column=3, padx=15)
        self.verse_cb.grid(row=1, column=3, padx=15)
        self.biblical_text_translation_label.grid(row=0, column=4)
        self.biblical_text_translation.grid(row=1, column=4)

        self.curr_book_opened = self.old_test_books_cb.get()

        self.body_justification_selector = ctk.CTkSegmentedButton(self.text_box_frame, values=['Left', 'Center', 'Right'], command=self._update_body_prevew_justification)
        self.body_t_box = ctk.CTkTextbox(self.text_box_frame, 800, 200, 10, 5, 4)

        self.body_justification_selector.grid(row=0, column=0, padx=10)
        self.body_t_box.grid(row=1, column=0, padx=10)
        
        self.body_font_size_label = ctk.CTkLabel(settings_sub_frame, text='Font Size')
        self.body_font_size_s = ctk.CTkSlider(settings_sub_frame, from_=10, to=100, variable=ctk.IntVar(self.root, 20), command=self._update_body_text_box_font_style)
        self.body_font_family_label = ctk.CTkLabel(settings_sub_frame, text='Font Family')
        self.body_font_family_cb = ctk.CTkComboBox(settings_sub_frame, values=self.font_families, command=self._update_body_text_box_font_style, state="readonly", variable=ctk.StringVar(self.root, self.font_families[0]))
        self.body_font_weight_label = ctk.CTkLabel(settings_sub_frame, text='Font Weight')
        self.body_font_weight_cb = ctk.CTkComboBox(settings_sub_frame, values=self.font_weights, command=self._update_body_text_box_font_style, state="readonly", variable=ctk.StringVar(self.root, self.font_weights[0]))
        self.body_font_slant_label = ctk.CTkLabel(settings_sub_frame, text='Font Slant')
        self.body_font_slant_cb = ctk.CTkComboBox(settings_sub_frame, values=self.font_slants, command=self._update_body_text_box_font_style, state="readonly", variable=ctk.StringVar(self.root, self.font_slants[0]))
        self.body_text_color_label = ctk.CTkLabel(settings_sub_frame, text='Text Color')
        self.body_text_color_e = ctk.CTkEntry(settings_sub_frame, textvariable=ctk.StringVar(self.root, 'White'))

        self.prev_passage_button = ctk.CTkButton(self.final_buttons_frame, text='Prev', command=lambda: self._change_curr_passage(-1))
        self.reset_text_button = ctk.CTkButton(self.final_buttons_frame, text='Reset Text', command=self._update_and_reset_body_text_box)
        self.next_passage_button = ctk.CTkButton(self.final_buttons_frame, text='Next', command=lambda: self._change_curr_passage(1))

        self.body_font_size_label.grid(row=0, column=0, pady=2)
        self.body_font_size_s.grid(row=1, column=0, pady=2)
        self.body_font_family_label.grid(row=2, column=0, pady=2)
        self.body_font_family_cb.grid(row=3, column=0, pady=2)
        self.body_font_weight_label.grid(row=4, column=0, pady=2)
        self.body_font_weight_cb.grid(row=5, column=0, pady=2)
        self.body_font_slant_label.grid(row=6, column=0, pady=2)
        self.body_font_slant_cb.grid(row=7, column=0, pady=2)
        self.body_text_color_label.grid(row=8, column=0, pady=2)
        self.body_text_color_e.grid(row=9, column=0, pady=2)

        self.prev_passage_button.grid(column=0, row=0, padx=20)
        self.reset_text_button.grid(column=1, row=0, padx=20)
        self.next_passage_button.grid(column=2, row=0, padx=20)

        self._update_body_text_box_font_style()
        self._update_and_reset_body_text_box(['Genesis'])

    def initialize_footer_frame(self):
        self.slide_footer_text_box_params_frame = ctk.CTkFrame(self.footer_frame)
        self.slide_footer_text_box_params_frame.grid(row=0, column=0, pady=1, padx=30)

        self.slide_footer_settings_params_frame = ctk.CTkFrame(self.footer_frame)
        self.slide_footer_settings_params_frame.grid(row=0, column=1, pady=1, padx=30)

        self.set_footer_passage_button_frame = ctk.CTkFrame(self.footer_frame)
        self.set_footer_passage_button_frame.grid(row=1, column=0, pady=1, padx=30)

        self.footer_justification_selector = ctk.CTkSegmentedButton(self.slide_footer_text_box_params_frame, values=['Left', 'Center', 'Right'], command=self._update_footer_justififcation_preview)
        self.footer_entry = ctk.CTkEntry(self.slide_footer_text_box_params_frame, 450, 150, corner_radius=5, border_width=2, placeholder_text='Enter Slide Footer')

        self.footer_justification_selector.grid(row=0, column=0)
        self.footer_entry.grid(row=1, column=0)

        self.footer_body_font_size_label = ctk.CTkLabel(self.slide_footer_settings_params_frame, text='Font Size')
        self.footer_body_font_size_s = ctk.CTkSlider(self.slide_footer_settings_params_frame, from_=10, to=100, variable=ctk.IntVar(self.root, 20), command=self._update_footer_entry_box_font_style)
        self.footer_body_font_family_label = ctk.CTkLabel(self.slide_footer_settings_params_frame, text='Font Family')
        self.footer_body_font_family_cb = ctk.CTkComboBox(self.slide_footer_settings_params_frame, values=self.font_families, command=self._update_footer_entry_box_font_style, state="readonly", variable=ctk.StringVar(self.root, self.font_families[0]))
        self.footer_body_font_weight_label = ctk.CTkLabel(self.slide_footer_settings_params_frame, text='Font Weight')
        self.footer_body_font_weight_cb = ctk.CTkComboBox(self.slide_footer_settings_params_frame, values=self.font_weights, command=self._update_footer_entry_box_font_style, state="readonly", variable=ctk.StringVar(self.root, self.font_weights[0]))
        self.footer_body_font_slant_label = ctk.CTkLabel(self.slide_footer_settings_params_frame, text='Font Slant')
        self.footer_body_font_slant_cb = ctk.CTkComboBox(self.slide_footer_settings_params_frame, values=self.font_slants, command=self._update_footer_entry_box_font_style, state="readonly", variable=ctk.StringVar(self.root, self.font_slants[0]))
        self.footer_font_color_label = ctk.CTkLabel(self.slide_footer_settings_params_frame, text='Text Color')
        self.footer_text_color_e = ctk.CTkEntry(self.slide_footer_settings_params_frame, textvariable=ctk.StringVar(self.root, 'White'))

        self.lazy_footer_update_switch = ctk.CTkSwitch(self.set_footer_passage_button_frame, text='Auto passage update', command=self._lazy_footer_switch_update, bg_color='#3e3e3e')
        self.set_footer_passage_button = ctk.CTkButton(self.set_footer_passage_button_frame, text='Set Header to current passage', command=self._set_footer_passage)

        self.footer_body_font_size_label.grid(row=0, column=0, pady=1)
        self.footer_body_font_size_s.grid(row=1, column=0, pady=1)
        self.footer_body_font_family_label.grid(row=2, column=0, pady=1)
        self.footer_body_font_family_cb.grid(row=3, column=0, pady=1)
        self.footer_body_font_weight_label.grid(row=4, column=0, pady=1)
        self.footer_body_font_weight_cb.grid(row=5, column=0, pady=1)
        self.footer_body_font_slant_label.grid(row=6, column=0, pady=1)
        self.footer_body_font_slant_cb.grid(row=7, column=0, pady=1)
        self.footer_font_color_label.grid(row=8, column=0, pady=1)
        self.footer_text_color_e.grid(row=9, column=0, pady=1)

        self.set_footer_passage_button.grid(row=0, column=0, pady=5, padx=15)
        self.lazy_footer_update_switch.grid(row=0, column=1, pady=5, padx=15)

        self._update_footer_entry_box_font_style()

    def initialize_bg_editor_frame(self):
        self.master_bg_editor_frame = ctk.CTkScrollableFrame(self.other_settings_frame, width=600, height=500)
        self.master_bg_editor_frame.pack()

        self.img_file_path_frame = ctk.CTkFrame(self.master_bg_editor_frame)
        self.img_file_path_frame.pack(pady=10)

        self.image_save_and_preview_button = ctk.CTkButton(self.master_bg_editor_frame, text='Save and preview image', command=lambda: self._update_and_show_image(self.image_path_e.get()))
        self.image_save_and_preview_button.pack(pady=20)

        self.img_preview_frame = ctk.CTkScrollableFrame(self.master_bg_editor_frame, width=600, height=500, orientation='horizontal')
        self.img_preview_frame.pack(pady=10)

        self.image_path_e = ctk.CTkEntry(self.img_file_path_frame, placeholder_text='Enter image file path', width=240, height=30)
        self.image_path_button = ctk.CTkButton(self.img_file_path_frame, text='Choose image file', command=lambda: self._open_file_browser([('PNG Files', '*.png'), ('JPEG Files', '*.jpg')]))
        self.color_e = ctk.CTkEntry(self.img_file_path_frame, placeholder_text='Enter color', width=240, height=30, state='disabled')

        self.bg_state_switch = ctk.CTkSwitch(self.img_file_path_frame, command=self._change_bg_state, text='Use Color as Background')

        self.bg_state_switch.grid(column=0, row=0, pady=10)
        self.image_path_e.grid(column=0, row=1, padx=20, pady=10)
        self.image_path_button.grid(column=1, row=1, padx=20, pady=10)
        self.color_e.grid(column=0, row=2, pady=10)
        self.image_label = ctk.CTkLabel(self.img_preview_frame, text='')

    def initialize_full_project_preview_frame(self):
        # self.master_preview_frame = ctk.CTkScrollableFrame(self.preview_frame, width=500, height=400, fg_color='transparent')
        # self.master_preview_frame.pack()

        # self.bg_frame = ctk.CTkFrame(self.master_preview_frame, width=self.img_preview_frame._desired_width, height=self.img_preview_frame._desired_height, fg_color=self.image_label._fg_color)
        # self.bg_frame.grid(column=0, row=1)

        # self.bg_label = ctk.CTkLabel(self.bg_frame, text='')

        # self.header_footer_wraplength = 400
        
        # self.header_preview_label = ctk.CTkLabel(self.master_preview_frame, text=self.header_entry.get(), wraplength=self.header_footer_wraplength, fg_color='transparent')
        # self.header_preview_label.grid(column=0, row=0, pady=200)
        # self.header_preview_label.configure(text=self.header_entry.get(), font=self.header_entry._font, text_color=self.header_entry._text_color)

        # self.body_preview_label = ctk.CTkLabel(self.master_preview_frame, text=self.body_t_box.get(0.0, 'end'), wraplength=self.master_preview_frame._desired_width, fg_color='transparent')
        # self.body_preview_label.grid(column=0, row=0)
        # self.body_preview_label.configure(text=self.body_t_box.get(0.0, 'end'), font=self.body_t_box._font, text_color=self.body_t_box._text_color)

        # self.footer_preview_label = ctk.CTkLabel(self.master_preview_frame, text=self.footer_entry.get(), wraplength=self.header_footer_wraplength, fg_color='transparent')
        # self.footer_preview_label.grid(column=0, row=0)
        # self.footer_preview_label.configure(text=self.footer_entry.get(), font=self.footer_entry._font, text_color=self.footer_entry._text_color)
        pass
    
    def _get_body(self):
        body_text = self.body_t_box.get(0.0, 'end')
        body_font_size = self.body_font_size_s.get()
        body_font_family = self.body_font_family_cb.get()
        body_font_weight = self.body_font_weight_cb.get()
        body_font_slant = self.body_font_slant_cb.get()
        body_text_color = self.body_text_color_e.get()
        body_justify = self.body_justification_selector.get()
        
        body_params = dict(
            text = body_text,
            font_size = body_font_size,
            font_family = body_font_family,
            font_weight = body_font_weight,
            font_slant = body_font_slant,
            text_color = body_text_color,
            justify = body_justify,
        )
        
        return body_params
    
    def _get_header(self):
        header_text = self.header_entry.get()
        header_body_font_size = self.header_body_font_size_s.get()
        header_body_font_family = self.header_body_font_family_cb.get()
        header_body_font_weight = self.header_body_font_weight_cb.get()
        header_body_font_slant = self.header_body_font_slant_cb.get()
        header_text_color = self.header_text_color_e.get()
        header_justify = self.header_justification_selector.get()
        
        header_params = dict(
            text = header_text,
            font_size = header_body_font_size,
            font_family = header_body_font_family,
            font_weight = header_body_font_weight,
            font_slant = header_body_font_slant,
            text_color = header_text_color,
            justify = header_justify
        )
        
        return header_params
    
    def _get_footer(self):
        footer_text = self.footer_entry.get()
        footer_body_font_size = self.footer_body_font_size_s.get()
        footer_body_font_family = self.footer_body_font_family_cb.get()
        footer_body_font_weight = self.footer_body_font_weight_cb.get()
        footer_body_font_slant = self.footer_body_font_slant_cb.get()
        footer_text_color = self.footer_text_color_e.get()
        header_justify = self.header_justification_selector.get()
        
        footer_params = dict(
            text = footer_text,
            font_size = footer_body_font_size,
            font_family = footer_body_font_family,
            font_weight = footer_body_font_weight,
            font_slant = footer_body_font_slant,
            text_color = footer_text_color,
            justify = header_justify
        )
        
        return footer_params
    
    def get(self):
        get_info = dict(
            header = self._get_header(),
            body = self._get_body(),
            footer = self._get_footer(),
        )
        
        return get_info
    
    def initialize_save_project_frame(self):
        self.save_project_file_path_frame = ctk.CTkFrame(self.save_settings_frame)
        self.save_project_file_path_frame.pack(pady=10)
        
        self.send_project_file_path_frame = ctk.CTkFrame(self.save_settings_frame)
        self.send_project_file_path_frame.pack(pady=70)
        
        self.save_path_e = ctk.CTkEntry(self.save_project_file_path_frame, placeholder_text='Enter export path', width=240, height=30)
        self.save_path_e.grid(column=0, row=0, padx=20)
        self.save_path_button = ctk.CTkButton(self.save_project_file_path_frame, text='Chose export file', command=lambda: self._get_export_project_file([('Powerpoint Files', '*.pptx'), ]))
        self.save_path_button.grid(column=1, row=0, padx=20)

        self.send_button = ctk.CTkButton(self.send_project_file_path_frame, text='Send and Update Text', command=self._send_and_update_project)
        self.send_button.grid(column=0, row=0, padx=20)
        self.save_project_path_button = ctk.CTkButton(self.send_project_file_path_frame, text='Save Project', command=self._save_project)
        self.save_project_path_button.grid(column=1, row=0, padx=20)

    def run_eventloops(self):
        per_second_event_loop = threading.Thread(target=self._per_second_event_loop)
        per_second_event_loop.daemon = True
        per_second_event_loop.start()

    def run_mainloop(self):
        self.root.mainloop()

    def run(self):
        self.run_eventloops()
        self.run_mainloop()








