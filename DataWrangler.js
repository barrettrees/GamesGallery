/* Singleton DataWrangler class
 * 
 * Interfaces with Loki.js to store, manage, and query data objects
 * 
 */

var DataWrangler = (function () {

	var db, games_db, authors_db;
	
	// Make Lokijs database (with name of file to persist data to)
	//db = new loki('db.json', {
	//	autoload: true,
	//	autoloadCallback : init,
	//	autosave: true, 
	//	autosaveInterval: 4000
	//});

	function init () {
	
		db = new loki('db.json');

		// Add two collections, called 'games' and 'authors', to the database
			// And add a bunch of game documents to the games collection,
			// and authors to the authors collection (both from data.js)
			// (One document = one game or one author)
		if (!db.getCollection('games')) {
			//console.log("Needed to make new games collection")
			games_db = db.addCollection('games');
			games_db.insert(games);
		}
		if (!db.getCollection('authors')) {
			authors_db = db.addCollection('authors');
			authors_db.insert(authors);
		}

		db.saveDatabase();
		
	}
	
	function getAllGames () {
		games_db = db.getCollection('games');

		// Get all games sorted by platform
		return games_db.chain().simplesort("platform").data();
	}
	
	function getGameByName (name) {
		//games_db = db.getCollection('games');

		return games_db.findOne({name: name});
	}

    return { // Public Functions:
        
        init : init,
        getAllGames : getAllGames, 
        getGameByName : getGameByName,
        
        // Returns the unique instance
        // Creates the instance if it doesn't exist yet 
        getInstance : function () {
            if (!instance) {
                instance = createInstance ();
            }
            return instance;
        }

    };
})(); 