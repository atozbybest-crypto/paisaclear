
from PIL import Image, ImageDraw, ImageFont
import pathlib

OUT = pathlib.Path("brand"); OUT.mkdir(exist_ok=True)
PAPER=(247,244,236); INK=(20,35,28); GREEN=(15,81,50); MUTED=(90,104,96); LINE=(214,208,194)
BOLD=r"C:\Windows\Fonts\segoeuib.ttf"; SEMI=r"C:\Windows\Fonts\seguisb.ttf"; REG=r"C:\Windows\Fonts\segoeui.ttf"
def f(p,s):
    try: return ImageFont.truetype(p,s)
    except Exception: return ImageFont.load_default()

def wrap(d, text, font, width):
    words, lines, cur = text.split(), [], ""
    for w in words:
        t=(cur+" "+w).strip()
        if d.textlength(t,font=font)<=width: cur=t
        else:
            if cur: lines.append(cur)
            cur=w
    if cur: lines.append(cur)
    return lines

def headline(d, text, width, start=74, minimum=52, max_lines=2):
    size = start
    while size > minimum:
        font = f(BOLD, size)
        lines = wrap(d, text, font, width)
        if len(lines) <= max_lines:
            return font, lines, size
        size -= 3
    font = f(BOLD, minimum)
    return font, wrap(d, text, font, width)[:max_lines], minimum

def build(W,H,path):
    img=Image.new("RGB",(W,H),PAPER); d=ImageDraw.Draw(img)
    d.rectangle([0,0,W,12],fill=GREEN)

    fb=f(BOLD,38); d.text((72,68),"Paisa",font=fb,fill=INK)
    w=d.textlength("Paisa",font=fb); d.text((72+w,68),"Clear",font=fb,fill=GREEN)
    tag="FREE · NO SIGN-UP"
    d.text((W-72-d.textlength(tag,font=f(SEMI,20)),78),tag,font=f(SEMI,20),fill=MUTED)

    y = int(H*0.17)
    d.text((72,y),"INDIAN FINANCIAL PRODUCTS, IN PLAIN LANGUAGE",font=f(SEMI,22),fill=GREEN)
    y += 58

    font, lines, size = headline(d,"Understand the product before you put money in it.", W-144)
    for line in lines:
        d.text((72,y),line,font=font,fill=INK); y += int(size*1.2)

    y += 26
    d.line([(72,y),(W-72,y)],fill=LINE,width=2); y += 40

    stats=[("226","products"),("6","categories"),("5","calculators")]
    col=(W-144)//3
    for i,(n,label) in enumerate(stats):
        x=72+i*col
        d.text((x,y),n,font=f(BOLD,72),fill=GREEN)
        d.text((x,y+92),label,font=f(REG,28),fill=MUTED)
    y += 184

    d.line([(72,y),(W-72,y)],fill=LINE,width=2); y += 40

    for b in ("Every figure carries the date it applied",
              "A link to the source on every product",
              "Nothing sold: no payments, no sign-up"):
        d.ellipse([72,y+13,84,y+25],fill=GREEN)
        d.text((100,y),b,font=f(REG,30),fill=INK); y += 54

    d.line([(72,H-190),(W-72,H-190)],fill=LINE,width=2)
    d.text((72,H-152),"paisaclear.co.in",font=f(BOLD,46),fill=GREEN)
    d.text((72,H-86),"Government schemes · Deposits · Funds · Bonds · ETFs · Insurance",font=f(REG,22),fill=MUTED)

    img.save(OUT/path,"PNG",optimize=True)
    return path

build(1080,1350,"intro-post-portrait.png")
build(1080,1080,"intro-post-square.png")
print("intro posts rebuilt")
