#!/usr/bin/env python3
import pathlib,json,concurrent.futures,urllib.request,subprocess
ids=[
7216020,7216016,31312633,16803970,6695388,5505171,
7911699,5212117,7651301,27901403,1804171,4012056,
28847247,13984040,4577394,31786110,31358274,17871326,
]
out=pathlib.Path("HALL-PHOTO-SOURCES");out.mkdir(exist_ok=True)
def fetch(i,photo_id):
 url=f"https://images.pexels.com/photos/{photo_id}/pexels-photo-{photo_id}.jpeg?auto=compress&cs=tinysrgb&w=2000"
 target=out/f"{i:02d}-pexels-{photo_id}.jpg"
 req=urllib.request.Request(url,headers={"User-Agent":"Mozilla/5.0","Accept":"image/jpeg,image/*"})
 with urllib.request.urlopen(req,timeout=70) as resp,open(target,"wb") as f:
  for c in iter(lambda:resp.read(1024*1024),b""):f.write(c)
 if target.stat().st_size<15000:raise ValueError(f"Photo too small {photo_id}")
 data=subprocess.check_output(["file","--brief",str(target)]).decode().strip()
 if not ("JPEG" in data or "image" in data.lower()):raise ValueError((photo_id,data))
 return {"photo_id":photo_id,"url":url,"source_page":f"https://www.pexels.com/photo/{photo_id}/","file":target.name,"bytes":target.stat().st_size,"mime":data}
with concurrent.futures.ThreadPoolExecutor(max_workers=5) as pool:
 result=list(pool.map(lambda x:fetch(*x),enumerate(ids)))
(out/"SOURCES.json").write_text(json.dumps(result,indent=2))
print("FINISHED",len(result),"photos",sum(x["bytes"] for x in result),"bytes")
