from pptx import Presentation
from pptx.util import *
from pptx.enum.text import PP_ALIGN
from pptx.dml.color import RGBColor
import os,sys
from io import BytesIO
from mutagen.mp3 import MP3
from mutagen.id3 import ID3
from PIL import Image
from data import MusicLibrary
import os
import json
# hash : song _ data : track number title album Artist
import qrcode
# importing the date class datetime module
from datetime import date
current_date = date.today()
# creating the date object of today's date
current_year = current_date.year
import hashlib

from mutagen.mp3 import MP3
from mutagen.easyid3 import EasyID3


set_name = 'The Raccoon'
set_logo = set_name+ '.png'


img_path = 'ForgedCards\\template\\ribbon.png'
prs = Presentation()
prs.slide_width = Cm(6)
prs.slide_height = Cm(9)
blank_slide_layout = prs.slide_layouts[6]
##
set_name = 'The Raccoon'
playlist_filepath = os.path.normpath('H:/Music/Playlists/'+set_name +'.m3u' )
with open(playlist_filepath) as f:
    content = f.readlines()
music_filepaths = [x.replace('../', '').strip() for x in content]
n = 0
for music_file in music_filepaths:

    if music_file.endswith(".mp3"):
        n = n+1
        song_info = MP3(music_file, ID3=EasyID3)
        stringf = "{0} - {1} - {2} - {3}".format(
            song_info['tracknumber'][0],
            song_info['title'][0],
            song_info['album'][0],
            song_info['artist'][0]
        )
        hash_object = hashlib.md5(stringf.encode())
        hasheds = str( hash_object.hexdigest()[0:10])

        qr_code = qrcode.make(hasheds)
        # save img to a file
        qr_code.save('ForgedCards/tmp/qr_code.png')



        tags = ID3(music_file)
        pict = tags.get("APIC:").data
        im = Image.open(BytesIO(pict))
        im.save('ForgedCards/tmp/album_cover.png')

        # FRONT SLIDE
        front_slide = prs.slides.add_slide(blank_slide_layout)
        top = left = Cm(0)
        pic = front_slide.shapes.add_picture(os.path.normpath('ForgedCards/tmp/album_cover.png'), Cm(0.4), Cm(0.4), Cm(5.2), Cm(5.2))

        artist_txBox = front_slide.shapes.add_textbox(Cm(0.4), Cm(5.8), Cm(5.2), Cm(1))
        artist_text_frame = artist_txBox.text_frame
        artist_text_frame.clear()
        artist_p = artist_text_frame.paragraphs[0]
        artist_run = artist_p.add_run()

        artist_run.text = song_info['artist'][0].upper()
        artist_font = artist_run.font
        artist_font.name = 'Selawik'
        artist_font.size = Pt(8)
        artist_font.bold = True
        artist_font.italic = None
        artist_font.color.rgb = RGBColor(0, 0, 0)
        artist_text_frame.margin_top = Cm(0.1)
        artist_text_frame.margin_bottom = Cm(0.1)
        artist_text_frame.margin_right = Cm(0)
        artist_text_frame.margin_left = Cm(0)

        song_txBox = front_slide.shapes.add_textbox(Cm(0.4), Cm(6.3), Cm(5.2), Cm(1))
        song_text_frame = song_txBox.text_frame
        song_text_frame.clear()
        song_p = song_text_frame.paragraphs[0]
        song_run = song_p.add_run()

        song_run.text = ' '.join(elem.capitalize() for elem in song_info['title'][0].split())
        song_font = song_run.font
        song_font.name = 'Selawik'
        song_font.size = Pt(7)
        song_font.bold = False
        song_font.italic = None
        song_font.color.rgb = RGBColor(0, 0, 0)
        song_text_frame.margin_top = Cm(0.1)
        song_text_frame.margin_bottom = Cm(0.1)
        song_text_frame.margin_right = Cm(0)
        song_text_frame.margin_left = Cm(0)


        # bottom left
        bottom_left_txBox = front_slide.shapes.add_textbox(Cm(0.4), Cm(8.4), Cm(2.6), Cm(0.5))
        bottom_left_text_frame = bottom_left_txBox.text_frame
        bottom_left_text_frame.clear()
        bottom_left_p = bottom_left_text_frame.paragraphs[0]
        bottom_left_run = bottom_left_p.add_run()

        bottom_left_run.text = song_info['tracknumber'][0] + ' ' + song_info['date'][0] + ' SAM\'S JUKEBOX'
        bottom_left_font = bottom_left_run.font
        bottom_left_font.name = 'Selawik'
        bottom_left_font.size = Pt(5)
        bottom_left_font.color.rgb = RGBColor(0, 0, 0)
        bottom_left_text_frame.margin_top = Cm(0.1)
        bottom_left_text_frame.margin_bottom = Cm(0.1)
        bottom_left_text_frame.margin_right = Cm(0)
        bottom_left_text_frame.margin_left = Cm(0)

        # bottom right
        bottom_right_txBox = front_slide.shapes.add_textbox(Cm(2.9), Cm(8.4), Cm(2.6), Cm(0.5))
        bottom_right_text_frame = bottom_right_txBox.text_frame
        bottom_right_text_frame.clear()
        bottom_right_p = bottom_right_text_frame.paragraphs[0]
        bottom_right_run = bottom_right_p.add_run()

        bottom_right_run.text = set_name + ' – ' + str(current_year) + ' ' + str('%02d'%(n)) + '/' + str('%02d'%(len(music_filepaths)))
        bottom_right_font = bottom_right_run.font
        bottom_right_font.name = 'Selawik'
        bottom_right_font.size = Pt(5)
        bottom_right_font.color.rgb = RGBColor(0, 0, 0)
        bottom_right_text_frame.margin_top = Cm(0.1)
        bottom_right_text_frame.margin_bottom = Cm(0.1)
        bottom_right_text_frame.margin_right = Cm(0)
        bottom_right_text_frame.margin_left = Cm(0)
        bottom_right_p.alignment = PP_ALIGN.RIGHT

        # Set logo
        pic = front_slide.shapes.add_picture('ForgedCards/'+ set_name +'/logo.png', Cm(4.4), Cm(7.4), Cm(1), Cm(1))



        # BACK SLIDE
        slide = prs.slides.add_slide(blank_slide_layout)
        #adding Qr code
        top = left = Cm(0)
        pic = slide.shapes.add_picture('ForgedCards/tmp/qr_code.png', left, top, Cm(6), Cm(6))

        #adding a ribbon
        left = Cm(0)
        top = Cm(7.6)
        pic = slide.shapes.add_picture(img_path, left, top)

        # add the text

        ### SAM'S JUKEBOX
        txBox = slide.shapes.add_textbox(Cm(0.3), Cm(6.05), Cm(5.40), Cm(1.05))
        text_frame = txBox.text_frame
        text_frame.clear()  # not necessary for newly-created shape
        p = text_frame.paragraphs[0]
        run = p.add_run()
        p.margin_top = Cm(0.13)
        p.margin_bottom = Cm(0.13)
        p.margin_right = Cm(0.25)
        p.margin_left = Cm(0.25)
        run.text = 'SAM\' JUKEBOX'
        font = run.font
        font.name = 'YellowTail'
        font.size = Pt(18)
        font.bold = False
        font.italic = None
        font.color.rgb = RGBColor(66, 66, 78)
        p.alignment = PP_ALIGN.CENTER


        ## The music in your hands
        txBox = slide.shapes.add_textbox(Cm(0.3), Cm(7.1), Cm(5.40), Cm(0.5))
        text_frame = txBox.text_frame
        text_frame.clear()  # not necessary for newly-created shape
        p = text_frame.paragraphs[0]
        run = p.add_run()
        p.margin_top = Cm(0.13)
        p.margin_bottom = Cm(0.13)
        p.margin_right = Cm(0.25)
        p.margin_left = Cm(0.25)

        run.text = 'T H E   M U S I C   I N   Y O U R   H A N D S'
        font = run.font
        font.name = 'Roboto Condensed'
        font.size = Pt(6)
        font.bold = False
        font.italic = None
        font.color.rgb = RGBColor(66, 66, 78)

        p.alignment = PP_ALIGN.CENTER

prs.save('ForgedCards\\test.pptx')



