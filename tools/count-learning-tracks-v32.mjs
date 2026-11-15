import fs from 'node:fs';
import {classifyLearningCourse} from '../public/academy/learning-map.js';
const index=JSON.parse(fs.readFileSync(process.argv[2],'utf8'));
const guided=new Set(index.guidedIds),counts={};
for(const course of index.catalog){
  if(!guided.has(course.id))continue;
  const track=classifyLearningCourse(course).track;
  counts[track]=(counts[track]||0)+1;
}
process.stdout.write(JSON.stringify(counts));
