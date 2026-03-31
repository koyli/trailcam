import { StubService } from "stub-service";
import { default as axios } from "axios";

// create server instance
const stubService = new StubService();
// start server
await stubService.start(4000);
// configure 

stubService.get("/cmd/standby/reset").reply(200, { "code" : 0 });


stubService.get("/cmd/getSetting").reply(200, { "code": 0,
	                                        "data": {
	                                            "mode":0,
	                                            "language":0,
	                                            "photo_or_video":2,
	                                            "photo_quality":27,
	                                            "multi_shot":1,
	                                            "video_quality":2,
	                                            "video_length":20,
	                                            "exposure_value":0,
	                                            "video_length_night":20,
	                                            "video_sound":1,
	                                            "video_type":0,
	                                            "night_overexpose":0,
	                                            "day_overexpose":3,
	                                            "frame_rate":30,
	                                            "reduce_blur":0,
	                                            "triger_min_interval":20,
	                                            "pir":1,
	                                            "auxiliary_pir":0,
	                                            "timelapse_start":5400,
	                                            "periodic_triger_interval":3600,
	                                            "time_zone":"Europe/London",
	                                            "date_format":2,
	                                            "time_format":1,
	                                            "camera_name":"CAM2",
	                                            "date_stamp":1,
	                                            "sd_override":0,
	                                            "onduty_time":60,
	                                            "offduty_time":60,
	                                            "password":-1,
	                                            "standby_timeout":300,
	                                            "wifi":1,
	                                            "version":5
                                                }
                                              }
                                        );



stubService.get("/list/detail/backward/900000/60").reply(200, {
  "code": 0,
  "data": [
    {
      "id": 134,
      "type": 2,
      "date": "2026-03-29 12:23:12",
      "size": 2437470,
      "uid": "680d5500"
    },
    {
      "id": 133,
      "type": 1,
      "date": "2026-03-29 12:23:11",
      "size": 3286602,
      "uid": "652a22d9"
    },
    {
      "id": 132,
      "type": 1,
      "date": "2026-03-29 12:23:10",
      "size": 3387097,
      "uid": "65991364"
    },
    {
      "id": 131,
      "type": 2,
      "date": "2026-03-28 22:45:35",
      "size": 14524281,
      "uid": "e31f4e75"
    },
    {
      "id": 130,
      "type": 1,
      "date": "2026-03-28 22:45:34",
      "size": 2910248,
      "uid": "a491783c"
    },
    {
      "id": 129,
      "type": 1,
      "date": "2026-03-28 22:45:33",
      "size": 1745817,
      "uid": "387c1ebd"
    },
    {
      "id": 128,
      "type": 2,
      "date": "2026-03-28 22:36:23",
      "size": 17794011,
      "uid": "fc97c226"
    },
    {
      "id": 127,
      "type": 1,
      "date": "2026-03-28 22:36:22",
      "size": 3674715,
      "uid": "16fb0b59"
    },
    {
      "id": 126,
      "type": 1,
      "date": "2026-03-28 22:36:21",
      "size": 3307076,
      "uid": "c36bde65"
    },
    {
      "id": 125,
      "type": 2,
      "date": "2026-03-28 22:35:19",
      "size": 17843757,
      "uid": "bc5e7db1"
    },
    {
      "id": 124,
      "type": 1,
      "date": "2026-03-28 22:35:18",
      "size": 3611196,
      "uid": "6c9fb34a"
    },
    {
      "id": 123,
      "type": 1,
      "date": "2026-03-28 22:35:17",
      "size": 3286203,
      "uid": "4f4ebbd2"
    },
    {
      "id": 122,
      "type": 2,
      "date": "2026-03-28 22:33:34",
      "size": 18900952,
      "uid": "a8c49687"
    },
    {
      "id": 121,
      "type": 1,
      "date": "2026-03-28 22:33:33",
      "size": 3962390,
      "uid": "cb34532b"
    },
    {
      "id": 120,
      "type": 1,
      "date": "2026-03-28 22:33:32",
      "size": 3733446,
      "uid": "85bbd30e"
    },
    {
      "id": 119,
      "type": 2,
      "date": "2026-03-28 22:29:11",
      "size": 19152562,
      "uid": "9a4f19cc"
    },
    {
      "id": 118,
      "type": 1,
      "date": "2026-03-28 22:29:10",
      "size": 3868746,
      "uid": "02cd497f"
    },
    {
      "id": 117,
      "type": 1,
      "date": "2026-03-28 22:29:09",
      "size": 3382161,
      "uid": "cfcf69e9"
    },
    {
      "id": 116,
      "type": 2,
      "date": "2026-03-28 22:22:00",
      "size": 18803729,
      "uid": "95160690"
    },
    {
      "id": 115,
      "type": 1,
      "date": "2026-03-28 22:21:59",
      "size": 3862322,
      "uid": "71feae5e"
    },
    {
      "id": 114,
      "type": 1,
      "date": "2026-03-28 22:21:58",
      "size": 3450468,
      "uid": "91da6f79"
    },
    {
      "id": 113,
      "type": 2,
      "date": "2026-03-28 22:20:46",
      "size": 19064425,
      "uid": "ded8f662"
    },
    {
      "id": 112,
      "type": 1,
      "date": "2026-03-28 22:20:45",
      "size": 4012363,
      "uid": "fcc6ee92"
    },
    {
      "id": 111,
      "type": 1,
      "date": "2026-03-28 22:20:44",
      "size": 3526148,
      "uid": "ec42b57b"
    },
    {
      "id": 110,
      "type": 2,
      "date": "2026-03-28 22:04:02",
      "size": 19240916,
      "uid": "fbbd577f"
    },
    {
      "id": 109,
      "type": 1,
      "date": "2026-03-28 22:04:01",
      "size": 3985965,
      "uid": "c454a7c7"
    },
    {
      "id": 108,
      "type": 1,
      "date": "2026-03-28 22:04:00",
      "size": 3590660,
      "uid": "4191ff56"
    },
    {
      "id": 107,
      "type": 2,
      "date": "2026-03-28 21:59:57",
      "size": 17991605,
      "uid": "150908de"
    },
    {
      "id": 106,
      "type": 1,
      "date": "2026-03-28 21:59:56",
      "size": 3288399,
      "uid": "be9ace21"
    },
    {
      "id": 105,
      "type": 1,
      "date": "2026-03-28 21:59:55",
      "size": 2611791,
      "uid": "75db0b56"
    },
    {
      "id": 104,
      "type": 2,
      "date": "2026-03-28 21:31:12",
      "size": 10292728,
      "uid": "91b0b055"
    },
    {
      "id": 103,
      "type": 1,
      "date": "2026-03-28 21:31:11",
      "size": 3319324,
      "uid": "41516c63"
    },
    {
      "id": 101,
      "type": 2,
      "date": "2026-03-28 21:30:45",
      "size": 16048176,
      "uid": "ed83d5f8"
    },
    {
      "id": 100,
      "type": 1,
      "date": "2026-03-28 21:30:44",
      "size": 3277236,
      "uid": "a66e1044"
    },
    {
      "id": 99,
      "type": 1,
      "date": "2026-03-28 21:30:43",
      "size": 2912491,
      "uid": "fdbfc9a9"
    },
    {
      "id": 98,
      "type": 2,
      "date": "2026-03-28 21:30:17",
      "size": 15991359,
      "uid": "0bb8cd04"
    },
    {
      "id": 97,
      "type": 1,
      "date": "2026-03-28 21:30:16",
      "size": 3338534,
      "uid": "0412df68"
    },
    {
      "id": 96,
      "type": 1,
      "date": "2026-03-28 21:30:15",
      "size": 3105108,
      "uid": "3b9a2179"
    },
    {
      "id": 95,
      "type": 2,
      "date": "2026-03-28 21:29:51",
      "size": 16211195,
      "uid": "801ce512"
    },
    {
      "id": 94,
      "type": 1,
      "date": "2026-03-28 21:29:50",
      "size": 3259251,
      "uid": "1474b88b"
    }
  ]
});

stubService.get("/cmd/info/1").reply(200, {
  "code": 0,
  "data": {
    "brand": "GardePro",
    "product": "E7",
    "ver": "V6.2.107 MCU V153"
  }
});
stubService.get("/cmd/info/2").reply(200, {
  "code": 0,
  "data": {
    "temperature": 23,
    "voltage": 33,
    "vol_value": 9516,
    "ext_power": 0
  }
});
stubService.get("/cmd/info/3").reply(200, {
  "code": 0,
  "data": {
    "status": 5,
    "total": 249889856,
    "used": 1013184,
    "photo": 89,
    "video": 44
  }
});
stubService.get("/cmd/info/4").reply(200, {
  "code": 0,
  "data": {
    "clock": "2026-03-29 12:36:04",
    "tz": "Europe/London"
  }
});
stubService.get("/cmd/info/5").reply(200, {
  "code": -1
});
stubService.get("/cmd/info/6").reply(200, {
  "code": -1
});
stubService.get("/cmd/getParaSetting").reply(200, {
  "code": 0,
  "para": {
    "mode_menu": 7,
    "photo_quality": 170009128,
    "video_quality": 7,
    "thumbnail_quality": 15,
    "photo_burst": 5,
    "video_len": 300,
    "name_len": 4,
    "side_pir": 0,
    "mic": 1,
    "lang": 1983,
    "md_tl": 1,
    "tl_start": 1,
    "tl_hours": 1,
    "sound_level": 1,
    "video_len_list": [
      3,
      5,
      10,
      15,
      20,
      25,
      30,
      40,
      50,
      60,
      120,
      180,
      300
    ],
    "night_video_len_list": [
      3,
      5,
      10,
      15,
      20,
      25,
      30,
      40,
      50,
      60,
      120,
      180,
      300
    ],
    "pir_delay_list": [
      0,
      5,
      10,
      15,
      20,
      30,
      40,
      50,
      60,
      120,
      180,
      240,
      300,
      360,
      420,
      480,
      540,
      600,
      900,
      1200,
      1500,
      1800,
      2100,
      2400,
      2700,
      3000,
      3300,
      3600
    ],
    "timezone": [
      "US/Alaska",
      "US/Aleutian",
      "US/Arizona",
      "US/Central",
      "US/Eastern",
      "US/East-Indiana",
      "US/Hawaii",
      "US/Indiana-Starke",
      "US/Michigan",
      "US/Mountain",
      "US/Pacific",
      "US/Pacific-New",
      "US/Samoa",
      "Canada/Atlantic",
      "Canada/Central",
      "Canada/Eastern",
      "Canada/Mountain",
      "Canada/Newfoundland",
      "Canada/Pacific",
      "Canada/Saskatchewan",
      "Canada/Yukon",
      "Europe/London",
      "Europe/Paris",
      "Europe/Berlin",
      "Europe/Moscow",
      "Europe/Kirov",
      "Europe/Saratov",
      "Europe/Volgograd",
      "Europe/Rome",
      "Europe/Madrid",
      "Europe/Lisbon",
      "Asia/Tokyo",
      "Asia/Shanghai",
      "Ukraine/Kyiv",
      "Australia/Lord_Howe",
      "Australia/Sydney",
      "Australia/Brisbane",
      "Australia/Adelaide",
      "Australia/Darwin",
      "Australia/Eucla",
      "Australia/Perth",
      "Etc/GMT",
      "Etc/GMT+1",
      "Etc/GMT+2",
      "Etc/GMT+3",
      "Etc/GMT+4",
      "Etc/GMT+5",
      "Etc/GMT+6",
      "Etc/GMT+7",
      "Etc/GMT+8",
      "Etc/GMT+9",
      "Etc/GMT+10",
      "Etc/GMT+11",
      "Etc/GMT+12",
      "Etc/GMT-1",
      "Etc/GMT-2",
      "Etc/GMT-3",
      "Etc/GMT-4",
      "Etc/GMT-5",
      "Etc/GMT-6",
      "Etc/GMT-7",
      "Etc/GMT-8",
      "Etc/GMT-9",
      "Etc/GMT-10",
      "Etc/GMT-11",
      "Etc/GMT-12",
      "Etc/GMT-13",
      "Etc/GMT-14"
    ],
    "country": [
      0,
      0,
      0,
      0,
      0,
      0,
      0,
      0,
      0,
      0,
      0,
      0,
      0,
      1,
      1,
      1,
      1,
      1,
      1,
      1,
      1,
      2,
      3,
      4,
      5,
      5,
      5,
      5,
      6,
      7,
      8,
      9,
      10,
      11,
      13,
      13,
      13,
      13,
      13,
      13,
      13,
      14,
      14,
      14,
      14,
      14,
      14,
      14,
      14,
      14,
      14,
      14,
      14,
      14,
      14,
      14,
      14,
      14,
      14,
      14,
      14,
      14,
      14,
      14,
      14,
      14,
      14,
      14
    ]
  }
});
stubService.get("/media/getIrStatus").reply(200, {
  "code": 0,
  "data": {
    "irStatus": "ir",
    "irPower": 0
  }
});
stubService.post("/cmd/standby/now").reply(200, {});

// stubService.get("/file/{}/{}").reply(200, {});
// stubService.get("/thumb/{}/{}").reply(200, {});

// POST /cmd/delete/134/MP4
                             
// sample tests
// const { data } = await axios.get("http://localhost:4000/api/users/1");
// expect(data).toEqual({ id: 1, name: "John" });
