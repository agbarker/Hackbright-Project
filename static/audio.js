(function()	{
	class Audio	{
		constructor()	{
			this.pitchSamples = new PitchDetector.MusicArray();
		}

		drawPitchMarkers(canvas2Context)	{
			canvas2Context.fillStyle = 'firebrick';
			canvas2Context.font = '14px serif';
			for (let i = 25; i < 1200; i += 25)	{
				const pos = i /2;
				canvas2Context.fillRect(65, pos, 4, 1);
				canvas2Context.fillText(i.toString(), 70, pos + 5);
			}
		}


		start()	{
			const {refs, KEYS} = PitchDetector;
			let audioReady = false;
			let loudEnough = false;
			const MIN_VOLUME = 5;

			const ref = document.location.pathname.replace(/^\//, '');

			const audioContext = new window.AudioContext();
			let audioEl = refs[ref] || document.querySelector('audio');
			const analyser = audioContext.createAnalyser();

			const {sampleRate} = audioContext;

			analyser.fftSize = 2048;
			analyser.minDecibels = -90;
			analyser.maxDecibels = -10;
			const bufferLength = analyser.frequencyBinCount;
			const dataArray = new Uint8Array(bufferLength);

			const canvasContext = refs.canvas.getContext('2d');

			const userMediaConstraints = {audio: true};

			const getUserMediaSuccess = stream => {
				const audioSource = audioContext.createMediaStreamSource(stream);
				refs.mic_audio.src = audioSource;

				audioSource.connect(analyser);
				audioReady = true;
			};

			const getUserMediaError = err => {
				err && console.error(err);
			};

			navigator.getUserMedia(userMediaConstraints, getUserMediaSuccess, getUserMediaError);

			let lastItem = 0;
			const STEPS_THRESHOLD = 5;

			const getKey = () => {
				const pitch = this.pitchSamples.mode;
				let closestLower = KEYS[0];
				let closestHigher = KEYS[KEYS.length - 1];

				for (var i = 0; i < KEYS.length; i++)	{
					if (KEYS[i].hz < pitch) closestLower = KEYS[i];
					if (KEYS[i].hz > pitch)	{
						closestHigher = KEYS[i];
						break;
					}
				}

				const distanceToLower = Math.abs(pitch - closestLower.hz);
				const distanceToHigher = Math.abs(pitch - closestHigher.hz);

				return Math.min(distanceToLower, distanceToHigher) === distanceToLower
					? closestLower
					: closestHigher;
			};


			const renderKey = key => {
			  const keyEls = document.querySelectorAll('[piano-key]');

			  for (let keyEl of keyEls) {
			    keyEl.style.fill = '';
			    keyEl.classList.remove('piano-key--lit');
			  }

			  const pressedKeyEl = SP_APP.refs[`key_${key.pos}`];
			  pressedKeyEl.classList.add('piano-key--lit');
			};


			const drawWave = () => {
				if (!loudEnough) return;
				canvasContext.fillStyle = 'firebrick';
				analyser.getByteTimeDomainData(dataArray);
				canvasContext.fillRect(0, 128, 1024, 2);

				let lastPos = 0;
				dataArray.forEach((item, i) => {
					if (i > 0 && i < dataArray.length && item > 128 && lastItem <= 128)	{
						const elapsedSteps = i - lastPos;
						lastPos = i;

						if (elapsedSteps > STEPS_THRESHOLD)	{
							const hertz = 1 / (elapsedSteps / sampleRate);
							this.pitchSamples.push(hertz);
						}
					}

					canvasContext.fillRect(i, item, 2, 2);

					lastItem = item;
				});
			};

			const drawFreq = () =>	{
				canvasContext.fillStyle = 'lightgray';
				analyser.getByteFrequencyData(dataArray);
				let volumeTotal = 0;
				canvasContext.fillRect(0, (300 - (256 / 10)), 1024, 1);

				dataArray.forEach((item, i) =>	{
					canvasContext.fillRect(i, 300 - item, 1, item);
					volumeTotal += item;
				});

				const volume = volumeTotal / dataArray.length;
		        const nowLoudEnough = volume > MIN_VOLUME;

		        if (loudEnough !== nowLoudEnough) {
		          this.pitchSamples.empty();
		        }

		        loudEnough = nowLoudEnough;
		        refs.db.textContent = volume;
			};

			const renderAudio = () => {
	        requestAnimationFrame(renderAudio);

	        if (!audioReady) return;

	        canvasContext.clearRect(0, 0, 1024, 300);

	        drawFreq();
	        drawWave();
	      };

	      renderAudio();

	      
	      var interval = setInterval(() => {
	      	console.log('hi! loudEnough:', loudEnough);
	        loudEnough && getKey();
	        
	      }, 250);

	      window.addEventListener('keydown', e => {
	        if (e.keyCode === 32) { // space
	          audioEl.paused ? audioEl.play() : audioEl.pause();
	        }
	      });

	      audioEl.play();

		}

		
	}

	PitchDetector.Audio = Audio;

})()

// let audio = new Audio();
// audio.start()