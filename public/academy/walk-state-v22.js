/* Separate walking-game progress; original course/V21 completion is untouched. */
export function newWalkRecord(scene,roleId=scene.roles?.[0]?.id||'learner') {
  return {version:22,sceneId:scene.id,roleId,chapterId:scene.chapters[0].id,seen:{},decisions:{},completed:[],notes:{},actions:[],position:null,roleRuns:{},updatedAt:null};
}
export function restoreWalkRecord(scene,raw) {
  const out=newWalkRecord(scene);
  if(!raw||raw.version!==22||raw.sceneId!==scene.id)return out;
  const chapters=new Map(scene.chapters.map(c=>[c.id,c])),roles=new Set((scene.roles||[]).map(r=>r.id));
  if(roles.has(raw.roleId))out.roleId=raw.roleId;
  if(chapters.has(raw.chapterId))out.chapterId=raw.chapterId;
  out.completed=[...new Set(Array.isArray(raw.completed)?raw.completed:[])].filter(id=>chapters.has(id));
  for(const [id,c] of chapters){
    const ids=new Set((c.observations||[]).map(o=>o.id));
    out.seen[id]=[...new Set(Array.isArray(raw.seen?.[id])?raw.seen[id]:[])].filter(v=>ids.has(v));
    const d=raw.decisions?.[id];
    if(d&&c.choices?.some(x=>x.id===d.choiceId))out.decisions[id]={choiceId:d.choiceId,assisted:d.assisted===true};
    if(typeof raw.notes?.[id]==='string')out.notes[id]=raw.notes[id].slice(0,4000);
    // A forged completion without the corresponding evidence/decision is rejected.
    if(out.completed.includes(id)&&(out.seen[id].length!==ids.size||(c.choices?.length&&!out.decisions[id])))out.completed=out.completed.filter(v=>v!==id);
  }
  if(raw.position&&['x','z','yaw'].every(k=>Number.isFinite(raw.position[k])&&Math.abs(raw.position[k])<10000))out.position={x:raw.position.x,z:raw.position.z,yaw:raw.position.yaw};
  out.actions=(Array.isArray(raw.actions)?raw.actions:[]).filter(a=>a&&typeof a.type==='string'&&a.type.length<80&&chapters.has(a.chapterId)&&typeof a.at==='string').slice(-600).map(a=>({type:a.type,chapterId:a.chapterId,assisted:a.assisted===true,at:a.at.slice(0,40)}));
  out.updatedAt=typeof raw.updatedAt==='string'?raw.updatedAt.slice(0,40):null;
  for(const role of roles){const run=raw.roleRuns?.[role];if(run&&typeof run==='object')out.roleRuns[role]=restoreWalkRecord(scene,{...run,version:22,sceneId:scene.id,roleId:role,roleRuns:{}});}
  return out;
}
