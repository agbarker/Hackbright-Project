PitchDetector.start = () => {
  const {Audio, Piano} = PitchDetector;

  // build refs object
  const refEls = document.querySelectorAll('[data-ref]');
  PitchDetector.refs = {};
  for (let refEl of refEls) {
    const ref = refEl.getAttribute('data-ref'); // dataset doesn't work on <svg>
    PitchDetector.refs[ref] = refEl;
  }


  const piano = new Piano();
  piano.render();

  // build the refs after rendering the piano
  PitchDetector.refManager = new PitchDetector.RefManager();
  PitchDetector.refManager.getRefs();

  console.log("Checkpoint 1")
  const audio = new Audio;
  audio.start();
};