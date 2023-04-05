import { F1TelemetryClient } from "f1-2021-udp";
import {KinesisClient,PutRecordCommand} from '@aws-sdk/client-kinesis'

const kinesis = new KinesisClient({ 
  region: "ap-south-1",
 
});


/*
*   'port' is optional, defaults to 20777

*   'bigintEnabled' is optional, defaults to true
     setting it to false makes the parser skip bigint values

*   'binaryButtonFlags' is optional, defaults to false
     setting it to true makes the parser return an object 
     with a binary flag for every button

*   'forwardAddresses' is optional, defaults to undefined
    it's an array of Address objects to forward unparsed telemetry to.
    each address object is comprised of a port and an optional ip address

*   'skipParsing' is optional, defaults to false
    setting it to true will make the client not parse and emit content.
    You can consume telemetry data using forwardAddresses instead.              
*/

const streamName = 'grande-strategia';
const client = new F1TelemetryClient({binaryButtonFlags: false});


client.start();

// motion 0
// client.on('motion',function(data) {
//     console.log(data);
// })

// // session 1
// client.on('session',function(data) {
//     console.log(data);
// })

// lap data 2
    client.on('lapData',function(data) {
      console.log(data.m_lapData[data.m_header.m_playerCarIndex].m_lapDistance);
      const record = {
        Data2: Buffer.from(JSON.stringify(data.m_lapData[data.m_header.m_playerCarIndex])),
        PartitionKey: 'Lapdata'
      };
      const params = {
        Data: record.Data2,
        StreamName: streamName,
        PartitionKey: record.PartitionKey
      };
      const command = new PutRecordCommand(params);
      kinesis.send(command)
    })
// event 3
// client.on('event',function(data) {
//     console.log(data);
// })

// participants 4
// client.on('participants',function(data) {
//     console.log(data);
// })

// // car setup 5
// client.on('carSetups',function(data) {
//     console.log(data);
// })

// car telemetry 6
client.on('carTelemetry', function(data) {
  const record = {
    Data: Buffer.from(JSON.stringify(data.m_carTelemetryData[data.m_header.m_playerCarIndex])),
    PartitionKey: 'Car-1'
  };
  const params = {
    Data: record.Data,
    StreamName: streamName,
    PartitionKey: record.PartitionKey
  };
  const command = new PutRecordCommand(params);

  kinesis.send(command)
    .then((data) => {
      // console.log(`Data sent to Kinesis Data Stream:`);
    })
    .catch((error) => {
      console.log(`Error sending data to Kinesis Data Stream: ${error}`);
    });
});

// // car status 7
// client.on('carStatus',function(data) {
//     console.log(data);
// })

// // final classification 8
// client.on('finalClassification',function(data) {
//     console.log(data);
// })

// lobby info 9
// client.on('lobbyInfo',function(data) {
//     console.log(data);
// })

// // car damage 10
// client.on('carDamage',function(data) {
//     console.log(data);
// })

// session history 11
// client.on('sessionHistory',function(data) {
//     console.log(data);
// })


// to start listening:

// and when you want to stop:
// client.stop();
// import { F1TelemetryClient } from "f1-2021-udp";

// const client = new F1TelemetryClient({
//   ip: "0.0.0.0", // listen on all available interfaces
//   port: 20777,
// });

// client.start();

// client.on("carTelemetry", function (data) {
//   console.log(data.m_carTelemetryData[data.m_header.m_playerCarIndex]);
// });

// ...
