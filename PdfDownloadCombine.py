import requests
import fitz # pip install PyMuPDF
import time

pdfs = []
upper = 968
for x in range(1, upper+1):
    url = f"https://babel.hathitrust.org/cgi/imgsrv/download/pdf?id=umn.31951p003993520&attachment=1&seq={x}&tracker=D2%3A"
    pdfFile = f"{x}.pdf"
    needIt = True
    loops = 0
    while needIt:
        loops+=1
        r = requests.get(url, allow_redirects=True)
        if r.status_code == 200:        
            open(pdfFile, "wb").write(r.content)
            pdfs.append(pdfFile)
            needIt = False
            print(f"Eh! {x} of {upper} done! Baddabing! Badam!")    
        else:
            naptime = 2 ** loops
            print(f"NAPTIME for {naptime}s!")
            time.sleep(naptime) # 2 to the power of loops, so 1, 2, 4, 8, 16, etc.

print("Lookin' good! We should get matching track suits!")

print("...")
print("Activating COMBINOTRON 2000")
print("...")
doc = fitz.open()
for pdf in pdfs:
    print(f"Combining {pdf}...")
    infile = fitz.open(pdf)
    doc.insertPDF(infile)
    infile.close()
doc.save("out.pdf", deflate=True, garbage=3)
print("Combining COMPLETED!!! BOOOOOOOP!!!")