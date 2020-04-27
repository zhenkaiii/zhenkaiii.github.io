// configure the test here
var TestConfig = {
  "TestName": "ABX Demo Test",
  "LoopByDefault": true,
  "ShowFileIDs": false,
  "ShowResults": false,
  "EnableABLoop": true,
  "EnableOnlineSubmission": true,
  "BeaqleServiceURL": "web_service/beaqleJS_Service.php",
  "SupervisorContact": "scwager@indiana.edu",
  "AudioRoot": "audio/",
  "Testsets": [
    //    
    {
      "Name": "Schubert",
      "TestID": "id1",
      "Files": {
        "A": "0.wav",
        "B": "1.wav",
      }
    },
    //    
    {
      "Name": "Castanets",
      "TestID": "id2",
      "Files": {
        "A": "3.wav",
        "B": "4.wav",
      }
    },
  ]
}
