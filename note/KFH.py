add_word(0xDEADC0DE)
add_word(0xDEADC0DE)

add_word(0x00000000)

fill(0x1E, 0x0)

add_utf16("NoteHax")
fill(0x16-len("NoteHax")*2, 0x0)

add_utf16("By")
fill(0x16-len("By")*2, 0x0)

add_utf16("Nba_Yoh")
fill(0x16-len("Nba_Yoh")*2, 0x0)

for i in range(3):
    add_ascii("notehax"*4)

add_word(0x00000001)
add_halfword(0x0002)
add_halfword(0x0003)
