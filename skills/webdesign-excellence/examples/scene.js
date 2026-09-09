import * as THREE from 'three';
import { GLTFLoader } from 'three/addons/loaders/GLTFLoader.js';

export async function mountScene(assetURL='assets/lumen.gltf') {
  window.exampleScene?.dispose();
  const host=document.querySelector('#scene'), status=document.querySelector('#scene-status');
  const controller=new AbortController(), {signal}=controller;
  const preference=matchMedia('(prefers-reduced-motion: reduce)');
  const labels=[...document.querySelectorAll('#scene-labels span')];
  let renderer, model, disposed=false, frame=0, progress=0, target=0, last=0, angle=0;
  const scene=new THREE.Scene();scene.background=new THREE.Color('#e6e5dc');
  const camera=new THREE.PerspectiveCamera(32,1,.05,30);
  const world=new THREE.Vector3(), direction=new THREE.Vector3(), raycaster=new THREE.Raycaster();
  const ownedGeometry=new Set(),ownedMaterial=new Set();
  function own(object){object.traverse(node=>{if(node.isMesh){ownedGeometry.add(node.geometry);for(const m of Array.isArray(node.material)?node.material:[node.material])ownedMaterial.add(m);}});return object;}
  function fail(message){status.textContent=message;labels.forEach(label=>label.style.visibility='hidden');}
  try {renderer=new THREE.WebGLRenderer({antialias:true});}catch {fail('3D unavailable. Read the three-part description below.');return;}
  renderer.setPixelRatio(Math.min(devicePixelRatio,1.5));renderer.shadowMap.enabled=true;renderer.shadowMap.type=THREE.PCFSoftShadowMap;
  renderer.toneMapping=THREE.ACESFilmicToneMapping;renderer.toneMappingExposure=1.15;host.replaceChildren(renderer.domElement);
  scene.add(new THREE.HemisphereLight('#fff6e7','#75867b',2));
  const key=new THREE.DirectionalLight('#fff5dc',4);key.position.set(-3,5,4);key.castShadow=true;key.shadow.mapSize.set(1024,1024);key.shadow.camera.left=-3;key.shadow.camera.right=3;key.shadow.camera.top=3;key.shadow.camera.bottom=-3;key.shadow.normalBias=.025;scene.add(key);
  const rim=new THREE.DirectionalLight('#dde9ff',2);rim.position.set(3,3,-3);scene.add(rim);
  const floor=own(new THREE.Mesh(new THREE.PlaneGeometry(200,200),new THREE.MeshStandardMaterial({color:'#e6e5dc',roughness:1})));floor.rotation.x=-Math.PI/2;floor.position.y=-.005;floor.receiveShadow=true;scene.add(floor);
  const roots=new Map();
  function frameCamera(){
    const width=host.clientWidth,height=host.clientHeight;if(!width||!height)return;
    renderer.setSize(width,height,false);camera.aspect=width/height;
    // Fit the entire reveal envelope, including narrow views; text occupies separate DOM space.
    const vertical=2.55,horizontal=2.15;
    const distance=Math.max(vertical,horizontal/camera.aspect)/(2*Math.tan(THREE.MathUtils.degToRad(camera.fov/2)))*1.2;
    camera.position.set(Math.sin(angle+.55)*distance,.95+distance*.3,Math.cos(angle+.55)*distance);
    camera.lookAt(0,1.05,0);camera.updateProjectionMatrix();render();
  }
  function projectLabels(){
    if(!model)return;model.updateMatrixWorld(true);camera.updateMatrixWorld(true);
    const occupied=[];
    for(const label of labels){
      const node=model.getObjectByName(label.dataset.part);node.getWorldPosition(world);
      if(label.dataset.part==='shade')world.y+=.18;
      world.x+=.45;
      const distance=camera.position.distanceTo(world);direction.copy(world).sub(camera.position).normalize();raycaster.set(camera.position,direction);
      const hit=raycaster.intersectObject(model,true)[0];
      const hidden=hit&&hit.object!==node&&hit.distance<distance-.12;
      world.project(camera);let x=(world.x*.5+.5)*host.clientWidth+30,y=(-world.y*.5+.5)*host.clientHeight;
      x=Math.max(8,Math.min(host.clientWidth-label.offsetWidth-8,x));y=Math.max(8,Math.min(host.clientHeight-50,y));
      for(const prior of occupied)if(Math.abs(prior-y)<30)y=prior+30;
      const visible=!hidden&&world.z>=-1&&world.z<=1&&y<host.clientHeight-35;
      label.style.visibility=visible?'visible':'hidden';label.style.transform=`translate(${x}px,${y}px)`;if(visible)occupied.push(y);
    }
  }
  function render(){if(disposed)return;renderer.render(scene,camera);projectLabels();}
  // Absolute canonical transforms make forward/reverse sampling and reassembly drift-free.
  function sampleAssembly(p){
    progress=Math.max(0,Math.min(1,p));target=progress;
    if(model)for(const [name,original] of roots){const node=model.getObjectByName(name);node.position.copy(original);if(name==='shade'||name==='cap')node.position.y+=progress*.65;if(name==='diffuser'){node.position.y+=progress*.2;node.position.x+=progress*.65;}}
    document.querySelector('#assembly').value=progress;document.querySelector('#reveal').textContent=progress>.5?'Reassemble':'Reveal parts';render();
  }
  function animate(now){const next=target;const delta=Math.min((now-last)/650,1);last=now;const p=progress+Math.sign(next-progress)*Math.min(Math.abs(next-progress),delta);sampleAssembly(p);target=next;document.querySelector('#reveal').textContent=target>.5?'Reassemble':'Reveal parts';if(progress!==target)frame=requestAnimationFrame(animate);}
  function pause(){cancelAnimationFrame(frame);target=progress;}
  function dispose(){if(disposed)return;disposed=true;pause();controller.abort();observer.disconnect();preference.removeEventListener('change',preferenceChanged);ownedGeometry.forEach(g=>g.dispose());ownedMaterial.forEach(m=>m.dispose());key.shadow.dispose();renderer.dispose();renderer.domElement.remove();labels.forEach(label=>label.style.visibility='hidden');}
  function preferenceChanged(){pause();sampleAssembly(progress>=.5?1:0);}
  const observer=new ResizeObserver(frameCamera);observer.observe(host);
  preference.addEventListener('change',preferenceChanged);
  document.querySelector('#assembly').addEventListener('input',e=>{pause();sampleAssembly(e.target.valueAsNumber);},{signal});
  document.querySelector('#reveal').addEventListener('click',()=>{const next=target>.5?0:1;pause();target=next;if(preference.matches)sampleAssembly(target);else{last=performance.now();frame=requestAnimationFrame(animate);}},{signal});
  document.querySelector('#rotate').addEventListener('click',()=>{angle=angle===0?Math.PI:0;frameCamera();},{signal});
  document.addEventListener('visibilitychange',()=>{if(document.hidden)pause();},{signal});
  renderer.domElement.addEventListener('webglcontextlost',e=>{e.preventDefault();pause();fail('3D context lost. Descriptions and controls remain available; reload to restore the view.');},{signal});
  addEventListener('pagehide',dispose,{signal});
  window.exampleScene={sampleAssembly,dispose,mount:mountScene,stats:()=>({progress,meshes:roots.size,calls:renderer.info.render.calls,triangles:renderer.info.render.triangles,geometries:renderer.info.memory.geometries,disposed,positions:model?Object.fromEntries([...roots.keys()].map(name=>[name,model.getObjectByName(name).position.toArray()])):{}})};
  try {
    const gltf=await new GLTFLoader().loadAsync(assetURL);
    if(disposed){own(gltf.scene);ownedGeometry.forEach(g=>g.dispose());ownedMaterial.forEach(m=>m.dispose());return;}
    model=own(gltf.scene);scene.add(model);model.traverse(node=>{if(node.isMesh){roots.set(node.name,node.position.clone());node.castShadow=true;node.receiveShadow=true;}});
    status.textContent='Original form study / 5 modeled parts';frameCamera();sampleAssembly(0);
  }catch{if(!disposed)fail('Model could not load. The three-part description below remains available.');}
  return window.exampleScene;
}

addEventListener('pageshow',event=>{if(event.persisted&&window.exampleScene?.stats().disposed)mountScene();});
