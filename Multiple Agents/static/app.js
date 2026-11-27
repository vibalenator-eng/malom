const $ = (id) => document.getElementById(id);
const SUIT_LABEL = { piros: "Piros", tok: "Tök", zold: "Zöld", makk: "Makk" };
const LABEL = { piros: "Piros", tok: "Tök", zold: "Zöld", makk: "Makk" };
const RANK = { A: "Á", "10": "X", K: "K", F: "F", Alo: "A" };
const RANK_LABEL = { A: "Ász", "10": "Tízes", K: "Király", F: "Felső", Alo: "Alsó" };
const CARD_COL = { A: 0, K: 1, F: 2, Alo: 3, "10": 4 };
const SUIT_ROW = { piros: 0, tok: 1, zold: 2, makk: 3 };
const NAME = { ai: "GÉP ELLEN", online: "ONLINE SZOBA", hotseat: "KÉT JÁTÉKOS" };
let session = null, gameState = null, pollTimer = null, toastTimer = null, pending = false;

function setSession(value) { session = value; localStorage.setItem("snapszer-session", JSON.stringify(value)); }
function showError(message) { $("lobbyError").textContent = message || ""; }
function toast(message, end=false) { const t=$("toast");t.textContent=message;t.className=`toast show${end?" end":""}`;clearTimeout(toastTimer);toastTimer=setTimeout(()=>t.className="toast",2600); }
async function request(url, options={}) { const res=await fetch(url,{headers:{"Content-Type":"application/json"},...options});const data=await res.json();if(!res.ok)throw new Error(data.error||"Sikertelen kérés.");return data; }
function startView() { $("lobby").classList.add("hidden");$("game").classList.remove("hidden");$("newGameTop").classList.remove("hidden");clearInterval(pollTimer);refresh();pollTimer=setInterval(refresh,900); }
async function create(mode) { showError("");try { const result=await request("/api/rooms",{method:"POST",body:JSON.stringify({mode,name:$(("playerName")).value.trim(),difficulty:Number($("aiDifficulty").value)})});setSession({...result,mode});startView(); } catch(e){showError(e.message);} }
async function join() { showError("");const code=$("roomCode").value.trim().toUpperCase();if(!code){showError("Írd be a szobakódot.");return;}try{const result=await request(`/api/rooms/${encodeURIComponent(code)}/join`,{method:"POST",body:JSON.stringify({name:$(("playerName")).value.trim()})});setSession({...result,mode:"online"});startView();}catch(e){showError(e.message);} }
function returnFromExpiredRoom(error) {
  if(!/Nem található ilyen szoba/i.test(error.message||""))return false;
  clearInterval(pollTimer);
  pollTimer=null;
  session=null;
  gameState=null;
  pending=false;
  localStorage.removeItem("snapszer-session");
  $("game").classList.add("hidden");
  $("lobby").classList.remove("hidden");
  $("newGameTop").classList.add("hidden");
  showError("A korábbi parti már nem él. Indíts új játékot.");
  return true;
}async function refresh() { if(!session||pending)return;try {const s=await request(`/api/rooms/${encodeURIComponent(session.code)}?token=${encodeURIComponent(session.token)}`);render(s);}catch(e){if(returnFromExpiredRoom(e))return;if(!gameState)toast(e.message);}}
async function act(action,extra={}) { if(pending)return;const before=gameState;pending=true;try{const s=await request(`/api/rooms/${encodeURIComponent(session.code)}/act`,{method:"POST",body:JSON.stringify({token:session.token,action,...extra})});const recent=s.recent_opponent_trick||(session.mode==="ai"&&s.finished&&s.winner===1&&s.last_trick?.length===2?s.last_trick:(session.mode==="ai"&&before?.lead_card&&s.message.includes("Kék vitte")?[before.lead_card,before.hand.find(c=>c.id===extra.card_id)].filter(Boolean):null));if(recent){render({...s,turn:1,lead_card:null,last_trick:recent,showing_recent_trick:true});await new Promise(resolve=>setTimeout(resolve,5000));}render(s);}catch(e){if(!returnFromExpiredRoom(e))toast(e.message);}finally{pending=false;} }
function suitMark(suit) {const paths={piros:'<path d="M12 21s-9-5.5-9-12a5 5 0 0 1 9-3 5 5 0 0 1 9 3c0 6.5-9 12-9 12Z"/>',tok:'<path d="M4 8h16l-1.4 10a2 2 0 0 1-2 1.7H7.4a2 2 0 0 1-2-1.7L4 8Z"/><path d="M3 8h18M7 5h10M9 3h6"/>',zold:'<path d="M20 4C9 4 4 9 4 17c0 2 1.5 3 3.4 2.3C15 16.4 17.5 10 20 4Z"/><path d="M5 19c4-5 8-8 13-12"/>',makk:'<path d="M12 3c-1.5 3-6 5-6 10a6 6 0 0 0 12 0c0-5-4.5-7-6-10Z"/><path d="M12 3v-2M9 6c-2-2-4-2-5-1 1 2 2 3 5 3m3-2c2-2 4-2 5-1-1 2-2 3-5 3"/>'};return `<svg class="suit-mark suit-${suit}" viewBox="0 0 24 24" aria-label="${SUIT_LABEL[suit]}">${paths[suit]}</svg>`;}
function cardFace(c,large=false,disabled=false) {const x=CARD_COL[c.rank]*100/7,y=SUIT_ROW[c.suit]*100/3;return `<div class="card ${large?"large":""} ${disabled?"disabled":""}" data-card="${c.id}" style="--cx:${x}%;--cy:${y}%" aria-label="${SUIT_LABEL[c.suit]} ${RANK_LABEL[c.rank]}"><span class="card-corner top-corner">${RANK[c.rank]}${suitMark(c.suit)}</span><span class="card-corner bottom-corner">${RANK[c.rank]}${suitMark(c.suit)}</span></div>`;}
function availableMarriages(s) {
  if(s.marriages?.length)return s.marriages;
  if(s.finished||s.turn!==s.player||s.lead_card)return [];
  const pairs=[];
  for(const suit of Object.keys(LABEL)){
    const pair=(s.hand||[]).filter(c=>c.suit===suit&&(c.rank==="K"||c.rank==="F"));
    if(pair.length===2)pairs.push({suit,points:suit===s.trump?40:20,cards:pair.map(c=>({id:c.id,rank:c.rank}))});
  }
  return pairs;
}
function fallbackCloseReason(s) {
  if(s.close_reason)return s.close_reason;
  if(s.finished)return "A leosztás már véget ért.";
  if(s.turn!==s.player)return "Csak a te körödben takarhatsz.";
  if(s.lead_card)return "Csak híváskor, lap kijátszása előtt takarhatsz.";
  if(s.closed_by!==null)return "A talon már be van takarva.";
  if(!(s.tricks||[]).some(n=>n>0))return "Legalább egy ütést le kell játszani előbb.";
  if(s.stock_count<2)return "Legalább két lefordított lap maradjon a felfordított adu fölött.";
  return "Most nem lehet betakarni.";
}
function fallbackExchangeReason(s) {
  if(s.exchange_reason)return s.exchange_reason;
  if(s.finished)return "A leosztás már véget ért.";
  if(s.turn!==s.player)return "Csak a te körödben cserélhetsz adut.";
  if(s.lead_card)return "Aducsere csak híváskor lehetséges.";
  if(s.closed_by!==null)return "A talon már be van takarva.";
  if(!s.trump_card)return "A felfordított adut már felhúzták.";
  if(!(s.hand||[]).some(c=>c.suit===s.trump&&c.rank==="Alo"))return "Nincs nálad adu Alsó.";
  return "Most nem lehet adut cserélni.";
}function render(s) {gameState=s;session.player=s.player;$("modeLabel").textContent=NAME[s.mode];$("turnLabel").textContent=s.finished?(s.winner===s.player?"Te nyertél!":`${s.names[s.winner]} nyert!`):s.turn===s.player?"Te következel":"Az ellenfél következik";$("tableMessage").textContent=s.message;$("trumpLabel").textContent=LABEL[s.trump];$("trumpIcon").innerHTML=suitMark(s.trump);$("stockLabel").textContent=s.talon_open?`${s.stock_count+(s.trump_card?1:0)} lap a talonban`:(s.closed_by!==null?"betakart talon":"nincs több húzás");
  $("scoreName0").textContent=s.names[0];$("scoreName1").textContent=s.names[1];$("score0").textContent=s.points[0];$("score1").textContent=s.points[1];$("opponentName").textContent=s.names[1-s.player];$("opponentAvatar").textContent=(s.names[1-s.player]||"K").slice(0,1).toUpperCase();$("opponentMeta").textContent=`${s.hand_counts[1-s.player]} lap · ${s.points[1-s.player]} pont`;$("playerNameLabel").textContent=s.names[s.player];$("playerMeta").textContent=`${s.hand_counts[s.player]} lap · ${s.points[s.player]} pont`;$("turnPill").textContent=s.finished?"VÉGE":s.turn===s.player?"TE JÖSSZ":"VÁRJ";
  $("opponentCards").innerHTML=Array.from({length:s.hand_counts[1-s.player]},()=>`<span class="back"></span>`).join("");$("hand").innerHTML=(s.hand||[]).map(c=>cardFace(c,false,!s.legal_ids.includes(c.id)||s.turn!==s.player||s.finished)).join("");
  const visibleTrick=s.lead_card?[s.lead_card]:(s.last_trick||[]);$("leadSlot").innerHTML=`<span class="slot-label">ELSŐ LAP</span>${visibleTrick[0]?cardFace(visibleTrick[0],true):'<span class="empty-card">·</span>'}`;$("replySlot").innerHTML=`<span class="slot-label">MÁSODIK LAP</span>${visibleTrick[1]?cardFace(visibleTrick[1],true):'<span class="empty-card">·</span>'}`;
  $("trumpCard").innerHTML=s.trump_card?cardFace(s.trump_card,true):'<span style="opacity:.6">—</span>';
  $("closeButton").disabled=!s.can_close;$("closeReason").textContent=s.can_close?"":fallbackCloseReason(s);$("closeReason").classList.toggle("hidden",s.can_close);
  $("exchangeButton").disabled=!s.can_exchange;$("exchangeReason").textContent=s.can_exchange?"":fallbackExchangeReason(s);$("exchangeReason").classList.toggle("hidden",s.can_exchange);
  const marriages=availableMarriages(s);const marriageList=$("marriages");marriageList.replaceChildren();marriages.forEach(m=>(m.cards||[]).forEach(c=>{const button=document.createElement("button");button.className="marriage-button";button.dataset.marriage=m.suit;button.dataset.card=c.id;button.textContent=m.points+" bemondása ("+LABEL[m.suit]+"): "+RANK_LABEL[c.rank]+" kijátszása";marriageList.appendChild(button);}));const heldPair=Object.keys(LABEL).some(suit=>{const ranks=(s.hand||[]).filter(c=>c.suit===suit).map(c=>c.rank);return ranks.includes("K")&&ranks.includes("F");});$("marriageHelp").textContent=marriages.length?"Válassz a két gomb közül: a kiválasztott Király vagy Felső kijátszásával mondod be a párt.":heldPair?"Megvan a Király + Felső pár, de bemondani csak akkor tudod, amikor te jössz ki.":"Most nincs bemondható pár: egy színből Király és Felső kell. Ha mindkettő nálad van és te jössz ki, a két bemondógomb a lapjaid felett jelenik meg.";$('marriageHeading').classList.toggle("hidden",!marriages.length);const yourTurn=s.turn===s.player&&!s.finished;$("actionHint").textContent=s.showing_recent_trick?`${s.message} Várj 5 másodpercet, amíg megnézed az ütést.`:s.finished?`${s.names[s.winner]} nyert! ${s.end_reason}. Végeredmény: ${s.points[0]}–${s.points[1]} pont.`:yourTurn?"Válassz ki egy lapot a kijátszáshoz.":s.mode==="online"&&s.names[1]==="Várakozás..."?"Küldd el a szobakódot a másik játékosnak.":"A másik játékos lépésére várunk.";
  $("roomBadge").classList.toggle("hidden",s.mode!=="online");$("roomCodeLabel").textContent=s.code;
  if(s.finished){clearInterval(pollTimer);toast(s.winner===s.player?`Nyertél: ${s.end_reason}!`:`A leosztás véget ért: ${s.end_reason}.`,true);}
}
$("aiButton").onclick=()=>create("ai");$("hotseatButton").onclick=()=>create("hotseat");$("onlineButton").onclick=()=>create("online");$("joinButton").onclick=join;$("roomCode").addEventListener("input",e=>e.target.value=e.target.value.toUpperCase().replace(/[^A-Z0-9]/g,""));
$("hand").addEventListener("click",e=>{const card=e.target.closest("[data-card]");if(!card||card.classList.contains("disabled"))return;act("play",{card_id:card.dataset.card});});
$("aiDifficulty").addEventListener("change",()=>{const text={1:"Kezdő: véletlenszerű, de szabályos lapválasztás.",2:"Könnyű: olcsó ütőlapot választ, ha tud; különben kis lapot dob.",3:"Közepes: figyelembe veszi az ütés értékét és az aduk megtartását.",4:"Nehéz: 24 lehetséges rejtett lapelosztással számol.",5:"Mester: 96 lehetséges rejtett lapelosztással számol."};$("difficultyHelp").textContent=text[Number($("aiDifficulty").value)];});
async function refreshTrainingArchiveStatus(){try{const stats=await request("/api/ai/stats");$("learningOption").textContent="6 · Tanuló — előkészítés ("+stats.saved_games+"/"+stats.capacity+" parti mentve)";}catch{}}
refreshTrainingArchiveStatus();
const renderWithBase=render;
render=function(s){renderWithBase(s);if(s.mode==="ai"){$("modeLabel").textContent+=" · "+["","KEZDŐ","KÖNNYŰ","KÖZEPES","NEHÉZ","MESTER"][s.ai_difficulty||3];if(s.finished)refreshTrainingArchiveStatus();}};
$("marriages").addEventListener("click",e=>{const b=e.target.closest("[data-marriage][data-card]");if(!b)return;act("play",{card_id:b.dataset.card,declare_suit:b.dataset.marriage});});
$("closeButton").onclick=()=>act("close");$("exchangeButton").onclick=()=>act("exchange");$("leaveButton").onclick=()=>{clearInterval(pollTimer);session=null;gameState=null;localStorage.removeItem("snapszer-session");$("game").classList.add("hidden");$("lobby").classList.remove("hidden");$("newGameTop").classList.add("hidden");};$("newGameTop").onclick=()=>$("leaveButton").click();$("copyButton").onclick=async()=>{try{await navigator.clipboard.writeText(`${location.origin} — szobakód: ${session.code}`);toast("A meghívó címét és a kódot másoltam.");}catch{toast(`Szobakód: ${session.code}`);}};
const saved=localStorage.getItem("snapszer-session");if(saved){try{session=JSON.parse(saved);startView();}catch{localStorage.removeItem("snapszer-session");}}
