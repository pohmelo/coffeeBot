//Authorized users array __This is for testing purposes only__
var authorized_users = [];

//Include libraries
var Bot = require('node-telegram-bot');

//Init the telegram bot
var bot = new Bot({
  token: '694049938:AAHrefnNLUWkbO_1EE64JyCySIZnxNvglPI'
});

//Attach on every received message
bot.on('message', function(message){
  parseMessage(message);
});

//Function to get the date and time
function getTime(){
  var d = new Date();
  var date = d.getDate();
  date = (date < 10 ? "0" : "") + date;
  var month = d.getMonth();
  month = (month < 10 ? "0" : "") + month;
  var year = d.getFullYear();
  var hour = d.getHours();
  hour = (hour < 10 ? "0" : "") + hour;
  var min = d.getMinutes();
  min = (min < 10 ? "0" : "") + min;
  return '[' + date + '/' + month + '/' + year + ' ' + hour + ':' + min + ']'
}

//Start the BOT
bot.start();
console.log("The BOT is ON");

//Function that handles the messagess
function parseMessage(message){

  switch(true){

    //Case when /start
    case message.text == "/start":
      bot.sendMessage({
        chat_id: message.chat.id,
        text: 'Authentication pls',
      });
      break;

    //Case when not authenticated
    case message.text != "/authentidrm" && !authenticate(message.from.id):
      bot.sendMessage({
        chat_id: message.chat.id,
        text: 'You are not authorized to use this bot. You need to identicate your user ID',
      });
      break;

    //Case when not authenticated and asking for authentication
    case message.text == "/authentidrm" && !authenticate(message.from.id):
      authorized_users.push(message.from.id);
      bot.sendMessage({
        chat_id: message.chat.id,
        text: 'You can now use the bot, type /coffee to get the current status of the coffee',
      });
      break;

    //Case when authenticated
    case message.text == "/coffee" && authenticate(message.from.id):
      bot.sendMessage({
        chat_id: message.chat.id,
        text: getTime() + " No real implementation yet. There prolly wouldn't be coffee anyway."
        //text: '[' + date + '/' + month + '/' + year + ' ' + hour + ':' + min + '] No real implementation yet. There prolly wouldn\'t be coffee anyway, so.....',
      });
      break;

    case message.text == "/uinfo":
      bot.sendMessage({
        chat_id: message.chat.id,
        text: getTime() + ' User ID: ' + message.from.id + ', name: ' + message.from.first_name + ' ' + message.from.last_name +  '.',
      });
      break;

  }
}

//Function to authenticate the user. ATM designed for testing purposes
function authenticate(userid){

  for(i = 0; i < authorized_users.length; i++){
    if(authorized_users[i] == userid){
      return true;
    }else{
      return false;
    }
  }
}
