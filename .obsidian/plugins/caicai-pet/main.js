const { Plugin } = require('obsidian');

// ─── LEVEL SPRITES ───────────────────────────────────────────
// Each level has open + blink variants. Base body is the same black cat,
// with accessories added per level.

// Shared: base cat body parts
const B = '#1a1a1a';  // body
const E = '#44dd66';  // eyes
const N = '#ff8899';  // nose
const I = '#443333';  // inner ear
const V = '#2d2d2d';  // belly
const X = '#333';     // closed eyes

// Helper: build SVG from rect array
function buildSVG(rects, viewBox = '0 0 20 20') {
  return `<svg xmlns='http://www.w3.org/2000/svg' viewBox='${viewBox}' shape-rendering='crispEdges'>${rects.map(([x,y,w,h,c]) => `<rect x='${x}' y='${y}' width='${w}' height='${h}' fill='${c}'/>`).join('')}</svg>`;
}

// Base cat body (shared across levels)
const BASE_BODY = [
  [4,1,2,2,B],[14,1,2,2,B],           // ears
  [5,2,1,1,I],[14,2,1,1,I],            // inner ears
  [4,3,12,2,B],                         // head
  [4,5,12,1,B],                         // eye row bg
  [4,6,12,1,B],[9,6,2,1,N],            // nose row
  [5,7,10,1,B],                         // chin
  [4,8,12,1,B],[7,8,6,1,V],            // body top
  [4,9,12,2,B],[6,9,8,2,V],            // body mid
  [4,11,12,1,B],[6,11,8,1,V],          // body low
  [5,12,3,1,B],[12,12,3,1,B],          // paws
  [16,9,1,1,B],[17,8,1,1,B],[18,7,1,1,B],[18,6,1,1,B],[19,5,1,1,B],[19,4,1,1,B],[18,4,1,1,B], // tail — curled up
];

const EYES_OPEN = [[6,5,2,1,E],[12,5,2,1,E]];
const EYES_CLOSED = [[6,5,2,1,X],[12,5,2,1,X]];

// Level 1: Kitten — smaller body, big head, no tail
const LV1_BODY = [
  [6,3,2,2,B],[14,3,2,2,B],            // big ears
  [7,4,1,1,I],[14,4,1,1,I],            // inner ears
  [6,5,10,2,B],                          // big head
  [6,7,10,1,B],                          // eye row
  [6,8,10,1,B],[10,8,2,1,N],            // nose
  [7,9,8,1,B],                           // chin
  [7,10,8,1,B],[9,10,4,1,V],            // tiny body
  [7,11,8,1,B],[9,11,4,1,V],            // body
  [8,12,2,1,B],[12,12,2,1,B],           // tiny paws
];
const LV1_EYES_OPEN = [[8,7,2,1,E],[13,7,2,1,E]];
const LV1_EYES_CLOSED = [[8,7,2,1,X],[13,7,2,1,X]];

// Level 3: Smart Cat — base + glasses
const GLASSES = [
  [5,4,3,1,'#6688cc'],[11,4,3,1,'#6688cc'],  // lens frames
  [5,5,1,1,'#88aaee'],[7,5,1,1,'#88aaee'],    // left lens shine
  [11,5,1,1,'#88aaee'],[13,5,1,1,'#88aaee'],  // right lens shine
  [8,4,3,1,'#6688cc'],                          // bridge
];

// Level 4: Scholar Cat — base + tiny book
const BOOK = [
  [17,3,3,1,'#cc6644'],                  // book top
  [17,4,3,2,'#dd8866'],                  // book pages
  [17,6,3,1,'#cc6644'],                  // book bottom
  [18,4,1,2,'#fff'],                      // page edge
];

// Level 5: Brain Cat — base + sparkles + glow
const SPARKLES = [
  [2,2,1,1,'#ffdd44'],[18,1,1,1,'#ffdd44'],   // stars
  [1,8,1,1,'#ffdd44'],[19,5,1,1,'#ffdd44'],
  [3,12,1,1,'#ffdd44'],[17,11,1,1,'#ffdd44'],
];
const BRAIN = [
  [17,2,2,1,'#ff88aa'],[16,3,3,1,'#ff88aa'],  // brain
  [16,4,3,1,'#ff99bb'],[17,5,2,1,'#ff88aa'],
];
const GLOW = [
  [3,4,1,1,'#44dd6644'],[16,4,1,1,'#44dd6644'],  // eye glow aura
];

// Build all level sprites
const SPRITES = {
  1: {
    open: buildSVG([...LV1_BODY, ...LV1_EYES_OPEN]),
    blink: buildSVG([...LV1_BODY, ...LV1_EYES_CLOSED]),
  },
  2: {
    open: buildSVG([...BASE_BODY, ...EYES_OPEN]),
    blink: buildSVG([...BASE_BODY, ...EYES_CLOSED]),
  },
  3: {
    open: buildSVG([...BASE_BODY, ...EYES_OPEN, ...GLASSES]),
    blink: buildSVG([...BASE_BODY, ...EYES_CLOSED, ...GLASSES]),
  },
  4: {
    open: buildSVG([...BASE_BODY, ...EYES_OPEN, ...GLASSES, ...BOOK]),
    blink: buildSVG([...BASE_BODY, ...EYES_CLOSED, ...GLASSES, ...BOOK]),
  },
  5: {
    open: buildSVG([...BASE_BODY, ...EYES_OPEN, ...GLASSES, ...BRAIN, ...SPARKLES]),
    blink: buildSVG([...BASE_BODY, ...EYES_CLOSED, ...GLASSES, ...BRAIN, ...SPARKLES]),
  },
};

// Backwards compat aliases
const CAT_OPEN = SPRITES[2].open;
const CAT_BLINK = SPRITES[2].blink;

function synthesizeMeow(audioCtx) {
  const now = audioCtx.currentTime;
  const duration = 0.35;

  // Main tone — cat meow is a descending frequency sweep
  const osc = audioCtx.createOscillator();
  const gain = audioCtx.createGain();
  const filter = audioCtx.createBiquadFilter();

  osc.type = 'sawtooth';
  osc.frequency.setValueAtTime(900, now);
  osc.frequency.exponentialRampToValueAtTime(500, now + 0.08);
  osc.frequency.exponentialRampToValueAtTime(700, now + 0.15);
  osc.frequency.exponentialRampToValueAtTime(400, now + duration);

  filter.type = 'bandpass';
  filter.frequency.setValueAtTime(1200, now);
  filter.Q.setValueAtTime(2, now);

  gain.gain.setValueAtTime(0, now);
  gain.gain.linearRampToValueAtTime(0.15, now + 0.03);
  gain.gain.setValueAtTime(0.15, now + 0.1);
  gain.gain.exponentialRampToValueAtTime(0.001, now + duration);

  osc.connect(filter);
  filter.connect(gain);
  gain.connect(audioCtx.destination);

  osc.start(now);
  osc.stop(now + duration);

  // Second harmonic for richness
  const osc2 = audioCtx.createOscillator();
  const gain2 = audioCtx.createGain();

  osc2.type = 'sine';
  osc2.frequency.setValueAtTime(1800, now);
  osc2.frequency.exponentialRampToValueAtTime(1000, now + 0.08);
  osc2.frequency.exponentialRampToValueAtTime(1400, now + 0.15);
  osc2.frequency.exponentialRampToValueAtTime(800, now + duration);

  gain2.gain.setValueAtTime(0, now);
  gain2.gain.linearRampToValueAtTime(0.05, now + 0.03);
  gain2.gain.exponentialRampToValueAtTime(0.001, now + duration);

  osc2.connect(gain2);
  gain2.connect(audioCtx.destination);

  osc2.start(now);
  osc2.stop(now + duration);
}

module.exports = class CaicaiPetPlugin extends Plugin {
  async onload() {
    this.audioCtx = null;
    this.blinkTimer = null;
    this.state = await this.loadState();

    // Create pet container with level-appropriate sprite
    this.petEl = document.createElement('div');
    this.petEl.addClass('caicai-pet');
    this.petEl.innerHTML = this.getSprite('open');
    document.body.appendChild(this.petEl);


    // Speech bubble
    this.bubbleEl = document.createElement('div');
    this.bubbleEl.addClass('caicai-bubble');
    this.bubbleEl.style.display = 'none';
    document.body.appendChild(this.bubbleEl);

    // Styles
    const style = document.createElement('style');
    style.textContent = `
      .caicai-pet {
        position: fixed;
        bottom: 16px;
        right: 24px;
        width: 56px;
        height: 56px;
        z-index: 9999;
        cursor: pointer;
        image-rendering: pixelated;
        animation: caicai-bob 3s ease-in-out infinite;
        transition: transform 0.1s;
      }
      .caicai-pet:hover {
        transform: scale(1.1);
      }
      .caicai-pet:active {
        transform: scale(0.95);
      }
      .caicai-pet svg {
        width: 100%;
        height: 100%;
      }
      .caicai-bubble {
        position: fixed;
        bottom: 78px;
        right: 16px;
        background: white;
        border: 2px solid #888;
        border-radius: 8px;
        padding: 6px 12px;
        font-family: 'Courier New', monospace;
        font-size: 13px;
        font-weight: bold;
        white-space: nowrap;
        color: #333;
        z-index: 10000;
        pointer-events: none;
        opacity: 0;
        transition: opacity 0.15s;
      }
      .caicai-bubble.show {
        opacity: 1;
      }
      .caicai-bubble::after {
        content: '';
        position: absolute;
        bottom: -8px;
        right: 20px;
        width: 0;
        height: 0;
        border-left: 6px solid transparent;
        border-right: 6px solid transparent;
        border-top: 8px solid #888;
      }
      @keyframes caicai-bob {
        0%, 100% { bottom: 16px; }
        50% { bottom: 19px; }
      }
      .caicai-hearts {
        position: fixed;
        bottom: 40px;
        right: 30px;
        z-index: 9998;
        pointer-events: none;
      }
      .caicai-heart {
        position: absolute;
        font-size: 16px;
        opacity: 1;
        animation: caicai-heart-float 1.2s ease-out forwards;
      }
      @keyframes caicai-pipa-bounce {
        0%, 100% { transform: translateY(0); }
        50% { transform: translateY(-10px); }
      }
      @keyframes caicai-heart-float {
        0% {
          transform: translate(0, 0) scale(0.5);
          opacity: 1;
        }
        50% {
          opacity: 1;
        }
        100% {
          transform: translate(var(--dx), -60px) scale(1);
          opacity: 0;
        }
      }
    `;
    document.head.appendChild(style);
    this.styleEl = style;

    // Hearts container
    this.heartsEl = document.createElement('div');
    this.heartsEl.addClass('caicai-hearts');
    document.body.appendChild(this.heartsEl);

    // Click handler
    this.petEl.addEventListener('click', () => this.onPetClick());

    // Blink loop
    this.startBlinking();

    // Pipa reminder every hour
    this.pipaTimer = null;
    this.startPipaReminder();

    // Meow texts
    // Level-based speech lines
    this.speechByLevel = {
      1: ['*tiny miao~*', 'Pet me!', 'I\'m just a kitten~', 'miao!', 'So much to learn!'],
      2: ['Caicai is here!', 'Pet me, pet me!', 'miao~ I love you!', '*purrs*', '*nuzzles*'],
      3: ['*adjusts glasses* miao!', 'Interesting wiki today~', 'Have you compiled lately?', 'Knowledge is power, miao!', 'Pet me, I\'m thinking~'],
      4: ['*looks up from book* miao~', 'The wiki grows stronger!', 'Your brain is impressive~', 'Scholar Cat approves!', 'More sources please~'],
      5: ['*radiates wisdom* ...miao.', 'We\'ve come so far, Jing~', 'Brain Cat sees all!', 'Peak knowledge achieved!', 'The ultimate miao~'],
    };

    // Mood-based extras
    this.moodSpeech = {
      lonely: ['I missed you!', 'You\'re finally back!', 'Don\'t leave me so long!'],
      sleepy: ['*yawns* oh, hi~', 'Was napping... miao~', '*blinks awake*'],
      excited: ['Let\'s go!!', 'So much energy!', 'What are we building?!'],
    };
  }

  onPetClick() {
    // Init audio on first click (browser policy)
    if (!this.audioCtx) {
      this.audioCtx = new AudioContext();
    }

    // Play meow sound
    synthesizeMeow(this.audioCtx);

    // Record pet
    this.state.total_pets = (this.state.total_pets || 0) + 1;
    this.state.xp = (this.state.xp || 0) + 1;
    const oldLevel = this.state.level;
    this.updateLevel();
    this.saveState();

    // Level up — flash and transform into new sprite
    if (this.state.level !== oldLevel) {
      this.petEl.style.filter = 'brightness(3)';
      this.petEl.style.transform = 'scale(1.3)';
      setTimeout(() => {
        this.petEl.innerHTML = this.getSprite('open');
        this.petEl.style.filter = '';
        this.petEl.style.transform = '';
      }, 400);
    }

    // Pick smart speech based on level + mood
    const level = this.state.level || 1;
    const mood = this.state.mood || 'happy';
    let pool = this.speechByLevel[level] || this.speechByLevel[1];
    if (this.moodSpeech[mood]) {
      pool = pool.concat(this.moodSpeech[mood]);
    }
    const text = pool[Math.floor(Math.random() * pool.length)];
    this.bubbleEl.textContent = text;
    this.bubbleEl.style.display = 'block';
    this.bubbleEl.addClass('show');

    // Jump animation
    this.petEl.style.animation = 'none';
    this.petEl.offsetHeight; // reflow
    this.petEl.style.bottom = '28px';
    setTimeout(() => {
      this.petEl.style.bottom = '';
      this.petEl.style.animation = 'caicai-bob 3s ease-in-out infinite';
    }, 200);

    // Spawn hearts
    this.spawnHearts();

    // Hide bubble after delay
    clearTimeout(this.bubbleTimeout);
    this.bubbleTimeout = setTimeout(() => {
      this.bubbleEl.removeClass('show');
      setTimeout(() => { this.bubbleEl.style.display = 'none'; }, 150);
    }, 1500);
  }

  spawnHearts() {
    const hearts = ['❤️', '💕', '💖', '🩷', '♥️'];
    const count = 3 + Math.floor(Math.random() * 3); // 3-5 hearts
    for (let i = 0; i < count; i++) {
      setTimeout(() => {
        const heart = document.createElement('span');
        heart.addClass('caicai-heart');
        heart.textContent = hearts[Math.floor(Math.random() * hearts.length)];
        heart.style.setProperty('--dx', (Math.random() - 0.5) * 50 + 'px');
        heart.style.left = Math.random() * 30 + 'px';
        heart.style.fontSize = (12 + Math.random() * 10) + 'px';
        this.heartsEl.appendChild(heart);
        setTimeout(() => heart.remove(), 1300);
      }, i * 100);
    }
  }

  getSprite(type) {
    const level = (this.state && this.state.level) || 1;
    const sprites = SPRITES[level] || SPRITES[1];
    return sprites[type] || sprites.open;
  }

  startBlinking() {
    const blink = () => {
      this.petEl.innerHTML = this.getSprite('blink');
      setTimeout(() => {
        this.petEl.innerHTML = this.getSprite('open');
      }, 150);
    };

    this.blinkTimer = setInterval(() => {
      blink();
      // Sometimes double blink
      if (Math.random() < 0.3) {
        setTimeout(blink, 300);
      }
    }, 3000 + Math.random() * 2000);
  }

  startPipaReminder() {
    const pipaMessages = [
      'Time to play Pipa! 🎵',
      'Pipa break! Your fingers miss the strings~',
      'miao~ Go practice Pipa!',
      '1 hour already! Pipa time~ 🎶',
      '*nudges* Pipa. Now. Please~',
      'Your Pipa is waiting for you! 🎵',
    ];

    // Remind every 60 minutes
    this.pipaTimer = setInterval(() => {
      const text = pipaMessages[Math.floor(Math.random() * pipaMessages.length)];

      // Show bubble
      this.bubbleEl.textContent = text;
      this.bubbleEl.style.display = 'block';
      this.bubbleEl.addClass('show');

      // Bounce the cat to get attention
      this.petEl.style.animation = 'none';
      this.petEl.offsetHeight;
      this.petEl.style.animation = 'caicai-pipa-bounce 0.3s ease 4';
      setTimeout(() => {
        this.petEl.style.animation = 'caicai-bob 3s ease-in-out infinite';
      }, 1200);

      // Play a gentle chime
      if (!this.audioCtx) this.audioCtx = new AudioContext();
      this.playChime(this.audioCtx);

      // Spawn music notes
      this.spawnHearts();

      // Hide after 5 seconds (longer than normal since it's a reminder)
      setTimeout(() => {
        this.bubbleEl.removeClass('show');
        setTimeout(() => { this.bubbleEl.style.display = 'none'; }, 150);
      }, 5000);

    }, 60 * 60 * 1000); // 1 hour
  }

  playChime(audioCtx) {
    const now = audioCtx.currentTime;
    // Two gentle notes like a Pipa pluck
    [440, 554].forEach((freq, i) => {
      const osc = audioCtx.createOscillator();
      const gain = audioCtx.createGain();
      osc.type = 'triangle';
      osc.frequency.setValueAtTime(freq, now + i * 0.15);
      gain.gain.setValueAtTime(0, now + i * 0.15);
      gain.gain.linearRampToValueAtTime(0.12, now + i * 0.15 + 0.02);
      gain.gain.exponentialRampToValueAtTime(0.001, now + i * 0.15 + 0.4);
      osc.connect(gain);
      gain.connect(audioCtx.destination);
      osc.start(now + i * 0.15);
      osc.stop(now + i * 0.15 + 0.5);
    });
  }

  async loadState() {
    const statePath = this.app.vault.adapter.basePath + '/pet/caicai-state.json';
    try {
      const fs = require('fs');
      const data = fs.readFileSync(statePath, 'utf-8');
      return JSON.parse(data);
    } catch {
      return { xp: 0, level: 1, level_name: 'Kitten', total_pets: 0, mood: 'curious' };
    }
  }

  saveState() {
    const statePath = this.app.vault.adapter.basePath + '/pet/caicai-state.json';
    try {
      const fs = require('fs');
      this.state.last_pet = new Date().toISOString();
      fs.writeFileSync(statePath, JSON.stringify(this.state, null, 2));
    } catch (e) {
      // silently fail
    }
  }

  updateLevel() {
    const levels = [
      { level: 1, name: 'Kitten', xp: 0 },
      { level: 2, name: 'Cat', xp: 50 },
      { level: 3, name: 'Smart Cat', xp: 150 },
      { level: 4, name: 'Scholar Cat', xp: 400 },
      { level: 5, name: 'Brain Cat', xp: 1000 },
    ];
    for (let i = levels.length - 1; i >= 0; i--) {
      if (this.state.xp >= levels[i].xp) {
        this.state.level = levels[i].level;
        this.state.level_name = levels[i].name;
        break;
      }
    }
  }

  onunload() {
    this.petEl?.remove();
    this.bubbleEl?.remove();
    this.heartsEl?.remove();
    this.styleEl?.remove();
    if (this.blinkTimer) clearInterval(this.blinkTimer);
    if (this.pipaTimer) clearInterval(this.pipaTimer);
    if (this.audioCtx) this.audioCtx.close();
  }
};
