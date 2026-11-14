#!/usr/bin/env python3
"""HALL stock-footage render. Each distinct Pexels clip once. No music in CI."""
import os,sys,subprocess,pathlib,concurrent.futures,urllib.request,urllib.error,json
from urllib.parse import urlparse
ROOT=pathlib.Path("hall-build"); ROOT.mkdir(exist_ok=True)
SRC=ROOT/"sources"; SRC.mkdir(exist_ok=True)
SEG=ROOT/"segments"; SEG.mkdir(exist_ok=True)
IDS=[29594574,8219164,5401861,19217894,30146335,4761733,10095265,7928972,2248637,7934652,10095255,3752637,31794185,11296534,35069286,12564705,35122649,2070037,33149173,31813741,14315016,19217898,34936158,31702087,10852299,19205430,38842352,31806786,5121701,32243771,14459264,31834970,20609204,5571779,3752640,31794139]
B=[0,8.824,15.418,22.291,29.304,36.548,43.328,50.736,55.960,62.067,68.778,75.929,80.016,86.703,94.087,99.915,107.880,114.590,121.231,128.592,135.187,142.060,146.680,153.739,160.798,167.811,173.314,180.280,184.506,189.753,194.978,198.438,202.083,205.404,208.887,211.069,215.203,219.624]
TEST=os.getenv("HALL_TEST","1")=="1"
if TEST:
 IDS=IDS[:2]
 B=[0,4.5,10]
def run(cmd):
 print("+"," ".join(str(x) for x in cmd),flush=True)
 subprocess.run(cmd,check=True)
def duration(p):
 return float(subprocess.check_output(["ffprobe","-v","error","-show_entries","format=duration","-of","default=noprint_wrappers=1:nokey=1",str(p)]).decode().strip())
def fetch(i,vid):
 url=f"https://www.pexels.com/download/video/{vid}/"
 req=urllib.request.Request(url,headers={"User-Agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/123.0.0.0 Safari/537.36","Accept":"video/mp4,*/*"})
 p=SRC/f"{i:02d}-{vid}.mp4"
 with urllib.request.urlopen(req,timeout=120) as resp,open(p,"wb") as f:
  print("Downloading:",url, "->",resp.url,flush=True)
  while True:
   data=resp.read(1024*1024)
   if not data:break
   f.write(data)
 if p.stat().st_size<50000:raise RuntimeError(f"Downloaded source too small: {p}")
 dur=duration(p); print(f"Downloaded {vid}: {p.stat().st_size/1e6:.1f} MB duration {dur:.1f}s",flush=True)
 return (i,p,dur,resp.url)
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:
 futures=[pool.submit(fetch,i,vid) for i,vid in enumerate(IDS)]
 outputs=[f.result() for f in futures]
sources={i:(p,dur,url) for i,p,dur,url in outputs}
segments=[]
for i,vid in enumerate(IDS):
 p,srcdur,url=sources[i]
 required=B[i+1]-B[i]
 # Slow footage only when source would otherwise be too short. No loops or repeated shots.
 rate=max(0.30,min(1.00,(srcdur-0.15)/required))
 filters=f"setpts=(PTS-STARTPTS)/{rate:.5f},fps=24,scale=1920:1080:force_original_aspect_ratio=increase,crop=1920:1080,eq=saturation=0.72:contrast=1.065:brightness=-0.02,format=yuv420p"
 target=SEG/f"shot-{i:02d}.mp4"
 run(["ffmpeg","-hide_banner","-loglevel","error","-y","-i",str(p),"-vf",filters,"-t",f"{required:.3f}","-an","-c:v","libx264","-preset","ultrafast","-crf","25","-pix_fmt","yuv420p","-movflags","+faststart",str(target)])
 segments.append(target)
concat=ROOT/"concat.txt"
concat.write_text("".join(f"file '{p.resolve()}'\n" for p in segments))
silent=pathlib.Path("HALL-FOOTAGE-ONLY-1080p.mp4")
run(["ffmpeg","-hide_banner","-loglevel","error","-y","-f","concat","-safe","0","-i",str(concat),"-c","copy","-movflags","+faststart",str(silent)])
manifest=[{"id":id,"source":sources[i][2],"start":B[i],"end":B[i+1],"used_once":True} for i,id in enumerate(IDS)]
pathlib.Path("HALL-FOOTAGE-LICENSE-SOURCES.json").write_text(json.dumps(manifest,indent=2))
print("FINISHED",silent,silent.stat().st_size,"bytes",duration(silent),"s",flush=True)
