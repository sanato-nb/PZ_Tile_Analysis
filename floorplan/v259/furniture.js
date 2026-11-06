// v259 uses candidate IDs for selection and exact sprite keys for placement.
let furnitureData;
let selectedCandidate = '';
let furnitureLocations = new Map();
let currentHit = -1;
let indexedModel = null;
let resultLimit = 30;

async function loadFurniture() {
  const raw = await decompress(bytesFromBase64(FURNITURE_B64), 'gzip');
  furnitureData = JSON.parse(new TextDecoder().decode(raw));
  const categories = [...new Set(Object.values(furnitureData.candidates).map(c => c.category))].sort();
  for (const category of categories) $('fCategory').add(new Option(category, category));
  $('files').disabled = false;
  $('sampleMap').disabled = false;
  refreshFurniture();
}

function candidateIds(key) {
  return furnitureData?.tiles[key] || [];
}

function indexFurniture() {
  furnitureLocations = new Map();
  for (const [level, floor] of model.floors) {
    for (const cell of floor.draw) {
      for (const item of cell.items) {
        const key = v256ItemKey(item);
        for (const id of candidateIds(key)) {
          if (!furnitureLocations.has(id)) furnitureLocations.set(id, []);
          furnitureLocations.get(id).push({level, x:cell.x, y:cell.y, key, layer:item.layer.name});
        }
      }
    }
  }
  indexedModel = model;
  currentHit = -1;
  refreshFurniture();
}

function refreshFurniture() {
  if (!furnitureData) return;
  const query = $('fQuery').value.trim().toLowerCase();
  const category = $('fCategory').value;
  const status = $('fStorage').value;
  const onlyMap = $('fMapOnly').checked;
  const matches = Object.entries(furnitureData.candidates).filter(([id, c]) =>
    (!category || c.category === category) && (!status || c.storage_status === status) &&
    (!onlyMap || furnitureLocations.has(id)) &&
    (!query || [id,c.display_name,c.registered_name,c.category,...c.keys].join(' ').toLowerCase().includes(query)));
  const results = $('fResults');
  results.replaceChildren();
  for (const [id,c] of matches.slice(0,resultLimit)) {
    const button = document.createElement('button');
    button.type = 'button';
    button.className = 'v256hit';
    button.setAttribute('aria-pressed', String(id === selectedCandidate));
    button.textContent = c.display_name + ' · ' + c.category + (model ? ' · 배치 ' + (furnitureLocations.get(id)?.length || 0) : '');
    button.onclick = () => { selectedCandidate = id; currentHit = -1; refreshFurniture(); moveFurniture(1); };
    results.append(button);
  }
  $('fCount').textContent = matches.length.toLocaleString() + '개 후보';
  $('fMore').hidden = matches.length <= resultLimit;
  const selected = furnitureData.candidates[selectedCandidate];
  const locations = furnitureLocations.get(selectedCandidate) || [];
  $('fSelection').textContent = selected ? [selected.display_name,selectedCandidate,selected.evidence,selected.name_status,
    '후보 저장소 판정 · ' + selected.storage_status,model ? '현재 맵 부품 배치 ' + locations.length + '건' : '위치 확인은 TMX를 연 뒤 가능합니다.'].join('\n') : '';
  $('fPosition').textContent = currentHit >= 0 && locations[currentHit] ?
    (currentHit+1)+' / '+locations.length+' · Level '+locations[currentHit].level+' · ('+locations[currentHit].x+', '+locations[currentHit].y+') · '+locations[currentHit].layer : '';
  for (const name of ['fNext','fPrev']) $(name).disabled = !locations.length;
  $('fClear').disabled = !selected;
  schedule();
}

function moveFurniture(step) {
  const hits = furnitureLocations.get(selectedCandidate) || [];
  if (!hits.length) return;
  currentHit = currentHit < 0 ? (step > 0 ? 0 : hits.length-1) : (currentHit+step+hits.length)%hits.length;
  const hit = hits[currentHit];
  if (currentFloor !== hit.level) selectFloor(hit.level);
  zoom = Math.max(zoom, 20/unit);
  const p = screen(hit.x+.5,hit.y+.5);
  panX += dims.w/2-p.x;
  panY += dims.h/2-p.y;
  inspect(hit.x,hit.y);
  refreshFurniture();
}

function markFurniture(cells,show,v) {
  if (!selectedCandidate) return;
  ctx.save();
  ctx.fillStyle = '#faad2a88';
  ctx.strokeStyle = '#8d4300';
  ctx.lineWidth = Math.max(1, Math.min(3,v*.1));
  for (const cell of cells) {
    if (!cell.items.some(item => show(item) && candidateIds(v256ItemKey(item)).includes(selectedCandidate))) continue;
    const p = screen(cell.x,cell.y);
    ctx.fillRect(p.x,p.y,v,v);
    ctx.strokeRect(p.x,p.y,v,v);
  }
  ctx.restore();
}

function partEvidence(key,id) {
  return furnitureData.storage[key]?.[id];
}

function inspectFurniture(items) {
  const blocks = $('details').querySelectorAll('.tile');
  items.forEach((item,i) => {
    const key = v256ItemKey(item);
    const def = furnitureData.defs[key];
    const ids = candidateIds(key);
    if (!def && !ids.length) return;
    const box = document.createElement('div');
    box.className = 'v256audit';
    const lines = [key + (def ? ' · v258 통합 타일' : ' · 가구 원장 타일 ID')];
    if (def) {
      for (const [field,label] of Object.entries(furnitureData.labels)) {
        if (def[field] != null && def[field] !== '') lines.push(label+' · '+def[field]);
      }
    }
    for (const id of ids) {
      const c = furnitureData.candidates[id], s = partEvidence(key,id);
      lines.push(c.display_name+' · '+c.category+' · '+id, '후보 저장소 판정 · '+c.storage_status);
      if (s) lines.push('이 부품의 저장소 · '+(s[1] || '유형 미기재')+' / 용량 '+(s[2] || '미기재')+' · '+s[0]);
    }
    box.textContent = lines.join('\n');
    blocks[i].prepend(box);
  });
}

function furnitureCsv(key) {
  const ids = candidateIds(key);
  return [JSON.stringify(furnitureData.defs[key] || null), JSON.stringify(ids.map(id => {
    const c = furnitureData.candidates[id];
    return {id,name:c.display_name,category:c.category,status:c.storage_status,part_storage:partEvidence(key,id)||null};
  }))];
}

for (const id of ['fQuery','fCategory','fStorage','fMapOnly']) $(id).addEventListener('input', () => {
  resultLimit = 30;
  refreshFurniture();
});
$('fMore').onclick = () => { resultLimit += 30; refreshFurniture(); };
$('fPrev').onclick = () => moveFurniture(-1);
$('fNext').onclick = () => moveFurniture(1);
$('fClear').onclick = () => { selectedCandidate=''; currentHit=-1; refreshFurniture(); };
$('sampleMap').onclick = async () => {
  const data = await decompress(bytesFromBase64(SAMPLE_B64),'gzip');
  const transfer = new DataTransfer();
  transfer.items.add(new File([data],'31_46.tmx'));
  $('files').files = transfer.files;
  $('files').dispatchEvent(new Event('change'));
};

const furnitureSymbols = {
  '테이블':'탁','좌석':'의','안락가구':'소','침구':'침','수납가구':'장',
  '가전':'전','급배수설비':'수','조명':'등','카운터':'대','쓰레기통':'통','작업대':'작'
};
function drawFurnitureSymbol(cell, show, v) {
  for (let i=cell.items.length-1; i>=0; i--) {
    const item = cell.items[i];
    if (!show(item) || item.mapping.tile?._v256?.active_flag === '0') continue;
    const ids = candidateIds(v256ItemKey(item));
    if (!ids.length) continue;
    const category = furnitureData.candidates[ids[0]].category;
    const symbol = furnitureSymbols[category];
    if (!symbol || !ids.every(id => furnitureData.candidates[id].category === category)) continue;
    const p = screen(cell.x,cell.y);
    ctx.fillStyle = '#397879';
    ctx.fillRect(p.x+v*.18,p.y+v*.18,v*.64,v*.64);
    if (options.labels && v>=17) {
      ctx.fillStyle='#fff'; ctx.font='bold '+Math.floor(v*.42)+'px sans-serif';
      ctx.textAlign='center';ctx.fillText(symbol,p.x+v*.5,p.y+v*.65);
    }
    return;
  }
}
