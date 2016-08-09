var SerialPort = require('serialport');

var port = new SerialPort('/dev/ttyACM1', {
  parser: SerialPort.parsers.readline('\n')
});

port.on('data', function (data) {

    // Include the File System module (https://nodejs.org/api/fs.html)
    var fs = require('fs');

    fs.appendFile('./data/data.csv', data, function(err) {

        if(err) {
            return console.log(err);
        }

    });

});
