/* V29 translation pack controls, layered over the complete V28 locale runtime.
 * A pack contains only the translation cache; no notes, form values or keys.
 * This does not turn language targets into fully authored translations.
 */
(function(root){
  'use strict';
  const baseAPI = root.MG_CURRICULUM_LOCALE_V28;
  const MAX_FILE_BYTES = 4 * 1024 * 1024;
  const MAX_ENTRIES = 3000;
  const MAX_CHARACTERS = 1000000;
  function validatePack(pack, supported=baseAPI?.supported || []) {
    if (!pack || pack.format !== 'macgyver-translation-cache' || pack.version !== 1 ||
        !Array.isArray(pack.entries) || pack.entries.length > MAX_ENTRIES) throw Error('Invalid translation pack.');
    const seen = new Set(); let characters = 0;
    for (const entry of pack.entries) {
      if (!Array.isArray(entry) || entry.length !== 2 || entry.some(value => typeof value !== 'string')) throw Error('Invalid translation entry.');
      const [key,value] = entry, split = key.indexOf('\u0000');
      if (split < 1 || !supported.includes(key.slice(0,split)) || key.indexOf('\u0000',split+1) !== -1 ||
          !key.slice(split+1).trim() || key.length > 2960 || !value.trim() || value.length > 12000 || seen.has(key)) throw Error('Invalid translation entry.');
      seen.add(key); characters += key.length + value.length;
    }
    if (characters > MAX_CHARACTERS) throw Error('Translation pack exceeds the device cache limit.');
    return {entries:pack.entries.length,characters,languages:[...new Set(pack.entries.map(entry=>entry[0].split('\u0000',1)[0]))]};
  }
  function create(options={}) {
    if (!baseAPI?.create) throw Error('Load curriculum-locale-v28.js before locale-v29.js.');
    const doc=root.document, host=options.packHost || options.status?.parentNode;
    let api, disposed=false, busy=false, pendingFile=0;
    const handlers=[], controls=doc.createElement('div');
    controls.className='locale-pack-v29'; controls.setAttribute('data-no-translate','');
    const download=doc.createElement('button'),upload=doc.createElement('button'),input=doc.createElement('input'),message=doc.createElement('p');
    download.type=upload.type='button'; input.type='file'; input.accept='.json,application/json'; input.hidden=true;
    download.dataset.localePack='export'; upload.dataset.localePack='import';
    message.setAttribute('role','status'); message.setAttribute('aria-live','polite');
    input.setAttribute('aria-label','Import translation JSON');
    controls.append(download,upload,input,message); host?.append?.(controls);
    const text=(zh,en)=>api?.language==='zh-TW'?zh:en;
    function refresh() {
      if(disposed)return;
      download.textContent=text('匯出此語系翻譯包','Export language pack');
      upload.textContent=text('匯入翻譯包','Import language pack');
      download.disabled=busy; upload.disabled=busy;
      if(!busy)message.textContent=text(
        '翻譯包可保存／移轉目前快取的段落（最多 3,000 段），不是整站完整翻譯；匯入後仍依畫面涵蓋率顯示。',
        'Packs save or transfer cached fragments (up to 3,000), not the entire site. Visible-section coverage remains the measure of completion.');
    }
    api=baseAPI.create({...options,onChange:state=>{pendingFile++; options.onChange?.(state);refresh();}});
    const listen=(node,event,fn)=>{node.addEventListener(event,fn);handlers.push(()=>node.removeEventListener(event,fn));};
    async function importPack(pack) {
      validatePack(pack,baseAPI.supported);
      const result=api.importCache(pack);
      if(!result)throw Error('Translation cache is unavailable.');
      await api.apply();
      return result;
    }
    function exportPack() {
      const pack=api.exportCache();
      if(!pack)throw Error('Translation cache is unavailable.');
      validatePack(pack,baseAPI.supported);
      return pack;
    }
    listen(download,'click',()=>{
      try{
        const pack=exportPack();
        if(!pack.entries.length){message.textContent=text('此語系尚無翻譯快取。先翻譯目前正文，再匯出。','No cached translations for this language. Translate a lesson first.');return;}
        const link=doc.createElement('a');
        const url=root.URL.createObjectURL(new root.Blob([JSON.stringify(pack,null,2)+'\n'],{type:'application/json'}));
        link.href=url;link.download='MacGyver_Translation_'+api.language+'.json';link.hidden=true;controls.append(link);link.click();link.remove();
        root.setTimeout(()=>root.URL.revokeObjectURL(url),1000);
        message.textContent=text(`已匯出 ${pack.entries.length} 段。只包含此語系已快取的正文；未包含整站所有課程。`,
          `Exported ${pack.entries.length} cached fragments for this language; this is not every course.`);
      }catch(error){message.textContent=text('無法匯出翻譯包：','Unable to export: ')+error.message;}
    });
    listen(upload,'click',()=>{input.value='';input.click();});
    listen(input,'change',async()=>{
      const file=input.files?.[0];if(!file)return;
      const epoch=++pendingFile;busy=true;refresh();
      try{
        if(file.size>MAX_FILE_BYTES)throw Error('Translation JSON exceeds 4 MiB.');
        const source=await file.text();
        if(disposed||epoch!==pendingFile)return;
        const pack=JSON.parse(source);
        const result=await importPack(pack);
        if(disposed||epoch!==pendingFile)return;
        message.textContent=text(`已匯入 ${result.imported} 段；${result.storageAvailable?'已保存在此裝置。':'目前僅保留於此分頁，裝置儲存不可用。'}`,
          `Imported ${result.imported} fragments. ${result.storageAvailable?'Saved on this device.':'Device storage is unavailable; available in this tab only.'}`);
      }catch(error){if(!disposed&&epoch===pendingFile)message.textContent=text('翻譯包未匯入：','Pack not imported: ')+error.message;}
      finally{if(!disposed){busy=false;download.disabled=false;upload.disabled=false;}input.value='';}
    });
    refresh();
    return Object.freeze({get language(){return api.language;},get preference(){return api.preference;},get status(){return api.status;},
      apply:node=>api.apply(node),invalidate:()=>api.invalidate(),readUrl:value=>{api.readUrl(value);refresh();},
      narrate:node=>api.narrate(node),stop:()=>api.stop(),exportCache:()=>api.exportCache(),importCache:importPack,
      exportPack,importPack,dispose:()=>{disposed=true;pendingFile++;api.dispose();handlers.forEach(remove=>remove());controls.remove();}});
  }
  root.MG_CURRICULUM_LOCALE_V29=Object.freeze({supported:baseAPI?.supported||[],create,validatePack,maxFileBytes:MAX_FILE_BYTES});
})(window);
