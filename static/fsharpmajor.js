
// Basic setup boilerplate for using VexFlow with the SVG rendering context:
VF = Vex.Flow;

var div = document.getElementById("fsharp")
var renderer = new VF.Renderer(div, VF.Renderer.Backends.SVG);

renderer.resize(500, 100);
var context = renderer.getContext();


// Create a stave of width 400 at position x10, y40 on the canvas.
var stave = new VF.Stave(10, 0, 400);
// Add a clef and time signature.
stave.addClef("treble").addTimeSignature("4/4");
// Connect it to the rendering context and draw!
stave.setContext(context).draw();

var notes = [
  // A quarter-note C.
  new VF.StaveNote({clef: "treble", keys: ["c/4"], duration: "q" }),

  new VF.StaveNote({clef: "treble", keys: ["d/4"], duration: "q" }),

  new VF.StaveNote({clef: "treble", keys: ["e/4"], duration: "q" }),

  new VF.StaveNote({clef: "treble", keys: ["f/4"], duration: "q" }),

  new VF.StaveNote({clef: "treble", keys: ["g/4"], duration: "q" }),

  new VF.StaveNote({clef: "treble", keys: ["a/4"], duration: "q" }),

  new VF.StaveNote({clef: "treble", keys: ["b/4"], duration: "q" }),

  new VF.StaveNote({clef: "treble", keys: ["c/5"], duration: "q" })  
  
];

// Create a voice in 4/4 and add above notes
var voice = new VF.Voice({num_beats: 8,  beat_value: 4});
voice.addTickables(notes);

// Format and justify the notes to 400 pixels.
var formatter = new VF.Formatter().joinVoices([voice]).format([voice], 300);

// Render voice
voice.draw(context, stave);





    



