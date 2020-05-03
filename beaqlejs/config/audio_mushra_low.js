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
  "MaxTestsPerRun": 13,
  "RequireMaxRating": false,
  "AudioRoot": "audio/SPL-V3-L/",
  "Testsets": [
    //
    {
  "Name": "Session-I (Low Bitrates)",
  "TestID": "id1_1",
  "Files": {
        "Reference": "/ref_framed/0444-00001-TMD.wav",
        "1": "model_a_64_framed/0444-00001-TMD.wav",
        "2": "model_c_64_framed/0444-00001-TMD.wav",
        "3": "model_d_64_framed/0444-00001-TMD.wav",
        "4": "model_b_79_framed/0444-00001-TMD.wav",
        "5": "model_a_79_framed/0444-00001-TMD.wav",
        "6": "lp_3p5_framed/0444-00001-TMD.wav",
        "7": "mp3_64_framed/0444-00001-TMD.wav",
    }
},
{
  "Name": "Session-I (Low Bitrates)",
  "TestID": "id1_1",
  "Files": {
        "Reference": "/ref_framed/1684-00001-AMD.wav",
        "1": "model_a_64_framed/1684-00001-AMD.wav",
        "2": "model_c_64_framed/1684-00001-AMD.wav",
        "3": "model_d_64_framed/1684-00001-AMD.wav",
        "4": "model_b_79_framed/1684-00001-AMD.wav",
        "5": "model_a_79_framed/1684-00001-AMD.wav",
        "6": "lp_3p5_framed/1684-00001-AMD.wav",
        "7": "mp3_64_framed/1684-00001-AMD.wav",
    }
},{
  "Name": "Session-I (Low Bitrates)",
  "TestID": "id1_1",
  "Files": {
        "Reference": "/ref_framed/0753-00001-PMO.wav",
        "1": "model_a_64_framed/0753-00001-PMO.wav",
        "2": "model_c_64_framed/0753-00001-PMO.wav",
        "3": "model_d_64_framed/0753-00001-PMO.wav",
        "4": "model_b_79_framed/0753-00001-PMO.wav",
        "5": "model_a_79_framed/0753-00001-PMO.wav",
        "6": "lp_3p5_framed/0753-00001-PMO.wav",
        "7": "mp3_64_framed/0753-00001-PMO.wav",
    }
},{
  "Name": "Session-I (Low Bitrates)",
  "TestID": "id1_1",
  "Files": {
        "Reference": "/ref_framed/0021-00001-RMD.wav",
        "1": "model_a_64_framed/0021-00001-RMD.wav",
        "2": "model_c_64_framed/0021-00001-RMD.wav",
        "3": "model_d_64_framed/0021-00001-RMD.wav",
        "4": "model_b_79_framed/0021-00001-RMD.wav",
        "5": "model_a_79_framed/0021-00001-RMD.wav",
        "6": "lp_3p5_framed/0021-00001-RMD.wav",
        "7": "mp3_64_framed/0021-00001-RMD.wav",
    }
},{
  "Name": "Session-I (Low Bitrates)",
  "TestID": "id1_1",
  "Files": {
        "Reference": "/ref_framed/1656-00003-HMD.wav",
        "1": "model_a_64_framed/1656-00003-HMD.wav",
        "2": "model_c_64_framed/1656-00003-HMD.wav",
        "3": "model_d_64_framed/1656-00003-HMD.wav",
        "4": "model_b_79_framed/1656-00003-HMD.wav",
        "5": "model_a_79_framed/1656-00003-HMD.wav",
        "6": "lp_3p5_framed/1656-00003-HMD.wav",
        "7": "mp3_64_framed/1656-00003-HMD.wav",
    }
},{
  "Name": "Session-I (Low Bitrates)",
  "TestID": "id1_1",
  "Files": {
        "Reference": "/ref_framed/0585-00002-EMO.wav",
        "1": "model_a_64_framed/0585-00002-EMO.wav",
        "2": "model_c_64_framed/0585-00002-EMO.wav",
        "3": "model_d_64_framed/0585-00002-EMO.wav",
        "4": "model_b_79_framed/0585-00002-EMO.wav",
        "5": "model_a_79_framed/0585-00002-EMO.wav",
        "6": "lp_3p5_framed/0585-00002-EMO.wav",
        "7": "mp3_64_framed/0585-00002-EMO.wav",
    }
},{
  "Name": "Session-I (Low Bitrates)",
  "TestID": "id1_1",
  "Files": {
        "Reference": "/ref_framed/0646-00001-CFD.wav",
        "1": "model_a_64_framed/0646-00001-CFD.wav",
        "2": "model_c_64_framed/0646-00001-CFD.wav",
        "3": "model_d_64_framed/0646-00001-CFD.wav",
        "4": "model_b_79_framed/0646-00001-CFD.wav",
        "5": "model_a_79_framed/0646-00001-CFD.wav",
        "6": "lp_3p5_framed/0646-00001-CFD.wav",
        "7": "mp3_64_framed/0646-00001-CFD.wav",
    }
},{
  "Name": "Session-I (Low Bitrates)",
  "TestID": "id1_1",
  "Files": {
        "Reference": "/ref_framed/1110-00001-JNO.wav",
        "1": "model_a_64_framed/1110-00001-JNO.wav",
        "2": "model_c_64_framed/1110-00001-JNO.wav",
        "3": "model_d_64_framed/1110-00001-JNO.wav",
        "4": "model_b_79_framed/1110-00001-JNO.wav",
        "5": "model_a_79_framed/1110-00001-JNO.wav",
        "6": "lp_3p5_framed/1110-00001-JNO.wav",
        "7": "mp3_64_framed/1110-00001-JNO.wav",
    }
},{
  "Name": "Session-I (Low Bitrates)",
  "TestID": "id1_1",
  "Files": {
        "Reference": "/ref_framed/0516-00001-SMD.wav",
        "1": "model_a_64_framed/0516-00001-SMD.wav",
        "2": "model_c_64_framed/0516-00001-SMD.wav",
        "3": "model_d_64_framed/0516-00001-SMD.wav",
        "4": "model_b_79_framed/0516-00001-SMD.wav",
        "5": "model_a_79_framed/0516-00001-SMD.wav",
        "6": "lp_3p5_framed/0516-00001-SMD.wav",
        "7": "mp3_64_framed/0516-00001-SMD.wav",
    }
},{
  "Name": "Session-I (Low Bitrates)",
  "TestID": "id1_1",
  "Files": {
        "Reference": "/ref_framed/0616-00001-GXD.wav",
        "1": "model_a_64_framed/0616-00001-GXD.wav",
        "2": "model_c_64_framed/0616-00001-GXD.wav",
        "3": "model_d_64_framed/0616-00001-GXD.wav",
        "4": "model_b_79_framed/0616-00001-GXD.wav",
        "5": "model_a_79_framed/0616-00001-GXD.wav",
        "6": "lp_3p5_framed/0616-00001-GXD.wav",
        "7": "mp3_64_framed/0616-00001-GXD.wav",
    }
},{
  "Name": "Session-I (Low Bitrates)",
  "TestID": "id1_1",
  "Files": {
        "Reference": "/ref_framed/0446-00002-KMD.wav",
        "1": "model_a_64_framed/0446-00002-KMD.wav",
        "2": "model_c_64_framed/0446-00002-KMD.wav",
        "3": "model_d_64_framed/0446-00002-KMD.wav",
        "4": "model_b_79_framed/0446-00002-KMD.wav",
        "5": "model_a_79_framed/0446-00002-KMD.wav",
        "6": "lp_3p5_framed/0446-00002-KMD.wav",
        "7": "mp3_64_framed/0446-00002-KMD.wav",
    }
},{
  "Name": "Session-I (Low Bitrates)",
  "TestID": "id1_1",
  "Files": {
        "Reference": "/ref_framed/2009-00003-BMD.wav",
        "1": "model_a_64_framed/2009-00003-BMD.wav",
        "2": "model_c_64_framed/2009-00003-BMD.wav",
        "3": "model_d_64_framed/2009-00003-BMD.wav",
        "4": "model_b_79_framed/2009-00003-BMD.wav",
        "5": "model_a_79_framed/2009-00003-BMD.wav",
        "6": "lp_3p5_framed/2009-00003-BMD.wav",
        "7": "mp3_64_framed/2009-00003-BMD.wav",
    }
},{
  "Name": "Session-I (Low Bitrates)",
  "TestID": "id1_1",
  "Files": {
        "Reference": "/ref_framed/1920-00003-LFD.wav",
        "1": "model_a_64_framed/1920-00003-LFD.wav",
        "2": "model_c_64_framed/1920-00003-LFD.wav",
        "3": "model_d_64_framed/1920-00003-LFD.wav",
        "4": "model_b_79_framed/1920-00003-LFD.wav",
        "5": "model_a_79_framed/1920-00003-LFD.wav",
        "6": "lp_3p5_framed/1920-00003-LFD.wav",
        "7": "mp3_64_framed/1920-00003-LFD.wav",
    }
},
  ]
}
