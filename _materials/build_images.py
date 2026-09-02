from PIL import Image, ImageOps
import os
M="/Users/igormanka/Desktop/projekty/movilla2/_materials/Movilla str"
P="/private/tmp/claude-501/-Users-igormanka-Desktop-projekty-movilla2/1e597c7f-2868-4aa1-9ad6-7036c5a80fe7/scratchpad/pdfimg"
OUT="/Users/igormanka/Desktop/projekty/movilla2/img"
def m(n): return f"{M}/img/{n}"
def p(n): return f"{P}/{n}.png"
PHOTOS={
 "arc70":{"hero":m("01_front_facade.png"),"ext-2":m("01_front_facade_beautiful_poland.png"),"ext-3":m("01_front_facade_same_location.png"),
   "ext-4":m("1.png"),"ext-5":m("2.png"),"ext-6":m("3.png"),"lake-1":p("70ARC-001-000"),"vertical":p("70ARC-002-014"),"lake-2":p("70ARC-008-035"),
   "garage":p("70ARC-009-039"),"int-1":p("70ARC-003-021"),"int-2":p("70ARC-003-022"),"int-3":p("70ARC-003-023"),"int-4":p("70ARC-006-027")},
 "mysa120":{"hero":m("designed_arch_house_facade.png"),"ext-2":m("designed_arch_house_facade 2.png"),"ext-3":m("designed_arch_house_scandinavian_wood_foundation.png"),
   "ext-4":m("designed_arch_house_variant_01_scandinavian.png"),"balcony-1":m("edited_house_balcony_recessed_windows.png"),"balcony-2":m("edited_house_balcony_recessed_windows 2.png"),
   "family":m("edited_family_near_house_realistic.png"),"lake-1":p("MYSA120_compressed_2-006-026"),"lake-2":p("MYSA120_compressed_2-007-029"),"lake-3":p("MYSA120_compressed_2-007-030"),
   "garage":p("MYSA120_compressed_2-009-034"),"garage-terrace":p("MYSA120_compressed_2-009-036"),"vertical":p("MYSA120_compressed_2-014-065"),"lake-4":p("MYSA120_compressed_2-016-073"),
   "int-1":p("MYSA120_compressed_2-003-020"),"int-2":p("MYSA120_compressed_2-003-021"),"int-3":p("MYSA120_compressed_2-003-022"),"int-4":p("MYSA120_compressed_2-006-025"),"int-5":p("MYSA120_compressed_2-008-033")},
 "barn85":{"hero":m("new_house_scandinavian_lived_in_yard.png"),"ext-2":m("new_house_scandinavian_lived_in_yard_different_angle.png"),"ext-3":m("new_house_scandinavian_lived_in_yard_right_side_angle.png"),
   "aerial":p("BarnHouse130-002-003"),"int-1":p("BarnHouse85-003-010"),"int-2":p("BarnHouse85-003-011")},
 "barn130":{"hero":m("house_new_location_family_chocolate_labrador.png"),"night":p("BarnHouse130-001-000"),"vertical":p("BarnHouse130-010-047"),"aerial":p("BarnHouse130-002-003"),
   "ext-2":m("new_house_scandinavian_lived_in_yard_right_side_angle.png"),"int-1":p("BarnHouse130-003-010"),"int-2":p("BarnHouse130-003-011")},
 "forest":{"hero":m("Forest/house1_karpaty_final.png"),"ext-2":m("Forest/house3_les_final.png"),"glamping":m("Forest/glamping_5houses_ground.png"),"vertical":m("Forest/glamping_1080x1920_final.png"),
   "ext-3":m("Forest/WhatsApp Image 2026-05-15 at 16.46.59.jpeg"),"ext-4":p("forestv1_2-001-000"),"ext-5":p("forestv1_2-003-005"),
   "int-1":m("Forest/Image_20260629100347_142_236.png"),"int-2":m("Forest/Image_20260630170306_230_236.jpg"),"int-3":m("Forest/Image_20260630170307_231_236.png"),
   "int-4":m("Forest/Image_20260630170307_232_236.png"),"int-5":m("Forest/Image_20260630170308_233_236.png"),"int-6":m("Forest/Image_20260630170309_234_236.png"),
   "int-7":m("Forest/Image_20260630170310_235_236.jpg"),"int-8":m("Forest/Image_20260630170310_236_236.jpg"),"int-9":m("Forest/Image_20260630170312_238_236.jpg"),
   "int-10":p("forestv1_2-007-008"),"int-11":p("forestv1_2-007-009")},
 "common":{"tech-1":m("processed_construction_02.png"),"tech-2":m("processed_construction_03.png"),"builder":m("vertical_professional_builder_thumb_up_house_600x900.png"),
   "detail-wall":p("70ARC-010-043"),"detail-floor":p("70ARC-011-066"),"frame":p("70ARC-004-024")},
}
PLANS={
 "arc70":{"plan-open":p("70ARC-006-029"),"plan-full":p("70ARC-007-033"),"section":p("70ARC-005-025")},
 "mysa120":{"plan-open":p("MYSA120_compressed_2-007-031"),"section":p("70ARC-005-025")},
 "barn85":{"plan-parter":p("BarnHouse85-005-015"),"plan-antresola":p("BarnHouse85-005-017"),"section":p("BarnHouse85-004-013")},
 "barn130":{"plan-parter":p("BarnHouse130-005-015"),"plan-antresola":p("BarnHouse130-005-017"),"section":p("BarnHouse130-004-013")},
 "forest":{"plan-parter":p("forestv1_2-006-006"),"plan-pietro":p("forestv1_2-006-007"),"elev-1":p("forestv1_2-008-010"),"elev-2":p("forestv1_2-008-011")},
}
def save(im, path, w, q):
    im=im.copy(); 
    if im.width>w: im=im.resize((w,int(im.height*w/im.width)),Image.LANCZOS)
    im.save(path,"WEBP",quality=q,method=6)
for grp,d in PHOTOS.items():
    os.makedirs(f"{OUT}/{grp}",exist_ok=True)
    for name,src in d.items():
        im=ImageOps.exif_transpose(Image.open(src)).convert("RGB")
        save(im,f"{OUT}/{grp}/{name}.webp",1920,78)
        save(im,f"{OUT}/{grp}/{name}-960.webp",960,74)
for grp,d in PLANS.items():
    for name,src in d.items():
        im=Image.open(src)
        if im.mode in("RGBA","LA","P"):
            bg=Image.new("RGB",im.size,(255,255,255)); bg.paste(im.convert("RGBA"),mask=im.convert("RGBA").split()[3]); im=bg
        im=im.convert("RGB")
        # trim white
        inv=ImageOps.invert(im.convert("L")).point(lambda v:255 if v>12 else 0)
        bb=inv.getbbox()
        if bb: im=im.crop((max(bb[0]-30,0),max(bb[1]-30,0),min(bb[2]+30,im.width),min(bb[3]+30,im.height)))
        save(im,f"{OUT}/{grp}/{name}.webp",1600,88)
# logo / favicon
logo=Image.open(f"{M}/logo.png").convert("RGBA"); logo.save(f"{OUT}/logo.png"); 
bb=logo.getbbox(); logo=logo.crop(bb); logo.thumbnail((800,800)); logo.save(f"{OUT}/logo.webp","WEBP",quality=95,lossless=True)
fav=Image.open(f"{M}/favmovilla.png").convert("RGBA")
for s in (32,180,512): fav.resize((s,s),Image.LANCZOS).save(f"{OUT}/favicon-{s}.png")
print("done")
