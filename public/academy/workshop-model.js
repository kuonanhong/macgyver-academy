import { resolveExercise, renderExerciseSvg } from './process-exercises.js';
export { renderExerciseSvg };
/** Original dimensionless assembly exercise; no physical CAD or process tolerances. */
export const DEFAULT_TOLERANCE = Object.freeze({ distance: 6, angle: 8 });
const finite = (n, d = 0) => Number.isFinite(Number(n)) ? Number(n) : d;
const clamp = (n, low, high) => Math.max(low, Math.min(high, n));
export const wrapAngle = n => ((finite(n) + 180) % 360 + 360) % 360 - 180;
export function normalizePose(p = {}) {
  return { x: clamp(finite(p.x, -86), -130, 130), y: clamp(finite(p.y, 50), -80, 80), z: clamp(finite(p.z, 30), 0, 65), rotation: wrapAngle(p.rotation ?? -24), grabbed: !!p.grabbed, precision: !!p.precision };
}
export function initialPose() { return normalizePose(); }
export function targetFor(step = {}, course = {}) {
  const a = step.assemblySpec || resolveExercise(course, step).target;
  return { x: clamp(finite(a.x, 0), -40, 40), y: clamp(finite(a.y, 0), -20, 20), z: clamp(finite(a.z, 8), 0, 40), rotation: wrapAngle(a.rotation ?? 0) };
}
export function alignment(pose, target, tolerance = DEFAULT_TOLERANCE) {
  const distance = Math.hypot(pose.x - target.x, pose.y - target.y, pose.z - target.z);
  const angle = Math.abs(wrapAngle(pose.rotation - target.rotation));
  return { distance, angle, aligned: distance <= tolerance.distance && angle <= tolerance.angle };
}
export function collides(pose) {
  // A clearly visible raised fixture. Lift or move around it; coordinates are schematic.
  return pose.x > -69 && pose.x < -37 && pose.y > -39 && pose.y < 20 && pose.z < 23;
}
export function advancePose(pose, axes, precision = false, environment = {}) {
  const p = normalizePose(pose);
  if (!p.grabbed) return { pose: p, blocked: false, needsGrab: true };
  const amount = precision || p.precision ? 1 : 4;
  const next = normalizePose({ ...p, x: p.x + finite(axes.x) * amount, y: p.y + finite(axes.y) * amount, z: p.z + finite(axes.z) * amount, rotation: p.rotation + finite(axes.rotation) * (precision || p.precision ? 1 : 4) });
  const samples = Math.max(1, Math.ceil(Math.hypot(next.x-p.x,next.y-p.y,next.z-p.z)/3));
  // Semantic scenes do not share an invisible generic fixture. Only a caller
  // that visibly renders the legacy fixture may explicitly enable that model.
  for(let i=1;environment.fixture===true&&i<=samples;i++){const f=i/samples;if(collides({x:p.x+(next.x-p.x)*f,y:p.y+(next.y-p.y)*f,z:p.z+(next.z-p.z)*f}))return {pose:p,blocked:true,needsGrab:false};}
  return { pose: next, blocked: false, needsGrab: false };
}
export function processKind(course = {}, step = {}) {
  return resolveExercise(course, step).scene;
}
/** Compatibility bridge for previously exported model renderers. */
export function assemblySvg({ course, step, pose, exercise, mentor = false, assembled = false, labels = {} }) {
  return renderExerciseSvg({ course, step, state: { pose, exercise }, mentor, assembled, labels });
}
