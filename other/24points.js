
var cards = ['', 'A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K'];

var players = function() {/*
belongcai
jiongsca
caster
cymurus
*/}.toString().split('\n').slice(1, -1).map(function(name) { return name.trim(); });

var len = cards.length;
var MAX_CARD_COUNT = 4;

players.map(function dealCards(name) {
  var playersCards = [];
  do {
    var count = {};
    var card;
    do {
      card = cards[(Math.random() * (len - 1)).toFixed(0)];
    } while( typeof(count[card]) !== 'undefined' || count[card] >= MAX_CARD_COUNT );
    playersCards.push(card);
    count[card] = count[card] + 1 || 1;
  } while( playersCards.length !== 4 );
  return [name, playersCards.sort(function(a, b) { return a - b; }).join('\t')].join(':\t');
}).forEach(function(row) { console.log(row); });