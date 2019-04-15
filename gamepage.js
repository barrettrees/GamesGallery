/*
 * Javascript to construct an individual game page (used by each game page) 
 */

function makeGamePage (gamename) {


	console.log ("makeGamePage for ", gamename)

	DataWrangler.init();

	var game = DataWrangler.getGameByName (gamename);

	$('.game-title').text(gamename)
	$('.byline').text(game['authors'].join(' / '))

	if (!game['showSourceDownload']) {
		$(".button.download").remove();
	}

	if (game['description']) {
		$("#game-description").append(game['description']);
	}
}