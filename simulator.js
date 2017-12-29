// var img = document.querySelector('img');
// img.addEventListener('click', onClick, false);

var ledStrip = document.getElementById("led-strip");
ledStrip.addEventListener('click', onClick, false);
// var i = 0;
var numLed = 5;
var ledOff = 'black.png';
var ledOn = 'red.png';

function onClick() {
		var ledStatesArr = [[0, 0, 0, 0, 1], [0, 0, 0, 1, 1], [0, 0, 1, 1, 1], [0, 1, 1, 1, 1], [1, 1, 1, 1, 1]];
    	// for (j =0; j<5; j++){
    	// 	// var delayTime = delay(2, 5);
    	// 	// setTimeout(rotate(ledStatesArr[j]), delayTime);
    	// 	rotate(ledStatesArr[j]);

    	// }
    	// (async function loop(){
    	// 	for (let i = 0; i<10; i++){
	    // 		let promise = new Promise(
	    // 		(resolve, reject) =>{
	    // 			window.setTimeout(function(){
	    // 				rotate(ledStatesArr[i%5], i);
	    // 				resolve();
	    // 			}, 100*(i+1));
	    // 		});

		   //  	await promise.then(()=> {
		   //  		updateLed(ledStatesArr[i%5]);
		   //  	});
    	// 	}
    	// });

    	var sequence = Promise.resolve();

    	for (let i = 0; i<100; i++){
    		sequence = sequence.then(function(){
    			window.setTimeout(function(){
	    				rotate(ledStatesArr[i%5], i);
	    				console.log('sequence time', 720*(i+1));
	    			}, 720*(i+1));
	    		// rotate(ledStatesArr[i%5], i);

    		}).then(function(){
    			window.setTimeout(function(){
    				updateLed(ledStatesArr[i%5]);
    			},720*(i+1));
    			// updateLed(ledStatesArr[i%5]);
    		});
    	}

		// 	for (let j = 0; len = 10, j< len; j++) {
    	
  //   		setTimeout(function(){
  //   				rotate(ledStatesArr[j%5], j);
  //   			updateLed(ledStatesArr[j%5]);
		// } , 100*j);

}

function rotate(ledStates, j){
	    
	   // console.log(delayTime);
    // 	setTimeout(updateLed(ledStates), delayTime);
    // setTimeout(function(){
    		
	    // i = i+1;
	    //  var deg = 72*i;
	    
	    var maxDeg = 72*(j+1);
	    var deg = 72*j;
	     console.log('max deg', maxDeg);
	     var sequence = Promise.resolve();
	     for (let i =j; i<72+j; i++){
	     	 
	     	 sequence = sequence.then(function(){
	     	 	deg = deg+1;
	     	 	console.log('loop time set', 720*(j+1)+10*i);
	     	 	 window.setTimeout(rotateToAngle(ledStates, deg), 720*(j+1)+10*i);

	     	 })
	     	
	    	
	    }
	   
	    	// setTimeout(function(){
	    	// 	updateLed(ledStates)
	    	// }, 100*j);
    // }, 100*i);
    // updateLed(ledStates);

}
function rotateToAngle(ledStates, deg){
	console.log('set deg', deg);
	ledStrip.removeAttribute('style');	
	     	 var css = '-webkit-transform: rotate(' + deg + 'deg); ';
	    ledStrip.setAttribute(
	        'style', css
	        );
	    console.log(css);
}

// function rotate(ledStates, currentDeg, targetDeg){
// 		deg 
// 		ledStrip.removeAttribute('style');	
// 	     	 var css = '-webkit-transform: rotate(' + deg + 'deg); ';
// 	    ledStrip.setAttribute(
// 	        'style', css
// 	        );
// 	    setTimeout('rotate(\''+ledStates+'\','+currentDeg+'+'\','+targetDeg+')', 100);
// }
function delay(rtime, rdiv){
	return 1000*rtime/rdiv;
}

function updateLed(ledStates){
	console.log(ledStates);
	for (var i = 0; i<numLed; i++){
		var led = document.getElementById('led'+(i+1));
		led.removeAttribute('style');
		var ledState;
		if (ledStates[i] == 1){
			ledState = ledOn;
		}
		else {
			ledState = ledOff;
		}
		var css = 'background-image: url('+ ledState+ ')';
		
		led.setAttribute(
			'style', css
		); 
	}
}
