/*
 * Javascript to construct the homepage 
 */

/* 
 * Add a card for each game that looks like:
      <a href="Snungeon/index.html">
      	<div class="game-card">
          <img src="Snungeon/screenshot.png" class="game-img">
          <h4>Snungeon</h4>
          <div class="byline">Ardent Eliot Reinhard / Cam Miller / Cecil Choi</div>
      	</div>
      </a>

    in id "game-container"
 */
function makeGameCards () {
	games = shuffle(games)

	// For each game 
	for (let game of games) {

		if (game["dir"]) {
			
			var link = $('<a href="' + game["dir"] + '/index.html"></a>');
			var card = $('<div></div>').addClass('game-card');

			link.append(card);
	
			card.append ($('<img class="game-img" src="' + game["dir"] + '/screenshot.png">'));
		
			card.append ($('<h4>' + game['name'] + '</h4>'));
			card.append ($('<div class="byline">' + game['authors'].join(' / ') + '</div>'));
	
			$('#game-container').append(link);
		}
	}

}


/* 
 * When the document is fully loaded
 */
$(window).on ("load", function () {
    makeGameCards();
    DataWrangler.init();

 //    let magicGrid = new MagicGrid({
	// 	container: "#game-container", // Required. Can be a class, id, or an HTMLElement.
	// 	items: 35, // Required for dynamic content.
	// 	animate: true, // Optional.
	// });

	// magicGrid.listen();
	// magicGrid.positionItems();

	// $('#game-container').imagesLoaded()
 //  		.always( function( instance ) {
 //    		magicGrid.listen();
	// 		magicGrid.positionItems();
 //  		})

});

function shuffle(array) {
  var currentIndex = array.length, temporaryValue, randomIndex;

  // While there remain elements to shuffle...
  while (0 !== currentIndex) {

    // Pick a remaining element...
    randomIndex = Math.floor(Math.random() * currentIndex);
    currentIndex -= 1;

    // And swap it with the current element.
    temporaryValue = array[currentIndex];
    array[currentIndex] = array[randomIndex];
    array[randomIndex] = temporaryValue;
  }

  return array;
};

