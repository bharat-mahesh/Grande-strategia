import { F1TelemetryClient } from "f1-2021-udp";
import {KinesisClient,PutRecordCommand} from '@aws-sdk/client-kinesis'

const kinesis = new KinesisClient({ 
  region: "ap-south-1",
  
});
let teammate=19


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
   
   client.on('participants',function(data) {  
     teammate=((data.m_participants.findIndex(x=> x.m_teamId==data.m_participants[19].m_teamId)));
   })
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
      // console.log(data.m_lapData[data.m_header.m_playerCarIndex].m_lapDistance);
      const record_lapMyCar = {
        Data2: Buffer.from(JSON.stringify(data.m_lapData[data.m_header.m_playerCarIndex])),
        PartitionKey: 'Lapdata-1'
      };
      const params_lapMyCar = {
        Data: record_lapMyCar.Data2,
        StreamName: streamName,
        PartitionKey: record_lapMyCar.PartitionKey
      };
      const command_lapMyCar = new PutRecordCommand(params_lapMyCar);

      const record_lapTeammate = {
        Data2: Buffer.from(JSON.stringify(data.m_lapData[teammate])),
        PartitionKey: 'Lapdata-2'
      };
      const params_lapTeammate = {
        Data: record_lapTeammate.Data2,
        StreamName: streamName,
        PartitionKey: record_lapTeammate.PartitionKey
      };
      const command_lapTeammate = new PutRecordCommand(params_lapTeammate);

      kinesis.send(command_lapMyCar)
      kinesis.send(command_lapTeammate)
    })
// event 3
// client.on('event',function(data) {
//     console.log(data);
// })
// participants 4

// // car setup 5
// client.on('carSetups',function(data) {
//     console.log(data);
// })

// car telemetry 6
client.on('carTelemetry', function(data) {
  // console.log(data.m_carTelemetryData[teammate])
  
  const record_myCar = {
    Data: Buffer.from(JSON.stringify(data.m_carTelemetryData[data.m_header.m_playerCarIndex])),
    PartitionKey: 'Car-1'
  };
  const params_myCar = {
    Data: record_myCar.Data,
    StreamName: streamName,
    PartitionKey: record_myCar.PartitionKey
  };
  const record_teammate = {
    Data: Buffer.from(JSON.stringify(data.m_carTelemetryData[teammate])),
    PartitionKey: 'Car-2'
  };
  const params_teammateCar = {
    Data: record_teammate.Data,
    StreamName: streamName,
    PartitionKey: record_teammate.PartitionKey
  };
  const command_myCar = new PutRecordCommand(params_myCar);
  const command_teammateCar = new PutRecordCommand(params_teammateCar);

  kinesis.send(command_myCar)
    .then((data) => {
      console.log(`My car data sent to Kinesis Data Stream:`);
    })
    .catch((error) => {
      console.log(`Error sending data to Kinesis Data Stream(Self): ${error}`);
    });

    kinesis.send(command_teammateCar)
    .then((data) => {
      console.log(`Teammate data sent to Kinesis Data Stream:`);
    })
    .catch((error) => {
      console.log(`Error sending data to Kinesis Data Stream(TM): ${error}`);
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
