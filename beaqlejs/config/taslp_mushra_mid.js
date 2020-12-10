// configure the test here
var TestConfig = {
  "TestName": "Mushra Test",
  "RateScalePng": "img/scale_abs.png",
  "RateScaleBgPng": "img/scale_abs_background.png",
  "RateMinValue": 0,
  "RateMaxValue": 100,
  "RateDefaultValue":100,
  "ShowFileIDs": false,
  "ShowResults": false,
  "LoopByDefault": true,
  "EnableABLoop": true,
  "EnableOnlineSubmission": true,
  "BeaqleServiceURL": "beaqleJS_Service.php",
  "SupervisorContact": "zhenk@iu.edu",
  "RandomizeTestOrder": false,
  "MaxTestsPerRun": 10,
  "RequireMaxRating": false,
  "AudioRoot": "/taslp-samples",
  "Testsets": [
    //
    {
  "Name": "Session-II (Mid Bitrates)",
  "TestID": "id1_1",
  "Files": {
        "Reference":"/d/DR5-MRWS1-SX410.wav" ,
        "1":"/d/DR5-MRWS1-SX410.wav",
        "2":"/k/DR5-MRWS1-SX410.wav",
        "3":"/2/DR5-MRWS1-SX410.wav",
        "4":"/f/DR5-MRWS1-SX410.wav",
        "5":"/c/DR5-MRWS1-SX410.wav",
    }
}
  ]
}
