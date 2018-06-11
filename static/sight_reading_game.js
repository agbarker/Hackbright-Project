
VF = Vex.Flow;

// Create an SVG renderer and attach it to the DIV element named "boo".
var div = document.getElementById("boo")
var renderer = new VF.Renderer(div, VF.Renderer.Backends.SVG);

// Configure the rendering context.
renderer.resize(500, 500);
var context = renderer.getContext();


var tickContext = new VF.TickContext();


var stave = new VF.Stave(10, 10, 10000)
.addClef('treble');


stave.setContext(context).draw();



var notes = import_notes.map(([letter, acc, octave, duration]) => {
	const note = new VF.StaveNote({
    clef: 'treble',
    keys: [`${letter}${acc}/${octave}`],
    duration: `${duration}`,
  })
  .setContext(context)
  .setStave(stave);


  if(acc) note.addAccidental(0, new VF.Accidental(acc));
	tickContext.addTickable(note)
	return note;
});


tickContext.preFormat().setX(400);

const visibleNoteGroups = [];


lowerCaseCodes = {"a": 97, "b": 98, "c": 99, "d": 100, "e": 101, "f": 102, "g": 103};
upperCaseCodes = {"a": 65, "b": 66, "c": 67, "d": 68, "e": 69, "f": 70, "g": 71};
noteAnswersQueue = [];

numCorrect = 0;
numFail = 0;
numTries = 0;


$(document).ready(function()	{
	$("#startgame").click(startGame)		
});

function startGame()	{
	interval = setInterval(addNote, 1000);
}

function addNote() {
	note = notes.shift();
 	noteAnswersQueue.push(note);
	if(!note) return;
	console.log(note.keys[0][0]);
  const group = context.openGroup();
  visibleNoteGroups.push(group);
	note.draw();
  context.closeGroup();
	group.classList.add('scroll');

  const box = group.getBoundingClientRect();
	group.classList.add('scrolling');

	// If a user doesn't answer in time make the note fall below the staff
	window.setTimeout(() => {
		const index = visibleNoteGroups.indexOf(group);
		if(index === -1) return;
		group.classList.add('too-slow');
    visibleNoteGroups.shift();
    noteAnswersQueue.shift();
    numFail += 1;
    $('#fail').get(0).innerHTML = "Fails: " + numFail;
	}, 5000);
};


$(document).keypress(function(e) {
    var keyCode = e.keyCode;

    note1 = noteAnswersQueue[0];
    

    if(keyCode == lowerCaseCodes[note1.keys[0][0]] || keyCode == upperCaseCodes[note1.keys[0][0]]){
        group = visibleNoteGroups.shift();
  		group.classList.add('correct');
  		noteAnswersQueue.shift();

		const transformMatrix = window.getComputedStyle(group).transform;

		const x = transformMatrix.split(',')[4].trim();

		group.style.transform = `translate(${x}px, -800px)`;
		numCorrect += 1;
		numTries += 1;
		$('#correct').get(0).innerHTML = "Correct: " + numCorrect;
		$('#tries').get(0).innerHTML = "Tries: " + numTries;
    }
    else {
    	numTries += 1;
    	$('#tries').get(0).innerHTML = "Tries: " + numTries;
    }
});


// If a user plays/identifies the note in time, send it up to note heaven.
document.getElementById('boo').addEventListener("keypress", (e) => {
	group = visibleNoteGroups.shift();
  	group.classList.add('correct');

	const transformMatrix = window.getComputedStyle(group).transform;

	const x = transformMatrix.split(',')[4].trim();

	group.style.transform = `translate(${x}px, -800px)`;
})
