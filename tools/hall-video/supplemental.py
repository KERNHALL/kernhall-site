#!/usr/bin/env python3
import concurrent.futures,urllib.request,pathlib,json
PHOTOS=[[13705890,"letter-writing"],[15829548,"long-shadows"],[6737254,"broken-mirror-face"],[5207601,"kept-letters-photograph"],[1669610,"shattered-reflection"],[30320607,"walking-away-sunset"],[25003042,"empty-chair-shore"],[4502523,"candle-in-window"],[9790376,"hands-letter"],[36959873,"three-shadows-beach"],[14780710,"person-alone-hall"],[33654941,"two-empty-chairs"],[3915968,"person-broken-mirror"],[9774248,"touching-broken-mirror"],[27165451,"empty-chair-on-pier"]]
base=pathlib.Path("hall-extra-photos");base.mkdir(exist_ok=True)
def fetch(item):
 i,(pid,title)=item
 url=f"https://images.pexels.com/photos/{pid}/pexels-photo-{pid}.jpeg?auto=compress&cs=tinysrgb&w=2200"
 dst=base/f"{i:02d}-{pid}.jpg"
 req=urllib.request.Request(url,headers={"User-Agent":"Mozilla/5.0","Accept":"image/jpeg,image/*"})
 with urllib.request.urlopen(req,timeout=90) as resp,open(dst,"wb") as f:
  for c in iter(lambda:resp.read(1024*1024),b""):f.write(c)
 if dst.stat().st_size<12000:raise RuntimeError("tiny image")
 return {"id":pid,"title":title,"filename":dst.name,"source":f"https://www.pexels.com/photo/{pid}/"}
with concurrent.futures.ThreadPoolExecutor(max_workers=5) as pool: res=list(pool.map(fetch,enumerate(PHOTOS)))
(base/"SOURCES.json").write_text(json.dumps(res,indent=2))
print("SUPPLEMENTAL PHOTO SOURCES",len(res))
