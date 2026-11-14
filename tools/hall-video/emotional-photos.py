#!/usr/bin/env python3
import concurrent.futures,urllib.request,pathlib,subprocess,json
PHOTOS=[[4737203,"old-photo-in-hand"],[24837736,"empty-chair"],[25811135,"old-photo-collection"],[31452619,"rain-window-silhouette"],[31901592,"woman-at-window"],[20473496,"hands-on-wet-glass"],[28571112,"candle-rain-window"],[10272700,"developed-photograph"],[3144296,"figure-by-window"],[18718971,"dark-corridor-person"],[4930104,"window-reflection"],[31165186,"two-on-bench"],[10815759,"lonely-waterfront"],[9352107,"chair-and-curtains"],[15146506,"lonely-man-night"],[18540099,"person-dark-window"],[14198668,"figure-dim-room"],[23391610,"elder-by-sea"],[17683513,"solo-harbor"],[30622463,"solo-figure-window"],[9371564,"black-white-silhouette"],[6113791,"dark-gesture"],[9410391,"reaching-into-light"],[5234193,"hands-together"],[14467148,"hand-reaching-light"],[8684458,"hand-into-light"],[10425282,"person-on-city-bench"],[16230982,"hands-monochrome"],[7216020,"large-empty-echo-hall"]]
base=pathlib.Path("hall-emotional-assets/photos");base.mkdir(parents=True,exist_ok=True)
def fetch(item):
 i,(pid,title)=item
 url=f"https://images.pexels.com/photos/{pid}/pexels-photo-{pid}.jpeg?auto=compress&cs=tinysrgb&w=2200"
 p=base/f"{i:02d}-{pid}.jpg"
 req=urllib.request.Request(url,headers={"User-Agent":"Mozilla/5.0","Accept":"image/jpeg,image/*"})
 with urllib.request.urlopen(req,timeout=90) as resp,open(p,"wb") as f:
  for chunk in iter(lambda:resp.read(1024*1024),b""):
   f.write(chunk)
 if p.stat().st_size<12000:raise ValueError(f"Too small: {pid}")
 return {"id":pid,"title":title,"filename":p.name,"page":f"https://www.pexels.com/photo/{pid}/","url":url,"bytes":p.stat().st_size}
with concurrent.futures.ThreadPoolExecutor(max_workers=5) as pool:
 result=list(pool.map(fetch,enumerate(PHOTOS)))
(base/"SOURCES.json").write_text(json.dumps(result,indent=2))
print("PHOTOS DONE:",len(result),sum(x["bytes"] for x in result))
