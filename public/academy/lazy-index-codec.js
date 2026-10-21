/* V15 wire format. The expanded in-memory index remains backward-compatible. */
export function expandLazyIndex(value) {
  if (value?.compactVersion !== 1) return value;
  const invalid = () => { throw Error('Invalid compact curriculum index.'); };
  if (value.lazyVersion !== 1 || !Array.isArray(value.catalog) || value.catalog.length > 20000) invalid();
  const descriptors = (entries, group) => {
    if (!entries || typeof entries !== 'object' || Array.isArray(entries)) invalid();
    return Object.fromEntries(Object.entries(entries).map(([id, tuple]) => {
      if (!/^[a-z0-9]+(?:[-_][a-z0-9]+)*$/.test(id) || ['constructor', 'prototype'].includes(id) || !Array.isArray(tuple) || tuple.length !== 2 || !/^[a-f0-9]{64}$/.test(tuple[0]) || !Number.isSafeInteger(tuple[1]) || tuple[1] < 2 || tuple[1] > 32 * 1024 * 1024) invalid();
      const [sha256, byteLength] = tuple, file = `data/lazy/${group}/${id}-${sha256.slice(0, 16)}.json`;
      return [id, {file, script: file.replace(/\.json$/, '.js'), sha256, byteLength}];
    }));
  };
  const catalog = value.catalog.map(course => {
    if (!course || typeof course !== 'object' || Array.isArray(course)) invalid();
    if (course.stages === undefined) return {...course};
    if (!Array.isArray(course.stages) || course.stages.length > 1000) invalid();
    return {...course, stages: course.stages.map(stage => {
      if (!stage || !Array.isArray(stage.steps) || stage.steps.length > 10000 || stage.steps.some(id => typeof id !== 'string')) invalid();
      return {...stage, steps: stage.steps.map(id => ({id}))};
    })};
  });
  return {lazyVersion: 1, guidedIds: value.guidedIds, catalog, photos: value.photos, release: value.release, courses: descriptors(value.courses, 'courses'), resources: descriptors(value.resources, 'resources'), auxiliary: descriptors(value.auxiliary, 'data')};
}
