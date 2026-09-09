export function mountMotion() {
window.exampleMotion?.dispose();
const $ = selector => document.querySelector(selector);
const preference = matchMedia('(prefers-reduced-motion: reduce)');
const clamp = x => Math.max(0, Math.min(1, x));
const ease = x => { x = clamp(x); return x*x*(3-2*x); };
let progress = 0, playing = false, frame = 0, last = 0;
// Direct sampling: holds at 0–.16, .42–.56 and .84–1; no callbacks establish state.
function sampleKinetic(p) {
  progress = clamp(p);
  const connect = ease((progress-.16)/.26), handoff = ease((progress-.56)/.28);
  $('.track').style.transform = `scaleX(${.05+.95*connect})`;
  $('.orbit').style.transform = `scale(${1-.2*connect})`;
  $('.word-one').style.opacity = 1-handoff;
  $('.word-one').style.transform = `translateY(${-24*handoff}px)`;
  $('.word-two').style.opacity = handoff;
  $('.word-two').style.transform = `translateY(${24*(1-handoff)}px)`;
  $('#kinetic-progress').value = progress;
  $('#kinetic-state').value = progress<.16?'Entry':progress<.56?'Connection':progress<.84?'Handoff':'Readable hold';
}
function stop() { playing=false; cancelAnimationFrame(frame); $('#kinetic-play').textContent='Play sequence'; }
function tick(now) {
  if (!playing) return;
  sampleKinetic(progress+(now-last)/6000); last=now;
  if(progress>=1) stop(); else frame=requestAnimationFrame(tick);
}
function play() {
  if(preference.matches){sampleKinetic(1);stop();return;}
  if(progress>=1) sampleKinetic(0);
  playing=true;last=performance.now();$('#kinetic-play').textContent='Pause sequence';frame=requestAnimationFrame(tick);
}
$('#kinetic-play').onclick=()=>playing?stop():play();
$('#kinetic-replay').onclick=()=>{stop();sampleKinetic(0);play();};
$('#kinetic-progress').oninput=e=>{stop();sampleKinetic(e.target.valueAsNumber);};
let tokenAnimation, pathAnimation;
function cancelWorkflow(){tokenAnimation?.cancel();pathAnimation?.cancel();}
function identity(){const name=$('#format').selectedOptions[0].textContent.split(' /')[0];$('#edition-name').textContent=name.toUpperCase();$('#format-identity').textContent=`${name} / ${$('#format').value}`;}
$('#format').onchange=()=>{cancelWorkflow();identity();$('#calculation-path').classList.remove('calculated');$('#token-pages').textContent=$('#format').value;$('#estimate-result').value='Format changed. Create a new estimate.';};
$('#estimate-form').onsubmit=e=>{
  e.preventDefault();const pages=Number($('#format').value);
  // Business result is synchronous; illustrative motion never invents pending or success.
  $('#estimate-result').value=`${(50*pages).toLocaleString('en-US')} printed pages`;
  cancelWorkflow();identity();$('#calculation-path').classList.add('calculated');
  if(!preference.matches) {
    tokenAnimation=$('#edition-token').animate([{transform:'scale(1)'},{transform:'scale(.96)',offset:.3},{transform:'scale(1)'}],{duration:300,easing:'ease-out'});
    pathAnimation=$('#calculation-path').animate([{clipPath:'inset(0 100% 0 0)'},{clipPath:'inset(0 0% 0 0)'}],{duration:500,easing:'cubic-bezier(.2,.8,.2,1)'});
  }
};
function changePreference(){stop();cancelWorkflow();sampleKinetic(preference.matches?1:progress);}
preference.addEventListener('change',changePreference);
function visibility(){if(document.hidden)stop();}
document.addEventListener('visibilitychange',visibility);
function dispose(){stop();cancelWorkflow();preference.removeEventListener('change',changePreference);document.removeEventListener('visibilitychange',visibility);removeEventListener('pagehide',dispose);for(const selector of ['#kinetic-play','#kinetic-replay'])$(selector).onclick=null;$('#kinetic-progress').oninput=null;$('#format').onchange=null;$('#estimate-form').onsubmit=null;}
addEventListener('pagehide',dispose);
window.exampleMotion={sampleKinetic,getState:()=>({progress,playing}),stop,dispose,mount:mountMotion};
sampleKinetic(preference.matches?1:0);

return window.exampleMotion;
}
mountMotion();

addEventListener('pageshow',event=>{if(event.persisted)mountMotion();});
