const video=document.querySelector('#video'),metadata=document.querySelector('#metadata');
const observer='IntersectionObserver' in window?new IntersectionObserver(entries=>{if(!entries[0].isIntersecting)video.pause();}):null;observer?.observe(video);
let url,callback,disposed=false,suspended=false,activeStream,recorder,stopRecording=()=>{};
function sync(mediaTime=video.currentTime){document.querySelector('#timeline').textContent=`Media time: ${mediaTime.toFixed(2)} s`;}
function requestFrame(){if(disposed||suspended||video.paused)return;if('requestVideoFrameCallback' in video)callback=video.requestVideoFrameCallback((_,info)=>{sync(info.mediaTime);requestFrame();});}
function attach(blob,name){video.pause();if(url)URL.revokeObjectURL(url);url=URL.createObjectURL(blob);video.src=url;metadata.textContent=`${name}: ${blob.size} bytes; ${blob.type||'container/codec unknown'}. Waiting for metadata.`;video.onloadedmetadata=()=>{metadata.textContent+=` ${video.videoWidth} × ${video.videoHeight}; ${Number.isFinite(video.duration)?video.duration.toFixed(2)+' s':'duration unavailable until decoded'}. Audio tracks and codec require a media inspector for arbitrary files.`;};}
video.addEventListener('play',requestFrame);
video.addEventListener('pause',()=>{if(callback!==undefined)video.cancelVideoFrameCallback?.(callback);});
for(const event of ['seeked','loadeddata','timeupdate'])video.addEventListener(event,()=>sync());
video.addEventListener('error',()=>{metadata.textContent='Playback failed. Keep the original; choose a browser-supported derivative or use a static alternative.';});
document.querySelector('#file').onchange=e=>{const file=e.target.files[0];if(file)attach(file,file.name);};
document.querySelector('#synthetic').onclick=async()=>{
  const button=document.querySelector('#synthetic');
  if(!window.MediaRecorder||!HTMLCanvasElement.prototype.captureStream){metadata.textContent='Local recording is unavailable. Choose an existing clip.';return;}
  button.disabled=true;const canvas=document.querySelector('#source'),ctx=canvas.getContext('2d');activeStream=canvas.captureStream(30);
  const mime=['video/webm;codecs=vp9','video/webm;codecs=vp8','video/mp4'].find(type=>MediaRecorder.isTypeSupported(type));
  let aborted=false,captureFrame;
  const chunks=[];recorder=new MediaRecorder(activeStream,mime?{mimeType:mime}:{});
  recorder.ondataavailable=e=>chunks.push(e.data);
  recorder.onstop=()=>{activeStream.getTracks().forEach(track=>track.stop());if(!disposed&&!aborted)attach(new Blob(chunks,{type:recorder.mimeType}),'Synthetic original / 640 × 360 / 30 requested fps / silent');button.disabled=false;};
  stopRecording=()=>{aborted=true;cancelAnimationFrame(captureFrame);if(recorder.state==='recording')recorder.stop();activeStream.getTracks().forEach(track=>track.stop());};
  recorder.start();const start=performance.now();
  function draw(now){if(disposed||suspended||aborted)return;const p=Math.min((now-start)/2000,1);ctx.fillStyle='#263c36';ctx.fillRect(0,0,640,360);ctx.fillStyle='#ed755b';ctx.beginPath();ctx.arc(80+p*480,180,32,0,Math.PI*2);ctx.fill();if(p<1)captureFrame=requestAnimationFrame(draw);else recorder.stop();}
  captureFrame=requestAnimationFrame(draw);
};
document.addEventListener('visibilitychange',()=>{if(document.hidden)video.pause();});
// A persisted page keeps its owned clip URL, but suspends all playback/recording.
addEventListener('pagehide',event=>{
  suspended=true;observer?.disconnect();video.pause();
  if(callback!==undefined)video.cancelVideoFrameCallback?.(callback);
  stopRecording();
  if(!event.persisted){disposed=true;if(url){URL.revokeObjectURL(url);url=undefined;}}
});
addEventListener('pageshow',event=>{
  if(event.persisted&&!disposed){suspended=false;observer?.observe(video);sync();}
});
