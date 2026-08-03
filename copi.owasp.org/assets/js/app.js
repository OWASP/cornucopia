// If you want to use Phoenix channels, run `mix help phx.gen.channel`
// to get started and then uncomment the line below.
// import "./user_socket.js"

// You can include dependencies in two ways.
//
// The simplest option is to put them in assets/vendor and
// import them using relative paths:
//
//     import "../vendor/some-package.js"
//
// Alternatively, you can `npm install some-package --prefix assets` and import
// them using a path starting with the package name:
//
//     import "some-package"
//

// Include phoenix_html to handle method=PUT/DELETE in forms and buttons.
import "phoenix_html"
// Establish Phoenix Socket and LiveView configuration.
import {Socket} from "phoenix"
import {LiveSocket} from "phoenix_live_view"
import topbar from "../vendor/topbar"
import dragula from "../vendor/dragula"

const ulidPattern = /^[0-9A-HJKMNP-TV-Z]{26}$/;

const isValidUlid = (value) => typeof value === 'string' && ulidPattern.test(value);

const exchangePlayerCapability = async (capability) => {
  if (typeof capability !== 'string' || capability.length === 0) {
    return;
  }

  const csrfToken = document.querySelector("meta[name='csrf-token']")?.getAttribute("content");

  if (!csrfToken) {
    return;
  }

  try {
    const response = await fetch('/api/player-capabilities/exchange', {
      method: 'POST',
      headers: {
        'X-CSRF-Token': csrfToken,
        'Content-Type': 'application/json'
      },
      credentials: 'same-origin',
      cache: 'no-store',
      body: JSON.stringify({ capability })
    });

    if (!response.ok) {
      throw new Error('Player capability exchange was rejected');
    }

    const result = await response.json();

    if (typeof result.redirect_to !== 'string' || !result.redirect_to.startsWith('/games/')) {
      throw new Error('Player capability exchange returned an invalid redirect');
    }

    window.location.assign(result.redirect_to);
  } catch (error) {
    console.warn('Unable to exchange player capability', error);
  }
};

const syncPlayerSession = (el) => {
  const persistenceMode = el?.dataset?.storePlayerSession;

  if (persistenceMode !== 'false') {
    return;
  }

  const gameId = el?.dataset?.gameId;
  const playerId = el?.dataset?.playerId;

  if (!isValidUlid(gameId) || !isValidUlid(playerId)) {
    return;
  }

  const csrfToken = document.querySelector("meta[name='csrf-token']")?.getAttribute("content");

  if (!csrfToken) {
    return;
  }

  return fetch(`/api/games/${gameId}/players/${playerId}/session`, {
    method: 'DELETE',
    headers: {
      'X-CSRF-Token': csrfToken,
      'Content-Type': 'application/json'
    },
    credentials: 'same-origin',
    cache: 'no-store'
  }).catch(error => console.warn('Unable to clear player session', error));
};

let Hooks = {}
Hooks.DragDrop = {
  mounted() {
    const getCardElement = (node) => {
      if (!node || typeof node.closest !== 'function') {
        return null;
      }

      return node.closest('[data-game][data-player][data-dealtcard]');
    };

    const drake = dragula([document.querySelector('#hand'), document.querySelector('#table')], {
      invalid: function (el, handle) {
        // Only allow dragging actual hand cards (with required data attributes) from non-player zones.
        const isPlayerZone = el.classList && el.classList.contains('card-player');
        const draggableCard = getCardElement(handle) || getCardElement(el) || el;
        const hasRequiredDataset = !!(draggableCard.dataset && draggableCard.dataset.game && draggableCard.dataset.player && draggableCard.dataset.dealtcard);

        return isPlayerZone || !hasRequiredDataset;
      },
      accepts: function (el, target, source, sibling) {
        console.log('accepts called', {target: target?.id, source: source?.id});
        const draggableCard = getCardElement(el) || el;

        // Only hand cards can be dropped on the table.
        if (!source || source.id !== 'hand') {
          return false;
        }

        if (!draggableCard.dataset || !draggableCard.dataset.game || !draggableCard.dataset.player || !draggableCard.dataset.dealtcard) {
          return false;
        }
        
        // Only allow dropping on table
        if (target && target.id === 'table') {
          // Check if "Your Card" section already has a card (not placeholder)
          const yourCardSection = Array.from(document.querySelectorAll('#table .card-player')).find(zone => {
            const nameDiv = zone.querySelector('.name');
            return nameDiv && (nameDiv.textContent.includes('Your Card') || nameDiv.textContent.includes('Drop a card'));
          });
          
          if (yourCardSection) {
            // Check if there's a card already (not the placeholder)
            const isPlaceholder = yourCardSection.textContent.includes('Drop a card');
            
            console.log('Your card section check:', {isPlaceholder});
            
            if (!isPlaceholder) {
              console.log('Blocked: card already on table');
              return false;
            }
          }
        }
        
        console.log('Accepting drop');
        return true;
      }
    });
    
    drake.on('drop', (element, target, source, sibling) => {
      console.log('Drop event', {target: target?.id});
      
      if (target && target.id === 'table') {
        const draggableCard = getCardElement(element) || element;
        const gameId = draggableCard?.dataset?.game;
        const playerId = draggableCard?.dataset?.player;
        const dealtCardId = draggableCard?.dataset?.dealtcard;

        if (!gameId || !playerId || !dealtCardId) {
          console.error('Blocked invalid card play request due to missing identifiers', {
            gameId,
            playerId,
            dealtCardId
          });
          drake.cancel(true);
          return;
        }

        fetch('/api/games/' + gameId + '/players/' + playerId + '/card', {
          method: 'PUT',
          headers: {
            'Content-Type': 'application/json',
            'X-CSRF-Token': csrfToken
          },
          credentials: 'same-origin',
          body: JSON.stringify({
            dealt_card_id: dealtCardId
          })
        }).then(response => {
          console.log('API response:', response.ok);
          if (!response.ok && source) {
            source.appendChild(element);
          }
          return response.ok;
        }).catch(err => {
          console.error('API error:', err);
          if (source) {
            source.appendChild(element);
          }
        });
      }
    });
  }
}

Hooks.CopyUrl = {
  mounted() {
    console.log("Mounted CopyUrl hook");
    const btn = this.el.querySelector("#copy-url-btn");
    const urlSpan = this.el.querySelector("#copied-url");
    const checkMark = this.el.querySelector("#url-copied");
    
    /*urlSpan.textContent = window.location.href;*/
    btn.addEventListener("click", () => {
      const url = urlSpan.value;
      navigator.clipboard.writeText(url).then(() => {
        checkMark.classList.remove("hidden");
      });
    });
  }
}

Hooks.PersistPlayerSession = {
  mounted() {
    void syncPlayerSession(this.el);
  },

  updated() {
    void syncPlayerSession(this.el);
  }
}

Hooks.ExchangePlayerCapability = {
  mounted() {
    this.handleEvent('exchange-player-capability', ({ capability }) => {
      void exchangePlayerCapability(capability);
    });
  }
}

let csrfToken = document.querySelector("meta[name='csrf-token']").getAttribute("content")
let liveSocket = new LiveSocket("/live", Socket, {
  longPollFallbackMs: location.host.startsWith("localhost") ? undefined : 2500, // Clients can switch to longpoll and get stuck during development when the server goes up and down
  params: {_csrf_token: csrfToken}, hooks: Hooks
})

// Show progress bar on live navigation and form submits
topbar.config({barColors: {0: "#29d"}, shadowColor: "rgba(0, 0, 0, .3)"})
window.addEventListener("phx:page-loading-start", _info => topbar.show(300))
window.addEventListener("phx:page-loading-stop", _info => topbar.hide())

// connect if there are any LiveViews on the page
liveSocket.connect()

// expose liveSocket on window for web console debug logs and latency simulation:
// >> liveSocket.enableDebug()
// >> liveSocket.enableLatencySim(1000)  // enabled for duration of browser session
// >> liveSocket.disableLatencySim()
window.liveSocket = liveSocket

