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
import { Socket } from "phoenix"
import { LiveSocket } from "phoenix_live_view"
import topbar from "../vendor/topbar"
import dragula from "../vendor/dragula"

let Hooks = {}
Hooks.DragDrop = {
  mounted() {
    const MAX_DIST = 80;
    const ELASTIC_POWER = 0.55;
    const BOUNCE_DURATION = 500;

    function lerp(a, b, t) {
      return a + (b - a) * t;
    }

    function applyElastic(dx, dy) {
      const dist = Math.sqrt(dx * dx + dy * dy);
      if (dist === 0) return { x: 0, y: 0 };
      const stretched = Math.min(Math.pow(dist, ELASTIC_POWER) * 6, MAX_DIST);
      const ratio = stretched / dist;
      return { x: dx * ratio, y: dy * ratio };
    }

    const drake = dragula([document.querySelector('#hand'), document.querySelector('#table')], {
      invalid: function (el, handle) {
        // Check if card has elastic class and handle elastic behavior
        if (el.classList.contains('card-elastic')) {
          return false; // Allow dragging elastic cards
        }
        // Don't allow dragging cards off of table
        return el.className === 'card-player' || document.querySelector('#round-played');
      },
      accepts: function (el, target, source, sibling) {
        console.log('accepts called', { target: target?.id, source: source?.id });

        // Check if this is an elastic card being dropped on table
        if (el.classList.contains('card-elastic') && target && target.id === 'table') {
          console.log('Elastic card dropped on table - will bounce back');
          return false; // Prevent dropping elastic cards on table
        }

        // Only allow dropping on table for normal cards
        if (target && target.id === 'table') {
          // Check if "Your Card" section already has a card (not placeholder)
          const yourCardSection = Array.from(document.querySelectorAll('#table .card-player')).find(zone => {
            const nameDiv = zone.querySelector('.name');
            return nameDiv && (nameDiv.textContent.includes('Your Card') || nameDiv.textContent.includes('Drop a card'));
          });

          if (yourCardSection) {
            // Check if there's a card already (not placeholder)
            const isPlaceholder = yourCardSection.textContent.includes('Drop a card');

            console.log('Your card section check:', { isPlaceholder });

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

    // Add elastic behavior to cards with card-elastic class
    const setupElasticCard = (card) => {
      if (!card || !card.classList.contains('card-elastic')) return;

      let dragState = {
        dragging: false,
        startX: 0,
        startY: 0,
        rafId: null,
        currentPos: { x: 0, y: 0 },
        originalTransform: card.style.transform || ''
      };

      const onPointerDown = (e) => {
        e.preventDefault();
        e.stopPropagation();

        const ds = dragState;
        if (ds.rafId) cancelAnimationFrame(ds.rafId);

        ds.dragging = true;
        ds.startX = e.clientX;
        ds.startY = e.clientY;

        card.classList.add('dragging');
        card.style.zIndex = '1000';
      };

      const onPointerMove = (e) => {
        const ds = dragState;
        if (!ds.dragging) return;

        const { x, y } = applyElastic(e.clientX - ds.startX, e.clientY - ds.startY);
        ds.currentPos = { x, y };

        card.style.transform = `translate(${x}px, ${y}px)`;
      };

      const onPointerUp = () => {
        const ds = dragState;
        if (!ds.dragging) return;

        ds.dragging = false;
        card.classList.remove('dragging');
        card.classList.add('bouncing');

        const startPos = { ...ds.currentPos };
        const start = Date.now();

        const animate = () => {
          const t = Math.min((Date.now() - start) / BOUNCE_DURATION, 1);
          const eased = 1 - Math.pow(1 - t, 4) * Math.cos(t * Math.PI * 3.8);
          const newPos = {
            x: lerp(startPos.x, 0, eased),
            y: lerp(startPos.y, 0, eased)
          };

          ds.currentPos = newPos;
          card.style.transform = `translate(${newPos.x}px, ${newPos.y}px)`;

          if (t < 1) {
            ds.rafId = requestAnimationFrame(animate);
          } else {
            card.style.transform = ds.originalTransform;
            card.classList.remove('bouncing');
            card.style.zIndex = '';
          }
        };

        ds.rafId = requestAnimationFrame(animate);
      };

      card.addEventListener('pointerdown', onPointerDown);
      card.addEventListener('pointermove', onPointerMove);
      card.addEventListener('pointerup', onPointerUp);
      card.addEventListener('pointercancel', onPointerUp);
      card.addEventListener('mouseleave', onPointerUp);
    };

    // Set up elastic behavior for existing cards
    document.querySelectorAll('#hand .card-elastic').forEach(setupElasticCard);

    // Watch for new cards being added
    const observer = new MutationObserver((mutations) => {
      mutations.forEach((mutation) => {
        mutation.addedNodes.forEach((node) => {
          if (node.nodeType === 1 && node.classList && node.classList.contains('card-elastic')) {
            setupElasticCard(node);
          }
        });
      });
    });

    observer.observe(document.querySelector('#hand'), {
      childList: true,
      subtree: true
    });

    drake.on('drop', (element, target, source, sibling) => {
      console.log('Drop event', { target: target?.id });

      if (target && target.id === 'table') {
        fetch('/api/games/' + element.dataset.game + '/players/' + element.dataset.player + '/card', {
          method: 'PUT',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({
            dealt_card_id: element.dataset.dealtcard
          })
        }).then(response => {
          console.log('API response:', response.ok);
          return response.ok;
        }).catch(err => {
          console.error('API error:', err);
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

let csrfToken = document.querySelector("meta[name='csrf-token']").getAttribute("content")
let liveSocket = new LiveSocket("/live", Socket, {
  longPollFallbackMs: location.host.startsWith("localhost") ? undefined : 2500, // Clients can switch to longpoll and get stuck during development when the server goes up and down
  params: { _csrf_token: csrfToken }, hooks: Hooks
})

// Show progress bar on live navigation and form submits
topbar.config({ barColors: { 0: "#29d" }, shadowColor: "rgba(0, 0, 0, .3)" })
window.addEventListener("phx:page-loading-start", _info => topbar.show(300))
window.addEventListener("phx:page-loading-stop", _info => topbar.hide())

// connect if there are any LiveViews on the page
liveSocket.connect()

// expose liveSocket on window for web console debug logs and latency simulation:
// >> liveSocket.enableDebug()
// >> liveSocket.enableLatencySim(1000)  // enabled for duration of browser session
// >> liveSocket.disableLatencySim()
window.liveSocket = liveSocket

