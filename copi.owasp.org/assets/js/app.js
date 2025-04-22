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

let Hooks = {}
Hooks.DragDrop = {
  mounted() {
    dragula([document.querySelector('#hand'), document.querySelector('#table')], {
      invalid: function (el, handle) {
        // Don't allow dragging cards off the table
        return el.className === 'card-player' || document.querySelector('#round-played');
      }
  }).on('drop', (element, target, source, sibling) => {
      if (target.id === 'table') {
        fetch('/api/games/' + element.dataset.game + '/players/' + element.dataset.player + '/card', {
          method: 'PUT',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({
            dealt_card_id: element.dataset.dealtcard
          })
        }).then(response => {
          console.log(response)
    
          if (response.ok) {
            return true;
          }
          else {
            // Need to cancel the drop here
            return false;
          }
        })
      }
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

