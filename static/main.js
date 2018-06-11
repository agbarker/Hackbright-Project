'use strict';

var _createClass = function () { function defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } } return function (Constructor, protoProps, staticProps) { if (protoProps) defineProperties(Constructor.prototype, protoProps); if (staticProps) defineProperties(Constructor, staticProps); return Constructor; }; }();

function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

(function () {
  var COLORS = {
    EBONY: 'ebony',
    IVORY: 'ivory'
  };
  var SHIFTS = {
    LEFT: 'LEFT',
    MIDDLE: 'MIDDLE',
    RIGHT: 'RIGHT'
  };

  function getKeyDeets(keyPos) {
    var key = keyPos % 12;
    var shift = void 0;
    var color = void 0;

    if (key === 2 || key === 7) {
      shift = SHIFTS.RIGHT;
      color = COLORS.EBONY;
    } else if (key === 5 || key === 10) {
      shift = SHIFTS.LEFT;
      color = COLORS.EBONY;
    } else if (key === 0) {
      shift = SHIFTS.MIDDLE;
      color = COLORS.EBONY;
    } else {
      shift = null;
      color = COLORS.IVORY;
    }
    return { shift: shift, color: color };
  }

  var Piano = function () {
    function Piano() {
      _classCallCheck(this, Piano);
    }

    _createClass(Piano, [{
      key: 'render',
      value: function render() {
        // key dimensions from http://www.rwgiangiulio.com/construction/manual/
        var _PitchDetector = PitchDetector;
        var KEYS = _PitchDetector.KEYS;
        var refs = _PitchDetector.refs;

        var pianoEl = refs.piano;
        var ns = 'http://www.w3.org/2000/svg';

        var left = 0;
        var blackKeyGroup = document.createElementNS(ns, 'g');
        var whiteKeyGroup = document.createElementNS(ns, 'g');

        KEYS.forEach(function (key) {
          var keyRect = document.createElementNS(ns, 'rect');
          var keyDeets = getKeyDeets(key.pos);
          var x = left;
          var height = 125;
          var width = 22;

          if (keyDeets.color === COLORS.EBONY) {
            height -= 45;
            width = 11;

            if (keyDeets.shift === SHIFTS.LEFT) {
              x = left - 7;
            } else if (keyDeets.shift === SHIFTS.MIDDLE) {
              x = left - 5;
            } else if (keyDeets.shift === SHIFTS.RIGHT) {
              x = left - 3;
            } else {
              console.warn('SHIFT was not set');
            }
          } else {
            left += 22;
            var keyText = document.createElementNS(ns, 'text');
            keyText.textContent = key.pos;

            keyText.setAttribute('x', x + width / 2);
            keyText.setAttribute('y', 10);
            keyText.setAttribute('text-anchor', 'middle');
            whiteKeyGroup.appendChild(keyText);
          }

          keyRect.setAttribute('rx', 2);
          keyRect.setAttribute('x', x);
          keyRect.setAttribute('y', 14);
          keyRect.setAttribute('width', width);
          keyRect.setAttribute('height', height);
          keyRect.setAttribute('data-ref', 'key_' + key.pos);
          keyRect.setAttribute('piano-key', true);
          keyRect.classList.add('piano-key');
          keyRect.classList.add('piano-key--' + keyDeets.color);

          if (keyDeets.color === COLORS.EBONY) {
            blackKeyGroup.appendChild(keyRect);
          } else {
            whiteKeyGroup.appendChild(keyRect);
          }
        });

        pianoEl.appendChild(whiteKeyGroup);
        pianoEl.appendChild(blackKeyGroup);
      }
    }]);

    return Piano;
  }();

  PitchDetector.Piano = Piano;
})();
'use strict';

var _createClass = function () { function defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } } return function (Constructor, protoProps, staticProps) { if (protoProps) defineProperties(Constructor.prototype, protoProps); if (staticProps) defineProperties(Constructor, staticProps); return Constructor; }; }();

function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

(function () {
  var RefManager = function () {
    function RefManager() {
      _classCallCheck(this, RefManager);
    }

    _createClass(RefManager, [{
      key: 'getRefs',
      value: function getRefs() {
        var refEls = document.querySelectorAll('[data-ref]');
        PitchDetector.refs = {};
        var _iteratorNormalCompletion = true;
        var _didIteratorError = false;
        var _iteratorError = undefined;

        try {
          for (var _iterator = refEls[Symbol.iterator](), _step; !(_iteratorNormalCompletion = (_step = _iterator.next()).done); _iteratorNormalCompletion = true) {
            var refEl = _step.value;

            var ref = refEl.getAttribute('data-ref'); // dataset doesn't work on <svg>
            PitchDetector.refs[ref] = refEl;
          }
        } catch (err) {
          _didIteratorError = true;
          _iteratorError = err;
        } finally {
          try {
            if (!_iteratorNormalCompletion && _iterator.return) {
              _iterator.return();
            }
          } finally {
            if (_didIteratorError) {
              throw _iteratorError;
            }
          }
        }
      }
    }]);

    return RefManager;
  }();

  PitchDetector.RefManager = RefManager;
})();
"use strict";

var _createClass = function () { function defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } } return function (Constructor, protoProps, staticProps) { if (protoProps) defineProperties(Constructor.prototype, protoProps); if (staticProps) defineProperties(Constructor, staticProps); return Constructor; }; }();

function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

(function () {
  var SmartArray = function () {
    function SmartArray() {
      _classCallCheck(this, SmartArray);

      this.dataArray = [];
    }

    _createClass(SmartArray, [{
      key: "push",
      value: function push(item) {
        this.dataArray.push(item);
      }
    }, {
      key: "empty",
      value: function empty() {
        this.dataArray.length = 0;
      }
    }, {
      key: "avg",
      get: function get() {
        return this.dataArray.reduce(function (result, time) {
          return result + time;
        }, 0) / this.dataArray.length;
      }
    }, {
      key: "median",
      get: function get() {
        if (!this.dataArray.length) return 0;
        var midPoint = Math.floor(this.dataArray.length / 2);
        return this.dataArray[midPoint];
      }
    }, {
      key: "mode",
      get: function get() {
        if (!this.dataArray.length) return 0;

        var counts = {};
        var mode = null;
        var max = 0;

        this.dataArray.forEach(function (item) {
          var value = Math.round(item * 10) / 10;

          counts[value] = (counts[value] || 0) + 1;

          if (counts[value] > max) {
            max = counts[value];
            mode = value;
          }
        });

        return mode;
      }
    }]);

    return SmartArray;
  }();

  PitchDetector.SmartArray = SmartArray;
})();
'use strict';

var _createClass = function () { function defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } } return function (Constructor, protoProps, staticProps) { if (protoProps) defineProperties(Constructor.prototype, protoProps); if (staticProps) defineProperties(Constructor, staticProps); return Constructor; }; }();

function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

(function () {
  var Audio = function () {
    function Audio() {
      _classCallCheck(this, Audio);

      this.pitchSamples = new PitchDetector.SmartArray();
    }

    _createClass(Audio, [{
      key: 'drawPitchMarkers',
      value: function drawPitchMarkers(canvas2Context) {
        canvas2Context.fillStyle = 'firebrick';
        canvas2Context.font = '14px serif';
        for (var i = 25; i < 1200; i += 25) {
          var pos = i / 2;
          canvas2Context.fillRect(65, pos, 4, 1);
          canvas2Context.fillText(i.toString(), 70, pos + 5);
        }
      }
    }, {
      key: 'start',
      value: function start() {
        var _this = this;

        var _PitchDetector = PitchDetector;
        var refs = _PitchDetector.refs;
        var KEYS = _PitchDetector.KEYS;

        var audioReady = false;
        var loudEnough = false;
        var MIN_VOLUME = 5;

        var ref = document.location.pathname.replace(/^\//, '');

        var audioContext = new window.AudioContext();
        var audioEl = refs[ref] || document.querySelector('audio');
        var analyser = audioContext.createAnalyser();

        var sampleRate = audioContext.sampleRate;


        analyser.fftSize = 2048;
        analyser.minDecibels = -90;
        analyser.maxDecibels = -10;
        var bufferLength = analyser.frequencyBinCount;
        var dataArray = new Uint8Array(bufferLength);

        var canvasContext = refs.canvas.getContext('2d');
        // const canvas2Context = refs.canvas2.getContext('2d');
        // this.drawPitchMarkers(canvas2Context);

        var userMediaConstraints = { audio: true };

        var getUserMediaSuccess = function getUserMediaSuccess(stream) {
          var audioSource = audioContext.createMediaStreamSource(stream);
          refs.mic_audio.src = audioSource;

          audioSource.connect(analyser);
          // comment/uncomment to play to speakers
          // audioSource.connect(audioContext.destination); // out to the speakers
          audioReady = true;
        };

        var getUserMediaError = function getUserMediaError(err) {
          err && console.error(err);
        };

        navigator.getUserMedia(userMediaConstraints, getUserMediaSuccess, getUserMediaError);

        // canvas2Context.fillStyle = 'rgba(0, 0, 0, 0.03)';

        var lastItem = 0;
        var STEPS_THRESHOLD = 5;

        var getKey = function getKey() {
          var pitch = _this.pitchSamples.mode;
          var closestLower = KEYS[0];
          var closestHigher = KEYS[KEYS.length - 1];

          for (var i = 0; i < KEYS.length; i++) {
            if (KEYS[i].hz < pitch) closestLower = KEYS[i];
            if (KEYS[i].hz > pitch) {
              closestHigher = KEYS[i];
              break; // going from low to high so we can stop here
            }
          }

          var distanceToLower = Math.abs(pitch - closestLower.hz);
          var distanceToHigher = Math.abs(pitch - closestHigher.hz);

          return Math.min(distanceToLower, distanceToHigher) === distanceToLower ? closestLower : closestHigher;
        };

        var renderKey = function renderKey() {
          var key = getKey();
          // refs.note.textContent = `That was note number ${key.pos}: ${key.name}`;

          // TODO (davidg): push this out into the Piano class
          var keyEls = document.querySelectorAll('[piano-key]');

          var _iteratorNormalCompletion = true;
          var _didIteratorError = false;
          var _iteratorError = undefined;

          try {
            for (var _iterator = keyEls[Symbol.iterator](), _step; !(_iteratorNormalCompletion = (_step = _iterator.next()).done); _iteratorNormalCompletion = true) {
              var keyEl = _step.value;

              keyEl.style.fill = '';
              keyEl.classList.remove('piano-key--lit');
            }
          } catch (err) {
            _didIteratorError = true;
            _iteratorError = err;
          } finally {
            try {
              if (!_iteratorNormalCompletion && _iterator.return) {
                _iterator.return();
              }
            } finally {
              if (_didIteratorError) {
                throw _iteratorError;
              }
            }
          }

          var pressedKeyEl = PitchDetector.refs['key_' + key.pos];
          pressedKeyEl.classList.add('piano-key--lit');
          // if (keyEl) keyEl.style.fill = '#2196f3';
          _this.pitchSamples.empty();
        };

        var drawWave = function drawWave() {
          if (!loudEnough) return;
          canvasContext.fillStyle = 'firebrick';
          analyser.getByteTimeDomainData(dataArray);
          canvasContext.fillRect(0, 128, 1024, 2);

          var lastPos = 0;
          dataArray.forEach(function (item, i) {
            if (i > 0 && i < dataArray.length && item > 128 && lastItem <= 128) {
              var elapsedSteps = i - lastPos;
              lastPos = i;

              if (elapsedSteps > STEPS_THRESHOLD) {
                var hertz = 1 / (elapsedSteps / sampleRate); // sampleRate = 44100
                _this.pitchSamples.push(hertz);
                // canvas2Context.fillRect(4, hertz / 2, 65, 1); // pitch marker
            }

            canvasContext.fillRect(i, item, 2, 2); // point in the wave

            lastItem = item;
          ;
        };

        var drawFreq = function drawFreq() {
          canvasContext.fillStyle = 'lightgray';
          analyser.getByteFrequencyData(dataArray);
          var volumeTotal = 0;
          canvasContext.fillRect(0, 300 - 256 / 10, 1024, 1);

          dataArray.forEach(function (item, i) {
            canvasContext.fillRect(i, 300 - item, 1, item);
            volumeTotal += item;
          });

          var volume = volumeTotal / dataArray.length;
          var nowLoudEnough = volume > MIN_VOLUME;

          if (loudEnough !== nowLoudEnough) {
            _this.pitchSamples.empty();
          }

          loudEnough = nowLoudEnough;
          refs.db.textContent = volume;
        };

        var renderAudio = function renderAudio() {
          requestAnimationFrame(renderAudio);

          if (!audioReady) return;

          canvasContext.clearRect(0, 0, 1024, 300);

          drawFreq();
          drawWave();
        };

        renderAudio();

        setInterval(function () {
          loudEnough && renderKey();
        }, 250);

        window.addEventListener('keydown', function (e) {
          if (e.keyCode === 32) {
            // space
            audioEl.paused ? audioEl.play() : audioEl.pause();
          }
        });

        audioEl.play();
      })
    };

    return Audio;
  }()

  PitchDetector.Audio = Audio;
})();
'use strict';

PitchDetector.KEYS = [{ pos: 1, hz: 27.5, name: 'A0 Double Pedal A' }, { pos: 2, hz: 29.1352, name: 'A♯0/B♭0' }, { pos: 3, hz: 30.8677, name: 'B0' }, { pos: 4, hz: 32.7032, name: 'C1 Pedal C' }, { pos: 5, hz: 34.6478, name: 'C♯1/D♭1' }, { pos: 6, hz: 36.7081, name: 'D1' }, { pos: 7, hz: 38.8909, name: 'D♯1/E♭1' }, { pos: 8, hz: 41.2034, name: 'E1' }, { pos: 9, hz: 43.6535, name: 'F1' }, { pos: 10, hz: 46.2493, name: 'F♯1/G♭1' }, { pos: 11, hz: 48.9994, name: 'G1' }, { pos: 12, hz: 51.9131, name: 'G♯1/A♭1' }, { pos: 13, hz: 55, name: 'A1' }, { pos: 14, hz: 58.2705, name: 'A♯1/B♭1' }, { pos: 15, hz: 61.7354, name: 'B1' }, { pos: 16, hz: 65.4064, name: 'C2 Deep C' }, { pos: 17, hz: 69.2957, name: 'C♯2/D♭2' }, { pos: 18, hz: 73.4162, name: 'D2' }, { pos: 19, hz: 77.7817, name: 'D♯2/E♭2' }, { pos: 20, hz: 82.4069, name: 'E2' }, { pos: 21, hz: 87.3071, name: 'F2' }, { pos: 22, hz: 92.4986, name: 'F♯2/G♭2' }, { pos: 23, hz: 97.9989, name: 'G2' }, { pos: 24, hz: 103.826, name: 'G♯2/A♭2' }, { pos: 25, hz: 110, name: 'A2' }, { pos: 26, hz: 116.541, name: 'A♯2/B♭2' }, { pos: 27, hz: 123.471, name: 'B2' }, { pos: 28, hz: 130.813, name: 'C3' }, { pos: 29, hz: 138.591, name: 'C♯3/D♭3' }, { pos: 30, hz: 146.832, name: 'D3' }, { pos: 31, hz: 155.563, name: 'D♯3/E♭3' }, { pos: 32, hz: 164.814, name: 'E3' }, { pos: 33, hz: 174.614, name: 'F3' }, { pos: 34, hz: 184.997, name: 'F♯3/G♭3' }, { pos: 35, hz: 195.998, name: 'G3' }, { pos: 36, hz: 207.652, name: 'G♯3/A♭3' }, { pos: 37, hz: 220, name: 'A3' }, { pos: 38, hz: 233.082, name: 'A♯3/B♭3' }, { pos: 39, hz: 246.942, name: 'B3' }, { pos: 40, hz: 261.626, name: 'C4 Middle C' }, { pos: 41, hz: 277.183, name: 'C♯4/D♭4' }, { pos: 42, hz: 293.665, name: 'D4' }, { pos: 43, hz: 311.127, name: 'D♯4/E♭4' }, { pos: 44, hz: 329.628, name: 'E4' }, { pos: 45, hz: 349.228, name: 'F4' }, { pos: 46, hz: 369.994, name: 'F♯4/G♭4' }, { pos: 47, hz: 391.995, name: 'G4' }, { pos: 48, hz: 415.305, name: 'G♯4/A♭4' }, { pos: 49, hz: 440, name: 'A4 A440' }, { pos: 50, hz: 466.164, name: 'A♯4/B♭4' }, { pos: 51, hz: 493.883, name: 'B4' }, { pos: 52, hz: 523.251, name: 'C5 Tenor C' }, { pos: 53, hz: 554.365, name: 'C♯5/D♭5' }, { pos: 54, hz: 587.33, name: 'D5' }, { pos: 55, hz: 622.254, name: 'D♯5/E♭5' }, { pos: 56, hz: 659.255, name: 'E5' }, { pos: 57, hz: 698.456, name: 'F5' }, { pos: 58, hz: 739.989, name: 'F♯5/G♭5' }, { pos: 59, hz: 783.991, name: 'G5' }, { pos: 60, hz: 830.609, name: 'G♯5/A♭5' }, { pos: 61, hz: 880, name: 'A5' }, { pos: 62, hz: 932.328, name: 'A♯5/B♭5' }, { pos: 63, hz: 987.767, name: 'B5' }, { pos: 64, hz: 1046.5, name: 'C6 Soprano C(High C)' }, { pos: 65, hz: 1108.73, name: 'C♯6/D♭6' }, { pos: 66, hz: 1174.66, name: 'D6' }, { pos: 67, hz: 1244.51, name: 'D♯6/E♭6' }, { pos: 68, hz: 1318.51, name: 'E6' }, { pos: 69, hz: 1396.91, name: 'F6' }, { pos: 70, hz: 1479.98, name: 'F♯6/G♭6' }, { pos: 71, hz: 1567.98, name: 'G6' }, { pos: 72, hz: 1661.22, name: 'G♯6/A♭6' }, { pos: 73, hz: 1760, name: 'A6' }, { pos: 74, hz: 1864.66, name: 'A♯6/B♭6' }, { pos: 75, hz: 1975.53, name: 'B6' }, { pos: 76, hz: 2093, name: 'C7 Double high C' }, { pos: 77, hz: 2217.46, name: 'C♯7/D♭7' }, { pos: 78, hz: 2349.32, name: 'D7' }, { pos: 79, hz: 2489.02, name: 'D♯7/E♭7' }, { pos: 80, hz: 2637.02, name: 'E7' }, { pos: 81, hz: 2793.83, name: 'F7' }, { pos: 82, hz: 2959.96, name: 'F♯7/G♭7' }, { pos: 83, hz: 3135.96, name: 'G7' }, { pos: 84, hz: 3322.44, name: 'G♯7/A♭7' }, { pos: 85, hz: 3520, name: 'A7' }, { pos: 86, hz: 3729.31, name: 'A♯7/B♭7' }, { pos: 87, hz: 3951.07, name: 'B7' }, { pos: 88, hz: 4186.01, name: 'C8 Eighth octave' }];
'use strict';

PitchDetector.printNotes = function () {
  var notes = ['a', 'b', 'c'];

  notes.forEach(function (note) {
    console.log('note');
  });
};
'use strict';

PitchDetector.start = function () {
  var _PitchDetector = PitchDetector;
  var Audio = _PitchDetector.Audio;
  var Piano = _PitchDetector.Piano;

  // build refs object

  var refEls = document.querySelectorAll('[data-ref]');
  PitchDetector.refs = {};
  var _iteratorNormalCompletion = true;
  var _didIteratorError = false;
  var _iteratorError = undefined;

  try {
    for (var _iterator = refEls[Symbol.iterator](), _step; !(_iteratorNormalCompletion = (_step = _iterator.next()).done); _iteratorNormalCompletion = true) {
      var refEl = _step.value;

      var ref = refEl.getAttribute('data-ref'); // dataset doesn't work on <svg>
      PitchDetector.refs[ref] = refEl;
    }
  } catch (err) {
    _didIteratorError = true;
    _iteratorError = err;
  } finally {
    try {
      if (!_iteratorNormalCompletion && _iterator.return) {
        _iterator.return();
      }
    } finally {
      if (_didIteratorError) {
        throw _iteratorError;
      }
    }
  }

  var piano = new Piano();
  piano.render();

  // build the refs after rendering the piano
  PitchDetector.refManager = new PitchDetector.RefManager();
  PitchDetector.refManager.getRefs();

  var audio = new Audio();
  audio.start();
};
