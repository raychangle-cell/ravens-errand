from pathlib import Path
html = r"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>Raven’s Errand — A Choice-Driven Adventure</title>
  <style>
    :root{
      --bg:#000;
      --fg:#fff;
      --muted:rgba(255,255,255,.75);
      --link:#4169e1;
      --linkHover:#00bfff;
      --danger:#ff4d4d;
      --good:#66ff66;
      --panel:#111;
      --border:rgba(255,255,255,.25);
      --shadow:rgba(0,0,0,.55);
      --maxw: 900px;
    }
    html,body{height:100%; margin:0; background:var(--bg); color:var(--fg); font-family: Georgia, serif;}
    .wrap{max-width:var(--maxw); margin:0 auto; padding:6vh 6vw;}
    @media (min-width: 900px){ .wrap{padding:6vh 0;} }
    h1,h2,h3{line-height:1.05; margin:.2em 0 .6em 0;}
    h1{font-size:2.3rem;}
    h2{font-size:1.75rem;}
    p{line-height:1.6; font-size:1.12rem; margin:.65em 0;}
    .muted{color:var(--muted);}
    .scene-img{width:100%; max-width:1200px; height:auto; max-height:520px; display:block; margin:0 auto 1rem auto; border-radius:14px; box-shadow:0 10px 24px var(--shadow); border:1px solid var(--border);}
    .card{background:linear-gradient(180deg, rgba(255,255,255,.06), rgba(255,255,255,.03)); border:1px solid var(--border); border-radius:16px; padding:1rem 1.1rem; margin:1rem 0; box-shadow:0 10px 22px var(--shadow);}
    .stats{display:flex; flex-wrap:wrap; gap:.6rem; align-items:center; justify-content:space-between;}
    .statline{display:flex; gap:.8rem; flex-wrap:wrap; font-size:1rem;}
    .pill{border:1px solid var(--border); border-radius:999px; padding:.35rem .7rem; background:rgba(0,0,0,.25);}
    .pill b{font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, "Liberation Mono", "Courier New", monospace;}
    .controls{display:flex; gap:.6rem; flex-wrap:wrap; align-items:center; justify-content:flex-end;}
    button{
      font:inherit;
      font-weight:700;
      color:var(--fg);
      background:transparent;
      border:2px solid var(--border);
      border-radius:999px;
      padding:.45rem .9rem;
      cursor:pointer;
      transition:transform .08s ease, border-color .15s ease, color .15s ease;
    }
    button:hover{border-color:rgba(255,255,255,.6); color:#fff;}
    button:active{transform:scale(.98);}
    a, .choice{
      color:var(--link);
      text-decoration:none;
      font-weight:700;
      cursor:pointer;
      border-bottom:2px solid rgba(65,105,225,.45);
      transition:color .15s ease, border-color .15s ease;
    }
    a:hover, .choice:hover{color:var(--linkHover); border-color:rgba(0,191,255,.55);}
    .choices{display:flex; flex-direction:column; gap:.55rem; margin-top:1rem;}
    .choiceRow{padding:.65rem .8rem; border:1px solid var(--border); border-radius:14px; background:rgba(0,0,0,.22);}
    .choiceHint{display:block; color:var(--muted); font-weight:400; font-size:.98rem; margin-top:.2rem;}
    .log{font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, "Liberation Mono", "Courier New", monospace;
         font-size:.95rem; color:rgba(255,255,255,.78); white-space:pre-wrap; line-height:1.4; margin-top:.4rem;}
    .flash{animation:flash 650ms ease;}
    @keyframes flash{0%{filter:brightness(1.25)}100%{filter:brightness(1)}}
    .tag{display:inline-block; padding:.12rem .55rem; border-radius:999px; border:1px solid var(--border); margin-right:.4rem; font-size:.95rem;}
    .tag.good{border-color:rgba(102,255,102,.45); color:rgba(102,255,102,.95);}
    .tag.bad{border-color:rgba(255,77,77,.5); color:rgba(255,77,77,.95);}
    .footer{margin-top:1.6rem; color:rgba(255,255,255,.6); font-size:.98rem;}
    .sr{position:absolute; left:-9999px; width:1px; height:1px; overflow:hidden;}
    .tiny{font-size:.98rem;}
  </style>
</head>
<body>
  <main class="wrap">
    <div class="card stats" aria-live="polite">
      <div class="statline">
        <span class="pill"><b>Resolve</b>: <span id="stResolve">3</span></span>
        <span class="pill"><b>Supplies</b>: <span id="stSupplies">3</span></span>
        <span class="pill"><b>Trust</b>: <span id="stTrust">2</span></span>
        <span class="pill"><b>Time</b>: <span id="stTime">4</span></span>
      </div>
      <div class="controls">
        <button id="btnMute" type="button" aria-pressed="false">Audio: Off</button>
        <button id="btnRestart" type="button">Restart</button>
      </div>
    </div>

    <img id="sceneImg" class="scene-img" alt="Scene illustration" />

    <section class="card">
      <h1 id="title"></h1>
      <p id="text"></p>
      <div id="choices" class="choices"></div>
      <div class="footer">
        <div><span class="muted">Tip:</span> Your choices change stats and unlock endings.</div>
        <div class="tiny muted">This is a standalone HTML game (no external assets). Save it anywhere and open in a browser.</div>
      </div>
    </section>

    <section class="card">
      <h2>Journey Log</h2>
      <div id="log" class="log" aria-live="polite"></div>
    </section>

    <p class="muted tiny">Made in a “Twine-like” branching style: readable scenes, meaningful choices, and consequence-driven endings.</p>
  </main>

<script>
/* =========================
   Raven’s Errand — Engine
   ========================= */

const SFX = {
  click: new Audio("data:audio/wav;base64,UklGRlQAAABXQVZFZm10IBAAAAABAAEAQB8AAIA+AAACABAAZGF0YVAAAAAAgP8AAP//AAD//wAA//8AAP//AAD//wAA//8AAP//AAD//wAA//8AAP//AAD//wAA"),
  ping:  new Audio("data:audio/wav;base64,UklGRlQAAABXQVZFZm10IBAAAAABAAEAQB8AAIA+AAACABAAZGF0YVAAAAAAAP8AAP//AACAAAD//wAAAP8AAP//AACAAAD//wAAAP8AAP//AACAAAD//wAA")
};

let audioOn = false;
function playSfx(a){
  try{
    if(!audioOn) return;
    a.currentTime = 0;
    a.volume = 0.45;
    a.play();
  }catch(e){}
}

const state0 = { resolve:3, supplies:3, trust:2, time:4, flags:{} };
let state = structuredClone(state0);

function clamp(n,min,max){ return Math.max(min, Math.min(max,n)); }

function applyDelta(delta){
  const before = {...state};
  if(delta.resolve)  state.resolve  = clamp(state.resolve  + delta.resolve, 0, 6);
  if(delta.supplies) state.supplies = clamp(state.supplies + delta.supplies,0, 6);
  if(delta.trust)    state.trust    = clamp(state.trust    + delta.trust,  0, 6);
  if(delta.time)     state.time     = clamp(state.time     + delta.time,   0, 6);
  if(delta.flags){
    for(const [k,v] of Object.entries(delta.flags)){ state.flags[k] = v; }
  }
  const changes = [];
  for(const k of ["resolve","supplies","trust","time"]){
    const d = state[k]-before[k];
    if(d!==0) changes.push(`${k}${d>0?"+":""}${d}`);
  }
  return changes.length ? changes.join(", ") : "no stat change";
}

function svgScene(title, subtitle, mood){
  // mood: "night" | "storm" | "fire" | "dawn"
  const bg = {
    night: ["#070812","#0a0b16","#111430"],
    storm: ["#070a0d","#0c121a","#1b2636"],
    fire:  ["#120505","#260707","#3a0f08"],
    dawn:  ["#080614","#1b1030","#2a2a55"]
  }[mood] || ["#000","#111","#222"];

  const accent = {
    night:"#7aa7ff",
    storm:"#66ffd6",
    fire:"#ff9b66",
    dawn:"#f5d76e"
  }[mood] || "#fff";

  const svg = `
  <svg xmlns="http://www.w3.org/2000/svg" width="1400" height="650" viewBox="0 0 1400 650">
    <defs>
      <linearGradient id="g" x1="0" x2="0" y1="0" y2="1">
        <stop offset="0" stop-color="${bg[0]}"/>
        <stop offset="0.55" stop-color="${bg[1]}"/>
        <stop offset="1" stop-color="${bg[2]}"/>
      </linearGradient>
      <radialGradient id="r" cx="70%" cy="30%" r="60%">
        <stop offset="0" stop-color="${accent}" stop-opacity="0.22"/>
        <stop offset="1" stop-color="${accent}" stop-opacity="0"/>
      </radialGradient>
      <filter id="grain">
        <feTurbulence type="fractalNoise" baseFrequency="0.85" numOctaves="2" stitchTiles="stitch"/>
        <feColorMatrix type="matrix" values="0 0 0 0 0.55  0 0 0 0 0.55  0 0 0 0 0.55  0 0 0 0.12 0"/>
      </filter>
    </defs>
    <rect width="1400" height="650" fill="url(#g)"/>
    <rect width="1400" height="650" fill="url(#r)"/>
    <g opacity="0.9">
      <path d="M0,520 C200,470 370,520 540,490 C720,450 900,520 1100,485 C1240,460 1340,470 1400,455 L1400,650 L0,650 Z"
            fill="rgba(0,0,0,0.35)"/>
      <path d="M0,560 C220,520 420,590 610,550 C790,510 940,600 1130,560 C1240,535 1340,540 1400,520 L1400,650 L0,650 Z"
            fill="rgba(0,0,0,0.45)"/>
    </g>
    <g filter="url(#grain)" opacity="0.65"><rect width="1400" height="650"/></g>
    <g>
      <text x="70" y="120" fill="rgba(255,255,255,0.95)" font-size="64" font-family="Georgia, serif">${escapeXml(title)}</text>
      <text x="72" y="168" fill="rgba(255,255,255,0.7)" font-size="28" font-family="Georgia, serif">${escapeXml(subtitle)}</text>
    </g>
    <g opacity="0.8">
      <circle cx="1070" cy="150" r="90" fill="${accent}" opacity="0.14"/>
      <circle cx="1070" cy="150" r="60" fill="${accent}" opacity="0.14"/>
      <circle cx="1070" cy="150" r="35" fill="${accent}" opacity="0.18"/>
    </g>
  </svg>`;
  return "data:image/svg+xml;charset=utf-8," + encodeURIComponent(svg);
}

function escapeXml(s){
  return String(s).replace(/[<>&"]/g, c => ({'<':'&lt;','>':'&gt;','&':'&amp;','"':'&quot;'}[c]));
}

/* =========================
   Story Content (Scenes)
   ========================= */

const scenes = {
  start: {
    title: "Raven’s Errand",
    mood: "night",
    text: `The city sleeps under a black sky. A single raven lands on your window ledge,
           carrying a sealed note: <span class="muted">“Deliver the lantern to the Old Gate before dawn.”</span>
           \n\nYou are the courier. You are also the one being watched.`,
    choices: [
      { label: "Open the note and read every line carefully.",
        hint: "+Trust, -Time (you learn the stakes, but waste precious minutes).",
        delta: { trust:+1, time:-1, flags:{ readNote:true } },
        next: "alley" },
      { label: "Pocket the note and leave immediately.",
        hint: "+Time (you move fast), but you might miss key information.",
        delta: { time:+0, flags:{ readNote:false } },
        next: "alley" },
      { label: "Light a candle and search your room for hidden symbols.",
        hint: "+Resolve, -Time (paranoia can be preparation).",
        delta: { resolve:+1, time:-1, flags:{ searchedRoom:true } },
        next: "alley" },
    ]
  },

  alley: {
    title: "The Narrow Alley",
    mood: "storm",
    text: `Rain starts without warning. The alley behind your building is a shortcut to the Old Gate,
           but the shadows here have names.\n\nA cloaked figure steps into your path and lifts a hand: “Lantern. Now.”`,
    choices: [
      { label: "Talk. Ask who sent them and why they want it.",
        hint: "Requires Trust ≥ 3 to keep them listening.",
        guard: () => state.trust >= 3,
        delta: { trust:+1, time:-1, flags:{ parley:true } },
        next: "parley" },
      { label: "Run into the rain and weave through the market stalls.",
        hint: "-Supplies (you drop something), -Time (the chase costs you).",
        delta: { supplies:-1, time:-1, flags:{ fled:true } },
        next: "market" },
      { label: "Stand your ground and bluff confidence.",
        hint: "+Resolve if you have it, but it might escalate.",
        delta: { resolve:+0, time:-1, flags:{ bluff:true } },
        next: "bluff" },
      { label: "Hand over a decoy pouch instead of the lantern.",
        hint: "Requires Supplies ≥ 3 (you must have packed a decoy).",
        guard: () => state.supplies >= 3,
        delta: { supplies:-1, trust:-1, flags:{ decoy:true } },
        next: "decoy" },
    ],
    fallbackText: "Some choices are locked because your stats are too low."
  },

  parley: {
    title: "Words in the Rain",
    mood: "storm",
    text: `Your calm voice slows their hand. The figure hesitates.\n\nThey whisper:
           “The Old Gate is a trap. If you walk in alone, you will not walk out.”`,
    choices: [
      { label: "Believe them and take the canal route instead.",
        hint: "+Time, -Supplies (the canal is longer and colder).",
        delta: { time:-1, supplies:-1, flags:{ canal:true } },
        next: "canal" },
      { label: "Accuse them of lying and push past.",
        hint: "+Resolve, -Trust (you burn the bridge).",
        delta: { resolve:+1, trust:-1, flags:{ defiant:true } },
        next: "market" },
      { label: "Ask them to come with you.",
        hint: "Requires Trust ≥ 4. If they agree, endings change.",
        guard: () => state.trust >= 4,
        delta: { trust:+0, time:-1, flags:{ ally:true } },
        next: "ally" },
    ]
  },

  bluff: {
    title: "A Dangerous Pause",
    mood: "night",
    text: `You don’t move. You don’t blink.\n\nThe figure circles you. “You’re brave,” they say,
           “or you’re desperate.” Behind them, more footsteps.`,
    choices: [
      { label: "Draw attention—shout for help.",
        hint: "-Trust (guards don’t like complications), -Time.",
        delta: { trust:-1, time:-1, flags:{ shouted:true } },
        next: "guards" },
      { label: "Offer a trade: information for safe passage.",
        hint: "Requires Trust ≥ 2. Better if you read the note.",
        guard: () => state.trust >= 2,
        delta: { trust:+1, time:-1, flags:{ traded:true } },
        next: "parley" },
      { label: "Strike first and sprint away while they flinch.",
        hint: "Requires Resolve ≥ 4. Otherwise you’ll get hurt.",
        guard: () => state.resolve >= 4,
        delta: { resolve:-1, time:-1, flags:{ struck:true } },
        next: "market" },
    ]
  },

  decoy: {
    title: "The Decoy",
    mood: "fire",
    text: `They snatch the pouch and tear it open. Their eyes flash with anger.\n\n“Clever,” they hiss,
           “but not clever enough.” The alley narrows behind you.`,
    choices: [
      { label: "Drop the lantern and escape while they hesitate.",
        hint: "You survive… but fail the mission.",
        delta: { trust:-1, time:+0, flags:{ failedMission:true } },
        next: "ending_fail" },
      { label: "Apologize, offer the real lantern, and ask for mercy.",
        hint: "Requires Trust ≥ 3 to avoid violence.",
        guard: () => state.trust >= 3,
        delta: { trust:+0, flags:{ surrendered:true } },
        next: "parley" },
      { label: "Climb the fire-escape ladder to the rooftops.",
        hint: "Costs Time but can save you.",
        delta: { time:-1, resolve:+1, flags:{ roof:true } },
        next: "rooftops" },
    ]
  },

  market: {
    title: "Market of Closed Stalls",
    mood: "dawn",
    text: `The market is a maze of canvas and rope. The rain turns stone into glass.
           \n\nYou spot three routes to the Old Gate: through the <b>bridge</b>, the <b>canal</b>, or the <b>chapel</b>.`,
    choices: [
      { label: "Cross the bridge under the lantern’s faint glow.",
        hint: "Faster, but exposed. -Time.",
        delta: { time:-1, flags:{ route:"bridge" } },
        next: "bridge" },
      { label: "Follow the canal—quiet, cold, and hidden.",
        hint: "-Supplies, but safer from eyes.",
        delta: { supplies:-1, flags:{ route:"canal" } },
        next: "canal" },
      { label: "Enter the chapel and ask the keeper for shelter.",
        hint: "+Trust if you’re honest; might cost Time.",
        delta: { trust:+1, time:-1, flags:{ route:"chapel" } },
        next: "chapel" },
    ]
  },

  guards: {
    title: "Lanternlight & Badges",
    mood: "storm",
    text: `Two guards appear—too quickly. They ask for your name, then for your bag.\n\nYour pulse tells you:
           someone called them <i>before</i> you shouted.`,
    choices: [
      { label: "Comply and hope procedure protects you.",
        hint: "High Trust helps here.",
        delta: { time:-1, flags:{ complied:true } },
        next: "inspection" },
      { label: "Lie about the lantern’s purpose.",
        hint: "Requires Resolve ≥ 3. Risky.",
        guard: () => state.resolve >= 3,
        delta: { trust:-1, time:-1, flags:{ lied:true } },
        next: "inspection" },
      { label: "Slip away into the crowd.",
        hint: "Costs Supplies, but avoids a search.",
        delta: { supplies:-1, time:-1, flags:{ slipped:true } },
        next: "market" },
    ]
  },

  inspection: {
    title: "Inspection",
    mood: "night",
    text: `A gloved hand reaches for the lantern.\n\nYou remember the note—whether you read it or not—said:
           <span class="muted">“Do not let anyone else touch it.”</span>`,
    choices: [
      { label: "Refuse politely. Hold eye contact. Do not yield.",
        hint: "Requires Resolve ≥ 4.",
        guard: () => state.resolve >= 4,
        delta: { resolve:+0, trust:-1, flags:{ refused:true } },
        next: "rooftops" },
      { label: "Let them take it to avoid conflict.",
        hint: "Mission fails.",
        delta: { trust:+0, flags:{ failedMission:true } },
        next: "ending_fail" },
      { label: "Offer to open it yourself and demonstrate it’s safe.",
        hint: "Works best if you read the note. +Trust.",
        delta: { trust:+1, time:-1, flags:{ demonstrated:true } },
        next: "market" },
    ]
  },

  chapel: {
    title: "The Small Chapel",
    mood: "dawn",
    text: `Inside, candles burn low. The keeper watches you like a person watches a storm:
           with patience and caution.\n\nThey say, “If you carry light, you carry responsibility.”`,
    choices: [
      { label: "Tell the truth about the errand.",
        hint: "+Trust, but you lose Time.",
        delta: { trust:+1, time:-1, flags:{ confessed:true } },
        next: "keeper" },
      { label: "Ask for food and bandages without explaining.",
        hint: "+Supplies if Trust ≥ 3.",
        guard: () => state.trust >= 3,
        delta: { supplies:+1, time:-1, flags:{ resupplied:true } },
        next: "keeper" },
      { label: "Leave immediately—chasing speed over safety.",
        hint: "-Time, but keeps your secrets.",
        delta: { time:-1, flags:{ hurried:true } },
        next: "bridge" },
    ]
  },

  keeper: {
    title: "The Keeper’s Warning",
    mood: "night",
    text: `The keeper leans close: “The Old Gate listens. It bargains. It never forgets.”
           \n\nThey press a small charm into your palm.`,
    choices: [
      { label: "Accept the charm and promise to return it.",
        hint: "+Resolve, +Trust.",
        delta: { resolve:+1, trust:+1, flags:{ charm:true } },
        next: "oldgate" },
      { label: "Decline and leave—no debts, no anchors.",
        hint: "-Trust, but saves Time.",
        delta: { trust:-1, time:+0, flags:{ charm:false } },
        next: "oldgate" },
      { label: "Ask the keeper to walk with you to the gate.",
        hint: "Requires Trust ≥ 4.",
        guard: () => state.trust >= 4,
        delta: { time:-1, flags:{ keeperAlly:true } },
        next: "oldgate" },
    ]
  },

  bridge: {
    title: "The Bridge",
    mood: "storm",
    text: `Wind screams across the bridge. Below, black water chews at stone.
           \n\nHalfway across, you see a second raven—this one wearing a ring of copper.`,
    choices: [
      { label: "Follow the raven’s flight path toward the Old Gate.",
        hint: "+Time (it guides you), but costs Resolve (fear).",
        delta: { time:+0, resolve:-1, flags:{ followedRaven:true } },
        next: "oldgate" },
      { label: "Ignore it and keep your eyes forward.",
        hint: "+Resolve.",
        delta: { resolve:+1, flags:{ ignoredRaven:true } },
        next: "oldgate" },
      { label: "Stop and examine the lantern closely.",
        hint: "If you read the note, you might notice something.",
        delta: { time:-1, flags:{ examined:true } },
        next: "lantern" },
    ]
  },

  lantern: {
    title: "Inside the Lantern",
    mood: "fire",
    text: `You open the lantern’s hatch. The flame is… wrong. It doesn’t burn upward.
           It curls inward, like it wants to become a secret.\n\nA thin whisper: “Name your price.”`,
    choices: [
      { label: "Offer your supplies for safe passage.",
        hint: "-Supplies, +Trust (you choose fairness).",
        delta: { supplies:-1, trust:+1, flags:{ bargained:"supplies" } },
        next: "oldgate" },
      { label: "Offer your time—promise something later.",
        hint: "-Time, +Resolve (you accept burden).",
        delta: { time:-1, resolve:+1, flags:{ bargained:"time" } },
        next: "oldgate" },
      { label: "Refuse the bargain and shut the lantern.",
        hint: "Requires Resolve ≥ 4.",
        guard: () => state.resolve >= 4,
        delta: { resolve:+0, flags:{ bargained:"refused" } },
        next: "oldgate" },
    ]
  },

  canal: {
    title: "The Canal Path",
    mood: "night",
    text: `The canal smells like old iron and forgotten coins. Footsteps echo here.
           \n\nYou see a reflection in the water that isn’t yours.`,
    choices: [
      { label: "Move quietly and conserve energy.",
        hint: "+Resolve, -Time.",
        delta: { resolve:+1, time:-1, flags:{ stealth:true } },
        next: "oldgate" },
      { label: "Sprint to outrun whatever follows.",
        hint: "-Resolve, -Time.",
        delta: { resolve:-1, time:-1, flags:{ sprinted:true } },
        next: "oldgate" },
      { label: "Stop and listen to the water’s warning.",
        hint: "+Trust if you’re willing to believe.",
        delta: { trust:+1, time:-1, flags:{ listened:true } },
        next: "oldgate" },
    ]
  },

  rooftops: {
    title: "Rooftop Lines",
    mood: "storm",
    text: `Tiles crack beneath your boots. The city looks like a map drawn by trembling hands.
           \n\nYou can see the Old Gate ahead—an arch of stone that drinks light.`,
    choices: [
      { label: "Leap the gap to reach the next roof.",
        hint: "Requires Resolve ≥ 4. Risky but fast.",
        guard: () => state.resolve >= 4,
        delta: { time:-1, resolve:-1, flags:{ leaped:true } },
        next: "oldgate" },
      { label: "Climb down carefully and re-enter the streets.",
        hint: "Safer. Costs Time.",
        delta: { time:-1, flags:{ climbedDown:true } },
        next: "oldgate" },
      { label: "Hide and wait for the pursuit to pass.",
        hint: "-Time, +Trust if you have an ally.",
        delta: { time:-1, flags:{ waited:true } },
        next: "oldgate" },
    ]
  },

  ally: {
    title: "An Unlikely Companion",
    mood: "dawn",
    text: `They step beside you. “I don’t like traps,” they say. “But I hate unfair ones more.”
           \n\nYou walk together. The city feels less sharp.`,
    choices: [
      { label: "Let them carry the lantern for a moment.",
        hint: "Tempting, but dangerous. (The note warned you.)",
        delta: { trust:-1, flags:{ sharedLantern:true } },
        next: "ending_fail" },
      { label: "Keep the lantern yourself and accept their guidance.",
        hint: "+Trust.",
        delta: { trust:+1, time:-1, flags:{ guided:true } },
        next: "oldgate" },
    ]
  },

  oldgate: {
    title: "The Old Gate",
    mood: "fire",
    text: `The arch stands like a sentence you can’t undo.\n\nA voice from within the stone:
           “Courier. Pay, and pass.”\n\nYou feel the lantern’s flame tighten, waiting for your decision.`,
    choices: [
      { label: "Pay with supplies: place food and coin at the threshold.",
        hint: "Needs Supplies ≥ 2.",
        guard: () => state.supplies >= 2,
        delta: { supplies:-2, flags:{ paid:"supplies" } },
        next: "final" },
      { label: "Pay with resolve: speak your true name and accept the consequences.",
        hint: "Needs Resolve ≥ 4.",
        guard: () => state.resolve >= 4,
        delta: { resolve:-1, trust:+1, flags:{ paid:"name" } },
        next: "final" },
      { label: "Pay with trust: ask an ally/keeper to negotiate.",
        hint: "Needs Trust ≥ 4 and an ally flag.",
        guard: () => state.trust >= 4 && (state.flags.keeperAlly || state.flags.ally),
        delta: { trust:-1, flags:{ paid:"negotiated" } },
        next: "final" },
      { label: "Refuse to pay and attempt to force your way through.",
        hint: "If Time is low, you may be swallowed by the gate.",
        delta: { time:-1, flags:{ paid:"refused" } },
        next: "final" },
    ]
  },

  final: {
    title: "Threshold",
    mood: "dawn",
    text: `The stone hums. The lantern’s flame becomes a thin thread, tying you to whatever comes next.`,
    choices: [
      { label: "Step through the arch with the lantern held high.",
        hint: "Endings depend on your stats and earlier choices.",
        delta: {},
        next: "ending" },
    ]
  },

  ending: {
    title: "Ending",
    mood: "dawn",
    text: "",
    choices: []
  },

  ending_fail: {
    title: "Ending — The Light Lost",
    mood: "night",
    text: `You survive, but the lantern does not.\n\nThe raven’s note dissolves in the rain.
           Somewhere, a door stays closed forever.\n\n<span class="tag bad">MISSION FAILED</span>`,
    choices: [
      { label: "Restart and try a different route.",
        hint: "New choices, new consequences.",
        delta: {},
        next: "start",
        restart:true
      },
    ]
  }
};

function computeEnding(){
  // Compute 3 main endings + 1 hidden, based on state + flags.
  const s = state;
  const f = state.flags;

  // Hidden: charm + bargained refused + resolve high
  if(f.charm && f.bargained === "refused" && s.resolve >= 5){
    return {
      title: "Ending — The Gate Remembers Your Courage",
      mood: "fire",
      text: `You refuse every bargain and keep your name.\n\nThe charm warms your palm.
             The Old Gate hesitates—for the first time in centuries—and opens without payment.\n\n
             On the other side, dawn is real.\n\n<span class="tag good">HIDDEN ENDING</span>
             <span class="tag good">COURAGE</span>`
    };
  }

  // Ending A: Prepared courier
  if(s.supplies >= 2 && s.trust >= 3 && s.time >= 2 && !f.failedMission){
    return {
      title: "Ending — The Courier Who Planned",
      mood: "dawn",
      text: `You pay fairly, arrive before the city fully wakes, and deliver the lantern intact.\n\n
             The Old Gate accepts your offering and returns something unexpected: <span class="muted">silence</span>.\n\n
             You leave with your life, your name, and a story that won’t sit still.\n\n
             <span class="tag good">SUCCESS</span> <span class="tag good">STABILITY</span>`
    };
  }

  // Ending B: Sacrifice
  if(s.resolve >= 4 && (f.paid === "name" || f.bargained === "time") && !f.failedMission){
    return {
      title: "Ending — The Price You Agreed To",
      mood: "fire",
      text: `You step through, and the lantern’s flame threads into your chest.\n\n
             You delivered it. The Old Gate keeps its promise.\n\n
             But the cost follows you like a second shadow.\n\n
             <span class="tag good">SUCCESS</span> <span class="tag bad">SACRIFICE</span>`
    };
  }

  // Ending C: Consumed by urgency / refusal
  if((s.time <= 1 || f.paid === "refused") && !f.failedMission){
    return {
      title: "Ending — Swallowed by Stone",
      mood: "night",
      text: `You try to force the world to cooperate.\n\nIt doesn’t.\n\n
             The gate drinks your lanternlight and closes like an eye.\n\n
             In the morning, people will say they heard a raven laugh.\n\n
             <span class="tag bad">FAILURE</span> <span class="tag bad">HUBRIS</span>`
    };
  }

  // Default: bittersweet
  return {
    title: "Ending — A Narrow Passage",
    mood: "storm",
    text: `You reach the Old Gate with just enough to pass.\n\n
           The lantern is delivered, but the city remembers the struggle more than the success.\n\n
           You walk away feeling older than yesterday.\n\n
           <span class="tag good">DELIVERED</span> <span class="tag bad">COSTLY</span>`
  };
}

function render(sceneId, opts={ fromChoice:null, changeText:null }){
  const sc = scenes[sceneId];
  if(!sc){ console.error("Missing scene:", sceneId); return; }

  // Set image (SVG data URI)
  const subtitle = (state.flags.route ? `Route: ${state.flags.route}` : "A branching story of choice & consequence");
  document.getElementById("sceneImg").src = svgScene(sc.title, subtitle, sc.mood);

  // Title/text
  document.getElementById("title").textContent = sc.title;

  // If ending node, compute ending content now
  let bodyText = sc.text;
  let choices = sc.choices;

  if(sceneId === "ending"){
    const end = computeEnding();
    bodyText = end.text;
    document.getElementById("title").textContent = end.title;
    document.getElementById("sceneImg").src = svgScene(end.title, "Your choices shaped this outcome", end.mood);
    choices = [
      { label: "Restart and explore a different ending.",
        hint: "Try boosting Trust, or refusing the lantern’s bargain.",
        delta: {}, next: "start", restart:true }
    ];
  }

  document.getElementById("text").innerHTML = bodyText;

  // Stats UI
  document.getElementById("stResolve").textContent  = state.resolve;
  document.getElementById("stSupplies").textContent = state.supplies;
  document.getElementById("stTrust").textContent    = state.trust;
  document.getElementById("stTime").textContent     = state.time;

  // Choices UI
  const cDiv = document.getElementById("choices");
  cDiv.innerHTML = "";

  const available = [];
  for(const ch of choices){
    if(ch.guard && !ch.guard()) continue;
    available.push(ch);
  }

  if(available.length === 0){
    const p = document.createElement("p");
    p.className = "muted";
    p.textContent = sc.fallbackText || "No available choices. Your path is blocked.";
    cDiv.appendChild(p);

    const back = document.createElement("div");
    back.className = "choiceRow";
    back.innerHTML = `<span class="choice">Restart</span><span class="choiceHint">Try a different approach.</span>`;
    back.querySelector(".choice").addEventListener("click", () => restart());
    cDiv.appendChild(back);
  } else {
    for(const ch of available){
      const row = document.createElement("div");
      row.className = "choiceRow";
      const a = document.createElement("span");
      a.className = "choice";
      a.textContent = ch.label;
      const hint = document.createElement("span");
      hint.className = "choiceHint";
      hint.textContent = ch.hint || "";
      row.appendChild(a);
      row.appendChild(hint);
      a.addEventListener("click", () => {
        playSfx(SFX.click);

        const change = applyDelta(ch.delta || {});
        appendLog(`→ ${ch.label}\n   (${change})`);

        // If mission failed flag set, go to fail ending immediately unless choice explicitly routes otherwise
        if(state.flags.failedMission && ch.next !== "ending_fail"){
          render("ending_fail");
          current = "ending_fail";
          flash();
          return;
        }

        // Restart behaviors
        if(ch.restart){
          restart();
          return;
        }

        current = ch.next;
        render(current);
        flash();
      });
      cDiv.appendChild(row);
    }
  }
}

function flash(){
  const card = document.querySelector(".card:nth-of-type(2)");
  card.classList.remove("flash");
  void card.offsetWidth;
  card.classList.add("flash");
}

function appendLog(line){
  const log = document.getElementById("log");
  const timeStamp = new Date().toLocaleTimeString([], {hour:'2-digit', minute:'2-digit'});
  log.textContent = `${log.textContent}${log.textContent ? "\n\n" : ""}${timeStamp} ${line}`;
}

function restart(){
  state = structuredClone(state0);
  document.getElementById("log").textContent = "";
  appendLog("Game restarted.");
  current = "start";
  render(current);
}

let current = "start";

/* =========================
   Controls
   ========================= */

document.getElementById("btnRestart").addEventListener("click", () => {
  playSfx(SFX.ping);
  restart();
});

document.getElementById("btnMute").addEventListener("click", (e) => {
  audioOn = !audioOn;
  e.currentTarget.textContent = `Audio: ${audioOn ? "On" : "Off"}`;
  e.currentTarget.setAttribute("aria-pressed", audioOn ? "true" : "false");
  if(audioOn) playSfx(SFX.ping);
});

/* Start */
appendLog("You received a raven’s note.");
render(current);
</script>
</body>
</html>
"""
out = Path("/mnt/data/Ravens_Errand_TwineStyle.html")
out.write_text(html, encoding="utf-8")
str(out)

