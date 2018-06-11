
(function() {
  class RefManager {
    getRefs() {
      const refEls = document.querySelectorAll('[data-ref]');
      PitchDetector.refs = {};
      for (let refEl of refEls) {
        const ref = refEl.getAttribute('data-ref'); // dataset doesn't work on <svg>
        PitchDetector.refs[ref] = refEl;
      }
    }
  }

  PitchDetector.RefManager = RefManager;
})();



// <script>var PitchDetector = {};</script>

  // <script src="static/constants.js"></script>
  // <script src="static/piano.js"></script>
  // <script src="static/start.js"></script>
  // <script src="static/refManager.js"></script>
  // <script src="static/musicArray.js"></script>
  // <script src="static/audio.js"></script>
  