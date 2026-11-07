/* Original V22 walkable-world collision and navigation; coordinates are metres. */
export const clamp = (n, a, b) => Math.max(a, Math.min(b, n));
export function normalizeInput(x, z) {
  const length = Math.hypot(x, z);
  return length > 1 ? {x: x / length, z: z / length} : {x, z};
}
export function isWalkable(x, z, bounds, obstacles = [], radius = .38) {
  if (!Number.isFinite(x) || !Number.isFinite(z)) return false;
  if (Math.abs(x) > bounds.width / 2 - radius || Math.abs(z) > bounds.depth / 2 - radius) return false;
  return !obstacles.some(o => {
    const nx = clamp(x, o.minX, o.maxX), nz = clamp(z, o.minZ, o.maxZ);
    return (x - nx) ** 2 + (z - nz) ** 2 < radius ** 2;
  });
}
export function moveWithCollisions(position, delta, bounds, obstacles = [], radius = .38) {
  let {x, z} = position;
  const pieces = Math.max(1, Math.ceil(Math.hypot(delta.x, delta.z) / Math.max(.05, radius * .45)));
  const dx = delta.x / pieces, dz = delta.z / pieces;
  for (let i = 0; i < pieces; i++) {
    if (isWalkable(x + dx, z + dz, bounds, obstacles, radius)) { x += dx; z += dz; }
    else {
      if (isWalkable(x + dx, z, bounds, obstacles, radius)) x += dx;
      if (isWalkable(x, z + dz, bounds, obstacles, radius)) z += dz;
    }
  }
  return {x, z};
}
export function cameraRelativeMove(input, yaw) {
  const n = normalizeInput(input.x, input.z), s = Math.sin(yaw), c = Math.cos(yaw);
  return {x:n.x * c + n.z * s, z:-n.x * s + n.z * c};
}
export function angleDelta(from, to) {
  const turn = Math.PI * 2;
  return ((to - from + Math.PI) % turn + turn) % turn - Math.PI;
}
export function approachVelocity(velocity, target, dt) {
  const gain = 1 - Math.exp(-dt * (target.x || target.z ? 14 : 22));
  const x = velocity.x + (target.x - velocity.x) * gain;
  const z = velocity.z + (target.z - velocity.z) * gain;
  return Math.hypot(x, z) < .015 ? {x: 0, z: 0} : {x, z};
}
export function stationBearing(position, approach, yaw) {
  return angleDelta(yaw, Math.atan2(position.x - approach.x, position.z - approach.z));
}
export function stationObstacles(stations) {
  return stations.map(station => ({
    minX: station.x - 1.7,
    maxX: station.x + 1.7,
    minZ: station.z - 1.8,
    maxZ: station.z + 1.8,
    minY: 0,
    maxY: station.photoSrc ? 5 : 3.15,
  }));
}
/** Fraction of the segment available for a following camera, with near-plane clearance. */
export function cameraClearFraction(origin, target, obstacles, clearance = .28) {
  const distance = Math.hypot(target.x - origin.x, target.y - origin.y, target.z - origin.z);
  if (distance < .01) return 1;
  let closest = 1;
  for (const box of obstacles) {
    let enter = 0, exit = 1;
    for (const [axis, min, max] of [['x', box.minX, box.maxX], ['y', box.minY, box.maxY], ['z', box.minZ, box.maxZ]]) {
      const delta = target[axis] - origin[axis];
      if (Math.abs(delta) < 1e-7) {
        if (origin[axis] < min || origin[axis] > max) { enter = 1; exit = 0; break; }
        continue;
      }
      const a = (min - origin[axis]) / delta, b = (max - origin[axis]) / delta;
      enter = Math.max(enter, Math.min(a, b));
      exit = Math.min(exit, Math.max(a, b));
      if (enter > exit) break;
    }
    if (enter <= exit && enter > 0) closest = Math.min(closest, Math.max(.06, enter - clearance / distance));
  }
  return closest;
}
export function findPath(start, target, bounds, obstacles = [], radius = .38, step = .55) {
  // An eight-neighbour A* grid, with corner-cutting prohibited for clearances.
  if (!isWalkable(start.x, start.z, bounds, obstacles, radius)) return [];
  const minX = -bounds.width / 2 + radius, minZ = -bounds.depth / 2 + radius;
  const columns = Math.floor((bounds.width - 2 * radius) / step) + 1;
  const rows = Math.floor((bounds.depth - 2 * radius) / step) + 1;
  const cell = p => ({x:clamp(Math.round((p.x - minX) / step),0,columns-1),z:clamp(Math.round((p.z-minZ)/step),0,rows-1)});
  const point = p => ({x:minX+p.x*step,z:minZ+p.z*step});
  const valid = p => p.x>=0&&p.z>=0&&p.x<columns&&p.z<rows&&isWalkable(point(p).x,point(p).z,bounds,obstacles,radius);
  const nearest = p => {
    if(valid(p))return p;
    for(let r=1;r<12;r++) {
      const candidates=[];
      for(let x=-r;x<=r;x++)for(let z=-r;z<=r;z++)if(Math.max(Math.abs(x),Math.abs(z))===r) {
        const q={x:p.x+x,z:p.z+z};if(valid(q))candidates.push(q);
      }
      if(candidates.length)return candidates.sort((a,b)=>Math.hypot(a.x-p.x,a.z-p.z)-Math.hypot(b.x-p.x,b.z-p.z))[0];
    }
    return null;
  };
  const first=nearest(cell(start)),last=nearest(cell(target));
  if(!first||!last)return [];
  const key=p=>p.z*columns+p.x, goal=key(last), firstKey=key(first);
  const heuristic=p=>Math.hypot(p.x-last.x,p.z-last.z);
  const open=[{...first,g:0,f:heuristic(first)}], costs=new Map([[firstKey,0]]), parents=new Map(), closed=new Set();
  let found=false;
  while(open.length) {
    let best=0;for(let i=1;i<open.length;i++)if(open[i].f<open[best].f)best=i;
    const current=open.splice(best,1)[0], ck=key(current);
    if(closed.has(ck))continue;
    if(ck===goal){found=true;break;}
    closed.add(ck);
    for(const [dx,dz] of [[1,0],[-1,0],[0,1],[0,-1],[1,1],[-1,1],[1,-1],[-1,-1]]) {
      const next={x:current.x+dx,z:current.z+dz},nk=key(next);
      if(!valid(next)||closed.has(nk))continue;
      if(dx&&dz&&(!valid({x:current.x+dx,z:current.z})||!valid({x:current.x,z:current.z+dz})))continue;
      const g=current.g+Math.hypot(dx,dz);
      if(g>=(costs.get(nk)??Infinity))continue;
      costs.set(nk,g);parents.set(nk,ck);open.push({...next,g,f:g+heuristic(next)});
    }
  }
  if(!found)return [];
  const route=[];let cursor=goal;
  while(cursor!==firstKey){route.push(point({x:cursor%columns,z:Math.floor(cursor/columns)}));cursor=parents.get(cursor);if(cursor===undefined)return [];}
  route.reverse();
  // Keep the exact requested target when it is clear; never teleport through a collider.
  if(isWalkable(target.x,target.z,bounds,obstacles,radius))route.push({x:target.x,z:target.z});
  return route;
}
export function nearestStation(position, stations, range=3.25) {
  let nearest=null,best=range;
  for(const station of stations) {
    const p=station.approach||station, distance=Math.hypot(position.x-p.x,position.z-p.z);
    if(distance<best){best=distance;nearest=station;}
  }
  return nearest;
}
