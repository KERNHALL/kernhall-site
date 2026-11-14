#!/usr/bin/env python3
import concurrent.futures,urllib.request,pathlib,subprocess,json,os
VIDEOS=[[7546133,"old-photographs"],[6959726,"hands-together"],[9945249,"rain-glass"],[11349554,"walking-in-mist"],[4122384,"dust-in-light"],[10473225,"holding-old-photo"],[5234909,"dust-particles"],[11349555,"wet-path-reflection"],[5168872,"holding-hands-close"],[29725267,"solitary-fog-night"],[4725696,"rain-glass-close"],[38883117,"dust-through-window"],[8057927,"man-remembers-photograph"],[18089050,"walking-away-light"]]
base=pathlib.Path("hall-emotional-assets/videos");base.mkdir(parents=True,exist_ok=True)
raw=base/"raw";raw.mkdir(exist_ok=True)
def fetch(item):
 i,(vid,title)=item
 url=f"https://www.pexels.com/download/video/{vid}/"
 r=raw/f"{i:02d}-{vid}.mp4"
 req=urllib.request.Request(url,headers={"User-Agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/123.0.0.0 Safari/537.36","Accept":"video/mp4,*/*"})
 with urllib.request.urlopen(req,timeout=120) as resp,open(r,"wb") as f:
  for c in iter(lambda:resp.read(1024*1024),b""):f.write(c)
 if r.stat().st_size<50000: raise ValueError(f"Missing source {vid}")
 out=base/f"{i:02d}-{vid}.mp4"
 cmd=["ffmpeg","-hide_banner","-loglevel","error","-y","-i",str(r),"-ss","0.25","-t","6.8","-vf","fps=24,scale=1280:720:force_original_aspect_ratio=increase,crop=1280:720,eq=saturation=0.76:contrast=1.045,format=yuv420p","-an","-c:v","libx264","-preset","veryfast","-crf","27",str(out)]
 subprocess.run(cmd,check=True)
 seconds=float(subprocess.check_output(["ffprobe","-v","error","-show_entries","format=duration","-of","default=noprint_wrappers=1:nokey=1",str(out)]).decode().strip())
 r.unlink()
 return {"id":vid,"title":title,"filename":out.name,"page":f"https://www.pexels.com/video/{vid}/","seconds":seconds,"bytes":out.stat().st_size}
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:
 result=list(pool.map(fetch,enumerate(VIDEOS)))
(base/"SOURCES.json").write_text(json.dumps(result,indent=2))
raw.rmdir()
print("VIDEOS DONE:",len(result),sum(x["bytes"] for x in result))
