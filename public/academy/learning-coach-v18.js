/* Small pure helpers for bounded, resumable teaching sessions. */
export function stageGuidancePlan(course,stepId,completed=[]){
 const stage=(course?.stages||[]).find(s=>(s.steps||[]).some(x=>x.id===stepId));
 if(!stage)return {stageId:null,total:0,pending:[],done:0};
 const done=new Set(completed),steps=stage.steps||[];
 return {stageId:stage.id,total:steps.length,pending:steps.filter(s=>!done.has(s.id)).map(s=>s.id),done:steps.filter(s=>done.has(s.id)).length};
}
export function guidanceContextMatches(session,{owner,courseId,stageId,page}){
 return !!session&&session.owner===owner&&session.courseId===courseId&&session.stageId===stageId&&page==='workshop';
}
export function learningBadges(course,progress={}){
 const ids=new Set((course?.stages||[]).flatMap(s=>s.steps||[]).map(s=>s.id)),completed=new Set((progress.completed||[]).filter(id=>ids.has(id))),assisted=new Set((progress.assisted||[]).filter(id=>completed.has(id)));
 return {completed:completed.size,assisted:assisted.size,independent:completed.size-assisted.size,total:ids.size};
}
