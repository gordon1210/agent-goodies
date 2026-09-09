"""Reproduce the original Lumen fixture; meters, Y-up, no external assets."""
import base64
import json
import math
from pathlib import Path
import struct

model = {'asset': {'version': '2.0', 'generator': 'Original Lumen lathe authoring script'}, 'scene': 0,
         'scenes': [{'nodes': []}], 'nodes': [], 'meshes': [], 'materials': [], 'accessors': [], 'bufferViews': []}
buffer = bytearray()

def accessor(values, kind, width, component=5126):
    while len(buffer) % 4:
        buffer.append(0)
    start = len(buffer)
    buffer.extend(struct.pack('<' + ('f' if component == 5126 else 'H') * len(values), *values))
    view = len(model['bufferViews'])
    model['bufferViews'].append({'buffer': 0, 'byteOffset': start, 'byteLength': len(buffer)-start})
    item = {'bufferView': view, 'componentType': component, 'count': len(values)//width, 'type': kind}
    if width == 3:
        item.update(min=[min(values[i::3]) for i in range(3)], max=[max(values[i::3]) for i in range(3)])
    model['accessors'].append(item)
    return len(model['accessors'])-1

def lathe(name, profile, color, roughness, metalness, position=(0,0,0)):
    positions, normals, indices = [], [], []
    segments = 64
    for j, (radius,y) in enumerate(profile):
        before, after = profile[max(0,j-1)], profile[min(len(profile)-1,j+1)]
        dr, dy = after[0]-before[0], after[1]-before[1]
        length = math.hypot(dr,dy) or 1
        for i in range(segments+1):
            theta = i*math.tau/segments
            positions.extend([radius*math.sin(theta),y,radius*math.cos(theta)])
            normals.extend([dy/length*math.sin(theta),-dr/length,dy/length*math.cos(theta)])
    for j in range(len(profile)-1):
        for i in range(segments):
            a=j*(segments+1)+i;b=a+segments+1
            indices.extend([a,a+1,b,b,a+1,b+1])
    material = len(model['materials'])
    model['materials'].append({'name': name+'-finish','pbrMetallicRoughness':{'baseColorFactor':[*color,1], 'roughnessFactor':roughness,'metallicFactor':metalness},'doubleSided':True})
    primitive = {'attributes':{'POSITION':accessor(positions,'VEC3',3),'NORMAL':accessor(normals,'VEC3',3)},'indices':accessor(indices,'SCALAR',1,5123),'material':material}
    model['meshes'].append({'name':name,'primitives':[primitive]})
    model['scenes'][0]['nodes'].append(len(model['nodes']))
    model['nodes'].append({'name':name,'mesh':len(model['meshes'])-1,'translation':list(position)})

# Radial sections include rolled edges, a hollow shade and closed base/diffuser.
lathe('base',[(0,0),(.40,0),(.45,.015),(.47,.045),(.47,.075),(.45,.105),(.38,.12),(0,.12)],(.25,.29,.25),.42,.25)
lathe('stem',[(0,0),(.035,0),(.039,.015),(.039,1.22),(.032,1.24),(0,1.24)],(.44,.36,.23),.3,.65,(0,.12,0))
lathe('shade',[(.09,.40),(.11,.40),(.14,.37),(.49,.06),(.51,.02),(.51,0),(.49,-.015),(.465,-.015),(.46,.02),(.125,.345),(.09,.36)][::-1],(.57,.135,.078),.48,.12,(0,1.12,0))
lathe('diffuser',[(0,0),(.42,0),(.445,.012),(.445,.035),(.425,.05),(0,.05)],(.84,.79,.64),.7,0,(0,1.09,0))
lathe('cap',[(0,0),(.065,0),(.065,.035),(.045,.05),(0,.05)],(.25,.29,.25),.38,.25,(0,1.52,0))
model['buffers']=[{'byteLength':len(buffer),'uri':'data:application/octet-stream;base64,'+base64.b64encode(buffer).decode()}]
Path(__file__).with_name('assets').joinpath('lumen.gltf').write_text(json.dumps(model,separators=(',',':'))+'\n')
print(f'Wrote original Lumen: {len(model["meshes"])} meshes, {len(buffer)} buffer bytes')
